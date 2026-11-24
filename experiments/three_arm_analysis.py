"""Analyze optional and guided verifier access against one shared baseline."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

from experiments.analysis import (
    analyze,
    load_records,
    repetition_score_summary,
    _paired_effect,
    _projections,
)


ARMS = ("baseline", "verifier", "guided_verifier")
CONTRASTS = {
    "optional_vs_baseline": ("baseline", "verifier"),
    "guided_vs_baseline": ("baseline", "guided_verifier"),
}
SETTING_FIELDS = ("max_output_tokens", "effort", "step_limit", "solve_limit_seconds")


def _block_repeated_scores(model_report: dict, records: list[dict], model: str) -> None:
    """Honor design/settings blockers added after the lower-level analysis."""
    for condition, metrics in model_report["conditions"].items():
        rows = [
            row
            for row in records
            if row.get("model") == model and row.get("condition") == condition
        ]
        metrics["repeated_benchmark_scores"] = repetition_score_summary(rows, complete=False)


def _design_blockers(
    planned: list[dict] | None, records: list[dict], configs: list[dict] | None
) -> list[dict]:
    blockers = []
    grouped = {}
    for row in planned if planned is not None else records:
        if row.get("condition") not in ARMS:
            blockers.append(
                {"code": "unknown_three_arm_condition", "detail": str(row.get("condition"))}
            )
            continue
        key = row.get("model"), row.get("task_id")
        grouped.setdefault(key, {}).setdefault(row["condition"], set()).add(row.get("repetition"))
    for (model, task), conditions in sorted(grouped.items()):
        if (
            set(conditions) != set(ARMS)
            or len({frozenset(repetitions) for repetitions in conditions.values()}) != 1
        ):
            blockers.append(
                {"code": "unbalanced_three_arm_design", "model": model, "detail": str(task)}
            )
    # Source/prompt hashes can legitimately differ when a guided condition is
    # added; compare the settings that control the shared resource policy.
    for field in SETTING_FIELDS:
        values = {
            json.dumps(config[field], sort_keys=True) for config in configs or [] if field in config
        }
        if len(values) > 1:
            blockers.append({"code": "incompatible_batch_settings", "detail": field})
    per_model_settings = {}
    for row in records:
        settings = row.get("model_settings")
        if isinstance(settings, dict):
            per_model_settings.setdefault(row.get("model"), set()).add(
                json.dumps(settings, sort_keys=True)
            )
    for model, settings in per_model_settings.items():
        if len(settings) > 1:
            blockers.append({"code": "incompatible_model_settings", "model": model})
    return blockers


def analyze_three_arms(
    records: Iterable[dict],
    expected_runs: Iterable[dict] | None = None,
    *,
    phase: str = "calibration",
    bootstrap_draws: int = 10_000,
    seed: int = 20261123,
    familywise_confidence_level: float = 0.95,
    descriptive_confidence_level: float = 0.95,
    workers: int = 4,
    per_run_cap_usd: float | None = None,
    batch_configs: list[dict] | None = None,
    exploratory_contrasts: bool = False,
) -> dict:
    """Use Bonferroni intervals for two prespecified contrasts on fresh main data.

    Calibration retains arm-only descriptive intervals and paired point changes;
    it never becomes a main treatment-effect analysis by being passed here.
    """
    if phase not in ("calibration", "main"):
        raise ValueError("Three-arm phase must be calibration or main")
    if exploratory_contrasts and phase != "calibration":
        raise ValueError(
            "exploratory_contrasts is only for calibration; main contrasts are reported separately"
        )
    if (
        not isinstance(familywise_confidence_level, (float, int))
        or isinstance(familywise_confidence_level, bool)
        or not 0 < familywise_confidence_level < 1
    ):
        raise ValueError("familywise_confidence_level must be strictly between zero and one")
    records = list(records)
    planned = list(expected_runs) if expected_runs is not None else None
    adjusted = 1 - (1 - familywise_confidence_level) / len(CONTRASTS)
    options = dict(
        phase=phase,
        bootstrap_draws=bootstrap_draws,
        seed=seed,
        confidence_level=adjusted,
        descriptive_confidence_level=descriptive_confidence_level,
        workers=workers,
        per_run_cap_usd=per_run_cap_usd,
    )
    summary = analyze(records, planned, conditions=CONTRASTS["optional_vs_baseline"], **options)
    additional_blockers = _design_blockers(planned, records, batch_configs)
    summary["blockers"].extend(additional_blockers)
    summary["complete"] = summary["complete"] and not additional_blockers
    summary["schema_version"] = 2
    summary["planned_conditions"] = list(ARMS)
    summary["multiplicity"] = {
        "method": "bonferroni",
        "co_primary_contrasts": list(CONTRASTS),
        "familywise_confidence_level": familywise_confidence_level,
        "per_contrast_confidence_level": adjusted,
        "interpretation": "Two prespecified two-sided contrast intervals use alpha/2 each. Familywise coverage is approximately the requested level for percentile bootstrap intervals, conditional on their marginal coverage; Bonferroni does not require independent contrasts.",
        "shared_baseline": True,
        "calibration_note": "Calibration exposes descriptive arm intervals and paired point changes only; causal co-primary intervals require the separate fresh main collection.",
    }
    summary["settings_compatibility"] = {
        "checked_fields": list(SETTING_FIELDS),
        "config_count": len(batch_configs or []),
        "source_prompt_hashes_may_differ": True,
    }
    analyses = {}
    for name, pair in CONTRASTS.items():
        selected = [row for row in records if row.get("condition") in pair]
        expected = (
            [row for row in planned if row.get("condition") in pair]
            if planned is not None
            else None
        )
        report = analyze(selected, expected, conditions=pair, **options)
        for model, model_report in report["models"].items():
            condition_metrics = model_report["conditions"]
            first = condition_metrics.get(pair[0], {}).get("task_averaged_success_percent")
            second = condition_metrics.get(pair[1], {}).get("task_averaged_success_percent")
            model_report["descriptive_difference_percentage_points"] = (
                second - first
                if summary["complete"]
                and model_report["complete"]
                and first is not None
                and second is not None
                else None
            )
            if phase == "main" and not summary["complete"]:
                model_report["paired_effect"] = {
                    "status": "blocked",
                    "blockers": summary["blockers"],
                    "reason": "Resolve the full three-arm planned denominator before reporting co-primary intervals",
                }
            if not summary["complete"]:
                model_report["complete"] = False
                _block_repeated_scores(model_report, selected, model)
        report["complete"] = report["complete"] and summary["complete"]
        report["interpretation"] = (
            "Main co-primary contrast"
            if phase == "main"
            else "Exploratory calibration paired point; no main effect CI"
        )
        analyses[name] = report
    summary["contrast_analyses"] = analyses
    if exploratory_contrasts:
        exploratory = {}
        for name, pair in CONTRASTS.items():
            models = {}
            for model in summary["models"]:
                if not summary["complete"]:
                    result = {"status": "blocked", "blockers": summary["blockers"]}
                else:
                    selected = [
                        row
                        for row in records
                        if row.get("model") == model and row.get("condition") in pair
                    ]
                    result = _paired_effect(selected, pair, bootstrap_draws, seed, adjusted)
                    if result["status"] == "ok":
                        result["status"] = "exploratory"
                        result["warnings"].append(
                            f"Only {result['family_count']} development families; prior calibration outcomes were inspected. This paired interval is exploratory, not confirmatory evidence or a main treatment effect."
                        )
                result["phase"] = "calibration"
                models[model] = result
            exploratory[name] = {
                "models": models,
                "confidence_level": adjusted,
                "interpretation": "Exploratory paired development contrast; both prespecified contrasts use the same adjusted coverage and method",
            }
        summary["exploratory_contrasts"] = exploratory
    for model, model_summary in summary["models"].items():
        model_summary["complete"] = model_summary["complete"] and summary["complete"]
        if not model_summary["complete"]:
            _block_repeated_scores(model_summary, records, model)
        model_summary["paired_effect"] = {
            "status": "reported_separately" if phase == "main" else "not_requested",
            "reason": "Use contrast_analyses for the two prespecified contrasts; calibration is descriptive only",
        }
        model_summary["descriptive_contrasts_percentage_points"] = {
            name: report["models"].get(model, {}).get("descriptive_difference_percentage_points")
            for name, report in analyses.items()
        }
        model_summary["main_workload_projections"] = _projections(
            model_summary["conditions"], ARMS, workers=workers, per_run_cap_usd=per_run_cap_usd
        )
        for projection in model_summary["main_workload_projections"]:
            projection["based_on_complete_planned_data"] = model_summary["complete"]
    summary["spend_note"] += (
        " Top-level spend counts each supplied resolved run once; do not sum contrast-level spend because their baseline records are shared."
    )
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", nargs="+", required=True)
    parser.add_argument("--expected", nargs="+", required=True)
    parser.add_argument("--phase", choices=("calibration", "main"), default="calibration")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--bootstrap-draws", type=int, default=10_000)
    parser.add_argument("--seed", type=int, default=20261123)
    parser.add_argument("--familywise-confidence-level", type=float, default=0.95)
    parser.add_argument("--descriptive-confidence-level", type=float, default=0.95)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--per-run-cap-usd", type=float)
    parser.add_argument(
        "--exploratory-contrasts",
        action="store_true",
        help="Explicitly report paired calibration intervals as exploratory development summaries",
    )
    args = parser.parse_args(argv)
    try:
        configs = []
        for path in args.expected:
            payload = json.loads(Path(path).read_text(encoding="utf-8-sig"))
            if isinstance(payload, dict) and isinstance(payload.get("config"), dict):
                configs.append(payload["config"])
        report = analyze_three_arms(
            load_records(args.results),
            load_records(args.expected),
            phase=args.phase,
            bootstrap_draws=args.bootstrap_draws,
            seed=args.seed,
            familywise_confidence_level=args.familywise_confidence_level,
            descriptive_confidence_level=args.descriptive_confidence_level,
            workers=args.workers,
            per_run_cap_usd=args.per_run_cap_usd,
            batch_configs=configs,
            exploratory_contrasts=args.exploratory_contrasts,
        )
    except (OSError, ValueError, TypeError, KeyError) as error:
        parser.error(str(error))
    rendered = json.dumps(report, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 2 if report["blockers"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
