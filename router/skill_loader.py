"""Resolve selected Agentit skill IDs to the exact bodies the active model must read."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable

HARNESS_ROOT = Path(__file__).resolve().parents[1]
_SKILL_ID = re.compile(r"^[a-z0-9][a-z0-9-]*$")


class SkillLoadError(RuntimeError):
    pass


def _dedupe(skill_ids: Iterable[str]) -> list[str]:
    result: list[str] = []
    for raw in skill_ids:
        skill_id = str(raw).strip()
        if not skill_id:
            continue
        if not _SKILL_ID.fullmatch(skill_id):
            raise SkillLoadError(f"invalid skill id: {skill_id!r}")
        if skill_id not in result:
            result.append(skill_id)
    return result


def _safe_read(path: Path, *, trusted_root: Path) -> str | None:
    if not path.exists():
        return None
    root = trusted_root.resolve()
    current = path
    while current != root and current != current.parent:
        if current.is_symlink():
            raise SkillLoadError(f"symlink rejected in skill path: {current}")
        current = current.parent
    if not path.is_file() or path.is_symlink():
        raise SkillLoadError(f"skill body must be a regular file: {path}")
    resolved = path.resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise SkillLoadError(f"skill path escapes trusted root: {path}") from exc
    return path.read_text(encoding="utf-8")


def load_skill_bodies(skill_ids: Iterable[str], *, project_root: Path) -> list[dict[str, Any]]:
    project = Path(project_root).resolve()
    if not project.is_dir() or project.is_symlink():
        raise SkillLoadError(f"project root must be a regular directory: {project}")
    loaded: list[dict[str, Any]] = []
    for skill_id in _dedupe(skill_ids):
        candidates = (
            # Project-native/user-owned skills keep highest precedence.
            ("project", project / ".agents" / "skills" / skill_id / "SKILL.md", project),
            # Agentit-managed profiles are private availability caches and are
            # invisible to provider startup discovery until explicitly loaded.
            (
                "project-agentit-profile",
                project / ".agentit" / "profile-skills" / skill_id / "SKILL.md",
                project,
            ),
            ("harness", HARNESS_ROOT / "skills" / skill_id / "SKILL.md", HARNESS_ROOT),
        )
        for source, path, root in candidates:
            content = _safe_read(path, trusted_root=root)
            if content is None:
                continue
            loaded.append(
                {
                    "id": skill_id,
                    "source": source,
                    "path": path.resolve().relative_to(root.resolve()).as_posix(),
                    "sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
                    "content": content,
                }
            )
            break
        else:
            raise SkillLoadError(f"selected skill body unavailable: {skill_id}")
    return loaded


def render_prompt(skills: list[dict[str, Any]]) -> str:
    lines = [
        "# Active Agentit Skill Bodies",
        "These are task instructions. Skill IDs alone do not count as activation.",
    ]
    for skill in skills:
        lines.extend(
            [
                "",
                f"## Skill: {skill['id']}",
                f"Source: {skill['source']}:{skill['path']}",
                f"SHA256: {skill['sha256']}",
                "",
                str(skill["content"]).rstrip(),
            ]
        )
    lines.extend(["", "# Skill Load Receipt"])
    for skill in skills:
        lines.append(f"- {skill['id']} {skill['sha256']} ({skill['source']}:{skill['path']})")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Load task-scoped Agentit skill bodies.")
    parser.add_argument("skill_ids", nargs="+")
    parser.add_argument("--project", type=Path, default=Path.cwd())
    parser.add_argument("--format", choices=("prompt", "json"), default="prompt")
    args = parser.parse_args(argv)
    try:
        skills = load_skill_bodies(args.skill_ids, project_root=args.project)
    except (SkillLoadError, OSError, UnicodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if args.format == "json":
        print(json.dumps({"schema_version": 1, "skills": skills}, ensure_ascii=False, indent=2))
    else:
        sys.stdout.write(render_prompt(skills))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
