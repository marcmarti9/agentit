"""Pinned ECC source and native tools behind Agentit's existing JIT boundary.

No natural-language routing, downloads, host installation or implicit activation.
The complete upstream tree stays intact; only the unified discovery view dedupes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LOCK = Path('vendor/ecc.lock.json')
POLICY = Path('references/ecc-policy.json')
SOURCE = Path('vendor/ecc')


class ECCError(ValueError):
    pass


def safe_file(root: Path, relative: str) -> Path:
    rel = PurePosixPath(relative)
    if (not relative or relative == '.' or rel.is_absolute() or '..' in rel.parts
            or '\\' in relative or rel.as_posix() != relative):
        raise ECCError(f'unsafe ECC path: {relative!r}')
    root = Path(root).absolute()
    if root.is_symlink():
        raise ECCError(f'symlink ECC root: {root}')
    # Resolve host ancestors (e.g. macOS /var -> /private/var), but never
    # a component within the declared repository/source boundary.
    root = root.resolve()
    target = root
    for part in rel.parts:
        target /= part
        if target.is_symlink():
            raise ECCError(f'symlink ECC path: {target}')
    if not target.is_file():
        raise ECCError(f'missing ECC file: {target}')
    return target


def policy(repo: Path = ROOT) -> dict[str, Any]:
    try:
        data = json.loads(safe_file(repo, POLICY.as_posix()).read_bytes())
        if data.get('schema_version') != 1 or not re.fullmatch(r'[0-9a-f]{40}', data['revision']):
            raise ECCError('invalid ECC integration policy')
        return data
    except (KeyError, TypeError, json.JSONDecodeError, OSError) as exc:
        raise ECCError(f'cannot load ECC policy: {exc}') from exc


def load_lock(repo: Path = ROOT) -> dict[str, Any] | None:
    path = Path(repo) / LOCK
    if not path.exists() and not path.is_symlink():
        # An ordinary Agentit fixture/checkout can legitimately have no ECC.
        if (Path(repo) / SOURCE).exists():
            raise ECCError('ECC source present without ownership/integrity lock')
        return None
    try:
        data = json.loads(safe_file(repo, LOCK.as_posix()).read_bytes())
        p = policy(repo)
        if (data.get('schema_version') != 1 or data.get('repository') != p['repository']
                or data.get('revision') != p['revision'] or not isinstance(data.get('files'), dict)
                or not isinstance(data.get('skills'), dict)):
            raise ECCError('ECC lock and reviewed source policy disagree')
        return data
    except (KeyError, TypeError, json.JSONDecodeError, OSError) as exc:
        raise ECCError(f'cannot load ECC lock: {exc}') from exc


def verified_bytes(repo: Path, relative: str, lock: dict[str, Any] | None = None) -> bytes:
    lock = load_lock(repo) if lock is None else lock
    if lock is None or relative not in lock['files']:
        raise ECCError(f'ECC file is not in the pinned source manifest: {relative}')
    target = safe_file(Path(repo), (SOURCE / relative).as_posix())
    content = target.read_bytes()
    entry = lock['files'][relative]
    if len(content) != entry['bytes'] or hashlib.sha256(content).hexdigest() != entry['sha256']:
        raise ECCError(f'ECC source integrity mismatch: {relative}')
    if sys.platform != 'win32' and bool(target.stat().st_mode & 0o111) != entry['executable']:
        # Yarn makes declared package executables runnable while linking bins.
        # Accept ONLY an added executable bit on a hash-verified, declared bin
        # after dependencies exist. All bytes and other modes remain checked.
        bins = {}
        if (not entry['executable'] and relative != 'package.json'
                and (Path(repo) / SOURCE / 'node_modules').is_dir()):
            package = json.loads(verified_bytes(repo, 'package.json', lock))
            bins = package.get('bin', {})
        declared = {bins} if isinstance(bins, str) else set(bins.values())
        if relative not in declared:
            raise ECCError(f'ECC source executable-mode mismatch: {relative}')
    return content


def verified_path(repo: Path, path: Path) -> None:
    """Verify ECC paths only; ordinary Agentit/project files retain their contract."""
    try:
        relative = path.absolute().relative_to((Path(repo) / SOURCE).absolute()).as_posix()
    except ValueError:
        return
    verified_bytes(repo, relative)


def verify_package(repo: Path, directory: Path) -> None:
    try:
        directory.absolute().relative_to((Path(repo) / SOURCE).absolute())
    except ValueError:
        return
    lock = load_lock(repo)
    prefix = directory.relative_to(Path(repo) / SOURCE).as_posix()+'/'
    expected = {name for name in lock['files'] if name.startswith(prefix)}
    actual = set()
    for path in directory.rglob('*'):
        if path.is_symlink():
            raise ECCError(f'symlink ECC package resource: {path}')
        if path.is_file():
            relative = path.relative_to(Path(repo) / SOURCE).as_posix()
            actual.add(relative)
            verified_bytes(repo, relative, lock)
    if actual != expected:
        raise ECCError(f'ECC package file inventory mismatch: {directory.name}')


def canonical_ids(repo: Path = ROOT) -> set[str]:
    lock = load_lock(repo)
    return set(lock['skills']) if lock else set()


def skill_dir(repo: Path, skill_id: str) -> Path:
    """Resolve a literal skill ID. Existing Agentit files keep precedence."""
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,63}', skill_id) or '--' in skill_id or skill_id.endswith('-'):
        raise ECCError(f'invalid ECC skill ID: {skill_id!r}')
    native = Path(repo) / 'skills' / skill_id
    if (native / 'SKILL.md').exists() or native.is_symlink():
        return native
    lock = load_lock(repo)
    if lock:
        alias = lock.get('aliases', {}).get(skill_id)
        if alias:
            raise ECCError(f'{skill_id} is a redundant ECC alias; select {alias["canonical"]} instead')
        entry = lock['skills'].get(skill_id)
        if entry:
            relative = entry['path']
            if relative != f'skills/{skill_id}/SKILL.md':
                raise ECCError(f'invalid ECC skill source mapping: {skill_id}')
            verified_bytes(repo, relative, lock)
            return Path(repo) / SOURCE / 'skills' / skill_id
    return native


def verify(repo: Path = ROOT) -> dict[str, Any]:
    lock = load_lock(repo)
    if lock is None:
        raise ECCError('ECC has not been materialized in this checkout')
    total = 0
    installed_bin_modes = []
    for relative in lock['files']:
        total += len(verified_bytes(repo, relative, lock))
        if (sys.platform != 'win32' and bool((Path(repo) / SOURCE / relative).stat().st_mode & 0o111)
                != lock['files'][relative]['executable']):
            installed_bin_modes.append(relative)
    return {'revision': lock['revision'], 'verified_files': len(lock['files']),
            'verified_bytes': total, 'canonical_ecc_skills': len(lock['skills']),
            'deduplicated_aliases': len(lock['aliases']), 'hooks_enabled_by_import': False,
            'installed_declared_bin_modes': installed_bin_modes}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog='agentit ecc', description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('status', help='Show pinned inventory, without enabling any component.')
    sub.add_parser('verify', help='Hash-verify the complete retained ECC source tree.')
    inventory = sub.add_parser('list', help='Discover one resource kind; content is not activated.')
    inventory.add_argument('--kind', choices=('skills', 'agents', 'commands', 'rules', 'hooks', 'contexts', 'workflows', 'mcp', 'aliases'), default='skills')
    resolve = sub.add_parser('resolve', help='Show the single canonical skill for a redundant name.')
    resolve.add_argument('skill_id')
    read = sub.add_parser('read', help='Read a pinned source file with its digest. No execution.')
    read.add_argument('path')
    run = sub.add_parser('run', help='Explicitly invoke the retained ECC native CLI; never auto-install.')
    run.add_argument('--allow-host-changes', action='store_true', help='Acknowledge that the selected native command may write host state. Requires task authorization.')
    run.add_argument('args', nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    try:
        lock = load_lock(ROOT)
        if lock is None:
            raise ECCError('ECC source absent; use the documented pinned import workflow')
        if args.command == 'status':
            value = {k: lock[k] for k in ('repository', 'revision', 'version')
}
            value.update(files=len(lock['files']), skills=len(lock['skills']), aliases=len(lock['aliases']),
                         resources={k: len(v) for k, v in lock['resources'].items()},
                         native_host_setup='not performed by import', integrity='run agentit ecc verify')
        elif args.command == 'verify':
            value = verify(ROOT)
        elif args.command == 'list':
            value = lock[args.kind] if args.kind in ('skills', 'aliases') else lock['resources'][args.kind]
        elif args.command == 'resolve':
            value = lock['aliases'].get(args.skill_id, {'canonical': args.skill_id})
            target = value['canonical']
            if target not in lock['skills'] and not (ROOT / 'skills' / target / 'SKILL.md').is_file():
                raise ECCError(f'unknown skill: {args.skill_id}')
        elif args.command == 'read':
            content = verified_bytes(ROOT, args.path, lock)
            value = {'path': str(SOURCE / args.path), 'upstream_revision': lock['revision'],
                     'sha256': hashlib.sha256(content).hexdigest(), 'bytes': len(content),
                     'authority': 'Source data, not permission to execute or override Agentit.',
                     'content': content.decode('utf-8')}
        else:
            command = args.args[1:] if args.args[:1] == ['--'] else args.args
            if 'auto-update' in command:
                raise ECCError('native auto-update cannot change a pinned source; review and re-import a new revision')
            if command not in ([], ['--help'], ['help'], ['-h']) and not args.allow_host_changes:
                raise ECCError('native ECC commands may modify host state; scoped authorization and --allow-host-changes are required')
            node = shutil.which('node')
            if not node:
                raise ECCError('Node.js is required only for native ECC execution, not skill delivery')
            if not (ROOT / SOURCE / 'node_modules').is_dir():
                raise ECCError('native dependencies absent; install the retained frozen lockfile with scripts disabled as documented in docs/ECC_INTEGRATION.md')
            verify(ROOT)
            # Keep cwd: ECC acts on the caller-selected project, not the vendor tree.
            return subprocess.run([node, str(ROOT / SOURCE / 'scripts/ecc.js'), *command], check=False).returncode
        print(json.dumps(value, indent=2, ensure_ascii=False))
        return 0
    except (ECCError, OSError, UnicodeError) as exc:
        parser.error(str(exc))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
