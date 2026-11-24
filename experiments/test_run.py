"""The last saved implementation must be scored after a resource-limit exit."""
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

os.environ['MSWEA_SILENT_STARTUP'] = '1'

from experiments.api_backend import BudgetExceeded, Completion, SpendLedger
from experiments import run


class SchedulingTests(unittest.TestCase):
    def test_three_arm_blocks_cover_every_order_and_position(self):
        from collections import Counter
        arms = ['baseline', 'verifier', 'guided_verifier']
        orders = [run.condition_order(arms, i) for i in range(300)]
        self.assertEqual(len(set(orders)), 6)
        self.assertEqual(set(Counter(orders).values()), {50})
        for position in range(3):
            self.assertEqual(set(Counter(order[position] for order in orders).values()), {100})

    def test_six_repetitions_cover_every_order_for_each_task_and_band(self):
        from collections import Counter
        arms = ['baseline', 'verifier', 'guided_verifier']
        for band in ('2000', '2400'):
            observed = []
            for index in range(50):
                orders = [run.task_condition_order(arms, f'{band}-{index}', repetition)
                          for repetition in range(1, 7)]
                self.assertEqual(len(set(orders)), 6)
                observed.extend(orders)
            self.assertEqual(set(Counter(observed).values()), {50})

    def test_task_orders_do_not_depend_on_shard_size_or_position(self):
        arms = ['baseline', 'verifier', 'guided_verifier']
        tasks = [f'task-{index}' for index in range(100)]
        global_orders = {(task, rep): run.task_condition_order(arms, task, rep)
                         for task in tasks for rep in range(1, 7)}
        shard_orders = {(task, rep): run.task_condition_order(arms, task, rep)
                        for shard in (tasks[::2], tasks[1::2])
                        for task in reversed(shard) for rep in range(1, 7)}
        self.assertEqual(global_orders, shard_orders)

    def test_invalid_repetition_cannot_create_a_second_identity(self):
        for repetition in (0, -1, True, 1.5):
            with self.subTest(repetition=repetition), self.assertRaises(ValueError):
                run.task_condition_order(['baseline'], 'task', repetition)


