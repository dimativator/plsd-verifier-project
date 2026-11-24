"""Offline distributed-protocol checks; no Docker, credentials or model calls."""
from copy import deepcopy
from decimal import Decimal
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from experiments import distributed as d


class DistributedTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='plinse-distributed-')
        self.root = Path(self.tmp.name)
        self.manifest = self.root / 'manifest.json'
        tasks = [dict(id=f'task-{band}-{i}', checker='integer_tokens')
                 for band in range(2) for i in range(2)]
        self.write(self.manifest, {'tasks': tasks})
        self.specs = []
        for rep in range(1, 7):
            for task in tasks:
                for arm in ['verifier', 'baseline', 'guided_verifier']:
                    self.specs.append(dict(phase='main', model='gpt-5.6-luna', task_id=task['id'],
                        family_id=task['id'], rating_band='2000-2399' if '-0-' in task['id'] else '2400+',
                        condition=arm, repetition=rep))
        self.image = {'Id': 'sha256:origin-index', 'Os': 'linux', 'Architecture': 'amd64',
                      'RootFS': {'Layers': ['sha256:layer-one', 'sha256:layer-two']},
                      'Config': {'Env': ['A=1'], 'Cmd': ['python3'], 'User': '65534:65534', 'WorkingDir': '/work'}}
        self.config = dict(output='C:/origin/batch', spend_root='C:/origin/spend',
            total_cap_usd='10.00', per_run_cap_usd='0.12', parallel_workers=8,
            max_output_tokens=16384, step_limit=100, solve_limit_seconds=600, effort='medium',
            runtime={'mini_swe_agent': '2.4.6', 'python': 'origin-controller',
                     'source_sha256': {}, 'image_ids': {'image:test': self.image['Id']}})
        self.original = self.root / 'global.json'
        self.write(self.original, {'runs': self.specs, 'config': self.config,
                                  'manifest_sha256': d.run.source_hash(self.manifest)})
        self.alloc = {w: {'families_by_band': {'2000-2399': 1, '2400+': 1}, 'total_cap_usd': '5.00'}
                      for w in ['ours', 'friend']}
        self.images = patch.object(d, '_inspect_image', return_value=deepcopy(self.image))
        self.images.start()
        self.plan = d.create_plan(self.original, self.root / 'plan', workers=self.alloc)

    def tearDown(self):
        self.images.stop()
        self.tmp.cleanup()

    @staticmethod
    def write(path, value):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value), encoding='utf-8')

    def prepare(self, owner='ours', **kwargs):
        with patch.object(d, 'validate_environment', return_value={'image:test': 'sha256:local-config'}):
            return d.worker(self.plan, owner, self.manifest, self.root / owner, **kwargs)

    def raw(self, root, spec, config, **changes):
        directory = d._result_path(root, spec).parent
        directory.mkdir(parents=True, exist_ok=True)
        (directory / 'main.py').write_text('print(1)\n', encoding='utf-8')
        row = dict(**spec, valid_run=True, hidden_passed=False, exit_status='Submitted',
                   infrastructure_error=None, model_cost_usd=0.0, cost_is_upper_bound=False,
                   solve_seconds=1, evaluation_seconds=1,
                   submission_sha256=d.run.source_hash(directory / 'main.py'),
                   model_settings={k: config[k] for k in ['effort', 'max_output_tokens']})
        row.update(changes)
        self.write(directory / 'result.json', row)
        self.write(directory / 'spec.json', {**spec, 'limits': config})
        return row

    def populate(self, owner):
        self.prepare(owner)
        root = self.root / owner
        expected = d._read(root / 'expected.json')
        for spec in expected['runs']:
            self.raw(root, spec, expected['config'])
        self.write(root / 'spend/ledger.json', {'limits': {'total': '5.00', 'per_run': '0.12'},
                                              'reservations': {}})
        return root

    def test_stratified_whole_family_assignment_preserves_global_order(self):
        self.assertEqual(len(self.plan['runs']), 72)
        for owner in ['ours', 'friend']:
            specs = [s for s in self.plan['runs'] if s['worker_id'] == owner]
            self.assertEqual(len(specs), 36)
            self.assertEqual({s['analysis_stratum'] for s in specs}, {owner + ':2000-2399', owner + ':2400+'})
            for family in self.plan['workers'][owner]['families']:
                self.assertEqual(len([s for s in specs if s['family_id'] == family]), 18)
        self.assertEqual([d._key(s) for s in self.plan['runs']], [d._key(s) for s in self.specs])
        self.assertNotIn('output', self.plan['shared_config'])
        self.assertNotIn('spend_root', self.plan['shared_config'])
        self.assertEqual(d.create_plan(self.original, self.root / 'plan', workers=self.alloc), self.plan)

    def test_missing_arm_and_overallocated_budget_reject(self):
        value = d._read(self.original)
        value['runs'].pop()
        self.write(self.original, value)
        with self.assertRaisesRegex(ValueError, 'all three arms'):
            d.create_plan(self.original, self.root / 'bad', workers=self.alloc)
        self.write(self.original, {'runs': self.specs, 'config': self.config,
                                  'manifest_sha256': d.run.source_hash(self.manifest)})
        over = deepcopy(self.alloc)
        over['ours']['total_cap_usd'] = '8.00'
        with self.assertRaisesRegex(ValueError, 'exceed'):
            d.create_plan(self.original, self.root / 'bad', workers=over)

    def test_portable_image_same_content_different_store_id_and_changed_layer(self):
        different = deepcopy(self.image)
        different['Id'] = 'sha256:classic-config-id'
        with patch.object(d.metadata, 'version', return_value='2.4.6'), \
             patch.object(d, '_inspect_image', return_value=different), \
             patch.object(d, 'verify_retry_environment') as verify:
            ids = d.validate_environment(self.plan, [])
        self.assertEqual(ids, {'image:test': 'sha256:classic-config-id'})
        self.assertEqual(verify.call_args.args[0]['runtime']['image_ids'], ids)
        different['RootFS']['Layers'][0] = 'sha256:changed'
        with patch.object(d.metadata, 'version', return_value='2.4.6'), \
             patch.object(d, '_inspect_image', return_value=different):
            with self.assertRaisesRegex(ValueError, 'image content changed'):
                d.validate_environment(self.plan, [])

    def test_wrong_actual_agent_version_precedes_credentials(self):
        with patch.object(d.metadata, 'version', return_value='2.5.0'), patch.object(d.run, 'load_key') as key:
            with self.assertRaisesRegex(ValueError, '2.4.6'):
                d.worker(self.plan, 'ours', self.manifest, self.root / 'ours', prepare_only=False)
        key.assert_not_called()

    def test_prepare_no_credentials_local_paths_and_immutable_expected(self):
        with patch.object(d.run, 'load_key') as key, patch.object(d.run, 'execute') as execute:
            report = self.prepare()
        key.assert_not_called()
        execute.assert_not_called()
        self.assertFalse(report['credentials_loaded'])
        self.assertFalse((self.root / 'ours/spend/ledger.json').exists())
        expected = d._read(self.root / 'ours/expected.json')
        self.assertEqual(expected['config']['output'], str((self.root / 'ours').resolve()))
        self.assertEqual(expected['config']['total_cap_usd'], '5.00')
        with self.assertRaisesRegex(ValueError, 'frozen file differs'):
            self.prepare(workers=4)

    def test_manifest_drift_and_partial_attempt_stop_before_key(self):
        self.prepare()
        spec = next(s for s in self.plan['runs'] if s['worker_id'] == 'ours')
        d._result_path(self.root / 'ours', spec).parent.mkdir(parents=True)
        with patch.object(d.run, 'load_key') as key:
            with self.assertRaisesRegex(ValueError, 'Incomplete original attempt'):
                self.prepare(prepare_only=False)
        key.assert_not_called()
        self.manifest.write_text('{}', encoding='utf-8')
        with patch.object(d.run, 'load_key') as key:
            with self.assertRaisesRegex(ValueError, 'manifest changed'):
                self.prepare(prepare_only=False)
        key.assert_not_called()

    def test_execute_preserves_completed_wrong_answers_and_skips_on_resume(self):
        self.prepare()
        root = self.root / 'ours'
        expected = d._read(root / 'expected.json')
        first = expected['runs'][0]
        self.raw(root, first, expected['config'], exit_status='budget_exhausted')
        called = []

        def fake(task, spec, config, ledger, key):
            self.assertEqual(key, 'unit-test-only')
            self.assertEqual(spec['worker_id'], 'ours')
            called.append(d._key(spec))
            return self.raw(Path(config['output']), spec, config)

        with patch.object(d.run, 'load_key', return_value='unit-test-only') as key, \
             patch.object(d.run, 'execute', side_effect=fake), patch('builtins.print'):
            self.prepare(prepare_only=False)
            self.prepare(prepare_only=False)
        self.assertEqual(len(called), 35)
        self.assertNotIn(d._key(first), called)
        self.assertEqual(key.call_count, 1)

    def test_merge_complete_and_missing_keep_original_denominator(self):
        ours = self.populate('ours')
        friend = self.populate('friend')
        report = d.merge(self.plan, {'ours': ours, 'friend': friend}, self.root / 'merged')
        self.assertTrue(report['complete'])
        self.assertEqual(report['selected_runs'], 72)
        self.assertEqual(report['all_attempt_cost_usd'], '0')
        missing = d.merge(self.plan, {'ours': ours}, self.root / 'partial')
        self.assertFalse(missing['complete'])
        rows = d._read(self.root / 'partial/merged-results.json')
        self.assertEqual(len(rows), 72)
        self.assertEqual(sum(r['exit_status'] == 'missing_planned_run' for r in rows), 36)

    def test_merge_rejects_wrong_owner_duplicate_hash_and_resource_drift(self):
        ours = self.populate('ours')
        expected = d._read(ours / 'expected.json')
        spec = expected['runs'][0]
        path = d._result_path(ours, spec)
        row = d._read(path)
        altered = deepcopy(row)
        altered['worker_id'] = 'friend'
        self.write(path, altered)
        with self.assertRaisesRegex(ValueError, 'owner or stratum'):
            d.merge(self.plan, {'ours': ours}, self.root / 'bad')
        self.write(path, row)
        self.write(ours / 'resolved-results.json', [row, row])
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            d.merge(self.plan, {'ours': ours / 'resolved-results.json'}, self.root / 'bad')
        (path.parent / 'main.py').write_text('print(2)\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Submission hash'):
            d.merge(self.plan, {'ours': ours}, self.root / 'bad')
        (path.parent / 'main.py').write_text('print(1)\n', encoding='utf-8')
        expected['config']['step_limit'] = 101
        self.write(ours / 'expected.json', expected)
        with self.assertRaisesRegex(ValueError, 'resource settings differ'):
            d.merge(self.plan, {'ours': ours}, self.root / 'bad')

    def test_merge_selected_retry_once_retains_all_attempt_charges(self):
        ours = self.populate('ours')
        expected = d._read(ours / 'expected.json')
        spec = expected['runs'][0]
        retry = ours.with_name(ours.name + '-infra-retry-1')
        config = deepcopy(expected['config'])
        config['output'] = str(retry)
        row = self.raw(retry, spec, config, hidden_passed=True, model_cost_usd=.02)
        row['resolution'] = {'selected_attempt': 'infra-retry-1', 'original_batch': 'C:/foreign/ours'}
        self.write(ours / 'resolved-results.json', [row])
        suffix = '/'.join(str(spec[k]) for k in d.IDENTITY)
        self.write(ours / 'spend/ledger.json', {'limits': {'total': '5.00', 'per_run': '.12'}, 'reservations': {
            'old': {'run_id': 'ours/' + suffix, 'status': 'pending', 'reserved': '.04'},
            'new': {'run_id': 'ours-infra-retry-1/' + suffix, 'status': 'settled', 'reserved': '.03', 'charged': '.02'}}})
        report = d.merge(self.plan, {'ours': ours / 'resolved-results.json'}, self.root / 'selected')
        self.assertEqual(report['selected_runs'], 1)
        self.assertEqual(Decimal(report['known_all_attempt_cost_usd']), Decimal('.06'))
        self.assertEqual(report['selected_result_cost_usd'], .02)
        self.assertEqual(len(d._read(self.root / 'selected/merged-results.json')), 72)

    def round_plan(self):
        tasks = [dict(id=f'round-task-{i}', checker='integer_tokens') for i in range(100)]
        self.write(self.manifest, {'tasks': tasks})
        specs = [dict(phase='main', model='gpt-5.6-luna', task_id=task['id'], family_id=task['id'],
                      rating_band='2000-2399' if index < 50 else '2400+', condition=arm, repetition=rep)
                 for rep in range(1, 6) for index, task in enumerate(tasks) for arm in sorted(d.ARMS)]
        config = {**self.config, 'total_cap_usd': '140.00'}
        self.write(self.original, {'runs': specs, 'config': config,
                                  'manifest_sha256': d.run.source_hash(self.manifest)})
        return d.create_round_plan(self.original, self.root / 'round-plan')

    def test_round_assignment_five_repetitions_shared_140_cap_rating_only(self):
        plan = self.round_plan()
        self.assertEqual(len(plan['runs']), 1500)
        self.assertEqual(sum(Decimal(w['total_cap_usd']) for w in plan['workers'].values()), Decimal('140'))
        self.assertEqual(plan['analysis_plan']['strata'], 'rating_band')
        for owner, reps, count, ceiling in [('ours', {1, 2, 3}, 900, '108.00'), ('friend', {4, 5}, 600, '72.00')]:
            specs = [s for s in plan['runs'] if s['worker_id'] == owner]
            self.assertEqual(len(specs), count)
            self.assertEqual({s['repetition'] for s in specs}, reps)
            self.assertEqual(len(plan['workers'][owner]['families']), 100)
            self.assertEqual(Decimal(plan['workers'][owner]['normal_run_ceiling_usd']), Decimal(ceiling))
        self.assertTrue(all('analysis_stratum' not in s for s in plan['runs']))
        self.assertEqual(d._load_plan(plan), plan)
        invalid = deepcopy(plan)
        invalid['runs'][0]['worker_id'] = 'friend'
        invalid['plan_sha256'] = d._digest({k: v for k, v in invalid.items() if k != 'plan_sha256'})
        with self.assertRaisesRegex(ValueError, 'ownership'):
            d._load_plan(invalid)
        merged = d.merge(plan, {}, self.root / 'round-missing')
        self.assertEqual(merged['planned_runs'], 1500)
        self.assertEqual(merged['missing_runs'], 1500)
        self.assertFalse(merged['complete'])

    def test_round_admission_stops_before_denied_round_without_agent_failures(self):
        plan = self.round_plan()
        state = {'accounted_usd': '0', 'limits': {'total': '84.00', 'per_run': '.12'}, 'reservations': {}}
        spent = {**state, 'accounted_usd': '50.00'}
        called = []

        def fake(task, spec, config, ledger, key):
            called.append(spec)
            return {**spec, 'exit_status': 'Submitted', 'model_cost_usd': 0}

        with patch.object(d, 'validate_environment', return_value={'image:test': 'sha256:local-config'}), \
             patch.object(d, 'SpendLedger') as ledger, \
             patch.object(d.run, 'load_key', return_value='unit-test-only'), \
             patch.object(d.run, 'execute', side_effect=fake), patch('builtins.print'):
            ledger.return_value.snapshot.side_effect = [state, spent, spent]
            report = d.worker(plan, 'ours', self.manifest, self.root / 'round-worker', prepare_only=False)
        self.assertEqual(len(called), 300)
        self.assertEqual({s['repetition'] for s in called}, {1})
        self.assertEqual(report['completed_runs'], 300)
        self.assertEqual(report['pending_runs'], 600)
        self.assertEqual(report['not_launched_repetitions'], [2, 3])
        self.assertEqual(report['status'], 'budget_stop_before_round')
        self.assertEqual(Decimal(report['budget_stop']['required_usd']), Decimal('40'))
        self.assertFalse(any((self.root / 'round-worker').glob('*/*/*/rep-*/result.json')))
        frozen = d._read(self.root / 'round-worker/expected.json')
        self.assertEqual(len(frozen['runs']), 900)

    def test_round_denied_initially_loads_no_credentials_or_runs(self):
        plan = self.round_plan()
        with patch.object(d, 'validate_environment', return_value={'image:test': 'sha256:local-config'}), \
             patch.object(d, 'SpendLedger') as ledger, \
             patch.object(d.run, 'load_key') as key, patch.object(d.run, 'execute') as execute:
            ledger.return_value.snapshot.return_value = {'accounted_usd': '50.00'}
            report = d.worker(plan, 'ours', self.manifest, self.root / 'denied', prepare_only=False)
        key.assert_not_called()
        execute.assert_not_called()
        self.assertEqual(report['pending_runs'], 900)
        self.assertFalse(report['credentials_loaded'])
        self.assertEqual(report['not_launched_repetitions'], [1, 2, 3])

    def test_family_mode_retains_normal_ceiling_guard(self):
        low = deepcopy(self.alloc)
        low['ours']['total_cap_usd'] = '1.00'
        with self.assertRaisesRegex(ValueError, 'Normal planned runs exceed worker cap'):
            d.create_plan(self.original, self.root / 'low-cap-family', workers=low)


if __name__ == '__main__':
    unittest.main()
