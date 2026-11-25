"""Checks for denominators, clustered inference, and budget projections."""

import json
import math
from pathlib import Path
import tempfile
import unittest

from experiments.analysis import (
    _descriptive_success_interval, _paired_effect, analyze, load_records, main,
    repetition_score_summary,
)


def result(task, condition, passed, repetition=0, *, family=None, band="2000-2399", model="test-model", **extra):
    row = {
        "model": model, "task_id": task, "family_id": family or task,
        "rating_band": band, "condition": condition, "repetition": repetition,
        "hidden_passed": passed, "valid_run": True, "infrastructure_error": None,
        "model_cost_usd": .10 if condition == "baseline" else .20,
        "solve_seconds": 10.0 if condition == "baseline" else 20.0,
        "evaluation_seconds": 2.0, "tool_events": [], "exit_status": "Submitted",
    }
    row.update(extra)
    return row


def fixtures(repetitions=2):
    # Four independent families per stratum, with positive, negative, and zero
    # effects. Repeating identical outcomes must not narrow a family-based CI.
    rows = []
    for band in ("2000-2399", "2400+"):
        for i, outcomes in enumerate(((False, True), (True, False), (False, False), (True, True))):
            for repetition in range(repetitions):
                for condition, passed in zip(("baseline", "verifier"), outcomes):
                    rows.append(result(f"{band}-{i}", condition, passed, repetition, band=band))
    return rows


def planned(rows):
    fields = ("model", "task_id", "family_id", "rating_band", "condition", "repetition")
    specs = []
    for row in rows:
        spec = {field: row[field] for field in fields}
        if "analysis_stratum" in row:
            spec["analysis_stratum"] = row["analysis_stratum"]
        specs.append(spec)
    return specs


def host_fixtures(repetitions=2, *, varying=False):
    # 60/40 task allocation across hosts, 50/50 across ratings. If resampling
    # ignores hosts, the constant-within-host outcomes can vary spuriously.
    rows = []
    for band in ("2000-2399", "2400+"):
        for host, count, outcomes in (("ours", 3, (False, True)), ("friend", 2, (True, False))):
            for task in range(count):
                values = (False, False) if varying and task == 0 else outcomes
                for repetition in range(repetitions):
                    for arm, passed in zip(("baseline", "verifier"), values):
                        rows.append(result(f"{host}-{band}-{task}", arm, passed, repetition,
                                           band=band, analysis_stratum=f"{host}:{band}"))
    return rows


class DenominatorTests(unittest.TestCase):
    def test_missing_unstarted_run_blocks_primary_effect(self):
        rows = fixtures()
        report = analyze(rows[:-1], planned(rows), phase="main", bootstrap_draws=100)
        self.assertFalse(report["complete"])
        self.assertEqual(len(report["missing_runs"]), 1)
        self.assertEqual(report["models"]["test-model"]["paired_effect"]["status"], "blocked")

    def test_budget_expiry_counts_last_scored_source_even_with_legacy_flag(self):
        rows = fixtures()
        rows[0].update(exit_status="budget_exhausted", valid_run=False, hidden_passed=False)
        report = analyze(rows, planned(rows), phase="main", bootstrap_draws=100)
        self.assertTrue(report["complete"])
        self.assertEqual(report["scored_runs"], len(rows))
        baseline = report["models"]["test-model"]["conditions"]["baseline"]
        self.assertEqual(baseline["budget_exhausted_scored_runs"], 1)
        self.assertTrue(any(w["code"] == "budget_outcome_counted_despite_legacy_valid_flag" for w in report["warnings"]))

    def test_infrastructure_failure_is_not_an_agent_failure_or_a_dropped_run(self):
        rows = fixtures()
        rows[0]["infrastructure_error"] = "worker unavailable"
        report = analyze(rows, planned(rows), phase="main", bootstrap_draws=100)
        self.assertFalse(report["complete"])
        self.assertEqual(report["scored_runs"], len(rows) - 1)
        self.assertTrue(any(b["code"] == "unscored_run" for b in report["blockers"]))

    def test_duplicate_attempt_cannot_be_counted_as_another_repetition(self):
        rows = fixtures()
        duplicate = dict(rows[0], hidden_passed=not rows[0]["hidden_passed"])
        report = analyze(rows + [duplicate], planned(rows), phase="main", bootstrap_draws=100)
        self.assertFalse(report["complete"])
        self.assertEqual(report["observed_unique_runs"], len(rows))
        self.assertTrue(any(b["code"] == "duplicate_observed_identity" for b in report["blockers"]))

    def test_main_needs_planned_denominator_not_just_observed_results(self):
        report = analyze(fixtures(), phase="main", bootstrap_draws=100)
        self.assertFalse(report["completeness_known"])
        self.assertTrue(any(b["code"] == "expected_manifest_missing" for b in report["blockers"]))

    def test_changed_family_metadata_blocks_inference(self):
        rows = fixtures()
        expected = planned(rows)
        rows[0]["family_id"] = "another-family"
        report = analyze(rows, expected, phase="main", bootstrap_draws=100)
        self.assertFalse(report["complete"])
        self.assertTrue(any(b["code"] == "planned_metadata_mismatch" for b in report["blockers"]))

    def test_planned_main_design_with_only_one_arm_is_blocked(self):
        rows = [row for row in fixtures() if row["condition"] == "baseline"]
        report = analyze(rows, planned(rows), phase="main", bootstrap_draws=100)
        self.assertFalse(report["complete"])
        self.assertFalse(report["models"]["test-model"]["complete"])
        self.assertTrue(any(b["code"] == "invalid_paired_design" for b in report["blockers"]))

    def test_missing_measurements_do_not_invalidate_a_scored_outcome(self):
        rows = fixtures()
        del rows[0]["model_cost_usd"]
        report = analyze(rows, planned(rows), phase="main", bootstrap_draws=100)
        self.assertTrue(report["complete"])
        self.assertEqual(report["models"]["test-model"]["paired_effect"]["status"], "ok")
        self.assertEqual(report["models"]["test-model"]["main_workload_projections"][0]["status"], "unavailable")


