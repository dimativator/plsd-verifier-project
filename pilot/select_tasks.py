"""Freeze the 40-task plumbing pilot before observing agent outcomes."""

import hashlib
import json
from pathlib import Path

CONTESTS = ["cf-1197-B", "cf-894-A", "cf-339-B", "cf-765-B",
            "cf-962-A", "cf-250-B", "cf-1256-B", "cf-934-A",
            "cf-1042-D", "cf-55-B", "cf-1025-C", "cf-199-C",
            "cf-1336-C", "cf-451-E", "cf-1380-E", "cf-1223-D",
            "cf-724-F", "cf-449-E", "cf-1109-E", "cf-1473-E"]


def select(project: Path) -> dict:
    bundle = project / "benchmark-data"
    humaneval = [json.loads(line) for line in (bundle / "kotlinhumaneval/tasks.jsonl").read_text().splitlines()]
    humaneval.sort(key=lambda row: hashlib.sha256(("20261114:" + row["id"]).encode()).hexdigest())
    contests = {row["id"]: row for row in
                (json.loads(line) for line in (bundle / "codecontests/tasks.jsonl").read_text().splitlines())}
    rows = []
    for dataset, tasks in [("kotlinhumaneval", humaneval[:20]), ("codecontests", [contests[tid] for tid in CONTESTS])]:
        for row in tasks:
            rows.append({"dataset": dataset, "id": row["id"], "rating_band": row.get("rating_band"),
                         "checker": "kotlin_harness" if dataset == "kotlinhumaneval" else
                         "casefold_tokens" if row["id"] == "cf-1197-B" else "tokens"})
    return {"seed": 20261114, "task_count": 40, "conditions": ["baseline", "verifier"],
            "model": "gpt-5.6-luna", "reasoning_effort": "medium", "repetitions": 1,
            "selection": {"kotlinhumaneval": "First 20 tasks sorted by SHA256('20261114:' + task_id)",
                          "codecontests": "Four tasks per rating band, reviewed for a unique output before any agent runs. Candidate order came from the same seeded hash. Explicit IDs are frozen here."},
            "checker_review": "Selected contest output requirements are integer scalars/vectors, a unique lexicographic permutation, a specified IPv6 expansion, or YES/NO. cf-1197-B explicitly permits any letter case. Other tokens are case-sensitive.",
            "hidden_suites": {"kotlinhumaneval": ["HiddenTests.kt"], "codecontests": ["private-tests.json"]},
            "generated_tests": "Excluded from this plumbing pilot before agent runs because generated input-domain validity has not been reviewed. Source data remains unchanged.",
            "runtime_limits": {"test_timeout_seconds": 10, "jvm_max_heap": "1g"},
            "agent_limits": {"steps": 0, "cost": 0, "wall_time_seconds": 0,
                             "meaning": "No imposed agent budget for this plumbing pilot"},
            "primary_outcome": "All final hidden tests pass", "tasks": rows}


if __name__ == "__main__":
    project = Path(__file__).resolve().parents[1]
    destination = project / "pilot/selection.json"
    value = select(project)
    if destination.exists() and json.loads(destination.read_text()) != value:
        raise ValueError("Refusing to alter an existing pilot selection")
    destination.write_text(json.dumps(value, indent=2) + "\n")
