"""Recover a stopped controller once without modifying any original attempt.

A result file, including a wrong answer or resource exit, is never rerun here.
Only identities missing a result at the frozen interruption snapshot are placed
in a separate recovery root. Immutable claims prohibit a second recovery of an
interrupted recovery attempt. All model charges remain in the original ledger.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from copy import deepcopy
from decimal import Decimal
import json
import os
from pathlib import Path
import time

from experiments import run
from experiments.api_backend import SpendLedger
from experiments.resolve_runs import (
    IDENTITY,
    _attempt,
    _checked_row,
    _claim_name,
    _immutable,
    _key,
    _read,
    _result_path,
    verify_retry_environment,
)


def _original_snapshot(batch: Path, specs: list[dict]) -> list[dict]:
    snapshot = []
    for spec in specs:
        result = _result_path(batch, spec)
        directory = result.parent
        row = _checked_row(result, spec) if result.exists() else None
        disposition = (
            "preserve_completed"
            if row is not None
            else "one_external_retry"
            if directory.exists()
            else "first_attempt"
        )
        # Host records are immutable evidence. Workspace scratch caches are not
        # required to classify the stop and are not part of this fingerprint.
        artifacts = {
            name: run.source_hash(directory / name)
            for name in ("result.json", "spec.json", "actions.jsonl", "trajectory.json", "main.py")
            if (directory / name).is_file()
        }
        snapshot.append(
            {
                "spec": spec,
                "disposition": disposition,
                "original_directory_existed": directory.exists(),
                "original_artifact_sha256": artifacts,
            }
        )
    return snapshot


def prepare(
    batch: Path, manifest: Path, *, workers: int = 6, recovery_root: Path | None = None, reason: str
) -> dict:
    batch, manifest = batch.resolve(), manifest.resolve()
    if workers < 1 or not reason.strip():
        raise ValueError("Positive workers and an explicit interruption reason are required")
    if batch.name.endswith("-recovery-1"):
        raise ValueError("Recover the original batch; a recovery cannot be recovered again")
    recovery_root = (recovery_root or batch.with_name(batch.name + "-recovery-1")).resolve()
    if recovery_root == batch or recovery_root.is_relative_to(batch):
        raise ValueError("Recovery must use a separate sibling root")
    expected_path = batch / "expected.json"
    expected = _read(expected_path)
    specs, config = expected["runs"], expected["config"]
    if not specs or len({_key(s) for s in specs}) != len(specs):
        raise ValueError("Original expected.json must contain unique planned identities")
    if Path(config["output"]).resolve() != batch:
        raise ValueError("Original output directory differs from expected.json")
    if run.source_hash(manifest) != expected.get("manifest_sha256"):
        raise ValueError("Validated task manifest changed")
    task_manifest = _read(manifest)
    tasks = {
        t["id"]: t
        for field in ("tasks", "calibration_tasks", "reserve_tasks")
        for t in task_manifest.get(field, [])
    }
    if any(s["task_id"] not in tasks for s in specs):
        raise ValueError("A planned task is absent from the validated manifest")
    verify_retry_environment(config, [tasks[s["task_id"]] for s in specs])
    dispositions = _original_snapshot(batch, specs)
    recover_specs = [r["spec"] for r in dispositions if r["disposition"] != "preserve_completed"]
    recovery_config = deepcopy(config)
    recovery_config.update(output=str(recovery_root), parallel_workers=workers)
    plan = {
        "schema_version": 1,
        "original_batch": str(batch),
        "original_expected_sha256": run.source_hash(expected_path),
        "manifest": str(manifest),
        "manifest_sha256": expected["manifest_sha256"],
        "recovery_controller_sha256": run.source_hash(Path(__file__)),
        "interruption_reason": reason,
        "dispositions": dispositions,
        "runs": recover_specs,
        "config": recovery_config,
        "policy": "Preserve every original result and raw attempt. One separate recovery per missing identity; no second recovery. All charges share the original ledger.",
    }
    plan_path = recovery_root / "recovery-plan.json"
    if plan_path.exists():
        if _read(plan_path) != plan:
            raise ValueError("Frozen recovery plan differs; original evidence/settings changed")
    else:
        if recovery_root.exists() and any(recovery_root.iterdir()):
            raise ValueError("Recovery root already contains unplanned files")
        _immutable(plan_path, plan)
        _immutable(
            recovery_root / "expected.json",
            {
                "runs": recover_specs,
                "config": recovery_config,
                "manifest_sha256": expected["manifest_sha256"],
                "recovery_original_expected_sha256": plan["original_expected_sha256"],
            },
        )
    for spec in recover_specs:
        result = _result_path(recovery_root, spec)
        claim = recovery_root / "claims" / (_claim_name(spec) + ".json")
        if result.exists():
            _checked_row(result, spec)
        elif claim.exists() or result.parent.exists():
            raise ValueError(
                "Recovery was already started but has no result; no automatic second attempt: "
                + "/".join(map(str, _key(spec)))
            )
    return plan


def summarize(plan: dict) -> dict:
    original = Path(plan["original_batch"])
    recovery = Path(plan["config"]["output"])
    ledger_path = Path(plan["config"]["spend_root"]) / "ledger.json"
    ledger_rows = (
        list(_read(ledger_path).get("reservations", {}).values()) if ledger_path.exists() else []
    )
    resolved, details = [], []
    for item in plan["dispositions"]:
        spec = item["spec"]
        first_path = _result_path(original, spec)
        second_path = _result_path(recovery, spec)
        first = _checked_row(first_path, spec) if first_path.exists() else None
        second = _checked_row(second_path, spec) if second_path.exists() else None
        if item["disposition"] == "preserve_completed" and second is not None:
            raise ValueError("A completed original identity was incorrectly recovered")
        selected = first if item["disposition"] == "preserve_completed" else second
        if selected is None:
            selected = {
                **spec,
                "valid_run": False,
                "hidden_passed": False,
                "exit_status": "missing_recovery_result",
                "model_cost_usd": 0,
                "cost_is_upper_bound": True,
                "infrastructure_error": {
                    "type": "ControllerInterrupted",
                    "message": "No selected result; no automatic second recovery",
                },
            }
        selected = deepcopy(selected)
        source = "original" if item["disposition"] == "preserve_completed" else "recovery-1"
        selected["resolution"] = {
            "selected_attempt": source,
            "original_batch": str(original),
            "recovery_disposition": item["disposition"],
        }
        resolved.append(selected)
        attempts = [_attempt(original, spec, first, ledger_rows)]
        if item["disposition"] != "preserve_completed":
            attempts.append(_attempt(recovery, spec, second, ledger_rows))
        details.append(
            {
                "spec": spec,
                "disposition": item["disposition"],
                "selected_attempt": source,
                "selected_result_path": str(first_path if source == "original" else second_path),
                "resolved_valid": selected.get("valid_run") is True
                and not selected.get("infrastructure_error"),
                "attempts": attempts,
                "all_attempt_cost_usd": str(
                    sum((Decimal(a["model_cost_usd"]) for a in attempts), Decimal(0))
                ),
            }
        )
    report = {
        "planned_runs": len(resolved),
        "resolved_valid_runs": sum(r["resolved_valid"] for r in details),
        "unresolved_runs": sum(not r["resolved_valid"] for r in details),
        "original_batch": str(original),
        "recovery_root": str(recovery),
        "original_completed_preserved": sum(
            i["disposition"] == "preserve_completed" for i in plan["dispositions"]
        ),
        "interrupted_original_attempts": sum(
            i["disposition"] == "one_external_retry" for i in plan["dispositions"]
        ),
        "previously_unstarted": sum(
            i["disposition"] == "first_attempt" for i in plan["dispositions"]
        ),
        "all_attempt_cost_usd": str(
            sum((Decimal(r["all_attempt_cost_usd"]) for r in details), Decimal(0))
        ),
        "shared_ledger": str(ledger_path),
        "runs": details,
        "cost_note": "Selected result cost excludes the interrupted original attempt. All original/recovery charges and pending reservation upper bounds are retained in this report and the original shared ledger.",
    }
    run.write_json(recovery / "resolved-results.json", resolved)
    run.write_json(recovery / "resolution.json", report)
    return report


def recover(
    batch: Path,
    manifest: Path,
    *,
    workers: int = 6,
    recovery_root: Path | None = None,
    reason: str,
    prepare_only: bool = True,
) -> dict:
    plan = prepare(batch, manifest, workers=workers, recovery_root=recovery_root, reason=reason)
    root = Path(plan["config"]["output"])
    pending = [s for s in plan["runs"] if not _result_path(root, s).exists()]
    if prepare_only:
        report = summarize(plan)
        report.update(
            credentials_loaded=False,
            model_calls=0,
            pending_recovery_runs=len(pending),
            prepare_only=True,
        )
        return report
    if pending:
        cfg = plan["config"]
        manifest_rows = _read(Path(plan["manifest"]))
        by_id = {
            t["id"]: t
            for name in ("tasks", "calibration_tasks", "reserve_tasks")
            for t in manifest_rows.get(name, [])
        }
        ledger = SpendLedger(
            Path(cfg["spend_root"]),
            total_limit_usd=cfg["total_cap_usd"],
            per_run_limit_usd=cfg["per_run_cap_usd"],
        )
        os.environ["MSWEA_SILENT_STARTUP"] = "1"
        os.environ["MSWEA_GLOBAL_CONFIG_DIR"] = str(run.PROJECT / "pilot/.runtime/mini-api-config")
        api_key = run.load_key()

        def execute_once(spec):
            claim = root / "claims" / (_claim_name(spec) + ".json")
            _immutable(
                claim,
                {
                    "spec": spec,
                    "claimed_unix": time.time(),
                    "original_expected_sha256": plan["original_expected_sha256"],
                },
            )
            row = run.execute(by_id[spec["task_id"]], spec, cfg, ledger, api_key)
            print(
                json.dumps(
                    {
                        k: row[k]
                        for k in (
                            "model",
                            "task_id",
                            "condition",
                            "repetition",
                            "exit_status",
                            "model_cost_usd",
                            "solve_seconds",
                        )
                    }
                ),
                flush=True,
            )
            return row

        try:
            with ThreadPoolExecutor(max_workers=workers) as pool:
                for future in as_completed([pool.submit(execute_once, s) for s in pending]):
                    future.result()
        finally:
            summarize(plan)
    return summarize(plan)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--recovery-root", type=Path)
    parser.add_argument("--reason", required=True)
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Run the frozen recovery; default is prepare-only with no credentials",
    )
    args = parser.parse_args()
    report = recover(
        args.batch,
        args.manifest,
        workers=args.workers,
        recovery_root=args.recovery_root,
        reason=args.reason,
        prepare_only=not args.execute,
    )
    print(
        json.dumps(
            {
                k: report[k]
                for k in (
                    "planned_runs",
                    "resolved_valid_runs",
                    "unresolved_runs",
                    "original_completed_preserved",
                    "interrupted_original_attempts",
                    "previously_unstarted",
                    "all_attempt_cost_usd",
                )
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
