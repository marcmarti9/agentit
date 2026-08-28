"""Mechanical JIT skill discovery for Agentit.

The host model owns semantic selection. This CLI only exposes bounded metadata
for requested packs and loads exact skill bodies after the model selects them.
It deliberately avoids dumping the whole skill catalog into startup context.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from router.skill_loader import SkillLoadError, load_skill_bodies, render_prompt


HARNESS_ROOT = Path(__file__).resolve().parents[1]
PACKS_PATH = HARNESS_ROOT / "skills" / "using-agent-skills" / "references" / "packs.md"


class SkillDiscoveryError(RuntimeError):
    pass


def _pack_sections() -> dict[str, str]:
    try:
        text = PACKS_PATH.read_text(encoding="utf-8")
    except OSError as exc:
        raise SkillDiscoveryError(f"cannot read pack map: {exc}") from exc
    matches = list(re.finditer(r"(?m)^## ([a-z0-9][a-z0-9_-]*)\s*$", text))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        if body.endswith("---"):
            body = body[:-3].rstrip()
        sections[match.group(1)] = body
    return sections


def _use_for(section: str) -> str:
    match = re.search(r"(?m)^\*\*Use for:\*\*\s*(.+)$", section)
    return match.group(1).strip() if match else ""


def _candidate_lines(section: str) -> list[str]:
    marker = "**Skills in this pack:**"
    if marker not in section:
        return []
    tail = section.split(marker, 1)[1]
    lines: list[str] = []
    for raw in tail.splitlines():
        line = raw.strip()
        if line.startswith("- `"):
            lines.append(line[2:])
        elif lines and line.startswith("## "):
            break
    return lines


def list_packs() -> list[dict[str, str]]:
    return [
        {"id": pack_id, "use_for": _use_for(section)}
        for pack_id, section in _pack_sections().items()
    ]


def pack_candidates(pack_ids: list[str]) -> list[dict[str, object]]:
    sections = _pack_sections()
    result: list[dict[str, object]] = []
    seen: set[str] = set()
    for pack_id in pack_ids:
        if pack_id not in sections:
            raise SkillDiscoveryError(
                f"unknown pack {pack_id!r}; valid: {', '.join(sections)}"
            )
        lines = _candidate_lines(sections[pack_id])
        for line in lines:
            match = re.match(r"`([^`]+)`\s*—\s*(.*)", line)
            if not match:
                continue
            skill_id, description = match.groups()
            key = f"{pack_id}:{skill_id}"
            if key in seen:
                continue
            seen.add(key)
            result.append(
                {"pack": pack_id, "id": skill_id, "description": description.strip()}
            )
    return result


def _render_packs(items: list[dict[str, str]]) -> str:
    return "\n".join(
        f"- {item['id']}: {item['use_for']}" for item in items
    ) + "\n"


def _render_candidates(items: list[dict[str, object]]) -> str:
    return "\n".join(
        f"- [{item['pack']}] {item['id']} — {item['description']}" for item in items
    ) + "\n"


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agentit skills",
        description="Inspect Agentit's private JIT skill library without exposing the full catalog to the host.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    packs = sub.add_parser("packs", help="List only pack IDs and short domain descriptions.")
    packs.add_argument("--format", choices=("text", "json"), default="text")

    candidates = sub.add_parser("candidates", help="Return bounded skill metadata for selected packs.")
    candidates.add_argument("pack_ids", nargs="+")
    candidates.add_argument("--format", choices=("text", "json"), default="text")

    show = sub.add_parser("show", help="Load exact selected SKILL.md bodies after semantic selection.")
    show.add_argument("skill_ids", nargs="+")
    show.add_argument("--project", type=Path, default=Path.cwd())
    show.add_argument("--format", choices=("prompt", "json"), default="prompt")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "packs":
            items = list_packs()
            if args.format == "json":
                print(json.dumps({"schema_version": 1, "packs": items}, ensure_ascii=False, indent=2))
            else:
                sys.stdout.write(_render_packs(items))
            return 0

        if args.command == "candidates":
            items = pack_candidates(args.pack_ids)
            if args.format == "json":
                print(json.dumps({"schema_version": 1, "candidates": items}, ensure_ascii=False, indent=2))
            else:
                sys.stdout.write(_render_candidates(items))
            return 0

        skills = load_skill_bodies(args.skill_ids, project_root=args.project)
        if args.format == "json":
            print(json.dumps({"schema_version": 1, "skills": skills}, ensure_ascii=False, indent=2))
        else:
            sys.stdout.write(render_prompt(skills))
        return 0
    except (SkillDiscoveryError, SkillLoadError, OSError, UnicodeError) as exc:
        parser.error(str(exc))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
