"""Select reviewed, fresh Codeforces tasks without executing benchmark code.

The selection is provisional until the Docker reference preflight passes. Generated
tests are deliberately excluded: their input domains have not been validated.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess
from typing import Any

PROJECT = Path(__file__).resolve().parents[1]
BANDS = ("2000-2399", "2400+")
DEFAULT_OUTPUT = PROJECT / "runs/calibration-20261123/task-validation.json"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_sha256(path: Path) -> str:
    """Portable digest of the text bundle, unaffected by Git's CRLF checkout."""
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def family_id(task_id: str) -> str:
    # At minimum, easy/hard versions of the same indexed contest problem cluster.
    return re.sub(r"([A-Z])\d+$", r"\1", task_id)


def seeded_key(task_id: str, seed: int) -> str:
    return hashlib.sha256(f"{seed}:{task_id}".encode()).hexdigest()


def exposed_tasks(project: Path) -> tuple[set[str], dict[str, str]]:
    exposed: set[str] = set()
    files = {}
    for folder in ("pilot", "python_pilot"):
        for path in sorted((project / folder).glob("*selection*.json")):
            rows = load(path).get("tasks", [])
            if not isinstance(rows, list):
                continue
            files[path.relative_to(project).as_posix()] = canonical_sha256(path)
            exposed.update(row["id"] if isinstance(row, dict) else row for row in rows)
    return exposed, files


def section(prompt: str, heading: str) -> str:
    # The first Output is the required format; example outputs occur afterwards.
    match = re.search(
        rf"\n{heading}\s*\n(.*?)(?:\n(?:Input|Output|Examples?|Note)\s*\n|$)", prompt, re.S
    )
    return match.group(1).strip() if match else ""


def read_suite(path: Path) -> list[tuple[str, str]]:
    data = load(path)
    inputs, outputs = data.get("input"), data.get("output")
    if not isinstance(inputs, list) or not isinstance(outputs, list) or len(inputs) != len(outputs):
        raise ValueError(f"Misaligned input/output arrays: {path.name}")
    if any(not isinstance(value, str) for value in inputs + outputs):
        raise ValueError(f"Non-string test payload: {path.name}")
    if any(not value.strip() for value in inputs):
        raise ValueError(f"Empty test input: {path.name}")
    return list(zip(inputs, outputs))


def input_key(value: str) -> str:
    # Conservative leakage filter: whitespace variants are treated as overlap.
    return " ".join(value.split())


def output_tokens(value: str, checker: str) -> list[str] | list[int]:
    tokens = value.split()
    if checker == "integer_tokens":
        if any(not re.fullmatch(r"[+-]?\d+", token) for token in tokens):
            raise ValueError("Noninteger output for integer checker")
        return [int(token) for token in tokens]
    if checker == "casefold_tokens":
        return [token.casefold() for token in tokens]
    if checker != "tokens":
        raise ValueError(f"Unknown checker: {checker}")
    return tokens


def compare_output(actual: str, expected: str, checker: str) -> bool:
    try:
        return output_tokens(actual, checker) == output_tokens(expected, checker)
    except ValueError:
        return False


def portable_cpp(source: str) -> tuple[str, int]:
    """Port the old MSVC 64-bit printf/scanf length modifier, without algorithm edits."""
    return re.subn(r"(?<!%)%I64([diuoxX])", r"%ll\1", source)


def suite_checks(
    public: list[tuple[str, str]], private: list[tuple[str, str]], checker: str
) -> list[str]:
    reasons = []
    if not public:
        reasons.append("empty_public_suite")
    if not private:
        reasons.append("empty_private_suite")
    public_keys = {input_key(inp) for inp, _ in public}
    if public_keys & {input_key(inp) for inp, _ in private}:
        reasons.append("actual_public_private_input_overlap")
    expected: dict[str, list[str] | list[int]] = {}
    for inp, out in public + private:
        try:
            answer = output_tokens(out, checker)
        except ValueError:
            reasons.append("expected_output_incompatible_with_checker")
            continue
        if not answer:
            reasons.append("empty_expected_output")
        key = input_key(inp)
        if key in expected and expected[key] != answer:
            reasons.append("actual_conflicting_expected_outputs")
        expected[key] = answer
        if "\x00" in inp or "\x00" in out:
            reasons.append("nul_in_test_payload")
    return sorted(set(reasons))


