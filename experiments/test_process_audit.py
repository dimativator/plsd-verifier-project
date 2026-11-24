"""Tests for verifier commands and diagnostics extracted from action logs."""

import json
from pathlib import Path
import tempfile
import unittest

from experiments.process_audit import (
    START,
    END,
    parse_wrapper_calls,
    guide_read_match,
    direct_crosshair_commands,
    diagnostics,
    corroborating_crosshair_lines,
    generate,
)


class ProcessAuditTests(unittest.TestCase):
    def action(self, text, **overrides):
        return {
            "command": "verify main.py",
            "source_before": "a" * 64,
            "source_after": "a" * 64,
            "result": {"stdout": text, "stderr": "", "returncode": 0},
            **overrides,
        }

    def marker(self, body="", code=0):
        return (
            START
            + json.dumps({"target": "main.py", "source_sha256": "a" * 64})
            + "\n"
            + body
            + "\n"
            + END
            + json.dumps({"returncode": code})
            + "\n"
        )

    def test_wrapper_boilerplate_is_neither_counterexample_nor_confirmation(self):
        calls, errors = parse_wrapper_calls(
            self.action(self.marker("No counterexample found is not proof of task correctness.")), 1
        )
        self.assertFalse(errors)
        self.assertEqual(calls[0]["diagnostics"]["categories"], ["no_explicit_diagnostic_observed"])

    def test_counterexample_and_confirmation_can_coexist_without_equating_them(self):
        calls, _ = parse_wrapper_calls(
            self.action(
                self.marker(
                    "/work/main.py:3: error: false when calling f(0)\n/work/main.py:9: info: Confirmed over all paths.",
                    1,
                )
            ),
            4,
        )
        self.assertEqual(
            set(calls[0]["diagnostics"]["categories"]),
            {"counterexample_reported", "confirmed_checked_contracts_reported"},
        )

    def test_multiple_calls_and_unpaired_markers(self):
        text = self.marker(
            "WARNING: Targets found, but contain no checkable functions."
        ) + self.marker("Verifier timed out after 30 seconds; result is inconclusive.", 124)
        calls, _ = parse_wrapper_calls(self.action(text), 2)
        self.assertEqual(len(calls), 2)
        self.assertIn(
            "unsupported_or_no_entrypoints_reported", calls[0]["diagnostics"]["categories"]
        )
        self.assertIn("timeout_reported", calls[1]["diagnostics"]["categories"])
        incomplete, _ = parse_wrapper_calls(
            self.action(START + json.dumps({"target": "main.py", "source_sha256": "a" * 64})), 3
        )
        self.assertFalse(incomplete[0]["marker_pair_complete"])

    def test_marker_text_in_command_is_not_counted(self):
        calls, _ = parse_wrapper_calls(self.action("", command=self.marker("")), 1)
        self.assertEqual(calls, [])

    def test_multi_wrapper_stderr_keeps_action_scope(self):
        action = self.action(self.marker() + self.marker())
        action["result"]["stderr"] = "/work/main.py:1: error: false when calling f(0)"
        calls, _ = parse_wrapper_calls(action, 1)
        self.assertNotIn("counterexample_reported", calls[0]["diagnostics"]["categories"])
        self.assertIn("counterexample_reported", calls[0]["action_scope_diagnostics"]["categories"])

    def test_guides_are_command_observations(self):
        self.assertIsNotNone(guide_read_match("cat /opt/plinse/CROSSHAIR_GUIDE.txt"))
        self.assertIsNone(
            guide_read_match("cat > main.py <<'PY'\nprint('/opt/plinse/CROSSHAIR_GUIDE.txt')\nPY")
        )

    def test_direct_module_executable_and_conditional_are_command_observations(self):
        calls = direct_crosshair_commands(
            "if command -v crosshair; then\n timeout 30s python3 -I -m crosshair check main.py\n crosshair check helper.py || true\nfi"
        )
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0]["detection_kind"], "python_module")
        self.assertEqual(calls[1]["detection_kind"], "crosshair_executable")

    def test_heredoc_docstrings_and_quoted_mentions_are_not_cli_commands(self):
        command = 'cat > main.py <<\'PY\'\n"""\npython3 -m crosshair check imaginary.py\ncat /opt/plinse/CROSSHAIR_GUIDE.txt\n"""\nPY\necho \'crosshair check imaginary.py\'\npython3 -m crosshair check real.py\n'
        calls = direct_crosshair_commands(command)
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0]["check_arguments"], ["real.py"])
        self.assertIsNone(guide_read_match(command))
        self.assertEqual(
            direct_crosshair_commands("python3 -c '\nprint(\"crosshair check imaginary.py\")\n'"),
            [],
        )
        self.assertEqual(
            direct_crosshair_commands("python3 -c 'print(1)' -m crosshair check imaginary.py"), []
        )
        self.assertEqual(
            direct_crosshair_commands("python3 helper.py -m crosshair check imaginary.py"), []
        )

    def test_no_entrypoint_warning_and_cli_configuration_error(self):
        warning = "WARNING: Targets found, but contain no checkable functions."
        self.assertEqual(
            diagnostics("", warning)["categories"], ["unsupported_or_no_entrypoints_reported"]
        )
        self.assertTrue(corroborating_crosshair_lines("", warning))
        error = "crosshair check: error: argument --analysis_kind: invalid analysis_kind value: ''"
        self.assertEqual(
            diagnostics("", error, returncode=2)["categories"],
            ["backend_or_loading_error_reported"],
        )
        self.assertTrue(corroborating_crosshair_lines("", error))

    def test_run_hashes_and_later_edit_are_temporal_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            directory = root / "model/task/verifier/rep-01"
            directory.mkdir(parents=True)
            result = {
                "phase": "calibration",
                "model": "model",
                "task_id": "task",
                "condition": "verifier",
                "repetition": 1,
                "valid_run": True,
                "hidden_passed": False,
                "shell_actions": 2,
                "submission_sha256": "b" * 64,
            }
            (directory / "result.json").write_text(json.dumps(result), encoding="utf-8")
            actions = [
                self.action(
                    self.marker("/work/main.py:1: error: false when calling f(0)", 1),
                    command="verify main.py; python3 -m crosshair check main.py",
                ),
                self.action("", source_after="b" * 64),
            ]
            (directory / "actions.jsonl").write_text(
                "\n".join(map(json.dumps, actions)), encoding="utf-8"
            )
            report = generate([root])
            self.assertEqual(report["summary"]["observed_wrapper_start_markers"], 1)
            self.assertEqual(report["summary"]["direct_cli_command_observations"], 1)
            self.assertEqual(report["summary"]["runs_with_verifier_evidence"], 1)
            self.assertEqual(report["summary"]["actions_with_verifier_evidence"], 1)
            self.assertTrue(report["runs"][0]["source_changed_after_counterexample_action"])
            self.assertTrue(report["runs"][0]["submission_hash_matches_last_action"])
            self.assertLessEqual(len(report["trace_selections"]), 3)
            self.assertEqual(
                sum((len(trace["selection_rules"]) for trace in report["trace_selections"])), 2
            )


if __name__ == "__main__":
    unittest.main()