class RepeatedBenchmarkScoreTests(unittest.TestCase):
    def test_round_scores_mean_and_sample_dispersion_use_benchmark_percentages(self):
        rows = [result(str(task), "baseline", task < successes, repetition)
                for repetition, successes in enumerate((1, 2, 3)) for task in range(4)]
        summary = repetition_score_summary(rows, complete=True)
        self.assertEqual(summary["status"], "ok")
        self.assertEqual(summary["scores_percent"], [25, 50, 75])
        self.assertEqual(summary["mean_score_percent"], 50)
        self.assertEqual(summary["sample_variance_percentage_points_squared"], 625)
        self.assertEqual(summary["sample_sd_percentage_points"], 25)
        self.assertEqual(summary["variance_ddof"], 1)
        self.assertTrue(summary["variance_estimable"])
        self.assertTrue(any("3 repetitions provide only 2 variance degrees of freedom" in warning for warning in summary["warnings"]))

    def test_five_rounds_report_four_variance_degrees_of_freedom(self):
        rows = [result(str(task), "baseline", task < successes, repetition)
                for repetition, successes in enumerate(range(1, 6), start=1)
                for task in range(5)]
        summary = repetition_score_summary(rows, complete=True)
        self.assertEqual(summary["scores_percent"], [20, 40, 60, 80, 100])
        self.assertEqual(summary["mean_score_percent"], 60)
        self.assertEqual(summary["sample_variance_percentage_points_squared"], 1000)
        self.assertTrue(any("5 repetitions provide only 4 variance degrees of freedom" in warning
                            for warning in summary["warnings"]))

    def test_constant_mixed_task_rounds_have_zero_round_variance(self):
        rows = [result(task, "baseline", passed, repetition)
                for repetition in range(3) for task, passed in (("a", True), ("b", False))]
        summary = repetition_score_summary(rows, complete=True)
        self.assertEqual(summary["scores_percent"], [50, 50, 50])
        self.assertEqual(summary["sample_variance_percentage_points_squared"], 0)
        self.assertEqual(summary["sample_sd_percentage_points"], 0)

    def test_one_round_reports_score_but_cannot_estimate_variance(self):
        summary = repetition_score_summary([result("a", "baseline", True),
                                            result("b", "baseline", False)], complete=True)
        self.assertEqual(summary["mean_score_percent"], 50)
        self.assertIsNone(summary["sample_sd_percentage_points"])
        self.assertIsNone(summary["sample_variance_percentage_points_squared"])
        self.assertFalse(summary["variance_estimable"])

    def test_different_task_sets_block_even_when_counts_and_families_match(self):
        rows = [result("a", "baseline", True, 0, family="shared"),
                result("b", "baseline", False, 0, family="shared"),
                result("a", "baseline", True, 1, family="shared"),
                result("c", "baseline", False, 1, family="shared")]
        summary = repetition_score_summary(rows, complete=True)
        self.assertEqual(summary["status"], "blocked")
        self.assertIsNone(summary["scores_percent"])
        self.assertIsNone(summary["mean_score_percent"])
        self.assertIsNone(summary["sample_sd_percentage_points"])
        self.assertTrue(all(row["score_percent"] is None for row in summary["rounds"]))
        self.assertEqual([row["provisional_score_percent"] for row in summary["rounds"]], [50, 50])

    def test_infrastructure_failure_is_not_silently_removed_from_a_round(self):
        rows = [result(task, "baseline", passed, repetition)
                for repetition in range(2) for task, passed in (("a", True), ("b", False))]
        rows[1].update(valid_run=False, infrastructure_error={"type": "WorkerUnavailable"})
        summary = repetition_score_summary(rows, complete=True)
        self.assertEqual(summary["status"], "blocked")
        self.assertEqual(summary["rounds"][0]["observed_runs"], 2)
        self.assertEqual(summary["rounds"][0]["scored_runs"], 1)
        self.assertTrue(summary["rounds"][0]["provisional"])
        self.assertIsNone(summary["mean_score_percent"])
        self.assertIsNone(summary["sample_variance_percentage_points_squared"])

    def test_budget_exit_keeps_the_last_saved_source_score_in_its_round(self):
        rows = [result(task, "baseline", passed, repetition)
                for repetition in range(2) for task, passed in (("a", True), ("b", False))]
        rows[1].update(valid_run=False, exit_status="budget_exhausted")
        summary = repetition_score_summary(rows, complete=True)
        self.assertEqual(summary["status"], "ok")
        self.assertEqual(summary["scores_percent"], [50, 50])

    def test_duplicate_identity_blocks_instead_of_changing_the_round_score(self):
        rows = [result("a", "baseline", True), result("b", "baseline", False)]
        summary = repetition_score_summary(rows + [dict(rows[0])], complete=True)
        self.assertEqual(summary["status"], "blocked")
        self.assertIsNone(summary["rounds"][0]["provisional_score_percent"])
        self.assertIsNone(summary["mean_score_percent"])

    def test_whole_unstarted_repetition_requires_the_planned_denominator(self):
        all_rows = fixtures(3)
        rows = [row for row in all_rows if row["repetition"] != 2]
        report = analyze(rows, planned(all_rows), phase="main", bootstrap_draws=100)
        for metrics in report["models"]["test-model"]["conditions"].values():
            summary = metrics["repeated_benchmark_scores"]
            self.assertEqual(summary["status"], "blocked")
            self.assertIsNone(summary["mean_score_percent"])
            self.assertIsNone(summary["sample_sd_percentage_points"])
            self.assertEqual(len(summary["rounds"]), 2)

    def test_unknown_manifest_keeps_only_provisional_round_diagnostics(self):
        report = analyze(fixtures(3), phase="calibration", bootstrap_draws=100)
        summary = report["models"]["test-model"]["conditions"]["baseline"]["repeated_benchmark_scores"]
        self.assertEqual(summary["status"], "blocked")
        self.assertIsNone(summary["mean_score_percent"])
        self.assertTrue(all(row["provisional"] for row in summary["rounds"]))

    def test_existing_metadata_blocker_suppresses_otherwise_balanced_scores(self):
        rows = fixtures(3)
        expected = planned(rows)
        rows[0]["family_id"] = "changed-family"
        report = analyze(rows, expected, phase="main", bootstrap_draws=100)
        for metrics in report["models"]["test-model"]["conditions"].values():
            self.assertEqual(metrics["repeated_benchmark_scores"]["status"], "blocked")
            self.assertIsNone(metrics["repeated_benchmark_scores"]["mean_score_percent"])

    def test_complete_balanced_analysis_exports_round_scores_beside_family_ci(self):
        rows = fixtures(3)
        report = analyze(rows, planned(rows), phase="main", bootstrap_draws=100)
        metrics = report["models"]["test-model"]["conditions"]["baseline"]
        summary = metrics["repeated_benchmark_scores"]
        self.assertEqual(summary["scores_percent"], [50, 50, 50])
        self.assertEqual(summary["mean_score_percent"], metrics["task_averaged_success_percent"])
        self.assertEqual(summary["sample_sd_percentage_points"], 0)
        self.assertIsNotNone(metrics["success_interval"]["confidence_interval_percent"])


