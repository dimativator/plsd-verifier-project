"""Regression checks for model-only operation, isolation, and hidden scoring."""

import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from pilot.codex_model import CodexConfig, CodexModel
from pilot.evaluate import evaluate, matches
from pilot.kotlin_tools import verification_guidance
from pilot.sandbox import environment, profile, run
from pilot.run import completion_requested, prepare_commands, summarize, validate_hidden_suites, load_results

PROJECT = Path(__file__).resolve().parents[1]


class ModelTests(unittest.TestCase):
    def rejected_event(self, event: dict, expected: str) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            config = CodexConfig("gpt-5.6-luna", "medium", temporary, temporary)
            events = [{"id": 1, "result": {}},
                      {"id": 2, "result": {"model": "gpt-5.6-luna", "thread": {"id": "test"}}},
                      {"id": 3, "result": {}}, event]

            class Process:
                pid = 9999999
                stdin = io.StringIO()
                stdout = io.StringIO("".join(json.dumps(item) + "\n" for item in events))

                def wait(self, **kwargs):
                    return 0

            with patch("pilot.codex_model.subprocess.Popen", return_value=Process()), patch("pilot.codex_model.os.killpg"):
                with self.assertRaisesRegex(RuntimeError, expected):
                    CodexModel(config)._completion([{"role": "system", "content": "Test"}, {"role": "user", "content": "Test"}])

    def test_native_tool_activity_is_rejected(self) -> None:
        self.rejected_event({"method": "item/started", "params": {"item": {"type": "commandExecution"}}}, "Unexpected Codex item")

    def test_model_reroute_is_rejected(self) -> None:
        self.rejected_event({"method": "model/rerouted", "params": {"toModel": "another-model"}}, "rerouted")

    def test_server_tool_request_is_rejected(self) -> None:
        self.rejected_event({"id": 99, "method": "item/tool/call", "params": {}}, "Unexpected Codex server request")

    def test_text_command_is_returned_to_mini_instead_of_executed(self) -> None:
        model = CodexModel(CodexConfig("gpt-5.6-luna", "medium", "/unused", "/unused"))
        with patch.object(model, "_completion", return_value="```bash\necho NEVER_EXECUTE_IN_CODEX\n```"), \
                patch("pilot.codex_model.subprocess.Popen") as spawn:
            message = model.query([])
        spawn.assert_not_called()
        self.assertEqual(message["extra"]["actions"], [{"command": "echo NEVER_EXECUTE_IN_CODEX"}])