class LastArtifactTests(unittest.TestCase):
    def test_budget_exhaustion_scores_final_source_and_keeps_denominator(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            public = root / 'benchmark-data/codecontests/tasks/task/public'
            hidden = public.parent / 'evaluator'
            public.mkdir(parents=True)
            hidden.mkdir()
            (public / 'prompt.txt').write_text('Double an integer.')
            (public / 'public-tests.json').write_text(json.dumps({'input': ['2'], 'output': ['4']}))
            (hidden / 'private-tests.json').write_text(json.dumps({'input': ['3'], 'output': ['6']}))
            ledger = SpendLedger(root / 'spend')

            class Backend:
                def __init__(self, **kwargs):
                    self.__dict__.update(kwargs)
                    self.calls = 0

                def complete(self, messages, *, run_id):
                    self.calls += 1
                    if self.calls > 1:
                        raise BudgetExceeded('Run cap reached')
                    identity = ledger.reserve(run_id, '.01')
                    ledger.settle(identity, '.01')
                    return Completion('```mswea_bash_command\nwrite_solution\n```',
                        self.model, self.model, 'response-test', {'input_tokens': 1, 'output_tokens': 1},
                        '.01', .1, 'completed', None, 'test', 'default', 'usage_derived')

            def execute(workspace, command, **kwargs):
                self.assertEqual(command, 'write_solution')
                import stat
                self.assertTrue(workspace.stat().st_mode & stat.S_IWOTH)
                self.assertTrue((workspace / 'main.py').stat().st_mode & stat.S_IWOTH)
                (workspace / 'main.py').write_text('print(int(input()) * 2)\n')
                return {'returncode': 0, 'stdout': '', 'stderr': '', 'timed_out': False,
                        'elapsed_seconds': .1, 'output_truncated': False}

            def evaluate(source, tests, scratch, checker):
                self.assertIn('* 2', source.read_text())
                return {'passed': True, 'test_count': 1, 'stage': 'hidden_tests'}

            config = {'output': str(root / 'batch'), 'max_output_tokens': 100,
                      'effort': 'medium', 'step_limit': 12, 'solve_limit_seconds': 30}
            spec = {'phase': 'calibration', 'model': 'gpt-6-luna', 'task_id': 'task',
                    'family_id': 'task', 'rating_band': '2000-2399', 'condition': 'baseline', 'repetition': 1}
            with patch.object(run, 'PROJECT', root), patch.object(run, 'OpenAIResponsesBackend', Backend), \
                    patch.object(run, 'run_isolated', execute), patch.object(run, 'evaluate_python', evaluate):
                result = run.execute({'id': 'task', 'checker': 'integer_tokens'}, spec, config, ledger, 'DUMMY')
            self.assertTrue(result['valid_run'])
            self.assertTrue(result['hidden_passed'])
            self.assertIsNone(result['infrastructure_error'])
            self.assertEqual(result['exit_status'], 'budget_exhausted')
            self.assertEqual(result['model_cost_usd'], .01)


class StandaloneControllerTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='plinse-run-controller-')
        self.root = Path(self.temporary.name)
        self.output, self.spend = self.root / 'batch', self.root / 'spend'
        self.manifest = self.root / 'manifest.json'
        self.manifest.write_text(json.dumps({'tasks': [{'id': 'task', 'family_id': 'family',
                                  'rating_band': '2000-2399', 'checker': 'integer_tokens'}]}))
        self.called = []

    def tearDown(self):
        self.temporary.cleanup()

    def invoke(self, *, cap='.30', prepare=False, key=None, execute=None):
        args = ['run', '--manifest', str(self.manifest), '--output', str(self.output),
                '--spend-root', str(self.spend), '--phase', 'main', '--models', 'gpt-5.6-luna',
                '--conditions', 'baseline', '--tasks', 'task', '--repetitions', '2',
                '--total-cap-usd', cap, '--per-run-cap-usd', '.12', '--workers', '1']
        if prepare:
            args.append('--prepare-only')
        with patch('sys.argv', args), patch.object(run, 'validate_frozen_tasks'), \
             patch.object(run.subprocess, 'check_output', return_value='sha256:offline-image'), \
             patch.object(run, 'load_key', side_effect=key or (lambda: 'offline-only')), \
             patch.object(run, 'execute', side_effect=execute or self.execute), patch('builtins.print'):
            run.main()

    def execute(self, task, spec, config, ledger, key):
        self.called.append(spec)
        row = {**spec, 'hidden_passed': False, 'exit_status': 'budget_exhausted',
               'model_cost_usd': 0, 'solve_seconds': 0, 'evaluation_seconds': 0,
               'model_settings': {k: config[k] for k in ('effort', 'max_output_tokens')}}
        directory = self.output / spec['model'] / spec['task_id'] / spec['condition'] / f"rep-{spec['repetition']:02d}"
        run.write_json(directory / 'result.json', row)
        return row

    def test_unfunded_batch_creates_no_attempt_or_scored_budget_failure(self):
        from unittest.mock import Mock
        key = Mock(side_effect=AssertionError('Credentials loaded before admission'))
        self.invoke(cap='.20', key=key)
        key.assert_not_called()
        self.assertEqual(self.called, [])
        self.assertFalse(any(self.output.glob('*/*/*/rep-*')))
        report = json.loads((self.output / 'controller-report.json').read_text())
        self.assertEqual(report['status'], 'budget_stopped_before_dispatch')
        self.assertEqual(report['pending_runs'], 2)

    def test_resume_preserves_completed_wrong_answers_and_budget_exits(self):
        from unittest.mock import Mock
        key = Mock(return_value='offline-only')
        self.invoke(key=key)
        originals = {p: p.read_bytes() for p in self.output.glob('*/*/*/rep-*/result.json')}
        self.invoke(key=key)
        self.assertEqual(len(self.called), 2)
        self.assertEqual(key.call_count, 1)
        self.assertEqual({p: p.read_bytes() for p in originals}, originals)
        self.assertTrue(all(json.loads(data)['exit_status'] == 'budget_exhausted' for data in originals.values()))

    def test_partial_original_rejects_before_key(self):
        from unittest.mock import Mock
        self.invoke(prepare=True)
        spec = json.loads((self.output / 'expected.json').read_text())['runs'][0]
        (self.output / spec['model'] / spec['task_id'] / spec['condition'] / 'rep-01').mkdir(parents=True)
        key = Mock(side_effect=AssertionError('Credentials loaded before artifact inspection'))
        with self.assertRaisesRegex(ValueError, 'Incomplete original attempt'):
            self.invoke(key=key)
        key.assert_not_called()

    def test_existing_stop_prevents_credentials_and_dispatch(self):
        from unittest.mock import Mock
        (self.root / 'STOP').write_text('stop')
        key = Mock(side_effect=AssertionError('Credentials loaded after STOP'))
        self.invoke(key=key)
        key.assert_not_called()
        self.assertEqual(self.called, [])

    def test_stop_after_first_run_leaves_remaining_identity_unstarted(self):
        def finish_first(*args):
            row = self.execute(*args)
            (self.root / 'STOP').write_text('stop')
            return row

        self.invoke(execute=finish_first)
        self.assertEqual(len(self.called), 1)
        self.assertEqual(len(list(self.output.glob('*/*/*/rep-*'))), 1)
        report = json.loads((self.output / 'controller-report.json').read_text())
        self.assertEqual(report['status'], 'user_stopped')
        self.assertEqual(report['pending_runs'], 1)


