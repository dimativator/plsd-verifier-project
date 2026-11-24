"""Run source-reference sanity checks inside the no-network Docker worker only."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import time

from validate_tasks import compare_output


def command_run(command: list[str], *, input_text: str | None = None, timeout: float = 10) -> dict:
    started = time.monotonic()
    try:
        result = subprocess.run(
            command, input=input_text, text=True, capture_output=True, timeout=timeout
        )
        return {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "elapsed_seconds": time.monotonic() - started,
            "timed_out": False,
        }
    except subprocess.TimeoutExpired:
        return {
            "returncode": None,
            "stdout": "",
            "stderr": "per-process timeout",
            "elapsed_seconds": time.monotonic() - started,
            "timed_out": True,
        }


def check_reference(reference: dict, data: dict) -> dict:
    started = time.monotonic()
    language, filename = reference["language"], reference["local_file"]
    record = {
        "language": language,
        "source_file": reference["file"],
        "public_passed": 0,
        "private_passed": 0,
        **{
            key: reference[key]
            for key in ("source_sha256_lf", "executed_sha256_lf", "msvc_i64_format_normalizations")
            if key in reference
        },
    }
    if language == "CPP":
        attempts = []
        for standard in ("gnu++17", "gnu++14"):
            compiled = command_run(
                [
                    "g++",
                    f"-std={standard}",
                    "-DONLINE_JUDGE",
                    "-O2",
                    filename,
                    "-o",
                    "reference-bin",
                ],
                timeout=60,
            )
            attempts.append(
                {
                    "standard": standard,
                    "returncode": compiled["returncode"],
                    "diagnostic": compiled["stderr"][-3000:],
                }
            )
            if compiled["returncode"] == 0:
                break
        record.update({"compilation_attempts": attempts, "online_judge_defined": True})
        command = ["./reference-bin"]
    elif language == "PYTHON":
        compiled = command_run([sys.executable, "-I", "-m", "py_compile", filename], timeout=15)
        command = [sys.executable, "-I", "-B", filename]
    else:
        return {**record, "status": "unsupported_language"}
    if compiled["returncode"] != 0:
        return {
            **record,
            "status": "compile_error",
            "diagnostic": compiled["stderr"][-3000:],
            "elapsed_seconds": time.monotonic() - started,
        }
    for suite in ("public", "private"):
        for index, (input_text, expected) in enumerate(data[suite]):
            result = command_run(
                command, input_text=input_text, timeout=data["per_test_timeout_seconds"]
            )
            if result["returncode"] != 0 or not compare_output(
                result["stdout"], expected, data["checker"]
            ):
                status = (
                    "timeout"
                    if result["timed_out"]
                    else "runtime_error"
                    if result["returncode"] != 0
                    else "wrong_answer"
                )
                return {
                    **record,
                    "status": status,
                    "failed_suite": suite,
                    "failed_test_index": index,
                    "diagnostic": result["stderr"][-2000:],
                    "actual_preview": result["stdout"][:1000],
                    "expected_preview": expected[:1000],
                    "elapsed_seconds": time.monotonic() - started,
                }
            record[f"{suite}_passed"] += 1
    return {**record, "status": "passed", "elapsed_seconds": time.monotonic() - started}


def main() -> None:
    if not Path("/.dockerenv").exists():
        raise SystemExit("Reference execution is allowed only inside Docker")
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    records = [check_reference(reference, data) for reference in data["references"]]
    # A bad answer from an executable source reference raises an oracle concern.
    # Compilation/interpreter incompatibility and slow secondary references are
    # recorded separately; one complete passing source reference is the minimum.
    passed = any(record["status"] == "passed" for record in records)
    contradiction = any(record["status"] == "wrong_answer" for record in records)
    print(
        json.dumps(
            {
                "id": data["id"],
                "status": "passed" if passed and not contradiction else "failed",
                "reference_results": records,
                "passing_reference_count": sum(r["status"] == "passed" for r in records),
                "public_test_count": len(data["public"]),
                "private_test_count": len(data["private"]),
                "oracle_limit": "Passing preserved source references is a sanity check, not an independent proof of test validity.",
            }
        )
    )


if __name__ == "__main__":
    main()
