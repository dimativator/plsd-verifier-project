"""Repeated mini-SWE-agent calibration with isolated Python execution."""

import argparse
from decimal import Decimal
import hashlib
import itertools
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

from experiments.api_backend import (
    APIError,
    BudgetExceeded,
    MiniAPIModel,
    OpenAIResponsesBackend,
    SpendLedger,
)
from experiments.dispatch import batch_admission, bounded_dispatch, controller_guard, stop_requested
from experiments.model_catalog import CALIBRATION_PRICES
from experiments.runtime import BASE_IMAGE, VERIFIER_IMAGE, evaluate_python, run_isolated
from experiments.submission_protocol import (
    SUBMISSION_MARKER,
    is_submission_action,
    non_submission_notice,
)

PROJECT = Path(__file__).resolve().parents[1]
MARKER = "echo " + SUBMISSION_MARKER
SYSTEM = (
    "You are a coding agent running under mini-SWE-agent. Propose exactly ONE shell action "
    "in a fenced mswea_bash_command code block, then STOP and wait for its actual observation. "
    "The dispatcher executes only the FIRST complete command block across your response; "
    "everything after that block is discarded. This applies to commentary and final-answer "
    "messages alike. Never assume a file was written or a check ran until its actual output "
    "has been returned on the next turn. Do not narrate or simulate future tool results. "
    "Work iteratively: implement, run useful checks, inspect observations, and revise. "
    "The problem is already included below; inspect files only if useful. "
    "To submit, use a SEPARATE action containing only: "
    + MARKER
    + ". Do not combine submission with writing code or running checks."
)
COMMON = (
    "Implement the complete Python 3.13 program in main.py, reading stdin and writing stdout. "
    "The final program must use only the Python standard library. Only main.py is collected. "
    "Put helpers in that file and guard stdin/stdout execution "
    'with if __name__ == "__main__": so helpers can be imported for checks. '
    "Read prompt.txt. Commands: compile checks Python syntax; run_tests runs public tests. "
    "You may use python/python3 and create additional tests. Produce the required answer for "
    "all legal inputs. Hidden tests are unavailable during solving. "
)
VERIFIER_GUIDANCE = (
    "\n\n" + (PROJECT / "experiments/CROSSHAIR_GUIDE.txt").read_text(encoding="utf-8") + "\n\n"
)
VERIFIER_WORKFLOW = (
    "\n\nVerification workflow, whenever undertaken:\n"
    "1. PLAN: identify one or two important correctness risks. Before the command block, "
    "briefly state the actual target, legal input scope, independently justified behavioral "
    "property and plausible defect it could reveal. You choose all helpers and checks.\n"
    "2. CHECK: run verify on actual answer-producing code, directly or through an importing "
    "sidecar under /work. Do not assume unchecked callee contracts. A range/type/safety "
    "assertion or a new built-in wrapper compared with the same expression is not a "
    "behavioral check of the algorithm. Agent-written independent tiny-case oracles and "
    "behavioral/metamorphic properties are allowed. Label bounded legal slices honestly; "
    "they do not change the required full-domain solution.\n"
    "3. INTERPRET: after EACH returned verifier observation, explain its actual status, "
    "scope and next action before issuing the next command. Empty checks, errors, "
    "inconclusive results and confirmation have different meanings.\n"
    "4. RESPOND: validate every candidate counterexample against the legal domain and "
    "replay the exact case against actual code in ordinary Python. Decide whether the "
    "implementation, property or domain assumption is wrong. Repair the justified cause, "
    "preserve a legal failing case as a regression check, and rerun verification and "
    "relevant concrete tests. An attempted edit is not a repair until you observe its "
    "effect and the rerun result. Do not exclude a valid case to obtain confirmation. "
    "For empty or unsupported checks, repair the setup or try a tractable actual "
    "component/property where feasible. Do not repeat an unchanged uninformative call.\n"
    "5. REVIEW COVERAGE: after a result, identify important behavior still unchecked. "
    "If the check only repeats a public sample, concerns an incidental helper, or leaves "
    "a specific important tractable risk, add or extend a complementary behavioral "
    "check where feasible. A meaningful bounded exhaustive check is not inadequate "
    "merely because it is small. After any material implementation change, rerun "
    "affected checks rather than relying on stale verification.\n"
    "6. CLOSE: state what behavior was checked, what feedback was addressed and which "
    "limitations remain. A completed workflow has a meaningful core-behavior check, "
    "addressed diagnostics and rerun affected checks; alternatively document a genuine "
    "tool/resource limit and the remaining uncertainty. Finding a bug, proving the "
    "whole program or reaching a fixed number of verifier calls is not required. "
    "Continue ordinary testing as useful. Only main.py is submitted and task success "
    "is determined by its outputs, not by verifier confirmation.\n"
    "The complete technical guide follows; the same text is available at "
    "/opt/plinse/CROSSHAIR_GUIDE.txt. "
)
WITH_VERIFIER = (
    (
        "You have OPTIONAL CrossHair access through verify main.py or verify check_contract.py. "
        "Decide whether and when to enter the verification workflow below. If you choose "
        "to use it, apply the shared checking and feedback protocol honestly. You may "
        "complete this task without invoking the verifier. "
    )
    + VERIFIER_WORKFLOW
    + VERIFIER_GUIDANCE
)
GUIDED_VERIFIER = (
    (
        "This is the INSTRUCTED verifier condition. After implementing an initial solution, "
        "enter and carry through the verification workflow below. One invocation is not "
        "by itself completion: use returned evidence to repair, recheck or refine coverage "
        "when a specific feasible next step can reduce an important risk. Do not stop "
        "merely because verify was called or returned zero. Follow the workflow stopping "
        "criteria within the existing task resource limits. "
    )
    + VERIFIER_WORKFLOW
    + VERIFIER_GUIDANCE
)


