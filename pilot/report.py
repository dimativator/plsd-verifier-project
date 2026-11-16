"""Collect pilot results, paired outcomes, and native Codex tool audit."""

import argparse
from collections import Counter
import csv
import json
from pathlib import Path

from pilot.run import load_results, summarize, write_json


def report(output: Path) -> dict:
    summary = summarize(output)
    selection = json.loads((output / "selection.json").read_text())
    rows = load_results(output)
    by_key = {(row["task_id"], row["condition"]): row for row in rows}
    paired = []
    for task in selection["tasks"]:
        baseline = by_key.get((task["id"], "baseline"))
        verifier = by_key.get((task["id"], "verifier"))
        if baseline is None or verifier is None:
            continue
        paired.append({"dataset": task["dataset"], "task_id": task["id"], "rating_band": task["rating_band"],
                       "baseline_passed": baseline["hidden_passed"], "verifier_passed": verifier["hidden_passed"],
                       "both_valid": baseline["valid_run"] and verifier["valid_run"],
                       "baseline_model_calls": baseline["model_calls"], "verifier_model_calls": verifier["model_calls"],
                       "explicit_verify_commands": verifier["explicit_verify_commands"]})
    with (output / "paired-results.csv").open("w", newline="") as stream:
        fields = ["dataset", "task_id", "rating_band", "baseline_passed", "verifier_passed", "both_valid",
                  "baseline_model_calls", "verifier_model_calls", "explicit_verify_commands"]
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(paired)
    native = Counter()
    models = Counter()
    server_requests = []
    reroutes = []
    calls = 0
    for path in output.glob("*/*/*/model/*.events.jsonl"):
        calls += 1
        for line in path.read_text().splitlines():
            event = json.loads(line)
            if event.get("id") == 2 and "result" in event:
                models[event["result"].get("model", "unknown")] += 1
            if event.get("method") == "item/started":
                native[event["params"]["item"]["type"]] += 1
            if "id" in event and "method" in event:
                server_requests.append(event["method"])
            if event.get("method") == "model/rerouted":
                reroutes.append(event["params"])
    unexpected = {kind: count for kind, count in native.items() if kind not in {"userMessage", "agentMessage", "reasoning"}}
    audit = {"model_calls": calls, "resolved_models": dict(models), "item_types": dict(native),
             "unexpected_native_tool_items": unexpected, "server_tool_or_approval_requests": server_requests,
             "model_reroutes": reroutes,
             "passed": not unexpected and not server_requests and not reroutes and set(models) == {"gpt-5.6-luna"}}
    write_json(output / "codex-tool-audit.json", audit)
    difficulties = []
    for band in ["800-1199", "1200-1599", "1600-1999", "2000-2399", "2400+"]:
        tasks = [row for row in paired if row["rating_band"] == band and row["both_valid"]]
        difficulties.append({"rating_band": band, "tasks": len(tasks),
                             "baseline_passed": sum(row["baseline_passed"] for row in tasks),
                             "verifier_passed": sum(row["verifier_passed"] for row in tasks)})
    summary.update({"invalid_evaluations": [{"task_id": row["task_id"], "condition": row["condition"], "reason": row["evaluation_error"]} for row in rows if not row["evaluation_valid"]],"native_codex_tool_audit": audit, "codecontests_by_difficulty": difficulties,
                    "exit_status_counts": dict(Counter(row["exit_status"] for row in rows)),
                    "verifier_condition_runs_using_verify": sum(row["condition"] == "verifier" and row["explicit_verify_commands"] > 0 for row in rows),
                    "paired_counts": dict(Counter(
                        "both_pass" if row["baseline_passed"] and row["verifier_passed"] else
                        "baseline_only" if row["baseline_passed"] else
                        "verifier_only" if row["verifier_passed"] else "both_fail"
                        for row in paired if row["both_valid"]))})
    write_json(output / "report.json", summary)
    lines = ["GPT-5.6-Luna / mini-SWE-agent pipeline pilot", "", f"Finished runs: {summary['finished_runs']}/{summary['requested_runs']}", "",
             "Dataset          Condition  Passed / valid  Hidden success rate"]
    for group in summary["groups"]:
        rate = f"{100 * group['success_rate']:.1f}%" if group["success_rate"] is not None else "pending"
        lines.append(f"{group['dataset']:16} {group['condition']:10} {group['hidden_passed']:2}/{group['valid_runs']:<2}             {rate}")
    lines += ["", f"Invalid evaluations excluded: {summary['invalid_evaluations']}"]
    lines += ["", "CodeContests rating band  Baseline  Verifier"]
    for band in difficulties:
        lines.append(f"{band['rating_band']:24} {band['baseline_passed']}/{band['tasks']}       {band['verifier_passed']}/{band['tasks']}")
    lines += ["", f"Verifier-enabled runs using the explicit verify command: {summary['verifier_condition_runs_using_verify']}/{len(selection['tasks'])}",
              f"Agent exit statuses: {summary['exit_status_counts']}",
              f"Native Codex tool audit passed: {audit['passed']}",
              f"Resolved models: {dict(models)}", "",
              "Metric: final code passes all hidden tests. Proof success is not scored.",
              "CodeContests uses original private tests. Generated tests are excluded.",
              "One run per task and condition. Both conditions have uncapped agent budgets in this plumbing pilot.",
              ("No agent called the verifier, so these scores do not measure the effect of verifier feedback."
               if not summary["verifier_condition_runs_using_verify"] else
               "Verifier availability is the treatment. Tool use is optional. This small calibration cannot establish a reliable treatment effect."),
              "Separate positive and negative verifier checks passed in pilot/preflight/verifier-tool-smoke.json.",
              "The separately archived harness debugging batch is excluded from these scores."]
    (output / "REPORT.txt").write_text("\n".join(lines) + "\n")
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("runs/pilot-20261114"))
    args = parser.parse_args()
    print(json.dumps(report(args.output.resolve()), indent=2))
