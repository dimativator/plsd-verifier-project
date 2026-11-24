"""Offline resolver checks; model execution and credential loading are mocked."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from experiments import resolve_runs as resolver


class ResolverTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='plinse-resolve-')
        self.root = Path(self.temporary.name)
        self.batch = self.root / 'calibration-v3'
        self.batch.mkdir()
        self.spec = {'phase': 'calibration', 'model': 'gpt-5.6-luna', 'task_id': 'task-a',
                     'family_id': 'family-a', 'rating_band': '2000-2399',
                     'condition': 'verifier', 'repetition': 1}
        self.manifest = self.root / 'validated-task-manifest.json'
        self.write(self.manifest, {'calibration_tasks': [{'id': 'task-a', 'checker': 'integer_tokens'}], 'tasks': []})
        self.expected = {'runs': [self.spec], 'manifest_sha256': resolver.run.source_hash(self.manifest),
                         'config': {'output': str(self.batch), 'effort': 'medium', 'max_output_tokens': 100,
                                    'step_limit': 12, 'solve_limit_seconds': 600,
                                    'spend_root': str(self.root / 'spend'), 'total_cap_usd': '15.00',
                                    'per_run_cap_usd': '0.28', 'parallel_workers': 4, 'runtime': {}}}
        self.write(self.batch / 'expected.json', self.expected)

    def tearDown(self):
        self.temporary.cleanup()

    @staticmethod
    def write(path, value):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value), encoding='utf-8')

    def original(self, **changes):
        row = {**self.spec, 'valid_run': True, 'hidden_passed': False, 'exit_status': 'Submitted',
               'infrastructure_error': None, 'model_cost_usd': .02, 'cost_is_upper_bound': False, **changes}
        self.write(resolver._result_path(self.batch, self.spec), row)
        return row

    def external(self):
        return self.original(valid_run=False, exit_status='infrastructure_error',
                             infrastructure_error={'type': 'APIError', 'message': 'Responses request failed (TimeoutError, HTTP None); see immutable logs'})

    def successful_retry(self, task, spec, config, ledger, api_key):
        self.assertEqual(api_key, 'unit-test-token')
        self.assertEqual(task['id'], 'task-a')
        self.assertEqual(config['effort'], 'medium')
        self.assertEqual(config['solve_limit_seconds'], 600)
        self.assertEqual(config['parallel_workers'], 2)
        row = {**spec, 'valid_run': True, 'hidden_passed': True, 'exit_status': 'Submitted',
               'infrastructure_error': None, 'model_cost_usd': .03, 'cost_is_upper_bound': False}
        self.write(resolver._result_path(Path(config['output']), spec), row)
        return row

    def test_valid_wrong_answer_never_retries_or_loads_credentials(self):
        raw = self.original()
        with patch.object(resolver.run, 'load_key') as key, patch.object(resolver.run, 'execute') as execute, patch.object(resolver, 'SpendLedger') as ledger:
            report = resolver.resolve_batch(self.batch, retry_invalid=True)
        key.assert_not_called()
        execute.assert_not_called()
        ledger.assert_not_called()
        self.assertEqual(report['eligible_external_failures'], 0)
        self.assertEqual(report['resolved_valid_runs'], 1)
        self.assertEqual(json.loads(resolver._result_path(self.batch, self.spec).read_text()), raw)
        self.assertFalse(json.loads((self.batch / 'resolved-results.json').read_text())[0]['hidden_passed'])

    def test_valid_budget_or_format_failure_never_retries(self):
        for status in ('budget_exhausted', 'RepeatedFormatError'):
            with self.subTest(status=status):
                self.original(exit_status=status)
                with patch.object(resolver.run, 'load_key') as key, patch.object(resolver.run, 'execute') as execute:
                    resolver.resolve_batch(self.batch, retry_invalid=True)
                key.assert_not_called()
                execute.assert_not_called()

    def test_external_failure_retry_is_once_and_original_cost_is_preserved(self):
        raw = self.external()
        with patch.object(resolver.run, 'load_key', return_value='unit-test-token') as key, patch.object(resolver.run, 'execute', side_effect=self.successful_retry) as execute:
            report = resolver.resolve_batch(self.batch, retry_invalid=True)
            again = resolver.resolve_batch(self.batch, retry_invalid=True)
        self.assertEqual(key.call_count, 1)
        self.assertEqual(execute.call_count, 1)
        self.assertEqual(report['unresolved_runs'], 0)
        self.assertTrue(report['credentials_loaded'])
        self.assertFalse(again['credentials_loaded'])
        selected = json.loads((self.batch / 'resolved-results.json').read_text())
        self.assertEqual(len(selected), 1)
        self.assertEqual(selected[0]['model_cost_usd'], .03)
        self.assertTrue(selected[0]['hidden_passed'])
        self.assertEqual(selected[0]['resolution']['selected_attempt'], 'infra-retry-1')
        self.assertEqual(report['all_attempt_cost_usd'], '0.05')
        self.assertEqual(json.loads(resolver._result_path(self.batch, self.spec).read_text()), raw)

    def test_dry_resolution_of_external_failure_does_not_load_key(self):
        self.external()
        with patch.object(resolver.run, 'load_key') as key, patch.object(resolver.run, 'execute') as execute:
            report = resolver.resolve_batch(self.batch)
        self.assertEqual(report['unresolved_runs'], 1)
        self.assertEqual(report['eligible_external_failures'], 1)
        self.assertFalse(report['credentials_loaded'])
        key.assert_not_called()
        execute.assert_not_called()

    def assert_frozen_caps_retained(self, total, per_run):
        self.expected['config'].update(total_cap_usd=total, per_run_cap_usd=per_run)
        self.write(self.batch / 'expected.json', self.expected)
        self.external()
        with patch.object(resolver.run, 'load_key', return_value='unit-test-token'), \
             patch.object(resolver.run, 'execute', side_effect=self.successful_retry), \
             patch.object(resolver, 'SpendLedger') as ledger:
            report = resolver.resolve_batch(self.batch, retry_invalid=True)
        ledger.assert_called_once_with(self.root / 'spend', total_limit_usd=total, per_run_limit_usd=per_run)
        self.assertEqual(report['resolved_valid_runs'], 1)

    def test_prompt_pilot_retry_retains_its_three_dollar_ledger(self):
        self.assert_frozen_caps_retained('3.00', '0.12')

    def test_main_retry_retains_its_frozen_main_ledger(self):
        self.assert_frozen_caps_retained('115.00', '0.12')

    def test_nonpositive_or_nonfinite_caps_reject_before_credentials(self):
        self.external()
        for total, per_run in [('0', '.12'), ('3', '0'), ('-1', '.12'), ('NaN', '.12')]:
            with self.subTest(total=total, per_run=per_run):
                self.expected['config'].update(total_cap_usd=total, per_run_cap_usd=per_run)
                self.write(self.batch / 'expected.json', self.expected)
                with patch.object(resolver.run, 'load_key') as key:
                    with self.assertRaisesRegex(ValueError, 'positive finite'):
                        resolver.resolve_batch(self.batch, retry_invalid=True)
                key.assert_not_called()

    def test_existing_ledger_caps_cannot_be_changed_by_retry(self):
        self.external()
        resolver.SpendLedger(self.root / 'spend', total_limit_usd='3.00', per_run_limit_usd='.12')
        with patch.object(resolver.run, 'load_key') as key:
            with self.assertRaisesRegex(ValueError, 'different spend caps'):
                resolver.resolve_batch(self.batch, retry_invalid=True)
        key.assert_not_called()

    def test_retry_controller_failure_remains_invalid_and_is_not_retried_again(self):
        self.external()
        with patch.object(resolver.run, 'load_key', return_value='unit-test-token') as key, patch.object(resolver.run, 'execute', side_effect=ConnectionError('external controller failure')) as execute:
            report = resolver.resolve_batch(self.batch, retry_invalid=True)
            again = resolver.resolve_batch(self.batch, retry_invalid=True)
        self.assertEqual(execute.call_count, 1)
        self.assertEqual(key.call_count, 1)
        self.assertEqual(report['unresolved_runs'], 1)
        self.assertEqual(again['runs'][0]['retry_controller_error']['type'], 'ConnectionError')
        self.assertEqual(len(json.loads((self.batch / 'resolved-results.json').read_text())), 1)

    def test_unknown_or_protocol_api_error_is_not_treated_as_external(self):
        for error in ({'type': 'ValueError', 'message': 'bad dataset'},
                      {'type': 'APIError', 'message': 'Native tool or unexpected output item returned by model-only backend'},
                      {'type': 'APIError', 'message': 'Responses request failed (HTTPError, HTTP 400); see logs'}):
            with self.subTest(error=error):
                self.original(valid_run=False, exit_status='infrastructure_error', infrastructure_error=error)
                with patch.object(resolver.run, 'load_key') as key:
                    report = resolver.resolve_batch(self.batch, retry_invalid=True)
                key.assert_not_called()
                self.assertEqual(report['eligible_external_failures'], 0)
                self.assertEqual(report['unresolved_runs'], 1)

    def test_changed_manifest_is_rejected_before_credentials(self):
        self.external()
        self.write(self.manifest, {'calibration_tasks': [{'id': 'changed'}]})
        with patch.object(resolver.run, 'load_key') as key:
            with self.assertRaises(ValueError):
                resolver.resolve_batch(self.batch, retry_invalid=True)
        key.assert_not_called()

    def test_incomplete_original_batch_cannot_start_paid_retries(self):
        with patch.object(resolver.run, 'load_key') as key:
            with self.assertRaises(ValueError):
                resolver.resolve_batch(self.batch, retry_invalid=True)
            report = resolver.resolve_batch(self.batch)
        key.assert_not_called()
        self.assertEqual(report['unresolved_runs'], 1)
        self.assertEqual(len(json.loads((self.batch / 'resolved-results.json').read_text())), 1)

    def test_ledger_preserves_cost_of_interrupted_retry_with_no_result(self):
        self.external()
        retry_root = self.batch.with_name(self.batch.name + '-infra-retry-1')
        self.write(retry_root / 'claims' / (resolver._claim_name(self.spec) + '.json'), {'claimed': True})
        run_id = '/'.join([retry_root.name, *(str(self.spec[name]) for name in resolver.IDENTITY)])
        self.write(self.root / 'spend' / 'ledger.json', {'reservations': {
            'uncertain': {'run_id': run_id, 'status': 'uncertain', 'reserved': '.08', 'charged': '.08'}}})
        with patch.object(resolver.run, 'load_key') as key:
            report = resolver.resolve_batch(self.batch, retry_invalid=True)
        key.assert_not_called()
        self.assertEqual(report['all_attempt_cost_usd'], '0.10')
        self.assertEqual(report['runs'][0]['attempts'][1]['cost_source'], 'shared_ledger')
        self.assertTrue(report['runs'][0]['attempts'][1]['cost_is_upper_bound'])

    def test_unfunded_retry_keeps_claim_unused_and_does_not_load_key(self):
        self.external()
        self.expected['config'].update(total_cap_usd='.30', per_run_cap_usd='.28')
        self.write(self.batch / 'expected.json', self.expected)
        ledger = resolver.SpendLedger(self.root / 'spend', total_limit_usd='.30', per_run_limit_usd='.28')
        ledger.reserve('other-pending', '.10')
        with patch.object(resolver.run, 'load_key') as key, patch.object(resolver.run, 'execute') as execute:
            report = resolver.resolve_batch(self.batch, retry_invalid=True)
        key.assert_not_called()
        execute.assert_not_called()
        self.assertEqual(report['retry_dispatch_status'], 'budget_stopped_before_dispatch')
        self.assertEqual(report['unresolved_runs'], 1)
        self.assertFalse(self.batch.with_name(self.batch.name + '-infra-retry-1').exists())

    def test_stop_prevents_retry_claim_and_credentials(self):
        self.external()
        (self.root / 'STOP').write_text('stop')
        with patch.object(resolver.run, 'load_key') as key, patch.object(resolver.run, 'execute') as execute:
            report = resolver.resolve_batch(self.batch, retry_invalid=True)
        key.assert_not_called()
        execute.assert_not_called()
        self.assertEqual(report['retry_dispatch_status'], 'user_stopped')
        self.assertFalse(self.batch.with_name(self.batch.name + '-infra-retry-1').exists())

    def test_other_controller_blocks_paid_retry_before_credentials(self):
        self.external()
        (self.root / 'controller.lock').write_text('different-process')
        with patch.object(resolver.run, 'load_key') as key:
            with self.assertRaisesRegex(ValueError, 'Another controller'):
                resolver.resolve_batch(self.batch, retry_invalid=True)
        key.assert_not_called()
        self.assertEqual((self.root / 'controller.lock').read_text(), 'different-process')

    def test_stop_after_first_retry_keeps_next_claim_available(self):
        first = self.external()
        second_spec = {**self.spec, 'condition': 'guided_verifier'}
        second = {**first, **second_spec}
        self.expected['runs'].append(second_spec)
        self.write(self.batch / 'expected.json', self.expected)
        self.write(resolver._result_path(self.batch, second_spec), second)
        called = []

        def finish_first(task, spec, config, ledger, key):
            called.append(spec)
            row = {**spec, 'valid_run': True, 'hidden_passed': True,
                   'exit_status': 'Submitted', 'infrastructure_error': None, 'model_cost_usd': 0}
            self.write(resolver._result_path(Path(config['output']), spec), row)
            (self.root / 'STOP').write_text('stop')
            return row

        with patch.object(resolver.run, 'load_key', return_value='unit-test-token'), \
             patch.object(resolver.run, 'execute', side_effect=finish_first):
            report = resolver.resolve_batch(self.batch, retry_invalid=True, workers=1)
        self.assertEqual(len(called), 1)
        self.assertEqual(report['retry_dispatch_status'], 'user_stopped')
        self.assertEqual(report['unresolved_runs'], 1)
        retry = self.batch.with_name(self.batch.name + '-infra-retry-1')
        self.assertFalse((retry / 'claims' / (resolver._claim_name(second_spec) + '.json')).exists())
        self.assertFalse(resolver._result_path(retry, second_spec).parent.exists())


if __name__ == '__main__':
    unittest.main()
