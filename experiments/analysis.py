"""Summarize planned runs without treating repetitions as independent tasks.

No third-party packages are required. See README.md for the result
contract, interpretation of the intervals, and command-line examples.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
import math
from pathlib import Path
import random
from statistics import mean, median, stdev, variance
from typing import Any, Iterable


PHASES = ("model_screen", "calibration", "main")
IDENTITY_FIELDS = ("model", "task_id", "condition", "repetition")
BUDGET_EXITS = {
    "budgetexhausted",
    "budgetexceeded",
    "costlimit",
    "costlimitexceeded",
    "tokenlimit",
    "tokenlimitexceeded",
    "steplimit",
    "steplimitexceeded",
    "walltimelimit",
    "walltimelimitexceeded",
    "timelimit",
    "timelimitexceeded",
    "limitsexceeded",
    "resourceexhausted",
    "resourcelimit",
}


def run_key(row: dict) -> tuple[str, str, str, int]:
    """An attempt is not an independent repetition; duplicate keys block analysis."""
    for field in IDENTITY_FIELDS[:3]:
        if not isinstance(row.get(field), str) or not row[field].strip():
            raise ValueError(f"{field} must be a nonempty string")
    repetition = row.get("repetition")
    if isinstance(repetition, bool) or not isinstance(repetition, int) or repetition < 0:
        raise ValueError("repetition must be a nonnegative integer")
    return row["model"], row["task_id"], row["condition"], repetition


def _number(value: Any) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(value)
        and value >= 0
    )


def _budget_exit(row: dict) -> bool:
    normalized = "".join(c for c in str(row.get("exit_status", "")).lower() if c.isalnum())
    return normalized in BUDGET_EXITS


def _scored(row: dict) -> bool:
    return (
        not row.get("infrastructure_error")
        and isinstance(row.get("hidden_passed"), bool)
        and (row.get("valid_run") is True or _budget_exit(row))
    )


def _row_metadata(row: dict) -> tuple[str, str, str, bool]:
    """Keep explicit assignment distinct from legacy rating-only metadata."""
    for field in ("family_id", "rating_band"):
        if not isinstance(row.get(field), str) or not row[field].strip():
            raise ValueError(field)
    explicit = "analysis_stratum" in row
    stratum = row.get("analysis_stratum", row["rating_band"])
    if not isinstance(stratum, str) or not stratum.strip():
        raise ValueError("analysis_stratum")
    return row["family_id"], row["rating_band"], stratum, explicit


def _quantile(values: list[float], probability: float) -> float:
    ordered = sorted(values)
    position = (len(ordered) - 1) * probability
    low = math.floor(position)
    high = math.ceil(position)
    return ordered[low] + (ordered[high] - ordered[low]) * (position - low)


def distribution(values: Iterable[float]) -> dict:
    values = list(values)
    if not values:
        return {
            "n": 0,
            "mean": None,
            "median": None,
            "p90": None,
            "p95": None,
            "minimum": None,
            "maximum": None,
            "sum": 0.0,
        }
    return {
        "n": len(values),
        "mean": mean(values),
        "median": median(values),
        "p90": _quantile(values, 0.90),
        "p95": _quantile(values, 0.95),
        "minimum": min(values),
        "maximum": max(values),
        "sum": sum(values),
    }


def repetition_score_summary(rows: Iterable[dict], *, complete: bool = False) -> dict:
    """Describe stochastic variation between complete fixed-benchmark rounds.

    ``complete`` must come from the planned-denominator audit, not merely from
    the presence of result files. Every round must contain the same tasks and
    a scored final outcome for each one. The sample SD/variance use ddof=1;
    they are not between-family variation or a confidence interval of the mean.
    """
    rows = list(rows)
    groups: dict[int, list[dict]] = defaultdict(list)
    identities = []
    model_conditions = set()
    blockers = []
    if not complete:
        blockers.append("The planned denominator is unknown, incomplete, or blocked")
    for row in rows:
        try:
            key = run_key(row)
        except (ValueError, TypeError, AttributeError) as error:
            blockers.append("Invalid run identity: " + str(error))
            continue
        identities.append(key)
        model_conditions.add((key[0], key[2]))
        groups[key[3]].append(row)
    if not groups:
        blockers.append("No benchmark rounds are present")
    if len(model_conditions) > 1:
        blockers.append("A repeated-score summary requires one model and condition")
    if len(identities) != len(set(identities)):
        blockers.append("Duplicate run identities cannot be counted as repeated outcomes")
    task_sets = [{row["task_id"] for row in group} for group in groups.values()]
    if task_sets and any(tasks != task_sets[0] for tasks in task_sets[1:]):
        blockers.append("Benchmark rounds contain different task sets")
    if any(not _scored(row) for row in rows):
        blockers.append("A benchmark round contains an unscored outcome")

    rounds = []
    for repetition, group in sorted(groups.items()):
        scored = [row for row in group if _scored(row)]
        duplicate_tasks = len({row["task_id"] for row in group}) != len(group)
        provisional = (
            100 * mean(int(row["hidden_passed"]) for row in scored)
            if scored and not duplicate_tasks
            else None
        )
        rounds.append(
            {
                "repetition": repetition,
                "observed_runs": len(group),
                "observed_task_count": len({row["task_id"] for row in group}),
                "scored_runs": len(scored),
                "passed_tasks": sum(row["hidden_passed"] for row in scored)
                if not duplicate_tasks
                else None,
                "score_percent": provisional if not blockers else None,
                "provisional_score_percent": provisional,
                "provisional": bool(blockers),
                "status": "blocked" if blockers else "complete",
            }
        )
    scores = [row["score_percent"] for row in rounds] if not blockers else None
    estimable = scores is not None and len(scores) >= 2
    warnings = []
    if groups and len(groups) < 10:
        warnings.append(
            f"Fewer than 10 benchmark rounds: the sample SD/variance are unstable; {len(groups)} repetitions provide only {len(groups) - 1} variance degrees of freedom"
        )
    if scores is not None and len(scores) == 1:
        warnings.append("One benchmark round cannot estimate stochastic SD or variance")
    return {
        "status": "blocked" if blockers else "ok",
        "rounds": rounds,
        "repetition_count": len(groups),
        "observed_task_union_count": len(set().union(*task_sets)) if task_sets else 0,
        "scores_percent": scores,
        "mean_score_percent": mean(scores) if scores else None,
        "sample_sd_percentage_points": stdev(scores) if estimable else None,
        "sample_variance_percentage_points_squared": variance(scores) if estimable else None,
        "variance_ddof": 1,
        "variance_estimable": estimable,
        "blockers": blockers,
        "warnings": warnings,
        "interpretation": "Each score is one complete benchmark round on the same task set. Sample SD/variance describe variation between repeated rounds on this fixed benchmark; they are not task-family uncertainty, a standard error, or a confidence interval of the mean. With few rounds, the variance estimate is unstable.",
    }


def _condition_metrics(rows: list[dict], *, complete: bool = False) -> dict:
    scored = [row for row in rows if _scored(row)]
    tasks: dict[str, list[int]] = defaultdict(list)
    for row in scored:
        tasks[row["task_id"]].append(int(row["hidden_passed"]))
    total_times = [
        row["solve_seconds"] + row["evaluation_seconds"]
        for row in scored
        if _number(row.get("solve_seconds")) and _number(row.get("evaluation_seconds"))
    ]
    costs = [row["model_cost_usd"] for row in rows if _number(row.get("model_cost_usd"))]
    return {
        "observed_runs": len(rows),
        "scored_runs": len(scored),
        "infrastructure_failures": sum(bool(row.get("infrastructure_error")) for row in rows),
        "budget_exhausted_scored_runs": sum(_budget_exit(row) for row in scored),
        "hidden_passed_runs": sum(row["hidden_passed"] for row in scored),
        "task_count_scored": len(tasks),
        "task_averaged_success_percent": 100 * mean(mean(scores) for scores in tasks.values())
        if tasks
        else None,
        "repeated_benchmark_scores": repetition_score_summary(rows, complete=complete),
        "success_is_provisional": True,
        "exit_status_counts": dict(
            sorted(Counter(str(row.get("exit_status", "missing")) for row in rows).items())
        ),
        "observed_model_spend_usd": sum(costs),
        "cost_upper_bound_runs": sum(bool(row.get("cost_is_upper_bound")) for row in rows),
        "observed_model_spend_is_upper_bound": any(row.get("cost_is_upper_bound") for row in rows),
        "runs_missing_cost": len(rows) - len(costs),
        "scored_run_cost_usd": distribution(
            row["model_cost_usd"] for row in scored if _number(row.get("model_cost_usd"))
        ),
        "scored_solve_seconds": distribution(
            row["solve_seconds"] for row in scored if _number(row.get("solve_seconds"))
        ),
        "scored_evaluation_seconds": distribution(
            row["evaluation_seconds"] for row in scored if _number(row.get("evaluation_seconds"))
        ),
        "scored_solve_plus_evaluation_seconds": distribution(total_times),
    }


def _interval(
    estimate: float,
    samples: list[float],
    uncertainty_estimable: bool,
    confidence_level: float = 0.95,
) -> dict:
    tail = (1 - confidence_level) / 2
    low, high = _quantile(samples, tail), _quantile(samples, 1 - tail)
    degenerate = math.isclose(low, high, abs_tol=1e-12, rel_tol=0)
    bounds = [low, high] if uncertainty_estimable and not degenerate else None
    return {
        "estimate": estimate,
        "confidence_level": confidence_level,
        "confidence_interval": bounds,
        "ci95": bounds if confidence_level == 0.95 else None,
        "bootstrap_percentile_bounds": [low, high],
        "bootstrap_degenerate": degenerate,
        "ci_suppressed": not uncertainty_estimable or degenerate,
    }


def _with_hoeffding_fallback(interval: dict, strata: dict, *, lower: float, upper: float) -> dict:
    """Offer a bounded-mean interval when family bootstrapping cannot vary.

    The simple stratified inequality is used only for one task per independent
    family. Repetitions stay inside that family's bounded observation.
    """
    interval.update(
        conservative_ci95=None,
        conservative_confidence_interval=None,
        ci_method="family_cluster_percentile_bootstrap"
        if interval["confidence_interval"] is not None
        else None,
    )
    one_task_per_family = all(
        len(tasks) == 1 for families in strata.values() for tasks in families.values()
    )
    if interval["confidence_interval"] is not None or not one_task_per_family:
        return interval
    total_families = sum(len(families) for families in strata.values())
    variance_proxy = sum(
        (len(families) / total_families) ** 2 / len(families) for families in strata.values()
    )
    half_width = (upper - lower) * math.sqrt(
        math.log(2 / (1 - interval["confidence_level"])) / 2 * variance_proxy
    )
    bounds = [
        max(lower, interval["estimate"] - half_width),
        min(upper, interval["estimate"] + half_width),
    ]
    interval.update(
        conservative_confidence_interval=bounds,
        conservative_ci95=bounds if interval["confidence_level"] == 0.95 else None,
        ci_method="hoeffding_conservative_fallback",
        conservative_half_width=half_width,
        conservative_fallback_assumptions="Independent families, one task per family, fixed stratum weights, and bounded task-level means; repetitions are not independent families.",
    )
    return interval


def _bootstrap_clusters(tasks: dict[str, dict], draws: int, seed: int) -> tuple:
    """Resample complete families, retaining fixed original task weights by stratum."""
    strata: dict[str, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
    for task in tasks.values():
        strata[task["stratum"]][task["family"]].append(task)
    arm_count = len(next(iter(tasks.values()))["means"])
    point = tuple(
        100 * mean(task["means"][arm] for task in tasks.values()) for arm in range(arm_count)
    )
    rng = random.Random(seed)
    samples = tuple([] for _ in range(arm_count))
    weighted_strata = []
    for stratum, families in sorted(strata.items()):
        members = [families[family] for family in sorted(families)]
        weight = sum(len(family_tasks) for family_tasks in members) / len(tasks)
        weighted_strata.append((weight, members))
    for _ in range(draws):
        arm_means = [0.0] * arm_count
        for weight, families in weighted_strata:
            sampled = [task for _ in range(len(families)) for task in rng.choice(families)]
            for arm in range(arm_count):
                arm_means[arm] += 100 * weight * mean(task["means"][arm] for task in sampled)
        for arm in range(arm_count):
            samples[arm].append(arm_means[arm])
    return point, samples, strata


def _stratum_summary(tasks: dict[str, dict], strata: dict) -> dict:
    rating_families: dict[str, set[str]] = defaultdict(set)
    for task in tasks.values():
        rating_families[task["rating_band"]].add(task["family"])
    task_counts = Counter(task["stratum"] for task in tasks.values())
    return {
        "family_counts_by_rating_band": {s: len(f) for s, f in sorted(rating_families.items())},
        "task_counts_by_rating_band": dict(
            sorted(Counter(t["rating_band"] for t in tasks.values()).items())
        ),
        "family_counts_by_analysis_stratum": {s: len(f) for s, f in sorted(strata.items())},
        "task_counts_by_analysis_stratum": dict(sorted(task_counts.items())),
        "analysis_stratum_task_weights": {
            s: n / len(tasks) for s, n in sorted(task_counts.items())
        },
    }


def _descriptive_success_interval(
    rows: list[dict],
    *,
    phase: str,
    complete: bool,
    draws: int,
    seed: int,
    confidence_level: float = 0.95,
) -> dict:
    """An arm-only calibration interval is descriptive, not a treatment effect."""
    scored = [row for row in rows if _scored(row)]
    by_task: dict[str, list[dict]] = defaultdict(list)
    for row in scored:
        by_task[row["task_id"]].append(row)
    estimate = (
        100
        * mean(mean(int(r["hidden_passed"]) for r in task_rows) for task_rows in by_task.values())
        if by_task
        else None
    )
    tasks = {}
    family_assignments: dict[str, set[tuple]] = defaultdict(set)
    issues = []
    for task_id, task_rows in sorted(by_task.items()):
        try:
            metadata = {_row_metadata(row) for row in task_rows}
        except ValueError as error:
            issues.append(f"Task {task_id} has missing/invalid metadata: {error}")
            continue
        if len(metadata) != 1:
            issues.append(f"Task {task_id} has missing/inconsistent family/stratum metadata")
            continue
        family, rating, stratum, explicit = next(iter(metadata))
        family_assignments[family].add((rating, stratum, explicit))
        tasks[task_id] = {
            "family": family,
            "rating_band": rating,
            "stratum": stratum,
            "means": (mean(int(row["hidden_passed"]) for row in task_rows),),
        }
    if any(len(assignments) != 1 for assignments in family_assignments.values()):
        issues.append("A family has inconsistent rating/analysis-stratum assignment")
    if not complete:
        issues.append("Planned outcomes are incomplete, blocked, or their denominator is unknown")
    summary = {
        "status": "blocked"
        if issues or not tasks
        else "exploratory"
        if phase != "main"
        else "main_descriptive",
        "estimate_percent": estimate,
        "ci95_percent": None,
        "confidence_level": confidence_level,
        "confidence_interval_percent": None,
        "conservative_confidence_interval_percent": None,
        "conservative_ci95_percent": None,
        "ci_method": None,
        "bootstrap_percentile_bounds_percent": None,
        "bootstrap_degenerate": None,
        "ci_suppressed": True,
        "task_count": len(by_task),
        "family_count": len(family_assignments),
        "family_counts_by_rating_band": {},
        "family_counts_by_analysis_stratum": {},
        "task_counts_by_analysis_stratum": {},
        "analysis_stratum_task_weights": {},
        "bootstrap_draws": draws,
        "bootstrap_seed": seed,
        "provisional": phase != "main" or not complete,
        "interpretation": (
            "Exploratory success on development families; model selection and calibration do not establish a main treatment effect."
            if phase != "main"
            else "Descriptive success in one main-study arm; use the paired result for the treatment effect."
        ),
        "inference_scope": "Comparable families within this sample's rating distribution; all observed repetitions remain clustered. This is not a conditional fixed-benchmark Monte Carlo interval.",
        "warnings": issues,
    }
    if any("analysis_stratum" in row for row in rows):
        summary["inference_scope"] = (
            "Comparable families within the frozen analysis-stratum task weights, conditional on the fixed "
            "execution-host allocation when strata are host-by-rating. Observed repetitions remain clustered; "
            "host variability and fixed-benchmark Monte Carlo uncertainty are not separately estimated."
        )
    if summary["status"] == "blocked":
        return summary
    point, samples, strata = _bootstrap_clusters(tasks, draws, seed)
    estimable = all(len(families) >= 2 for families in strata.values())
    interval = _with_hoeffding_fallback(
        _interval(point[0], samples[0], estimable, confidence_level), strata, lower=0, upper=100
    )
    summary.update(
        estimate_percent=interval["estimate"],
        ci95_percent=interval["ci95"],
        confidence_interval_percent=interval["confidence_interval"],
        conservative_confidence_interval_percent=interval["conservative_confidence_interval"],
        conservative_ci95_percent=interval["conservative_ci95"],
        ci_method=interval["ci_method"],
        bootstrap_percentile_bounds_percent=interval["bootstrap_percentile_bounds"],
        bootstrap_degenerate=interval["bootstrap_degenerate"],
        ci_suppressed=interval["ci_suppressed"],
        **_stratum_summary(tasks, strata),
    )
    if len(family_assignments) < 20:
        summary["warnings"].append(
            "Fewer than 20 independent families: this exploratory percentile-bootstrap CI can have poor coverage; repetitions do not increase the family count"
        )
    if not estimable:
        summary["warnings"].append(
            "At least one stratum has fewer than two families; its between-family uncertainty cannot be estimated"
        )
    if interval["bootstrap_degenerate"]:
        summary["warnings"].append(
            "Bootstrap bounds are degenerate; they are not a precise zero-width CI or evidence of certainty"
        )
    if interval["conservative_confidence_interval"] is not None:
        summary["warnings"].append(
            "A distribution-free Hoeffding fallback is reported separately; it can be very wide and assumes independent families with one task per family"
        )
    if phase == "model_screen":
        summary["warnings"].append(
            "Model-screen intervals are not simultaneous and do not adjust for selecting a model on these same tasks"
        )
    return summary


def _paired_effect(
    rows: list[dict],
    conditions: tuple[str, str],
    draws: int,
    seed: int,
    confidence_level: float = 0.95,
) -> dict:
    by_task: dict[str, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
    for row in rows:
        if row["condition"] in conditions:
            by_task[row["task_id"]][row["condition"]].append(row)
    issues = []
    tasks = {}
    family_assignments: dict[str, set[tuple]] = defaultdict(set)
    for task_id, arms in sorted(by_task.items()):
        repetitions = [
            {row["repetition"] for row in arms.get(condition, [])} for condition in conditions
        ]
        if not repetitions[0] or repetitions[0] != repetitions[1]:
            issues.append(f"Task {task_id} has unbalanced condition/repetition sets")
            continue
        task_rows = [row for arm in arms.values() for row in arm]
        if any(not _scored(row) for row in task_rows):
            issues.append(f"Task {task_id} has an unscored planned outcome")
            continue
        try:
            metadata = {_row_metadata(row) for row in task_rows}
        except ValueError as error:
            issues.append(f"Task {task_id} has missing/invalid metadata: {error}")
            continue
        if len(metadata) != 1:
            issues.append(f"Task {task_id} has inconsistent family/stratum metadata")
            continue
        family, rating, stratum, explicit = next(iter(metadata))
        family_assignments[family].add((rating, stratum, explicit))
        tasks[task_id] = {
            "family": family,
            "rating_band": rating,
            "stratum": stratum,
            "repetitions": len(repetitions[0]),
            "means": tuple(mean(int(row["hidden_passed"]) for row in arms[c]) for c in conditions),
        }
    for family, assignments in family_assignments.items():
        if len(assignments) != 1:
            issues.append(
                f"Family {family} has inconsistent rating/analysis-stratum assignment; freeze one family-level stratum"
            )
    if issues or not tasks:
        return {"status": "blocked", "blockers": issues or ["No paired tasks"]}

    point, samples, strata = _bootstrap_clusters(tasks, draws, seed)
    differences = [right - left for left, right in zip(*samples)]
    estimable = all(len(families) >= 2 for families in strata.values())
    effect = _with_hoeffding_fallback(
        _interval(point[1] - point[0], differences, estimable, confidence_level),
        strata,
        lower=-100,
        upper=100,
    )
    warnings = []
    if not estimable:
        warnings.append(
            "At least one stratum has fewer than two families; its between-family uncertainty cannot be estimated by this bootstrap"
        )
    if len(family_assignments) < 20:
        warnings.append(
            "Fewer than 20 independent families: percentile-bootstrap coverage can be poor"
        )
    if effect["bootstrap_degenerate"]:
        warnings.append(
            "The effect bootstrap is degenerate; zero-width bounds do not establish precision or equivalence"
        )
    if effect["conservative_confidence_interval"] is not None:
        warnings.append(
            "A separate bounded-mean Hoeffding interval is available; its conservative width does not establish a precise effect"
        )
    summary = {
        "status": "ok",
        "conditions": list(conditions),
        "task_count": len(tasks),
        "family_count": len(family_assignments),
        **_stratum_summary(tasks, strata),
        "repetitions_by_task": {task_id: task["repetitions"] for task_id, task in tasks.items()},
        "arm_success_percent": {
            c: _with_hoeffding_fallback(
                _interval(point[arm], samples[arm], estimable, confidence_level),
                strata,
                lower=0,
                upper=100,
            )
            for arm, c in enumerate(conditions)
        },
        "difference_percentage_points": effect,
        "bootstrap_draws": draws,
        "bootstrap_seed": seed,
        "confidence_level": confidence_level,
        "method": "Stratified paired family-cluster percentile bootstrap, retaining all tasks, conditions and repetitions of each sampled family",
        "inference_scope": "Comparable task families within the frozen rating distribution; observed repeated outcomes are kept together. This does not separately estimate model Monte Carlo uncertainty conditional on the fixed benchmark.",
        "warnings": warnings,
    }
    if any("analysis_stratum" in row for row in rows):
        summary["inference_scope"] = (
            "Comparable task families within the frozen analysis-stratum task weights, conditional on the fixed "
            "execution-host allocation when strata are host-by-rating. All conditions and observed repetitions "
            "remain clustered; host variability and fixed-benchmark Monte Carlo uncertainty are not separately estimated."
        )
    return summary


def _projections(
    metrics: dict, conditions: tuple[str, ...], *, workers: int, per_run_cap_usd: float | None
) -> list[dict]:
    projected = []
    for repetitions in (2, 3, 5, 6):
        option: dict[str, Any] = {
            "families": 100,
            "tasks_per_family": 1,
            "repetitions_per_arm": repetitions,
            "arms": len(conditions),
            "agent_runs": 100 * repetitions * len(conditions),
            "workers": workers,
        }
        available = all(
            condition in metrics and metrics[condition]["scored_runs"] > 0
            for condition in conditions
        )
        measurements_complete = available and all(
            metrics[c][field]["n"] == metrics[c]["scored_runs"]
            for c in conditions
            for field in ("scored_run_cost_usd", "scored_solve_plus_evaluation_seconds")
        )
        option["status"] = "estimated" if measurements_complete else "unavailable"
        option["cost_estimate_includes_upper_bounds"] = any(
            metrics.get(c, {}).get("cost_upper_bound_runs", 0) for c in conditions
        )
        if measurements_complete:
            for statistic in ("mean", "median", "p90", "p95", "minimum", "maximum"):
                option[f"model_cost_usd_at_observed_{statistic}"] = (
                    100
                    * repetitions
                    * sum(metrics[c]["scored_run_cost_usd"][statistic] for c in conditions)
                )
                seconds = (
                    100
                    * repetitions
                    * sum(
                        metrics[c]["scored_solve_plus_evaluation_seconds"][statistic]
                        for c in conditions
                    )
                )
                option[f"serial_worker_seconds_at_observed_{statistic}"] = seconds
                option[f"ideal_worker_hours_at_observed_{statistic}"] = seconds / workers / 3600
        else:
            option["reason"] = (
                "Every scored run in both planned arms needs measured model cost, solve time and evaluation time"
            )
        option["model_charge_ceiling_usd"] = (
            option["agent_runs"] * per_run_cap_usd if per_run_cap_usd is not None else None
        )
        option["notes"] = [
            "Projection assumes calibration task difficulty/rating mix, prompts and run budgets represent the main workload; changing those settings invalidates a direct cost/runtime extrapolation.",
            "Mean-based totals estimate expected workload; sums of per-run p90/p95 values are planning envelopes, not total-cost/runtime quantiles or confidence bounds.",
            "Observed minimum/maximum projections are empirical scenarios, not guaranteed bounds; only an enforced charge cap yields a deterministic model-charge ceiling.",
            "Wall-time division by workers assumes full utilization and excludes setup, queueing, contention and report preparation. It is not measured CPU time.",
            "For distributed work, project each host's assigned load with its own concurrency/throughput and take the maximum; unequal host task shares (for example 60/40) must not be blindly divided by pooled workers.",
            "Main-run projections exclude calibration, failed infrastructure attempts and billed retries; budget those separately. Small calibration samples may miss tail behavior.",
        ]
        projected.append(option)
    return projected


def analyze(
    records: Iterable[dict],
    expected_runs: Iterable[dict] | None = None,
    *,
    phase: str = "calibration",
    bootstrap_draws: int = 10_000,
    seed: int = 20261123,
    conditions: tuple[str, str] = ("baseline", "verifier"),
    workers: int = 4,
    per_run_cap_usd: float | None = None,
    confidence_level: float = 0.95,
    descriptive_confidence_level: float = 0.95,
) -> dict:
    """Return a JSON-safe audit, calibration projections, and main-only inference.

    Supply final resolved outcomes only, one per planned identity. Preserve earlier
    attempts separately; passing every attempt here would double-count repetitions.
    """
    if phase not in PHASES:
        raise ValueError(f"phase must be one of {PHASES}")
    if len(conditions) != 2 or len(set(conditions)) != 2:
        raise ValueError("Exactly two distinct planned conditions are required")
    if bootstrap_draws < 2 or workers < 1:
        raise ValueError("bootstrap_draws must be at least two and workers at least one")
    if per_run_cap_usd is not None and not _number(per_run_cap_usd):
        raise ValueError("per_run_cap_usd must be nonnegative and finite")
    for level in (confidence_level, descriptive_confidence_level):
        if not _number(level) or not 0 < level < 1:
            raise ValueError("Confidence levels must be finite and strictly between zero and one")
    blockers: list[dict] = []
    warnings: list[dict] = []
    observed: dict[tuple, dict] = {}
    planned: dict[tuple, dict] = {}
    raw_records = list(records)
    expected_list = list(expected_runs) if expected_runs is not None else None
    for label, source, destination in (
        ("observed", raw_records, observed),
        ("planned", expected_list or [], planned),
    ):
        for index, row in enumerate(source):
            try:
                key = run_key(row)
            except (ValueError, TypeError, AttributeError) as error:
                blockers.append(
                    {"code": f"invalid_{label}_identity", "index": index, "detail": str(error)}
                )
                continue
            if key in destination:
                blockers.append({"code": f"duplicate_{label}_identity", "run": list(key)})
                continue
            destination[key] = row
            if row.get("phase", phase) != phase:
                blockers.append(
                    {"code": "mixed_phases", "run": list(key), "detail": str(row.get("phase"))}
                )
            if label == "planned" and "analysis_stratum" in row:
                value = row["analysis_stratum"]
                if not isinstance(value, str) or not value.strip():
                    blockers.append(
                        {
                            "code": "invalid_planned_metadata",
                            "run": list(key),
                            "detail": "analysis_stratum",
                        }
                    )
    if expected_list is None:
        (blockers if phase == "main" else warnings).append(
            {
                "code": "expected_manifest_missing",
                "detail": "Unstarted runs and the intended denominator cannot be inferred from result files",
            }
        )
    elif not planned:
        blockers.append({"code": "expected_manifest_empty"})
    missing = sorted(set(planned) - set(observed))
    unexpected = sorted(set(observed) - set(planned)) if expected_list is not None else []
    for code, keys in (("missing_planned_run", missing), ("unexpected_run", unexpected)):
        blockers.extend({"code": code, "run": list(key)} for key in keys)
    task_metadata: dict[str, set[tuple]] = defaultdict(set)
    family_assignments: dict[str, set[tuple]] = defaultdict(set)
    for key, row in observed.items():
        try:
            metadata = _row_metadata(row)
        except ValueError as error:
            blockers.append(
                {"code": "missing_task_metadata", "run": list(key), "detail": str(error)}
            )
        else:
            task_metadata[row["task_id"]].add(metadata)
            family, rating, stratum, explicit = metadata
            family_assignments[family].add((rating, stratum, explicit))
        for field in ("family_id", "rating_band"):
            if field in planned.get(key, {}) and row.get(field) != planned[key][field]:
                blockers.append(
                    {"code": "planned_metadata_mismatch", "run": list(key), "detail": field}
                )
        if key in planned and (
            ("analysis_stratum" in row) != ("analysis_stratum" in planned[key])
            or row.get("analysis_stratum") != planned[key].get("analysis_stratum")
        ):
            blockers.append(
                {
                    "code": "planned_metadata_mismatch",
                    "run": list(key),
                    "detail": "analysis_stratum",
                }
            )
        if not _scored(row):
            blockers.append(
                {
                    "code": "unscored_run",
                    "run": list(key),
                    "detail": "Resolve external failures; otherwise score the final source, including agent budget exhaustion",
                }
            )
        elif _budget_exit(row) and row.get("valid_run") is not True:
            warnings.append(
                {"code": "budget_outcome_counted_despite_legacy_valid_flag", "run": list(key)}
            )
        for field in ("model_cost_usd", "solve_seconds", "evaluation_seconds"):
            if not _number(row.get(field)):
                warnings.append({"code": "missing_measurement", "run": list(key), "detail": field})
        if row.get("cost_is_upper_bound"):
            warnings.append(
                {
                    "code": "cost_is_conservative_upper_bound",
                    "run": list(key),
                    "detail": "Unsettled request reservations are not exact billed usage",
                }
            )
    for task, metadata in task_metadata.items():
        if len(metadata) > 1:
            blockers.append({"code": "inconsistent_task_metadata", "detail": task})
    for family, assignments in family_assignments.items():
        if len(assignments) > 1:
            blockers.append({"code": "inconsistent_family_stratum", "detail": family})

    models = sorted({key[0] for key in set(observed) | set(planned)})
    model_summaries = {}
    for model in models:
        rows = [row for key, row in observed.items() if key[0] == model]
        by_condition: dict[str, list[dict]] = defaultdict(list)
        for row in rows:
            by_condition[row["condition"]].append(row)
        model_blockers = [
            b
            for b in blockers
            if b.get("model", model) == model and ("run" not in b or b["run"][0] == model)
        ]
        main_effect = {
            "status": "not_requested",
            "reason": "Model screens and calibration are not the main treatment-effect study",
        }
        if phase == "main":
            main_effect = (
                {"status": "blocked", "blockers": model_blockers}
                if model_blockers
                else _paired_effect(rows, conditions, bootstrap_draws, seed, confidence_level)
            )
            if not model_blockers and main_effect["status"] == "blocked":
                model_blockers = [
                    {"code": "invalid_paired_design", "model": model, "detail": detail}
                    for detail in main_effect["blockers"]
                ]
                blockers.extend(model_blockers)
        complete = expected_list is not None and not model_blockers
        metrics = {
            condition: _condition_metrics(group, complete=complete)
            for condition, group in sorted(by_condition.items())
        }
        for condition, condition_metrics in metrics.items():
            condition_metrics["success_is_provisional"] = phase != "main" or not complete
            condition_metrics["success_interval"] = _descriptive_success_interval(
                by_condition[condition],
                phase=phase,
                complete=complete,
                draws=bootstrap_draws,
                seed=seed,
                confidence_level=descriptive_confidence_level,
            )
            condition_metrics["task_averaged_success_confidence_level"] = (
                descriptive_confidence_level
            )
            condition_metrics["task_averaged_success_confidence_interval_percent"] = (
                condition_metrics["success_interval"]["confidence_interval_percent"]
            )
            condition_metrics["task_averaged_success_conservative_confidence_interval_percent"] = (
                condition_metrics["success_interval"]["conservative_confidence_interval_percent"]
            )
            condition_metrics["task_averaged_success_ci95_percent"] = condition_metrics[
                "success_interval"
            ]["ci95_percent"]
            condition_metrics["task_averaged_success_conservative_ci95_percent"] = (
                condition_metrics["success_interval"]["conservative_ci95_percent"]
            )
        projections = _projections(
            metrics, conditions, workers=workers, per_run_cap_usd=per_run_cap_usd
        )
        for projection in projections:
            projection["based_on_complete_planned_data"] = complete
            if not complete:
                projection["notes"].append(
                    "These calibration projections are provisional: the planned denominator is unknown or has unresolved blockers."
                )
        model_summaries[model] = {
            "planned_runs": sum(key[0] == model for key in planned)
            if expected_list is not None
            else None,
            "observed_unique_runs": len(rows),
            "scored_runs": sum(_scored(row) for row in rows),
            "complete": complete,
            "conditions": metrics,
            "paired_effect": main_effect,
            "main_workload_projections": projections,
        }
    if expected_list is None or blockers:
        for model, model_summary in model_summaries.items():
            for condition, metrics in model_summary["conditions"].items():
                group = [
                    row
                    for key, row in observed.items()
                    if key[0] == model and row["condition"] == condition
                ]
                metrics["repeated_benchmark_scores"] = repetition_score_summary(
                    group, complete=False
                )
    return {
        "schema_version": 1,
        "phase": phase,
        "planned_conditions": list(conditions),
        "confidence_level": confidence_level,
        "descriptive_confidence_level": descriptive_confidence_level,
        "planned_runs": len(planned) if expected_list is not None else None,
        "observed_result_records": len(raw_records),
        "observed_unique_runs": len(observed),
        "scored_runs": sum(_scored(row) for row in observed.values()),
        "completeness_known": expected_list is not None,
        "complete": expected_list is not None and not blockers,
        "missing_runs": [list(key) for key in missing],
        "unexpected_runs": [list(key) for key in unexpected],
        "blockers": blockers,
        "warnings": warnings,
        "models": model_summaries,
        "observed_model_spend_usd": sum(
            row["model_cost_usd"] for row in observed.values() if _number(row.get("model_cost_usd"))
        ),
        "observed_model_spend_is_upper_bound": any(
            row.get("cost_is_upper_bound") for row in observed.values()
        ),
        "spend_note": "Resolved results only. Add billed superseded attempts from the controller ledger before reconciling total project spend. Amounts tagged cost_is_upper_bound include conservative unsettled reservations, not exact billed usage.",
    }


def _payload_rows(payload: Any) -> list[dict]:
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        if "task_id" in payload and "condition" in payload:
            return [payload]
        for key in ("runs", "results", "planned_runs", "jobs"):
            if isinstance(payload.get(key), list):
                return payload[key]
    raise ValueError(
        "Expected a run object, a run list, or an object containing a runs/results/planned_runs/jobs list"
    )


def load_records(paths: Iterable[str | Path]) -> list[dict]:
    records = []
    for supplied in paths:
        path = Path(supplied)
        files = sorted(path.rglob("result.json")) if path.is_dir() else [path]
        if not files:
            raise ValueError(f"No result.json files below {path}")
        for file in files:
            if file.suffix == ".jsonl":
                for line in file.read_text(encoding="utf-8-sig").splitlines():
                    if line.strip():
                        records.extend(_payload_rows(json.loads(line)))
            else:
                records.extend(_payload_rows(json.loads(file.read_text(encoding="utf-8-sig"))))
    return records


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--results",
        nargs="+",
        required=True,
        help="Run JSON/JSONL files or directories containing result.json",
    )
    parser.add_argument(
        "--expected", help="Frozen list of all planned run identities, including unstarted runs"
    )
    parser.add_argument("--phase", choices=PHASES, default="calibration")
    parser.add_argument("--conditions", nargs=2, default=("baseline", "verifier"))
    parser.add_argument("--bootstrap-draws", type=int, default=10_000)
    parser.add_argument("--seed", type=int, default=20261123)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--per-run-cap-usd", type=float)
    parser.add_argument(
        "--confidence-level",
        type=float,
        default=0.95,
        help="Main contrast interval coverage; .975 for two Bonferroni co-primary contrasts",
    )
    parser.add_argument("--descriptive-confidence-level", type=float, default=0.95)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        expected = load_records([args.expected]) if args.expected else None
        summary = analyze(
            load_records(args.results),
            expected,
            phase=args.phase,
            bootstrap_draws=args.bootstrap_draws,
            seed=args.seed,
            conditions=tuple(args.conditions),
            workers=args.workers,
            per_run_cap_usd=args.per_run_cap_usd,
            confidence_level=args.confidence_level,
            descriptive_confidence_level=args.descriptive_confidence_level,
        )
    except (OSError, ValueError, TypeError) as error:
        parser.error(str(error))
    rendered = json.dumps(summary, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 2 if summary["blockers"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
