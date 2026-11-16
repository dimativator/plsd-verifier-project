"""Prepare a reviewed, difficulty-balanced 100-task Codeforces experiment."""

from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path

from pilot.evaluate import reference_check
from pilot.run import validate_hidden_suites, write_json


def main() -> None:
    project = Path(__file__).resolve().parents[1]
    candidates = json.loads((project / 'pilot/expanded-candidates.json').read_text())
    rejected_outputs = {
        'cf-491-A', 'cf-686-B', 'cf-1436-B', 'cf-322-A',
        'cf-1165-C', 'cf-1266-C', 'cf-681-C', 'cf-1316-C',
        'cf-12-E', 'cf-323-B', 'cf-762-C',
        'cf-1345-E', 'cf-1205-F', 'cf-521-E', 'cf-1491-G', 'cf-91-E',
    }
    incomplete_statements = {'cf-171-G', 'cf-409-C', 'cf-670-D2', 'cf-690-A2', 'cf-913-C'}
    output = project / 'pilot/expanded-preflight'
    destination = project / 'pilot/expanded-selection.json'
    if destination.exists():
        raise FileExistsError('Selection already frozen')
    tasks = []
    screening = []
    bands = ['800-1199', '1200-1599', '1600-1999', '2000-2399', '2400+']
    for band in bands:
        pool = [r for r in candidates if r['rating_band'] == band and r['id'] not in rejected_outputs | incomplete_statements]
        for row in candidates:
            if row['rating_band'] == band and row['id'] in incomplete_statements:
                screening.append({'id': row['id'], 'reason': 'Missing or underspecified problem body'})
            if row['rating_band'] == band and row['id'] in rejected_outputs:
                screening.append({'id': row['id'], 'reason': 'Output allows multiple solutions; requires a semantic checker'})

        def check(row: dict) -> tuple[dict, dict]:
            selected = {'dataset': 'codecontests', 'id': row['id'], 'rating_band': band,
                        'difficulty': row['difficulty'], 'checker': 'tokens',
                        'output_requirement': row['output_requirement'],
                        'checker_review': 'Unique required scalar/vector/string or explicitly fixed optimal output; whitespace tokens'}
            validate_hidden_suites(project, {'tasks': [selected]})
            try:
                result = reference_check(project, selected, output / row['id'])
            except (StopIteration, ValueError) as error:
                result = {'passed': False, 'stage': 'reference_setup', 'error': str(error)}
            write_json(output / row['id'] / 'result.json', result)
            return selected, result

        with ThreadPoolExecutor(max_workers=4) as executor:
            checked = list(executor.map(check, pool))
        eligible = []
        for selected, result in checked:
            if result['passed']:
                eligible.append(selected)
            else:
                screening.append({'id': selected['id'], 'reason': 'Source reference sanity check failed',
                                  'stage': result.get('stage')})
        if len(eligible) < 20:
            write_json(output / 'screening.json', screening)
            raise ValueError(f'Only {len(eligible)} eligible tasks in {band}')
        tasks.extend(eligible[:20])
        print(band, 'selected', 20, 'checked', len(pool), flush=True)
    selection = json.loads((project / 'pilot/guidance-selection.json').read_text())
    selection.update({'task_count': 100, 'tasks': tasks,
                      'selection': '20 per rating band. Candidate order SHA256(20261114-expanded:task_id). Exclude all prior run selections, absent private tests, conflicting expected outputs, image placeholders, and outputs needing semantic or floating checkers. Output requirements manually reviewed. Take first 20 reference-passing reviewed candidates per band before agent outcomes.',
                      'purpose': 'Expanded comparison with frozen optional-verifier guidance. One independent attempt per condition and task.',
                      'checker_review': 'Stored per task. Exact case-sensitive whitespace-token checker.',
                      'screening_exclusions': screening,
                      'criteria': {'primary': 'Fraction passing all original private tests, paired across conditions.',
                                   'secondary': 'Actual verifier execution, diagnostics, and subsequent revisions. Command mentions alone are not execution.',
                                   'interpretation': 'Report all tasks and rating bands. No task removal or replacement based on agent outcomes.'}})
    write_json(destination, selection)
    summary = {'reference_checks': len(tasks), 'failed': [],
               'selection_sha256': hashlib.sha256(destination.read_bytes()).hexdigest(),
               'checks': [{'id': row['id'], 'passed': True} for row in tasks]}
    write_json(output / 'summary.json', summary)
    write_json(output / 'screening.json', screening)
    print('Frozen 100 tasks:', destination)


if __name__ == '__main__':
    main()
