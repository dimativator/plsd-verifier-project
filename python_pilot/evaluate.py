"""Trusted Python evaluator, run only after the agent submits."""
import ast
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import shutil
import tempfile

from pilot.sandbox import profile, run
from python_pilot.runtime import execution_environment


def evaluate(project: Path, task: dict, submission: Path, scratch: Path) -> dict:
    if not submission.is_file() or submission.is_symlink():
        return {'passed': False, 'stage': 'missing_submission'}
    try:
        ast.parse(submission.read_text())
    except SyntaxError as error:
        return {'passed': False, 'stage': 'syntax_error', 'error': str(error)}
    tests = json.loads((project / 'benchmark-data/codecontests/tasks' / task['id'] / 'evaluator/private-tests.json').read_text())
    if not tests['input'] or len(tests['input']) != len(tests['output']):
        raise ValueError('Empty or unaligned hidden suite')
    common = project / 'python_pilot/toolchains/common'
    config = json.loads((common / 'config.json').read_text())
    scratch.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=scratch) as directory:
        workspace = Path(directory)
        shutil.copyfile(submission, workspace / 'main.py')
        env = execution_environment(workspace, common, None)
        policy = profile(workspace, [common])

        def check(item: tuple[int, tuple[str, str]]) -> dict:
            index, (given, expected) = item
            result = run([config['python'], '-B', str(workspace / 'main.py')], cwd=workspace,
                         env=env, sandbox=policy, input_text=given, timeout=10)
            passed = result['returncode'] == 0 and not result['timed_out'] and result['stdout'].split() == expected.split()
            return {'case': index, 'passed': passed, 'returncode': result['returncode'],
                    'timed_out': result['timed_out'], 'actual': result['stdout'][:3000],
                    'expected': expected[:3000], 'stderr': result['stderr'][:3000]}

        with ThreadPoolExecutor(max_workers=2) as pool:
            checks = list(pool.map(check, enumerate(zip(tests['input'], tests['output']))))
    return {'stage': 'hidden_tests', 'passed': all(r['passed'] for r in checks), 'test_count': len(checks),
            'passed_count': sum(r['passed'] for r in checks), 'failures': [r for r in checks if not r['passed']]}