def metadata_reasons(
    row: dict, exposed_families: set[str], *, calibration: bool = False
) -> list[str]:
    reasons = []
    if row["rating_band"] not in BANDS:
        reasons.append("rating_below_2000")
    was_exposed = family_id(row["id"]) in exposed_families
    if was_exposed != calibration:
        reasons.append(
            "previously_exposed_family" if was_exposed else "not_exposed_calibration_pool"
        )
    if not row["private_test_count"]:
        reasons.append("empty_private_suite")
    for flag in (
        "held_out_public_input_overlap",
        "repeated_inputs_with_different_expected_outputs",
    ):
        if row.get(flag):
            reasons.append(flag)
    return reasons


def inspect_task(project: Path, row: dict, review: dict) -> tuple[dict, list[str]]:
    task_dir = project / "benchmark-data/codecontests" / row["task_dir"]
    prompt = (task_dir / "public/prompt.txt").read_text(encoding="utf-8")
    reasons = []
    if "<image>" in prompt:
        reasons.append("missing_statement_image")
    if not section(prompt, "Input") or not section(prompt, "Output"):
        reasons.append("missing_input_or_output_section")
    if section(prompt, "Output") != review["output_requirement"]:
        reasons.append("review_output_requirement_drift")
    if canonical_sha256(task_dir / "public/prompt.txt") != review["prompt_sha256_lf"]:
        reasons.append("review_statement_drift")
    public = read_suite(task_dir / "public/public-tests.json")
    private = read_suite(task_dir / "evaluator/private-tests.json")
    if len(public) != row["public_test_count"] or len(private) != row["private_test_count"]:
        reasons.append("metadata_test_count_mismatch")
    reasons.extend(suite_checks(public, private, review["checker"]))
    references = load(task_dir / "evaluator/references/index.json")
    supported = [ref for ref in references if ref["language"] in {"PYTHON", "CPP", "JAVA"}]
    if not supported:
        reasons.append("no_supported_source_reference")
    record = {
        "id": row["id"],
        "dataset": "codecontests",
        "rating": row["difficulty"],
        "rating_band": row["rating_band"],
        "family": family_id(row["id"]),
        "checker": review["checker"],
        "checker_review": review["rationale"],
        "output_requirement": review["output_requirement"],
        "input_requirement": section(prompt, "Input"),
        "input_domain_review": {
            "status": "source_statement_screened_not_exhaustively_proved",
            "checks": [
                "input/output sections retained",
                "no missing image markers",
                "nonempty string test inputs",
                "reference preflight required",
            ],
            "limitation": "No generic parser can establish every task's semantic input constraints; original private tests retained without generated tests.",
        },
        "public_test_count": len(public),
        "private_test_count": len(private),
        "references": supported,
        "data_sha256_lf": {
            name: canonical_sha256(task_dir / name)
            for name in (
                "public/prompt.txt",
                "public/public-tests.json",
                "evaluator/private-tests.json",
            )
        },
        "behavioral_validation": "pending",
    }
    return record, sorted(set(reasons))


def select_by_band(
    records: list[dict], count: int, reserve: int, seed: int
) -> tuple[list[dict], list[dict]]:
    selected, reserves = [], []
    used_families: set[str] = set()
    for band in BANDS:
        rows = sorted(
            (r for r in records if r["rating_band"] == band),
            key=lambda r: seeded_key(r["id"], seed),
        )
        unique = []
        for row in rows:
            if row["family"] not in used_families:
                unique.append(row)
                used_families.add(row["family"])
        if len(unique) < count + reserve:
            raise ValueError(
                f"Insufficient reviewed {band} families: {len(unique)} < {count + reserve}"
            )
        selected.extend(unique[:count])
        reserves.extend(unique[count : count + reserve])
    return selected, reserves


