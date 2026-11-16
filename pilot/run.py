"""Run a frozen task selection through mini-SWE-agent in both conditions."""

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
import hashlib
import json
import logging
import os
from pathlib import Path
import re
import shlex
import shutil
import sys
import time

from pilot.codex_model import CodexConfig, CodexModel, prepare_codex_home
from pilot.evaluate import evaluate
from pilot.sandbox import environment, profile, run

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class RunConfig:
    project: Path
    output: Path
    workers: int
    model: str = "gpt-5.6-luna"
    effort: str = "medium"


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    temporary.replace(path)


def prepare_commands(project: Path) -> None:
    common = project / "pilot/toolchain/common"
    verifier = project / "pilot/toolchain/verifier"
    shutil.copyfile(project / "pilot/kotlin_tools.py", common / "kotlin_tools.py")
    shutil.copyfile(project / "pilot/verifier-quickstart.txt", verifier / "QUICKSTART.txt")
    python = str(project / ".venv/bin/python")
    obsolete = common / "bin/test"
    if obsolete.exists():
        obsolete.unlink()
    for action in ["compile", "run_tests", "verify"]:
        directory = verifier if action == "verify" else common
        (directory / "bin").mkdir(exist_ok=True)
        command = [python, str(common / "kotlin_tools.py"), "--toolchain", str(common / "toolchain.json")]
        if action == "verify":
            command += ["--verifier", str(verifier / "toolchain.json")]
        command.append("test" if action == "run_tests" else action)
        target = directory / "bin" / action
        target.write_text("#!/bin/sh\nexec " + shlex.join(command) + ' "$@"\n')
        target.chmod(0o755)


def completion_requested(command: str, output: str, returncode: int) -> bool:
    marker = "COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT"
    return (returncode == 0 and marker in output.splitlines()
            and command.strip() == "echo " + marker)