class InferenceTests(unittest.TestCase):
    def test_task_averaging_gives_each_task_equal_weight_despite_repetition_count(self):
        rows = []
        for repetition in range(20):
            rows.extend([result("many-repeats", "baseline", False, repetition),
                         result("many-repeats", "verifier", True, repetition)])
        rows.extend([result("one-repeat", "baseline", False), result("one-repeat", "verifier", False)])
        report = analyze(rows, planned(rows), phase="main", bootstrap_draws=100)
        effect = report["models"]["test-model"]["paired_effect"]
        self.assertEqual(effect["difference_percentage_points"]["estimate"], 50)
        self.assertEqual(effect["task_count"], 2)
        summary = report["models"]["test-model"]["conditions"]["baseline"]["repeated_benchmark_scores"]
        self.assertEqual(summary["status"], "blocked")
        self.assertIsNone(summary["mean_score_percent"])

    def test_duplicating_repetitions_with_identical_task_means_does_not_narrow_ci(self):
        reports = [analyze(rows, planned(rows), phase="main", bootstrap_draws=400, seed=3)
                   for rows in (fixtures(1), fixtures(10))]
        effects = [r["models"]["test-model"]["paired_effect"] for r in reports]
        self.assertEqual(effects[0]["difference_percentage_points"], effects[1]["difference_percentage_points"])
        self.assertEqual(effects[0]["family_count"], 8)
        self.assertEqual(effects[0]["family_counts_by_rating_band"], {"2000-2399": 4, "2400+": 4})

    def test_shared_family_members_are_resampled_together(self):
        rows = []
        for family, outcomes in (("good", (False, True)), ("bad", (True, False))):
            for variant in range(5):
                for arm, passed in zip(("baseline", "verifier"), outcomes):
                    rows.append(result(f"{family}-{variant}", arm, passed, family=family))
        report = analyze(rows, planned(rows), phase="main", bootstrap_draws=400)
        effect = report["models"]["test-model"]["paired_effect"]
        self.assertEqual(effect["family_count"], 2)
        self.assertEqual(effect["task_count"], 10)
        self.assertEqual(effect["difference_percentage_points"]["ci95"], [-100.0, 100.0])

    def test_rating_distribution_keeps_original_task_weights_in_cluster_draws(self):
        rows = []
        for i in range(2):
            for arm, passed in (("baseline", False), ("verifier", True)):
                rows.append(result(f"lower-{i}", arm, passed))
        for i in range(6):
            for arm, passed in (("baseline", True), ("verifier", False)):
                rows.append(result(f"higher-{i}", arm, passed, band="2400+"))
        report = analyze(rows, planned(rows), phase="main", bootstrap_draws=100)
        effect = report["models"]["test-model"]["paired_effect"]
        self.assertEqual(effect["difference_percentage_points"]["estimate"], -50)
        self.assertEqual(effect["difference_percentage_points"]["bootstrap_percentile_bounds"], [-50, -50])

    def test_unequal_family_sizes_do_not_change_frozen_stratum_weights(self):
        rows = []
        for task, family, outcomes in (("good-1", "good", (False, True)),
                                       ("good-2", "good", (False, True)),
                                       ("bad", "bad", (True, False))):
            for arm, passed in zip(("baseline", "verifier"), outcomes):
                rows.append(result(task, arm, passed, family=family))
        for task in ("higher-1", "higher-2"):
            for arm in ("baseline", "verifier"):
                rows.append(result(task, arm, False, band="2400+"))
        effect = analyze(rows, planned(rows), phase="main", bootstrap_draws=400)["models"]["test-model"]["paired_effect"]
        self.assertAlmostEqual(effect["difference_percentage_points"]["estimate"], 20)
        self.assertEqual(effect["difference_percentage_points"]["ci95"], [-60, 60])

    def test_degenerate_bootstrap_is_flagged_and_not_published_as_zero_width_ci(self):
        rows = fixtures()
        for row in rows:
            row["hidden_passed"] = True
        report = analyze(rows, planned(rows), phase="main", bootstrap_draws=100)
        effect = report["models"]["test-model"]["paired_effect"]
        self.assertEqual(effect["difference_percentage_points"]["estimate"], 0)
        self.assertIsNone(effect["difference_percentage_points"]["ci95"])
        self.assertTrue(effect["difference_percentage_points"]["bootstrap_degenerate"])
        self.assertIsNone(effect["arm_success_percent"]["baseline"]["ci95"])

    def test_single_family_stratum_cannot_estimate_its_family_uncertainty(self):
        rows = [result("a", "baseline", False), result("a", "verifier", True),
                result("b", "baseline", True, band="2400+"), result("b", "verifier", False, band="2400+")]
        effect = analyze(rows, planned(rows), phase="main", bootstrap_draws=100)["models"]["test-model"]["paired_effect"]
        self.assertIsNone(effect["difference_percentage_points"]["ci95"])
        self.assertTrue(any("fewer than two families" in warning for warning in effect["warnings"]))

    def test_model_screens_and_calibration_do_not_report_main_effect_cis(self):
        for phase in ("model_screen", "calibration"):
            report = analyze(fixtures(), phase=phase, bootstrap_draws=100)
            effect = report["models"]["test-model"]["paired_effect"]
            self.assertEqual(effect["status"], "not_requested")
            self.assertNotIn("difference_percentage_points", effect)

    def test_six_family_model_screen_gets_exploratory_arm_ci_and_small_sample_warning(self):
        rows = []
        for model in ("model-1", "model-2", "model-3"):
            for band in ("2000-2399", "2400+"):
                for task_number, passed in enumerate((True, False, True)):
                    for repetition in range(2):
                        rows.append(result(f"{band}-{task_number}", "baseline", passed,
                                           repetition, model=model, band=band))
        report = analyze(rows, planned(rows), phase="model_screen", bootstrap_draws=400)
        for model in report["models"].values():
            metrics = model["conditions"]["baseline"]
            interval = metrics["success_interval"]
            self.assertEqual(interval["status"], "exploratory")
            self.assertEqual(interval["family_count"], 6)
            self.assertEqual(interval["family_counts_by_rating_band"], {"2000-2399": 3, "2400+": 3})
            self.assertIsNotNone(interval["ci95_percent"])
            self.assertEqual(metrics["task_averaged_success_ci95_percent"], interval["ci95_percent"])
            self.assertTrue(metrics["success_is_provisional"])
            self.assertTrue(any("Fewer than 20" in warning for warning in interval["warnings"]))
            self.assertTrue(any("not simultaneous" in warning for warning in interval["warnings"]))
            self.assertEqual(model["paired_effect"]["status"], "not_requested")

    def test_calibration_ci_retains_repetitions_in_their_task_cluster(self):
        intervals = []
        for rows in (fixtures(1), fixtures(8)):
            report = analyze(rows, planned(rows), phase="calibration", bootstrap_draws=400)
            intervals.append(report["models"]["test-model"]["conditions"]["baseline"]["success_interval"])
        self.assertEqual(intervals[0]["ci95_percent"], intervals[1]["ci95_percent"])
        self.assertEqual(intervals[0]["family_count"], 8)

    def test_incomplete_calibration_does_not_publish_subset_ci(self):
        rows = fixtures()
        report = analyze(rows[:-1], planned(rows), phase="calibration", bootstrap_draws=100)
        interval = report["models"]["test-model"]["conditions"]["baseline"]["success_interval"]
        self.assertEqual(interval["status"], "blocked")
        self.assertIsNone(interval["ci95_percent"])

    def test_all_pass_calibration_does_not_claim_zero_width_ci(self):
        rows = [dict(row, hidden_passed=True) for row in fixtures()]
        report = analyze(rows, planned(rows), phase="calibration", bootstrap_draws=100)
        interval = report["models"]["test-model"]["conditions"]["baseline"]["success_interval"]
        self.assertEqual(interval["estimate_percent"], 100)
        self.assertTrue(interval["bootstrap_degenerate"])
        self.assertIsNone(interval["ci95_percent"])

    def test_six_all_pass_families_get_wide_conservative_fallback(self):
        rows = []
        for band in ("2000-2399", "2400+"):
            for task in range(3):
                for repetition in range(2):
                    rows.append(result(f"{band}-{task}", "baseline", True, repetition, band=band))
        interval = analyze(rows, planned(rows), phase="model_screen", bootstrap_draws=100)["models"]["test-model"]["conditions"]["baseline"]["success_interval"]
        self.assertTrue(interval["bootstrap_degenerate"])
        self.assertIsNone(interval["ci95_percent"])
        self.assertEqual(interval["ci_method"], "hoeffding_conservative_fallback")
        low, high = interval["conservative_ci95_percent"]
        self.assertAlmostEqual(low, 44.556, places=3)
        self.assertEqual(high, 100)

    def test_hundred_equal_effect_families_get_conservative_27_point_bounds(self):
        rows = []
        for task in range(100):
            band = "2000-2399" if task < 50 else "2400+"
            for repetition in range(2):
                for arm in ("baseline", "verifier"):
                    rows.append(result(str(task), arm, False, repetition, band=band))
        effect = analyze(rows, planned(rows), phase="main", bootstrap_draws=100)["models"]["test-model"]["paired_effect"]["difference_percentage_points"]
        self.assertTrue(effect["bootstrap_degenerate"])
        self.assertIsNone(effect["ci95"])
        self.assertEqual(effect["ci_method"], "hoeffding_conservative_fallback")
        low, high = effect["conservative_ci95"]
        self.assertAlmostEqual(low, -27.162, places=3)
        self.assertAlmostEqual(high, 27.162, places=3)

    def test_fallback_is_not_used_for_unequal_family_sizes(self):
        rows = []
        for task, family in (("a1", "a"), ("a2", "a"), ("b", "b")):
            for arm in ("baseline", "verifier"):
                rows.append(result(task, arm, False, family=family))
        report = analyze(rows, planned(rows), phase="main", bootstrap_draws=100)
        effect = report["models"]["test-model"]["paired_effect"]["difference_percentage_points"]
        self.assertTrue(effect["bootstrap_degenerate"])
        self.assertIsNone(effect["conservative_ci95"])
        self.assertIsNone(effect["ci_method"])
        self.assertIsNone(report["models"]["test-model"]["conditions"]["baseline"]["success_interval"]["conservative_ci95_percent"])

    def test_normal_bootstrap_keeps_its_method_and_needs_no_fallback(self):
        rows = fixtures()
        effect = analyze(rows, planned(rows), phase="main", bootstrap_draws=400)["models"]["test-model"]["paired_effect"]["difference_percentage_points"]
        self.assertFalse(effect["bootstrap_degenerate"])
        self.assertEqual(effect["ci_method"], "family_cluster_percentile_bootstrap")
        self.assertIsNone(effect["conservative_ci95"])

    def test_bonferroni_coverage_has_general_fields_and_no_mislabelled_ci95(self):
        rows = fixtures()
        regular = analyze(rows, planned(rows), phase="main", bootstrap_draws=1000, seed=7)
        adjusted = analyze(rows, planned(rows), phase="main", bootstrap_draws=1000, seed=7, confidence_level=.975)
        first = regular["models"]["test-model"]["paired_effect"]["difference_percentage_points"]
        second = adjusted["models"]["test-model"]["paired_effect"]["difference_percentage_points"]
        self.assertEqual(second["confidence_level"], .975)
        self.assertIsNone(second["ci95"])
        self.assertLessEqual(second["confidence_interval"][0], first["confidence_interval"][0])
        self.assertGreaterEqual(second["confidence_interval"][1], first["confidence_interval"][1])
        descriptive = adjusted["models"]["test-model"]["conditions"]["baseline"]["success_interval"]
        self.assertEqual(descriptive["confidence_level"], .95)
        self.assertIsNotNone(descriptive["ci95_percent"])

    def test_hoeffding_fallback_obeys_requested_coverage(self):
        rows = [dict(row, hidden_passed=True) for row in fixtures()]
        reports = [analyze(rows, planned(rows), phase="main", bootstrap_draws=100, confidence_level=level)
                   for level in (.95, .975)]
        bounds = [report["models"]["test-model"]["paired_effect"]["difference_percentage_points"] for report in reports]
        self.assertLess(bounds[1]["conservative_confidence_interval"][0], bounds[0]["conservative_confidence_interval"][0])
        self.assertGreater(bounds[1]["conservative_confidence_interval"][1], bounds[0]["conservative_confidence_interval"][1])
        self.assertIsNone(bounds[1]["conservative_ci95"])
        self.assertEqual(bounds[1]["ci_method"], "hoeffding_conservative_fallback")

    def test_non95_descriptive_interval_uses_accurate_field_names(self):
        rows = fixtures()
        report = analyze(rows, planned(rows), phase="calibration", bootstrap_draws=100,
                         descriptive_confidence_level=.975)
        interval = report["models"]["test-model"]["conditions"]["baseline"]["success_interval"]
        self.assertEqual(interval["confidence_level"], .975)
        self.assertIsNone(interval["ci95_percent"])
        self.assertIsNotNone(interval["confidence_interval_percent"])

    def test_invalid_confidence_levels_are_rejected(self):
        for level in (0, 1, -.1, float("nan"), True):
            with self.assertRaises(ValueError):
                analyze([], confidence_level=level)

    def test_different_models_are_not_pooled(self):
        rows = fixtures()
        other = [dict(row, model="other-model", hidden_passed=True) for row in rows]
        report = analyze(rows + other, planned(rows + other), phase="main", bootstrap_draws=100)
        self.assertEqual(set(report["models"]), {"test-model", "other-model"})
        self.assertEqual(report["models"]["test-model"]["paired_effect"]["task_count"], 8)


