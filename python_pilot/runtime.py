"""Shared environment and immutable file helpers for the Python experiment."""
import hashlib
import json
from pathlib import Path
import tempfile

from pilot.sandbox import environment


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode='w', dir=path.parent, delete=False) as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False)
        stream.write('\n')
        temporary = Path(stream.name)
    temporary.replace(path)


def digest(path: Path) -> str | None:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() and not path.is_symlink() else None


def execution_environment(workspace: Path, common: Path, verifier: Path | None) -> dict[str, str]:
    bins = ([verifier / 'bin'] if verifier else []) + [common / 'bin']
    env = environment(workspace, bins)
    env['PYTHONPATH'] = str(common / 'pythonpath')
    env['PYTHONNOUSERSITE'] = '1'
    env['JAVA_HOME'] = '/Library/Java/JavaVirtualMachines/temurin-21.jdk/Contents/Home'
    if verifier:
        config = json.loads((verifier / 'config.json').read_text())
        if config.get('library_paths'):
            env['DYLD_LIBRARY_PATH'] = ':'.join(config['library_paths'])
    return env


def tool_events(output: str) -> list[dict]:
    events = []
    for line in output.splitlines():
        if line.startswith('PLSD_TOOL_EVENT '):
            try:
                events.append(json.loads(line[len('PLSD_TOOL_EVENT '):]))
            except json.JSONDecodeError:
                pass
    return events
