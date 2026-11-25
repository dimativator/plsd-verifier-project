"""Tests for leakage rejection, checker semantics and prespecified selection."""
import unittest

from experiments.validate_tasks import compare_output, family_id, metadata_reasons, portable_cpp, section, select_by_band, suite_checks
from experiments.validation_preflight import freeze


class ValidationTests(unittest.TestCase):
    def test_numeric_checker_accepts_formatting_but_rejects_wrong_values(self):
        self.assertTrue(compare_output("  +007\n-0 ", "7 0", "integer_tokens"))
        self.assertFalse(compare_output("7.0", "7", "integer_tokens"))
        self.assertFalse(compare_output("7 8", "7", "integer_tokens"))
        self.assertFalse(compare_output("7 0", "7 -1", "integer_tokens"))

    def test_string_checker_preserves_significant_bits_and_labels(self):
        self.assertFalse(compare_output("1", "001", "tokens"))
        self.assertFalse(compare_output("yes", "YES", "tokens"))
        self.assertTrue(compare_output("yes\n", "YES", "casefold_tokens"))

    def test_cpp_portability_preserves_algorithm_and_normalizes_only_legacy_formats(self):
        source = 'scanf("%d%I64d", &n, &x); printf("%I64u %%I64d", x); x += 1;'
        adapted, count = portable_cpp(source)
        self.assertEqual(adapted, 'scanf("%d%lld", &n, &x); printf("%llu %%I64d", x); x += 1;')
        self.assertEqual(count, 2)

    def test_empty_hidden_and_public_private_leakage_are_rejected(self):
        self.assertIn("empty_private_suite", suite_checks([("1", "2")], [], "integer_tokens"))
        self.assertIn("actual_public_private_input_overlap", suite_checks([("1  2\n", "3")], [("1\n2", "3")], "integer_tokens"))

    def test_conflicting_hidden_answers_and_noninteger_oracles_are_rejected(self):
        self.assertIn("actual_conflicting_expected_outputs", suite_checks([("1", "2")], [("3", "4"), ("3\n", "5")], "integer_tokens"))
        self.assertIn("expected_output_incompatible_with_checker", suite_checks([("1", "2")], [("3", "0.25")], "integer_tokens"))

    def test_output_section_does_not_accidentally_review_an_example(self):
        text = "task\nInput\n\nRead n.\n\nOutput\n\nPrint n squared.\n\nExamples\n\nInput\n2\nOutput\n4\n"
        self.assertEqual(section(text, "Output"), "Print n squared.")
        self.assertEqual(section(text, "Input"), "Read n.")

    def test_exposed_sibling_is_not_fresh(self):
        row = {"id": "cf-1184-B3", "rating_band": "2400+", "private_test_count": 5}
        self.assertEqual(family_id(row["id"]), family_id("cf-1184-B2"))
        self.assertIn("previously_exposed_family", metadata_reasons(row, {family_id("cf-1184-B2")}))

    def test_selection_is_order_independent_and_clusters_siblings(self):
        rows = [{"id": f"cf-{number}-A", "family": f"cf-{number}-A", "rating_band": band} for band, numbers in [("2000-2399", range(10)), ("2400+", range(10, 20))] for number in numbers]
        chosen, reserves = select_by_band(rows, 3, 2, 123)
        other, other_reserves = select_by_band(list(reversed(rows)), 3, 2, 123)
        self.assertEqual(chosen, other)
        self.assertEqual(reserves, other_reserves)
        self.assertEqual(len({r["family"] for r in chosen + reserves}), 10)
        with self.assertRaises(ValueError):
            select_by_band(rows[:3], 3, 0, 123)

    def test_freeze_uses_only_validated_candidates_and_seeded_replacements(self):
        rows = [{"id": f"cf-{number}-A", "family": f"cf-{number}-A", "rating_band": band} for band, numbers in [("2000-2399", range(3)), ("2400+", range(3, 6))] for number in numbers]
        initial, _ = select_by_band(rows, 1, 0, 123)
        rejected = initial[0]["id"]
        results = [{"id": r["id"], "status": "failed" if r["id"] == rejected else "passed"} for r in rows]
        manifest = {"reviewed_candidates": rows, "calibration_tasks": [], "tasks": initial, "seed": 123}
        frozen = freeze(manifest, results, 1)
        self.assertNotIn(rejected, {r["id"] for r in frozen["tasks"]})
        self.assertEqual(frozen["replacement_record"]["removed_from_initial_sample"], [rejected])
        self.assertTrue(all(r["behavioral_validation"] == "passed" for r in frozen["tasks"]))


if __name__ == "__main__":
    unittest.main()
