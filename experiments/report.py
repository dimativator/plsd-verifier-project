"""Plot study accuracy and cost with family-bootstrap intervals."""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path
from statistics import mean

from experiments.analysis import _bootstrap_clusters, _quantile, run_key

ARMS = ("baseline", "verifier", "guided_verifier")
LABELS = {
    "baseline": "Baseline",
    "verifier": "Optional verifier",
    "guided_verifier": "Instructed verifier",
}
COLORS = {"baseline": "#4B5563", "verifier": "#0072B2", "guided_verifier": "#D55E00"}
COST_FIELDS = ("phase", "model", "task_id", "condition", "repetition", "all_attempt_accounted_usd")


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def decimal_cost(value: object) -> Decimal:
    try:
        cost = Decimal(str(value))
    except InvalidOperation as error:
        raise ValueError("Cost must be a finite nonnegative number") from error
    if not cost.is_finite() or cost < 0:
        raise ValueError("Cost must be a finite nonnegative number")
    return cost


def _read_outcomes(directory: Path) -> list[dict]:
    rows = read_json(directory / "combined-results.json")
    expected = read_json(directory / "combined-expected.json")["runs"]
    if not isinstance(rows, list) or not rows or not isinstance(expected, list):
        raise ValueError("Study rows and expected runs must be nonempty lists")
    observed_keys = [run_key(row) for row in rows]
    planned_keys = [run_key(row) for row in expected]
    if (
        len(set(observed_keys)) != len(rows)
        or len(set(planned_keys)) != len(expected)
        or set(observed_keys) != set(planned_keys)
    ):
        raise ValueError("Duplicate, missing, or unexpected study identity")
    planned = {run_key(row): row for row in expected}
    for row in rows:
        spec = planned[run_key(row)]
        if any(
            row.get(field) != spec.get(field)
            for field in ("phase", "family_id", "rating_band", "analysis_stratum")
        ):
            raise ValueError("Observed family or stratum differs from the planned identity")
    return rows


def _read_costs(directory: Path, rows: list[dict]) -> dict[tuple, Decimal]:
    observed_keys = {run_key(row) for row in rows}
    phases = {row.get("phase") for row in rows}
    if len(phases) != 1 or None in phases:
        raise ValueError("One explicit collection phase is required")
    costs = {}
    with (directory / "all-attempt-costs.csv").open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if not set(COST_FIELDS) <= set(reader.fieldnames or []):
            raise ValueError("Cost table is missing required columns")
        for record in reader:
            record["repetition"] = int(record["repetition"])
            if record["phase"] not in phases:
                raise ValueError("Cost table collection phase differs")
            key = run_key(record)
            if key in costs:
                raise ValueError("Duplicate logical-run cost")
            costs[key] = decimal_cost(record["all_attempt_accounted_usd"])
    if set(costs) != set(observed_keys):
        raise ValueError("Cost table and planned identities differ")
    audit = read_json(directory / "data-audit.json")
    if set(audit["by_condition_accounted_usd"]) != {row["condition"] for row in rows}:
        raise ValueError("Audited conditions differ from observed conditions")
    if sum(costs.values(), Decimal(0)) != decimal_cost(audit["all_attempt_accounted_usd"]):
        raise ValueError("Cost table does not reconcile with the audited total")
    for condition, amount in audit["by_condition_accounted_usd"].items():
        subtotal = sum((cost for key, cost in costs.items() if key[2] == condition), Decimal(0))
        if subtotal != decimal_cost(amount):
            raise ValueError("Condition costs do not reconcile with audited totals")
    return costs


@dataclass(frozen=True)
class Study:
    """Selected outcomes and all-attempt costs for one model."""

    rows: tuple[dict, ...]
    costs: dict[tuple, Decimal]
    model: str

    @classmethod
    def load(cls, directory: Path, *, model: str | None = None) -> "Study":
        rows = _read_outcomes(directory)
        models = {row["model"] for row in rows}
        if model is None:
            if len(models) != 1:
                raise ValueError("Select --model when a study contains multiple models")
            model = next(iter(models))
        if model not in models:
            raise ValueError("Requested model is absent from the study")
        costs = _read_costs(directory, rows)
        selected = tuple(row for row in rows if row["model"] == model)
        if any(
            row.get("valid_run") is not True
            or row.get("infrastructure_error")
            or not isinstance(row.get("hidden_passed"), bool)
            for row in selected
        ):
            raise ValueError("Resolve infrastructure failures before plotting")
        return cls(selected, {run_key(row): costs[run_key(row)] for row in selected}, model)


