"""Explicit integration checks: PLINSE_DOCKER_TESTS=1 enables local containers."""
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from experiments.runtime import OUTPUT_LIMIT, VERIFIER_IMAGE, evaluate_python, matches, run_isolated


class CheckerTests(unittest.TestCase):
    def test_numeric_and_literal_outputs_differ(self):
        self.assertTrue(matches('01 +2', '1 2', 'integer_tokens'))
        self.assertFalse(matches('01', '1', 'tokens'))
        self.assertFalse(matches('1.0', '1', 'integer_tokens'))
        self.assertFalse(matches('1_000', '1000', 'integer_tokens'))
        self.assertFalse(matches('', '1', 'integer_tokens'))
        with self.assertRaises(ValueError):
            matches('a', 'a', 'unreviewed')


class EvaluatorControllerTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='plinse-controller-')
        self.root = Path(self.temporary.name)
        self.source = self.root / 'candidate.py'
        self.source.write_text('print(1)\n')
        self.tests = {'input': ['task-input\n'], 'output': ['secret-answer\n']}

    def tearDown(self):
        self.temporary.cleanup()

    def worker(self, **kwargs):
        return {'returncode': 0, 'stdout': '[]', 'stderr': '', 'timed_out': False,
                'elapsed_seconds': .1, 'output_truncated': False, **kwargs}

    def test_missing_docker_is_infrastructure_failure(self):
        with patch('experiments.runtime.subprocess.Popen', side_effect=FileNotFoundError('docker missing')):
            result = evaluate_python(self.source, self.tests, self.root / 'missing-docker')
        self.assertFalse(result['passed'])
        self.assertEqual(result['infrastructure_error']['type'], 'DockerLaunchError')

    def test_malformed_controller_output_is_infrastructure_failure(self):
        with patch('experiments.runtime.run_isolated', return_value=self.worker(stdout='not JSON')):
            result = evaluate_python(self.source, self.tests, self.root / 'bad-json')
        self.assertEqual(result['infrastructure_error']['type'], 'EvaluatorProtocolError')

    def test_resource_killed_container_remains_scored_failure(self):
        with patch('experiments.runtime.run_isolated', return_value=self.worker(returncode=137)):
            result = evaluate_python(self.source, self.tests, self.root / 'oom')
        self.assertFalse(result['passed'])
        self.assertNotIn('infrastructure_error', result)

    def test_only_inputs_enter_container_and_bad_answer_remains_scored_failure(self):
        rows = [{'case': 0, 'returncode': 0, 'stdout': 'wrong', 'timed_out': False,
                 'output_truncated': False}]
        with patch('experiments.runtime.run_isolated', return_value=self.worker(stdout=json.dumps(rows))) as isolated:
            result = evaluate_python(self.source, self.tests, self.root / 'wrong-answer')
        self.assertFalse(result['passed'])
        self.assertNotIn('infrastructure_error', result)
        self.assertEqual(json.loads(isolated.call_args.kwargs['input_text']), self.tests['input'])
        self.assertNotIn('secret-answer', (self.root / 'wrong-answer' / '_evaluate.py').read_text())


@unittest.skipUnless(os.environ.get('PLINSE_DOCKER_TESTS') == '1', 'explicit local Docker integration')
class ContainerTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='plinse-integration-')
        self.root = Path(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def test_temporary_helpers_persist_between_agent_actions(self):
        first = run_isolated(self.root, "printf 'print(42)\\n' > /tmp/helper.py", timeout=20)
        self.assertEqual(first['returncode'], 0, first)
        second = run_isolated(self.root, 'python /tmp/helper.py', timeout=20)
        self.assertEqual(second['returncode'], 0, second)
        self.assertEqual(second['stdout'].strip(), '42')

    def test_container_does_not_inherit_key_or_have_outbound_network(self):
        script = """import os,socket
assert os.getenv('OPENAI_API_KEY') is None
sock=socket.socket();sock.settimeout(1)
try:sock.connect(('1.1.1.1',443))
except OSError:print('isolated')
else:raise AssertionError('outbound network enabled')
"""
        (self.root / 'smoke.py').write_text(script)
        result = run_isolated(self.root, 'python smoke.py', timeout=20)
        self.assertEqual(result['returncode'], 0, result)
        self.assertIn('isolated', result['stdout'])

    def test_hidden_scorer_rejects_wrong_answer_and_early_exit(self):
        source = self.root / 'candidate.py'
        tests = {'input': ['2\n', '5\n'], 'output': ['4\n', '10\n']}
        source.write_text('print(int(input())*2)\n')
        result = evaluate_python(source, tests, self.root / 'correct', 'integer_tokens')
        self.assertTrue(result['passed'], result)
        source.write_text('print(0)\n')
        self.assertFalse(evaluate_python(source, tests, self.root / 'wrong')['passed'])
        source.write_text('raise SystemExit(0)\n')
        self.assertFalse(evaluate_python(source, tests, self.root / 'empty')['passed'])

    def test_action_timeout_terminates_container(self):
        (self.root / 'wait.py').write_text('import time\ntime.sleep(30)\n')
        result = run_isolated(self.root, 'python wait.py', timeout=1)
        self.assertTrue(result['timed_out'], result)

    def test_action_output_flood_is_stopped_and_capture_is_bounded(self):
        (self.root / 'flood.py').write_text('import os\nwhile True: os.write(1,b"x"*65536)\n')
        result = run_isolated(self.root, 'python flood.py', timeout=15)
        self.assertTrue(result['output_truncated'], result)
        self.assertLessEqual(len(result['stdout'].encode()) + len(result['stderr'].encode()), OUTPUT_LIMIT)
        self.assertFalse(result['timed_out'], result)
        self.assertLess(result['elapsed_seconds'], 15)

    def test_hidden_output_flood_is_scored_failure_without_crashing_worker(self):
        source = self.root / 'candidate.py'
        source.write_text('import os\nwhile True: os.write(1,b"x"*65536)\n')
        result = evaluate_python(source, {'input': ['\n'], 'output': ['1\n']}, self.root / 'flood')
        self.assertFalse(result['passed'])
        self.assertEqual(result['stage'], 'hidden_tests')
        self.assertNotIn('infrastructure_error', result)
        self.assertTrue(result['cases'][0]['output_truncated'])
        self.assertLessEqual(len(result['cases'][0]['stdout']), 200000)

    def test_crosshair_finds_bad_contract_and_accepts_good_one(self):
        for correct in (True, False):
            code = 'def increment(x: int) -> int:\n    """post: _ == x + 1"""\n    return x ' + ('+ 1\n' if correct else '- 1\n')
            (self.root / 'main.py').write_text(code)
            result = run_isolated(self.root, 'verify main.py', image=VERIFIER_IMAGE, timeout=45)
            self.assertEqual(result['returncode'] == 0, correct, result)
            self.assertIn('PLINSE_VERIFY_END', result['stdout'])


if __name__ == '__main__':
    unittest.main()