def execute_agent(config: RunConfig, selected: dict, condition: str) -> dict:
    from minisweagent.agents.default import DefaultAgent
    from minisweagent.environments.local import LocalEnvironment
    from minisweagent.exceptions import Submitted

    directory = config.output / selected["dataset"] / selected["id"] / condition
    result_path = directory / "result.json"
    if result_path.exists():
        return json.loads(result_path.read_text())
    if directory.exists():
        raise FileExistsError(f"Incomplete attempt requires inspection before retry: {directory}")
    directory.mkdir(parents=True)
    workspace = directory / "workspace"
    task = config.project / "benchmark-data" / selected["dataset"] / "tasks" / selected["id"]
    shutil.copytree(task / "public", workspace)
    public_metadata = json.loads((task / "public/task.json").read_text())
    if selected["dataset"] == "codecontests":
        public_metadata["output_checker"] = selected["checker"]
        write_json(workspace / "task.json", public_metadata)
    common = config.project / "pilot/toolchain/common"
    verifier = config.project / "pilot/toolchain/verifier"
    readable = [common, config.project / ".venv"] + ([verifier] if condition == "verifier" else [])
    bins = ([verifier / "bin"] if condition == "verifier" else []) + [common / "bin", config.project / ".venv/bin"]
    env = environment(workspace, bins)
    policy = profile(workspace, readable)
    (directory / "sandbox.sb").write_text(policy)
    actions_path = directory / "actions.jsonl"

    class AgentEnvironment(LocalEnvironment):
        executed_actions: int = 0

        def execute(self, action: dict, cwd: str = "", **kwargs) -> dict:
            if action["command"].strip() == "echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT" and not self.executed_actions:
                return {"returncode": 1, "output": "Implement the solution before submitting.", "exception_info": ""}
            started = time.time()
            result = run(["/bin/bash", "-c", action["command"]], cwd=workspace, env=env, sandbox=policy)
            output = {"returncode": result["returncode"], "output": result["stdout"] + result["stderr"],
                      "exception_info": ""}
            self.executed_actions += 1
            if ("COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT" in result["stdout"].splitlines()
                    and not completion_requested(action["command"], result["stdout"], result["returncode"])):
                output["output"] += "\nNot submitted. Inspect the tool results above. Submit in a separate action containing only: echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT\n"
            with actions_path.open("a") as stream:
                stream.write(json.dumps({"started": started, "elapsed_seconds": time.time() - started,
                                         "action": action, "result": output}) + "\n")
            if completion_requested(action["command"], result["stdout"], result["returncode"]):
                raise Submitted({"role": "exit", "content": "",
                                 "extra": {"exit_status": "Submitted", "submission": ""}})
            return output

    commands = (
        "Commands: compile compiles your submission. run_tests compiles it and runs the supplied public tests. "
        "Both commands are on PATH. You can also write your own tests and run ordinary shell commands. "
        "Only the required submission file is collected, so put any helper functions in that file. "
        "Read prompt.txt for the complete problem and keep the required function signature or main entry point. "
        "The final score depends only on passing hidden behavioral tests, which are unavailable during solving."
    )
    if condition == "verifier":
        commands += (
            " You also have the optional verify command, which invokes Jormungandr/SnaKt on your submission. "
            "Consider running verify on an early implementation when it involves array bounds, integer overflow, "
            "division, loop boundaries, or invariants that public tests do not cover. Run it as a shell command, "
            "inspect its diagnostics on the next turn, and decide whether to revise code or specifications. "
            "You can try verify without annotations: it attempts supported safety obligations, but may need "
            "preconditions or loop invariants. It does not infer the problem's functional specification. "
            f"Read {verifier / 'QUICKSTART.txt'} for a minimal example and diagnostic guidance. "
            f"The full specification guide is {verifier / 'SPECIFICATIONS.md'}. "
            "A failed proof is not necessarily a code defect. Unsupported or skipped declarations are not verified. "
            "Only add assumptions justified by the problem and its callers. Do not narrow the task's input domain "
            "or suppress checks merely to get a successful verification result. "
            "Verification remains optional and has no direct effect on your score. Choose when and how to use it."
        )
    model = CodexModel(CodexConfig(config.model, config.effort,
                                   str(config.project / "pilot/.runtime/codex-home"), str(directory / "model")))
    agent = DefaultAgent(
        model, AgentEnvironment(cwd=str(workspace), env=env),
        system_template=("You are a coding agent running under mini-SWE-agent. "
                         "Respond with a short explanation followed by exactly ONE mswea_bash_command code block. "
                         "Your shell command is executed by mini-SWE-agent. "
                         "Work iteratively: inspect the task and files, implement a solution, run public tests "
                         "and any additional checks you find useful, inspect their results, and revise as needed. "
                         "Commands return observations on your next turn. Use those observations to decide your next step. "
                         "When finished, submit in a SEPARATE action containing only: "
                         "echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT. "
                         "Do not combine submission with writing code or running checks. "
                         "Do not use any native Codex tools."),
        instance_template="{{task}}", step_limit=0, cost_limit=0, wall_time_limit_seconds=0,
        output_path=directory / "trajectory.json")
    problem = (task / "public/prompt.txt").read_text()
    started = time.time()
    LOGGER.info("START %s %s %s", selected["dataset"], selected["id"], condition)
    failure = None
    try:
        completion = agent.run(task=commands + "\n\nRequired submission: " + public_metadata["solution_file"] + "\n\n" + problem)
    except Exception as error:
        failure = {"type": type(error).__name__, "message": str(error)}
        completion = {"exit_status": type(error).__name__}
        LOGGER.exception("Agent infrastructure failed: %s %s", selected["id"], condition)
    final_source = workspace / public_metadata["solution_file"]
    submission = directory / public_metadata["solution_file"]
    if final_source.is_file() and not final_source.is_symlink():
        shutil.copyfile(final_source, submission)
    hidden = evaluate(config.project, selected, submission, directory / "evaluator-scratch")
    write_json(directory / "hidden-evaluation.json", hidden)
    actions = [json.loads(line) for line in actions_path.read_text().splitlines()] if actions_path.exists() else []
    verify_calls = sum(bool(re.search(r"(?:^|[;&|\n])\s*verify(?:\s|$)", row["action"]["command"])) for row in actions)
    result = {"dataset": selected["dataset"], "task_id": selected["id"], "condition": condition,
              "model": config.model, "reasoning_effort": config.effort,
              "started_unix": started, "elapsed_seconds": time.time() - started,
              "exit_status": completion.get("exit_status"), "infrastructure_error": failure,
              "valid_run": failure is None, "hidden_passed": hidden["passed"],
              "model_calls": agent.n_calls, "shell_actions": len(actions),
              "explicit_verify_commands": verify_calls, "hidden_suite": selected["dataset"] + ":" +
              ("unexposed_humaneval_cases" if selected["dataset"] == "kotlinhumaneval" else "original_private_tests"),
              "submission_sha256": hashlib.sha256(submission.read_bytes()).hexdigest() if submission.exists() else None}
    write_json(result_path, result)
    LOGGER.info("DONE %s %s hidden_passed=%s calls=%d verify_commands=%d", selected["id"], condition,
                hidden["passed"], agent.n_calls, verify_calls)
    return result


