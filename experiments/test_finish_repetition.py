"""Offline checks for finishing one existing repetition without rerunning outcomes."""
from copy import deepcopy
from decimal import Decimal
import json
from pathlib import Path
import tempfile
from threading import Event
import unittest
from unittest.mock import Mock, patch

from experiments import distributed as d
from experiments import extend_rounds as e
from experiments import finish_repetition as f
from experiments.test_extend_rounds import MemoryLedger


class FinishRepetitionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='plinse-finish-test-')
        self.root = Path(self.temp.name)
        self.output = self.root / 'extension'
        self.batch = self.output / 'extension-rep-0008'
        self.manifest = self.root / 'manifest.json'
        self.tasks = [{'id': f'task-{i}'} for i in range(100)]
        self.write(self.manifest, {'tasks': self.tasks})
        self.config = {'output': str(self.batch), 'spend_root': str(self.output / 'spend'),
                       'total_cap_usd': '50.00', 'per_run_cap_usd': '0.12', 'parallel_workers': 8,
                       'effort': 'medium', 'max_output_tokens': 16384,
                       'runtime': {'image_ids': {'image': 'pinned'}, 'source_sha256': {}}}
        self.specs = [dict(phase='main', model='gpt-5.6-luna', task_id=task['id'], family_id=task['id'],
                           condition=arm, repetition=8, rating_band='2000-2399' if index < 50 else '2400+',
                           worker_id='ours')
                      for index, task in enumerate(self.tasks) for arm in sorted(d.ARMS)]
        self.expected = {'runs': self.specs, 'config': self.config,
                         'manifest_sha256': d.run.source_hash(self.manifest)}
        self.write(self.batch / 'expected.json', self.expected)
        self.ledger = MemoryLedger(self.output / 'spend', '50.00', '.12')
        self.called = []
        for index, spec in enumerate(self.specs[:171]):
            self.raw(spec, infrastructure=index == 170)
        self.original_bytes = {p: p.read_bytes() for p in self.batch.rglob('*') if p.is_file()}
        self.write(self.output / 'status.json', {'completed_runs': 771, 'batch_completed': 171,
                   'completed_repetitions': [6, 7], 'prior_charge_usd': '0', 'remote_reserve_usd': '0'})
        self.write(self.batch / 'batch-report.json', {'complete': False, 'completed_runs': 171})

    def tearDown(self):
        self.temp.cleanup()

    @staticmethod
    def write(path, value):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value), encoding='utf-8')

    def raw(self, spec, *, infrastructure=False, config=None, passed=False):
        config = deepcopy(config or self.config)
        directory = d._result_path(Path(config['output']), spec).parent
        directory.mkdir(parents=True, exist_ok=True)
        (directory / 'main.py').write_text('print(1)\n', encoding='utf-8')
        row = {**spec, 'valid_run': not infrastructure, 'hidden_passed': passed,
               'infrastructure_error': {'type': 'APIError',
                                        'message': 'Responses request failed (HTTPError, HTTP 429); see log'} if infrastructure else None,
               'exit_status': 'infrastructure_error' if infrastructure else 'Submitted',
               'model_cost_usd': 0, 'cost_is_upper_bound': False,
               'model_settings': {k: config[k] for k in ('effort', 'max_output_tokens')},
               'submission_sha256': d.run.source_hash(directory / 'main.py')}
        self.write(directory / 'result.json', row)
        self.write(directory / 'spec.json', {**spec, 'limits': config})
        return row

    def execute(self, task, spec, config, ledger, key):
        self.called.append((spec, Path(config['output'])))
        reservation = ledger.reserve(e.run_id(Path(config['output']), spec), '.12')
        ledger.settle(reservation, '.02')
        return self.raw(spec, config=config)

    def info(self, *args):
        rows = [d._read(d._result_path(self.batch, s)) for s in self.specs
                if d._result_path(self.batch, s).exists()]
        pending = [s for s in self.specs if not d._result_path(self.batch, s).exists()]
        external = [s for s in self.specs if d._result_path(self.batch, s).exists()
                    and f.resolver.external_failure_reason(d._read(d._result_path(self.batch, s)))]
        return dict(batch=self.batch, root=self.output, expected=self.expected, config=self.config,
                    specs=self.specs, tasks=self.tasks, pending=pending, rows=rows,
                    external=external, repetition=8)

    def invoke(self, *, execute=None, key_loader=None, **kwargs):
        with patch.object(f, 'inspect', side_effect=self.info), \
             patch.object(f, 'SpendLedger', return_value=self.ledger), \
             patch.object(f.resolver, 'SpendLedger', return_value=self.ledger), \
             patch.object(f.resolver, 'verify_retry_environment'), \
             patch.object(f.run, 'load_key', side_effect=key_loader or (lambda: 'offline-only')), \
             patch.object(f.run, 'execute', side_effect=execute or self.execute), patch('builtins.print'):
            return f.finish(self.batch, self.manifest, **kwargs)

    def test_fill_129_only_retry_external_after_300_and_preserve_originals(self):
        def execute(task, spec, config, ledger, key):
            if Path(config['output']) != self.batch:
                self.assertEqual(len(list(self.batch.glob('*/*/*/rep-*/result.json'))), 300)
            return self.execute(task, spec, config, ledger, key)
        report = self.invoke(execute=execute, workers=4)
        originals = [spec for spec, root in self.called if root == self.batch]
        retries = [(spec, root) for spec, root in self.called if root != self.batch]
        self.assertEqual(len(originals), 129)
        self.assertEqual({d._key(s) for s in originals}, {d._key(s) for s in self.specs[171:]})
        self.assertEqual(len(retries), 1)
        self.assertEqual(d._key(retries[0][0]), d._key(self.specs[170]))
        self.assertTrue(retries[0][1].name.endswith('-infra-retry-1'))
        self.assertTrue(all(s['repetition'] == 8 for s, _ in self.called))
        self.assertFalse((self.output / 'extension-rep-0009').exists())
        for path, before in self.original_bytes.items():
            self.assertEqual(path.read_bytes(), before, str(path))
        self.assertEqual(report['status'], 'complete_requested_repetition')
        self.assertTrue(report['eligible_for_repetition_summary'])
        selected = d._read(self.batch / 'resolved-results.json')
        self.assertEqual(len(selected), 300)
        self.assertEqual(sum(r['resolution']['selected_attempt'] == 'infra-retry-1' for r in selected), 1)
        self.assertLessEqual(self.ledger.maximum, Decimal('50'))
        self.assertEqual(d._read(self.output / 'status.json')['completed_runs'], 900)

    def test_valid_wrong_answers_and_budget_exits_are_never_retried(self):
        path = d._result_path(self.batch, self.specs[0])
        row = d._read(path)
        row.update(exit_status='budget_exhausted', hidden_passed=False)
        self.write(path, row)
        report = self.invoke(workers=4)
        retries = [s for s, root in self.called if root != self.batch]
        self.assertEqual([d._key(s) for s in retries], [d._key(self.specs[170])])
        self.assertTrue(report['complete'])
        selected = d._read(self.batch / 'resolved-results.json')
        selected_budget = next(r for r in selected if d._key(r) == d._key(self.specs[0]))
        self.assertFalse(selected_budget['hidden_passed'])
        self.assertEqual(selected_budget['resolution']['selected_attempt'], 'original')

    def test_budget_admission_counts_pending_and_preserves_no_new_agent_failures(self):
        self.ledger.rows = {str(index): dict(run_id=f'older/run-{index}', status='pending', reserved='.10')
                            for index in range(350)}
        # A pending charge counts conservatively; the whole $15.60 remainder cannot fit.
        key = Mock(side_effect=AssertionError('Key loaded without whole-remainder funding'))
        report = self.invoke(key_loader=key)
        key.assert_not_called()
        self.assertEqual(report['status'], 'budget_stopped')
        self.assertEqual(Decimal(report['required_remaining_usd']), Decimal('15.60'))
        self.assertEqual(self.called, [])
        self.assertEqual(len(list(self.batch.glob('*/*/*/rep-*/result.json'))), 171)

    def test_stop_prevents_credentials_and_new_attempts(self):
        (self.output / 'STOP').write_text('stop', encoding='utf-8')
        key = Mock(side_effect=AssertionError('Key loaded after STOP'))
        report = self.invoke(key_loader=key)
        key.assert_not_called()
        self.assertEqual(report['status'], 'user_stopped')
        self.assertEqual(self.called, [])
        self.assertFalse((self.output / 'controller.lock').exists())

    def test_existing_controller_lock_prevents_any_work(self):
        (self.output / 'controller.lock').write_text('other-controller', encoding='utf-8')
        key = Mock(side_effect=AssertionError('Key loaded despite controller lock'))
        with self.assertRaises(FileExistsError):
            self.invoke(key_loader=key)
        key.assert_not_called()
        self.assertEqual(self.called, [])
        self.assertEqual((self.output / 'controller.lock').read_text(encoding='utf-8'), 'other-controller')

    def test_prepare_only_never_loads_credentials_or_changes_originals(self):
        key = Mock(side_effect=AssertionError('Key loaded by preparation'))
        report = self.invoke(key_loader=key, prepare_only=True)
        key.assert_not_called()
        self.assertEqual(report['pending_original_runs'], 129)
        self.assertEqual(report['known_external_failures'], 1)
        self.assertEqual(report['status'], 'prepared')
        self.assertFalse((self.output / 'controller.lock').exists())
        self.assertEqual(self.called, [])

    def test_resolver_only_completion_reports_credential_loading(self):
        for spec in self.specs[171:]:
            self.raw(spec)
        key = Mock(return_value='offline-only')
        report = self.invoke(key_loader=key, workers=1)
        self.assertEqual(key.call_count, 1)
        self.assertTrue(report['credentials_loaded'])
        self.assertTrue(report['resolver_credentials_loaded'])
        self.assertEqual(len(self.called), 1)
        self.assertTrue(self.called[0][1].name.endswith('-infra-retry-1'))
        status = d._read(self.output / 'status.json')
        self.assertTrue(status['credentials_loaded'])
        self.assertTrue(status['resolver_credentials_loaded'])

    def test_original_fill_credential_flag_survives_resolver_without_retries(self):
        self.raw(self.specs[170])
        key = Mock(return_value='offline-only')
        report = self.invoke(key_loader=key, workers=4)
        self.assertEqual(key.call_count, 1)
        self.assertTrue(report['credentials_loaded'])
        self.assertFalse(report['resolver_credentials_loaded'])
        self.assertTrue(report['complete'])

    def test_stop_reports_draining_until_admitted_active_job_finishes(self):
        second_started, release_second = Event(), Event()
        observed = []
        original_writer = f.run.write_json
        first_key = d._key(self.specs[171])

        def execute(task, spec, config, ledger, key):
            if d._key(spec) == first_key:
                self.assertTrue(second_started.wait(10))
                row = self.execute(task, spec, config, ledger, key)
                (self.output / 'STOP').write_text('stop')
                return row
            second_started.set()
            self.assertTrue(release_second.wait(10))
            return self.execute(task, spec, config, ledger, key)

        def publish(path, data):
            original_writer(path, data)
            if Path(path).name == 'status.json' and data['status'] == 'user_stopped' and data['active_runs']:
                observed.append(data['draining'])
                release_second.set()

        with patch.object(f.run, 'write_json', side_effect=publish):
            report = self.invoke(execute=execute, workers=2)
        self.assertTrue(observed)
        self.assertTrue(all(observed))
        self.assertEqual(len(self.called), 2)
        self.assertEqual(report['status'], 'user_stopped')
        self.assertFalse(report['draining'])
        self.assertFalse(d._read(self.output / 'status.json')['draining'])


if __name__ == '__main__':
    unittest.main()