def write_json(path: Path, data: object):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def load_key() -> str:
    # Explicit task-local file takes precedence over unrelated process settings.
    path = PROJECT.parent / ".env"
    if path.exists():
        for line in path.read_text(encoding="utf-8-sig").splitlines():
            if line.strip().startswith("OPENAI_API_KEY="):
                value = line.split("=", 1)[1].strip().strip('"').strip("'")
                if value:
                    return value
    key = os.environ.get("OPENAI_API_KEY", "")
    if not key:
        raise ValueError("No OPENAI_API_KEY configured; never place it in a run manifest")
    return key


def source_hash(path: Path) -> str | None:
    return (
        hashlib.sha256(path.read_bytes()).hexdigest()
        if path.is_file() and not path.is_symlink()
        else None
    )


def condition_order(conditions: list[str], block_index: int) -> tuple[str, ...]:
    orders = list(itertools.permutations(conditions))
    return orders[block_index % len(orders)]


def task_condition_order(conditions: list[str], task_id: str, repetition: int) -> tuple[str, ...]:
    """Cycle every task through all arm orders, independently of worker shards."""
    if (
        not task_id
        or isinstance(repetition, bool)
        or not isinstance(repetition, int)
        or repetition < 1
    ):
        raise ValueError("A task ID and positive repetition are required")
    phase = int.from_bytes(hashlib.sha256(("20261123:" + task_id).encode()).digest()[:8], "big")
    return condition_order(conditions, phase + repetition - 1)


def validate_frozen_tasks(tasks: list[dict]):
    from experiments.validate_tasks import canonical_sha256

    for task in tasks:
        directory = PROJECT / "benchmark-data/codecontests/tasks" / task["id"]
        for relative, expected in task["data_sha256_lf"].items():
            if canonical_sha256(directory / relative) != expected:
                raise ValueError(f"Frozen task data changed: {task['id']}/{relative}")
        suite = json.loads((directory / "evaluator/private-tests.json").read_text(encoding="utf-8"))
        if not suite["input"] or len(suite["input"]) != len(suite["output"]):
            raise ValueError(f"Invalid frozen private suite: {task['id']}")


def _prepare_workspace(task: dict, directory: Path) -> tuple[Path, Path, str]:
    workspace = directory / "workspace"
    workspace.mkdir(parents=True)
    # Docker's UID 65534 needs write access to this new workspace on Linux hosts.
    workspace.chmod(0o777)
    original = PROJECT / "benchmark-data/codecontests/tasks" / task["id"]
    problem = (original / "public/prompt.txt").read_text(encoding="utf-8")
    problem = problem.replace("Write a Kotlin program", "Write a Python 3 program").replace(
        "Main.kt", "main.py"
    )
    (workspace / "prompt.txt").write_text(problem, encoding="utf-8")
    (workspace / "main.py").write_text("# Write your Python solution here.\n", encoding="utf-8")
    shutil.copyfile(original / "public/public-tests.json", workspace / "public-tests.json")
    write_json(
        workspace / "task.json",
        {"id": task["id"], "checker": task["checker"], "solution_file": "main.py"},
    )
    for name in ("prompt.txt", "main.py", "public-tests.json", "task.json"):
        (workspace / name).chmod(0o666)
    return workspace, original, problem


