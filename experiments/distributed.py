"""Frozen two-worker execution and merge; preparation never loads credentials.

Workers can own source families or complete full-benchmark repetitions.
Run the global specifications verbatim; neither sharding nor retries create new
repetitions. Native Windows controllers and Docker Linux images are supported.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from copy import deepcopy
from decimal import Decimal, InvalidOperation
import hashlib
from importlib import metadata
import json
import os
from pathlib import Path
import platform
import subprocess
import sys

from experiments import run
from experiments.api_backend import SpendLedger
from experiments.resolve_runs import IDENTITY, _key, _read, _result_path, verify_retry_environment

ARMS = {"baseline", "verifier", "guided_verifier"}
LOCAL_SETTINGS = {"output", "spend_root", "total_cap_usd", "parallel_workers"}
DEFAULT_WORKERS = {
    "ours": {"families_by_band": {"2000-2399": 30, "2400+": 30}, "total_cap_usd": "140.00"},
    "friend": {"families_by_band": {"2000-2399": 20, "2400+": 20}, "total_cap_usd": "95.00"},
}
ROUND_WORKERS = {
    "ours": {"repetitions": [1, 2, 3], "total_cap_usd": "84.00"},
    "friend": {"repetitions": [4, 5], "total_cap_usd": "56.00"},
}


def _encoded(value) -> bytes:
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def _digest(value) -> str:
    return hashlib.sha256(_encoded(value)).hexdigest()


def _money(value) -> Decimal:
    try:
        number = Decimal(str(value))
    except (InvalidOperation, ValueError) as error:
        raise ValueError("Invalid frozen spend cap") from error
    if not number.is_finite() or number <= 0:
        raise ValueError("Spend caps must be positive and finite")
    return number


def _immutable(path: Path, value) -> None:
    data = _encoded(value)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() != data:
            raise ValueError(f"Existing frozen file differs: {path}")
        return
    with path.open("xb") as stream:
        stream.write(data)


def image_fingerprint(inspected: dict) -> dict:
    """Image content/runtime identity, independent of Docker store .Id format."""
    config = inspected.get("Config") or {}
    runtime = {
        name: config.get(name) or [] for name in ("Env", "Cmd", "Entrypoint", "Shell", "OnBuild")
    }
    runtime.update(
        {
            name: config.get(name) or {}
            for name in ("Volumes", "ExposedPorts", "Labels", "Healthcheck")
        }
    )
    runtime.update({name: config.get(name) or "" for name in ("User", "WorkingDir", "StopSignal")})
    runtime["ArgsEscaped"] = bool(config.get("ArgsEscaped", False))
    content = {
        "os": inspected["Os"],
        "architecture": inspected["Architecture"],
        "variant": inspected.get("Variant") or "",
        "layers": inspected["RootFS"]["Layers"],
        "config": runtime,
    }
    return {"sha256": _digest(content), "content": content}


def _inspect_image(name: str) -> dict:
    return json.loads(subprocess.check_output(["docker", "image", "inspect", name], text=True))[0]


def _safe_components(spec: dict) -> None:
    for field in ("phase", "model", "task_id", "condition", "family_id"):
        value = spec[field]
        if (
            not isinstance(value, str)
            or not value
            or value in {".", ".."}
            or any(c in value for c in "/\\:")
        ):
            raise ValueError(f"Unsafe run identity component: {field}")


def _global_expected(plan: dict) -> dict:
    return {
        "runs": plan["runs"],
        "config": plan["shared_config"],
        "manifest_sha256": plan["manifest_sha256"],
        "analysis_plan": plan.get("analysis_plan", {}),
        "distributed_plan_sha256": plan["plan_sha256"],
    }


def _load_plan(value: Path | str | dict) -> dict:
    plan = deepcopy(value) if isinstance(value, dict) else _read(Path(value))
    unsigned = {k: v for k, v in plan.items() if k != "plan_sha256"}
    if plan.get("plan_sha256") != _digest(unsigned):
        raise ValueError("Distributed plan fingerprint differs")
    if len({_key(s) for s in plan["runs"]}) != len(plan["runs"]):
        raise ValueError("Duplicate global run identities")
    mode = plan.get("assignment_mode", "families")
    if mode not in {"families", "repetitions"}:
        raise ValueError("Unknown worker assignment mode")
    for spec in plan["runs"]:
        _safe_components(spec)
        owner = spec["worker_id"]
        stratum = (
            spec["rating_band"] if mode == "repetitions" else owner + ":" + spec["rating_band"]
        )
        if (
            owner not in plan["workers"]
            or spec["family_id"] not in plan["workers"][owner]["families"]
            or spec.get("analysis_stratum", spec["rating_band"] if mode == "repetitions" else None)
            != stratum
            or (
                mode == "repetitions"
                and spec["repetition"] not in plan["workers"][owner]["repetitions"]
            )
        ):
            raise ValueError("Global ownership/analysis stratum differs")
    if mode == "repetitions":
        assigned = [rep for profile in plan["workers"].values() for rep in profile["repetitions"]]
        if sorted(assigned) != list(range(1, plan["repetitions"] + 1)):
            raise ValueError("Worker repetitions must exhaust the planned rounds exactly once")
        _money(plan["round_retry_reserve_usd"])
    return plan


def create_plan(
    global_expected: Path | str,
    output: Path | str,
    *,
    seed: int = 20261123,
    workers: dict | None = None,
    repetitions: int = 6,
    _assignment_mode: str = "families",
    _round_retry_reserve_usd: str = "4.00",
) -> dict:
    original = _read(Path(global_expected))
    specs, shared = deepcopy(original["runs"]), deepcopy(original["config"])
    if not specs or len({_key(s) for s in specs}) != len(specs):
        raise ValueError("Global expected file requires unique nonempty run identities")
    family_bands, groups = {}, {}
    for spec in specs:
        _safe_components(spec)
        family, band = spec["family_id"], spec["rating_band"]
        if family in family_bands and family_bands[family] != band:
            raise ValueError("A source family spans rating bands")
        family_bands[family] = band
        key = spec["model"], spec["task_id"]
        groups.setdefault(key, {}).setdefault(spec["condition"], set()).add(spec["repetition"])
    wanted_reps = set(range(1, repetitions + 1))
    if any(set(g) != ARMS or any(r != wanted_reps for r in g.values()) for g in groups.values()):
        raise ValueError("Every model/task must contain all three arms and all full repetitions")
    round_mode = _assignment_mode == "repetitions"
    if _assignment_mode not in {"families", "repetitions"}:
        raise ValueError("Unknown worker assignment mode")
    settings = deepcopy(
        workers if workers is not None else (ROUND_WORKERS if round_mode else DEFAULT_WORKERS)
    )
    if not settings or any(not name or any(c in name for c in "/\\:") for name in settings):
        raise ValueError("Worker IDs must be safe nonempty path components")
    per_run = _money(shared["per_run_cap_usd"])
    total = sum((_money(w["total_cap_usd"]) for w in settings.values()), Decimal(0))
    if total > _money(shared["total_cap_usd"]):
        raise ValueError("Worker allocations exceed the frozen global main cap")
    for worker in settings.values():
        worker["families"] = []
    assignment = {}
    if round_mode:
        assigned = [rep for profile in settings.values() for rep in profile["repetitions"]]
        if any(type(rep) is not int for rep in assigned) or sorted(assigned) != sorted(wanted_reps):
            raise ValueError("Worker repetitions must exhaust the planned rounds exactly once")
        for owner, profile in settings.items():
            profile["families"] = sorted(family_bands)
            assignment.update({rep: owner for rep in profile["repetitions"]})
        _money(_round_retry_reserve_usd)
    else:
        for band in sorted(set(family_bands.values())):
            families = sorted(
                (f for f, b in family_bands.items() if b == band),
                key=lambda f: hashlib.sha256(f"{seed}:{band}:{f}".encode()).hexdigest(),
            )
            counts = [settings[w]["families_by_band"].get(band, 0) for w in settings]
            if any(not isinstance(n, int) or n < 0 for n in counts) or sum(counts) != len(families):
                raise ValueError(f"Worker family allocation does not exhaust band {band}")
            offset = 0
            for owner, count in zip(settings, counts):
                chosen = families[offset : offset + count]
                settings[owner]["families"].extend(chosen)
                assignment.update({f: owner for f in chosen})
                offset += count
    for spec in specs:
        owner = assignment[spec["repetition"] if round_mode else spec["family_id"]]
        if spec.get("worker_id", owner) != owner:
            raise ValueError("Existing global worker assignment differs")
        stratum = spec["rating_band"] if round_mode else owner + ":" + spec["rating_band"]
        if spec.get("analysis_stratum", stratum) != stratum:
            raise ValueError("Existing global analysis stratum differs")
        spec["worker_id"] = owner
        if round_mode:
            spec.pop("analysis_stratum", None)
        else:
            spec["analysis_stratum"] = stratum
    for owner, worker in settings.items():
        worker["normal_run_ceiling_usd"] = str(
            per_run * sum(s["worker_id"] == owner for s in specs)
        )
        if not round_mode and Decimal(worker["normal_run_ceiling_usd"]) > _money(
            worker["total_cap_usd"]
        ):
            raise ValueError(f"Normal planned runs exceed worker cap: {owner}")
    for field in ("output", "spend_root"):
        shared.pop(field, None)
    images = {}
    for name, expected_id in shared["runtime"]["image_ids"].items():
        inspected = _inspect_image(name)
        if inspected["Id"] != expected_id:
            raise ValueError(f"Origin image changed before plan freeze: {name}")
        fp = image_fingerprint(inspected)
        if fp["content"]["os"] != "linux" or fp["content"]["architecture"] != "amd64":
            raise ValueError("This protocol requires pinned linux/amd64 container images")
        images[name] = fp
    shared["runtime"]["portable_image_fingerprints"] = {k: v["sha256"] for k, v in images.items()}
    analysis = deepcopy(original.get("analysis_plan", {}))
    analysis["strata"] = "rating_band" if round_mode else "analysis_stratum (worker_id:rating_band)"
    plan = {
        "schema_version": 1,
        "seed": seed,
        "repetitions": repetitions,
        "origin_expected_sha256": run.source_hash(Path(global_expected)),
        "launcher_sha256": run.source_hash(Path(__file__)),
        "manifest_sha256": original["manifest_sha256"],
        "shared_config": shared,
        "portable_images": images,
        "workers": settings,
        "runs": specs,
        "analysis_plan": analysis,
        "policy": "Whole source families; preserve global run order/IDs; local keys and ledgers; no automatic retries.",
    }
    if round_mode:
        plan.update(
            assignment_mode="repetitions",
            round_retry_reserve_usd=str(_round_retry_reserve_usd),
            policy="Complete repetitions on execution workers; shared API budget split into local caps; "
            "admit each round only with its full pending per-run ceilings plus retry reserve; "
            "unlaunched runs remain missing; preserve planned denominator; no automatic retries.",
        )
    plan["plan_sha256"] = _digest(plan)
    output = Path(output)
    _immutable(output / "plan.json", plan)
    _immutable(output / "global-expected.json", _global_expected(plan))
    return plan


def create_round_plan(
    global_expected: Path | str,
    output: Path | str,
    *,
    seed: int = 20261123,
    workers: dict | None = None,
    repetitions: int = 5,
    retry_reserve_usd: str = "4.00",
) -> dict:
    """Assign complete repetitions, retaining each family's observations across workers."""
    return create_plan(
        global_expected,
        output,
        seed=seed,
        workers=workers,
        repetitions=repetitions,
        _assignment_mode="repetitions",
        _round_retry_reserve_usd=retry_reserve_usd,
    )


