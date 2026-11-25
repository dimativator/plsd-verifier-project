#!/usr/local/bin/python
"""Public-only tool commands installed read-only in experiment images."""

import ast
import hashlib
import json
import re
from pathlib import Path
import subprocess
import sys
import time


def main():
    command = Path(sys.argv[0]).name
    if command == "verify":
        target = sys.argv[1] if len(sys.argv) > 1 else "main.py"
        path = Path(target).resolve()
        if not path.is_relative_to(Path("/work")) or not path.is_file():
            raise SystemExit("Verification target must be a regular file in /work")
        print(
            "PLINSE_VERIFY_START "
            + json.dumps(
                {"target": target, "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
            ),
            flush=True,
        )
        print("No counterexample found is not proof of task correctness.", flush=True)
        started = time.monotonic()
        try:
            result = subprocess.run(
                [
                    "crosshair",
                    "check",
                    "--analysis_kind=PEP316,asserts",
                    "--report_all",
                    "--per_condition_timeout",
                    "10",
                    "--per_path_timeout",
                    "5",
                    str(path),
                ],
                timeout=30,
            )
            code = result.returncode
        except subprocess.TimeoutExpired:
            print("Verifier timed out after 30 seconds; result is inconclusive.", flush=True)
            code = 124
        print(
            "PLINSE_VERIFY_END "
            + json.dumps({"returncode": code, "elapsed_seconds": time.monotonic() - started}),
            flush=True,
        )
        return code
    source = Path("main.py")
    ast.parse(source.read_text(), filename="main.py")
    if command == "compile":
        print("Python syntax check passed.")
        return 0
    tests = json.loads(Path("public-tests.json").read_text())
    checker = json.loads(Path("task.json").read_text()).get("checker", "tokens")
    if not tests["input"] or len(tests["input"]) != len(tests["output"]):
        raise SystemExit("Public suite is empty or unaligned")
    good = True
    for index, (given, expected) in enumerate(zip(tests["input"], tests["output"])):
        try:
            result = subprocess.run(
                [sys.executable, "-B", "main.py"],
                input=given,
                capture_output=True,
                text=True,
                timeout=10,
            )
            if checker == "integer_tokens":
                try:
                    same = all(
                        re.fullmatch(r"[+-]?[0-9]+", x)
                        for x in result.stdout.split() + expected.split()
                    ) and [int(x) for x in result.stdout.split()] == [
                        int(x) for x in expected.split()
                    ]
                except ValueError:
                    same = False
            elif checker == "casefold_tokens":
                same = result.stdout.casefold().split() == expected.casefold().split()
            else:
                same = result.stdout.split() == expected.split()
            passed = result.returncode == 0 and same
            row = {
                "case": index,
                "passed": passed,
                "returncode": result.returncode,
                "expected": expected[:3000],
                "actual": result.stdout[:3000],
                "stderr": result.stderr[:3000],
            }
        except subprocess.TimeoutExpired:
            passed = False
            row = {"case": index, "passed": False, "timed_out": True}
        print(json.dumps(row), flush=True)
        good = good and passed
        if not passed:
            break
    return 0 if good else 1


if __name__ == "__main__":
    raise SystemExit(main())
