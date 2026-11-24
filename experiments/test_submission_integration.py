"""Submission liveness with real mini-SWE control flow and mocked external I/O."""
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

os.environ['MSWEA_SILENT_STARTUP'] = '1'

from experiments import run
from experiments.api_backend import Completion, SpendLedger
from experiments.submission_protocol import SUBMISSION_MARKER


class SubmissionIntegrationTests(unittest.TestCase):
    def exercise(self, commands, *, expect_notice=False):
        with tempfile.TemporaryDirectory(prefix='plinse-submit-') as name:
            root = Path(name)
            public = root / 'benchmark-data/codecontests/tasks/task/public'
            hidden = public.parent / 'evaluator'
            public.mkdir(parents=True)
            hidden.mkdir()
            (public / 'prompt.txt').write_text('Triple an integer.', encoding='utf-8')
            (public / 'public-tests.json').write_text(json.dumps({'input': ['2'], 'output': ['6']}))
            (hidden / 'private-tests.json').write_text(json.dumps({'input': ['3'], 'output': ['9']}))
            ledger = SpendLedger(root / 'spend')
            backend_calls, shell_calls = [], []
            owner = self

            class Backend:
                def __init__(self, **kwargs):
                    self.__dict__.update(kwargs)

                def complete(self, messages, *, run_id):
                    index = len(backend_calls)
                    owner.assertLess(index, len(commands), 'Submission should finish without another model call')
                    if expect_notice and index == len(commands) - 1:
                        owner.assertIn('not submitted, run echo ' + SUBMISSION_MARKER + ' to submit',
                                       messages[-1]['content'])
                    backend_calls.append(commands[index])
                    identity = ledger.reserve(run_id, '.001')
                    ledger.settle(identity, '.001')
                    return Completion('```mswea_bash_command\n' + commands[index] + '\n```',
                                      self.model, self.model, 'response-test',
                                      {'input_tokens': 1, 'output_tokens': 1}, '.001', .1,
                                      'completed', None, 'test', 'default', 'usage_derived')

            def execute(workspace, command, **kwargs):
                shell_calls.append(command)
                changed = 'write_revision' in command
                (workspace / 'main.py').write_text('print(int(input()) * ' + ('4' if changed else '3') + ')\n')
                return {'returncode': 0, 'stdout': SUBMISSION_MARKER + '\n' if changed else 'Syntax passed\n',
                        'stderr': '', 'timed_out': False, 'elapsed_seconds': .1, 'output_truncated': False}

            def evaluate(source, tests, scratch, checker):
                return {'passed': '* 3' in source.read_text(), 'test_count': 1, 'stage': 'hidden_tests'}

            cfg = {'output': str(root / 'batch'), 'max_output_tokens': 100, 'effort': 'medium',
                   'step_limit': 100, 'solve_limit_seconds': 30}
            spec = {'phase': 'calibration', 'model': 'gpt-5.6-luna', 'task_id': 'task',
                    'family_id': 'task', 'rating_band': '2000-2399', 'condition': 'baseline', 'repetition': 1}
            with patch.object(run, 'PROJECT', root), patch.object(run, 'OpenAIResponsesBackend', Backend), \
                 patch.object(run, 'run_isolated', execute), patch.object(run, 'evaluate_python', evaluate):
                row = run.execute({'id': 'task', 'checker': 'integer_tokens'}, spec, cfg, ledger, 'unit-test')
            source = (root / 'batch/gpt-5.6-luna/task/baseline/rep-01/main.py').read_text()
            return row, backend_calls, shell_calls, source

    def test_cd_prefixed_submission_finishes_without_running_or_repeating_it(self):
        commands = ['write_solution && compile', f'cd /work && echo {SUBMISSION_MARKER}']
        row, calls, shell, source = self.exercise(commands)
        self.assertTrue(row['valid_run'])
        self.assertEqual(row['exit_status'], 'Submitted')
        self.assertTrue(row['hidden_passed'])
        self.assertEqual(calls, commands)
        self.assertEqual(shell, commands[:1])
        self.assertEqual(row['shell_actions'], 1)

    def test_combined_write_and_marker_is_observed_before_real_submission(self):
        commands = ['write_solution && compile', f'write_revision; echo {SUBMISSION_MARKER}',
                    f'echo {SUBMISSION_MARKER}']
        row, calls, shell, source = self.exercise(commands, expect_notice=True)
        self.assertTrue(row['valid_run'])
        self.assertEqual(row['exit_status'], 'Submitted')
        self.assertEqual(calls, commands)
        self.assertEqual(shell, commands[:2])
        self.assertIn('* 4', source)
        self.assertFalse(row['hidden_passed'])
        self.assertEqual(row['shell_actions'], 2)


if __name__ == '__main__':
    unittest.main()
