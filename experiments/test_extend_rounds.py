"""Focused offline extension-controller checks; no Docker or API calls."""
from concurrent.futures import Future
from copy import deepcopy
from decimal import Decimal
import json
from pathlib import Path
import tempfile
from threading import RLock
import unittest
from unittest.mock import Mock, patch

from experiments import extend_rounds as e


class MemoryLedger:
    """The real ledger's accounting/cap semantics without filesystem latency."""
    def __init__(self, directory, total_limit_usd, per_run_limit_usd):
        self.cap, self.per_run = Decimal(total_limit_usd), Decimal(per_run_limit_usd)
        self.rows = {}
        self.lock = RLock()
        self.maximum = Decimal(0)

    @staticmethod
    def cost(row):
        return Decimal(row['reserved'] if row['status'] == 'pending' else row['charged'])

    def reserve(self, run_id, amount):
        amount = Decimal(amount)
        with self.lock:
            total = sum((self.cost(r) for r in self.rows.values()), Decimal(0))
            own = sum((self.cost(r) for r in self.rows.values() if r['run_id'] == run_id), Decimal(0))
            if total + amount > self.cap or own + amount > self.per_run:
                raise AssertionError('Admission allowed a run to exhaust a ledger ceiling')
            key = str(len(self.rows))
            self.rows[key] = dict(run_id=run_id, reserved=str(amount), status='pending')
            self.maximum = max(self.maximum, total + amount)
            return key

    def settle(self, identity, amount):
        with self.lock:
            self.rows[identity].update(status='settled', charged=str(amount))

    def snapshot(self):
        with self.lock:
            rows = deepcopy(self.rows)
        return {'reservations': rows,
                'accounted_usd': str(sum((self.cost(r) for r in rows.values()), Decimal(0)))}


class ImmediatePool:
    """Deterministically surface STOP written during the first submit."""
    def __init__(self, **kwargs):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def submit(self, call, *args):
        future = Future()
        try:
            future.set_result(call(*args))
        except Exception as error:
            future.set_exception(error)
        return future


class ExtendRoundTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='plinse-extension-test-')
        self.root = Path(self.temp.name)
        self.output = self.root / 'queue'
        self.after = self.root / 'original'
        self.after.mkdir()
        self.write(self.after / 'worker-report.json', {'status': 'complete'})
        self.tasks = [{'id': f'task-{i}'} for i in range(100)]
        self.plan = {'runs': [dict(phase='main', model='gpt-5.6-luna', task_id=t['id'],
                                  family_id=t['id'], rating_band='2000-2399' if i < 50 else '2400+',
                                  condition=arm, repetition=rep, worker_id='ours' if rep <= 3 else 'friend')
                              for rep in range(1, 6) for i, t in enumerate(self.tasks) for arm in sorted(e.d.ARMS)],
                     'plan_sha256': 'source-plan-test', 'manifest_sha256': 'manifest-test',
                     'shared_config': {'per_run_cap_usd': '0.12', 'max_output_tokens': 16384,
                                       'effort': 'medium', 'runtime': {'image_ids': {'image': 'pinned'}}}}
        self.called = []
        self.ledgers = []

    def tearDown(self):
        self.temp.cleanup()

    @staticmethod
    def write(path, value):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value), encoding='utf-8')

    def execute(self, task, spec, config, ledger, key):
        identity = e.run_id(Path(config['output']), spec)
        reservation = ledger.reserve(identity, '.12')
        ledger.settle(reservation, '.12')
        self.called.append(spec)
        row = {**spec, 'valid_run': True, 'infrastructure_error': None,
               'exit_status': 'Submitted', 'model_cost_usd': .12,
               'model_settings': {k: config[k] for k in ('effort', 'max_output_tokens')}}
        self.write(e.d._result_path(Path(config['output']), spec), row)
        return row

    def ledger(self, *args, **kwargs):
        result = MemoryLedger(*args, **kwargs)
        self.ledgers.append(result)
        return result

    def invoke(self, *, execute=None, ledger=None, key_loader=None, **kwargs):
        with patch.object(e.d, '_load_plan', return_value=deepcopy(self.plan)), \
             patch.object(e.d, '_tasks', return_value=self.tasks), \
             patch.object(e.d, 'validate_environment', return_value={'image': 'pinned'}), \
             patch.object(e, 'SpendLedger', side_effect=ledger or self.ledger), \
             patch.object(e.run, 'load_key', side_effect=key_loader or (lambda: 'offline-test-key')), \
             patch.object(e.run, 'execute', side_effect=execute or self.execute), patch('builtins.print'):
            return e.controller(plan_path=self.root / 'plan.json', manifest=self.root / 'manifest.json',
                                output=self.output, after_worker=self.after, **kwargs)

    def test_round_specs_300_unique_new_global_ids_and_original_conditions(self):
        specs = e.round_specs(self.plan, 6)
        self.assertEqual(len(specs), 300)
        self.assertEqual(len({e.d._key(s) for s in specs}), 300)
        original = {e.d._key(s) for s in self.plan['runs']}
        self.assertFalse(original & {e.d._key(s) for s in specs})
        self.assertEqual({s['repetition'] for s in specs}, {6})
        self.assertEqual({s['condition'] for s in specs}, e.d.ARMS)
        self.assertTrue(all('analysis_stratum' not in s for s in specs))
        self.assertEqual({s['task_id'] for s in specs}, {t['id'] for t in self.tasks})
        with self.assertRaisesRegex(ValueError, 'overlaps'):
            e.round_specs(self.plan, 5)

    def test_lifetime_hold_survives_pending_settlement_and_uncertain_charge(self):
        def snapshot(status, reserved, charged=None):
            row = dict(run_id='active', status=status, reserved=reserved)
            if charged is not None:
                row['charged'] = charged
            return {'reservations': {'first': row}}
        for state in [snapshot('pending', '.08'), snapshot('settled', '.08', '.02'),
                      snapshot('uncertain', '.08', '.08')]:
            result = e.admission(state, {'active'}, Decimal('.12'), Decimal('.23'))
            self.assertEqual(Decimal(result['required_for_next_run_usd']), Decimal('.24'))
            self.assertFalse(result['admitted'])
        result = e.admission(snapshot('settled', '.08', '.02'), set(), Decimal('.12'), Decimal('.23'))
        self.assertTrue(result['admitted'])
        self.assertEqual(Decimal(result['required_for_next_run_usd']), Decimal('.14'))

    def test_hold_covers_active_with_no_first_reservation_and_zero_cost_refund(self):
        state = {'reservations': {}}
        self.assertFalse(e.admission(state, {'new-a', 'new-b'}, Decimal('.12'), Decimal('.35'))['admitted'])
        state['reservations']['rejected'] = dict(run_id='new-a', status='rejected', reserved='.08', charged='0')
        result = e.admission(state, {'new-a', 'new-b'}, Decimal('.12'), Decimal('.36'))
        self.assertTrue(result['admitted'])
        self.assertEqual(Decimal(result['required_for_next_run_usd']), Decimal('.36'))

    def test_pending_and_uncertain_completed_costs_keep_full_accounting(self):
        state = {'reservations': {
            'pending': dict(run_id='old-pending', status='pending', reserved='.10'),
            'uncertain': dict(run_id='old-uncertain', status='uncertain', reserved='.08', charged='.08'),
            'settled': dict(run_id='old-settled', status='settled', reserved='.09', charged='.02')}}
        result = e.admission(state, {'new'}, Decimal('.12'), Decimal('.43'))
        self.assertEqual(Decimal(result['accounted_usd']), Decimal('.20'))
        self.assertEqual(Decimal(result['required_for_next_run_usd']), Decimal('.44'))
        self.assertFalse(result['admitted'])

    def test_per_run_bound_violation_stops_admission(self):
        state = {'reservations': {'excess': dict(run_id='old', status='settled', reserved='.12', charged='.13')}}
        result = e.admission(state, set(), Decimal('.12'), Decimal('50'))
        self.assertFalse(result['admitted'])

    def test_finished_run_releases_unused_lifetime_hold_with_fresh_accounting(self):
        def cheap(task, spec, config, ledger, key):
            identity = e.run_id(Path(config['output']), spec)
            reservation = ledger.reserve(identity, '.08')
            ledger.settle(reservation, '.02')
            self.called.append(spec)
            row = {**spec, 'valid_run': True, 'infrastructure_error': None,
                   'exit_status': 'Submitted', 'model_cost_usd': .02,
                   'model_settings': {k: config[k] for k in ('effort', 'max_output_tokens')}}
            self.write(e.d._result_path(Path(config['output']), spec), row)
            return row
        with patch.object(e, 'ThreadPoolExecutor', ImmediatePool):
            report = self.invoke(execute=cheap, cap_usd='.14', workers=3)
        self.assertEqual(len(self.called), 2)
        self.assertEqual(Decimal(report['accounted_usd']), Decimal('.04'))
        self.assertEqual(report['status'], 'budget_stopped')
        self.assertLessEqual(self.ledgers[0].maximum, Decimal('.14'))

    def test_concurrent_hard_50_cap_preserves_last_partial_repetition(self):
        report = self.invoke(cap_usd='50.00', workers=8)
        self.assertEqual(report['status'], 'budget_stopped')
        self.assertEqual(report['completed_runs'], 416)
        self.assertEqual(report['completed_repetitions'], [6])
        self.assertEqual(Decimal(report['accounted_usd']), Decimal('49.92'))
        self.assertLessEqual(self.ledgers[0].maximum, Decimal('50.00'))
        self.assertEqual(len(self.called), 416)
        first = e.d._read(self.output / 'extension-rep-0006/batch-report.json')
        last = e.d._read(self.output / 'extension-rep-0007/batch-report.json')
        self.assertTrue(first['eligible_for_repetition_summary'])
        self.assertEqual(last['planned_runs'], 300)
        self.assertEqual(last['completed_runs'], 116)
        self.assertEqual(last['not_launched_runs'], 184)
        self.assertFalse(last['eligible_for_repetition_summary'])
        self.assertEqual(len(e.d._read(self.output / 'extension-rep-0007/expected.json')['runs']), 300)

    def test_stop_during_submit_prevents_further_admission(self):
        def execute(*args):
            row = self.execute(*args)
            e.stop(self.output)
            return row
        with patch.object(e, 'ThreadPoolExecutor', ImmediatePool):
            report = self.invoke(execute=execute, cap_usd='50.00', workers=3)
        self.assertEqual(len(self.called), 1)
        self.assertEqual(report['status'], 'user_stopped')
        partial = e.d._read(self.output / 'extension-rep-0006/batch-report.json')
        self.assertFalse(partial['eligible_for_repetition_summary'])
        self.assertEqual(partial['not_launched_runs'], 299)
        self.assertFalse(report['draining'])

    def test_raw_complete_round_with_infrastructure_error_is_not_completed_repetition(self):
        def fail_last(*args):
            row = self.execute(*args)
            if len(self.called) == 300:
                row.update(valid_run=False, exit_status='infrastructure_error',
                           infrastructure_error={'type': 'APIError', 'message': 'external failure'})
                self.write(e.d._result_path(Path(args[2]['output']), args[1]), row)
            return row

        with patch.object(e, 'ThreadPoolExecutor', ImmediatePool):
            report = self.invoke(execute=fail_last, cap_usd='50.00', workers=1)
        self.assertEqual(report['status'], 'infrastructure_stopped')
        self.assertEqual(report['completed_runs'], 300)
        self.assertEqual(report['completed_repetitions'], [])
        batch = e.d._read(self.output / 'extension-rep-0006/batch-report.json')
        self.assertTrue(batch['complete'])
        self.assertFalse(batch['eligible_for_repetition_summary'])

    def test_stop_while_waiting_does_not_load_credentials_or_create_ledger(self):
        (self.after / 'worker-report.json').unlink()
        (self.after / 'controller.lock').write_text('offline', encoding='utf-8')
        e.stop(self.output)
        key = Mock(side_effect=AssertionError('Credentials loaded while waiting'))
        report = self.invoke(key_loader=key)
        key.assert_not_called()
        self.assertEqual(report['status'], 'user_stopped_before_extension')
        self.assertEqual(self.ledgers, [])
        self.assertFalse((self.output / 'controller.lock').exists())
        self.assertFalse(report['credentials_loaded'])

    def test_completed_results_are_skipped_on_resume(self):
        def execute(*args):
            row = self.execute(*args)
            e.stop(self.output)
            return row
        with patch.object(e, 'ThreadPoolExecutor', ImmediatePool):
            self.invoke(execute=execute, cap_usd='.24', workers=1)
        self.assertEqual(len(self.called), 1)
        (self.output / 'STOP').unlink()
        ledger = self.ledgers[0]
        report = self.invoke(cap_usd='.24', workers=1, ledger=lambda *a, **k: ledger)
        self.assertEqual(len(self.called), 2)
        self.assertEqual(len({e.d._key(s) for s in self.called}), 2)
        self.assertEqual(report['completed_runs'], 2)
        self.assertEqual(report['status'], 'budget_stopped')

    def test_partial_attempt_rejected_before_credentials(self):
        spec = e.round_specs(self.plan, 6)[0]
        e.d._result_path(self.output / 'extension-rep-0006', spec).parent.mkdir(parents=True)
        key = Mock(side_effect=AssertionError('Credentials loaded before partial-attempt rejection'))
        with self.assertRaisesRegex(ValueError, 'Incomplete original attempt'):
            self.invoke(cap_usd='.24', workers=1, key_loader=key)
        key.assert_not_called()
        self.assertEqual(self.called, [])


if __name__ == '__main__':
    unittest.main()
