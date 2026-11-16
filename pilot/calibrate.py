"""Freeze and sanity-check a separate algorithmic calibration sample."""

from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path

from pilot.evaluate import reference_check
from pilot.run import validate_hidden_suites, write_json


def prepare(project: Path) -> None:
    families = {
        "cf-460-C": "Binary search with a difference-array feasibility check",
        "cf-483-B": "Binary search with integer division and inclusion-exclusion",
        "cf-1060-C": "Subarray sums, product overflow, and rectangle boundaries",
        "cf-895-B": "Counting pairs with duplicates and inclusive division boundaries",
        "cf-1355-C": "Prefix sums and strict triangle-inequality boundaries",
        "cf-607-B": "Interval dynamic programming and empty-interval base cases",
        "cf-988-F": "Dynamic programming with unreachable states and rain boundaries",
        "cf-958-C2": "Prefix remainders and dynamic programming over nonempty partitions",
    }
    previous = json.loads((project / "pilot/selection.json").read_text())
    excluded = {row["id"] for row in previous["tasks"]}
    metadata = {row["id"]: row for row in map(json.loads,
                (project / "benchmark-data/codecontests/tasks.jsonl").read_text().splitlines())}
    tasks = []
    for tid, family in families.items():
        assert tid not in excluded
        row = metadata[tid]
        assert not row["repeated_inputs_with_different_expected_outputs"]
        tasks.append({"dataset": "codecontests", "id": tid, "rating_band": row["rating_band"],
                      "difficulty": row["difficulty"], "checker": "tokens", "family": family})
    selection = {**previous, "task_count": len(tasks), "tasks": tasks,
                 "purpose": "Calibration only, excluded from future confirmatory evaluation",
                 "selection": "Eight previously unused Codeforces problems chosen by algorithm family and complete input/output statements, before any agent outcomes. Ratings 1600-2100. No filtering by verifier success or model outcomes.",
                 "checker_review": "All eight statements require one uniquely determined integer. Whitespace-token comparison is sufficient.",
                 "screening_exclusions": {"cf-922-E": "An input constraint is missing and represented as <image>."},
                 "criteria": {
                     "workflow_ready": "Agents consume tool observations before submission, with no infrastructure errors.",
                     "verifier_engagement": "Record calls and consumed diagnostics separately from hidden-test outcomes. Unsupported or skipped checks do not establish verification.",
                     "difficulty_headroom": "Baseline hidden-test success below 100 percent indicates headroom in this sample.",
                     "descriptive_outcome": "Report both success rates and paired wins/losses/ties. No significance or efficacy claim from eight tasks.",
                     "inconclusive_for_feedback_effect": "No verifier calls, no supported diagnostics, baseline ceiling, or infrastructure errors prevent a useful feedback-effect interpretation."}}

    target = project / "pilot/calibration-selection.json"
    if target.exists() and json.loads(target.read_text()) != selection:
        raise ValueError("Refusing to change a frozen calibration selection")
    write_json(target, selection)
    validate_hidden_suites(project, selection)
    output = project / "pilot/calibration-preflight"

    def check(task: dict) -> dict:
        result = reference_check(project, task, output / task["id"])
        write_json(output / task["id"] / "result.json", result)
        return {"id": task["id"], "passed": result["passed"]}

    with ThreadPoolExecutor(max_workers=4) as executor:
        checks = list(executor.map(check, tasks))
    summary = {"reference_checks": len(checks), "failed": [r for r in checks if not r["passed"]],
               "selection_sha256": hashlib.sha256(target.read_bytes()).hexdigest(), "checks": checks}
    write_json(output / "summary.json", summary)
    print(json.dumps(summary, indent=2))
    if summary["failed"]:
        raise RuntimeError("Reference sanity checks failed")


if __name__ == "__main__":
    prepare(Path(__file__).resolve().parents[1])