def execute(task: dict, spec: dict, config: dict, ledger: SpendLedger, api_key: str) -> dict:
    from minisweagent.agents.default import DefaultAgent
    from minisweagent.environments.local import LocalEnvironment
    from minisweagent.exceptions import Submitted

    directory = (
        Path(config["output"])
        / spec["model"]
        / spec["task_id"]
        / spec["condition"]
        / f"rep-{spec['repetition']:02d}"
    )
    result_path = directory / "result.json"
    if result_path.exists():
        return json.loads(result_path.read_text(encoding="utf-8"))
    if directory.exists():
        raise FileExistsError(f"Inspect incomplete attempt before resuming: {directory}")
    workspace, original, problem = _prepare_workspace(task, directory)
    write_json(
        directory / "spec.json",
        {**spec, "limits": config, "task_data_hashes": task.get("data_sha256_lf")},
    )
    image = VERIFIER_IMAGE if spec["condition"] in ("verifier", "guided_verifier") else BASE_IMAGE
    actions = []
    started = time.monotonic()
    deadline = started + config["solve_limit_seconds"]
    run_id = "/".join(
        [Path(config["output"]).name]
        + [str(spec[k]) for k in ("phase", "model", "task_id", "condition", "repetition")]
    )
    backend = OpenAIResponsesBackend(
        model=spec["model"],
        price=CALIBRATION_PRICES[spec["model"]],
        ledger=ledger,
        log_dir=directory / "model",
        max_output_tokens=config["max_output_tokens"],
        reasoning_effort=config["effort"],
        timeout_seconds=config["solve_limit_seconds"],
        max_retries=1,
        deadline_monotonic=deadline,
        api_key=api_key,
    )

    class Model(MiniAPIModel):
        def query(self, messages, **kwargs):
            remaining = deadline - time.monotonic()
            if remaining <= 2:
                raise BudgetExceeded("Solve-time budget exhausted")
            self.backend.timeout = max(1, remaining - 1)
            return super().query(messages, **kwargs)

    class Environment(LocalEnvironment):
        def get_template_vars(self, **kwargs):
            return {"cwd": "/work", **kwargs}

        def execute(self, action, cwd="", **kwargs):
            if time.monotonic() >= deadline:
                raise BudgetExceeded("Solve-time budget exhausted")
            command = action["command"]
            if is_submission_action(command):
                if not actions:
                    return {
                        "returncode": 1,
                        "output": "Implement the solution before submitting.",
                        "exception_info": "",
                    }
                raise Submitted(
                    {
                        "role": "exit",
                        "content": "",
                        "extra": {"exit_status": "Submitted", "submission": ""},
                    }
                )
            before = source_hash(workspace / "main.py")
            result = run_isolated(
                workspace,
                command,
                image=image,
                timeout=max(1, min(60, deadline - time.monotonic())),
            )
            # Docker daemon/launch failures are external failures, not wrong answers.
            if result["returncode"] in (125, 126, 127) and "docker:" in result["stderr"].lower():
                raise RuntimeError("Container infrastructure failed: " + result["stderr"][:1000])
            after = source_hash(workspace / "main.py")
            row = {
                "command": command,
                "result": result,
                "source_before": before,
                "source_after": after,
            }
            notice = non_submission_notice(command, result["stdout"] + result["stderr"])
            if notice:
                row["submission_notice"] = notice
            actions.append(row)
            with (directory / "actions.jsonl").open("a", encoding="utf-8") as stream:
                stream.write(json.dumps(row, ensure_ascii=False) + "\n")
            if before != after and after:
                revision = directory / "source-revisions" / f"action-{len(actions):03d}.py"
                revision.parent.mkdir(exist_ok=True)
                shutil.copyfile(workspace / "main.py", revision)
            return {
                "returncode": result["returncode"],
                "output": ((notice + "\n" if notice else "") + result["stdout"] + result["stderr"])[
                    :24000
                ],
                "exception_info": "",
            }

    model = Model(backend, run_id)
    agent = DefaultAgent(
        model,
        Environment(cwd=str(workspace)),
        system_template=SYSTEM,
        instance_template="{{task}}",
        step_limit=config["step_limit"],
        cost_limit=0,
        wall_time_limit_seconds=config["solve_limit_seconds"],
        output_path=directory / "trajectory.json",
    )
    failure = None
    status = "unknown"
    try:
        verifier_instructions = {
            "baseline": "",
            "verifier": WITH_VERIFIER,
            "guided_verifier": GUIDED_VERIFIER,
        }[spec["condition"]]
        completed = agent.run(task=COMMON + verifier_instructions + "\n\n" + problem)
        status = completed.get("exit_status", "unknown")
        if status in ("LimitsExceeded", "TimeExceeded"):
            status = "budget_exhausted"
    except BudgetExceeded:
        status = "budget_exhausted"
    except APIError as error:
        if time.monotonic() >= deadline - 2:
            status = "budget_exhausted"
        else:
            failure = {"type": type(error).__name__, "message": str(error)}
            status = "infrastructure_error"
    except Exception as error:
        failure = {"type": type(error).__name__, "message": str(error)}
        status = "infrastructure_error"
    solve_seconds = time.monotonic() - started
    submission = directory / "main.py"
    if source_hash(workspace / "main.py"):
        shutil.copyfile(workspace / "main.py", submission)
    evaluation_started = time.monotonic()
    try:
        tests = json.loads((original / "evaluator/private-tests.json").read_text(encoding="utf-8"))
        hidden = evaluate_python(
            submission, tests, directory / "evaluation-workspace", task["checker"]
        )
        if hidden.get("infrastructure_error"):
            failure = failure or hidden["infrastructure_error"]
    except Exception as error:
        hidden = {"passed": False, "stage": "evaluator_infrastructure"}
        failure = {"type": type(error).__name__, "message": str(error)}
    evaluation_seconds = time.monotonic() - evaluation_started
    write_json(directory / "hidden-evaluation.json", hidden)
    snapshot = ledger.snapshot()
    costs = [r for r in snapshot["reservations"].values() if r["run_id"] == run_id]
    cost = sum((Decimal(r.get("charged", r["reserved"])) for r in costs), Decimal(0))
    completions = [
        json.loads(p.read_text(encoding="utf-8"))
        for p in (directory / "model").glob("call-*/completion.json")
    ]
    usage = {
        key: sum(c["usage"].get(key, 0) for c in completions)
        for key in ("input_tokens", "output_tokens", "total_tokens")
    }
    result = {
        **spec,
        "exit_status": status,
        "valid_run": failure is None,
        "infrastructure_error": failure,
        "hidden_passed": hidden["passed"],
        "evaluation_infrastructure_error": hidden.get("infrastructure_error"),
        "model_cost_usd": float(cost),
        "cost_is_upper_bound": any(r["status"] != "settled" for r in costs),
        "solve_seconds": solve_seconds,
        "evaluation_seconds": evaluation_seconds,
        "model_calls": model.call_count,
        "usage": usage,
        "shell_actions": len(actions),
        "tool_events": [
            {"event": "verify_invocation_observed"}
            for a in actions
            if "PLINSE_VERIFY_START " in a["result"]["stdout"]
        ],
        "submission_sha256": source_hash(submission),
        "hidden_test_count": hidden.get("test_count"),
        "model_settings": {
            "effort": config["effort"],
            "max_output_tokens": config["max_output_tokens"],
        },
    }
    write_json(result_path, result)
    return result


