"""Four-condition Python pilot using the existing mini-SWE/Codex transport."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
import json
import logging
from pathlib import Path
import shutil
import time

from pilot.codex_model import CodexConfig, CodexModel, prepare_codex_home
from pilot.run import completion_requested, validate_hidden_suites
from pilot.sandbox import profile, run
from python_pilot.evaluate import evaluate
from python_pilot.runtime import digest, execution_environment, tool_events, write_json

CONDITIONS = ['baseline', 'crosshair', 'nagini', 'esbmc']
LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class RunConfig:
    project: Path
    output: Path
    model: str = 'gpt-5.6-luna'
    effort: str = 'medium'


def execute_agent(config: RunConfig, task: dict, condition: str) -> dict:
    from minisweagent.agents.default import DefaultAgent
    from minisweagent.environments.local import LocalEnvironment
    from minisweagent.exceptions import Submitted

    directory = config.output / 'codecontests' / task['id'] / condition
    if (directory / 'result.json').exists():
        return json.loads((directory / 'result.json').read_text())
    if directory.exists():
        raise FileExistsError(f'Inspect incomplete attempt before retry: {directory}')
    workspace = directory / 'workspace'
    workspace.mkdir(parents=True)
    original = config.project / 'benchmark-data/codecontests/tasks' / task['id'] / 'public'
    problem = (original / 'prompt.txt').read_text().replace('Write a Kotlin program', 'Write a Python 3 program').replace('Main.kt', 'main.py')
    (workspace / 'prompt.txt').write_text(problem)
    (workspace / 'main.py').write_text('# Write your solution here.\n')
    shutil.copyfile(original / 'public-tests.json', workspace / 'public-tests.json')
    write_json(workspace / 'task.json', {'id': task['id'], 'target_language': 'Python 3.13', 'solution_file': 'main.py'})
    root = config.project / 'python_pilot'
    common = root / 'toolchains/common'
    verifier = root / 'toolchains' / condition if condition != 'baseline' else None
    readable = [common]
    if verifier:
        readable += [verifier]
        if condition != 'esbmc':
            readable += [root / 'envs' / condition]
    env = execution_environment(workspace, common, verifier)
    policy = profile(workspace, readable)
    (directory / 'sandbox.sb').write_text(policy)
    actions = []
    seen_events = set()
    snapshots = directory / 'source-revisions'
    snapshots.mkdir()

    class AgentEnvironment(LocalEnvironment):
        def execute(self, action: dict, cwd: str = '', **kwargs) -> dict:
            command = action['command']
            if command.strip() == 'echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT' and not actions:
                return {'returncode': 1, 'output': 'Implement the solution before submitting.', 'exception_info': ''}
            before = digest(workspace / 'main.py')
            started = time.time()
            result = run(['/bin/bash', '-c', command], cwd=workspace, env=env, sandbox=policy)
            after = digest(workspace / 'main.py')
            output = {'returncode': result['returncode'], 'output': result['stdout'] + result['stderr'], 'exception_info': ''}
            submitted = completion_requested(command, result['stdout'], result['returncode'])
            if 'COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT' in result['stdout'].splitlines() and not submitted:
                output['output'] += '\nNot submitted. Submit with a separate action containing only: echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT\n'
            event_file = workspace / '.plsd-tool-events.jsonl'
            new_events = []
            telemetry_errors = []
            if event_file.exists():
                for line in event_file.read_text(errors='replace').splitlines(keepends=True):
                    if not line.endswith('\n'):
                        continue  # A background tool may still be writing this record.
                    try:
                        event = json.loads(line)
                        event_id = event['event_id']
                        if event_id not in seen_events:
                            new_events.append(event)
                            seen_events.add(event_id)
                    except (ValueError, KeyError, TypeError):
                        telemetry_errors.append('Malformed wrapper event ignored')
            observation = json.dumps(output, ensure_ascii=False)[:24000]
            visible_events = []
            for line in output['output'].splitlines():
                if line.startswith('PLSD_TOOL_EVENT ') and json.dumps(line, ensure_ascii=False)[1:-1] in observation:
                    visible_events.extend(tool_events(line))
            row = {'started': started, 'elapsed_seconds': time.time() - started, 'action': action,
                   'result': output, 'source_before': before, 'source_after': after,
                   'source_changed': before != after, 'events': new_events, 'visible_event_markers': visible_events, 'telemetry_errors': telemetry_errors}
            actions.append(row)
            with (directory / 'actions.jsonl').open('a') as stream:
                stream.write(json.dumps(row) + '\n')
            if before != after and after:
                shutil.copyfile(workspace / 'main.py', snapshots / f'action-{len(actions):04d}.py')
            if submitted:
                raise Submitted({'role': 'exit', 'content': '', 'extra': {'exit_status': 'Submitted', 'submission': ''}})
            return output

    instructions = (
        'Implement the complete Python 3 program in main.py, reading stdin and writing stdout. '
        'Only main.py is collected. Put helper functions in that file. Guard stdin/stdout execution with '
        'if __name__ == "__main__": so helpers can be imported for checks. '
        'Read prompt.txt. Commands on PATH: compile checks Python syntax; run_tests executes supplied public tests. '
        'python and python3 run the benchmark Python interpreter. You may write and run additional tests. '
        'Use focused checks of boundaries and algorithmic properties where useful. '
        'Produce a correct solution for all valid inputs. Hidden tests are unavailable during solving. '
        'The nagini_contracts package is importable in every condition. Proof-only expressions are not ordinary runtime checks; the evaluator does not erase them. '
    )
    if verifier:
        instructions += (
            f'Use the {condition} verifier as part of solving this task. First read {verifier / "GUIDE.txt"} for usage and examples. '
            'After implementing an initial solution, run verify on at least one relevant property of the actual algorithm before submitting. '
            'Choose a property that can expose a real bug, such as a loop invariant, array bounds, arithmetic safety, or a functional relationship. '
            'Do not substitute ordinary tests for this verifier attempt. Run the verify command through the shell. '
            'Inspect its returned diagnostics on your next turn. Fix any identified defect, or explain why the result is unsupported, inconclusive, or needs additional proof information. '
            'If a whole-program check is unsupported, try a focused check of an actual helper or algorithmic component. '
            'After inspecting the feedback, decide whether further verification or testing is useful. '
            'You may create a verification harness that imports the actual algorithm from main.py, or a version with proof annotations and an identical algorithm body. '
            'Do not narrow the task input domain or verify a substitute algorithm merely to obtain a successful result. '
        )
    model = CodexModel(CodexConfig(config.model, config.effort, str(config.project / 'pilot/.runtime/codex-home'), str(directory / 'model')))
    agent = DefaultAgent(model, AgentEnvironment(cwd=str(workspace), env=env),
        system_template=('You are a coding agent running under mini-SWE-agent. Respond with a short explanation '
            'followed by exactly ONE mswea_bash_command code block. Your shell command is executed by mini-SWE-agent. '
            'Work iteratively: inspect the task, implement, run checks, inspect their results, and revise as needed. '
            'Commands return observations on your next turn. When finished, submit in a SEPARATE action containing only: '
            'echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT. Do not combine submission with writing code or running checks. '
            'Do not use native Codex tools.'), instance_template='{{task}}', step_limit=0, cost_limit=0,
        wall_time_limit_seconds=0, output_path=directory / 'trajectory.json')
    started = time.time()
    LOGGER.info('START %s %s', task['id'], condition)
    failure = None
    try:
        completion = agent.run(task=instructions + '\n\n' + problem)
    except Exception as error:
        failure = {'type': type(error).__name__, 'message': str(error)}
        completion = {'exit_status': type(error).__name__}
        LOGGER.exception('Agent failed: %s %s', task['id'], condition)
    submission = directory / 'main.py'
    if digest(workspace / 'main.py'):
        shutil.copyfile(workspace / 'main.py', submission)
    hidden = evaluate(config.project, task, submission, directory / 'evaluator-scratch')
    write_json(directory / 'hidden-evaluation.json', hidden)
    verify_indices = [i for i, a in enumerate(actions) if any(e['event'] == 'verify_end' for e in a['visible_event_markers'])]
    verified_before = False
    edited_after = 0
    for a in actions:
        if verified_before and a['source_changed']:
            edited_after += 1
        verified_before |= any(e['event'] == 'verify_end' for e in a['visible_event_markers'])
    result = {'task_id': task['id'], 'rating': task['rating'], 'condition': condition,
        'model': config.model, 'reasoning_effort': config.effort, 'started_unix': started,
        'elapsed_seconds': time.time() - started, 'exit_status': completion.get('exit_status'),
        'infrastructure_error': failure, 'valid_run': failure is None and completion.get('exit_status') == 'Submitted',
        'hidden_passed': hidden['passed'], 'submission_sha256': digest(submission),
        'model_calls': agent.n_calls, 'shell_actions': len(actions),
        'public_test_calls': sum(e['event'] == 'public_tests_start' for a in actions for e in a['events']),
        'verify_calls': sum(e['event'] == 'verify_start' for a in actions for e in a['events']),
        'verify_completed': sum(e['event'] == 'verify_end' for a in actions for e in a['events']),
        'verifier_observations_followed_by_action': sum(i + 1 < len(actions) for i in verify_indices),
        'source_edits_after_verifier_feedback': edited_after,
        'interpretation': 'Edits after feedback are temporal association, not evidence of causality. Tool counts use wrapper event files, including redirected calls. Feedback markers indicate returned output, not comprehension; redirected feedback read later needs trajectory audit.'}
    write_json(directory / 'result.json', result)
    LOGGER.info('DONE %s %s pass=%s verify=%s', task['id'], condition, hidden['passed'], result['verify_calls'])
    return result


def summarize(output: Path) -> dict:
    selection = json.loads((output / 'selection.json').read_text())
    conditions = selection.get('conditions', CONDITIONS)
    rows = [json.loads(p.read_text()) for p in output.glob('codecontests/*/*/result.json')]
    rows = [row for row in rows if row['condition'] in conditions]
    groups = []
    for condition in conditions:
        for low, high in [(1800, 10000), (1800, 2000), (2000, 2400), (2400, 10000)]:
            group = [r for r in rows if r['condition'] == condition and low <= r['rating'] < high]
            valid = [r for r in group if r['valid_run']]
            groups.append({'condition': condition, 'rating_min': low, 'rating_max_exclusive': high,
                'finished': len(group), 'valid': len(valid), 'passed': sum(r['hidden_passed'] for r in valid),
                'success_rate': sum(r['hidden_passed'] for r in valid) / len(valid) if valid else None,
                'trials_running_public_tests': sum(r['public_test_calls'] > 0 for r in group),
                'trials_calling_verify': sum(r['verify_calls'] > 0 for r in group),
                'verify_calls': sum(r['verify_calls'] for r in group),
                'trials_editing_after_verify': sum(r['source_edits_after_verifier_feedback'] > 0 for r in group)})
    pairs = []
    baseline = {r['task_id']: r for r in rows if r['condition'] == 'baseline' and r['valid_run']}
    for condition in [c for c in conditions if c != 'baseline']:
        paired = [(baseline[r['task_id']], r) for r in rows if r['condition'] == condition and r['valid_run'] and r['task_id'] in baseline]
        pairs.append({'condition': condition, 'paired': len(paired),
            'verifier_only_pass': [b['task_id'] for a, b in paired if b['hidden_passed'] and not a['hidden_passed']],
            'baseline_only_pass': [a['task_id'] for a, b in paired if a['hidden_passed'] and not b['hidden_passed']]})
    report = {'updated_unix': time.time(), 'finished': len(rows), 'groups': groups, 'pairs': pairs}
    write_json(output / 'summary.json', report)
    lines = ['Python verifier comparison', f'Completed: {len(rows)} / {len(selection["tasks"]) * len(conditions)}',
             '', 'condition | rating | finished | valid | hidden pass | public-test users | verifier users | edits after feedback']
    for g in groups:
        band = 'all' if (g['rating_min'], g['rating_max_exclusive']) == (1800, 10000) else str(g['rating_min']) + '-' + (str(g['rating_max_exclusive'] - 1) if g['rating_max_exclusive'] != 10000 else 'plus')
        lines.append(f"{g['condition']} | {band} | {g['finished']} | {g['valid']} | {g['passed']} | {g['trials_running_public_tests']} | {g['trials_calling_verify']} | {g['trials_editing_after_verify']}")
    lines += ['', 'Counts cover instrumented commands. Edits after feedback are temporal, not causal evidence.',
              'Infrastructure failures are excluded from valid-run success rates and retained in raw results.',
              'Paired outcomes: ' + json.dumps(pairs)]
    (output / 'summary.txt').write_text('\n'.join(lines) + '\n')
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--selection', type=Path, default=Path('python_pilot/selection.json'))
    parser.add_argument('--workers', type=int, default=4)
    args = parser.parse_args()
    project = Path(__file__).resolve().parents[1]
    output = args.output.resolve()
    selection = json.loads(args.selection.read_text())
    conditions = selection.get('conditions', CONDITIONS)
    if not conditions or len(set(conditions)) != len(conditions) or any(c not in CONDITIONS for c in conditions):
        raise ValueError('Invalid condition selection')
    validate_hidden_suites(project, selection)
    for task in selection['tasks']:
        for relative, expected in task['data_sha256'].items():
            path = project / 'benchmark-data/codecontests/tasks' / task['id'] / relative
            if digest(path) != expected:
                raise ValueError(f'Dataset changed: {path}')
    sources = list((project / 'python_pilot').glob('*.py')) + list((project / 'python_pilot/guides').glob('*.txt')) + [project / 'pilot/codex_model.py', project / 'pilot/sandbox.py', project / 'pilot/run.py']
    manifest = {'selection': selection, 'sources': {str(p.relative_to(project)): digest(p) for p in sources},
        'toolchain': json.loads((project / 'python_pilot/toolchains/provenance.json').read_text()), 'workers': args.workers}
    output.mkdir(parents=True, exist_ok=True)
    if (output / 'config.json').exists() and json.loads((output / 'config.json').read_text()) != manifest:
        raise ValueError('Resume configuration/source mismatch')
    for path in sources:
        saved = output / 'runner-source' / path.relative_to(project)
        saved.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, saved)
    write_json(output / 'config.json', manifest)
    write_json(output / 'selection.json', selection)
    prepare_codex_home(project / 'pilot/.runtime/codex-home')
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
    config = RunConfig(project, output)
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = []
        for i, task in enumerate(selection['tasks']):
            for condition in conditions[i % len(conditions):] + conditions[:i % len(conditions)]:
                futures.append(pool.submit(execute_agent, config, task, condition))
        for future in as_completed(futures):
            future.result()
            summarize(output)
    summarize(output)


if __name__ == '__main__':
    main()