def build_manifest(
    project: Path,
    reviews_path: Path,
    *,
    seed: int = 20261123,
    per_band: int = 50,
    reserves: int = 10,
) -> dict:
    exposed, exposure_hashes = exposed_tasks(project)
    exposed_families = {family_id(task) for task in exposed}
    reviews = load(reviews_path)
    rows = [
        json.loads(line)
        for line in (project / "benchmark-data/codecontests/tasks.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
        if line.strip()
    ]
    accepted, calibration, exclusions = [], [], []
    metadata_clean = Counter()
    calibration_ids = set(reviews["calibration_ids"])
    for row in rows:
        is_calibration = row["id"] in calibration_ids
        reasons = metadata_reasons(row, exposed_families, calibration=is_calibration)
        if not reasons and not is_calibration:
            metadata_clean[row["rating_band"]] += 1
        review = reviews["reviews"].get(row["id"])
        if not review:
            reasons.append("no_explicit_statement_checker_review")
        elif review.get("status", "accepted") != "accepted":
            reasons.append(
                "checker_review_rejected: " + review.get("exclusion_reason", "ambiguous contract")
            )
        if reasons:
            exclusions.append({"id": row["id"], "reasons": reasons})
            continue
        try:
            record, reasons = inspect_task(project, row, review)
        except (ValueError, KeyError) as error:
            reasons = [f"invalid_test_payload: {error}"]
        if reasons:
            exclusions.append({"id": row["id"], "reasons": reasons})
        else:
            (calibration if is_calibration else accepted).append(record)
    if {r["id"] for r in calibration} != calibration_ids:
        raise ValueError(
            "At least one calibration task failed static validation; inspect exclusions"
        )
    tasks, reserve_tasks = select_by_band(accepted, per_band, reserves, seed)
    calibration.sort(key=lambda r: (BANDS.index(r["rating_band"]), seeded_key(r["id"], seed)))
    return {
        "schema_version": 1,
        "status": "provisional_pending_reference_preflight",
        "seed": seed,
        "source_commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=project, text=True
        ).strip(),
        "selection_rule": "SHA256(seed:task_id) within each band, explicit checker-reviewed candidates, distinct source families; first 50 main and next 10 reserves per band by default",
        "hidden_suite": "original_private_tests_only",
        "generated_tests": "excluded_before_runs_due_to_unvalidated_domains",
        "hash_scheme": "SHA256 UTF-8 source bytes with CRLF normalized to LF",
        "exposed_task_count": len(exposed),
        "exposure_manifests_sha256_lf": exposure_hashes,
        "review_file_sha256_lf": canonical_sha256(reviews_path),
        "metadata_clean_fresh_counts": dict(metadata_clean),
        "reviewed_static_pass_counts": dict(Counter(r["rating_band"] for r in accepted)),
        "calibration_tasks": calibration,
        "tasks": tasks,
        "reserves": reserve_tasks,
        "reviewed_candidates": accepted,
        "exclusions": exclusions,
        "freeze_gate": "Require source references to pass every public and private case in no-network Docker; replace failed candidates in the prespecified within-band order before main runs. Do not select or replace using model outcomes.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=PROJECT)
    parser.add_argument(
        "--reviews", type=Path, required=True
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--seed", type=int, default=20261123)
    parser.add_argument("--per-band", type=int, default=50)
    parser.add_argument("--reserves-per-band", type=int, default=10)
    args = parser.parse_args()
    result = build_manifest(
        args.project,
        args.reviews,
        seed=args.seed,
        per_band=args.per_band,
        reserves=args.reserves_per_band,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "output": str(args.output),
                "status": result["status"],
                "main_tasks": len(result["tasks"]),
                "reserves": len(result["reserves"]),
                "calibration": len(result["calibration_tasks"]),
                "reviewed_static_pass_counts": result["reviewed_static_pass_counts"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
