"""Model-only Responses API transport with conservative shared spend control.

No credentials are read from files. The ledger accounts for all in-flight
requests and retains their full reservation after ambiguous failures. Use one
ledger directory for the entire calibration, including every worker/process.
"""

from contextlib import contextmanager
from dataclasses import asdict, dataclass, field
from decimal import Decimal
import json
import os
from pathlib import Path
import re
import time
from typing import Mapping, Sequence
import urllib.error
import urllib.request
import uuid

from experiments.model_catalog import FrozenPrice, model_ids


class BudgetExceeded(RuntimeError):
    pass


class APIError(RuntimeError):
    pass


def _immutable_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False)
        stream.write("\n")


class SpendLedger:
    """File-locked reservations shared across threads and local processes."""

    def __init__(
        self,
        directory: Path | str,
        total_limit_usd: str = "15.00",
        per_run_limit_usd: str = "0.28",
        lock_timeout_seconds: float = 30,
    ):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self.total_limit = Decimal(total_limit_usd)
        self.per_run_limit = Decimal(per_run_limit_usd)
        self.lock_timeout = lock_timeout_seconds
        if self.total_limit <= 0 or self.per_run_limit <= 0:
            raise ValueError("Spend caps must be positive")
        with self._locked():
            state = self._read()
            limits = {"total": str(self.total_limit), "per_run": str(self.per_run_limit)}
            if "limits" in state and state["limits"] != limits:
                raise ValueError("Existing ledger has different spend caps")
            state["limits"] = limits
            self._write(state)

    @contextmanager
    def _locked(self):
        target = self.directory / "ledger.lock"
        deadline = time.monotonic() + self.lock_timeout
        while True:
            try:
                descriptor = os.open(target, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
                os.write(descriptor, str(os.getpid()).encode("ascii"))
                os.close(descriptor)
                break
            except (FileExistsError, PermissionError):
                if time.monotonic() >= deadline:
                    raise TimeoutError(
                        "Ledger lock held; inspect its owner before removing a stale lock"
                    )
                time.sleep(0.01)
        try:
            yield
        finally:
            target.unlink()

    def _read(self) -> dict:
        path = self.directory / "ledger.json"
        return (
            json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"reservations": {}}
        )

    def _write(self, state: dict) -> None:
        temporary = self.directory / ("ledger-" + uuid.uuid4().hex + ".tmp")
        with temporary.open("x", encoding="utf-8") as stream:
            json.dump(state, stream, indent=2)
            stream.flush()
            os.fsync(stream.fileno())
        temporary.replace(self.directory / "ledger.json")

    @staticmethod
    def _accounted(row: Mapping) -> Decimal:
        return Decimal(row["reserved"] if row["status"] == "pending" else row["charged"])

    def reserve(self, run_id: str, amount: Decimal | str) -> str:
        amount = Decimal(amount)
        if not run_id or amount <= 0:
            raise ValueError("A run ID and positive reservation are required")
        with self._locked():
            state = self._read()
            rows = state["reservations"].values()
            total = sum((self._accounted(row) for row in rows), Decimal(0))
            run_total = sum(
                (self._accounted(row) for row in rows if row["run_id"] == run_id), Decimal(0)
            )
            if total + amount > self.total_limit or run_total + amount > self.per_run_limit:
                raise BudgetExceeded(
                    f"Reservation ${amount} exceeds remaining calibration/run budget"
                )
            identity = uuid.uuid4().hex
            row = {
                "run_id": run_id,
                "reserved": str(amount),
                "status": "pending",
                "created_unix": time.time(),
            }
            state["reservations"][identity] = row
            self._write(state)
            _immutable_json(self.directory / "events" / (identity + "-reserve.json"), row)
            return identity

    def settle(
        self, reservation_id: str, actual_cost: Decimal | str, *, is_upper_bound: bool = False
    ) -> None:
        self._finish(
            reservation_id,
            Decimal(actual_cost),
            "usage_upper_bound" if is_upper_bound else "settled",
        )

    def fail(self, reservation_id: str, charge_as_reserved: bool = True) -> None:
        """Retain an upper bound after uncertain delivery; refund a definite rejection."""
        with self._locked():
            row = self._read()["reservations"][reservation_id]
            amount = Decimal(row["reserved"]) if charge_as_reserved else Decimal(0)
        self._finish(reservation_id, amount, "uncertain" if charge_as_reserved else "rejected")

    def _finish(self, identity: str, amount: Decimal, status: str) -> None:
        if amount < 0:
            raise ValueError("Negative charges are invalid")
        with self._locked():
            state = self._read()
            row = state["reservations"][identity]
            if row["status"] != "pending":
                raise ValueError("Reservation already finalized")
            row.update(status=status, charged=str(amount), finished_unix=time.time())
            self._write(state)
            _immutable_json(self.directory / "events" / (identity + "-finish.json"), row)
            if amount > Decimal(row["reserved"]):
                raise BudgetExceeded(
                    "Actual usage exceeded reserved bound; recorded charge and stopped"
                )

    def snapshot(self) -> dict:
        with self._locked():
            state = self._read()
        rows = list(state["reservations"].values())
        return {
            **state,
            "accounted_usd": str(sum((self._accounted(row) for row in rows), Decimal(0))),
            "pending_usd": str(
                sum(
                    (Decimal(row["reserved"]) for row in rows if row["status"] == "pending"),
                    Decimal(0),
                )
            ),
            "uncertain_usd": str(
                sum(
                    (Decimal(row["charged"]) for row in rows if row["status"] == "uncertain"),
                    Decimal(0),
                )
            ),
            "usage_upper_bound_usd": str(
                sum(
                    (
                        Decimal(row["charged"])
                        for row in rows
                        if row["status"] == "usage_upper_bound"
                    ),
                    Decimal(0),
                )
            ),
        }


