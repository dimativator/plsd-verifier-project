"""Queue 300-run repetitions under one API ledger, with a graceful stop file.

This controller adds repetitions without changing the original frozen protocol.
It reserves each active job's whole remaining per-run allowance before dispatch.
The final repetition may be partial when budget/stop prevents further admission;
its unstarted jobs remain missing and it is excluded from repetition summaries.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from copy import deepcopy
from datetime import datetime, timezone
from decimal import Decimal
import json
import os
from pathlib import Path
import time

from experiments import distributed as d, run
from experiments.api_backend import SpendLedger


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def money(value, *, zero=False) -> Decimal:
    result = Decimal(str(value))
    if not result.is_finite() or result < 0 or (not zero and result == 0):
        raise ValueError("Budget amounts must be finite and positive (offsets may be zero)")
    return result


def accounted_by_run(snapshot: dict) -> dict[str, Decimal]:
    totals = defaultdict(Decimal)
    for row in snapshot["reservations"].values():
        amount = money(row["reserved"] if row["status"] == "pending" else row["charged"], zero=True)
        totals[row["run_id"]] += amount
    return dict(totals)


def admission(snapshot: dict, active: set[str], per_run: Decimal, cap: Decimal) -> dict:
    """Hold lifetime allowances, not just the next request's reservation.

    Active threads may make requests after this snapshot. Their full remaining
    allowances are held here, so those requests cannot invalidate admission.
    Only the controller thread adds/removes active identities.
    """
    costs = accounted_by_run(snapshot)
    spent = sum(costs.values(), Decimal(0))
    held = sum(
        (max(Decimal(0), per_run - costs.get(key, Decimal(0))) for key in active), Decimal(0)
    )
    violation = any(value > per_run for value in costs.values())
    return {
        "accounted_usd": str(spent),
        "active_allowance_usd": str(held),
        "required_for_next_run_usd": str(spent + held + per_run),
        "per_run_bound_violation": violation,
        "admitted": not violation and spent + held + per_run <= cap,
    }


def round_specs(plan: dict, repetition: int) -> list[dict]:
    if repetition <= max(s["repetition"] for s in plan["runs"]):
        raise ValueError("Extension repetition overlaps the original assignment")
    first = min(s["repetition"] for s in plan["runs"])
    groups = {}
    for spec in plan["runs"]:
        if spec["repetition"] == first:
            groups.setdefault((spec["model"], spec["task_id"]), {})[spec["condition"]] = spec
    if len(groups) != 100 or any(set(g) != d.ARMS for g in groups.values()):
        raise ValueError("Extension requires 100 tasks with all three conditions")
    specs = []
    for (_, task_id), arms in groups.items():
        for arm in run.task_condition_order(
            ["baseline", "verifier", "guided_verifier"], task_id, repetition
        ):
            spec = deepcopy(arms[arm])
            spec.update(repetition=repetition, worker_id="ours")
            spec.pop("analysis_stratum", None)
            specs.append(spec)
    return specs


def run_id(output: Path, spec: dict) -> str:
    return "/".join(
        [output.name]
        + [str(spec[k]) for k in ("phase", "model", "task_id", "condition", "repetition")]
    )


def stop(output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    (output / "STOP").write_text(
        "Stop further admissions; let active evaluations finish.\n", encoding="utf-8"
    )


def controller(
    *,
    plan_path: Path,
    manifest: Path,
    output: Path,
    after_worker: Path,
    cap_usd="50.00",
    prior_charge_usd="0",
    remote_reserve_usd="0",
    budget_scope="new_batches_only",
    workers=8,
    prepare_only=False,
) -> dict:
    if workers < 1:
        raise ValueError("workers must be positive")
    output, after_worker = output.resolve(), after_worker.resolve()
    plan_path, manifest = plan_path.resolve(), manifest.resolve()
    plan = d._load_plan(plan_path)
    cap = money(cap_usd)
    offset = money(prior_charge_usd, zero=True) + money(remote_reserve_usd, zero=True)
    allowance = cap - offset
    if allowance <= 0:
        raise ValueError("Prior charges and remote allowance exhaust the combined cap")
    if budget_scope not in {"new_batches_only", "all_experiments"}:
        raise ValueError("Unknown budget scope")
    tasks = d._tasks(plan, manifest, plan["runs"])
    image_ids = d.validate_environment(plan, tasks)
    first_rep = max(s["repetition"] for s in plan["runs"]) + 1
    round_specs(plan, first_rep)
    definition = {
        "schema_version": 1,
        "source_plan": str(plan_path),
        "source_plan_sha256": plan["plan_sha256"],
        "controller_sha256": run.source_hash(Path(__file__)),
        "manifest": str(manifest),
        "manifest_sha256": plan["manifest_sha256"],
        "batch_size": 300,
        "first_repetition": first_rep,
        "workers": workers,
        "combined_cap_usd": str(cap),
        "budget_scope": budget_scope,
        "prior_charge_usd": str(money(prior_charge_usd, zero=True)),
        "remote_reserve_usd": str(money(remote_reserve_usd, zero=True)),
        "new_ledger_cap_usd": str(allowance),
        "after_worker": str(after_worker),
        "stop_rule": "Budget and STOP only; no automatic stopping on scores. "
        "Hold full per-run allowances before admission; drain active jobs. "
        "Exclude incomplete repetitions from repetition aggregates.",
        "accounting_limit": "This ledger covers this controller only. Remote expenditure "
        "requires a separately enforced allocation; shared key is not a shared ledger.",
    }
    d._immutable(output / "extension-plan.json", definition)
    status = {
        **definition,
        "status": "prepared",
        "pid": os.getpid(),
        "updated_utc": now(),
        "completed_repetitions": [],
        "completed_runs": 0,
        "accounted_usd": "0",
        "combined_accounted_and_reserved_usd": str(offset),
        "credentials_loaded": False,
    }
    if prepare_only:
        return status
    descriptor = os.open(output / "controller.lock", os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    os.write(descriptor, str(os.getpid()).encode("ascii"))
    os.close(descriptor)
    ledger = None

    def publish(**changes):
        status.update(changes, updated_utc=now())
        status["draining"] = bool(status.get("draining") and status.get("active_runs", 0) > 0)
        if ledger is not None:
            snapshot = ledger.snapshot()
            costs = accounted_by_run(snapshot)
            spent = sum(costs.values(), Decimal(0))
            status.update(
                accounted_usd=str(spent),
                combined_accounted_and_reserved_usd=str(offset + spent),
                pending_requests=sum(
                    r["status"] == "pending" for r in snapshot["reservations"].values()
                ),
            )
        run.write_json(output / "status.json", status)

    try:
        # Do not compete with, restart, or change the original controller.
        while not (after_worker / "worker-report.json").exists():
            if (output / "STOP").exists():
                publish(status="user_stopped_before_extension")
                return status
            if not (after_worker / "controller.lock").exists():
                raise ValueError(
                    "Original worker has no completion report or active controller; inspect it first"
                )
            publish(status="waiting_for_original_worker")
            time.sleep(10)
        predecessor = d._read(after_worker / "worker-report.json")
        if predecessor.get("status") != "complete":
            raise ValueError("Original worker did not complete normally; inspect before extending")
        # Detect changes made while the background controller was waiting.
        d.validate_environment(plan, tasks)
        ledger = SpendLedger(
            output / "spend",
            total_limit_usd=str(allowance),
            per_run_limit_usd=plan["shared_config"]["per_run_cap_usd"],
        )
        per_run = money(plan["shared_config"]["per_run_cap_usd"])
        by_id = {t["id"]: t for t in tasks}
        os.environ["MSWEA_SILENT_STARTUP"] = "1"
        os.environ["MSWEA_GLOBAL_CONFIG_DIR"] = str(run.PROJECT / "pilot/.runtime/mini-api-config")
        key = None
        repetition = first_rep
        while True:
            if (output / "STOP").exists():
                publish(status="user_stopped", active_runs=0)
                break
            specs = round_specs(plan, repetition)
            batch_root = output / f"extension-rep-{repetition:04d}"
            config = deepcopy(plan["shared_config"])
            config.update(
                output=str(batch_root),
                spend_root=str(output / "spend"),
                total_cap_usd=str(allowance),
                parallel_workers=workers,
            )
            config["runtime"]["image_ids"] = image_ids
            expected = {
                "runs": specs,
                "config": config,
                "manifest_sha256": plan["manifest_sha256"],
                "analysis_plan": deepcopy(plan.get("analysis_plan", {})),
                "extension": {
                    "source_plan_sha256": plan["plan_sha256"],
                    "controller_plan_sha256": d._digest(definition),
                    "incomplete_repetitions": "Preserve every outcome; exclude partial repetitions from repetition aggregates.",
                },
            }
            # Inspect every attempt before resuming; never overwrite partial artifacts.
            pending, existing = [], []
            for spec in specs:
                path = d._result_path(batch_root, spec)
                if path.exists():
                    row = d._read(path)
                    d._check_row(row, spec, config)
                    if row.get("valid_run") is not True or row.get("infrastructure_error"):
                        raise ValueError(
                            f"Prior infrastructure failure requires resolution: {path}"
                        )
                    existing.append(row)
                elif path.parent.exists():
                    raise ValueError(
                        f"Incomplete original attempt; preserve/resolve before resuming: {path.parent}"
                    )
                else:
                    pending.append(spec)
            status["completed_runs"] += len(existing)
            # Avoid even creating a planned round if no first run can be admitted.
            next_admission = admission(ledger.snapshot(), set(), per_run, allowance)
            if pending and not next_admission["admitted"]:
                publish(status="budget_stopped", next_admission=next_admission, active_runs=0)
                break
            d._immutable(batch_root / "expected.json", expected)
            publish(
                status="running",
                repetition=repetition,
                batch_completed=len(existing),
                active_runs=0,
            )
            active = {}
            cursor = 0
            reason = None
            with ThreadPoolExecutor(max_workers=workers) as pool:
                while cursor < len(pending) or active:
                    if (output / "STOP").exists():
                        reason = "user_stopped"
                    while reason is None and cursor < len(pending) and len(active) < workers:
                        check = admission(
                            ledger.snapshot(), set(active.values()), per_run, allowance
                        )
                        if not check["admitted"]:
                            # A running job can free its unused lifetime allowance.
                            if not active:
                                reason = "budget_stopped"
                            break
                        if key is None:
                            key = run.load_key()
                            status["credentials_loaded"] = True
                        if (output / "STOP").exists():
                            reason = "user_stopped"
                            break
                        spec = pending[cursor]
                        identity = run_id(batch_root, spec)
                        future = pool.submit(
                            run.execute, by_id[spec["task_id"]], spec, config, ledger, key
                        )
                        active[future] = identity
                        cursor += 1
                    publish(
                        active_runs=len(active),
                        batch_launched=len(existing) + cursor,
                        draining=reason is not None,
                    )
                    if not active:
                        break
                    finished, _ = wait(active, timeout=5, return_when=FIRST_COMPLETED)
                    for future in finished:
                        row = future.result()
                        # The future finishes only after all request reservations settle.
                        del active[future]
                        status["completed_runs"] += 1
                        status["batch_completed"] += 1
                        print(
                            json.dumps(
                                {
                                    k: row[k]
                                    for k in (
                                        "task_id",
                                        "condition",
                                        "repetition",
                                        "exit_status",
                                        "model_cost_usd",
                                    )
                                }
                            ),
                            flush=True,
                        )
                        if row.get("valid_run") is not True or row.get("infrastructure_error"):
                            reason = "infrastructure_stopped"
            complete = status["batch_completed"] == 300
            report = {
                "repetition": repetition,
                "planned_runs": 300,
                "completed_runs": status["batch_completed"],
                "complete": complete,
                "eligible_for_repetition_summary": complete and reason != "infrastructure_stopped",
                "not_launched_runs": len(pending) - cursor,
                "stop_reason": reason,
                "finished_utc": now(),
            }
            run.write_json(batch_root / "batch-report.json", report)
            if report["eligible_for_repetition_summary"]:
                status["completed_repetitions"].append(repetition)
            publish(active_runs=0)
            if reason:
                publish(status=reason)
                break
            repetition += 1
        return status
    except Exception as error:
        publish(status="controller_error", error_type=type(error).__name__, error=str(error))
        raise
    finally:
        if ledger is not None:
            run.write_json(output / "spend-snapshot.json", ledger.snapshot())
        (output / "controller.lock").unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["run", "stop", "status"])
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--plan", type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--after-worker", type=Path)
    parser.add_argument("--cap-usd", default="50.00")
    parser.add_argument("--prior-charge-usd", default="0")
    parser.add_argument("--remote-reserve-usd", default="0")
    parser.add_argument(
        "--budget-scope",
        choices=["new_batches_only", "all_experiments"],
        default="new_batches_only",
    )
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--prepare-only", action="store_true")
    args = parser.parse_args()
    if args.action == "stop":
        stop(args.output)
        print("Stop requested. Active evaluations will finish; no more jobs will launch.")
    elif args.action == "status":
        print((args.output / "status.json").read_text(encoding="utf-8"))
    else:
        if not all([args.plan, args.manifest, args.after_worker]):
            parser.error("run requires --plan, --manifest and --after-worker")
        print(
            json.dumps(
                controller(
                    plan_path=args.plan,
                    manifest=args.manifest,
                    output=args.output,
                    after_worker=args.after_worker,
                    cap_usd=args.cap_usd,
                    prior_charge_usd=args.prior_charge_usd,
                    remote_reserve_usd=args.remote_reserve_usd,
                    budget_scope=args.budget_scope,
                    workers=args.workers,
                    prepare_only=args.prepare_only,
                ),
                indent=2,
            ),
            flush=True,
        )


if __name__ == "__main__":
    main()
