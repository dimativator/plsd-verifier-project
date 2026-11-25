"""Checks for a shared baseline, adjusted coverage, and merged batch plans."""

import json
from pathlib import Path
import tempfile
import unittest

from experiments.test_analysis import fixtures, planned
from experiments.three_arm_analysis import analyze_three_arms, main


def three_arm_rows():
    rows = fixtures(2)
    return rows + [dict(row, condition="guided_verifier", model_cost_usd=.30)
                   for row in rows if row["condition"] == "verifier"]


class ThreeArmTests(unittest.TestCase):
    def test_two_main_contrasts_use_bonferroni_and_shared_baseline(self):
        rows = three_arm_rows()
        report = analyze_three_arms(rows, planned(rows), phase="main", bootstrap_draws=200, per_run_cap_usd=.12)
        self.assertTrue(report["complete"])
        self.assertEqual(report["multiplicity"]["per_contrast_confidence_level"], .975)
        self.assertEqual(report["observed_unique_runs"], 48)
        self.assertAlmostEqual(report["observed_model_spend_usd"], 9.6)
        self.assertEqual(len(report["contrast_analyses"]), 2)
        for contrast in report["contrast_analyses"].values():
            effect = contrast["models"]["test-model"]["paired_effect"]["difference_percentage_points"]
            self.assertEqual(effect["confidence_level"], .975)
            self.assertIsNone(effect["ci95"])
            self.assertIsNotNone(effect["confidence_interval"])
        projections = report["models"]["test-model"]["main_workload_projections"]
        self.assertEqual([p["agent_runs"] for p in projections], [600, 900, 1500, 1800])
        self.assertAlmostEqual(projections[2]["model_charge_ceiling_usd"], 180)
        self.assertAlmostEqual(projections[3]["model_charge_ceiling_usd"], 216)

    def test_calibration_keeps_arm_intervals_and_points_but_no_main_contrast_ci(self):
        rows = three_arm_rows()
        report = analyze_three_arms(rows, planned(rows), phase="calibration", bootstrap_draws=100)
        self.assertTrue(report["complete"])
        for condition in report["models"]["test-model"]["conditions"].values():
            self.assertEqual(condition["success_interval"]["confidence_level"], .95)
        for contrast in report["contrast_analyses"].values():
            model = contrast["models"]["test-model"]
            self.assertEqual(model["paired_effect"]["status"], "not_requested")
            self.assertEqual(model["descriptive_difference_percentage_points"], 0)
        self.assertNotIn("exploratory_contrasts", report)

    def test_explicit_calibration_paired_intervals_remain_exploratory(self):
        rows = three_arm_rows()
        report = analyze_three_arms(rows, planned(rows), phase="calibration", bootstrap_draws=200,
                                    exploratory_contrasts=True)
        self.assertEqual(report["phase"], "calibration")
        self.assertEqual(set(report["exploratory_contrasts"]), {"optional_vs_baseline", "guided_vs_baseline"})
        for contrast in report["exploratory_contrasts"].values():
            result = contrast["models"]["test-model"]
            self.assertEqual(result["status"], "exploratory")
            self.assertEqual(result["phase"], "calibration")
            self.assertEqual(result["difference_percentage_points"]["confidence_level"], .975)
            self.assertIsNotNone(result["difference_percentage_points"]["confidence_interval"])
            self.assertTrue(any("prior calibration outcomes were inspected" in warning for warning in result["warnings"]))
        for contrast in report["contrast_analyses"].values():
            self.assertEqual(contrast["models"]["test-model"]["paired_effect"]["status"], "not_requested")

    def test_exploratory_option_cannot_relabel_main_or_hide_missing_runs(self):
        rows = three_arm_rows()
        with self.assertRaises(ValueError):
            analyze_three_arms(rows, planned(rows), phase="main", exploratory_contrasts=True)
        report = analyze_three_arms(rows[:-1], planned(rows), phase="calibration", exploratory_contrasts=True, bootstrap_draws=100)
        for contrast in report["exploratory_contrasts"].values():
            self.assertEqual(contrast["models"]["test-model"]["status"], "blocked")

    def test_missing_guided_outcome_blocks_both_co_primary_intervals(self):
        rows = three_arm_rows()
        report = analyze_three_arms(rows[:-1], planned(rows), phase="main", bootstrap_draws=100)
        self.assertFalse(report["complete"])
        for contrast in report["contrast_analyses"].values():
            self.assertFalse(contrast["complete"])
            self.assertEqual(contrast["models"]["test-model"]["paired_effect"]["status"], "blocked")

    def test_three_arm_plan_must_include_equal_repetition_sets(self):
        rows = [row for row in three_arm_rows() if row["condition"] != "guided_verifier"]
        report = analyze_three_arms(rows, planned(rows), phase="calibration", bootstrap_draws=100)
        self.assertFalse(report["complete"])
        self.assertTrue(any(b["code"] == "unbalanced_three_arm_design" for b in report["blockers"]))

    def test_metadata_may_differ_in_hashes_but_resource_settings_must_match(self):
        rows = three_arm_rows()
        configs = [{"max_output_tokens": 16384, "effort": "medium", "runtime": {"hash": "first"}},
                   {"max_output_tokens": 16384, "effort": "medium", "runtime": {"hash": "second"}}]
        report = analyze_three_arms(rows, planned(rows), batch_configs=configs, bootstrap_draws=100)
        self.assertTrue(report["complete"])
        configs[1]["max_output_tokens"] = 8192
        report = analyze_three_arms(rows, planned(rows), batch_configs=configs, bootstrap_draws=100)
        self.assertFalse(report["complete"])
        self.assertTrue(any(b["code"] == "incompatible_batch_settings" for b in report["blockers"]))

    def test_complete_three_arm_report_keeps_round_scores_and_sample_sd(self):
        rows = three_arm_rows()
        report = analyze_three_arms(rows, planned(rows), phase="main", bootstrap_draws=100)
        for metrics in report["models"]["test-model"]["conditions"].values():
            summary = metrics["repeated_benchmark_scores"]
            self.assertEqual(summary["status"], "ok")
            self.assertEqual(summary["scores_percent"], [50, 50])
            self.assertEqual(summary["sample_sd_percentage_points"], 0)

    def assert_repeated_scores_blocked_everywhere(self, report):
        reports = [report, *report["contrast_analyses"].values()]
        for part in reports:
            for metrics in part["models"]["test-model"]["conditions"].values():
                summary = metrics["repeated_benchmark_scores"]
                self.assertEqual(summary["status"], "blocked")
                self.assertIsNone(summary["mean_score_percent"])
                self.assertIsNone(summary["sample_sd_percentage_points"])
                self.assertTrue(all(row["provisional"] for row in summary["rounds"]))

    def test_three_arm_settings_blocker_suppresses_all_comparable_round_summaries(self):
        rows = three_arm_rows()
        configs = [{"step_limit": 100}, {"step_limit": 12}]
        report = analyze_three_arms(rows, planned(rows), batch_configs=configs, bootstrap_draws=100)
        self.assertFalse(report["complete"])
        self.assert_repeated_scores_blocked_everywhere(report)

    def test_three_arm_design_blocker_suppresses_otherwise_complete_two_arm_rounds(self):
        rows = [row for row in three_arm_rows() if row["condition"] != "guided_verifier"]
        report = analyze_three_arms(rows, planned(rows), bootstrap_draws=100)
        self.assertFalse(report["complete"])
        self.assert_repeated_scores_blocked_everywhere(report)

    def test_cli_merges_optional_and_guided_manifests_without_recounting_baseline(self):
        rows = three_arm_rows()
        optional = [row for row in rows if row["condition"] != "guided_verifier"]
        guided = [row for row in rows if row["condition"] == "guided_verifier"]
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for name, part in (("optional", optional), ("guided", guided)):
                (root / f"{name}-results.json").write_text(json.dumps(part), encoding="utf-8")
                (root / f"{name}-expected.json").write_text(json.dumps({"runs": planned(part),
                    "config": {"max_output_tokens": 16384, "effort": "medium"}}), encoding="utf-8")
            output = root / "combined.json"
            code = main(["--results", str(root / "optional-results.json"), str(root / "guided-results.json"),
                         "--expected", str(root / "optional-expected.json"), str(root / "guided-expected.json"),
                         "--phase", "calibration", "--bootstrap-draws", "100", "--output", str(output)])
            self.assertEqual(code, 0)
            report = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(report["planned_runs"], len(rows))
            self.assertEqual(report["observed_unique_runs"], len(rows))


if __name__ == "__main__":
    unittest.main()
