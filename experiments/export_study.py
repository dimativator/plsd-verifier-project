"""Export the public Codeforces study data and verify its checksums."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import re
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path, PurePosixPath

ARMS = ("baseline", "verifier", "guided_verifier")
IDENTITY = ("phase", "model", "task_id", "condition", "repetition")
ROW_FIELDS = (
    *IDENTITY,
    "family_id",
    "rating_band",
    "hidden_passed",
    "valid_run",
    "exit_status",
    "model_cost_usd",
    "cost_is_upper_bound",
    "solve_seconds",
    "evaluation_seconds",
)
SPEC_FIELDS = (*IDENTITY, "family_id", "rating_band")
RESOURCE_FIELDS = (
    "effort",
    "max_output_tokens",
    "step_limit",
    "solve_limit_seconds",
    "per_run_cap_usd",
)
ANALYSIS_FIELDS = (
    "schema_version",
    "phase",
    "planned_conditions",
    "confidence_level",
    "descriptive_confidence_level",
    "planned_runs",
    "observed_result_records",
    "observed_unique_runs",
    "scored_runs",
    "completeness_known",
    "complete",
    "missing_runs",
    "unexpected_runs",
    "blockers",
    "warnings",
    "models",
    "observed_model_spend_usd",
    "observed_model_spend_is_upper_bound",
    "spend_note",
    "multiplicity",
    "settings_compatibility",
    "contrast_analyses",
    "reporting_scope",
)
PROCESS_COUNTS = (
    "runs",
    "runs_with_verifier_evidence",
    "runs_with_wrapper",
    "runs_with_direct_cli",
    "runs_with_corroborating_diagnostics",
    "wrapper_calls",
    "complete_wrapper_pairs",
    "direct_cli_commands",
    "direct_cli_commands_with_corroborating_diagnostics",
    "verifier_evidence_actions",
    "runs_with_later_main_py_change_after_verifier_action",
    "runs_with_later_main_py_change_after_counterexample_action",
    "runs_with_guide_read_command",
    "marker_anomalies",
    "inline_marker_boundary_normalizations",
    "strict_parser_marker_anomalies_before_boundary_normalization",
    "missing_action_logs",
    "action_count_mismatches",
)
DIAGNOSTICS = {
    "counterexample_reported",
    "confirmed_checked_contracts_reported",
    "inconclusive_reported",
    "unsupported_or_no_entrypoints_reported",
    "backend_or_loading_error_reported",
    "timeout_reported",
    "no_explicit_diagnostic_observed",
    "unclassified_nonzero_return",
}
SOURCE_FILES = {
    "analysis.py",
    "api_backend.py",
    "container_tools.py",
    "model_catalog.py",
    "process_audit.py",
    "run.py",
    "runtime.py",
    "submission_protocol.py",
    "three_arm_analysis.py",
    "validate_tasks.py",
}
PROMPT_HASHES = (
    "system_prompt_sha256",
    "common_prompt_sha256",
    "verifier_prompt_sha256",
    "guided_verifier_prompt_sha256",
)
HASH = re.compile(r"[0-9a-f]{64}\Z")
PRIVATE_PATH = re.compile(
    r"(?<![A-Za-z0-9])[A-Za-z]:[\\/]|\\\\[^\\]|(?:^|[\s\"\'=])/(?:Users|home|mnt|tmp|private|var)/"
)
SECRET = re.compile(
    r"sk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{20,}|-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY-----"
)


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def nonnegative_decimal(value):
    try:
        amount = Decimal(str(value))
    except InvalidOperation as error:
        raise ValueError("Malformed cost") from error
    if not amount.is_finite() or amount < 0:
        raise ValueError("Costs must be finite and nonnegative")
    return amount


def nonnegative_count(value):
    if type(value) is not int or value < 0:
        raise ValueError("Counts must be nonnegative integers")
    return value


def validate_sha256(value):
    if not isinstance(value, str) or not HASH.fullmatch(value):
        raise ValueError("Invalid SHA-256 fingerprint")
    return value


def validate_public_values(value):
    if isinstance(value, dict):
        for key, item in value.items():
            validate_public_values(key)
            validate_public_values(item)
    elif isinstance(value, list):
        for item in value:
            validate_public_values(item)
    elif isinstance(value, str) and (PRIVATE_PATH.search(value) or SECRET.search(value)):
        raise ValueError("Public export contains an absolute personal path or credential pattern")
    elif isinstance(value, float) and not math.isfinite(value):
        raise ValueError("Public export contains a nonfinite number")


def run_identity(row):
    return tuple(row[field] for field in IDENTITY)


def public_spec(source):
    row = {field: source[field] for field in SPEC_FIELDS}
    if (
        row["phase"] != "main"
        or row["condition"] not in ARMS
        or type(row["repetition"]) is not int
        or row["repetition"] not in range(1, 9)
        or not re.fullmatch(r"gpt-[A-Za-z0-9_.-]+", row["model"])
        or not re.fullmatch(r"cf-\d+-[A-Za-z0-9]+", row["task_id"])
        or not re.fullmatch(r"cf-\d+-[A-Za-z0-9]+", row["family_id"])
        or row["rating_band"] not in {"2000-2399", "2400+"}
    ):
        raise ValueError("Unexpected public run identity")
    return row


def model_settings(source):
    result = {field: source[field] for field in ("effort", "max_output_tokens")}
    if (
        result["effort"] not in {"none", "minimal", "low", "medium", "high", "xhigh"}
        or nonnegative_count(result["max_output_tokens"]) == 0
    ):
        raise ValueError("Invalid model settings")
    return result


def public_result(source):
    result = public_spec(source)
    for field in ROW_FIELDS:
        if field not in result:
            result[field] = source[field]
    if (
        result["valid_run"] is not True
        or type(result["hidden_passed"]) is not bool
        or type(result["cost_is_upper_bound"]) is not bool
        or source.get("infrastructure_error")
        or source.get("evaluation_infrastructure_error")
    ):
        raise ValueError("Selected results must be valid Boolean outcomes")
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", result["exit_status"]):
        raise ValueError("Unexpected exit status")
    for field in ("model_cost_usd", "solve_seconds", "evaluation_seconds"):
        if type(result[field]) not in (int, float):
            raise ValueError("Run costs and times must be numeric")
        nonnegative_decimal(result[field])
    result["model_settings"] = model_settings(source["model_settings"])
    result["tool_events"] = [
        {"event": "verify_invocation_observed"}
        for event in source.get("tool_events", [])
        if isinstance(event, dict) and event.get("event") == "verify_invocation_observed"
    ]
    return result


def public_process_counts(source):
    result = {
        field: nonnegative_count(source[field]) for field in PROCESS_COUNTS if field in source
    }
    for field in ("runs_by_diagnostic_category", "verifier_actions_by_diagnostic_category"):
        result[field] = {
            category: nonnegative_count(value)
            for category, value in source.get(field, {}).items()
            if category in DIAGNOSTICS
        }
    return result


def json_bytes(value):
    validate_public_values(value)
    return (json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")


def _source_inputs(source):
    raw_rows = read_json(source / "combined-results.json")
    raw_expected = read_json(source / "combined-expected.json")
    raw_audit = read_json(source / "data-audit.json")
    if raw_audit.get("complete") is not True:
        raise ValueError("Refusing an incomplete source-data audit")
    source_names = (
        "combined-results.json",
        "combined-expected.json",
        "all-attempt-costs.csv",
        "data-audit.json",
        "process-summary.json",
        "analysis_original_5.json",
        "analysis_all_8.json",
    )
    source_hashes = {
        name: hashlib.sha256((source / name).read_bytes()).hexdigest() for name in source_names
    }
    for name in (
        "combined-results.json",
        "combined-expected.json",
        "analysis_original_5.json",
        "analysis_all_8.json",
    ):
        recorded = raw_audit.get("analysis_hashes", {}).get(name)
        if recorded is not None and validate_sha256(recorded) != source_hashes[name]:
            raise ValueError("Source artifact differs from its completed audit hash")
    return raw_rows, raw_expected, raw_audit, source_hashes


def _public_rows(raw_rows, expected_runs):
    rows = [public_result(row) for row in raw_rows]
    specs = [public_spec(row) for row in expected_runs]
    observed, planned = (
        {run_identity(row): row for row in rows},
        {run_identity(row): row for row in specs},
    )
    if len(rows) != len(observed) or len(specs) != len(planned) or set(observed) != set(planned):
        raise ValueError("Duplicate, missing or unexpected selected identities")
    if (
        len(rows) != 2400
        or len({r["task_id"] for r in rows}) != 100
        or len({r["family_id"] for r in rows}) != 100
        or Counter(r["condition"] for r in rows) != Counter({arm: 800 for arm in ARMS})
        or Counter(r["repetition"] for r in rows) != Counter({rep: 300 for rep in range(1, 9)})
    ):
        raise ValueError("Study requires 100 families, eight complete repetitions and three arms")
    groups = defaultdict(set)
    for row in rows:
        if public_spec(row) != planned[run_identity(row)]:
            raise ValueError("Selected/planned family metadata differs")
        groups[(row["model"], row["task_id"])].add((row["condition"], row["repetition"]))
    wanted = {(arm, rep) for arm in ARMS for rep in range(1, 9)}
    if any(group != wanted for group in groups.values()):
        raise ValueError("Unbalanced task/repetition matrix")
    return rows, specs, planned


def _public_configs(raw_configs):
    configs = []
    for config in raw_configs:
        minimal = model_settings(config)
        minimal.update({field: config[field] for field in RESOURCE_FIELDS if field not in minimal})
        for field in ("step_limit", "solve_limit_seconds", "per_run_cap_usd"):
            if nonnegative_decimal(minimal[field]) == 0:
                raise ValueError("Resource limits must be positive")
        validate_public_values(minimal)
        configs.append(minimal)
    if not configs or any(config != configs[0] for config in configs):
        raise ValueError("Agent resource settings differ across source batches")
    return configs


def _cost_table(source, planned, raw_audit):
    costs = {}
    with (source / "all-attempt-costs.csv").open(encoding="utf-8-sig", newline="") as stream:
        for cost in csv.DictReader(stream):
            cost["repetition"] = int(cost["repetition"])
            key = run_identity(cost)
            if key not in planned or key in costs:
                raise ValueError("Unexpected or duplicate cost identity")
            costs[key] = nonnegative_decimal(cost["all_attempt_accounted_usd"])
    if set(costs) != set(planned):
        raise ValueError("Cost CSV does not cover every planned identity")
    total = sum(costs.values(), Decimal(0))
    by_arm = {
        arm: sum((value for key, value in costs.items() if key[3] == arm), Decimal(0))
        for arm in ARMS
    }
    if total != nonnegative_decimal(raw_audit["all_attempt_accounted_usd"]) or any(
        by_arm[arm] != nonnegative_decimal(raw_audit["by_condition_accounted_usd"][arm])
        for arm in ARMS
    ):
        raise ValueError("Cost CSV totals do not reconcile with audited totals")
    return costs, total, by_arm


def _public_audit(raw_audit, raw_rows, rows, total, by_arm):
    status_counts, status_costs = Counter(), defaultdict(Decimal)
    for ledger in raw_audit["ledgers"]:
        for status in ("settled", "uncertain", "pending", "rejected", "usage_upper_bound"):
            status_counts[status] += nonnegative_count(
                ledger.get("status_counts", {}).get(status, 0)
            )
            status_costs[status] += nonnegative_decimal(
                ledger.get("status_usd", {}).get(status, "0")
            )
    if sum(status_costs.values(), Decimal(0)) != total:
        raise ValueError("Ledger status costs do not reconcile")
    retry_count = sum(
        row.get("resolution", {}).get("selected_attempt", "original") != "original"
        for row in raw_rows
    )
    if (
        retry_count != nonnegative_count(raw_audit["retry_selected"])
        or raw_audit["selected_runs"] != len(rows)
        or raw_audit["task_families"] != 100
    ):
        raise ValueError("Audit selection counts do not reconcile")
    selected_cost = sum((nonnegative_decimal(r["model_cost_usd"]) for r in rows), Decimal(0))
    if selected_cost != nonnegative_decimal(raw_audit["selected_attempt_cost_usd"]):
        raise ValueError("Selected-attempt costs do not reconcile")
    audit = {
        "schema_version": 1,
        "complete": True,
        "selected_runs": len(rows),
        "task_families": 100,
        "runs_per_arm": dict(Counter(r["condition"] for r in rows)),
        "runs_per_repetition": {
            str(k): v for k, v in Counter(r["repetition"] for r in rows).items()
        },
        "retry_selected": retry_count,
        "all_attempt_accounted_usd": str(total),
        "by_condition_accounted_usd": {arm: str(value) for arm, value in by_arm.items()},
        "selected_attempt_cost_usd": str(selected_cost),
        "status_counts": dict(status_counts),
        "status_usd": {k: str(v) for k, v in status_costs.items()},
        "source_archive_sha256": validate_sha256(raw_audit["source_archive_sha256"]),
        "protocol_sha256": validate_sha256(raw_audit["protocol_sha256"]),
        "note": "All-attempt accounted costs include superseded attempts and conservative ambiguous-delivery charges; they are not exact provider invoices.",
    }
    return audit


def _public_provenance(raw_configs, source_hashes, rows, audit):
    fingerprints = []
    for config in raw_configs:
        runtime = config.get("runtime", {})
        public = {
            "source_sha256": {
                name: validate_sha256(value)
                for name, value in runtime.get("source_sha256", {}).items()
                if name in SOURCE_FILES
            },
            "prompt_sha256": {
                name: validate_sha256(runtime[name]) for name in PROMPT_HASHES if name in runtime
            },
            "portable_image_fingerprints": {
                name: validate_sha256(value)
                for name, value in runtime.get("portable_image_fingerprints", {}).items()
                if name in {"plinse-eval:20261123", "plinse-crosshair:20261123"}
            },
        }
        if public not in fingerprints:
            fingerprints.append(public)
    provenance = {
        "schema_version": 1,
        "source_protocol_sha256": audit["protocol_sha256"],
        "source_archive_sha256": audit["source_archive_sha256"],
        "recorded_runtime_fingerprints": fingerprints,
        "source_artifact_sha256": source_hashes,
        "task_ids": sorted({r["task_id"] for r in rows}),
        "original_planned_repetitions": [1, 2, 3, 4, 5],
        "exploratory_extension_repetitions": [6, 7, 8],
        "provenance_note": "Recorded hashes bind the original protocol metadata. Raw attempts, requests and source-machine paths are not part of this public analysis dataset.",
    }
    return provenance


def _public_process_summary(public_process_source):
    process = {
        "schema_version": 1,
        "expected_selected_runs": 2400,
        "selected_runs_audited": nonnegative_count(public_process_source["selected_runs_audited"]),
        "complete": public_process_source["complete"] is True,
        "summary": public_process_counts(public_process_source["summary"]),
        "by_condition": {
            arm: public_process_counts(public_process_source["by_condition"][arm]) for arm in ARMS
        },
        "limitations": "Observed wrapper markers/CLI commands and diagnostics do not prove semantic coverage or causally effective repairs. Diagnostic categories overlap. Later source changes concern main.py and do not establish that feedback caused the edit.",
    }
    if (
        not process["complete"]
        or process["selected_runs_audited"] != 2400
        or any(process["by_condition"][arm]["runs"] != 800 for arm in ARMS)
    ):
        raise ValueError("Process summary denominator differs")
    if "by_repetition_condition" in public_process_source:
        process["by_repetition_condition"] = {
            str(rep): {
                arm: public_process_counts(
                    public_process_source["by_repetition_condition"][str(rep)][arm]
                )
                for arm in ARMS
            }
            for rep in range(1, 9)
        }
    return process


def _write_export(output, payloads):
    manifest = {
        "schema_version": 1,
        "algorithm": "sha256",
        "files": {
            name: hashlib.sha256(data).hexdigest() for name, data in sorted(payloads.items())
        },
    }
    payloads["SHA256SUMS.json"] = json_bytes(manifest)
    # Check every destination before writing, so a conflict leaves the export intact.
    for name, data in payloads.items():
        destination = output / name
        if destination.is_symlink() or destination.exists() and destination.read_bytes() != data:
            raise ValueError(f"Existing public artifact differs: {name}")
    output.mkdir(parents=True, exist_ok=True)
    for name, data in payloads.items():
        destination = output / name
        if not destination.exists():
            with destination.open("xb") as stream:
                stream.write(data)
    return sorted(payloads)


def export_study(source: Path, output: Path) -> dict:
    source, output = Path(source).resolve(), Path(output)
    if output.is_symlink():
        raise ValueError("Refusing symlink output directory")
    output = output.resolve()
    raw_rows, expected, raw_audit, source_hashes = _source_inputs(source)
    rows, specs, planned = _public_rows(raw_rows, expected["runs"])
    configs = _public_configs(expected["batch_configs"])
    costs, total, by_arm = _cost_table(source, planned, raw_audit)
    audit = _public_audit(raw_audit, raw_rows, rows, total, by_arm)
    provenance = _public_provenance(expected["batch_configs"], source_hashes, rows, audit)
    process = _public_process_summary(read_json(source / "process-summary.json"))
    payloads = {
        "combined-results.json": json_bytes(rows),
        "combined-expected.json": json_bytes({"runs": specs, "batch_configs": configs}),
        "data-audit.json": json_bytes(audit),
        "protocol-provenance.json": json_bytes(provenance),
        "process-summary.json": json_bytes(process),
    }
    for name in ("analysis_original_5.json", "analysis_all_8.json"):
        analysis = read_json(source / name)
        public = {field: analysis[field] for field in ANALYSIS_FIELDS if field in analysis}
        if public.get("complete") is not True or public.get("blockers"):
            raise ValueError("Refusing incomplete source analysis")
        payloads[name] = json_bytes(public)
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow([*IDENTITY, "all_attempt_accounted_usd"])
    for key, amount in sorted(costs.items()):
        writer.writerow([*key, str(amount)])
    payloads["all-attempt-costs.csv"] = stream.getvalue().encode("utf-8")
    files = _write_export(output, payloads)
    return {"selected_runs": len(rows), "all_attempt_accounted_usd": str(total), "files": files}


def verify_export(directory: Path) -> dict:
    """Verify declared public input hashes without writing or following escapes."""
    directory = Path(directory)
    if directory.is_symlink():
        raise ValueError("Refusing symlink verification directory")
    directory = directory.resolve()
    manifest_path = directory / "SHA256SUMS.json"
    if manifest_path.is_symlink():
        raise ValueError("Refusing symlink checksum manifest")
    manifest = read_json(manifest_path)
    if (
        not isinstance(manifest, dict)
        or manifest.get("schema_version", 1) != 1
        or manifest.get("algorithm") != "sha256"
        or not isinstance(manifest.get("files"), dict)
        or not manifest["files"]
    ):
        raise ValueError("Invalid checksum-manifest schema")
    checked = 0
    for name, expected in manifest["files"].items():
        if not isinstance(name, str) or not name or "\\" in name or ":" in name or "\x00" in name:
            raise ValueError("Unsafe checksum member path")
        relative = PurePosixPath(name)
        if (
            relative.is_absolute()
            or ".." in relative.parts
            or relative.as_posix() != name
            or name in {".", "SHA256SUMS.json"}
        ):
            raise ValueError("Unsafe checksum member path")
        target = directory.joinpath(*relative.parts)
        if (
            target.is_symlink()
            or not target.resolve().is_relative_to(directory)
            or not target.is_file()
        ):
            raise ValueError("Missing checksum member or path escape")
        if hashlib.sha256(target.read_bytes()).hexdigest() != validate_sha256(expected):
            raise ValueError(f"Checksum digest differs: {name}")
        checked += 1
    return {"verified_files": checked, "algorithm": "sha256"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--verify", type=Path, help="Read-only verification of the public SHA256SUMS.json"
    )
    args = parser.parse_args()
    if args.verify:
        if args.input or args.output:
            parser.error("--verify cannot be combined with --input or --output")
        result = verify_export(args.verify)
    else:
        if not args.input or not args.output:
            parser.error("Export requires both --input and --output")
        result = export_study(args.input, args.output)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
