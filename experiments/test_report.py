"""Portable report regressions; no raw ledger, network, Docker, or API key."""

import csv
import json
import tempfile
import unittest
from copy import deepcopy
from decimal import Decimal
from pathlib import Path

from experiments.analysis import run_key
from experiments.report import Study, accuracy_cost_points


class ReportTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.rows = []
        for index in range(4):
            for repetition in (1, 2):
                for condition in ("baseline", "verifier", "guided_verifier"):
                    self.rows.append(
                        {
                            "phase": "main",
                            "model": "model",
                            "task_id": f"task-{index}",
                            "family_id": f"family-{index}",
                            "rating_band": str(index // 2),
                            "condition": condition,
                            "repetition": repetition,
                            "hidden_passed": bool(index % 2),
                            "valid_run": True,
                            "infrastructure_error": None,
                        }
                    )
        self.costs = {
            run_key(row): Decimal("0.01") + Decimal(int(row["hidden_passed"])) / 100
            for row in self.rows
        }
        self.write("combined-results.json", self.rows)
        self.write(
            "combined-expected.json",
            {
                "runs": [
                    {
                        k: v
                        for k, v in row.items()
                        if k not in {"hidden_passed", "valid_run", "infrastructure_error"}
                    }
                    for row in self.rows
                ]
            },
        )
        self.write(
            "data-audit.json",
            {
                "all_attempt_accounted_usd": str(sum(self.costs.values(), Decimal(0))),
                "by_condition_accounted_usd": {
                    arm: str(
                        sum((cost for key, cost in self.costs.items() if key[2] == arm), Decimal(0))
                    )
                    for arm in ("baseline", "verifier", "guided_verifier")
                },
                "ledgers": [{"path": "nonexistent/private/ledger.json"}],
            },
        )
        self.write_costs()

    def tearDown(self):
        self.temporary.cleanup()

    def write(self, name, value):
        (self.root / name).write_text(json.dumps(value), encoding="utf-8")

    def write_costs(self, *, extra=False, missing=False, invalid=False):
        with (self.root / "all-attempt-costs.csv").open(
            "w", encoding="utf-8", newline=""
        ) as stream:
            writer = csv.writer(stream)
            writer.writerow(
                [
                    "phase",
                    "model",
                    "task_id",
                    "condition",
                    "repetition",
                    "all_attempt_accounted_usd",
                ]
            )
            for index, row in enumerate(self.rows):
                if missing and index == 0:
                    continue
                values = [
                    row[field] for field in ("phase", "model", "task_id", "condition", "repetition")
                ]
                values.append("NaN" if invalid and index == 0 else str(self.costs[run_key(row)]))
                writer.writerow(values)
                if extra and index == 0:
                    writer.writerow(values)

    def test_cost_export_is_canonical_and_joint_resamples_preserve_relation(self):
        study = Study.load(self.root)
        output = accuracy_cost_points(study, draws=200)
        for point in output["points"].values():
            self.assertEqual(point["accuracy_percent"], 50)
            self.assertAlmostEqual(point["mean_all_attempt_cost_usd_per_task"], 0.015)
            for accuracy, cost in zip(
                point["accuracy_ci95_percent"], point["cost_ci95_usd_per_task"]
            ):
                self.assertAlmostEqual(cost, 0.01 + accuracy / 10000)

    def test_repeating_same_family_outcomes_does_not_narrow_family_intervals(self):
        original = Study.load(self.root)
        more = deepcopy(self.rows)
        for row in more:
            row["repetition"] += 2
        rows = self.rows + more
        costs = dict(self.costs)
        costs.update(
            {
                run_key(row): Decimal("0.01") + Decimal(int(row["hidden_passed"])) / 100
                for row in more
            }
        )
        repeated = Study(tuple(rows), costs, "model")
        first = accuracy_cost_points(original, draws=200)
        second = accuracy_cost_points(repeated, draws=200)
        for condition in first["points"]:
            for field in ("accuracy_ci95_percent", "cost_ci95_usd_per_task"):
                self.assertEqual(
                    first["points"][condition][field], second["points"][condition][field]
                )

    def test_duplicate_missing_or_nonfinite_cost_cannot_be_plotted(self):
        for kwargs in ({"extra": True}, {"missing": True}, {"invalid": True}):
            with self.subTest(kwargs=kwargs):
                self.write_costs(**kwargs)
                with self.assertRaises(ValueError):
                    Study.load(self.root)

    def test_wrong_audit_total_cannot_be_plotted(self):
        self.write(
            "data-audit.json",
            {"all_attempt_accounted_usd": "999", "by_condition_accounted_usd": {}},
        )
        with self.assertRaises(ValueError):
            Study.load(self.root)

    def test_planned_collection_phase_must_match_selected_outcome(self):
        path = self.root / "combined-expected.json"
        expected = json.loads(path.read_text(encoding="utf-8"))
        expected["runs"][0]["phase"] = "calibration"
        self.write("combined-expected.json", expected)
        with self.assertRaises(ValueError):
            Study.load(self.root)

    def test_missing_result_changed_metadata_or_unresolved_failure_blocks_plot(self):
        for changed in (
            self.rows[:-1],
            [
                {**row, "family_id": "changed"} if index == 0 else row
                for index, row in enumerate(self.rows)
            ],
            [
                {**row, "valid_run": False} if index == 0 else row
                for index, row in enumerate(self.rows)
            ],
        ):
            with self.subTest(changed=changed[0]):
                self.write("combined-results.json", changed)
                with self.assertRaises(ValueError):
                    Study.load(self.root)


if __name__ == "__main__":
    unittest.main()