def _tasks(plan: dict, manifest: Path, specs: list[dict]) -> list[dict]:
    if run.source_hash(manifest) != plan["manifest_sha256"]:
        raise ValueError("Frozen validated-task manifest changed")
    document = _read(manifest)
    tasks = {
        t["id"]: t
        for field in ("tasks", "calibration_tasks", "reserve_tasks")
        for t in document.get(field, [])
    }
    ids = list(dict.fromkeys(s["task_id"] for s in specs))
    if any(task not in tasks for task in ids):
        raise ValueError("Assigned task is absent from the validated manifest")
    return [tasks[task] for task in ids]


def validate_environment(plan: dict, tasks: list[dict]) -> dict:
    if plan["launcher_sha256"] != run.source_hash(Path(__file__)):
        raise ValueError("Frozen distributed launcher source changed")
    if (
        plan["shared_config"]["runtime"].get("mini_swe_agent") != "2.4.6"
        or metadata.version("mini-swe-agent") != "2.4.6"
    ):
        raise ValueError("Worker requires actual mini-SWE-agent 2.4.6")
    config = deepcopy(plan["shared_config"])
    local_ids = {}
    for name, expected in plan["portable_images"].items():
        inspected = _inspect_image(name)
        if image_fingerprint(inspected) != expected:
            raise ValueError(f"Portable frozen image content changed: {name}")
        local_ids[name] = inspected["Id"]
    config["runtime"]["image_ids"] = local_ids
    verify_retry_environment(config, tasks)
    return local_ids


