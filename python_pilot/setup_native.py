"""Fetch verified Homebrew bottles into a local, relocatable ESBMC dependency tree."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import subprocess
import urllib.request

ROOT = Path(__file__).resolve().parent / 'toolchains/esbmc'


def fetch(name: str) -> dict:
    metadata = json.load(urllib.request.urlopen('https://formulae.brew.sh/api/formula/' + name + '.json'))
    bottle = metadata['bottle']['stable']['files']['arm64_tahoe']
    repository = 'homebrew/core/' + name.replace('@', '/')
    token = json.load(urllib.request.urlopen('https://ghcr.io/token?service=ghcr.io&scope=repository:' + repository + ':pull'))['token']
    archive = ROOT / (name + '.tar.gz')
    if not archive.exists() or hashlib.file_digest(archive.open('rb'), 'sha256').hexdigest() != bottle['sha256']:
        offset = archive.stat().st_size if archive.exists() else 0
        headers = {'Authorization': 'Bearer ' + token}
        if offset:
            headers['Range'] = f'bytes={offset}-'
        request = urllib.request.Request(bottle['url'], headers=headers)
        response = urllib.request.urlopen(request)
        append = offset and response.status == 206
        print('Downloading', name, 'resume' if append else 'fresh', offset, flush=True)
        with response, archive.open('ab' if append else 'wb') as target:
            while chunk := response.read(1024 * 1024):
                target.write(chunk)
    digest = hashlib.file_digest(archive.open('rb'), 'sha256').hexdigest()
    if digest != bottle['sha256']:
        raise ValueError('Checksum mismatch: ' + name)
    cellar = ROOT / 'cellar'
    cellar.mkdir(exist_ok=True)
    subprocess.run(['tar', '-xzf', str(archive), '-C', str(cellar)], check=True)
    print('Fetched', name, metadata['versions']['stable'], flush=True)
    return {'name': name, 'version': metadata['versions']['stable'], 'url': bottle['url'], 'sha256': digest}


def main() -> None:
    with ThreadPoolExecutor(max_workers=4) as pool:
        records = list(pool.map(fetch, ['z3', 'boost', 'llvm@21', 'icu4c@79', 'xz', 'zstd', 'gmp', 'mpfr']))
    (ROOT / 'native-dependencies.json').write_text(json.dumps(records, indent=2) + '\n')
    libraries = list((ROOT / 'cellar').glob('**/lib/*.dylib'))
    by_name = {path.name: path.resolve() for path in libraries}
    by_name['libz3.5.1.dylib'] = by_name['libz3.dylib']
    binary = ROOT / 'release/release/bin/esbmc'
    files = {p.resolve() for p in libraries} | {binary}
    for path in files:
        lines = subprocess.check_output(['otool', '-L', str(path)], text=True).splitlines()[1:]
        for line in lines:
            old = line.strip().split(' (')[0]
            if old.startswith('/opt/homebrew/') or old.startswith('@@HOMEBREW_'):
                name = Path(old).name
                if name not in by_name:
                    raise ValueError(f'Unresolved dependency {old} in {path}')
                subprocess.run(['install_name_tool', '-change', old, str(by_name[name]), str(path)], check=True)
        subprocess.run(['codesign', '--force', '--sign', '-', str(path)], check=True, capture_output=True)
    result = subprocess.run([str(binary), '--version'], text=True, capture_output=True)
    print(result.stdout, result.stderr)
    if result.returncode:
        raise RuntimeError('Relocated ESBMC does not start')


if __name__ == '__main__':
    main()
