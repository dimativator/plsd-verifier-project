"""Integrity checks for the published study archive; no extraction or API calls."""

import csv
import hashlib
import io
import json
import re
import unittest
import zipfile
from collections import Counter
from decimal import Decimal
from pathlib import Path

BUNDLE = Path(__file__).resolve().parents[1] / "studies/codeforces-20261124/data.zip"
IDENTITY = ("phase", "model", "task_id", "condition", "repetition")
MEMBERS = {
    "SHA256SUMS.json",
    "all-attempt-costs.csv",
    "combined-expected.json",
    "combined-results.json",
    "data-audit.json",
    "executed-experiment-source.zip",
    "executed-source-manifest.json",
    "process-summary.json",
    "protocol-provenance.json",
    "report-settings.json",
    "task-manifest.json",
    "validation_reviews.json",
}


class StudyBundleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.archive = zipfile.ZipFile(BUNDLE)

    @classmethod
    def tearDownClass(cls):
        cls.archive.close()

    def read(self, name):
        return json.loads(self.archive.read(name))

    def test_inventory_and_hashes(self):
        names = self.archive.namelist()
        self.assertEqual(len(names), len(MEMBERS))
        self.assertEqual(set(names), MEMBERS)
        manifest = self.read("SHA256SUMS.json")
        self.assertEqual(manifest["algorithm"], "sha256")
        self.assertEqual(set(manifest["files"]), MEMBERS - {"SHA256SUMS.json"})
        for name, expected in manifest["files"].items():
            self.assertEqual(hashlib.sha256(self.archive.read(name)).hexdigest(), expected)
        source = self.read("executed-source-manifest.json")
        source_bytes = self.archive.read("executed-experiment-source.zip")
        self.assertEqual(hashlib.sha256(source_bytes).hexdigest(), source["archive_sha256"])
        with zipfile.ZipFile(io.BytesIO(source_bytes)) as nested:
            for name, expected in source["source_files_sha256"].items():
                self.assertEqual(hashlib.sha256(nested.read(name)).hexdigest(), expected)

    def test_complete_outcomes_and_costs(self):
        rows = self.read("combined-results.json")
        key = lambda row: tuple(row[field] for field in IDENTITY)
        expected = {key(row) for row in self.read("combined-expected.json")["runs"]}
        self.assertEqual(len(rows), 2400)
        self.assertEqual(len({key(row) for row in rows}), 2400)
        self.assertEqual({key(row) for row in rows}, expected)
        self.assertTrue(
            all(row["valid_run"] and isinstance(row["hidden_passed"], bool) for row in rows)
        )
        self.assertEqual(
            Counter(row["repetition"] for row in rows), {rep: 300 for rep in range(1, 9)}
        )
        arms = {"baseline", "verifier", "guided_verifier"}
        self.assertEqual(Counter(row["condition"] for row in rows), {arm: 800 for arm in arms})
        costs = {}
        for row in csv.DictReader(io.StringIO(self.archive.read("all-attempt-costs.csv").decode())):
            row["repetition"] = int(row["repetition"])
            identity, amount = key(row), Decimal(row["all_attempt_accounted_usd"])
            self.assertNotIn(identity, costs)
            self.assertTrue(amount.is_finite() and amount >= 0)
            costs[identity] = amount
        self.assertEqual(set(costs), expected)
        audit = self.read("data-audit.json")
        self.assertEqual(sum(costs.values()), Decimal("44.22626659"))
        self.assertEqual(sum(costs.values()), Decimal(audit["all_attempt_accounted_usd"]))
        for arm in arms:
            self.assertEqual(
                sum(value for identity, value in costs.items() if identity[3] == arm),
                Decimal(audit["by_condition_accounted_usd"][arm]),
            )
        tasks = self.read("task-manifest.json")
        self.assertEqual(len(tasks["tasks"]), 100)
        self.assertEqual(len(tasks["calibration_tasks"]), 10)
        self.assertEqual(
            Counter(task["checker"] for task in tasks["tasks"]),
            {"integer_tokens": 84, "tokens": 16},
        )
        self.assertEqual({task["id"] for task in tasks["tasks"]}, {row["task_id"] for row in rows})

    def test_public_data_has_no_credentials_or_machine_paths(self):
        personal_path = re.compile(rb"(?<![A-Za-z0-9])[A-Za-z]:[\\/]|/(?:Users|home)/")
        secret = re.compile(
            rb"(?<![A-Za-z0-9])sk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{20,}|-----BEGIN .*PRIVATE KEY-----"
        )
        for name in MEMBERS - {"executed-experiment-source.zip"}:
            text = self.archive.read(name)
            self.assertIsNone(personal_path.search(text), name)
            self.assertIsNone(secret.search(text), name)


if __name__ == "__main__":
    unittest.main()
