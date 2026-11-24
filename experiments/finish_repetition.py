"""Finish one interrupted extension repetition, preserving every raw attempt."""

from __future__ import annotations

import argparse
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from copy import deepcopy
from decimal import Decimal
import json
import os
from pathlib import Path

from experiments import distributed as d, extend_rounds as e, resolve_runs as resolver, run
from experiments.api_backend import SpendLedger


def inspect(batch: Path, manifest: Path) -> dict:
    batch, manifest = batch.resolve(), manifest.resolve()
    root = batch.parent
    definition = d._read(root / "extension-plan.json")
    expected = d._read(batch / "expected.json")
    plan = d._load_plan(Path(definition["source_plan"]))
    if (
        expected["extension"]["source_plan_sha256"] != plan["plan_sha256"]
        or expected["extension"]["controller_plan_sha256"] != d._digest(definition)
        or expected["manifest_sha256"] != plan["manifest_sha256"]
    ):
        raise ValueError("Interrupted repetition differs from original frozen protocol")
    specs, config = expected["runs"], expected["config"]
    reps = {s["repetition"] for s in specs}
    if len(reps) != 1 or specs != e.round_specs(plan, next(iter(reps))):
        raise ValueError("Expected exactly one original 300-evaluation repetition")
    tasks = d._tasks(plan, manifest, specs)
    image_ids = d.validate_environment(plan, tasks)
    wanted = deepcopy(plan["shared_config"])
    wanted.update(
        output=str(batch),
        spend_root=str(root / "spend"),
        total_cap_usd=definition["new_ledger_cap_usd"],
        parallel_workers=definition["workers"],
    )
    wanted["runtime"]["image_ids"] = image_ids
    if config != wanted:
        raise ValueError("Interrupted repetition settings changed")
    pending, rows, external = [], [], []
    for spec in specs:
        path = d._result_path(batch, spec)
        if path.exists():
            row = resolver._checked_row(path, spec)
            d._check_row(row, spec, config)
            if row.get("valid_run") is not True or row.get("infrastructure_error"):
                if not resolver.external_failure_reason(row):
                    raise ValueError(f"Unrecognized invalid result requires inspection: {path}")
                external.append(spec)
            rows.append(row)
        elif path.parent.exists():
            raise ValueError(f"Incomplete attempt directory requires inspection: {path.parent}")
        else:
            pending.append(spec)
    return dict(
        batch=batch,
        root=root,
        expected=expected,
        config=config,
        specs=specs,
        tasks=tasks,
        pending=pending,
        rows=rows,
        external=external,
        repetition=next(iter(reps)),
    )