def accuracy_cost_points(study: Study, *, draws: int = 10_000, seed: int = 20261123) -> dict:
    """Use the same family draws for costs, scores, and every assigned condition."""
    if draws < 2:
        raise ValueError("At least two bootstrap draws are required")
    grouped = defaultdict(lambda: defaultdict(list))
    for row in study.rows:
        grouped[row["task_id"]][row["condition"]].append(row)
    tasks, family_metadata = {}, {}
    complete_repetitions = None
    for task_id, arms in sorted(grouped.items()):
        if set(arms) != set(ARMS):
            raise ValueError("Every task needs all three conditions")
        repetitions = [{row["repetition"] for row in arms[arm]} for arm in ARMS]
        if any(reps != repetitions[0] for reps in repetitions[1:]):
            raise ValueError("Conditions have different repetition identities")
        if complete_repetitions is None:
            complete_repetitions = repetitions[0]
        elif repetitions[0] != complete_repetitions:
            raise ValueError("Plot requires complete repetitions over the same task set")
        metadata = {
            (row["family_id"], row["rating_band"], row.get("analysis_stratum", row["rating_band"]))
            for group in arms.values()
            for row in group
        }
        if len(metadata) != 1:
            raise ValueError("Inconsistent family or rating metadata within a task")
        family, rating, stratum = next(iter(metadata))
        if family in family_metadata and family_metadata[family] != (rating, stratum):
            raise ValueError("A source family spans inference strata")
        family_metadata[family] = rating, stratum
        accuracy_means = tuple(mean(int(row["hidden_passed"]) for row in arms[arm]) for arm in ARMS)
        cost_means = tuple(
            float(
                sum((study.costs[run_key(row)] for row in arms[arm]), Decimal(0)) / len(arms[arm])
            )
            for arm in ARMS
        )
        tasks[task_id] = {
            "family": family,
            "rating_band": rating,
            "stratum": stratum,
            "means": accuracy_means + cost_means,
        }
    _, samples, strata = _bootstrap_clusters(tasks, draws, seed)
    if any(len(families) < 2 for families in strata.values()):
        raise ValueError("At least two independent families per stratum are required")
    points = {}
    for index, condition in enumerate(ARMS):
        rows = [row for row in study.rows if row["condition"] == condition]
        accuracy = 100 * mean(task["means"][index] for task in tasks.values())
        cost = mean(task["means"][index + len(ARMS)] for task in tasks.values())
        points[condition] = {
            "label": LABELS[condition],
            "accuracy_percent": accuracy,
            "accuracy_ci95_percent": [_quantile(samples[index], tail) for tail in (0.025, 0.975)],
            "mean_all_attempt_cost_usd_per_task": cost,
            "cost_ci95_usd_per_task": [
                _quantile(samples[index + len(ARMS)], tail) / 100 for tail in (0.025, 0.975)
            ],
            "evaluations": len(rows),
            "independent_task_families": len(family_metadata),
            "repetitions": sorted({row["repetition"] for row in rows}),
        }
    return {
        "model": study.model,
        "points": points,
        "bootstrap_draws": draws,
        "bootstrap_seed": seed,
        "method": "Rating-stratified family bootstrap; keep all repetitions and both metrics together.",
        "intervals": "95% marginal percentile intervals on each axis, not a joint 95% region.",
        "cost_definition": "All-attempt accounted API cost per planned evaluation, including infrastructure retries and conservative uncertain charges; preparation excluded.",
        "inference_scope": "Comparable task families; excludes invoice uncertainty and separate fixed-benchmark Monte Carlo inference.",
    }


