"""Preflight checks for dataset integrity, isolation, execution, and final scoring."""
import json
from pathlib import Path
import tempfile

from pilot.sandbox import profile, run
from python_pilot.evaluate import evaluate
from python_pilot.runtime import digest, execution_environment, tool_events, write_json


def main() -> None:
    project = Path(__file__).resolve().parents[1]
    root = project / 'python_pilot'
    common = root / 'toolchains/common'
    tasks = json.loads((root / 'selection.json').read_text())['tasks']
    assert len(tasks) == 50 and len({t['id'] for t in tasks}) == 50
    assert all(t['rating'] >= 1800 and t['checker'] == 'tokens' for t in tasks)
    counts = [sum(lo <= t['rating'] < hi for t in tasks) for lo, hi in [(1800, 2000), (2000, 2400), (2400, 10000)]]
    assert counts == [10, 20, 20]
    for task in tasks:
        for relative, expected in task['data_sha256'].items():
            assert digest(project / 'benchmark-data/codecontests/tasks' / task['id'] / relative) == expected
    report = {'selection_count': len(tasks), 'rating_counts': counts, 'data_hashes_match': True}
    with tempfile.TemporaryDirectory(dir=root) as tmp:
        workspace = Path(tmp)
        env = execution_environment(workspace, common, None)
        policy = profile(workspace, [common])
        for forbidden in [project / 'benchmark-data/codecontests/tasks/cf-483-B/evaluator/private-tests.json', root / 'envs/crosshair/bin/crosshair', root / 'envs/nagini/bin/nagini', root / 'toolchains/esbmc/config.json']:
            result = run(['/bin/cat', str(forbidden)], cwd=workspace, env=env, sandbox=policy)
            assert result['returncode'] != 0, forbidden
        result = run(['/bin/bash', '-c', 'command -v verify'], cwd=workspace, env=env, sandbox=policy)
        assert result['returncode'] != 0
        report['baseline_isolation_passed'] = True
        (workspace / 'main.py').write_text('print(int(input()) + 1)\n')
        write_json(workspace / 'public-tests.json', {'input': ['3\n'], 'output': ['4\n']})
        result = run(['/bin/bash', '-c', 'run_tests'], cwd=workspace, env=env, sandbox=policy)
        assert result['returncode'] == 0 and any(e['event'] == 'public_tests_end' and e['passed'] for e in tool_events(result['stdout']))
        (workspace / 'main.py').write_text('print(0)\n')
        result = run(['/bin/bash', '-c', 'run_tests'], cwd=workspace, env=env, sandbox=policy)
        assert result['returncode'] == 1
        (workspace / 'main.py').write_text('def broken(\n')
        result = run(['/bin/bash', '-c', 'compile'], cwd=workspace, env=env, sandbox=policy)
        assert result['returncode'] != 0
        report['public_positive_negative_syntax_passed'] = True
        task = next(t for t in tasks if t['id'] == 'cf-483-B')
        # Independently implement this existing scalar-output task to exercise the actual private suite.
        (workspace / 'main.py').write_text('''import sys

def solve():
    a, b, x, y = map(int, sys.stdin.buffer.read().split())
    lo, hi = 0, 2 * (a + b)
    while lo < hi:
        mid = (lo + hi) // 2
        if mid - mid // x >= a and mid - mid // y >= b and mid - mid // (x * y) >= a + b:
            hi = mid
        else:
            lo = mid + 1
    print(lo)

if __name__ == '__main__':
    solve()
''')
        correct = evaluate(project, task, workspace / 'main.py', workspace / 'scratch')
        assert correct['passed'], correct
        (workspace / 'main.py').write_text('print(0)\n')
        wrong = evaluate(project, task, workspace / 'main.py', workspace / 'scratch')
        assert not wrong['passed'] and wrong['test_count'] > 0
        report['hidden_positive_negative_passed'] = True
        report['hidden_suite_test_count'] = correct['test_count']
    write_json(root / 'runner-preflight.json', report)
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