@unittest.skipUnless(os.environ.get('PLINSE_DOCKER_TESTS') == '1', 'explicit local Docker integration')
class NativeWorkspaceContainerTests(unittest.TestCase):
    def test_unprivileged_agent_can_edit_fresh_workspace_and_tmp(self):
        # On native Linux these host-created files retain the host user's UID.
        # Real UID-65534 Docker writes verify the permission boundary, without API calls.
        with tempfile.TemporaryDirectory(prefix='plinse-native-write-') as name:
            root = Path(name)
            public = root / 'benchmark-data/codecontests/tasks/task/public'
            hidden = public.parent / 'evaluator'
            public.mkdir(parents=True)
            hidden.mkdir()
            (public / 'prompt.txt').write_text('Double an integer.')
            (public / 'public-tests.json').write_text(json.dumps({'input': ['2'], 'output': ['4']}))
            (hidden / 'private-tests.json').write_text(json.dumps({'input': ['3'], 'output': ['6']}))
            ledger = SpendLedger(root / 'spend')

            class Backend:
                def __init__(self, **kwargs):
                    self.__dict__.update(kwargs)
                    self.calls = 0

                def complete(self, messages, *, run_id):
                    self.calls += 1
                    if self.calls > 1:
                        raise BudgetExceeded('Run cap reached')
                    command = "printf 'print(int(input()) * 2)\\n' > main.py && printf 'ok' > /tmp/uid-write-check"
                    return Completion('```mswea_bash_command\n' + command + '\n```',
                        self.model, self.model, 'response-test', {'input_tokens': 1, 'output_tokens': 1},
                        '0', .1, 'completed', None, 'test', 'default', 'usage_derived')

            config = {'output': str(root / 'batch'), 'max_output_tokens': 100,
                      'effort': 'medium', 'step_limit': 12, 'solve_limit_seconds': 30}
            spec = {'phase': 'calibration', 'model': 'gpt-6-luna', 'task_id': 'task',
                    'family_id': 'task', 'rating_band': '2000-2399', 'condition': 'baseline', 'repetition': 1}
            with patch.object(run, 'PROJECT', root), patch.object(run, 'OpenAIResponsesBackend', Backend):
                row = run.execute({'id': 'task', 'checker': 'integer_tokens'}, spec, config, ledger, 'OFFLINE')
            self.assertTrue(row['valid_run'], row)
            self.assertTrue(row['hidden_passed'], row)
            directory = root / 'batch/gpt-6-luna/task/baseline/rep-01'
            self.assertEqual((directory / 'workspace/.tmp/uid-write-check').read_text(), 'ok')


if __name__ == '__main__':
    unittest.main()
