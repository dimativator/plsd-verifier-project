"""Validate selected source references using the project's isolated Docker runtime."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from pathlib import Path
import shutil
import time
import uuid

try:
    from experiments.validate_tasks import (
        BANDS,
        PROJECT,
        canonical_sha256,
        load,
        portable_cpp,
        read_suite,
        seeded_key,
        select_by_band,
    )
except ModuleNotFoundError:
    from validate_tasks import (
        BANDS,
        PROJECT,
        canonical_sha256,
        load,
        portable_cpp,
        read_suite,
        seeded_key,
        select_by_band,
    )


def preflight_task(project: Path, task: dict, scratch: Path, timeout: float) -> dict:
    try:
        from experiments.runtime import run_isolated
    except ModuleNotFoundError:
        from runtime import run_isolated
    task_dir = project / "benchmark-data/codecontests/tasks" / task["id"]
    for relative, expected in task["data_sha256_lf"].items():
        if canonical_sha256(task_dir / relative) != expected:
            return {"id": task["id"], "status": "data_hash_drift", "file": relative}
    workspace = scratch / f"{task['id']}-{uuid.uuid4().hex[:8]}"
    workspace.mkdir(parents=True, exist_ok=False)
    for filename in ("validation_worker.py", "validate_tasks.py"):
        shutil.copyfile(Path(__file__).with_name(filename), workspace / filename)
    references = []
    for reference in sorted(
        task["references"], key=lambda r: (r["language"] != "CPP", r["language"] != "PYTHON")
    ):
        if reference["language"] not in {"CPP", "PYTHON"}:
            continue
        local = Path(reference["file"]).name
        source = task_dir / "evaluator" / reference["file"]
        if source.is_symlink() or not source.resolve().is_relative_to(
            (task_dir / "evaluator/references").resolve()
        ):
            return {"id": task["id"], "status": "reference_path_escape"}
        source_text = source.read_text(encoding="utf-8")
        adapted, normalizations = (
            portable_cpp(source_text) if reference["language"] == "CPP" else (source_text, 0)
        )
        (workspace / local).write_text(adapted, encoding="utf-8")
        references.append(
            {
                **reference,
                "local_file": local,
                "source_sha256_lf": canonical_sha256(source),
                "executed_sha256_lf": canonical_sha256(workspace / local),
                "msvc_i64_format_normalizations": normalizations,
            }
        )
    payload = {
        "id": task["id"],
        "checker": task["checker"],
        "public": read_suite(task_dir / "public/public-tests.json"),
        "private": read_suite(task_dir / "evaluator/private-tests.json"),
        "references": references,
        "per_test_timeout_seconds": 10,
    }
    (workspace / "reference-check.json").write_text(json.dumps(payload), encoding="utf-8")
    started = time.monotonic()
    result = run_isolated(
        workspace, "python validation_worker.py reference-check.json", timeout=timeout
    )
    record = {
        "id": task["id"],
        "docker_elapsed_seconds": time.monotonic() - started,
        "worker_workspace": str(workspace),
        "runtime": {key: result.get(key) for key in ("returncode", "timed_out", "elapsed_seconds")},
    }
    if result["returncode"] != 0:
        return {
            **record,
            "status": "worker_timeout" if result.get("timed_out") else "worker_error",
            "diagnostic": result.get("stderr", "")[-3000:],
        }
    try:
        data = json.loads(result["stdout"])
    except (ValueError, KeyError):
        return {
            **record,
            "status": "worker_output_error",
            "diagnostic": result.get("stdout", "")[-3000:],
        }
    return {**record, **data}


def freeze(manifest: dict, results: list[dict], per_band: int) -> dict:
    indexed = {result["id"]: result for result in results}
    accepted = []
    for row in manifest["reviewed_candidates"]:
        if indexed.get(row["id"], {}).get("status") == "passed":
            accepted.append(
                {
                    **row,
                    "behavioral_validation": "passed",
                    "reference_preflight": indexed[row["id"]],
                }
            )
    tasks, _ = select_by_band(accepted, per_band, 0, manifest["seed"])
    calibration = []
    for task in manifest["calibration_tasks"]:
        record = indexed.get(task["id"], {})
        if record.get("status") != "passed":
            raise ValueError(f"Calibration reference validation did not pass: {task['id']}")
        calibration.append(
            {**task, "behavioral_validation": "passed", "reference_preflight": record}
        )
    chosen = {task["id"] for task in tasks}
    reserves = sorted(
        (task for task in accepted if task["id"] not in chosen),
        key=lambda r: (BANDS.index(r["rating_band"]), seeded_key(r["id"], manifest["seed"])),
    )
    old = {task["id"] for task in manifest["tasks"]}
    return {
        **manifest,
        "status": "reference_sanity_passed_ready_for_protocol_freeze",
        "tasks": tasks,
        "calibration_tasks": calibration,
        "reserves": reserves,
        "replacement_record": {
            "removed_from_initial_sample": sorted(old - chosen),
            "promoted_from_seeded_reserves": sorted(chosen - old),
        },
        "reference_preflight_summary": {
            "attempted": len(results),
            "passed": len(accepted) + len(calibration),
            "statuses": {
                status: sum(r["status"] == status for r in results)
                for status in sorted({r["status"] for r in results})
            },
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=PROJECT)
    parser.add_argument(
        "--manifest", type=Path, default=PROJECT / "runs/calibration-20261123/task-validation.json"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT / "runs/calibration-20261123/reference-preflight.json",
    )
    parser.add_argument("--kind", choices=("all", "calibration", "main"), default="all")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--task-timeout", type=float, default=240)
    parser.add_argument("--limit", type=int)
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Reuse completed pass/fail records from output; worker errors are retried",
    )
    parser.add_argument("--freeze-output", type=Path)
    parser.add_argument("--per-band", type=int, default=50)
    args = parser.parse_args()
    manifest = load(args.manifest)
    tasks = []
    if args.kind in {"all", "calibration"}:
        tasks.extend(manifest["calibration_tasks"])
    if args.kind in {"all", "main"}:
        tasks.extend(manifest["reviewed_candidates"])
    if args.limit is not None:
        tasks = tasks[: args.limit]
    previous_data = load(args.output) if args.resume and args.output.exists() else {}
    if previous_data and previous_data.get("manifest_sha256_lf") != canonical_sha256(args.manifest):
        raise ValueError("Cannot resume reference checks against a different task manifest")
    previous = previous_data.get("results", [])
    results = {r["id"]: r for r in previous if r["status"] in {"passed", "failed"}}
    scratch = args.output.parent / "reference-workspaces"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    wanted = {task["id"] for task in tasks}
    results = {key: value for key, value in results.items() if key in wanted}

    def save() -> None:
        args.output.write_text(
            json.dumps(
                {
                    "manifest_sha256_lf": canonical_sha256(args.manifest),
                    "reference_portability_policy": "Copied C++ source only: MSVC %I64[d/i/u/o/x/X] replaced with ISO %ll[d/i/u/o/x/X]; original source untouched. Python references are not translated.",
                    "results": sorted(results.values(), key=lambda r: r["id"]),
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(preflight_task, args.project, task, scratch, args.task_timeout): task[
                "id"
            ]
            for task in tasks
            if task["id"] not in results
        }
        for future in as_completed(futures):
            task_id = futures[future]
            try:
                result = future.result()
            except Exception as error:
                result = {
                    "id": task_id,
                    "status": "controller_error",
                    "diagnostic": f"{type(error).__name__}: {error}",
                }
            results[task_id] = result
            save()
            print(
                json.dumps(
                    {
                        "id": task_id,
                        "status": result["status"],
                        "completed": len(results),
                        "total": len(tasks),
                    }
                ),
                flush=True,
            )
    if args.freeze_output:
        frozen = freeze(manifest, list(results.values()), args.per_band)
        args.freeze_output.write_text(
            json.dumps(frozen, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        print(
            json.dumps({"freeze_output": str(args.freeze_output), "status": frozen["status"]}),
            flush=True,
        )


if __name__ == "__main__":
    main()