def validate_hidden_suites(project: Path, selection: dict) -> None:
    for task in selection["tasks"]:
        if task["dataset"] != "codecontests":
            continue
        path = project / "benchmark-data/codecontests/tasks" / task["id"] / "evaluator/private-tests.json"
        tests = json.loads(path.read_text())
        if not tests["input"] or len(tests["input"]) != len(tests["output"]):
            raise ValueError(f"Missing or unaligned original private tests: {task['id']}")


def load_results(output: Path) -> list[dict]:
    paths = sorted(output.glob("*/*/*/result.json"))
    invalid_tasks = set()
    for path in paths:
        evaluation = json.loads((path.parent / "hidden-evaluation.json").read_text())
        if evaluation.get("stage") == "hidden_tests" and evaluation.get("test_count") == 0:
            invalid_tasks.add((path.parent.parent.parent.name, path.parent.parent.name))
    # Eligibility belongs to the task, even if a submission failed before testing.
    project = Path(__file__).resolve().parents[1]
    selection = output / "selection.json"
    if selection.exists():
        for task in json.loads(selection.read_text())["tasks"]:
            if task["dataset"] == "codecontests":
                suite = project / "benchmark-data/codecontests/tasks" / task["id"] / "evaluator/private-tests.json"
                if suite.exists() and not json.loads(suite.read_text())["input"]:
                    invalid_tasks.add((task["dataset"], task["id"]))
    rows = []
    for path in paths:
        row = json.loads(path.read_text())
        key = (path.parent.parent.parent.name, path.parent.parent.name)
        row["evaluation_valid"] = key not in invalid_tasks
        if not row["evaluation_valid"]:
            row["valid_run"] = False
            row["evaluation_error"] = "No hidden tests in the selected evaluation suite"
        rows.append(row)
    return rows