class RuntimeTests(unittest.TestCase):
    def test_submission_must_be_a_separate_action(self) -> None:
        marker = "COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT"
        self.assertFalse(completion_requested("compile\nrun_tests\necho " + marker, "Compiled\nTests passed\n" + marker + "\n", 0))
        self.assertTrue(completion_requested("echo " + marker, marker + "\n", 0))
        self.assertFalse(completion_requested("run_tests", marker + "\n", 0))
        self.assertFalse(completion_requested("echo " + marker, marker + "\n", 1))

    def test_summary_uses_frozen_sample_size(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "selection.json").write_text(json.dumps({"model": "gpt-5.6-luna", "tasks": [
                {"dataset": "codecontests", "id": "one"}, {"dataset": "codecontests", "id": "two"}]}))
            result = summarize(root)
            self.assertEqual(result["requested_runs"], 4)
            self.assertFalse(result["all_runs_valid"])
            self.assertEqual([row["requested"] for row in result["groups"]], [0, 0, 2, 2])

    def test_empty_private_suite_is_rejected_before_launch(self) -> None:
        with self.assertRaisesRegex(ValueError, "Missing or unaligned"):
            validate_hidden_suites(PROJECT, {"tasks": [{"dataset": "codecontests", "id": "cf-958-C2"}]})

    def test_empty_evaluation_is_not_an_agent_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            run_dir = root / "codecontests/task/baseline"
            run_dir.mkdir(parents=True)
            (run_dir / "result.json").write_text(json.dumps({"valid_run": True}))
            (run_dir / "hidden-evaluation.json").write_text(json.dumps({"stage": "hidden_tests", "test_count": 0}))
            other = root / "codecontests/task/verifier"
            other.mkdir()
            (other / "result.json").write_text(json.dumps({"valid_run": True}))
            (other / "hidden-evaluation.json").write_text(json.dumps({"stage": "compilation", "test_count": 0}))
            rows = load_results(root)
            self.assertEqual(len(rows), 2)
            self.assertTrue(all(not item["evaluation_valid"] for item in rows))
            row = rows[0]
            self.assertFalse(row["valid_run"])
            self.assertFalse(row["evaluation_valid"])
            self.assertTrue(json.loads((run_dir / "result.json").read_text())["valid_run"])

    def test_public_test_command_resolves_to_real_tool_and_runs(self) -> None:
        prepare_commands(PROJECT)
        common = PROJECT / "pilot/toolchain/common"
        with tempfile.TemporaryDirectory(dir=PROJECT / "pilot/.runtime") as directory:
            workspace = Path(directory)
            (workspace / "Solution.kt").write_text("fun answer(): Int = 42\n")
            (workspace / "PublicTests.kt").write_text("fun main() { check(answer() == 42) }\n")
            (workspace / "task.json").write_text(json.dumps({"id": "smoke", "submission_format": "function", "solution_file": "Solution.kt", "visible_tests": "PublicTests.kt"}))
            env = environment(workspace, [common / "bin", PROJECT / ".venv/bin"])
            policy = profile(workspace, [common, PROJECT / ".venv"])
            result = run(["/bin/bash", "-c", "command -v run_tests && run_tests"], cwd=workspace, env=env, sandbox=policy)
            self.assertEqual(result["returncode"], 0, result)
            self.assertIn("All public harness assertions passed.", result["stdout"])

    def test_verifier_guidance_preserves_uncertainty(self) -> None:
        text = verification_guidance("warning: unsupported feature; verification skipped", 0)
        self.assertIn("Incomplete coverage", text)
        self.assertNotIn("All verified", text)
        self.assertIn("Unproved obligation", verification_guidance("Postcondition might not hold", 1))
        self.assertIn("Possible tool/backend failure", verification_guidance("INTERNAL_ERROR", 1))
        self.assertIn("cannot classify", verification_guidance("error: unresolved reference", 1))

    def test_quickstart_example_and_failed_postcondition(self) -> None:
        prepare_commands(PROJECT)
        common = PROJECT / "pilot/toolchain/common"
        verifier = PROJECT / "pilot/toolchain/verifier"
        guide = (PROJECT / "pilot/verifier-quickstart.txt").read_text()
        example = guide[guide.index("import org.jetbrains.kotlin.formver.plugin.*"):guide.index("\nThe precondition")]
        with tempfile.TemporaryDirectory(dir=PROJECT / "pilot/.runtime") as directory:
            workspace = Path(directory)
            (workspace / "task.json").write_text(json.dumps({"solution_file": "Solution.kt"}))
            env = environment(workspace, [verifier / "bin", common / "bin", PROJECT / ".venv/bin"])
            policy = profile(workspace, [common, verifier, PROJECT / ".venv"])
            for correct in (True, False):
                source = example if correct else example.replace("return x + 1", "return x - 1")
                (workspace / "Solution.kt").write_text(source)
                result = run(["/bin/bash", "-c", "verify"], cwd=workspace, env=env, sandbox=policy)
                self.assertEqual(result["returncode"] == 0, correct, result)
                self.assertIn("Original verifier diagnostics", result["stdout"])
                if correct:
                    self.assertIn("verified 1 declaration", result["stdout"])
                else:
                    self.assertIn("Unproved obligation", result["stdout"])
                    self.assertIn("postcondition", result["stderr"])
            baseline = profile(workspace, [common, PROJECT / ".venv"])
            blocked = run(["/bin/cat", str(verifier / "QUICKSTART.txt")], cwd=workspace, env=env, sandbox=baseline)
            self.assertNotEqual(blocked["returncode"], 0)

    def test_output_checkers(self) -> None:
        self.assertTrue(matches("1  2\n", "1\n2", "tokens"))
        self.assertFalse(matches("1 3", "1 2", "tokens"))
        self.assertTrue(matches("yEs\n", "YES", "casefold_tokens"))
        self.assertFalse(matches("yes", "YES", "tokens"))

    def test_jvm_starts_and_secrets_and_other_processes_stay_blocked(self) -> None:
        common = PROJECT / "pilot/toolchain/common"
        config = json.loads((common / "toolchain.json").read_text())
        with tempfile.TemporaryDirectory(dir=PROJECT / "pilot/.runtime") as directory:
            workspace = Path(directory)
            secret = workspace.parent / (workspace.name + "-secret.txt")
            secret.write_text("PRIVATE_SENTINEL")
            try:
                policy = profile(workspace, [common])
                env = environment(workspace, [])
                self.assertEqual(run([config["java"], "-version"], cwd=workspace, env=env, sandbox=policy)["returncode"], 0)
                read = run(["/bin/cat", str(secret)], cwd=workspace, env=env, sandbox=policy)
                self.assertNotEqual(read["returncode"], 0)
                self.assertNotIn("PRIVATE_SENTINEL", read["stdout"])
                verifier = run(["/bin/cat", str(PROJECT / "pilot/toolchain/verifier/toolchain.json")], cwd=workspace, env=env, sandbox=policy)
                self.assertNotEqual(verifier["returncode"], 0)
                inspect = run(["/bin/ps", "e", "-p", str(os.getpid())], cwd=workspace, env=env, sandbox=policy)
                self.assertNotEqual(inspect["returncode"], 0)
            finally:
                secret.unlink()

    def test_wrong_solution_fails_hidden_tests(self) -> None:
        with tempfile.TemporaryDirectory(dir=PROJECT / "pilot/.runtime") as directory:
            root = Path(directory)
            source = root / "Solution.kt"
            source.write_text("fun maxElement(l: List<Int>): Int = 0\n")
            result = evaluate(PROJECT, {"dataset": "kotlinhumaneval", "id": "humaneval-034", "checker": "kotlin_harness"}, source, root / "scratch")
            self.assertEqual(result["stage"], "hidden_tests")
            self.assertFalse(result["passed"])

    def test_early_successful_process_exit_cannot_bypass_hidden_assertions(self) -> None:
        with tempfile.TemporaryDirectory(dir=PROJECT / "pilot/.runtime") as directory:
            root = Path(directory)
            source = root / "Solution.kt"
            source.write_text("fun maxElement(l: List<Int>): Int { kotlin.system.exitProcess(0) }\n")
            result = evaluate(PROJECT, {"dataset": "kotlinhumaneval", "id": "humaneval-034", "checker": "kotlin_harness"}, source, root / "scratch")
            self.assertEqual(result["execution"]["returncode"], 0)
            self.assertFalse(result["harness_completed"])
            self.assertFalse(result["passed"])


if __name__ == "__main__":
    unittest.main()
