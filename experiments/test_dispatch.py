"""Offline controller admission and ownership regressions."""
from decimal import Decimal
import os
from pathlib import Path
import tempfile
import unittest

from experiments.api_backend import SpendLedger
from experiments.dispatch import batch_admission, bounded_dispatch, controller_guard, stop_requested


class DispatchTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='plinse-dispatch-')
        self.root = Path(self.temporary.name)
        self.spend = self.root / 'spend'

    def tearDown(self):
        self.temporary.cleanup()

    def test_pending_and_uncertain_costs_block_whole_batch_admission(self):
        ledger = SpendLedger(self.spend, total_limit_usd='.30', per_run_limit_usd='.12')
        ledger.reserve('old-pending', '.08')
        uncertain = ledger.reserve('old-uncertain', '.08')
        ledger.fail(uncertain)
        check = batch_admission(ledger, 2, total_cap_usd='.30', per_run_cap_usd='.12')
        self.assertFalse(check['admitted'])
        self.assertEqual(Decimal(check['accounted_usd']), Decimal('.16'))
        self.assertEqual(Decimal(check['required_remaining_usd']), Decimal('.24'))
        self.assertEqual(len(ledger.snapshot()['reservations']), 2)

    def test_settlement_frees_only_unused_allowance_before_batch_start(self):
        ledger = SpendLedger(self.spend, total_limit_usd='.30', per_run_limit_usd='.12')
        reserved = ledger.reserve('finished', '.10')
        ledger.settle(reserved, '.02')
        self.assertTrue(batch_admission(ledger, 2, total_cap_usd='.30', per_run_cap_usd='.12')['admitted'])

    def test_controller_claim_is_exclusive_and_never_removes_someone_elses_lock(self):
        lock = self.root / 'controller.lock'
        lock.write_text('other-owner', encoding='ascii')
        with self.assertRaisesRegex(ValueError, 'Another controller'):
            with controller_guard(self.spend):
                self.fail('Claim accepted')
        self.assertEqual(lock.read_text(encoding='ascii'), 'other-owner')

    def test_nested_resolver_borrows_parent_claim_but_cannot_dispatch_twice(self):
        lock = self.root / 'controller.lock'
        lock.write_text(str(os.getpid()), encoding='ascii')
        with controller_guard(self.spend, inherit_current_process=True):
            with self.assertRaisesRegex(ValueError, 'Another dispatcher'):
                with controller_guard(self.spend, inherit_current_process=True):
                    self.fail('Concurrent nested dispatcher accepted')
        self.assertTrue(lock.exists())
        self.assertFalse((self.root / 'dispatch.lock').exists())

    def test_guard_releases_its_own_claim_on_controller_error(self):
        with self.assertRaisesRegex(RuntimeError, 'test-stop'):
            with controller_guard(self.spend):
                raise RuntimeError('test-stop')
        self.assertFalse((self.root / 'controller.lock').exists())
        self.assertFalse((self.root / 'dispatch.lock').exists())

    def test_stop_after_first_completion_does_not_prequeue_later_jobs(self):
        completed = []

        def execute(value):
            completed.append(value)
            (self.root / 'STOP').write_text('stop', encoding='ascii')
            return value

        results = list(bounded_dispatch(range(20), execute, workers=1,
                                        stopped=lambda: stop_requested(self.spend)))
        self.assertEqual(completed, [0])
        self.assertEqual(results, [(0, 0)])

    def test_existing_stop_prevents_every_submission(self):
        (self.root / 'STOP').write_text('stop', encoding='ascii')
        results = list(bounded_dispatch(range(20), lambda value: self.fail('Unexpected work'), workers=3,
                                        stopped=lambda: stop_requested(self.spend)))
        self.assertEqual(results, [])


if __name__ == '__main__':
    unittest.main()