def _pending_runs(output: Path, specs: list[dict], config: dict) -> list[dict]:
    pending = []
    model_settings = {key: config[key] for key in ("effort", "max_output_tokens")}
    for spec in specs:
        directory = (
            output
            / spec["model"]
            / spec["task_id"]
            / spec["condition"]
            / f"rep-{spec['repetition']:02d}"
        )
        result_path = directory / "result.json"
        if result_path.exists():
            row = json.loads(result_path.read_text(encoding="utf-8"))
            if (
                any(row.get(key) != value for key, value in spec.items())
                or row.get("model_settings") != model_settings
            ):
                raise ValueError(f"Existing result differs from the frozen batch: {result_path}")
        elif directory.exists():
            raise ValueError(f"Incomplete original attempt; inspect before resuming: {directory}")
        else:
            pending.append(spec)
    return pending


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("runs/calibration-20261123/validated-task-manifest.json"),
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--spend-root", type=Path, default=Path("runs/calibration-20261123/spend"))
    parser.add_argument(
        "--models", nargs="+", default=["gpt-6-luna", "gpt-5.6-luna", "gpt-6.1-sol"]
    )
    parser.add_argument(
        "--conditions",
        nargs="+",
        choices=["baseline", "verifier", "guided_verifier"],
        default=["baseline"],
    )
    parser.add_argument("--repetitions", type=int, default=2)
    parser.add_argument("--task-count", type=int)
    parser.add_argument("--tasks", nargs="+")
    parser.add_argument(
        "--phase", choices=["model_screen", "calibration", "main"], default="model_screen"
    )
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--max-output-tokens", type=int, default=16384)
    parser.add_argument("--step-limit", type=int, default=100)
    parser.add_argument("--solve-limit-seconds", type=int, default=600)
    parser.add_argument("--per-run-cap-usd", default="0.28")
    parser.add_argument("--total-cap-usd", default="15.00")
    parser.add_argument("--effort", default="medium")
    parser.add_argument(
        "--prepare-only",
        action="store_true",
        help="Freeze and show the planned batch without loading credentials or calling a model",
    )
    args = parser.parse_args()
    if args.workers < 1:
        raise ValueError("workers must be positive")
    os.environ["MSWEA_SILENT_STARTUP"] = "1"
    os.environ["MSWEA_GLOBAL_CONFIG_DIR"] = str(PROJECT / "pilot/.runtime/mini-api-config")
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    tasks = manifest["tasks"] if args.phase == "main" else manifest["calibration_tasks"]
    if args.tasks:
        tasks = [t for t in tasks if t["id"] in args.tasks]
    else:
        # Alternate bands so a short screen contains both difficulty strata.
        groups = [[t for t in tasks if t["rating_band"] == band] for band in ["2000-2399", "2400+"]]
        count = (
            args.task_count
            if args.task_count is not None
            else (len(tasks) if args.phase == "main" else 6)
        )
        tasks = [
            t
            for pair in __import__("itertools").zip_longest(*groups)
            for t in pair
            if t is not None
        ][:count]
    if not tasks or args.repetitions < 1:
        raise ValueError("Tasks and repetitions must be nonempty")
    validate_frozen_tasks(tasks)
    for model in args.models:
        if model not in CALIBRATION_PRICES:
            raise ValueError("Model has no frozen official price")
    specs = []
    for repetition in range(1, args.repetitions + 1):
        for task in tasks:
            for model in args.models:
                for condition in task_condition_order(args.conditions, task["id"], repetition):
                    specs.append(
                        {
                            "phase": args.phase,
                            "model": model,
                            "task_id": task["id"],
                            "family_id": task.get("family_id", task.get("family", task["id"])),
                            "rating_band": task["rating_band"],
                            "condition": condition,
                            "repetition": repetition,
                        }
                    )
    config = {
        "output": str(args.output.resolve()),
        "max_output_tokens": args.max_output_tokens,
        "step_limit": args.step_limit,
        "solve_limit_seconds": args.solve_limit_seconds,
        "effort": args.effort,
        "per_run_cap_usd": args.per_run_cap_usd,
        "total_cap_usd": args.total_cap_usd,
        "spend_root": str(args.spend_root.resolve()),
        "parallel_workers": args.workers,
        "condition_scheduling": "task-ID seeded starting permutation, advance once per repetition; independent of shard task order",
    }
    config["runtime"] = {
        "python": sys.version,
        "mini_swe_agent": "2.4.6",
        "source_sha256": {
            name: source_hash(Path(__file__).with_name(name))
            for name in [
                "run.py",
                "runtime.py",
                "api_backend.py",
                "model_catalog.py",
                "container_tools.py",
                "analysis.py",
                "three_arm_analysis.py",
                "validate_tasks.py",
                "process_audit.py",
                "submission_protocol.py",
                "dispatch.py",
                "resolve_runs.py",
            ]
        },
        "image_ids": {
            image: subprocess.check_output(
                ["docker", "image", "inspect", "--format", "{{.Id}}", image], text=True
            ).strip()
            for image in [BASE_IMAGE, VERIFIER_IMAGE]
        },
        "system_prompt_sha256": hashlib.sha256(SYSTEM.encode()).hexdigest(),
        "common_prompt_sha256": hashlib.sha256(COMMON.encode()).hexdigest(),
        "verifier_prompt_sha256": hashlib.sha256(WITH_VERIFIER.encode()).hexdigest(),
        "guided_verifier_prompt_sha256": hashlib.sha256(GUIDED_VERIFIER.encode()).hexdigest(),
    }
    args.output.mkdir(parents=True, exist_ok=True)
    expected = {"runs": specs, "config": config, "manifest_sha256": source_hash(args.manifest)}
    if args.phase == "main":
        expected["analysis_plan"] = {
            "unit": "source task family",
            "strata": "rating_band",
            "task_weighting": "equal task weight after averaging independent repetitions",
            "repetition_reporting": {
                "score": "percentage of tasks solved in each complete benchmark repetition",
                "aggregate": "mean repetition score for identical complete task sets",
                "dispersion": "sample standard deviation (percentage points) and variance (percentage-points squared)",
                "variance_ddof": 1,
                "interpretation": "observed aggregate-score variation across repetitions; distinct from family-generalization confidence intervals",
                "incomplete_rounds": "suppress aggregate repetition mean/dispersion until all planned rounds are resolved",
            },
            "contrasts": [["baseline", "verifier"], ["baseline", "guided_verifier"]],
            "contrast_confidence_level": 0.975,
            "descriptive_arm_confidence_level": 0.95,
            "bootstrap_draws": 10000,
            "bootstrap_seed": 20261123,
            "multiplicity": "two Bonferroni co-primary contrasts",
            "resource_exhaustion": "score the last saved implementation",
            "unused_or_unsupported_verifier": "retain assigned condition",
        }
    target = args.output / "expected.json"
    if target.exists() and json.loads(target.read_text(encoding="utf-8")) != expected:
        raise ValueError("Existing batch manifest differs; use a new output directory")
    write_json(target, expected)
    if args.prepare_only:
        print(
            json.dumps(
                {
                    "prepared_runs": len(specs),
                    "families": len({s["family_id"] for s in specs}),
                    "output": str(args.output.resolve()),
                    "model_charge_ceiling_usd": str(Decimal(args.per_run_cap_usd) * len(specs)),
                    "credentials_loaded": False,
                    "model_calls": 0,
                }
            ),
            flush=True,
        )
        return
    with controller_guard(args.spend_root):
        pending = _pending_runs(args.output, specs, config)
        report = {
            "planned_runs": len(specs),
            "preserved_runs": len(specs) - len(pending),
            "pending_runs": len(pending),
            "credentials_loaded": False,
        }
        if stop_requested(args.spend_root) or not pending:
            report["status"] = "user_stopped" if pending else "complete"
            write_json(args.output / "controller-report.json", report)
            print(json.dumps(report), flush=True)
            return
        ledger = SpendLedger(
            args.spend_root,
            total_limit_usd=args.total_cap_usd,
            per_run_limit_usd=args.per_run_cap_usd,
        )
        try:
            admission = batch_admission(
                ledger,
                len(pending),
                total_cap_usd=args.total_cap_usd,
                per_run_cap_usd=args.per_run_cap_usd,
            )
            report["admission"] = admission
            if not admission["admitted"]:
                report["status"] = "budget_stopped_before_dispatch"
                write_json(args.output / "controller-report.json", report)
                print(json.dumps(report), flush=True)
                return
            api_key = load_key()
            report["credentials_loaded"] = True
            by_id = {t["id"]: t for t in tasks}
            for _, row in bounded_dispatch(
                pending,
                lambda spec: execute(by_id[spec["task_id"]], spec, config, ledger, api_key),
                workers=args.workers,
                stopped=lambda: stop_requested(args.spend_root),
            ):
                report["pending_runs"] -= 1
                print(
                    json.dumps(
                        {
                            k: row[k]
                            for k in [
                                "model",
                                "task_id",
                                "condition",
                                "repetition",
                                "hidden_passed",
                                "exit_status",
                                "model_cost_usd",
                                "solve_seconds",
                                "evaluation_seconds",
                            ]
                        }
                    ),
                    flush=True,
                )
            report["status"] = "user_stopped" if report["pending_runs"] else "complete"
            write_json(args.output / "controller-report.json", report)
        finally:
            write_json(args.output / "spend-snapshot.json", ledger.snapshot())


if __name__ == "__main__":
    main()