def _local_config(
    plan: dict, owner: str, output: Path, parallel_workers: int, image_ids: dict
) -> dict:
    config = deepcopy(plan["shared_config"])
    config.update(
        output=str(output),
        spend_root=str(output / "spend"),
        total_cap_usd=str(plan["workers"][owner]["total_cap_usd"]),
        parallel_workers=parallel_workers,
    )
    config["runtime"]["image_ids"] = image_ids
    return config


def _check_config(config: dict, plan: dict, owner: str) -> None:
    if _money(config["total_cap_usd"]) != _money(plan["workers"][owner]["total_cap_usd"]):
        raise ValueError("Worker spend cap differs from allocation")
    if set(config["runtime"]["image_ids"]) != set(plan["portable_images"]):
        raise ValueError("Worker-local image identities are missing")
    normalized = {k: deepcopy(v) for k, v in config.items() if k not in LOCAL_SETTINGS}
    normalized["runtime"]["image_ids"] = plan["shared_config"]["runtime"]["image_ids"]
    expected = {k: v for k, v in plan["shared_config"].items() if k not in LOCAL_SETTINGS}
    if normalized != expected:
        raise ValueError("Worker source/image/prompt/resource settings differ from shared protocol")


def _check_row(row: dict, spec: dict, config: dict) -> None:
    if any(row.get(k) != v for k, v in spec.items()):
        raise ValueError("Result identity, owner or stratum differs from global plan")
    if row.get("model_settings") != {k: config[k] for k in ("effort", "max_output_tokens")}:
        raise ValueError("Result model settings differ from frozen protocol")


