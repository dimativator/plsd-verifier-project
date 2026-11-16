"""Build isolated tool wrappers and record the installed verifier versions."""
import json
import importlib.metadata
from pathlib import Path
import shlex
import shutil
import subprocess

from python_pilot.runtime import digest, write_json


def main() -> None:
    project = Path(__file__).resolve().parents[1]
    root = project / 'python_pilot'
    python = '/opt/homebrew/opt/python@3.13/bin/python3.13'
    common = root / 'toolchains/common'
    (common / 'bin').mkdir(parents=True, exist_ok=True)
    (common / 'pythonpath').mkdir(exist_ok=True)
    shutil.copyfile(root / 'tools.py', common / 'tools.py')
    contracts = next((root / 'envs/nagini/lib').glob('python*/site-packages/nagini_contracts'))
    shutil.copytree(contracts, common / 'pythonpath/nagini_contracts', dirs_exist_ok=True)
    for alias in ['python', 'python3']:
        link = common / 'bin' / alias
        if not link.exists():
            link.symlink_to(python)
    write_json(common / 'config.json', {'python': python})
    configs = {'baseline': {'python': python}}
    for name in ['crosshair', 'nagini', 'esbmc']:
        directory = root / 'toolchains' / name
        (directory / 'bin').mkdir(parents=True, exist_ok=True)
        executable = (root / 'envs' / name / 'bin' / name) if name != 'esbmc' else directory / 'release/release/bin/esbmc'
        config = {'python': python, 'backend': name, 'executable': str(executable)}
        if name == 'nagini':
            config['z3'] = str(root / 'envs/nagini/bin/z3')
        write_json(directory / 'config.json', config)
        shutil.copyfile(root / 'guides' / (name + '.txt'), directory / 'GUIDE.txt')
        configs[name] = config
    for action in ['compile', 'run_tests', 'verify']:
        destinations = [common] if action != 'verify' else [root / 'toolchains' / n for n in ['crosshair', 'nagini', 'esbmc']]
        for directory in destinations:
            command = [python, str(common / 'tools.py'), '--config', str(directory / 'config.json'), 'test' if action == 'run_tests' else action]
            wrapper = directory / 'bin' / action
            wrapper.write_text('#!/bin/sh\nexec ' + shlex.join(command) + ' "$@"\n')
            wrapper.chmod(0o755)
    provenance = {'runtime_python': python, 'runtime_version': subprocess.check_output([python, '-V'], text=True).strip(),
                  'crosshair': '0.0.113', 'nagini': '1.3.1', 'esbmc': '8.6.0',
                  'mini_swe_agent': importlib.metadata.version('mini-swe-agent'),
                  'codex_cli': subprocess.check_output(['/opt/homebrew/bin/codex', '--version'], text=True).strip(),
                  'esbmc_relocated_binary_sha256': digest(root / 'toolchains/esbmc/release/release/bin/esbmc'),
                  'esbmc_native_dependencies': json.loads((root / 'toolchains/esbmc/native-dependencies.json').read_text()),
                  'configs': configs, 'common_tools_sha256': digest(common / 'tools.py')}
    for name in ['crosshair', 'nagini']:
        lock = subprocess.check_output(['/opt/homebrew/bin/uv', 'pip', 'freeze', '--python', str(root / 'envs' / name / 'bin/python')], text=True)
        (root / (name + '-requirements.lock.txt')).write_text(lock)
    write_json(root / 'toolchains/provenance.json', provenance)


if __name__ == '__main__':
    main()