class HostBlockedInferenceTests(unittest.TestCase):
    def test_host_by_rating_bootstrap_preserves_60_40_task_weights(self):
        rows = host_fixtures()
        report = analyze(rows, planned(rows), phase="main", bootstrap_draws=200)
        self.assertTrue(report["complete"])
        model = report["models"]["test-model"]
        effect = model["paired_effect"]
        self.assertAlmostEqual(effect["difference_percentage_points"]["estimate"], 20)
        for bound in effect["difference_percentage_points"]["bootstrap_percentile_bounds"]:
            self.assertAlmostEqual(bound, 20)
        self.assertEqual(effect["family_counts_by_rating_band"], {"2000-2399": 5, "2400+": 5})
        counts = {f"{host}:{band}": n for host, n in (("ours", 3), ("friend", 2))
                  for band in ("2000-2399", "2400+")}
        self.assertEqual(effect["family_counts_by_analysis_stratum"], counts)
        self.assertEqual(effect["task_counts_by_analysis_stratum"], counts)
        self.assertEqual(effect["analysis_stratum_task_weights"], {s: n / 10 for s, n in counts.items()})
        self.assertIn("fixed execution-host", effect["inference_scope"])
        for arm, expected in (("baseline", 40), ("verifier", 60)):
            interval = model["conditions"][arm]["success_interval"]
            self.assertAlmostEqual(interval["estimate_percent"], expected)
            for bound in interval["bootstrap_percentile_bounds_percent"]:
                self.assertAlmostEqual(bound, expected)
            self.assertEqual(interval["analysis_stratum_task_weights"], effect["analysis_stratum_task_weights"])
            self.assertEqual(interval["family_counts_by_rating_band"], {"2000-2399": 5, "2400+": 5})

    def test_host_clusters_keep_repetitions_together(self):
        effects = []
        for repetitions in (1, 6):
            rows = host_fixtures(repetitions, varying=True)
            report = analyze(rows, planned(rows), phase="main", bootstrap_draws=400, seed=3)
            self.assertTrue(report["complete"])
            effect = report["models"]["test-model"]["paired_effect"]
            self.assertEqual(effect["family_count"], 10)
            effects.append(effect["difference_percentage_points"])
        self.assertEqual(effects[0], effects[1])
        self.assertFalse(effects[0]["bootstrap_degenerate"])

    def test_single_family_host_cells_suppress_bootstrap_and_use_same_fallback(self):
        rows = []
        for band in ("2000-2399", "2400+"):
            for host, outcomes in (("ours", (False, True)), ("friend", (True, False))):
                for arm, passed in zip(("baseline", "verifier"), outcomes):
                    rows.append(result(f"{host}-{band}", arm, passed, band=band,
                                       analysis_stratum=f"{host}:{band}"))
        report = analyze(rows, planned(rows), phase="main", bootstrap_draws=100)
        self.assertTrue(report["complete"])
        effect = report["models"]["test-model"]["paired_effect"]
        self.assertTrue(all(n == 1 for n in effect["family_counts_by_analysis_stratum"].values()))
        self.assertTrue(any("fewer than two families" in w for w in effect["warnings"]))
        ci = effect["difference_percentage_points"]
        self.assertIsNone(ci["confidence_interval"])
        self.assertEqual(ci["ci_method"], "hoeffding_conservative_fallback")
        self.assertAlmostEqual(ci["conservative_half_width"], 200 * math.sqrt(math.log(40) / 8))
        for condition in report["models"]["test-model"]["conditions"].values():
            self.assertIsNone(condition["success_interval"]["confidence_interval_percent"])
            self.assertEqual(condition["success_interval"]["ci_method"], "hoeffding_conservative_fallback")

    def test_frozen_analysis_assignment_checks_presence_and_value(self):
        for change in ("changed_observed", "missing_observed", "missing_planned"):
            with self.subTest(change=change):
                rows = host_fixtures()
                specs = planned(rows)
                if change == "changed_observed":
                    rows[0]["analysis_stratum"] = "friend:2000-2399"
                elif change == "missing_observed":
                    del rows[0]["analysis_stratum"]
                else:
                    del specs[0]["analysis_stratum"]
                report = analyze(rows, specs, phase="main", bootstrap_draws=100)
                self.assertFalse(report["complete"])
                self.assertTrue(any(b["code"] == "planned_metadata_mismatch" and b["detail"] == "analysis_stratum"
                                    for b in report["blockers"]))
                self.assertEqual(report["models"]["test-model"]["paired_effect"]["status"], "blocked")

    def test_paired_arms_cannot_be_assigned_to_different_hosts(self):
        rows = [result("same-task", "baseline", False, analysis_stratum="ours:2000-2399"),
                result("same-task", "verifier", True, analysis_stratum="friend:2000-2399")]
        # Even a plan containing those inconsistent assignments cannot make
        # them a valid paired source-family comparison.
        report = analyze(rows, planned(rows), phase="main", bootstrap_draws=100)
        self.assertFalse(report["complete"])
        self.assertTrue(any(b["code"] == "inconsistent_task_metadata" for b in report["blockers"]))
        self.assertEqual(_paired_effect(rows, ("baseline", "verifier"), 100, 3)["status"], "blocked")

    def test_shared_family_cannot_cross_hosts_or_mix_explicit_with_legacy_rows(self):
        for first, second in (("ours:2000-2399", "friend:2000-2399"), ("2000-2399", None)):
            with self.subTest(first=first, second=second):
                rows = []
                for task, assignment in (("variant-a", first), ("variant-b", second)):
                    for arm in ("baseline", "verifier"):
                        extra = {"analysis_stratum": assignment} if assignment is not None else {}
                        rows.append(result(task, arm, True, family="shared", **extra))
                for phase in ("calibration", "main"):
                    report = analyze(rows, planned(rows), phase=phase, bootstrap_draws=100)
                    self.assertFalse(report["complete"])
                    self.assertTrue(any(b["code"] == "inconsistent_family_stratum" for b in report["blockers"]))
                    for metrics in report["models"]["test-model"]["conditions"].values():
                        self.assertEqual(metrics["success_interval"]["status"], "blocked")
                        self.assertIsNone(metrics["repeated_benchmark_scores"]["mean_score_percent"])
                # Direct mathematical entrypoints enforce this too, before a
                # fallback could silently pool the inconsistent family.
                self.assertEqual(_paired_effect(rows, ("baseline", "verifier"), 100, 3)["status"], "blocked")
                interval = _descriptive_success_interval(
                    [r for r in rows if r["condition"] == "baseline"], phase="main", complete=True,
                    draws=100, seed=3)
                self.assertEqual(interval["status"], "blocked")
                self.assertIsNone(interval["conservative_confidence_interval_percent"])

    def test_invalid_analysis_stratum_values_block_without_crashing(self):
        for value in (None, "", "  ", 3, [], {}):
            with self.subTest(value=value):
                rows = fixtures()
                rows[0]["analysis_stratum"] = value
                report = analyze(rows, planned(rows), phase="calibration", bootstrap_draws=100)
                self.assertFalse(report["complete"])
                self.assertTrue(any(b["detail"] == "analysis_stratum" for b in report["blockers"]
                                    if b["code"] in ("missing_task_metadata", "invalid_planned_metadata")))

    def test_explicit_rating_only_strata_preserve_legacy_numeric_inference(self):
        reports = []
        for rows in (fixtures(), [dict(r, analysis_stratum=r["rating_band"]) for r in fixtures()]):
            reports.append(analyze(rows, planned(rows), phase="main", bootstrap_draws=400, seed=3))
        effects = [r["models"]["test-model"]["paired_effect"] for r in reports]
        self.assertEqual(effects[0]["difference_percentage_points"], effects[1]["difference_percentage_points"])
        self.assertEqual(effects[0]["arm_success_percent"], effects[1]["arm_success_percent"])
        self.assertEqual(effects[0]["family_counts_by_rating_band"], effects[1]["family_counts_by_rating_band"])