def worker(
    plan: Path | str | dict,
    worker_id: str,
    manifest: Path | str,
    output: Path | str,
    *,
    prepare_only: bool = True,
    workers: int = 8,
) -> dict:
    plan = _load_plan(plan)
    if worker_id not in plan["workers"] or workers < 1:
        raise ValueError("Unknown worker or invalid concurrency")
    specs = [s for s in plan["runs"] if s["worker_id"] == worker_id]
    output, manifest = Path(output).resolve(), Path(manifest).resolve()
    tasks = _tasks(plan, manifest, specs)
    local_ids = validate_environment(plan, tasks)
    config = _local_config(plan, worker_id, output, workers, local_ids)
    expected = {
        "runs": specs,
        "config": config,
        "manifest_sha256": plan["manifest_sha256"],
        "distributed": {"worker_id": worker_id, "plan_sha256": plan["plan_sha256"]},
        "host_runtime": {
            "python": sys.version,
            "platform": platform.platform(),
            "machine": platform.machine(),
            "logical_cpus": os.cpu_count(),
        },
    }
    _immutable(output / "expected.json", expected)
    pending = []
    for spec in specs:
        path = _result_path(output, spec)
        if path.exists():
            _check_row(_read(path), spec, config)
        elif path.parent.exists():
            raise ValueError(
                f"Incomplete original attempt; preserve/resolve before new calls: {path.parent}"
            )
        else:
            pending.append(spec)
    report = {
        "worker_id": worker_id,
        "planned_runs": len(specs),
        "pending_runs": len(pending),
        "completed_runs": len(specs) - len(pending),
        "prepare_only": prepare_only,
        "credentials_loaded": False,
        "output": str(output),
        "total_cap_usd": config["total_cap_usd"],
        "per_run_cap_usd": config["per_run_cap_usd"],
    }
    if prepare_only or not pending:
        return report
    lock = output / "controller.lock"
    try:
        descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as error:
        raise ValueError(
            "Worker controller already claimed; inspect it before restarting"
        ) from error
    os.write(descriptor, str(os.getpid()).encode())
    os.close(descriptor)
    ledger = None
    try:
        ledger = SpendLedger(
            output / "spend",
            total_limit_usd=config["total_cap_usd"],
            per_run_limit_usd=config["per_run_cap_usd"],
        )
        os.environ["MSWEA_SILENT_STARTUP"] = "1"
        os.environ["MSWEA_GLOBAL_CONFIG_DIR"] = str(run.PROJECT / "pilot/.runtime/mini-api-config")
        key = None
        by_id = {t["id"]: t for t in tasks}
        round_mode = plan.get("assignment_mode") == "repetitions"
        if round_mode:
            repetitions = sorted(plan["workers"][worker_id]["repetitions"])
            batches = (
                [spec for spec in pending if spec["repetition"] == repetition]
                for repetition in repetitions
            )
        else:
            batches = [pending]
        report["round_admissions"] = []
        for batch in batches:
            if not batch:
                continue
            if round_mode:
                accounted = Decimal(ledger.snapshot()["accounted_usd"])
                remaining = _money(config["total_cap_usd"]) - accounted
                required = _money(config["per_run_cap_usd"]) * len(batch) + _money(
                    plan["round_retry_reserve_usd"]
                )
                admission = {
                    "repetition": batch[0]["repetition"],
                    "pending_runs": len(batch),
                    "remaining_usd": str(remaining),
                    "required_usd": str(required),
                    "admitted": remaining >= required,
                }
                report["round_admissions"].append(admission)
                if remaining < required:
                    report.update(
                        status="budget_stop_before_round",
                        budget_stop=admission,
                        not_launched_repetitions=sorted(
                            {
                                s["repetition"]
                                for s in pending
                                if s["repetition"] >= batch[0]["repetition"]
                            }
                        ),
                    )
                    # Do not create run directories or score unlaunched jobs as agent failures.
                    break
            if key is None:
                key = run.load_key()
                report["credentials_loaded"] = True
            with ThreadPoolExecutor(max_workers=workers) as pool:
                futures = [
                    pool.submit(run.execute, by_id[s["task_id"]], s, config, ledger, key)
                    for s in batch
                ]
                for future in as_completed(futures):
                    row = future.result()
                    report["completed_runs"] += 1
                    report["pending_runs"] -= 1
                    print(
                        json.dumps(
                            {
                                k: row[k]
                                for k in (
                                    "worker_id",
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
        report.setdefault("status", "complete")
        run.write_json(output / "worker-report.json", report)
    finally:
        if ledger is not None:
            run.write_json(output / "spend-snapshot.json", ledger.snapshot())
        lock.unlink()
    return report


def _portable_basename(path: str) -> str:
    return path.replace("\\", "/").rstrip("/").rsplit("/", 1)[-1]


def _selected_directory(root: Path, expected: dict, spec: dict, row: dict) -> Path:
    selected = (row.get("resolution") or {}).get("selected_attempt", "original")
    if selected == "original":
        return _result_path(root, spec).parent
    suffix = {"infra-retry-1": "-infra-retry-1", "recovery-1": "-recovery-1"}.get(selected)
    if suffix is None:
        raise ValueError("Unrecognized selected external attempt")
    names = {root.name + suffix, _portable_basename(expected["config"]["output"]) + suffix}
    candidates = [_result_path(root.parent / name, spec).parent for name in names]
    present = [p for p in candidates if (p / "result.json").exists()]
    if len(present) != 1:
        raise ValueError(
            "Retain exactly one selected external-attempt artifact directory alongside worker root"
        )
    return present[0]


def _ledger_cost(root: Path, expected: dict, specs: list[dict]) -> dict:
    path = root / "spend/ledger.json"
    if not path.exists():
        path = root / "spend-snapshot.json"
    if not path.exists():
        return {"available": False, "accounted_usd": None, "reservation_ids": []}
    state = _read(path)
    limits = state.get("limits") or {}
    if any(
        _money(limits.get(k, 0)) != _money(expected["config"][v])
        for k, v in [("total", "total_cap_usd"), ("per_run", "per_run_cap_usd")]
    ):
        raise ValueError("Worker ledger caps differ from frozen allocation")
    suffixes = {"/".join(str(s[k]) for k in IDENTITY) for s in specs}
    origin = _portable_basename(expected["config"]["output"])
    allowed = {origin, origin + "-infra-retry-1", origin + "-recovery-1"}
    external = {}
    total = Decimal(0)
    for reservation in state["reservations"].values():
        parts = str(reservation["run_id"]).split("/", 1)
        if len(parts) != 2 or parts[0] not in allowed or parts[1] not in suffixes:
            raise ValueError("Ledger contains a run owned by another shard/protocol")
        if parts[0] != origin:
            external.setdefault(parts[1], set()).add(parts[0])
            if len(external[parts[1]]) > 1:
                raise ValueError("More than one external replacement namespace for one identity")
        amount = Decimal(
            str(
                reservation["reserved"]
                if reservation["status"] == "pending"
                else reservation["charged"]
            )
        )
        if not amount.is_finite() or amount < 0:
            raise ValueError("Malformed worker ledger amount")
        total += amount
    return {
        "available": True,
        "accounted_usd": str(total),
        "reservation_ids": sorted(state["reservations"]),
        "source": str(path),
        "over_cap": total > _money(expected["config"]["total_cap_usd"]),
        "retains_uncertain_charges": any(
            x["status"] != "settled" for x in state["reservations"].values()
        ),
    }


def merge(plan: Path | str | dict, worker_roots: dict[str, Path | str], output: Path | str) -> dict:
    plan = _load_plan(plan)
    if set(worker_roots) - set(plan["workers"]):
        raise ValueError("Unknown supplied worker")
    planned = {_key(s): s for s in plan["runs"]}
    selected, costs, blockers, reservation_ids = {}, {}, [], set()
    for owner, supplied in worker_roots.items():
        supplied = Path(supplied).resolve()
        root = supplied if supplied.is_dir() else supplied.parent
        expected = _read(root / "expected.json")
        assigned = [s for s in plan["runs"] if s["worker_id"] == owner]
        if (
            expected.get("distributed") != {"worker_id": owner, "plan_sha256": plan["plan_sha256"]}
            or expected.get("manifest_sha256") != plan["manifest_sha256"]
            or expected["runs"] != assigned
        ):
            raise ValueError("Worker expected file/ownership differs from global plan")
        _check_config(expected["config"], plan, owner)
        if supplied.is_file():
            rows = _read(supplied)
            if not isinstance(rows, list):
                raise ValueError("Selected-results input must be an explicit JSON list")
        else:
            rows = [_read(p) for p in sorted(root.glob("*/*/*/rep-*/result.json"))]
        for row in rows:
            key = _key(row)
            if key in selected:
                raise ValueError("Duplicate selected global run identity")
            spec = planned.get(key)
            if spec is None or spec["worker_id"] != owner:
                raise ValueError("Unknown run or wrong worker ownership")
            _check_row(row, spec, expected["config"])
            directory = _selected_directory(root, expected, spec, row)
            raw = _read(directory / "result.json")
            if {k: v for k, v in row.items() if k != "resolution"} != raw:
                raise ValueError("Selected result differs from preserved raw attempt")
            recorded = _read(directory / "spec.json")
            if any(recorded.get(k) != v for k, v in spec.items()):
                raise ValueError("Attempt specification differs from global plan")
            _check_config(recorded["limits"], plan, owner)
            if run.source_hash(directory / "main.py") != row.get("submission_sha256"):
                raise ValueError("Submission hash differs from selected artifact")
            selected[key] = row
        costs[owner] = _ledger_cost(root, expected, assigned)
        ids = set(costs[owner]["reservation_ids"])
        if reservation_ids & ids:
            raise ValueError("Duplicate ledger reservation across workers")
        reservation_ids |= ids
        if not costs[owner]["available"] or costs[owner].get("over_cap"):
            blockers.append({"code": "worker_cost_missing_or_over_cap", "worker_id": owner})
    merged = []
    for spec in plan["runs"]:
        row = selected.get(_key(spec))
        if row is None:
            row = {
                **spec,
                "valid_run": False,
                "hidden_passed": False,
                "exit_status": "missing_planned_run",
                "model_cost_usd": 0,
                "cost_is_upper_bound": True,
                "infrastructure_error": {
                    "type": "MissingPlannedRun",
                    "message": "No selected worker result",
                },
            }
        if row.get("valid_run") is not True or row.get("infrastructure_error"):
            blockers.append({"code": "unresolved_planned_run", "identity": list(_key(spec))})
        merged.append(row)
    complete_cost = set(costs) == set(plan["workers"]) and all(
        c["available"] for c in costs.values()
    )
    total = sum((Decimal(c["accounted_usd"]) for c in costs.values() if c["available"]), Decimal(0))
    report = {
        "complete": not blockers,
        "planned_runs": len(plan["runs"]),
        "selected_runs": len(selected),
        "missing_runs": len(plan["runs"]) - len(selected),
        "blockers": blockers,
        "worker_costs": costs,
        "all_attempt_cost_usd": str(total) if complete_cost else None,
        "known_all_attempt_cost_usd": str(total),
        "cost_accounting_complete": complete_cost,
        "selected_result_cost_usd": sum(
            float(r.get("model_cost_usd", 0)) for r in selected.values()
        ),
        "cost_note": "All-attempt ledger totals include original/retry/pending charges. Selected result costs are separate; an external attempt is not a new repetition.",
    }
    output = Path(output)
    run.write_json(output / "merged-results.json", merged)
    _immutable(output / "global-expected.json", _global_expected(plan))
    run.write_json(output / "merge-report.json", report)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("plan")
    p.add_argument("--expected", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p = sub.add_parser("round-plan", help="Five repetitions: ours 1-3/$84, friend 4-5/$56")
    p.add_argument("--expected", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p = sub.add_parser("worker")
    p.add_argument("--plan", type=Path, required=True)
    p.add_argument("--worker", required=True)
    p.add_argument("--manifest", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--workers", type=int, default=8)
    p.add_argument(
        "--execute", action="store_true", help="Default is prepare-only with no credentials"
    )
    p = sub.add_parser("merge")
    p.add_argument("--plan", type=Path, required=True)
    p.add_argument("--worker", action="append", default=[], metavar="ID=ROOT_OR_RESOLVED_JSON")
    p.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.command in {"plan", "round-plan"}:
        p = (create_round_plan if args.command == "round-plan" else create_plan)(
            args.expected, args.output
        )
        report = {
            "planned_runs": len(p["runs"]),
            "plan_sha256": p["plan_sha256"],
            "workers": p["workers"],
        }
    elif args.command == "worker":
        report = worker(
            args.plan,
            args.worker,
            args.manifest,
            args.output,
            prepare_only=not args.execute,
            workers=args.workers,
        )
    else:
        supplied = {}
        for pair in args.worker:
            owner, separator, path = pair.partition("=")
            if not separator or owner in supplied:
                parser.error("Supply each worker exactly once as ID=ROOT_OR_RESOLVED_JSON")
            supplied[owner] = path
        report = merge(args.plan, supplied, args.output)
    print(json.dumps(report, indent=2), flush=True)
    if args.command == "merge" and not report["complete"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
