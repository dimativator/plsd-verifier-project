"""Controller ownership and conservative admission for paid experiment batches."""

from __future__ import annotations

from collections import defaultdict
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from contextlib import contextmanager
from decimal import Decimal
import os
from pathlib import Path


def controller_root(spend_root: Path | str) -> Path:
    return Path(spend_root).resolve().parent


def stop_requested(spend_root: Path | str) -> bool:
    return (controller_root(spend_root) / "STOP").exists()


@contextmanager
def controller_guard(spend_root: Path | str, *, inherit_current_process: bool = False):
    """Share the existing controller lock and serialize nested dispatchers.

    A resolver called synchronously by the finishing controller may inherit its
    same-process claim. The separate dispatch lock prevents two such nested
    dispatchers from admitting work concurrently. Stale claims are never removed.
    """
    root = controller_root(spend_root)
    root.mkdir(parents=True, exist_ok=True)
    controller = root / "controller.lock"
    dispatch = root / "dispatch.lock"
    owned_controller = owned_dispatch = False
    try:
        try:
            descriptor = os.open(controller, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError as error:
            if not inherit_current_process or controller.read_text(encoding="ascii").strip() != str(
                os.getpid()
            ):
                raise ValueError(
                    f"Another controller owns {controller}; inspect before restarting"
                ) from error
        else:
            owned_controller = True
            with os.fdopen(descriptor, "w", encoding="ascii") as stream:
                stream.write(str(os.getpid()))
        try:
            descriptor = os.open(dispatch, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError as error:
            raise ValueError(
                f"Another dispatcher owns {dispatch}; inspect before restarting"
            ) from error
        owned_dispatch = True
        with os.fdopen(descriptor, "w", encoding="ascii") as stream:
            stream.write(str(os.getpid()))
        yield
    finally:
        if owned_dispatch:
            dispatch.unlink()
        if owned_controller:
            controller.unlink()


def batch_admission(ledger, pending_runs: int, *, total_cap_usd: str, per_run_cap_usd: str) -> dict:
    """Require every pending run's complete lifetime ceiling before dispatch."""
    total, per_run = Decimal(total_cap_usd), Decimal(per_run_cap_usd)
    if (
        not total.is_finite()
        or not per_run.is_finite()
        or total <= 0
        or per_run <= 0
        or type(pending_runs) is not int
        or pending_runs < 0
    ):
        raise ValueError("Admission requires positive finite caps and a nonnegative run count")
    snapshot = ledger.snapshot()
    costs = defaultdict(Decimal)
    for row in snapshot.get("reservations", {}).values():
        amount = Decimal(row["reserved"] if row["status"] == "pending" else row["charged"])
        if not amount.is_finite() or amount < 0:
            raise ValueError("Ledger contains an invalid charge")
        costs[row["run_id"]] += amount
    accounted = sum(costs.values(), Decimal(0))
    required = per_run * pending_runs
    overrun = any(value > per_run for value in costs.values())
    return {
        "admitted": not overrun and accounted + required <= total,
        "pending_runs": pending_runs,
        "accounted_usd": str(accounted),
        "required_remaining_usd": str(required),
        "total_cap_usd": str(total),
        "per_run_bound_violated": overrun,
    }


def bounded_dispatch(items, execute, *, workers: int, stopped):
    """Submit at most ``workers`` admitted jobs; STOP drains those already active."""
    if workers < 1:
        raise ValueError("workers must be positive")
    pending = iter(items)
    exhausted = False
    with ThreadPoolExecutor(max_workers=workers) as pool:
        active = {}
        while active or not exhausted:
            while not exhausted and len(active) < workers and not stopped():
                try:
                    item = next(pending)
                except StopIteration:
                    exhausted = True
                    break
                active[pool.submit(execute, item)] = item
            if not active:
                break
            finished, _ = wait(active, timeout=1, return_when=FIRST_COMPLETED)
            for future in finished:
                item = active.pop(future)
                yield item, future.result()