class ProjectionAndInputTests(unittest.TestCase):
    def test_main_run_counts_caps_and_measured_worker_hours(self):
        rows = fixtures()
        report = analyze(rows, planned(rows), per_run_cap_usd=.28, workers=4)
        r2, r3, r5, r6 = report["models"]["test-model"]["main_workload_projections"]
        self.assertEqual((r2["agent_runs"], r3["agent_runs"], r5["agent_runs"], r6["agent_runs"]), (400, 600, 1000, 1200))
        self.assertAlmostEqual(r2["model_charge_ceiling_usd"], 112)
        self.assertAlmostEqual(r3["model_charge_ceiling_usd"], 168)
        self.assertAlmostEqual(r5["model_charge_ceiling_usd"], 280)
        self.assertAlmostEqual(r6["model_charge_ceiling_usd"], 336)
        self.assertAlmostEqual(r2["model_cost_usd_at_observed_mean"], 60)
        self.assertAlmostEqual(r5["model_cost_usd_at_observed_mean"], 150)
        self.assertAlmostEqual(r2["serial_worker_seconds_at_observed_mean"], 6800)
        self.assertAlmostEqual(r2["ideal_worker_hours_at_observed_mean"], 6800 / 4 / 3600)

    def test_unsettled_cost_reservation_is_not_reported_as_exact_billed_spend(self):
        rows = fixtures()
        rows[0]["cost_is_upper_bound"] = True
        report = analyze(rows, planned(rows), bootstrap_draws=100)
        self.assertTrue(report["observed_model_spend_is_upper_bound"])
        metrics = report["models"]["test-model"]["conditions"]["baseline"]
        self.assertEqual(metrics["cost_upper_bound_runs"], 1)
        self.assertTrue(metrics["observed_model_spend_is_upper_bound"])
        self.assertTrue(report["models"]["test-model"]["main_workload_projections"][0]["cost_estimate_includes_upper_bounds"])
        self.assertTrue(any(warning["code"] == "cost_is_conservative_upper_bound" for warning in report["warnings"]))

    def test_load_jsonl_and_cli_write_explicit_missing_denominator(self):
        rows = fixtures()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            data = root / "results.jsonl"
            expected = root / "manifest.json"
            output = root / "summary.json"
            data.write_text("\n".join(json.dumps(row) for row in rows[:-1]), encoding="utf-8")
            expected.write_text(json.dumps({"runs": planned(rows)}), encoding="utf-8")
            self.assertEqual(len(load_records([data])), len(rows) - 1)
            code = main(["--results", str(data), "--expected", str(expected), "--phase", "main",
                         "--bootstrap-draws", "100", "--output", str(output)])
            self.assertEqual(code, 2)
            summary = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(summary["planned_runs"], len(rows))
            self.assertEqual(len(summary["missing_runs"]), 1)

    def test_mixed_phases_are_blocked(self):
        rows = fixtures()
        rows[0]["phase"] = "model_screen"
        report = analyze(rows, planned(rows), phase="main", bootstrap_draws=100)
        self.assertTrue(any(blocker["code"] == "mixed_phases" for blocker in report["blockers"]))


if __name__ == "__main__":
    unittest.main()
