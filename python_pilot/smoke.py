"""Exercise real verifier wrappers inside the benchmark sandbox."""
import argparse
import json
from pathlib import Path
from pilot.sandbox import profile, run
from python_pilot.runtime import execution_environment, write_json


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('backends', nargs='*', default=['crosshair', 'nagini', 'esbmc'])
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    common = root / 'toolchains/common'
    sources = {
        'crosshair': 'def increment(x: int) -> int:\n    """post: _ == x + 1"""\n    return x + VALUE\n',
        'nagini': 'from nagini_contracts.contracts import *\ndef increment(x: int) -> int:\n    Ensures(Result() == x + 1)\n    return x + VALUE\n',
        'esbmc': 'def increment(x: int) -> int:\n    return x + VALUE\n',
    }
    for backend in args.backends:
        verifier = root / 'toolchains' / backend
        readable = [common, verifier] + ([root / 'envs' / backend] if backend != 'esbmc' else [])
        for case, value in [('positive', 1), ('negative', 2)]:
            workspace = root / 'smoke' / backend / case
            workspace.mkdir(parents=True, exist_ok=True)
            (workspace / 'main.py').write_text(sources[backend].replace('VALUE', str(value)))
            target = 'main.py'
            if backend == 'esbmc':
                (workspace / 'harness.py').write_text('from main import increment\nx: int = __VERIFIER_nondet_int()\n__ESBMC_assume(x >= 0 and x <= 100)\nassert increment(x) == x + 1\n')
                target = 'harness.py'
            env = execution_environment(workspace, common, verifier)
            result = run(['/bin/bash', '-c', 'verify ' + target], cwd=workspace, env=env, sandbox=profile(workspace, readable))
            write_json(workspace.parent / (case + '.json'), result)
            print(backend, case, result, flush=True)


if __name__ == '__main__':
    main()
