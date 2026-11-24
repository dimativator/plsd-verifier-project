"""Offline recovery policy checks; no credentials, Docker or model calls."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from experiments import recover_interrupted as recovery


class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='plinse-controller-recovery-')
        self.root = Path(self.tmp.name)
        self.batch = self.root / 'batch'
        self.batch.mkdir()
        self.specs = [dict(phase='calibration', model='gpt-5.6-luna', task_id='task',
                           family_id='family', rating_band='2000-2399', condition=arm,
                           repetition=1) for arm in ('baseline', 'verifier', 'guided_verifier')]
        self.manifest = self.root / 'manifest.json'
        self.write(self.manifest, {'calibration_tasks': [{'id': 'task', 'checker': 'integer_tokens'}]})
        self.config = {'output': str(self.batch), 'spend_root': str(self.root / 'spend'),
                       'total_cap_usd': '3.00', 'per_run_cap_usd': '0.12',
                       'parallel_workers': 6, 'max_output_tokens': 100, 'effort': 'medium',
                       'step_limit': 100, 'solve_limit_seconds': 600, 'runtime': {}}
        self.write(self.batch / 'expected.json', {'runs': self.specs, 'config': self.config,
                                                'manifest_sha256': recovery.run.source_hash(self.manifest)})
        self.environment = patch.object(recovery, 'verify_retry_environment')
        self.environment.start()
        self.reason = 'Controller absent and Docker stopped; external interruption observed'

    def tearDown(self):
        self.environment.stop()
        self.tmp.cleanup()

    @staticmethod
    def write(path, value):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value), encoding='utf-8')

    def result(self, root, spec, **changes):
        row = {**spec, 'valid_run': True, 'hidden_passed': False, 'exit_status': 'Submitted',
               'infrastructure_error': None, 'model_cost_usd': .01, 'cost_is_upper_bound': False,
               'solve_seconds': 20, **changes}
        self.write(recovery._result_path(root, spec), row)
        return row

    def call(self, **kw):
        return recovery.recover(self.batch, self.manifest, reason=self.reason, **kw)

    def test_prepare_classifies_and_preserves_every_original_without_credentials(self):
        self.result(self.batch, self.specs[0])
        (recovery._result_path(self.batch, self.specs[1]).parent / 'workspace').mkdir(parents=True)
        before = (self.batch / 'expected.json').read_bytes()
        with patch.object(recovery.run, 'load_key') as key, patch.object(recovery.run, 'execute') as execute:
            report = self.call()
        key.assert_not_called()
        execute.assert_not_called()
        self.assertEqual(report['original_completed_preserved'], 1)
        self.assertEqual(report['interrupted_original_attempts'], 1)
        self.assertEqual(report['previously_unstarted'], 1)
        self.assertEqual(report['pending_recovery_runs'], 2)
        self.assertEqual((self.batch / 'expected.json').read_bytes(), before)
        selected = recovery._read(self.batch.with_name('batch-recovery-1') / 'resolved-results.json')
        self.assertEqual(len(selected), 3)
        self.assertEqual(sum(r['valid_run'] for r in selected), 1)

    def test_completed_wrong_answer_and_budget_exit_never_rerun(self):
        for spec, status in zip(self.specs, ('Submitted', 'budget_exhausted', 'RepeatedFormatError')):
            self.result(self.batch, spec, exit_status=status)
        with patch.object(recovery.run, 'load_key') as key, patch.object(recovery.run, 'execute') as execute:
            report = self.call(prepare_only=False)
        key.assert_not_called()
        execute.assert_not_called()
        self.assertEqual(report['original_completed_preserved'], 3)
        self.assertEqual(report['unresolved_runs'], 0)

    def test_one_recovery_and_fresh_first_attempt_use_same_ledger_and_original_config(self):
        original = self.result(self.batch, self.specs[0])
        (recovery._result_path(self.batch, self.specs[1]).parent / 'workspace').mkdir(parents=True)
        calls = []

        def fake(task, spec, cfg, ledger, key):
            self.assertEqual(cfg['spend_root'], self.config['spend_root'])
            self.assertEqual(cfg['step_limit'], 100)
            self.assertEqual(cfg['total_cap_usd'], '3.00')
            self.assertEqual(key, 'unit-test')
            calls.append(spec['condition'])
            return self.result(Path(cfg['output']), spec)

        with patch.object(recovery.run, 'load_key', return_value='unit-test') as key, \
             patch.object(recovery.run, 'execute', side_effect=fake), patch.object(recovery, 'SpendLedger') as ledger:
            report = self.call(prepare_only=False)
            self.call(prepare_only=False)
        self.assertEqual(sorted(calls), ['guided_verifier', 'verifier'])
        self.assertEqual(key.call_count, 1)
        ledger.assert_called_once_with(Path(self.config['spend_root']), total_limit_usd='3.00', per_run_limit_usd='0.12')
        self.assertEqual(report['resolved_valid_runs'], 3)
        self.assertEqual(recovery._read(recovery._result_path(self.batch, self.specs[0])), original)

    def test_changed_original_evidence_or_settings_reject_before_credentials(self):
        self.result(self.batch, self.specs[0])
        self.call()
        self.result(self.batch, self.specs[0], hidden_passed=True)
        with patch.object(recovery.run, 'load_key') as key:
            with self.assertRaisesRegex(ValueError, 'Frozen recovery plan differs'):
                self.call(prepare_only=False)
        key.assert_not_called()

    def test_claimed_incomplete_recovery_cannot_be_retried(self):
        self.call()
        root = self.batch.with_name('batch-recovery-1')
        recovery._immutable(root / 'claims' / (recovery._claim_name(self.specs[0]) + '.json'), {'claimed': True})
        with patch.object(recovery.run, 'load_key') as key, patch.object(recovery.run, 'execute') as execute:
            with self.assertRaisesRegex(ValueError, 'no automatic second attempt'):
                self.call(prepare_only=False)
        key.assert_not_called()
        execute.assert_not_called()

    def test_interrupted_original_reservations_and_recovery_charge_both_count(self):
        self.result(self.batch, self.specs[0])
        plan = recovery.prepare(self.batch, self.manifest, reason=self.reason)
        recovered_root = Path(plan['config']['output'])
        self.result(recovered_root, self.specs[1])
        spec = self.specs[1]
        suffix = '/'.join(str(spec[k]) for k in recovery.IDENTITY)
        self.write(Path(self.config['spend_root']) / 'ledger.json', {'reservations': {
            'old': {'run_id': self.batch.name + '/' + suffix, 'status': 'pending', 'reserved': '.04'},
            'new': {'run_id': recovered_root.name + '/' + suffix, 'status': 'settled', 'reserved': '.03', 'charged': '.02'}}})
        report = recovery.summarize(plan)
        row = next(r for r in report['runs'] if r['spec']['condition'] == 'verifier')
        self.assertEqual(row['all_attempt_cost_usd'], '0.06')
        self.assertTrue(row['attempts'][0]['cost_is_upper_bound'])
        selected = recovery._read(recovered_root / 'resolved-results.json')
        self.assertEqual(len(selected), 3)
        self.assertEqual(selected[1]['resolution']['selected_attempt'], 'recovery-1')

    def test_frozen_environment_failure_precedes_key_loading(self):
        with patch.object(recovery, 'verify_retry_environment', side_effect=ValueError('Frozen image changed')), \
             patch.object(recovery.run, 'load_key') as key:
            with self.assertRaisesRegex(ValueError, 'Frozen image changed'):
                self.call(prepare_only=False)
        key.assert_not_called()


if __name__ == '__main__':
    unittest.main()
