"""Resolve planned results with at most one retry of genuine external failures.

Raw attempts and their shared spend-ledger entries are never overwritten. The
resolved list, together with the original expected.json, is the analysis input.
"""

import argparse
from copy import deepcopy
from decimal import Decimal, InvalidOperation
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

from experiments import run
from experiments.api_backend import SpendLedger
from experiments.dispatch import batch_admission, bounded_dispatch, controller_guard, stop_requested

IDENTITY = ("phase", "model", "task_id", "condition", "repetition")


def _read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _key(row: dict) -> tuple:
    return tuple(row[name] for name in IDENTITY)


def _result_path(root: Path, spec: dict) -> Path:
    return (
        root
        / spec["model"]
        / spec["task_id"]
        / spec["condition"]
        / f"rep-{spec['repetition']:02d}"
        / "result.json"
    )


def _claim_name(spec: dict) -> str:
    return hashlib.sha256(json.dumps(_key(spec)).encode()).hexdigest()


def _immutable(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as stream:
        json.dump(payload, stream, indent=2)
        stream.write("\n")


def external_failure_reason(row: dict) -> str | None:
    """Use explicit failure evidence; an unsuccessful answer is never enough."""
    if row.get("valid_run") is not False:
        return None
    if row.get("exit_status") in {
        "budget_exhausted",
        "LimitsExceeded",
        "TimeExceeded",
        "RepeatedFormatError",
    }:
        return None
    error = row.get("infrastructure_error") or row.get("evaluation_infrastructure_error")
    if not isinstance(error, dict):
        return None
    kind, message = error.get("type"), str(error.get("message", ""))
    if kind in {"DockerLaunchError", "EvaluatorWorkerError", "EvaluatorProtocolError"}:
        return kind + ": " + message[:1000]
    if kind == "RuntimeError" and message.startswith("Container infrastructure failed:"):
        return message[:1000]
    if kind == "APIError" and message.startswith("Responses request failed ("):
        status = re.search(r"HTTP (None|[0-9]+)", message)
        if status and status.group(1) in {"None", "408", "409", "429", "500", "502", "503", "504"}:
            return message[:1000]
    return None


def _checked_row(path: Path, spec: dict) -> dict:
    row = _read(path)
    if not isinstance(row, dict) or any(row.get(name) != value for name, value in spec.items()):
        raise ValueError(f"Result identity differs from original plan: {path}")
    return row


def verify_retry_environment(config: dict, tasks: list[dict]) -> None:
    """Refuse to silently retry with changed code, images, or task materials."""
    runtime = config.get("runtime", {})
    for name, expected in runtime.get("source_sha256", {}).items():
        if run.source_hash(Path(run.__file__).with_name(name)) != expected:
            raise ValueError(f"Frozen runner source changed: {name}")
    for image, expected in runtime.get("image_ids", {}).items():
        actual = subprocess.check_output(
            ["docker", "image", "inspect", "--format", "{{.Id}}", image], text=True
        ).strip()
        if actual != expected:
            raise ValueError(f"Frozen image changed: {image}")
    for task in tasks:
        base = run.PROJECT / "benchmark-data/codecontests/tasks" / task["id"]
        for relative, expected in task.get("data_sha256_lf", {}).items():
            actual = hashlib.sha256(
                (base / relative).read_bytes().replace(b"\r\n", b"\n")
            ).hexdigest()
            if actual != expected:
                raise ValueError(f"Frozen task data changed: {task['id']}/{relative}")


def _attempt(root: Path, spec: dict, row: dict | None, ledger_rows: list[dict]) -> dict:
    run_id = "/".join([root.name, *(str(spec[name]) for name in IDENTITY)])
    reservations = [entry for entry in ledger_rows if entry.get("run_id") == run_id]
    if reservations:
        cost = sum(
            (
                Decimal(entry["reserved"] if entry["status"] == "pending" else entry["charged"])
                for entry in reservations
            ),
            Decimal(0),
        )
    else:
        cost = Decimal(str(row.get("model_cost_usd", 0))) if row else Decimal(0)
    return {
        "result_path": str(_result_path(root, spec)),
        "present": row is not None,
        "valid_run": row.get("valid_run") if row else False,
        "exit_status": row.get("exit_status") if row else "missing_result",
        "infrastructure_error": row.get("infrastructure_error") if row else None,
        "model_cost_usd": str(cost),
        "cost_source": "shared_ledger" if reservations else "raw_result",
        "cost_is_upper_bound": any(entry["status"] != "settled" for entry in reservations)
        or bool(row and row.get("cost_is_upper_bound")),
        "reservation_count": len(reservations),
    }


def _run_retries(batch: Path, expected: dict, tasks: dict, originals: dict, workers: int) -> dict:
    config = expected["config"]
    retry_root = batch.with_name(batch.name + "-infra-retry-1")
    eligible = [
        spec
        for spec in expected["runs"]
        if originals[_key(spec)] is not None and external_failure_reason(originals[_key(spec)])
    ]
    pending = [
        spec
        for spec in eligible
        if not _result_path(retry_root, spec).exists()
        and not (retry_root / "claims" / (_claim_name(spec) + ".json")).exists()
    ]
    result = {
        "status": "no_pending_retries",
        "admission": None,
        "credentials_loaded": False,
        "errors": {},
    }
    if not pending:
        return result
    try:
        total, per_run = str(config["total_cap_usd"]), str(config["per_run_cap_usd"])
        limits = [Decimal(total), Decimal(per_run)]
    except (KeyError, InvalidOperation) as error:
        raise ValueError("Retry requires explicit valid frozen spend caps") from error
    if any(not limit.is_finite() or limit <= 0 for limit in limits):
        raise ValueError("Retry requires positive finite frozen spend caps")
    retry_config = deepcopy(config)
    retry_config.update(output=str(retry_root), parallel_workers=workers)
    spend_root = Path(config.get("spend_root", batch.parent / "spend"))
    with controller_guard(spend_root, inherit_current_process=True):
        if stop_requested(spend_root):
            result["status"] = "user_stopped"
            return result
        verify_retry_environment(config, [tasks[spec["task_id"]] for spec in pending])
        ledger = SpendLedger(spend_root, total_limit_usd=total, per_run_limit_usd=per_run)
        result["admission"] = batch_admission(
            ledger, len(pending), total_cap_usd=total, per_run_cap_usd=per_run
        )
        if not result["admission"]["admitted"]:
            result["status"] = "budget_stopped_before_dispatch"
            return result
        plan = {
            "original_expected_sha256": run.source_hash(batch / "expected.json"),
            "retry_controller_sha256": run.source_hash(Path(__file__)),
            "manifest_sha256": expected["manifest_sha256"],
            "runs": eligible,
            "config": retry_config,
            "policy": "One retry of explicitly external failures; no retry of wrong answers, formatting, or budgets.",
        }
        plan_path = retry_root / "retry-plan.json"
        if plan_path.exists():
            if _read(plan_path) != plan:
                raise ValueError("Existing retry plan differs from original batch")
        else:
            _immutable(plan_path, plan)
        os.environ["MSWEA_SILENT_STARTUP"] = "1"
        os.environ["MSWEA_GLOBAL_CONFIG_DIR"] = str(run.PROJECT / "pilot/.runtime/mini-api-config")
        api_key = run.load_key()
        result["credentials_loaded"] = True

        def execute_once(spec):
            if stop_requested(spend_root):
                return
            claim = retry_root / "claims" / (_claim_name(spec) + ".json")
            try:
                _immutable(
                    claim,
                    {
                        "spec": spec,
                        "claimed_unix": time.time(),
                        "reason": external_failure_reason(originals[_key(spec)]),
                    },
                )
            except FileExistsError:
                return
            try:
                run.execute(tasks[spec["task_id"]], spec, retry_config, ledger, api_key)
                _checked_row(_result_path(retry_root, spec), spec)
            except Exception as error:
                failure = {"type": type(error).__name__, "message": str(error)[:2000]}
                result["errors"][_key(spec)] = failure
                _immutable(
                    retry_root / "receipts" / (_claim_name(spec) + ".json"),
                    {
                        "spec": spec,
                        "controller_error": failure,
                        "note": "The one allowed retry was claimed; no automatic second attempt.",
                    },
                )

        for _ in bounded_dispatch(
            pending, execute_once, workers=workers, stopped=lambda: stop_requested(spend_root)
        ):
            pass
        result["status"] = "user_stopped" if stop_requested(spend_root) else "finished_dispatch"
    return result


def resolve_batch(
    batch: Path | str,
    *,
    retry_invalid: bool = False,
    workers: int = 2,
    manifest_path: Path | None = None,
) -> dict:
    batch = Path(batch).resolve()
    if workers < 1:
        raise ValueError("workers must be positive")
    if batch.name.endswith("-infra-retry-1"):
        raise ValueError("Resolve the original batch; retries cannot themselves be retried")
    expected_path = batch / "expected.json"
    expected = _read(expected_path)
    specs, config = expected["runs"], expected["config"]
    if not specs or len({_key(spec) for spec in specs}) != len(specs):
        raise ValueError("Original expected.json must contain unique planned identities")
    if Path(config["output"]).resolve() != batch:
        raise ValueError("Original output directory differs from expected.json")
    manifest_path = (manifest_path or batch.parent / "validated-task-manifest.json").resolve()
    if run.source_hash(manifest_path) != expected.get("manifest_sha256"):
        raise ValueError("Validated task manifest changed from original expected.json")
    manifest = _read(manifest_path)
    task_rows = [
        *manifest.get("tasks", []),
        *manifest.get("calibration_tasks", []),
        *manifest.get("reserve_tasks", []),
    ]
    by_id = {task["id"]: task for task in task_rows}
    if any(spec["task_id"] not in by_id for spec in specs):
        raise ValueError("A planned task is absent from the validated manifest")
    original = {
        _key(spec): _checked_row(_result_path(batch, spec), spec)
        if _result_path(batch, spec).exists()
        else None
        for spec in specs
    }
    retry_root = batch.with_name(batch.name + "-infra-retry-1")
    if retry_invalid and any(row is None for row in original.values()):
        raise ValueError(
            "Original batch is incomplete; wait for every planned result before retrying"
        )
    retry = {
        "status": "not_requested",
        "admission": None,
        "credentials_loaded": False,
        "errors": {},
    }
    if retry_invalid:
        retry = _run_retries(batch, expected, by_id, original, workers)
    spend_root = Path(config.get("spend_root", batch.parent / "spend"))
    ledger_path = spend_root / "ledger.json"
    ledger_rows = (
        list(_read(ledger_path).get("reservations", {}).values()) if ledger_path.exists() else []
    )
    resolved, details = [], []
    for spec in specs:
        key, first = _key(spec), original[_key(spec)]
        reason = external_failure_reason(first) if first else None
        retry_path = _result_path(retry_root, spec)
        second = _checked_row(retry_path, spec) if retry_path.exists() else None
        if second is not None and not reason:
            raise ValueError("Found a retry for an ineligible original result")
        selected = second if second is not None else first
        if selected is None:
            selected = {
                **spec,
                "valid_run": False,
                "hidden_passed": False,
                "exit_status": "missing_result",
                "infrastructure_error": {
                    "type": "MissingPlannedRun",
                    "message": "Original result is not present",
                },
                "model_cost_usd": 0,
                "cost_is_upper_bound": True,
            }
        selected = deepcopy(selected)
        selected["resolution"] = {
            "selected_attempt": "infra-retry-1" if second is not None else "original",
            "original_batch": str(batch),
            "retry_reason": reason,
        }
        resolved.append(selected)
        attempts = [_attempt(batch, spec, first, ledger_rows)]
        claim_path = retry_root / "claims" / (_claim_name(spec) + ".json")
        if second is not None or claim_path.exists():
            attempts.append(_attempt(retry_root, spec, second, ledger_rows))
        receipt_path = retry_root / "receipts" / (_claim_name(spec) + ".json")
        details.append(
            {
                "spec": spec,
                "eligible_external_failure": bool(reason),
                "retry_reason": reason,
                "retry_claimed": claim_path.exists(),
                "retry_completed": second is not None,
                "selected_attempt": selected["resolution"]["selected_attempt"],
                "resolved_valid": selected.get("valid_run") is True
                and not selected.get("infrastructure_error"),
                "attempts": attempts,
                "all_attempt_cost_usd": str(
                    sum((Decimal(item["model_cost_usd"]) for item in attempts), Decimal(0))
                ),
                "retry_controller_error": retry["errors"].get(key)
                or (_read(receipt_path).get("controller_error") if receipt_path.exists() else None),
            }
        )
    summary = {
        "original_batch": str(batch),
        "original_expected_sha256": run.source_hash(expected_path),
        "manifest_sha256": expected["manifest_sha256"],
        "planned_runs": len(specs),
        "eligible_external_failures": sum(item["eligible_external_failure"] for item in details),
        "retry_requested": retry_invalid,
        "credentials_loaded": retry["credentials_loaded"],
        "retry_dispatch_status": retry["status"],
        "retry_admission": retry["admission"],
        "resolved_valid_runs": sum(item["resolved_valid"] for item in details),
        "unresolved_runs": sum(not item["resolved_valid"] for item in details),
        "retry_root": str(retry_root),
        "shared_ledger": str(ledger_path),
        "runs": details,
        "all_attempt_cost_usd": str(
            sum((Decimal(item["all_attempt_cost_usd"]) for item in details), Decimal(0))
        ),
        "cost_note": "Analysis uses selected-attempt cost only. All raw attempts and conservative reservations remain in the shared ledger; unresolved identities remain invalid.",
    }
    run.write_json(batch / "resolved-results.json", resolved)
    run.write_json(batch / "resolution.json", summary)
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch", type=Path, required=True)
    parser.add_argument("--retry", choices=["invalid"])
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()
    report = resolve_batch(
        args.batch,
        retry_invalid=args.retry == "invalid",
        workers=args.workers,
        manifest_path=args.manifest,
    )
    print(
        json.dumps(
            {
                key: report[key]
                for key in (
                    "planned_runs",
                    "eligible_external_failures",
                    "resolved_valid_runs",
                    "unresolved_runs",
                    "all_attempt_cost_usd",
                )
            }
        )
    )


if __name__ == "__main__":
    main()
