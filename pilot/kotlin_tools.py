"""Compiler and visible-test commands. This module contains no hidden-test paths."""

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


def compiler_command(config: dict, source_files: list[Path], output: Path, plugin: dict | None = None) -> list[str]:
    args = [config["java"], "-Xss30m", "-Xmx2g", "-XX:-UsePerfData", "-cp",
            os.pathsep.join(config["compiler_classpath"]), "org.jetbrains.kotlin.cli.jvm.K2JVMCompiler",
            "-no-stdlib", "-no-reflect", "-jvm-target", "17", "-classpath",
            os.pathsep.join(config["library_classpath"]), "-d", str(output)]
    if plugin is not None:
        args += ["-Xplugin=" + plugin["plugin"], "-Xreport-all-warnings",
                 "-P", "plugin:org.jetbrains.kotlin.formver:error_style=both",
                 "-P", "plugin:org.jetbrains.kotlin.formver:trust_report=" + str(output.parent / "trust-report.txt")]
    return args + [str(path) for path in source_files]


def java_command(config: dict, classes: Path, main_class: str) -> list[str]:
    return [config["java"], "-Xmx1g", "-XX:-UsePerfData", "-cp",
            os.pathsep.join([str(classes), *config["library_classpath"]]), main_class]


def verification_guidance(diagnostics: str, returncode: int) -> str:
    """Conservative reading aid; never replace or reinterpret the raw evidence as proof."""
    lower = diagnostics.lower()
    lines = ["Verifier reading aid (heuristic; full diagnostics follow):"]
    if any(term in lower for term in ("unsupported", "skipped", "untracked", "unchecked library", "unchecked_library")):
        lines.append("- Incomplete coverage: inspect unsupported/skipped or untracked operations and the trust report. These are not verified code.")
    if any(term in lower for term in ("could not establish", "might not hold", "verification_condition_not_established", "viper_verification_error")):
        lines.append("- Unproved obligation: inspect the location and clause below. This can indicate a code defect, missing valid assumptions/invariants, or a limitation of the model. It is not a confirmed counterexample.")
    if any(term in lower for term in ("internal error", "internal_error", "exception", "verifier_unavailable", "invalid generated", "cannot run program")):
        lines.append("- Possible tool/backend failure: inspect the original error before treating it as a code defect.")
    if returncode and len(lines) == 1:
        lines.append("- Command failed: inspect the original compiler/backend error below. Fix syntax or API errors if reported. This wrapper cannot classify the failure reliably.")
    if returncode == 0:
        lines.append("- Command completed. Check the trust report for verified declarations and assumptions. This does not establish task correctness or coverage of skipped code.")
    lines.append("Next: inspect the evidence, revise code or justified specifications if useful, then rerun verify or public tests. Do not narrow valid task inputs to satisfy a proof.")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--toolchain", type=Path, required=True)
    parser.add_argument("--verifier", type=Path)
    parser.add_argument("command", choices=["compile", "test", "verify"])
    args = parser.parse_args()
    workspace = Path.cwd()
    config = json.loads(args.toolchain.read_text())
    task = json.loads((workspace / "task.json").read_text())
    solution = workspace / task["solution_file"]
    if solution.is_symlink() or not solution.is_file():
        raise ValueError("Submission must be a regular Kotlin source file")
    public = args.command == "test"
    visible = workspace / task["visible_tests"] if task.get("visible_tests") else None
    if public and visible is None:
        print("This task has no supplied public harness. Compile or add your own tests.")
        return
    output = workspace / ".build" / args.command / "classes"
    if output.parent.exists():
        shutil.rmtree(output.parent)
    output.mkdir(parents=True)
    sources = [solution]
    main_class = "MainKt"
    if public and task["submission_format"] == "function":
        sources.append(visible)
        main_class = "PublicTestsKt"
    plugin = None
    env = os.environ.copy()
    if args.command == "verify":
        if args.verifier is None:
            parser.error("Verifier is unavailable in this condition")
        plugin = json.loads(args.verifier.read_text())
        env["Z3_EXE"] = plugin["z3"]
        env["SILICON_PARALLEL_VERIFIERS"] = "2"
    if args.command == "verify":
        compiled = subprocess.run(compiler_command(config, sources, output, plugin), env=env,
                                  capture_output=True, text=True)
        print(verification_guidance(compiled.stdout + compiled.stderr, compiled.returncode), flush=True)
        print("\nOriginal verifier diagnostics:", flush=True)
        print(compiled.stdout, end="", flush=True)
        print(compiled.stderr, end="", file=sys.stderr, flush=True)
        trust_report = output.parent / "trust-report.txt"
        if trust_report.exists():
            print("\nTrust report:\n" + trust_report.read_text(), flush=True)
        else:
            print("\nNo trust report produced. Coverage is unknown.", flush=True)
        raise SystemExit(compiled.returncode)
    compiled = subprocess.run(compiler_command(config, sources, output, plugin), env=env)
    if compiled.returncode:
        raise SystemExit(compiled.returncode)
    if not public:
        print("Compilation passed.")
        return
    if task["submission_format"] == "function":
        result = subprocess.run(java_command(config, output, main_class), timeout=10)
        if result.returncode:
            raise SystemExit(result.returncode)
        print("All public harness assertions passed.")
        return
    tests = json.loads(visible.read_text())
    for index, (given, expected) in enumerate(zip(tests["input"], tests["output"])):
        result = subprocess.run(java_command(config, output, main_class), input=given,
                                capture_output=True, text=True, timeout=10)
        casefold = task.get("output_checker") == "casefold_tokens"
        actual_tokens = (result.stdout.casefold() if casefold else result.stdout).split()
        expected_tokens = (expected.casefold() if casefold else expected).split()
        correct = result.returncode == 0 and actual_tokens == expected_tokens
        print(json.dumps({"case": index, "passed": correct, "returncode": result.returncode,
                          "expected": expected, "actual": result.stdout, "stderr": result.stderr}))
        if not correct:
            raise SystemExit(1)
    print(f"All {len(tests['input'])} public tests passed.")


if __name__ == "__main__":
    main()