def finish(batch: Path, manifest: Path, *, workers=8, prepare_only=False) -> dict:
    if workers < 1:
        raise ValueError("workers must be positive")
    info = inspect(batch, manifest)
    batch, root, config = info["batch"], info["root"], info["config"]
    status = d._read(root / "status.json")
    report = dict(
        repetition=info["repetition"],
        planned_runs=300,
        preserved_original_runs=len(info["rows"]),
        pending_original_runs=len(info["pending"]),
        known_external_failures=len(info["external"]),
        operation="finish_repetition_only",
        credentials_loaded=False,
        resolver_credentials_loaded=False,
        status="prepared",
        active_runs=0,
    )
    if prepare_only:
        return report
    lock = root / "controller.lock"
    descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    os.write(descriptor, str(os.getpid()).encode("ascii"))
    os.close(descriptor)
    ledger = None
    previous_round_runs = status["completed_runs"] - status["batch_completed"]
    completed = len(info["rows"])

    def publish(**changes):
        report.update(changes, updated_utc=e.now())
        report["draining"] = (
            report["status"] in {"user_stopped", "infrastructure_stopped"}
            and report["active_runs"] > 0
        )
        if ledger is not None:
            snapshot = ledger.snapshot()
            spent = sum(e.accounted_by_run(snapshot).values(), Decimal(0))
            report.update(
                accounted_usd=str(spent),
                pending_requests=sum(
                    r["status"] == "pending" for r in snapshot["reservations"].values()
                ),
            )
        status.update(
            report,
            pid=os.getpid(),
            completed_runs=previous_round_runs + completed,
            batch_completed=completed,
        )
        if "accounted_usd" in report:
            status["combined_accounted_and_reserved_usd"] = str(
                Decimal(status["prior_charge_usd"])
                + Decimal(status["remote_reserve_usd"])
                + Decimal(report["accounted_usd"])
            )
        run.write_json(root / "status.json", status)
        run.write_json(batch / "finish-repetition-report.json", report)

    try:
        # A separate immutable recovery record leaves the original controller frozen.
        recovery = {
            "schema_version": 1,
            "operation": "finish_repetition_only",
            "repetition": info["repetition"],
            "expected_sha256": run.source_hash(batch / "expected.json"),
            "controller_sha256": run.source_hash(Path(__file__)),
            "workers": workers,
            "policy": "Fill unstarted original identities; retain originals; "
            "one separate retry of recognized external failures; stop after this repetition.",
        }
        d._immutable(batch / "finish-repetition-plan.json", recovery)
        checkpoint = batch / "before-finish-checkpoint.json"
        if not checkpoint.exists():
            d._immutable(
                checkpoint,
                {
                    "status": deepcopy(status),
                    "batch_report": d._read(batch / "batch-report.json"),
                    "preserved_results": {
                        str(d._result_path(batch, row).relative_to(batch)): run.source_hash(
                            d._result_path(batch, row)
                        )
                        for row in info["rows"]
                    },
                },
            )
        if (root / "STOP").exists():
            publish(status="user_stopped")
            return report
        ledger = SpendLedger(
            Path(config["spend_root"]),
            total_limit_usd=config["total_cap_usd"],
            per_run_limit_usd=config["per_run_cap_usd"],
        )
        cap, per_run = Decimal(config["total_cap_usd"]), Decimal(config["per_run_cap_usd"])
        snapshot = ledger.snapshot()
        costs = e.accounted_by_run(snapshot)
        # The whole fixed remainder fits at the lifetime ceiling; no global-budget
        # exception can turn an unstarted identity into an agent failure.
        required = per_run * (len(info["pending"]) + len(info["external"]))
        if (
            any(value > per_run for value in costs.values())
            or sum(costs.values(), Decimal(0)) + required > cap
        ):
            publish(status="budget_stopped", required_remaining_usd=str(required))
            return report
        os.environ["MSWEA_SILENT_STARTUP"] = "1"
        os.environ["MSWEA_GLOBAL_CONFIG_DIR"] = str(run.PROJECT / "pilot/.runtime/mini-api-config")
        by_id = {task["id"]: task for task in info["tasks"]}
        key = None
        active = {}
        cursor = 0
        reason = None
        with ThreadPoolExecutor(max_workers=workers) as pool:
            while cursor < len(info["pending"]) or active:
                if (root / "STOP").exists():
                    reason = "user_stopped"
                while reason is None and cursor < len(info["pending"]) and len(active) < workers:
                    if key is None:
                        key = run.load_key()
                        report["credentials_loaded"] = True
                    if (root / "STOP").exists():
                        reason = "user_stopped"
                        break
                    spec = info["pending"][cursor]
                    future = pool.submit(
                        run.execute, by_id[spec["task_id"]], spec, config, ledger, key
                    )
                    active[future] = spec
                    cursor += 1
                publish(
                    status=reason or "finishing_repetition",
                    active_runs=len(active),
                    not_launched_runs=len(info["pending"]) - cursor,
                )
                if not active:
                    break
                done, _ = wait(active, timeout=5, return_when=FIRST_COMPLETED)
                for future in done:
                    row = future.result()
                    del active[future]
                    completed += 1
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
        if reason:
            publish(status=reason, active_runs=0)
            return report
        if (root / "STOP").exists():
            publish(status="user_stopped", active_runs=0)
            return report
        originals = [
            resolver._checked_row(d._result_path(batch, spec), spec) for spec in info["specs"]
        ]
        eligible = [row for row in originals if resolver.external_failure_reason(row)]
        costs = e.accounted_by_run(ledger.snapshot())
        if sum(costs.values(), Decimal(0)) + per_run * len(eligible) > cap:
            publish(status="budget_stopped_before_retries", active_runs=0)
            return report
        # Resolver records one claimed retry per external failure, with original
        # and retry costs retained in this same ledger. No answer-quality retries.
        publish(status="resolving_external_failures", active_runs=len(eligible))
        resolution = resolver.resolve_batch(
            batch, retry_invalid=True, workers=1, manifest_path=manifest.resolve()
        )
        report["resolver_credentials_loaded"] = resolution["credentials_loaded"]
        report["credentials_loaded"] = (
            report["credentials_loaded"] or resolution["credentials_loaded"]
        )
        selected = d._read(batch / "resolved-results.json")
        complete = (
            len(selected) == 300
            and resolution["unresolved_runs"] == 0
            and all(
                row.get("valid_run") is True and not row.get("infrastructure_error")
                for row in selected
            )
        )
        report.update(
            completed_runs=300,
            resolved_valid_runs=resolution["resolved_valid_runs"],
            infrastructure_retries=sum(r["retry_claimed"] for r in resolution["runs"]),
            complete=complete,
            eligible_for_repetition_summary=complete,
            selected_results=str(batch / "resolved-results.json"),
        )
        if complete:
            checkpoint_data = d._read(checkpoint)
            if any(
                run.source_hash(batch / name) != expected_hash
                for name, expected_hash in checkpoint_data["preserved_results"].items()
            ):
                raise ValueError("An original preserved result changed during recovery")
            report["scores"] = {
                arm: {
                    "solved": sum(
                        bool(row["hidden_passed"]) for row in selected if row["condition"] == arm
                    ),
                    "total": sum(row["condition"] == arm for row in selected),
                }
                for arm in sorted(d.ARMS)
            }
            status["completed_repetitions"] = sorted(
                set(status["completed_repetitions"]) | {info["repetition"]}
            )
            run.write_json(
                batch / "batch-report.json",
                {
                    "repetition": info["repetition"],
                    "planned_runs": 300,
                    "completed_runs": 300,
                    "complete": True,
                    "eligible_for_repetition_summary": True,
                    "not_launched_runs": 0,
                    "stop_reason": "requested_repetition_finished",
                    "finished_utc": e.now(),
                    "selected_results": str(batch / "resolved-results.json"),
                    "raw_originals_preserved": True,
                    "infrastructure_retries": report["infrastructure_retries"],
                },
            )
        publish(
            status="complete_requested_repetition" if complete else "unresolved_external_failure",
            active_runs=0,
        )
        return report
    except Exception as error:
        publish(
            status="controller_error",
            error_type=type(error).__name__,
            error=str(error),
            active_runs=0,
        )
        raise
    finally:
        if ledger is not None:
            run.write_json(root / "spend-snapshot.json", ledger.snapshot())
        lock.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--prepare-only", action="store_true")
    args = parser.parse_args()
    print(
        json.dumps(
            finish(args.batch, args.manifest, workers=args.workers, prepare_only=args.prepare_only),
            indent=2,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
