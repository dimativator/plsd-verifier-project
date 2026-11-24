"""Read host action logs and summarize observed verifier process evidence.

No commands or agent code are executed. Only the named host result/action logs
are read; model requests, workspace files, environment settings and credentials
are not read. Markers are observations in captured output, not authenticated
audit events: an agent could print a matching marker itself.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shlex

START = "PLINSE_VERIFY_START "
END = "PLINSE_VERIFY_END "
HASH = re.compile(r"[0-9a-f]{64}")
GUIDE = r"(?:/opt/plinse/)?CROSSHAIR_GUIDE\.txt"
LIMITATION = (
    "Host-captured stdout/stderr markers are observed text, not authenticated proof of tool execution; "
    "an agent could echo them. Guide-read commands do not prove the guide was read or understood. "
    "Source hashes describe main.py at action boundaries; edits within an action cannot be ordered "
    "relative to feedback. Later edits are temporal descriptions, not evidence that feedback caused them. "
    "A reported counterexample is not independently reproduced here, and confirmed checked contracts "
    "do not establish benchmark correctness or exclude vacuous/narrow contracts."
    " Direct CLI detections are anchored shell-command observations, not proof that a conditional branch "
    "executed. Here-document bodies and quoted nested scripts are not searched for CLI calls. "
    "Corroborating diagnostics are action-scoped and may not be assigned among multiple commands."
)


def shell_segments(command: str) -> list[dict]:
    """Conservative shell token scan, excluding here-document/quoted script bodies."""
    segments, heredocs = [], []
    accumulated = ""
    first_line = 1
    for line_number, raw in enumerate(command.splitlines(), 1):
        if heredocs:
            delimiter, strip_tabs = heredocs[0]
            if (raw.lstrip("\t") if strip_tabs else raw).rstrip("\r") == delimiter:
                heredocs.pop(0)
            continue
        if not accumulated:
            first_line = line_number
        accumulated += raw + "\n"
        try:
            lexer = shlex.shlex(accumulated, posix=True, punctuation_chars=";&|<>")
            lexer.whitespace_split = True
            tokens = list(lexer)
        except ValueError:
            # Continue a multiline quoted argument; do not treat its contents as
            # a new anchored shell command.
            continue
        for index, token in enumerate(tokens[:-1]):
            if token == "<<":
                delimiter = tokens[index + 1]
                strip_tabs = delimiter.startswith("-")
                if delimiter == "-" and index + 2 < len(tokens):
                    delimiter = tokens[index + 2]
                elif strip_tabs:
                    delimiter = delimiter[1:]
                heredocs.append((delimiter, strip_tabs))
        current = []
        for token in tokens + [";"]:
            if token and all(char in ";&|" for char in token):
                if current:
                    segments.append(
                        {
                            "shell_line_start": first_line,
                            "shell_line_end": line_number,
                            "argv": current,
                        }
                    )
                current = []
            else:
                current.append(token)
        accumulated = ""
    return segments


def command_argv(tokens: list[str]) -> list[str]:
    """Remove common shell control/prefix words without interpreting branches."""
    tokens = list(tokens)
    for _ in range(6):
        while tokens and (
            tokens[0] in {"then", "do", "else", "if", "elif", "while", "until", "!"}
            or re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*=.*", tokens[0], re.S)
        ):
            tokens.pop(0)
        if not tokens:
            return []
        name = tokens[0].rsplit("/", 1)[-1]
        if name in {"command", "exec", "env", "time", "timeout"}:
            tokens.pop(0)
            while tokens and tokens[0].startswith("-"):
                option = tokens.pop(0)
                if name == "env" and option in {"-u", "--unset"} and tokens:
                    tokens.pop(0)
            if name == "timeout" and tokens and re.fullmatch(r"[0-9.]+[smhd]?", tokens[0]):
                tokens.pop(0)
            continue
        return tokens
    return tokens


def direct_crosshair_commands(command: str) -> list[dict]:
    found = []
    for segment in shell_segments(command):
        tokens = command_argv(segment["argv"])
        if not tokens:
            continue
        name = tokens[0].rsplit("/", 1)[-1]
        arguments = []
        kind = None
        if name == "crosshair":
            kind, arguments = "crosshair_executable", tokens[1:]
        elif re.fullmatch(r"python(?:[0-9]+(?:\.[0-9]+)*)?", name):
            index = 1
            while index < len(tokens):
                option = tokens[index]
                if option == "-m":
                    module = index + 1
                    if module < len(tokens) and tokens[module] in {
                        "crosshair",
                        "crosshair.__main__",
                    }:
                        kind, arguments = "python_module", tokens[module + 1 :]
                    break
                if option in {"-c", "-"} or not option.startswith("-"):
                    break
                index += 2 if option in {"-W", "-X"} else 1
        # Help/version/installation mentions are not verification attempts.
        if kind and arguments and arguments[0] == "check":
            found.append(
                {
                    **segment,
                    "detection_kind": kind,
                    "check_arguments": arguments[1:],
                    "command_observation": shlex.join(segment["argv"]),
                }
            )
    return found


def corroborating_crosshair_lines(stdout: str, stderr: str) -> list[str]:
    evidence = []
    for line in (stdout + "\n" + stderr).splitlines():
        if re.search(
            r"\.pyi?:\d+(?::\d+)?:\s*(?:info|error|warning):|targets found, but contain no checkable functions|no checkable (?:functions|entry[ -]?points)|crosshair(?:\s+\w+)?:\s*error:|no module named ['\"]?crosshair",
            line,
            re.I,
        ):
            evidence.append(line[:1000])
    return evidence[:8]


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def guide_read_match(command: str) -> str | None:
    if not re.search(GUIDE, command):
        return None
    for segment in shell_segments(command):
        tokens = command_argv(segment["argv"])
        if not tokens:
            continue
        name = tokens[0].rsplit("/", 1)[-1]
        if name in {
            "cat",
            "head",
            "tail",
            "sed",
            "awk",
            "less",
            "more",
            "bat",
            "rg",
            "grep",
        } and any(re.search(GUIDE, token) for token in tokens[1:]):
            return "shell_reader_and_guide_path"
        if re.fullmatch(r"python(?:[0-9]+(?:\.[0-9]+)*)?", name) and "-c" in tokens:
            if re.search(
                rf"(?:Path|open)\s*\([^\n]*{GUIDE}[^\n]*(?:read_text|read_bytes|\.read\s*\()",
                " ".join(tokens),
            ):
                return "python_read_expression_and_guide_path"
    return None


def diagnostics(stdout: str, stderr: str, *, returncode=None, timed_out=False) -> dict:
    evidence: dict[str, list[str]] = defaultdict(list)
    for line in (stdout + "\n" + stderr).splitlines():
        text = line.strip()
        if not text or text.startswith((START, END)):
            continue
        low = text.lower()
        if "no counterexample found is not proof of task correctness" in low:
            continue
        category = None
        if re.search(r"\bfalse when(?:\s+calling)?\b", low) or re.search(
            r"\b(?:[a-z_]\w*(?:error|exception)|exception)\b.*\bwhen calling\b", low
        ):
            category = "counterexample_reported"
        elif re.search(r"\bconfirmed over all paths\b|\binfo:\s*confirmed[.!]", low):
            category = "confirmed_checked_contracts_reported"
        elif re.search(
            r"no checkable functions|no (?:checkable )?entry[ -]?points|not checking any|unsupported|cannot (?:analy[sz]e|check)|unable to (?:analy[sz]e|check)",
            low,
        ):
            category = "unsupported_or_no_entrypoints_reported"
        elif re.search(r"verifier timed out|timed? out|time limit exceeded", low):
            category = "timeout_reported"
        elif re.search(
            r"traceback \(most recent call last\)|crosshairinternal|crosshairerror|modulenotfounderror|importerror|syntaxerror|internal error|backend error|crosshair(?:\s+\w+)?:\s*error:|no module named ['\"]?crosshair",
            low,
        ):
            category = "backend_or_loading_error_reported"
        elif re.search(
            r"\bnot confirmed\b|cannot confirm|could not confirm|unable to confirm", low
        ):
            category = "inconclusive_reported"
        if category and len(evidence[category]) < 8:
            evidence[category].append(text[:1000])
    if timed_out or returncode == 124:
        evidence.setdefault("timeout_reported", []).append(
            "Captured action timeout or wrapper returncode 124."
        )
    if not evidence:
        category = (
            "no_explicit_diagnostic_observed"
            if returncode in (None, 0)
            else "unclassified_nonzero_return"
        )
        evidence[category] = []
    return {"categories": sorted(evidence), "evidence": dict(evidence)}


def parse_wrapper_calls(action: dict, line_number: int) -> tuple[list[dict], list[dict]]:
    result = action.get("result", {})
    stdout, stderr = result.get("stdout", ""), result.get("stderr", "")
    lines = stdout.splitlines()
    calls, anomalies = [], []
    current = None
    for index, line in enumerate(lines):
        kind = "start" if line.startswith(START) else "end" if line.startswith(END) else None
        if not kind:
            continue
        prefix = START if kind == "start" else END
        try:
            payload = json.loads(line[len(prefix) :])
            if not isinstance(payload, dict):
                raise ValueError("marker payload is not an object")
            if kind == "start" and (
                not isinstance(payload.get("target"), str)
                or not HASH.fullmatch(str(payload.get("source_sha256", "")))
            ):
                raise ValueError("START requires target and 64-character hexadecimal source hash")
            if kind == "end" and not isinstance(payload.get("returncode"), int):
                raise ValueError("END requires integer returncode")
        except ValueError as error:
            anomalies.append(
                {
                    "action_line": line_number,
                    "stdout_line": index + 1,
                    "kind": "malformed_" + kind,
                    "error": str(error),
                }
            )
            continue
        if kind == "start":
            if current is not None:
                current["stdout_end_line"] = index
                current["marker_pair_complete"] = False
                current["_end"] = index
                calls.append(current)
            current = {
                "action_line": line_number,
                "stdout_start_line": index + 1,
                "wrapper_start": payload,
                "_start": index,
            }
        elif current is None:
            anomalies.append(
                {"action_line": line_number, "stdout_line": index + 1, "kind": "end_without_start"}
            )
        else:
            current.update(
                {
                    "wrapper_end": payload,
                    "stdout_end_line": index + 1,
                    "marker_pair_complete": True,
                    "_end": index + 1,
                }
            )
            calls.append(current)
            current = None
    if current is not None:
        current.update(
            {"stdout_end_line": len(lines), "marker_pair_complete": False, "_end": len(lines)}
        )
        calls.append(current)
    for number, call in enumerate(calls, 1):
        text = "\n".join(lines[call.pop("_start") : call.pop("_end")])
        end = call.get("wrapper_end", {})
        # stderr has no ordering relative to separate stdout wrapper segments.
        # Attribute stderr to a call only when the action has one observed call.
        attributable_stderr = stderr if len(calls) == 1 else ""
        call.update(
            {
                "call_within_action": number,
                "diagnostics": diagnostics(
                    text,
                    attributable_stderr,
                    returncode=end.get("returncode"),
                    timed_out=bool(result.get("timed_out") and not call["marker_pair_complete"]),
                ),
                "stdout_excerpt": text[:8000],
                "stdout_excerpt_truncated": len(text) > 8000,
                "stderr_excerpt": attributable_stderr[:4000],
                "stderr_attribution": "single-wrapper action scope"
                if len(calls) == 1
                else "not attributed: multiple wrappers share one stderr stream",
                "source_before_action": action.get("source_before"),
                "source_after_action": action.get("source_after"),
                "source_changed_within_action": action.get("source_before")
                != action.get("source_after"),
                "action_returncode": result.get("returncode"),
                "action_timed_out": result.get("timed_out", False),
                "action_output_truncated": result.get("output_truncated", False),
            }
        )
        call["action_scope_diagnostics"] = diagnostics(
            stdout,
            stderr,
            returncode=result.get("returncode"),
            timed_out=result.get("timed_out", False),
        )
        target = call["wrapper_start"]["target"]
        main_target = target in {"main.py", "./main.py", "/work/main.py"}
        call["wrapper_target_is_main_py"] = main_target
        call["wrapper_hash_matches_main_before_action"] = (
            call["wrapper_start"]["source_sha256"] == action.get("source_before")
            if main_target
            else None
        )
        call["wrapper_hash_matches_main_after_action"] = (
            call["wrapper_start"]["source_sha256"] == action.get("source_after")
            if main_target
            else None
        )
    return calls, anomalies


def audit_run(result_path: Path, batch_root: Path) -> dict:
    result = load_json(result_path)
    required = {"model", "task_id", "condition", "repetition"}
    if not required <= result.keys():
        raise ValueError("Result is missing run identity fields")
    directory = result_path.parent
    actions_path = directory / "actions.jsonl"
    actions, parse_errors = [], []
    if actions_path.is_file() and not actions_path.is_symlink():
        for line_number, line in enumerate(
            actions_path.read_text(encoding="utf-8").splitlines(), 1
        ):
            if not line.strip():
                continue
            try:
                action = json.loads(line)
                if not isinstance(action, dict) or not isinstance(action.get("result"), dict):
                    raise ValueError("action/result is not an object")
                actions.append((line_number, action))
            except ValueError as error:
                parse_errors.append({"line": line_number, "error": str(error)})
    guide_commands, calls, direct_commands, anomalies = [], [], [], []
    changed_lines = [
        number
        for number, action in actions
        if action.get("source_before") != action.get("source_after")
    ]
    chain_discontinuities = []
    for index, (line_number, action) in enumerate(actions):
        command = str(action.get("command", ""))
        guide = guide_read_match(command)
        if guide:
            guide_commands.append(
                {
                    "action_line": line_number,
                    "match_method": guide,
                    "command_excerpt": command[:2000],
                    "action_returncode": action["result"].get("returncode"),
                    "action_output_truncated": action["result"].get("output_truncated", False),
                }
            )
        observations, errors = parse_wrapper_calls(action, line_number)
        direct_observations = direct_crosshair_commands(command)
        action_result = action["result"]
        action_diagnostics = diagnostics(
            action_result.get("stdout", ""),
            action_result.get("stderr", ""),
            returncode=action_result.get("returncode"),
            timed_out=action_result.get("timed_out", False),
        )
        corroboration = corroborating_crosshair_lines(
            action_result.get("stdout", ""), action_result.get("stderr", "")
        )
        for call in observations:
            later = [number for number in changed_lines if number > line_number]
            call.update(
                {
                    "evidence_kind": "wrapper_stdout_marker",
                    "command_excerpt": command[:3000],
                    "later_source_change_action_lines": later,
                    "source_changed_in_later_action": bool(later),
                    "final_main_hash_differs_from_wrapper_start": result.get("submission_sha256")
                    != call["wrapper_start"]["source_sha256"]
                    if call["wrapper_target_is_main_py"] and result.get("submission_sha256")
                    else None,
                }
            )
        calls.extend(observations)
        for number, direct in enumerate(direct_observations, 1):
            later = [number for number in changed_lines if number > line_number]
            direct_commands.append(
                {
                    **direct,
                    "evidence_kind": "direct_crosshair_cli_command",
                    "action_line": line_number,
                    "direct_command_within_action": number,
                    "command_excerpt": command[:3000],
                    "diagnostics": action_diagnostics,
                    "action_scope_diagnostics": action_diagnostics,
                    "diagnostic_scope": "whole action output; this is not per-command attribution",
                    "corroborating_crosshair_diagnostic_observed": bool(corroboration),
                    "corroborating_diagnostic_lines": corroboration,
                    "source_before_action": action.get("source_before"),
                    "source_after_action": action.get("source_after"),
                    "source_changed_within_action": action.get("source_before")
                    != action.get("source_after"),
                    "later_source_change_action_lines": later,
                    "source_changed_in_later_action": bool(later),
                    "action_returncode": action_result.get("returncode"),
                    "action_timed_out": action_result.get("timed_out", False),
                    "action_output_truncated": action_result.get("output_truncated", False),
                }
            )
        anomalies.extend(errors)
        if index and actions[index - 1][1].get("source_after") != action.get("source_before"):
            chain_discontinuities.append(line_number)
    categories = Counter(
        category for call in calls for category in call["diagnostics"]["categories"]
    )
    evidence = calls + direct_commands
    counterexample_changes = [
        call
        for call in evidence
        if "counterexample_reported" in call["action_scope_diagnostics"]["categories"]
        and call["source_changed_in_later_action"]
    ]
    return {
        "batch": batch_root.name,
        **{
            key: result.get(key)
            for key in (
                "phase",
                "model",
                "task_id",
                "family_id",
                "rating_band",
                "condition",
                "repetition",
                "valid_run",
                "infrastructure_error",
                "exit_status",
                "hidden_passed",
            )
        },
        "result_path": str(result_path.resolve()),
        "actions_path": str(actions_path.resolve()),
        "result_sha256": file_hash(result_path),
        "actions_sha256": file_hash(actions_path)
        if actions_path.is_file() and not actions_path.is_symlink()
        else None,
        "action_count": len(actions),
        "result_reported_shell_actions": result.get("shell_actions"),
        "guide_read_command_count": len(guide_commands),
        "guide_read_commands": guide_commands,
        "observed_wrapper_start_count": len(calls),
        "observed_complete_wrapper_pair_count": sum(call["marker_pair_complete"] for call in calls),
        "verifier_usage_observed": bool(evidence),
        "wrapper_usage_observed": bool(calls),
        "direct_cli_command_count": len(direct_commands),
        "direct_cli_commands_with_corroborating_diagnostics": sum(
            d["corroborating_crosshair_diagnostic_observed"] for d in direct_commands
        ),
        "verifier_evidence_action_lines": sorted({call["action_line"] for call in evidence}),
        "diagnostic_call_counts": dict(categories),
        "direct_cli_action_scope_diagnostic_counts": dict(
            Counter(
                category
                for call in direct_commands
                for category in call["diagnostics"]["categories"]
            )
        ),
        "source_changed_action_lines": changed_lines,
        "source_change_chain_discontinuity_action_lines": chain_discontinuities,
        "source_changed_after_any_verifier_action": any(
            call["source_changed_in_later_action"] for call in evidence
        ),
        "source_changed_after_counterexample_action": bool(counterexample_changes),
        "initial_main_sha256": actions[0][1].get("source_before") if actions else None,
        "final_action_main_sha256": actions[-1][1].get("source_after") if actions else None,
        "submission_sha256": result.get("submission_sha256"),
        "submission_hash_matches_last_action": result.get("submission_sha256")
        == actions[-1][1].get("source_after")
        if actions and result.get("submission_sha256")
        else None,
        "result_recorded_verify_event_count": sum(
            event.get("event") == "verify_invocation_observed"
            for event in result.get("tool_events", [])
            if isinstance(event, dict)
        ),
        "action_parse_errors": parse_errors,
        "marker_anomalies": anomalies,
        "missing_actions_despite_reported_actions": not actions_path.exists()
        and bool(result.get("shell_actions")),
        "wrapper_calls": calls,
        "direct_crosshair_commands": direct_commands,
    }


def summarize(runs: list[dict]) -> dict:
    return {
        "completed_runs": len(runs),
        "valid_runs": sum(bool(run.get("valid_run")) for run in runs),
        "runs_with_guide_read_command": sum(bool(run["guide_read_command_count"]) for run in runs),
        "guide_read_commands": sum(run["guide_read_command_count"] for run in runs),
        "runs_with_verifier_evidence": sum(run["verifier_usage_observed"] for run in runs),
        "actions_with_verifier_evidence": sum(
            len(run["verifier_evidence_action_lines"]) for run in runs
        ),
        "runs_with_observed_wrapper_start": sum(run["wrapper_usage_observed"] for run in runs),
        "valid_runs_with_observed_wrapper_start": sum(
            bool(run.get("valid_run")) and run["wrapper_usage_observed"] for run in runs
        ),
        "runs_with_direct_cli_command": sum(bool(run["direct_cli_command_count"]) for run in runs),
        "direct_cli_command_observations": sum(run["direct_cli_command_count"] for run in runs),
        "direct_cli_commands_with_corroborating_diagnostics": sum(
            run["direct_cli_commands_with_corroborating_diagnostics"] for run in runs
        ),
        "observed_wrapper_start_markers": sum(run["observed_wrapper_start_count"] for run in runs),
        "complete_wrapper_marker_pairs": sum(
            run["observed_complete_wrapper_pair_count"] for run in runs
        ),
        "diagnostic_call_counts": dict(
            sum((Counter(run["diagnostic_call_counts"]) for run in runs), Counter())
        ),
        "direct_cli_action_scope_diagnostic_counts": dict(
            sum(
                (Counter(run["direct_cli_action_scope_diagnostic_counts"]) for run in runs),
                Counter(),
            )
        ),
        "runs_with_later_source_change_after_verifier_action": sum(
            run["source_changed_after_any_verifier_action"] for run in runs
        ),
        "runs_with_later_source_change_after_counterexample_action": sum(
            run["source_changed_after_counterexample_action"] for run in runs
        ),
        "runs_with_action_parse_errors": sum(bool(run["action_parse_errors"]) for run in runs),
        "runs_with_marker_anomalies": sum(bool(run["marker_anomalies"]) for run in runs),
    }


def trace_selections(runs: list[dict]) -> list[dict]:
    chosen: dict[tuple, dict] = {}
    rules = [
        ("first_wrapper_or_direct_cli_evidence", None),
        ("first_concrete_counterexample_report", "counterexample_reported"),
        ("first_unsupported_or_no_entrypoints_report", "unsupported_or_no_entrypoints_reported"),
    ]
    for rule, category in rules:
        found = False
        for run in runs:
            observations = sorted(
                run["wrapper_calls"] + run["direct_crosshair_commands"],
                key=lambda c: (
                    c["action_line"],
                    c["evidence_kind"],
                    c.get("call_within_action", c.get("direct_command_within_action", 0)),
                ),
            )
            for call in observations:
                call_scope = category is None or category in call["diagnostics"]["categories"]
                action_scope = (
                    category in call["action_scope_diagnostics"]["categories"]
                    if category
                    else False
                )
                if call_scope or action_scope:
                    key = (
                        run["actions_path"],
                        call["action_line"],
                        call["evidence_kind"],
                        call.get("call_within_action", call.get("direct_command_within_action")),
                    )
                    if key not in chosen:
                        chosen[key] = {
                            "selection_rules": [],
                            "batch": run["batch"],
                            **{
                                field: run.get(field)
                                for field in (
                                    "model",
                                    "task_id",
                                    "condition",
                                    "repetition",
                                    "hidden_passed",
                                )
                            },
                            "actions_path": run["actions_path"],
                            "result_path": run["result_path"],
                            **call,
                        }
                    chosen[key]["selection_rules"].append(rule)
                    chosen[key].setdefault("selection_evidence_scope", {})[rule] = (
                        "whole action output for a direct CLI command observation"
                        if call["evidence_kind"] == "direct_crosshair_cli_command"
                        else "wrapper stdout or single-wrapper action stderr"
                        if call_scope
                        else "whole action output; stderr cannot be assigned among its multiple wrappers"
                    )
                    found = True
                    break
            if found:
                break
    return list(chosen.values())


def generate(roots: list[Path]) -> dict:
    runs, errors, expectations = [], [], []
    seen = set()
    for root in sorted((path.resolve() for path in roots), key=str):
        expected_path = root / "expected.json"
        expected = (
            load_json(expected_path).get("runs", [])
            if expected_path.is_file() and not expected_path.is_symlink()
            else []
        )
        completed_keys = set()
        for result_path in sorted(root.glob("*/*/*/rep-*/result.json")):
            resolved = result_path.resolve()
            if resolved in seen:
                continue
            if result_path.is_symlink() or not resolved.is_relative_to(root):
                errors.append(
                    {"path": str(result_path), "error": "symlink or path escape rejected"}
                )
                continue
            seen.add(resolved)
            try:
                run = audit_run(result_path, root)
                runs.append(run)
                completed_keys.add(
                    tuple(
                        run.get(key)
                        for key in ("phase", "model", "task_id", "condition", "repetition")
                    )
                )
            except (OSError, ValueError, TypeError, KeyError) as error:
                errors.append(
                    {"path": str(result_path), "error": f"{type(error).__name__}: {error}"}
                )
        pending = [
            spec
            for spec in expected
            if tuple(
                spec.get(key) for key in ("phase", "model", "task_id", "condition", "repetition")
            )
            not in completed_keys
        ]
        expectations.append(
            {
                "batch": root.name,
                "results_root": str(root),
                "expected_runs": len(expected) if expected else None,
                "completed_results": len(completed_keys),
                "pending_or_missing_expected_runs": pending,
            }
        )
    runs.sort(key=lambda run: run["result_path"])
    groups = defaultdict(list)
    for run in runs:
        groups[(run["model"], run["condition"])].append(run)
    return {
        "schema_version": 2,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "Read-only postprocessing of completed host result records and raw host actions; no agent code or commands executed.",
        "limitations": LIMITATION,
        "count_definitions": "Wrapper START marker counts and direct CLI command counts are separate evidence channels, not a sum of authenticated executions. Run/action usage counts take the union and never double-count a run/action with both channels. Direct CLI diagnostic counts are whole-action observations, possibly shared by multiple commands.",
        "trace_selection_rule": "Lexicographic result-path order, then host action-line order (evidence-kind order breaks same-action ties); first wrapper/direct-CLI evidence, first explicit counterexample, first unsupported/no-entrypoints. Duplicate events merge rules. No hidden-success selection.",
        "expectations": expectations,
        "summary": summarize(runs),
        "by_condition": {
            condition: summarize([run for run in runs if run["condition"] == condition])
            for condition in sorted({run["condition"] for run in runs})
        },
        "by_model_condition": [
            {"model": key[0], "condition": key[1], **summarize(group)}
            for key, group in sorted(groups.items())
        ],
        "trace_selections": trace_selections(runs),
        "read_errors": errors,
        "runs": runs,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--results",
        type=Path,
        nargs="+",
        help="Explicit result roots; phases are never inferred or mixed automatically",
    )
    parser.add_argument(
        "--output", type=Path, default=Path("runs/calibration-20261123/process-audit.json")
    )
    args = parser.parse_args()
    if not args.results:
        parser.error("--results is required")
    report = generate(args.results)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.output.with_suffix(".tmp")
    temporary.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temporary.replace(args.output)
    print(
        json.dumps(
            {
                "output": str(args.output.resolve()),
                "summary": report["summary"],
                "trace_selections": len(report["trace_selections"]),
            }
        )
    )


if __name__ == "__main__":
    main()
