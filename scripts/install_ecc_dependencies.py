#!/usr/bin/env python3
"""Install pinned native ECC dependencies without changing retained source bytes."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from router.ecc import ECCError, SOURCE, load_lock, safe_file, verified_bytes, verify


def strict_json(data: bytes):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ECCError(f'duplicate manifest key: {key}')
            result[key] = value
        return result
    def invalid(value):
        raise ECCError(f'non-JSON manifest number: {value}')
    return json.loads(data, object_pairs_hook=pairs, parse_constant=invalid)


def restore_manifest(repo: Path, original: bytes) -> dict:
    lock = load_lock(repo)
    expected = lock['files']['package.json']
    if (hashlib.sha256(original).hexdigest() != expected['sha256']
            or len(original) != expected['bytes']):
        raise ECCError('original manifest does not match the pinned source')
    path = safe_file(repo, (SOURCE / 'package.json').as_posix())
    observed = path.read_bytes()
    # Canonical JSON distinguishes booleans, numbers and strings; duplicate keys
    # and NaN/Infinity are refused rather than hidden by ordinary dict equality.
    normalize = lambda data: json.dumps(strict_json(data), sort_keys=True,
                                        ensure_ascii=False, allow_nan=False)
    if normalize(observed) != normalize(original):
        raise ECCError('native installer changed manifest semantics; source retained for inspection')
    for relative in lock['files']:
        if relative != 'package.json':
            verified_bytes(repo, relative, lock)
    restored = observed != original
    if restored:
        mode = path.stat().st_mode & 0o777
        fd, temporary = tempfile.mkstemp(prefix='.agentit-manifest-', dir=path.parent)
        try:
            with os.fdopen(fd, 'wb') as output:
                output.write(original)
                output.flush()
                os.fsync(output.fileno())
            os.chmod(temporary, mode)
            if safe_file(repo, (SOURCE / 'package.json').as_posix()).read_bytes() != observed:
                raise ECCError('manifest changed concurrently; refusing restoration')
            os.replace(temporary, path)
        finally:
            Path(temporary).unlink(missing_ok=True)
    return {'format_only_restoration': restored,
            'installer_manifest_sha256': hashlib.sha256(observed).hexdigest(),
            'source': verify(repo)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true', help='Execute the native dependency installation.')
    args = parser.parse_args()
    try:
        verify(ROOT)
        original = verified_bytes(ROOT, 'package.json')
        manager = strict_json(original).get('packageManager', '')
        if not isinstance(manager, str) or not re.fullmatch(r'yarn@\d+\.\d+\.\d+\+sha512\.[0-9a-f]+', manager):
            raise ECCError('native manager must be an exact integrity-pinned Yarn version')
        command = ['corepack', 'yarn', 'install', '--immutable', '--mode=skip-build']
        if not args.apply:
            print(json.dumps({'mode': 'plan', 'manager': manager, 'command': command}))
            return 0
        env = dict(os.environ, COREPACK_DEFAULT_TO_LATEST='0', COREPACK_ENABLE_AUTO_PIN='0',
                   YARN_ENABLE_SCRIPTS='false')
        subprocess.run(command, cwd=ROOT / SOURCE, env=env, check=True)
        print(json.dumps(restore_manifest(ROOT, original), indent=2))
        return 0
    except (ECCError, OSError, ValueError, subprocess.CalledProcessError) as exc:
        parser.error(str(exc))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