@dataclass(frozen=True)
class Completion:
    text: str
    requested_model: str
    resolved_model: str
    response_id: str
    usage: dict
    cost_usd: str
    elapsed_seconds: float
    status: str
    incomplete_details: dict | None
    log_directory: str
    service_tier: str | None
    cost_kind: str
    phase: str | None = None
    output_message_count: int = 0
    output_message_phases: tuple[str | None, ...] = ()
    selected_message_count: int = 0
    selection_error: str | None = None
    assistant_messages: list[dict] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


def input_token_upper_bound(messages: Sequence[Mapping]) -> int:
    """Conservative byte bound plus 4K framing allowance for plain-text inputs.

    The adapter supports only role/content text messages, with no tool schemas or
    media. Actual usage is always checked against this reservation after a call.
    """
    return len(json.dumps(list(messages), ensure_ascii=False).encode("utf-8")) + 4096


class OpenAIResponsesBackend:
    def __init__(
        self,
        *,
        model: str,
        price: FrozenPrice,
        ledger: SpendLedger,
        log_dir: Path | str,
        max_output_tokens: int,
        reasoning_effort: str | None = None,
        timeout_seconds: float = 120,
        max_retries: int = 2,
        api_key: str | None = None,
        base_url: str = "https://api.openai.com/v1",
        deadline_monotonic: float | None = None,
    ):
        self.api_key = api_key if api_key is not None else os.environ.get("OPENAI_API_KEY", "")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is missing from the process environment")
        if price.model != model:
            raise ValueError("Frozen price must match requested model exactly")
        if max_output_tokens < 1 or timeout_seconds <= 0 or max_retries not in (0, 1, 2):
            raise ValueError("Invalid output limit, timeout, or retry count")
        if base_url.rstrip("/") != "https://api.openai.com/v1":
            raise ValueError("This adapter sends credentials only to the official OpenAI API")
        self.model, self.price, self.ledger = model, price, ledger
        self.log_dir, self.max_output_tokens = Path(log_dir), max_output_tokens
        self.reasoning_effort, self.timeout, self.max_retries = (
            reasoning_effort,
            timeout_seconds,
            max_retries,
        )
        self.base_url = base_url.rstrip("/")
        self.deadline_monotonic = deadline_monotonic

    def _clean(self, value: object) -> object:
        encoded = json.dumps(value, ensure_ascii=False).replace(self.api_key, "[REDACTED]")
        encoded = re.sub(r"sk-[A-Za-z0-9_-]+", "[REDACTED]", encoded)
        return json.loads(encoded)

    def _request(
        self,
        method: str,
        path: str,
        payload: dict | None = None,
        *,
        timeout_seconds: float | None = None,
    ) -> dict:
        data = json.dumps(payload).encode("utf-8") if payload is not None else None
        request = urllib.request.Request(
            self.base_url + path,
            data=data,
            method=method,
            headers={"Authorization": "Bearer " + self.api_key, "Content-Type": "application/json"},
        )
        with urllib.request.urlopen(
            request, timeout=self.timeout if timeout_seconds is None else timeout_seconds
        ) as response:
            return json.loads(response.read().decode("utf-8"))

    def _attempt_timeout(self) -> float:
        if self.deadline_monotonic is None:
            return self.timeout
        permitted = min(self.timeout, self.deadline_monotonic - time.monotonic() - 1)
        if permitted <= 1:
            raise BudgetExceeded("Solve-time deadline leaves no time for another API request")
        return permitted

    def list_models(self) -> list[str]:
        """An availability lookup; /models does not advertise reasoning capability."""
        identity = "models-" + uuid.uuid4().hex
        result = self._request("GET", "/models")
        _immutable_json(self.log_dir / (identity + ".json"), self._clean(result))
        return model_ids(result)

    def complete(
        self, messages: Sequence[Mapping], *, run_id: str, max_input_tokens: int | None = None
    ) -> Completion:
        clean_messages = []
        for message in messages:
            if (
                not {"role", "content"} <= set(message)
                or set(message) - {"role", "content", "phase"}
                or message["role"] not in {"system", "developer", "user", "assistant"}
                or not isinstance(message["content"], str)
            ):
                raise ValueError(
                    "Only role/content plain-text messages with optional assistant phase are supported"
                )
            if "phase" in message and (
                message["role"] != "assistant"
                or message["phase"] not in {None, "commentary", "final_answer"}
            ):
                raise ValueError("phase is only supported on assistant messages")
            clean_messages.append(dict(message))
        bound = input_token_upper_bound(clean_messages)
        if max_input_tokens is not None and max_input_tokens < bound:
            raise ValueError("max_input_tokens is below the conservative request bound")
        bound = max_input_tokens if max_input_tokens is not None else bound
        if bound > 272_000:
            raise ValueError(
                "Input bound exceeds 272000 tokens; long-context pricing is outside this frozen calibration"
            )
        maximum = self.price.maximum_cost(bound, self.max_output_tokens)
        payload = {
            "model": self.model,
            "input": clean_messages,
            "max_output_tokens": self.max_output_tokens,
            "store": False,
            "tools": [],
            "service_tier": "default",
        }
        if self.reasoning_effort is not None:
            payload["reasoning"] = {"effort": self.reasoning_effort}
        call_dir = self.log_dir / ("call-" + uuid.uuid4().hex)
        _immutable_json(
            call_dir / "request.json",
            self._clean(
                {
                    "payload": payload,
                    "run_id": run_id,
                    "input_token_upper_bound": bound,
                    "maximum_cost_usd": str(maximum),
                    "price": asdict(self.price),
                    "timeout_seconds": self.timeout,
                    "max_retries": self.max_retries,
                }
            ),
        )
        call_started = time.monotonic()
        for attempt in range(self.max_retries + 1):
            self._attempt_timeout()
            reservation = self.ledger.reserve(run_id, maximum)
            try:
                attempt_timeout = self._attempt_timeout()
            except BudgetExceeded:
                self.ledger.fail(reservation, charge_as_reserved=False)
                raise
            started = time.monotonic()
            _immutable_json(
                call_dir / f"attempt-{attempt:02d}-start.json",
                {
                    "reservation_id": reservation,
                    "timeout_seconds": attempt_timeout,
                    "deadline_monotonic": self.deadline_monotonic,
                },
            )
            try:
                result = self._request(
                    "POST", "/responses", payload, timeout_seconds=attempt_timeout
                )
            except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as error:
                code = error.code if isinstance(error, urllib.error.HTTPError) else None
                response_error = None
                if isinstance(error, urllib.error.HTTPError):
                    try:
                        response_error = error.read(65536).decode("utf-8", errors="replace")
                    finally:
                        error.close()
                definitely_rejected = (
                    code is not None and 400 <= code < 500 and code not in {408, 409}
                )
                self.ledger.fail(reservation, charge_as_reserved=not definitely_rejected)
                _immutable_json(
                    call_dir / f"attempt-{attempt:02d}-error.json",
                    self._clean(
                        {
                            "type": type(error).__name__,
                            "http_status": code,
                            "message": str(error),
                            "response_error": response_error,
                            "elapsed_seconds": time.monotonic() - started,
                            "reservation_id": reservation,
                            "accounting": "refunded_rejection"
                            if definitely_rejected
                            else "reserved_upper_bound_retained",
                        }
                    ),
                )
                retryable = code in {408, 409, 429, 500, 502, 503, 504} or code is None
                if not retryable or attempt == self.max_retries:
                    raise APIError(
                        f"Responses request failed ({type(error).__name__}, HTTP {code}); see {call_dir}"
                    ) from None
                delay = min(2**attempt, 4)
                if self.deadline_monotonic is not None:
                    available = self.deadline_monotonic - time.monotonic() - 2
                    if available <= 0:
                        raise BudgetExceeded(
                            "Solve-time deadline exhausted after API failure"
                        ) from None
                    delay = min(delay, available)
                time.sleep(delay)
                continue
            _immutable_json(call_dir / f"attempt-{attempt:02d}-response.json", self._clean(result))
            try:
                usage = result.get("usage") or {}
                actual, cost_kind = self.price.accounted_cost(usage)
            except (ValueError, TypeError, ArithmeticError) as error:
                self.ledger.fail(reservation, charge_as_reserved=True)
                raise APIError(
                    f"Cannot establish exact cost; reservation retained: {error}"
                ) from None
            self.ledger.settle(reservation, actual, is_upper_bound=cost_kind != "usage_derived")
            if usage["input_tokens"] > bound or usage["output_tokens"] > self.max_output_tokens:
                raise APIError(
                    "Provider token usage exceeded the reserved token bound; stop calibration"
                )
            output = result.get("output", [])
            if any(item.get("type") not in {"message", "reasoning"} for item in output):
                raise APIError(
                    "Native tool or unexpected output item returned by model-only backend"
                )
            messages_out = [item for item in output if item.get("type") == "message"]
            phases = tuple(item.get("phase") for item in messages_out)
            selected = messages_out
            phase = None
            selection_error = None
            if any(value is not None for value in phases):
                finals = [item for item in messages_out if item.get("phase") == "final_answer"]
                if any(value not in {None, "commentary", "final_answer"} for value in phases):
                    selected = []
                    selection_error = "Response contained an unknown assistant message phase."
                elif len(finals) == 1:
                    selected = finals
                    phase = "final_answer"
                else:
                    selected = []
                    selection_error = (
                        "Response contained multiple final_answer messages; selection is ambiguous."
                        if finals
                        else "Response contained commentary but no final_answer message."
                    )
            text = "\n".join(
                part.get("text", part.get("refusal", ""))
                for item in selected
                for part in item.get("content", [])
                if part.get("type") in {"output_text", "refusal"}
            )
            assistant_messages = [
                {
                    "role": "assistant",
                    "phase": item.get("phase"),
                    "text": "\n".join(
                        part.get("text", part.get("refusal", ""))
                        for part in item.get("content", [])
                        if part.get("type") in {"output_text", "refusal"}
                    ),
                }
                for item in messages_out
            ]
            if not isinstance(result.get("model"), str) or not isinstance(result.get("id"), str):
                raise APIError("Response omitted resolved model or response ID")
            completion = Completion(
                text,
                self.model,
                result["model"],
                result["id"],
                usage,
                str(actual),
                time.monotonic() - call_started,
                result.get("status", "unknown"),
                result.get("incomplete_details"),
                str(call_dir),
                result.get("service_tier"),
                cost_kind,
                phase,
                len(messages_out),
                phases,
                len(selected),
                selection_error,
                assistant_messages,
            )
            _immutable_json(call_dir / "completion.json", self._clean(completion.to_dict()))
            return completion
        raise AssertionError("Unreachable retry state")


