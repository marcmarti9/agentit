#!/usr/bin/env python3
"""Reproducible full ECC import and metadata generation; no network or upstream execution.

Run with --source pointing to a checkout of the reviewed commit. Default invocation
verifies the existing snapshot. --source-revision is for an independently pinned
offline archive; it is a reported revision, not a Git/signature verification.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from router.ecc import ECCError, LOCK, SOURCE, policy, safe_file, verify

BEGIN = '<!-- ECC-GENERATED BEGIN -->'
END = '<!-- ECC-GENERATED END -->'


def metadata(path: Path) -> dict:
    text = path.read_bytes().decode('utf-8')
    if not text.startswith('---\n'):
        raise ECCError(f'missing frontmatter: {path}')
    raw = yaml.safe_load(text.split('---', 2)[1])
    if not isinstance(raw, dict) or not raw.get('description'):
        raise ECCError(f'missing skill description: {path}')
    return raw


def source_files(source: Path) -> dict:
    entries = {}
    for base, dirs, files in os.walk(source, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in ('.git', 'node_modules', '__pycache__'))
        for name in dirs:
            if (Path(base) / name).is_symlink():
                raise ECCError(f'symlink source directory: {Path(base) / name}')
        for name in sorted(files):
            file = Path(base) / name
            rel = file.relative_to(source).as_posix()
            data = safe_file(source, rel).read_bytes()
            entries[rel] = {'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data),
                            'executable': bool(file.stat().st_mode & 0o111)}
    if 'LICENSE' not in entries or 'package.json' not in entries or 'scripts/ecc.js' not in entries:
        raise ECCError('source is not a complete ECC checkout')
    return dict(sorted(entries.items()))


def generate(repo: Path, source: Path, reported_revision: str | None = None) -> dict:
    p = policy(repo)
    source = source.absolute()
    if source.is_symlink() or not source.is_dir():
        raise ECCError('source must be a regular directory')
    if (source / '.git').exists():
        revision = subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip()
        dirty = subprocess.check_output(['git', '-C', str(source), 'status', '--porcelain'], text=True).strip()
        if dirty:
            raise ECCError('source checkout has uncommitted changes')
    else:
        revision = reported_revision
    if revision != p['revision']:
        raise ECCError(f'upstream revision must be exactly {p["revision"]}, received {revision}')
    files = source_files(source)
    all_skills = {f.split('/')[1] for f in files if f.count('/') == 2 and f.startswith('skills/') and f.endswith('/SKILL.md')}
    aliases = p['aliases']
    active = all_skills - aliases.keys()
    assigned = [sid for pack in p['packs'].values() for sid in pack['skills']]
    if len(assigned) != len(set(assigned)) or set(assigned) != active:
        raise ECCError(f'reviewed pack assignment differs from canonical upstream skills: missing={sorted(active-set(assigned))}, unknown={sorted(set(assigned)-active)}')
    native = {f.parent.name for f in (repo/'skills').glob('*/SKILL.md')}
    if active & native:
        raise ECCError(f'unreviewed skill ID collision: {sorted(active & native)}')
    for name, entry in aliases.items():
        if name not in all_skills or entry['canonical'] not in active | native:
            raise ECCError(f'invalid alias decision: {name}')
    target = repo / SOURCE
    if target.parent.is_symlink() or target.is_symlink():
        raise ECCError('symlink vendor target or parent rejected')
    if target.exists():
        verify(repo)  # Ownership and old-byte checks before any replacement.
        if source_files(target) != files:
            raise ECCError('existing pinned source differs; reconcile upstream update explicitly, never overwrite it silently')
    else:
        if target.is_symlink():
            raise ECCError('symlink vendor target rejected')
        target.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='.ecc-import-', dir=target.parent) as tmp:
            staged = Path(tmp) / 'ecc'
            staged.mkdir()
            for relative in files:
                dest = staged / relative
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(safe_file(source, relative), dest)
            os.replace(staged, target)
    skills = {}
    for sid in sorted(active):
        path = f'skills/{sid}/SKILL.md'
        m = metadata(target / path)
        description = ' '.join(str(m['description']).split())
        skills[sid] = {'path': path, 'description': description,
                       'pack': next(k for k,v in p['packs'].items() if sid in v['skills'])}
    resources = {}
    for kind, prefix in {'agents':'agents/', 'commands':'commands/', 'rules':'rules/', 'hooks':'hooks/',
                         'contexts':'contexts/', 'workflows':'workflows/', 'mcp':'mcp-configs/'}.items():
        resources[kind] = [f for f in files if f.startswith(prefix)]
    lock = {'schema_version': 1, 'repository': p['repository'], 'revision': p['revision'],
            'version': json.loads((target/'package.json').read_text())['version'],
            'files': files, 'skills': skills, 'aliases': aliases, 'resources': resources}
    (repo/LOCK).write_text(json.dumps(lock, indent=2, ensure_ascii=False)+'\n')
    catalogs(repo, p, lock)
    return verify(repo)


def catalogs(repo: Path, p: dict, lock: dict) -> None:
    path = repo/'profiles.yaml'
    data = yaml.safe_load(path.read_text())
    for name, additions in p['profile_additions'].items():
        profile = data['profiles'][name]
        profile['skills'] = list(dict.fromkeys([*profile.get('skills',[]), *additions]))
    for name, pack in p['packs'].items():
        data['profiles'][name] = {'description': pack['description']+' Availability only, never auto-activation.',
                                  'extends':['core'], 'skills':pack['skills']}
    data['profiles']['ecc'] = {'description':'Complete canonical ECC library, JIT only. Native host integration remains opt-in.',
                                'extends':['core', *p['packs']], 'skills':[]}
    data['profiles']['all']['extends'] = list(dict.fromkeys([*data['profiles']['all'].get('extends',[]), 'ecc']))
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=96))
    path=repo/'references/agentit-skill-packs.md'
    text=path.read_text()
    if BEGIN in text:
        text=text.split(BEGIN)[0].rstrip()+'\n'
    lines=[BEGIN, '', 'The full ECC source lives once in `vendor/ecc`. See `docs/ECC_INTEGRATION.md` for canonical owners, native tool setup and the explicit alias decisions.', '']
    for name, pack in p['packs'].items():
        lines += [f'## {name}', '', f'**Use for:** {pack["description"]}', '', '**Skills in this pack:**', '']
        for sid in pack['skills']:
            lines.append(f'- `{sid}` — {lock["skills"][sid]["description"]}')
        lines += ['', '---', '']
    lines.append(END)
    path.write_text(text.rstrip()+'\n\n'+'\n'.join(lines)+'\n')


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path)
    parser.add_argument('--source-revision')
    args=parser.parse_args()
    try:
        result=generate(ROOT,args.source,args.source_revision) if args.source else verify(ROOT)
        print(json.dumps(result,indent=2))
        return 0
    except (ECCError,OSError,ValueError,subprocess.CalledProcessError) as exc:
        parser.error(str(exc))
        return 2


if __name__=='__main__':
    raise SystemExit(main())
