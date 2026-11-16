"""Agent-visible Python commands. No evaluator paths or reference solutions."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import time
import uuid


def emit(kind: str, **fields) -> None:
    event = {'event': kind, 'event_id': str(uuid.uuid4()), 'timestamp': time.time(), **fields}
    with Path('.plsd-tool-events.jsonl').open('a') as stream:
        stream.write(json.dumps(event) + '\n')
    print('PLSD_TOOL_EVENT ' + json.dumps(event), flush=True)


def verify(config: dict, arguments: list[str]) -> int:
    backend = config.get('backend')
    if not backend:
        raise ValueError('No verifier is available in this condition')
    target = arguments[0] if arguments and not arguments[0].startswith('-') else 'main.py'
    extra = arguments[1:] if arguments and not arguments[0].startswith('-') else arguments
    path = Path(target).resolve()
    if not path.is_relative_to(Path.cwd().resolve()) or not path.is_file():
        raise ValueError('Verification target must be a file in this workspace')
    if backend == 'crosshair':
        command = [config['executable'], 'check', '--analysis_kind=PEP316,asserts', '--report_all', str(path), *extra]
    elif backend == 'nagini':
        command = [config['executable'], '--z3=' + config['z3'], str(path), *extra]
    else:
        unwind = [] if any(arg == '--unwind' or arg.startswith('--unwind=') for arg in extra) else ['--unwind', '10']
        command = [config['executable'], str(path), '--python', config['python'], *unwind, *extra]
    started = time.time()
    snapshots = Path('.plsd-verification-sources')
    snapshots.mkdir(exist_ok=True)
    source_hash = hashlib.sha256(path.read_bytes()).hexdigest()
    (snapshots / (source_hash + '.py')).write_bytes(path.read_bytes())
    emit('verify_start', backend=backend, target=target,
         target_sha256=source_hash, main_sha256=hashlib.sha256(Path('main.py').read_bytes()).hexdigest(), command=command)
    print('A skipped check, timeout, unsupported feature, or absence of a counterexample is not proof of task correctness.', flush=True)
    result = subprocess.run(command, stderr=subprocess.STDOUT)
    emit('verify_end', backend=backend, returncode=result.returncode, elapsed_seconds=time.time() - started)
    return result.returncode


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('command', choices=['compile', 'test', 'verify'])
    parser.add_argument('arguments', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    config = json.loads(args.config.read_text())
    if args.command == 'verify':
        raise SystemExit(verify(config, args.arguments))
    source = Path('main.py')
    ast.parse(source.read_text(), filename=str(source))
    emit('compile_end', passed=True)
    if args.command == 'compile':
        return
    tests = json.loads(Path('public-tests.json').read_text())
    emit('public_tests_start', count=len(tests['input']))
    good = True
    for index, (given, expected) in enumerate(zip(tests['input'], tests['output'])):
        try:
            result = subprocess.run([config['python'], '-B', str(source)], input=given,
                                    capture_output=True, text=True, timeout=10)
            correct = result.returncode == 0 and result.stdout.split() == expected.split()
            emit('public_test_case', case=index, passed=correct, returncode=result.returncode,
                 expected=expected, actual=result.stdout[:5000], stderr=result.stderr[:5000])
        except subprocess.TimeoutExpired:
            correct = False
            emit('public_test_case', case=index, passed=False, timed_out=True)
        good = good and correct
        if not correct:
            break
    emit('public_tests_end', passed=good)
    raise SystemExit(0 if good else 1)


if __name__ == '__main__':
    main()
