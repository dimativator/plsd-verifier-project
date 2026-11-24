"""Offline checks for transport accounting; no credentials or network needed."""
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal
import io
import json
from pathlib import Path
import tempfile
import types
import unittest
from unittest.mock import patch
import urllib.error

from experiments.api_backend import APIError, BudgetExceeded, MiniAPIModel, OpenAIResponsesBackend, SpendLedger
from experiments.model_catalog import CALIBRATION_PRICES, FrozenPrice, economical_candidates, model_ids


def price(model="test-model"):
    # Deliberately synthetic rates: unit-test fixture, never production pricing.
    return FrozenPrice(model, "1", "0.1", "2", "https://example.test/unit-test-pricing", "2000-01-01")


def response():
    return {"id": "resp-test", "model": "test-model-snapshot", "status": "completed",
            "usage": {"input_tokens": 100, "output_tokens": 20,
                      "input_tokens_details": {"cached_tokens": 10}},
            "output": [{"type": "reasoning"}, {"type": "message", "content": [{"type": "output_text", "text": "answer"}]}]}


class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.directory = Path(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def test_inflight_reservations_cannot_oversubscribe_across_workers(self):
        ledger = SpendLedger(self.directory, "1", "1")

        def reserve(index):
            try:
                # Construct independently as separate worker processes would.
                return SpendLedger(self.directory, "1", "1").reserve(str(index), "0.1")
            except BudgetExceeded:
                return None

        with ThreadPoolExecutor(max_workers=12) as pool:
            ids = list(pool.map(reserve, range(40)))
        self.assertEqual(sum(identity is not None for identity in ids), 10)
        self.assertEqual(Decimal(ledger.snapshot()["pending_usd"]), Decimal("1"))

    def test_settlement_refunds_unused_reservation(self):
        ledger = SpendLedger(self.directory, "1", "0.3")
        identity = ledger.reserve("run-a", "0.3")
        ledger.settle(identity, "0.05")
        ledger.reserve("run-a", "0.25")
        with self.assertRaises(BudgetExceeded):
            ledger.reserve("run-a", "0.01")
        self.assertEqual(Decimal(ledger.snapshot()["accounted_usd"]), Decimal("0.3"))

    def test_uncertain_failure_retains_upper_bound_but_rejection_refunds(self):
        ledger = SpendLedger(self.directory, "1", "1")
        uncertain = ledger.reserve("run-a", "0.4")
        rejected = ledger.reserve("run-a", "0.4")
        ledger.fail(uncertain)
        ledger.fail(rejected, charge_as_reserved=False)
        state = ledger.snapshot()
        self.assertEqual(Decimal(state["uncertain_usd"]), Decimal("0.4"))
        self.assertEqual(Decimal(state["accounted_usd"]), Decimal("0.4"))
        with self.assertRaises(ValueError):
            ledger.settle(uncertain, "0")

    def test_actual_overrun_is_recorded_before_stop(self):
        ledger = SpendLedger(self.directory, "1", "1")
        identity = ledger.reserve("run-a", "0.1")
        with self.assertRaises(BudgetExceeded):
            ledger.settle(identity, "0.2")
        self.assertEqual(Decimal(ledger.snapshot()["accounted_usd"]), Decimal("0.2"))


class BackendTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.ledger = SpendLedger(self.root / "ledger", "1", "1")
        self.backend = OpenAIResponsesBackend(model="test-model", price=price(), ledger=self.ledger,
            log_dir=self.root / "logs", max_output_tokens=100, api_key="sk-unit-test-secret", max_retries=2)

    def tearDown(self):
        self.temporary.cleanup()

    def test_success_records_resolved_model_usage_and_exact_cache_cost(self):
        with patch.object(self.backend, "_request", return_value=response()) as request:
            completion = self.backend.complete([{"role": "user", "content": "hello"}], run_id="screen-a")
        self.assertEqual(completion.text, "answer")
        self.assertEqual(completion.resolved_model, "test-model-snapshot")
        self.assertEqual(Decimal(completion.cost_usd), Decimal("0.000131"))
        self.assertEqual(Decimal(self.ledger.snapshot()["pending_usd"]), Decimal(0))
        sent = request.call_args.args[2]
        self.assertEqual(sent["tools"], [])
        self.assertNotIn("reasoning", sent)
        self.assertFalse(sent["store"])

    def test_reasoning_is_opt_in(self):
        self.backend.reasoning_effort = "low"
        with patch.object(self.backend, "_request", return_value=response()) as request:
            self.backend.complete([{"role": "user", "content": "hello"}], run_id="screen-a")
        self.assertEqual(request.call_args.args[2]["reasoning"], {"effort": "low"})

    def test_timeout_retry_retains_ambiguous_request_reservation(self):
        with patch.object(self.backend, "_request", side_effect=[TimeoutError("timed out"), response()]) as request, patch("experiments.api_backend.time.sleep"):
            completion = self.backend.complete([{"role": "user", "content": "hello"}], run_id="screen-a")
        self.assertEqual(request.call_count, 2)
        state = self.ledger.snapshot()
        self.assertGreater(Decimal(state["uncertain_usd"]), Decimal(0))
        self.assertEqual(Decimal(state["accounted_usd"]), Decimal(state["uncertain_usd"]) + Decimal(completion.cost_usd))

    def test_retry_timeout_shrinks_with_remaining_solve_deadline(self):
        clock = {"now": 100.0}
        timeouts = []
        self.backend.timeout = 30
        self.backend.max_retries = 1
        self.backend.deadline_monotonic = 120

        def request(*args, **kwargs):
            timeouts.append(kwargs["timeout_seconds"])
            if len(timeouts) == 1:
                clock["now"] = 107
                raise TimeoutError("first request disconnected")
            clock["now"] = 109
            return response()

        def sleep(seconds):
            clock["now"] += seconds

        with patch("experiments.api_backend.time.monotonic", side_effect=lambda: clock["now"]), patch("experiments.api_backend.time.sleep", side_effect=sleep), patch.object(self.backend, "_request", side_effect=request):
            self.backend.complete([{"role": "user", "content": "hello"}], run_id="screen-a")
        self.assertEqual(timeouts, [19, 11])
        self.assertGreater(Decimal(self.ledger.snapshot()["uncertain_usd"]), Decimal(0))

    def test_no_retry_request_is_sent_after_deadline(self):
        clock = {"now": 100.0}
        self.backend.deadline_monotonic = 110

        def request(*args, **kwargs):
            clock["now"] = 110
            raise TimeoutError("deadline reached")

        with patch("experiments.api_backend.time.monotonic", side_effect=lambda: clock["now"]), patch.object(self.backend, "_request", side_effect=request) as transport:
            with self.assertRaises(BudgetExceeded):
                self.backend.complete([{"role": "user", "content": "hello"}], run_id="screen-a")
        self.assertEqual(transport.call_count, 1)
        self.assertGreater(Decimal(self.ledger.snapshot()["uncertain_usd"]), Decimal(0))

    def test_expired_deadline_does_not_reserve_or_send(self):
        self.backend.deadline_monotonic = 101
        with patch("experiments.api_backend.time.monotonic", return_value=100), patch.object(self.backend, "_request") as transport:
            with self.assertRaises(BudgetExceeded):
                self.backend.complete([{"role": "user", "content": "hello"}], run_id="screen-a")
        transport.assert_not_called()
        self.assertEqual(self.ledger.snapshot()["reservations"], {})

    def test_deadline_expiring_during_reservation_refunds_unsent_request(self):
        clock = {"now": 100.0}
        self.backend.deadline_monotonic = 110
        original_reserve = self.ledger.reserve

        def reserve(*args, **kwargs):
            identity = original_reserve(*args, **kwargs)
            clock["now"] = 110
            return identity

        with patch("experiments.api_backend.time.monotonic", side_effect=lambda: clock["now"]), patch.object(self.ledger, "reserve", side_effect=reserve), patch.object(self.backend, "_request") as transport:
            with self.assertRaises(BudgetExceeded):
                self.backend.complete([{"role": "user", "content": "hello"}], run_id="screen-a")
        transport.assert_not_called()
        self.assertEqual(Decimal(self.ledger.snapshot()["accounted_usd"]), Decimal(0))

    def test_rate_limit_retry_refunds_rejected_request(self):
        rejected = urllib.error.HTTPError("https://api.openai.com/v1/responses", 429, "rate limit", {}, io.BytesIO())
        with patch.object(self.backend, "_request", side_effect=[rejected, response()]), patch("experiments.api_backend.time.sleep"):
            completion = self.backend.complete([{"role": "user", "content": "hello"}], run_id="screen-a")
        self.assertEqual(Decimal(self.ledger.snapshot()["accounted_usd"]), Decimal(completion.cost_usd))

    def test_retries_are_bounded_and_secrets_never_logged(self):
        with patch.object(self.backend, "_request", side_effect=TimeoutError("sk-unit-test-secret")) as request, patch("experiments.api_backend.time.sleep"):
            with self.assertRaises(APIError):
                self.backend.complete([{"role": "user", "content": "hello"}], run_id="screen-a")
        self.assertEqual(request.call_count, 3)
        saved = "".join(path.read_text(encoding="utf-8") for path in (self.root / "logs").rglob("*.json"))
        self.assertNotIn("sk-unit-test-secret", saved)

    def test_missing_usage_retains_reservation_and_does_not_retry(self):
        result = response()
        del result["usage"]
        with patch.object(self.backend, "_request", return_value=result) as request:
            with self.assertRaises(APIError):
                self.backend.complete([{"role": "user", "content": "hello"}], run_id="screen-a")
        self.assertEqual(request.call_count, 1)
        self.assertGreater(Decimal(self.ledger.snapshot()["uncertain_usd"]), Decimal(0))

    def test_tool_output_is_rejected_after_recording_real_charge(self):
        result = response()
        result["output"] = [{"type": "function_call", "name": "shell"}]
        with patch.object(self.backend, "_request", return_value=result):
            with self.assertRaises(APIError):
                self.backend.complete([{"role": "user", "content": "hello"}], run_id="screen-a")
        self.assertEqual(Decimal(self.ledger.snapshot()["accounted_usd"]), Decimal("0.000131"))

    def test_budget_denial_prevents_network(self):
        self.ledger.reserve("screen-a", "0.999")
        with patch.object(self.backend, "_request") as request:
            with self.assertRaises(BudgetExceeded):
                self.backend.complete([{"role": "user", "content": "hello"}], run_id="screen-a")
        request.assert_not_called()

    def test_low_input_bound_and_price_mismatch_rejected(self):
        with patch.object(self.backend, "_request") as request:
            with self.assertRaises(ValueError):
                self.backend.complete([{"role": "user", "content": "hello"}], run_id="screen-a", max_input_tokens=1)
        request.assert_not_called()
        with self.assertRaises(ValueError):
            OpenAIResponsesBackend(model="other", price=price(), ledger=self.ledger,
                log_dir=self.root / "logs", max_output_tokens=100, api_key="test")

    def test_long_context_is_rejected_before_network(self):
        with patch.object(self.backend, "_request") as request:
            with self.assertRaises(ValueError):
                self.backend.complete([{"role": "user", "content": "hello"}], run_id="screen-a", max_input_tokens=272001)
        request.assert_not_called()

    def test_unreported_cache_writes_are_accounted_as_labelled_upper_bound(self):
        self.backend.price = FrozenPrice("test-model", "1", "0.1", "2", "https://example.test/pricing", "2000-01-01", "1.25")
        with patch.object(self.backend, "_request", return_value=response()) as request:
            completion = self.backend.complete([{"role": "user", "content": "hello"}], run_id="screen-a")
        self.assertEqual(completion.cost_kind, "upper_bound_unreported_cache_writes")
        self.assertEqual(Decimal(completion.cost_usd), Decimal("0.0001535"))
        self.assertEqual(Decimal(self.ledger.snapshot()["usage_upper_bound_usd"]), Decimal(completion.cost_usd))
        self.assertEqual(request.call_args.args[2]["service_tier"], "default")

    def test_mini_adapter_returns_one_shell_action_and_accounting(self):
        result = response()
        result["output"][1]["content"][0]["text"] = "Check.\n```mswea_bash_command\necho hi\n```"
        module = types.ModuleType("minisweagent.exceptions")
        module.FormatError = type("FormatError", (Exception,), {})
        with patch.dict("sys.modules", {"minisweagent.exceptions": module}), patch.object(self.backend, "_request", return_value=result):
            model = MiniAPIModel(self.backend, "agent-a")
            answer = model.query([{"role": "user", "content": "hello", "extra": {"cost": 0}}])
        self.assertEqual(answer["extra"]["actions"], [{"command": "echo hi"}])
        self.assertEqual(model.call_count, 1)
        self.assertGreater(answer["extra"]["cost"], 0)
        self.assertNotIn("api_key", json.dumps(model.serialize()))

    def test_mini_format_failure_still_records_charge(self):
        module = types.ModuleType("minisweagent.exceptions")
        module.FormatError = type("FormatError", (Exception,), {})
        with patch.dict("sys.modules", {"minisweagent.exceptions": module}), patch.object(self.backend, "_request", return_value=response()):
            with self.assertRaises(module.FormatError):
                MiniAPIModel(self.backend, "agent-a").query([{"role": "user", "content": "hello"}])
        self.assertEqual(Decimal(self.ledger.snapshot()["accounted_usd"]), Decimal("0.000131"))

    def test_first_commentary_command_is_selected_and_later_final_is_discarded(self):
        result = response()
        result["output"] = [
            {"type": "message", "phase": "commentary", "content": [{"type": "output_text", "text": "```mswea_bash_command\necho COMMENTARY\n```"}]},
            {"type": "message", "phase": "final_answer", "content": [{"type": "output_text", "text": "```mswea_bash_command\necho FINAL\n```"}]},
        ]
        module = types.ModuleType("minisweagent.exceptions")
        module.FormatError = type("FormatError", (Exception,), {})
        with patch.dict("sys.modules", {"minisweagent.exceptions": module}), patch.object(self.backend, "_request", return_value=result):
            answer = MiniAPIModel(self.backend, "agent-a").query([{"role": "user", "content": "hello"}])
        self.assertEqual(answer["extra"]["actions"], [{"command": "echo COMMENTARY"}])
        self.assertEqual(answer["phase"], "commentary")
        self.assertEqual(answer["extra"]["output_message_count"], 2)
        self.assertEqual(answer["extra"]["output_message_phases"], ["commentary", "final_answer"])
        self.assertEqual(answer["extra"]["selected_message_count"], 1)
        self.assertNotIn("FINAL", answer["content"])
        self.assertEqual(answer["extra"]["later_commands_ignored"], 1)
        self.assertEqual(Decimal(self.ledger.snapshot()["accounted_usd"]), Decimal("0.000131"))

    def test_incomplete_response_with_closed_commentary_command_can_execute_it(self):
        result = response()
        result["status"] = "incomplete"
        result["incomplete_details"] = {"reason": "max_output_tokens"}
        result["output"] = [{"type": "message", "phase": "commentary", "content": [{"type": "output_text", "text": "```bash\necho CLOSED\n```"}]}]
        module = types.ModuleType("minisweagent.exceptions")
        module.FormatError = type("FormatError", (Exception,), {})
        with patch.dict("sys.modules", {"minisweagent.exceptions": module}), patch.object(self.backend, "_request", return_value=result):
            assistant = MiniAPIModel(self.backend, "agent-a").query([{"role": "user", "content": "hello"}])
        self.assertEqual(assistant["extra"]["actions"], [{"command": "echo CLOSED"}])
        self.assertEqual(assistant["extra"]["api_status"], "incomplete")

    def test_unclosed_command_executes_nothing_and_reports_that_explicitly(self):
        result = response()
        result["status"] = "incomplete"
        result["output"] = [{"type": "message", "phase": "commentary", "content": [{"type": "output_text", "text": "```bash\necho NOT_CLOSED\n"}]}]
        module = types.ModuleType("minisweagent.exceptions")
        module.FormatError = type("FormatError", (Exception,), {})
        with patch.dict("sys.modules", {"minisweagent.exceptions": module}), patch.object(self.backend, "_request", return_value=result):
            with self.assertRaises(module.FormatError) as rejected:
                MiniAPIModel(self.backend, "agent-a").query([{"role": "user", "content": "hello"}])
        assistant, observation = rejected.exception.args
        self.assertNotIn("actions", assistant["extra"])
        self.assertIn("NO COMMANDS EXECUTED", observation["content"])

    def test_multiple_final_messages_are_rejected_as_ambiguous(self):
        result = response()
        result["output"] = [{"type": "message", "phase": "final_answer", "content": [{"type": "output_text", "text": "```bash\necho hi\n```"}]}] * 2
        with patch.object(self.backend, "_request", return_value=result):
            completion = self.backend.complete([{"role": "user", "content": "hello"}], run_id="screen-a")
        self.assertEqual(completion.text, "")
        self.assertEqual(completion.selected_message_count, 0)
        self.assertIn("ambiguous", completion.selection_error)

    def test_assistant_phase_is_preserved_in_replayed_api_input(self):
        module = types.ModuleType("minisweagent.exceptions")
        module.FormatError = type("FormatError", (Exception,), {})
        result = response()
        result["output"][1]["content"][0]["text"] = "```bash\necho hi\n```"
        messages = [{"role": "user", "content": "task"},
                    {"role": "assistant", "content": "```bash\necho previous\n```", "phase": "final_answer"},
                    {"role": "user", "content": "observation", "extra": {"phase": "commentary"}}]
        with patch.dict("sys.modules", {"minisweagent.exceptions": module}), patch.object(self.backend, "_request", return_value=result) as request:
            MiniAPIModel(self.backend, "agent-a").query(messages)
        sent = request.call_args.args[2]["input"]
        self.assertEqual(sent[1]["phase"], "final_answer")
        self.assertNotIn("phase", sent[2])

    def test_first_write_then_actual_observation_replays_no_phantom_test_commands(self):
        first = response()
        first["output"] = [
            {"type": "message", "phase": "commentary", "content": [{"type": "output_text", "text": "Inspecting the task first."}]},
            {"type": "message", "phase": "commentary", "content": [{"type": "output_text", "text": "Write now.\n```bash\nprintf 'print(1)' > main.py\n```\nThis unexecuted trailing plan is discarded."}]},
            {"type": "message", "phase": "final_answer", "content": [{"type": "output_text", "text": "```bash\nrun_tests PHANTOM\n```"}]},
        ]
        second = response()
        second["output"] = [{"type": "message", "phase": "final_answer", "content": [{"type": "output_text", "text": "```bash\nrun_tests ACTUAL\n```"}]}]
        module = types.ModuleType("minisweagent.exceptions")
        module.FormatError = type("FormatError", (Exception,), {})
        with patch.dict("sys.modules", {"minisweagent.exceptions": module}), patch.object(self.backend, "_request", side_effect=[first, second]) as request:
            model = MiniAPIModel(self.backend, "agent-a")
            initial = {"role": "user", "content": "task"}
            action = model.query([initial])
            self.assertEqual(action["extra"]["actions"], [{"command": "printf 'print(1)' > main.py"}])
            self.assertNotIn("trailing plan", action["content"])
            self.assertNotIn("PHANTOM", action["content"])
            observed = model.format_observation_messages(action, [{"returncode": 0, "output": "real write output"}])
            self.assertIn("Only the first proposed command was executed; later proposals were discarded", observed[0]["content"])
            next_action = model.query([initial, action, *observed])
        replayed = request.call_args.args[2]["input"]
        self.assertEqual(replayed[1]["phase"], "commentary")
        self.assertNotIn("PHANTOM", json.dumps(replayed))
        self.assertNotIn("trailing plan", json.dumps(replayed))
        self.assertIn("real write output", replayed[2]["content"])
        self.assertEqual(next_action["extra"]["actions"], [{"command": "run_tests ACTUAL"}])

    def test_general_backend_text_stays_final_only_while_messages_preserve_order(self):
        result = response()
        result["output"] = [
            {"type": "reasoning", "encrypted_content": "do-not-copy-to-assistant-messages"},
            {"type": "message", "phase": "commentary", "content": [{"type": "output_text", "text": "```bash\necho FIRST\n```"}]},
            {"type": "message", "phase": "final_answer", "content": [{"type": "output_text", "text": "FINAL TEXT"}]},
        ]
        with patch.object(self.backend, "_request", return_value=result):
            completion = self.backend.complete([{"role": "user", "content": "hello"}], run_id="screen-a")
        self.assertEqual(completion.text, "FINAL TEXT")
        self.assertEqual([row["phase"] for row in completion.assistant_messages], ["commentary", "final_answer"])
        self.assertNotIn("encrypted_content", json.dumps(completion.assistant_messages))

    def test_native_tool_is_rejected_even_with_valid_final_message(self):
        result = response()
        result["output"][1]["phase"] = "final_answer"
        result["output"][1]["content"][0]["text"] = "```bash\necho hi\n```"
        result["output"].append({"type": "function_call", "name": "shell"})
        with patch.object(self.backend, "_request", return_value=result):
            with self.assertRaises(APIError):
                self.backend.complete([{"role": "user", "content": "hello"}], run_id="screen-a")


class CatalogTests(unittest.TestCase):
    def test_candidates_require_actual_availability_and_explicit_price(self):
        available = model_ids({"data": [{"id": "test-model"}, {"id": "unpriced"}, {"id": "test-model"}]})
        self.assertEqual(economical_candidates(available, {"test-model": price(), "not-available": price("not-available")}), ["test-model"])

    def test_missing_cache_price_is_not_silently_guessed(self):
        known = FrozenPrice("test-model", "1", None, "2", "https://example.test/pricing", "2000-01-01")
        with self.assertRaises(ValueError):
            known.actual_cost(response()["usage"])

    def test_explicit_cache_write_usage_and_frozen_rates(self):
        known = CALIBRATION_PRICES["gpt-6-luna"]
        usage = {"input_tokens": 100, "output_tokens": 20,
                 "input_tokens_details": {"cached_tokens": 10, "cache_write_tokens": 30}}
        self.assertEqual(known.actual_cost(usage), Decimal("0.00001985"))
        self.assertEqual(known.maximum_cost(100, 20), Decimal("0.0000225"))
        self.assertEqual(known.accounted_cost(usage)[1], "usage_derived")


if __name__ == "__main__":
    unittest.main()
