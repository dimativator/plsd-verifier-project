"""Offline public-export privacy, integrity and statistical-equivalence checks."""

import csv
import hashlib
import json
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

from experiments import export_study as e
from experiments.three_arm_analysis import analyze_three_arms


class ExportStudyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="plinse-public-export-")
        self.root = Path(self.temp.name)
        self.source, self.output = self.root / "input", self.root / "public"
        self.source.mkdir()
        self.rows, self.specs, self.costs = [], [], []
        for rep in range(1, 9):
            for task in range(100):
                for arm_index, arm in enumerate(e.ARMS):
                    spec = dict(
                        phase="main",
                        model="gpt-5.6-luna",
                        task_id=f"cf-{1000 + task}-A",
                        family_id=f"cf-{1000 + task}-A",
                        rating_band="2000-2399" if task < 50 else "2400+",
                        condition=arm,
                        repetition=rep,
                        worker_id="private-host",
                    )
                    self.specs.append(spec)
                    self.rows.append(
                        {
                            **spec,
                            "hidden_passed": (task + rep + arm_index) % 5 != 0,
                            "valid_run": True,
                            "infrastructure_error": None,
                            "exit_status": "Submitted",
                            "model_cost_usd": 0.01,
                            "cost_is_upper_bound": False,
                            "solve_seconds": 1.5,
                            "evaluation_seconds": 0.1,
                            "model_settings": {"effort": "medium", "max_output_tokens": 16384},
                            "tool_events": [{"event": "verify_invocation_observed"}]
                            if arm == "guided_verifier"
                            else [],
                            "resolution": {
                                "selected_attempt": "infra-retry-1"
                                if len(self.rows) < 33
                                else "original",
                                "original_batch": r"C:\Users\private-person\Downloads\original",
                            },
                        }
                    )
                    self.costs.append(
                        {**{k: spec[k] for k in e.IDENTITY}, "all_attempt_accounted_usd": ".02"}
                    )
        self.config = {
            "effort": "medium",
            "max_output_tokens": 16384,
            "step_limit": 100,
            "solve_limit_seconds": 600,
            "per_run_cap_usd": ".12",
            "output": r"C:\Users\private-person\study",
            "spend_root": "/home/private-person/spend",
            "runtime": {
                "source_sha256": {"analysis.py": "1" * 64},
                "common_prompt_sha256": "2" * 64,
                "portable_image_fingerprints": {"plinse-eval:20261123": "3" * 64},
            },
        }
        self.audit = {
            "complete": True,
            "selected_runs": 2400,
            "task_families": 100,
            "retry_selected": 33,
            "all_attempt_accounted_usd": "48.00",
            "by_condition_accounted_usd": {arm: "16.00" for arm in e.ARMS},
            "selected_attempt_cost_usd": "24.00",
            "source_archive_sha256": "4" * 64,
            "protocol_sha256": "5" * 64,
            "ledgers": [
                {
                    "path": r"C:\Users\private-person\ledger.json",
                    "reservation_ids": ["private-id"],
                    "status_counts": {"settled": 2000, "uncertain": 1},
                    "status_usd": {"settled": "47.00", "uncertain": "1.00"},
                }
            ],
        }
        self.process = {
            "selected_runs_audited": 2400,
            "complete": True,
            "summary": {"runs": 2400},
            "by_condition": {
                arm: {
                    "runs": 800,
                    "runs_with_verifier_evidence": 800 if arm == "guided_verifier" else 0,
                }
                for arm in e.ARMS
            },
            "examples": [
                {"actions_source": r"C:\Users\private-person\secret", "command": "not public"}
            ],
            "runs": [{"private_path": "/home/private-person/raw"}],
        }
        self.write_inputs()

    def tearDown(self):
        self.temp.cleanup()

    def write(self, name, value):
        (self.source / name).write_text(json.dumps(value), encoding="utf-8")

    def write_costs(self, rows):
        with (self.source / "all-attempt-costs.csv").open(
            "w", encoding="utf-8", newline=""
        ) as stream:
            writer = csv.DictWriter(stream, fieldnames=[*e.IDENTITY, "all_attempt_accounted_usd"])
            writer.writeheader()
            writer.writerows(rows)

    def write_inputs(self):
        self.write("combined-results.json", self.rows)
        self.write("combined-expected.json", {"runs": self.specs, "batch_configs": [self.config]})
        self.write("data-audit.json", self.audit)
        self.write("process-summary.json", self.process)
        for name in ("analysis_original_5.json", "analysis_all_8.json"):
            self.write(
                name,
                {
                    "complete": True,
                    "blockers": [],
                    "phase": "main",
                    "private_extra": "/home/private-person/private",
                },
            )
        self.write_costs(self.costs)

    @staticmethod
    def hashes(root):
        return {
            p.name: hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.iterdir()
            if p.is_file()
        }

    def test_nested_private_fields_excluded_and_source_unchanged(self):
        self.rows[0]["model_settings"]["private"] = {
            "path": r"C:\Users\private-person\key",
            "credential": "sk-" + "a" * 40,
        }
        self.rows[0]["tool_events"] = [
            {"event": "verify_invocation_observed", "private": {"path": "/home/private-person/key"}}
        ]
        self.config["runtime"]["source_sha256"][r"C:\Users\private-person\unknown.py"] = "8" * 64
        self.audit["private"] = {"path": "/home/private-person/private"}
        self.write_inputs()
        before = self.hashes(self.source)
        result = e.export_study(self.source, self.output)
        self.assertEqual(result["selected_runs"], 2400)
        self.assertEqual(result["all_attempt_accounted_usd"], "48.00")
        self.assertEqual(before, self.hashes(self.source))
        for path in self.output.iterdir():
            text = path.read_text()
            self.assertNotIn("private-person", text)
            self.assertNotIn("private-host", text)
            self.assertNotIn("private-id", text)
            self.assertNotIn("sk-" + "a" * 40, text)
        clean = json.loads((self.output / "combined-results.json").read_text())
        self.assertNotIn("resolution", clean[0])
        self.assertNotIn("worker_id", clean[0])
        self.assertNotIn("infrastructure_error", clean[0])
        self.assertEqual(clean[0]["tool_events"], [{"event": "verify_invocation_observed"}])
        process = json.loads((self.output / "process-summary.json").read_text())
        self.assertNotIn("examples", process)
        self.assertNotIn("runs", process)
        self.assertEqual(
            process["by_condition"]["guided_verifier"]["runs_with_verifier_evidence"], 800
        )

    def test_public_rows_reproduce_same_statistics(self):
        e.export_study(self.source, self.output)
        rows = json.loads((self.output / "combined-results.json").read_text())
        expected = json.loads((self.output / "combined-expected.json").read_text())
        options = dict(
            phase="main", bootstrap_draws=20, seed=20261123, workers=8, per_run_cap_usd=0.12
        )
        original = analyze_three_arms(self.rows, self.specs, batch_configs=[self.config], **options)
        public = analyze_three_arms(
            rows, expected["runs"], batch_configs=expected["batch_configs"], **options
        )
        self.assertTrue(public["complete"])
        self.assertEqual(original, public)

    def test_cost_join_and_totals_mismatches_rejected_before_output(self):
        variants = [self.costs[:-1], self.costs + [self.costs[0]]]
        foreign = deepcopy(self.costs)
        foreign[-1]["task_id"] = "cf-999999-A"
        variants.append(foreign)
        for value in ("-1", "NaN", "Infinity", ".03"):
            bad = deepcopy(self.costs)
            bad[-1]["all_attempt_accounted_usd"] = value
            variants.append(bad)
        for index, variant in enumerate(variants):
            with self.subTest(index=index):
                self.write_costs(variant)
                target = self.root / f"bad-output-{index}"
                with self.assertRaises(ValueError):
                    e.export_study(self.source, target)
                self.assertFalse(target.exists())

    def test_idempotent_export_checksums_and_unrelated_files(self):
        self.output.mkdir()
        unrelated = self.output / "README.md"
        unrelated.write_text("Unrelated user-owned file.\n")
        first = e.export_study(self.source, self.output)
        before = self.hashes(self.output)
        second = e.export_study(self.source, self.output)
        self.assertEqual(first, second)
        self.assertEqual(before, self.hashes(self.output))
        manifest = json.loads((self.output / "SHA256SUMS.json").read_text())
        for name, value in manifest["files"].items():
            self.assertEqual(value, hashlib.sha256((self.output / name).read_bytes()).hexdigest())
        (self.output / "combined-results.json").write_text("User edited this file.")
        before_failure = self.hashes(self.output)
        with self.assertRaisesRegex(ValueError, "Existing public artifact differs"):
            e.export_study(self.source, self.output)
        self.assertEqual(before_failure, self.hashes(self.output))
        self.assertEqual(unrelated.read_text(), "Unrelated user-owned file.\n")

    def test_absolute_paths_inside_allowed_analysis_tree_fail_closed(self):
        self.write(
            "analysis_all_8.json",
            {
                "complete": True,
                "blockers": [],
                "models": {"nested": {"path": "/home/private-person/key"}},
            },
        )
        with self.assertRaisesRegex(ValueError, "personal path"):
            e.export_study(self.source, self.output)
        self.assertFalse(self.output.exists())

    def test_invalid_or_duplicate_selected_rows_not_relabelled(self):
        self.rows[-1]["infrastructure_error"] = {"type": "APIError", "message": "Failure"}
        self.write("combined-results.json", self.rows)
        with self.assertRaises(ValueError):
            e.export_study(self.source, self.output)
        self.rows[-1] = deepcopy(self.rows[0])
        self.write("combined-results.json", self.rows)
        with self.assertRaises(ValueError):
            e.export_study(self.source, self.output)
        self.assertFalse(self.output.exists())

    def test_lf_csv_and_readonly_verification_tamper_and_path_escape(self):
        e.export_study(self.source, self.output)
        csv_path = self.output / "all-attempt-costs.csv"
        original_csv = csv_path.read_bytes()
        self.assertNotIn(b"\r", original_csv)
        self.assertEqual(original_csv.count(b"\n"), 2401)
        before = self.hashes(self.output)
        self.assertEqual(e.verify_export(self.output), {"verified_files": 8, "algorithm": "sha256"})
        self.assertEqual(before, self.hashes(self.output))
        csv_path.write_bytes(original_csv + b" ")
        with self.assertRaisesRegex(ValueError, "digest differs"):
            e.verify_export(self.output)
        csv_path.write_bytes(original_csv)
        manifest_path = self.output / "SHA256SUMS.json"
        original_manifest = manifest_path.read_bytes()
        outside = self.root / "outside.json"
        outside.write_text("Private outside artifact.")
        outside_hash = hashlib.sha256(outside.read_bytes()).hexdigest()
        for name in (
            "../outside.json",
            "/outside.json",
            r"C:\outside.json",
            r"..\outside.json",
            "a/../outside.json",
        ):
            with self.subTest(name=name):
                manifest_path.write_text(
                    json.dumps({"algorithm": "sha256", "files": {name: outside_hash}})
                )
                with self.assertRaisesRegex(ValueError, "path"):
                    e.verify_export(self.output)
        manifest_path.write_bytes(original_manifest)
        self.assertEqual(e.verify_export(self.output)["verified_files"], 8)


if __name__ == "__main__":
    unittest.main()