def summarize(output: Path) -> dict:
    selection = json.loads((output / "selection.json").read_text())
    results = load_results(output)
    groups = []
    for dataset in ["kotlinhumaneval", "codecontests"]:
        for condition in ["baseline", "verifier"]:
            rows = [row for row in results if row["dataset"] == dataset and row["condition"] == condition]
            valid = [row for row in rows if row["valid_run"]]
            passed = sum(row["hidden_passed"] for row in valid)
            groups.append({"dataset": dataset, "condition": condition, "requested": sum(task["dataset"] == dataset for task in selection["tasks"]),
                           "finished": len(rows), "valid_runs": len(valid), "hidden_passed": passed,
                           "success_rate": passed / len(valid) if valid else None,
                           "infrastructure_failures": sum(row.get("infrastructure_error") is not None for row in rows),
                           "invalid_evaluations": sum(not row["evaluation_valid"] for row in rows),
                           "explicit_verify_commands": sum(row["explicit_verify_commands"] for row in valid)})
    report = {"model": selection["model"], "requested_runs": 2 * len(selection["tasks"]), "finished_runs": len(results),
              "all_runs_valid": len(results) == 2 * len(selection["tasks"]) and all(row["valid_run"] for row in results),
              "metric": "fraction of final submissions passing all hidden tests", "groups": groups,
              "generated_tests_used": False, "purpose": "Pipeline pilot. One repetition per task, no agent budget imposed. Not an estimate of a reliable treatment effect."}
    write_json(output / "summary.json", report)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("runs/pilot-20261114"))
    parser.add_argument("--selection", type=Path, default=Path("pilot/selection.json"))
    parser.add_argument("--preflight", type=Path, default=Path("pilot/preflight"))
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--task", action="append")
    parser.add_argument("--condition", choices=["baseline", "verifier"])
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args()
    project = Path(__file__).resolve().parents[1]
    output = args.output.resolve()
    config = RunConfig(project, output, args.workers)
    if args.summary_only:
        print(json.dumps(summarize(output), indent=2))
        return
    os.environ["MSWEA_SILENT_STARTUP"] = "1"
    os.environ["MSWEA_GLOBAL_CONFIG_DIR"] = str(project / "pilot/.runtime/mini-config")
    output.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                        handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler(output / "runner.log")])
    selection = json.loads(args.selection.read_text())
    validate_hidden_suites(project, selection)
    if (output / "selection.json").exists() and json.loads((output / "selection.json").read_text()) != selection:
        raise ValueError("Frozen selection differs from existing run")
    write_json(output / "selection.json", selection)
    preflight = json.loads((args.preflight / "summary.json").read_text())
    if preflight["reference_checks"] != len(selection["tasks"]) or preflight["failed"]:
        raise ValueError("The frozen sample has not passed all reference sanity checks")
    selection_hash = hashlib.sha256(args.selection.read_bytes()).hexdigest()
    if args.selection != Path("pilot/selection.json") and preflight.get("selection_sha256") != selection_hash:
        raise ValueError("Preflight does not match this frozen selection")
    run_config = {"selection_sha256": selection_hash,
                  "source_code_sha256": {path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                                         for path in sorted((project / "pilot").glob("*.py"))},
                  "verifier_quickstart_sha256": hashlib.sha256((project / "pilot/verifier-quickstart.txt").read_bytes()).hexdigest(),
                  "mini_swe_agent_version": "2.4.6", "codex_cli_version": "0.146.0",
                  "verifier_revision": "f30b44d6ebb238db28cb3b8a56b07a6c0adbaca9",
                  "toolchain": json.loads((project / "pilot/toolchain/provenance.json").read_text()),
                  "python": sys.version, "parallel_workers": args.workers,
                  "local_disk_available_bytes": shutil.disk_usage(project).free,
                  "native_codex_tools": "disabled; environments=[], feature switches off, unexpected calls rejected",
                  "isolation": "macOS sandbox denies network, private home data, cross-workspace access, and writes outside own workspace"}
    if (output / "run-config.json").exists():
        previous = json.loads((output / "run-config.json").read_text())
        if (previous["source_code_sha256"] != run_config["source_code_sha256"]
                or previous.get("verifier_quickstart_sha256") != run_config["verifier_quickstart_sha256"]):
            raise ValueError("Runner source changed since this run began. Use a new output directory.")
    else:
        write_json(output / "run-config.json", run_config)
    prepare_codex_home(project / "pilot/.runtime/codex-home")
    prepare_commands(project)
    jobs = []
    for index, selected in enumerate(selection["tasks"]):
        if args.task and selected["id"] not in args.task:
            continue
        for condition in (["baseline", "verifier"] if index % 2 == 0 else ["verifier", "baseline"]):
            if args.condition and condition != args.condition:
                continue
            jobs.append((selected, condition))
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(execute_agent, config, selected, condition): (selected, condition)
                   for selected, condition in jobs}
        for future in as_completed(futures):
            future.result()
            summarize(output)
    print(json.dumps(summarize(output), indent=2))


if __name__ == "__main__":
    main()