def draw_plot(payload: dict, output: Path, *, xlim=None, ylim=None) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FuncFormatter, MaxNLocator

    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 11,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "pdf.fonttype": 42,
            "svg.fonttype": "none",
        }
    )
    figure, axis = plt.subplots(figsize=(8, 5.6))
    positions = {"baseline": (13, -6), "verifier": (-13, -9), "guided_verifier": (13, 10)}
    for condition, point in payload["points"].items():
        x, y = point["mean_all_attempt_cost_usd_per_task"], point["accuracy_percent"]
        low_x, high_x = point["cost_ci95_usd_per_task"]
        low_y, high_y = point["accuracy_ci95_percent"]
        axis.errorbar(
            x,
            y,
            xerr=[[x - low_x], [high_x - x]],
            yerr=[[y - low_y], [high_y - y]],
            fmt="o",
            markersize=8,
            color=COLORS[condition],
            elinewidth=1.5,
            capsize=4,
            capthick=1.3,
            zorder=3,
        )
        dx, dy = positions[condition]
        axis.annotate(
            f"{LABELS[condition]}\n{y:.1f}% | ${x:.4f}/task",
            (x, y),
            xytext=(dx, dy),
            textcoords="offset points",
            fontsize=10.4,
            ha="left" if dx > 0 else "right",
            va="bottom" if dy > 0 else "top",
            color=COLORS[condition],
            bbox={"boxstyle": "round,pad=.22", "fc": "white", "ec": "none", "alpha": 0.88},
        )
    axis.set_xlabel("Mean accounted API cost per task (USD)", labelpad=9)
    axis.set_ylabel("Accuracy: tasks solved (%)", labelpad=9)
    axis.xaxis.set_major_locator(MaxNLocator(nbins=12, steps=[1, 2, 5, 10]))
    axis.xaxis.set_major_formatter(FuncFormatter(lambda value, _: f"${value:.3g}"))
    if xlim is not None:
        axis.set_xlim(*xlim)
    if ylim is not None:
        axis.set_ylim(*ylim)
    axis.grid(color="#E5E7EB", linewidth=0.8, zorder=0)
    figure.suptitle(
        "Accuracy vs mean cost per task",
        x=0.5,
        y=0.97,
        ha="center",
        fontsize=17,
        fontweight="bold",
        color="#142D42",
    )
    figure.subplots_adjust(left=0.12, right=0.97, bottom=0.15, top=0.89)
    for suffix in ("png", "pdf", "svg"):
        path = output / f"accuracy-vs-cost.{suffix}"
        figure.savefig(path, dpi=240, bbox_inches="tight", facecolor="white")
        if suffix == "svg":
            text = "\n".join(
                line.rstrip() for line in path.read_text(encoding="utf-8").splitlines()
            )
            path.write_bytes((text + "\n").encode("utf-8"))
    plt.close(figure)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--study", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model")
    parser.add_argument("--draws", type=int, default=10_000)
    parser.add_argument("--seed", type=int, default=20261123)
    parser.add_argument("--xlim", type=float, nargs=2)
    parser.add_argument("--ylim", type=float, nargs=2)
    args = parser.parse_args(argv)
    for limits in (args.xlim, args.ylim):
        if limits and (not all(math.isfinite(value) for value in limits) or limits[0] >= limits[1]):
            parser.error("Axis limits must be finite and increasing")
    settings_path = args.study / "report-settings.json"
    settings = read_json(settings_path) if settings_path.exists() else {}
    payload = accuracy_cost_points(
        Study.load(args.study, model=args.model), draws=args.draws, seed=args.seed
    )
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "accuracy-cost-points.json").write_text(
        json.dumps(payload, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )
    with (args.output / "accuracy-cost-points.csv").open(
        "w", encoding="utf-8", newline=""
    ) as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(
            [
                "condition",
                "mean_cost_usd_per_task",
                "cost_ci95_low",
                "cost_ci95_high",
                "accuracy_percent",
                "accuracy_ci95_low",
                "accuracy_ci95_high",
            ]
        )
        for condition, point in payload["points"].items():
            writer.writerow(
                [
                    condition,
                    point["mean_all_attempt_cost_usd_per_task"],
                    *point["cost_ci95_usd_per_task"],
                    point["accuracy_percent"],
                    *point["accuracy_ci95_percent"],
                ]
            )
    draw_plot(
        payload,
        args.output,
        xlim=args.xlim or settings.get("xlim"),
        ylim=args.ylim or settings.get("ylim"),
    )
    print(
        json.dumps(
            {"output": str(args.output), "model": payload["model"], "points": payload["points"]},
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
