"""Materialize explicit selections; never infer intent or inherit a profile.

Receipts attest bytes delivered by this process, not model attention or sandboxing.
Project-native skills are intentional overrides. Private caches require ownership
and freshness evidence from the installer. Hashes are integrity checks, not signatures.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sys
from typing import Any, Iterable
import uuid

HARNESS_ROOT = Path(__file__).resolve().parents[1]
_SKILL_ID = re.compile(r'^[a-z0-9][a-z0-9-]*$')

class SkillLoadError(RuntimeError):
    pass

def _digest(content: str) -> str:
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def _dedupe(skill_ids: Iterable[str]) -> list[str]:
    if isinstance(skill_ids, (str, bytes)):
        raise SkillLoadError('skill IDs must be an explicit sequence')
    result: list[str] = []
    for raw in skill_ids:
        if not isinstance(raw, str) or not _SKILL_ID.fullmatch(raw) or len(raw)>64 or '--' in raw or raw.endswith('-'):
            raise SkillLoadError(f'invalid skill id: {raw!r}')
        if raw not in result:
            result.append(raw)
    return result

def _project(path: Path) -> Path:
    path = Path(path).absolute()
    # Check before resolve(): resolving first hides the evidence.
    if path.is_symlink() or not path.is_dir():
        raise SkillLoadError(f'project root must be a regular directory: {path}')
    return path.resolve()

def _safe_read(path: Path, *, trusted_root: Path) -> str | None:
    root = _project(trusted_root)
    path = Path(path).absolute()
    try:
        parts = path.relative_to(root).parts
    except ValueError as exc:
        raise SkillLoadError(f'path escapes trusted root: {path}') from exc
    if '..' in parts:
        raise SkillLoadError(f'parent traversal rejected: {path}')
    current = root
    for part in parts:
        current /= part
        if current.is_symlink():  # including dangling symlinks
            raise SkillLoadError(f'symlink rejected: {current}')
    if not path.exists():
        return None
    if not path.is_file():
        raise SkillLoadError(f'resource must be a regular file: {path}')
    return path.read_text(encoding='utf-8')

def _cache_file(project: Path, skill_id: str, relative: str, content: str) -> None:
    text = _safe_read(project/'.agentit/skills-manifest.json', trusted_root=project)
    if text is None:
        raise SkillLoadError(f'unmanaged private skill cache: {skill_id}; refresh the profile')
    try:
        manifest = json.loads(text)
        if manifest.get('schema_version') != 1:
            raise ValueError('unsupported manifest')
        meta = manifest['skills'][skill_id]
        destination = f'.agentit/profile-skills/{skill_id}/SKILL.md'
        if meta.get('managed') is not True or meta.get('destination') != destination:
            raise ValueError('ownership/destination mismatch')
        entry = meta.get('files', {}).get(relative)
        if entry is None and relative == 'SKILL.md':
            entry = meta  # compatible with older body-only managed manifests
        if not isinstance(entry, dict) or entry.get('managed') is not True:
            raise ValueError('resource not managed')
        if entry.get('installed_sha256') != _digest(content):
            raise ValueError('installed hash mismatch')
        canonical = _safe_read(HARNESS_ROOT/'skills'/skill_id/relative, trusted_root=HARNESS_ROOT)
        if canonical is not None and entry.get('source_sha256') != _digest(canonical):
            raise ValueError('cache source is stale relative to the current harness')
    except (KeyError, TypeError, AttributeError, ValueError) as exc:
        raise SkillLoadError(f'invalid/stale private skill cache {skill_id}/{relative}: {exc}; refresh the profile') from exc

def _body(identifier: str, source: str, path: Path, root: Path, content: str) -> dict[str, Any]:
    if not content.strip():
        raise SkillLoadError(f'empty selected resource: {identifier}')
    return {'id': identifier, 'source': source, 'path': path.relative_to(root).as_posix(),
            'resource_root': str(root), 'skill_root': str(path.parent),
            'sha256': _digest(content), 'bytes': len(content.encode('utf-8')), 'content': content}

def load_skill_bodies(skill_ids: Iterable[str], *, project_root: Path) -> list[dict[str, Any]]:
    project = _project(project_root)
    loaded = []
    for skill_id in _dedupe(skill_ids):
        candidates = (
            ('project', project/'.agents/skills'/skill_id/'SKILL.md', project),
            ('project-agentit-profile', project/'.agentit/profile-skills'/skill_id/'SKILL.md', project),
            ('harness', HARNESS_ROOT/'skills'/skill_id/'SKILL.md', HARNESS_ROOT),
        )
        for source, path, root in candidates:
            content = _safe_read(path, trusted_root=root)
            if content is None:
                continue
            if source == 'project-agentit-profile':
                _cache_file(project, skill_id, 'SKILL.md', content)
            loaded.append(_body(skill_id, source, path, root, content))
            break
        else:
            raise SkillLoadError(f'selected skill body unavailable: {skill_id}')
    return loaded

def load_reference_bodies(locators: Iterable[str], *, project_root: Path) -> list[dict[str, Any]]:
    """Read exact UTF-8 resources. External URIs require the host's read tool.

    Supported: repo:references/x.md, project:docs/x.md, skill:ID/references/x.md.
    No code execution, network fetch, implicit dependency expansion or traversal.
    """
    project = _project(project_root)
    result = []
    if isinstance(locators, (str, bytes)):
        raise SkillLoadError("resource locators must be an explicit sequence")
    seen: set[str] = set()
    for locator in locators:
        if not isinstance(locator, str) or ':' not in locator:
            raise SkillLoadError(f'resource needs an explicit root: {locator!r}')
        if locator in seen:
            continue
        seen.add(locator)
        source, relative = locator.split(':', 1)
        parts = Path(relative).parts
        if not relative or Path(relative).is_absolute() or '..' in parts or '\\' in relative:
            raise SkillLoadError(f'invalid resource path: {locator!r}')
        cache_skill = None
        if source == 'repo':
            root = HARNESS_ROOT; path = root/relative
        elif source == 'project':
            root = project; path = root/relative
        elif source == 'skill':
            skill_id, sep, resource = relative.partition('/')
            if not sep or not resource:
                raise SkillLoadError('skill resource must name a file')
            skill = load_skill_bodies([skill_id], project_root=project)[0]
            root = Path(skill['resource_root']); path = Path(skill['skill_root'])/resource
            if skill['source'] == 'project-agentit-profile':
                cache_skill = (skill_id, resource)
        else:
            raise SkillLoadError(f'unsupported resource root: {source}; use the host read tool')
        content = _safe_read(path, trusted_root=root)
        if content is None:
            raise SkillLoadError(f'selected resource unavailable: {locator}')
        if cache_skill:
            _cache_file(project, *cache_skill, content)
        result.append(_body(locator, source, path, root, content))
    return result

def validate_bodies(ids: list[str], bodies: list[dict[str, Any]]) -> None:
    if (not isinstance(bodies, list) or any(not isinstance(b, dict) for b in bodies)
            or [b.get('id') for b in bodies] != ids):
        raise SkillLoadError('delivered bodies do not match the exact selection')
    for body in bodies:
        content = body.get('content')
        if not isinstance(content, str) or not content.strip() or body.get('sha256') != _digest(content):
            raise SkillLoadError('delivered body missing, empty or hash-mismatched')
        if body.get('bytes') != len(content.encode('utf-8')):
            raise SkillLoadError('delivered body byte count mismatch')

def delivery_receipt(bodies: list[dict[str, Any]], *, task_id: str, stage: str, context_origin: str='unspecified') -> dict[str, Any]:
    if not task_id.strip() or not stage.strip():
        raise SkillLoadError('delivery receipt requires explicit task_id and stage')
    validate_bodies([b['id'] for b in bodies], bodies)
    return {'schema_version': 1, 'kind': 'agentit.context.delivery',
            'task_id': task_id, 'stage': stage, 'context_origin': context_origin,
            'created_at': datetime.now(timezone.utc).isoformat(),
            'resources': [{k: b[k] for k in ('id','source','path','sha256','bytes')} for b in bodies],
            'delivered_bytes': sum(b['bytes'] for b in bodies),
            'proves_model_compliance': False, 'proves_context_erasure': False}

def write_delivery_receipt(receipt: dict[str, Any], *, project_root: Path) -> Path:
    root = _project(project_root)
    directory = root
    for part in ('.agentit','context'):
        directory /= part
        if directory.is_symlink():
            raise SkillLoadError(f'symlink receipt directory rejected: {directory}')
        directory.mkdir(mode=0o700, exist_ok=True)
    path = directory/f'{uuid.uuid4().hex}.json'
    fd = os.open(path, os.O_WRONLY|os.O_CREAT|os.O_EXCL, 0o600)
    with os.fdopen(fd,'w',encoding='utf-8') as handle:
        json.dump(receipt,handle,ensure_ascii=False,indent=2); handle.write('\n')
    return path

def render_prompt(skills: list[dict[str, Any]]) -> str:
    validate_bodies([s['id'] for s in skills], skills)
    lines = ['# Delivered Agentit Skill Bodies',
             'Skill IDs alone do not count as activation. These exact bodies are delivered, not proof they were followed.',
             'Host safety and explicit task/project constraints govern. Upstream workflow suggestions do not auto-select other skills,',
             'grant tools, mandate unrelated stages, or override the task scope. Report unavailable review/isolation honestly.']
    for skill in skills:
        lines.extend(['',f"## Skill: {skill['id']}",f"Source: {skill['source']}:{skill['path']}",
                      f"Resource root: {skill['resource_root']}", f"Skill root: {skill['skill_root']}",
                      f"SHA256: {skill['sha256']}",'',skill['content'].rstrip()])
    lines.extend(['','# Skill Load Receipt'])
    lines.extend(f"- {s['id']} {s['sha256']} ({s['bytes']} bytes)" for s in skills)
    return '\n'.join(lines)+'\n'

def main(argv: list[str] | None=None) -> int:
    parser=argparse.ArgumentParser(description='Load task-scoped Agentit bodies.')
    parser.add_argument('skill_ids',nargs='+'); parser.add_argument('--project',type=Path,default=Path.cwd())
    parser.add_argument('--format',choices=('prompt','json'),default='prompt')
    args=parser.parse_args(argv)
    try:
        skills=load_skill_bodies(args.skill_ids,project_root=args.project)
        print(json.dumps({'schema_version':1,'skills':skills},ensure_ascii=False,indent=2) if args.format=='json' else render_prompt(skills),end='\n')
        return 0
    except (SkillLoadError,OSError,UnicodeError) as exc:
        print(f'ERROR: {exc}',file=sys.stderr); return 2

if __name__=='__main__':
    raise SystemExit(main())