class MiniAPIModel:
    """Execute the first complete proposed shell command, then await observation.

    Responses can emit several assistant messages before the transport returns.
    Their later commands have not seen tool feedback and must not enter replayed
    context as if executed. General backend.text remains final-answer text.
    """

    def __init__(self, backend: OpenAIResponsesBackend, run_id: str):
        self.backend, self.run_id = backend, run_id
        self.call_count = 0
        self.last_usage = {}

    def query(self, messages: list[dict], **kwargs) -> dict:
        from minisweagent.exceptions import FormatError

        plain = []
        for row in messages:
            message = {"role": row["role"], "content": row.get("content", "")}
            phase = row.get("phase", (row.get("extra") or {}).get("phase"))
            if row["role"] == "assistant" and phase is not None:
                message["phase"] = phase
            plain.append(message)
        completion = self.backend.complete(plain, run_id=self.run_id)
        self.call_count += 1
        self.last_usage = completion.usage
        proposed = completion.assistant_messages or [
            {"role": "assistant", "phase": completion.phase, "text": completion.text}
        ]
        pattern = re.compile(r"```(?:mswea_bash_command|bash)\s*\n(.*?)\n```", re.DOTALL)
        commands = [
            (index, source, match)
            for index, source in enumerate(proposed)
            for match in pattern.finditer(source["text"])
        ]
        chosen = commands[0] if commands else None
        content = chosen[1]["text"][: chosen[2].end()] if chosen else ""
        chosen_phase = chosen[1].get("phase") if chosen else None
        later_ignored = max(0, len(commands) - 1)
        extra = {
            "cost": float(completion.cost_usd),
            "cost_kind": completion.cost_kind,
            "usage": completion.usage,
            "timestamp": time.time(),
            "requested_model": completion.requested_model,
            "resolved_model": completion.resolved_model,
            "response_id": completion.response_id,
            "service_tier": completion.service_tier,
            "api_status": completion.status,
            "incomplete_details": completion.incomplete_details,
            "log_directory": completion.log_directory,
            "native_tools_enabled": False,
            "phase": chosen_phase,
            "output_message_count": completion.output_message_count,
            "output_message_phases": list(completion.output_message_phases),
            "selected_message_count": 1 if chosen else 0,
            "selection_error": None if chosen else "No complete command block was returned.",
            "final_text_selection_error": completion.selection_error,
            "protocol": "first_complete_command",
            "proposed_command_count": len(commands),
            "later_commands_ignored": later_ignored,
            "selected_output_message_index": chosen[0] if chosen else None,
        }
        assistant = {"role": "assistant", "content": content, "extra": extra}
        if chosen_phase is not None:
            assistant["phase"] = chosen_phase
        if chosen is None:
            reason = "No fully closed mswea_bash_command or bash command block was returned."
            raise FormatError(
                assistant,
                {
                    "role": "user",
                    "content": "NO COMMANDS EXECUTED: the previous response was rejected. "
                    + reason
                    + " Return exactly one mswea_bash_command code block containing the command to execute now. Do not assume previous code was written or checks ran. To finish, run echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT.",
                },
            )
        extra["actions"] = [{"command": chosen[2].group(1)}]
        return assistant

    def format_message(self, **kwargs) -> dict:
        return kwargs

    def format_observation_messages(
        self, message: dict, outputs: list[dict], template_vars: dict | None = None
    ) -> list[dict]:
        notice = (
            "Only the first proposed command was executed; later proposals were discarded.\n"
            if (message.get("extra") or {}).get("later_commands_ignored", 0)
            else ""
        )
        return [
            {
                "role": "user",
                "content": notice + json.dumps(output, ensure_ascii=False)[: 24000 - len(notice)],
            }
            for output in outputs
        ]

    def get_template_vars(self, **kwargs) -> dict:
        return {
            "model_name": self.backend.model,
            "reasoning_effort": self.backend.reasoning_effort,
            "max_output_tokens": self.backend.max_output_tokens,
        }

    def serialize(self) -> dict:
        return {
            "info": {
                "config": {
                    "model": self.get_template_vars(),
                    "model_type": "experiments.api_backend.MiniAPIModel",
                },
                "model_backend": "openai_responses_no_native_tools",
                "action_protocol": "first_complete_command",
                "run_id": self.run_id,
                "price": asdict(self.backend.price),
            }
        }
