"""Trusted hidden-test evaluator, separate from mini-SWE-agent workspaces."""

from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import secrets
import shutil
import tempfile

from pilot.kotlin_tools import compiler_command, java_command
from pilot.sandbox import environment, profile, run


def matches(actual: str, expected: str, checker: str) -> bool:
    if checker == "casefold_tokens":
        return actual.casefold().split() == expected.casefold().split()
    if checker == "tokens":
        return actual.split() == expected.split()
    raise ValueError(f"Unsupported output checker: {checker}")


def execute_cases(command: list[str], tests: dict, checker: str, workspace: Path,
                  common: Path, workers: int = 2) -> dict:
    pairs = list(zip(tests["input"], tests["output"]))
    if len(tests["input"]) != len(tests["output"]):
        raise ValueError("Unaligned test data")
    env = environment(workspace, [])
    sandbox = profile(workspace, [common])

    def case(item: tuple[int, tuple[str, str]]) -> dict:
        index, (given, expected) = item
        result = run(command, cwd=workspace, env=env, sandbox=sandbox, input_text=given, timeout=10)
        correct = result["returncode"] == 0 and not result["timed_out"] and matches(result["stdout"], expected, checker)
        return {"case": index, "passed": correct, "returncode": result["returncode"],
                "timed_out": result["timed_out"], "actual": result["stdout"][:3000],
                "stderr": result["stderr"][:3000], "expected": expected[:3000]}

    with ThreadPoolExecutor(max_workers=workers) as executor:
        results = list(executor.map(case, enumerate(pairs)))
    return {"test_count": len(results), "passed_count": sum(row["passed"] for row in results),
            "passed": bool(results) and all(row["passed"] for row in results),
            "failures": [row for row in results if not row["passed"]]}


def evaluate(project: Path, selected: dict, submission: Path, scratch: Path) -> dict:
    dataset = project / "benchmark-data" / selected["dataset"]
    task = dataset / "tasks" / selected["id"]
    public_task = json.loads((task / "public/task.json").read_text())
    common = project / "pilot/toolchain/common"
    config = json.loads((common / "toolchain.json").read_text())
    scratch.mkdir(parents=True, exist_ok=True)
    if submission.is_symlink() or not submission.is_file():
        return {"passed": False, "stage": "missing_or_invalid_submission", "test_count": 0, "passed_count": 0}
    with tempfile.TemporaryDirectory(prefix="eval-", dir=scratch) as directory:
        workspace = Path(directory)
        source = workspace / public_task["solution_file"]
        shutil.copyfile(submission, source)
        sources = [source]
        sentinel = None
        if selected["dataset"] == "kotlinhumaneval":
            harness = workspace / "HiddenTests.kt"
            original = (task / "evaluator/HiddenTests.kt").read_text().rstrip()
            if not original.endswith("}"):
                raise ValueError("Unexpected hidden harness structure")
            sentinel = "PLSD_HARNESS_COMPLETED_" + secrets.token_hex(16)
            harness.write_text(original[:-1] + f'\n    kotlin.io.println("{sentinel}")\n}}\n')
            sources.append(harness)
            main = "HiddenTestsKt"
        else:
            main = "MainKt"
        classes = workspace / "classes"
        classes.mkdir()
        env = environment(workspace, [])
        sandbox = profile(workspace, [common])
        compile_result = run(compiler_command(config, sources, classes), cwd=workspace, env=env, sandbox=sandbox)
        if compile_result["returncode"]:
            return {"passed": False, "stage": "compilation", "compilation": compile_result,
                    "test_count": 0, "passed_count": 0}
        # The runtime gets compiled classes, never the source harness or test-data directory.
        for path in sources:
            path.unlink()
        command = java_command(config, classes, main)
        if selected["dataset"] == "kotlinhumaneval":
            result = run(command, cwd=workspace, env=env, sandbox=sandbox, timeout=10)
            completed = sentinel in result["stdout"].splitlines()
            passed = result["returncode"] == 0 and not result["timed_out"] and completed
            return {"passed": passed, "harness_completed": completed,
                    "stage": "hidden_tests", "test_count": 1,
                    "test_count_unit": "harness (all unexposed assertions)",
                    "passed_count": int(passed),
                    "execution": result}
        tests = json.loads((task / "evaluator/private-tests.json").read_text())
        return {"stage": "hidden_tests", "suite": "original_private_tests",
                **execute_cases(command, tests, selected["checker"], workspace, common)}


def reference_check(project: Path, selected: dict, output: Path) -> dict:
    """Sanity-check source references without ever exposing them to the agent."""
    task = project / "benchmark-data" / selected["dataset"] / "tasks" / selected["id"]
    if selected["dataset"] == "kotlinhumaneval":
        return evaluate(project, selected, task / "evaluator/Reference.kt", output / "scratch")
    common = project / "pilot/toolchain/common"
    references = json.loads((task / "evaluator/reference-solutions.json").read_text())
    # The existing GNU compiler supports the source dataset's GNU C++ programs.
    reference = next(row for row in references if row["language"] == "CPP")
    output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="reference-", dir=output) as directory:
        workspace = Path(directory)
        source = workspace / "reference.cpp"
        reference_code = reference["code"]
        portability_fixes = []
        if "%I64d" in reference_code:
            reference_code = reference_code.replace("%I64d", "%lld")
            portability_fixes.append("Replace Windows %I64d with standard %lld in the temporary reference copy")
        source.write_text(reference_code)
        binary = workspace / "reference"
        compiled = run(["/opt/homebrew/bin/g++-14", "-std=gnu++17", "-O2", str(source), "-o", str(binary)],
                       cwd=workspace, env=environment(workspace, []))
        if compiled["returncode"]:
            return {"passed": False, "stage": "reference_compilation", "compilation": compiled}
        combined = {"input": [], "output": []}
        for path in [task / "public/public-tests.json", task / "evaluator/private-tests.json"]:
            tests = json.loads(path.read_text())
            for key in combined:
                combined[key].extend(tests[key])
        return {"language": "CPP", "suite": "public_and_original_private", "stage": "reference_tests",
                "portability_fixes": portability_fixes,
                **execute_cases([str(binary)], combined, selected["checker"], workspace, common)}
