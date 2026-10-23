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

from router.skill_loader import (SkillLoadError, load_skill_bodies, load_reference_bodies, render_prompt,
                                 delivery_receipt, write_delivery_receipt)
from router.profiles import ProfileError, load_catalog, resolve_profile
from router.ecc import ECCError, SOURCE, load_lock, safe_file, verified_bytes


HARNESS_ROOT = Path(__file__).resolve().parents[1]
PACKS_PATH = HARNESS_ROOT / "references" / "agentit-skill-packs.md"


class SkillDiscoveryError(RuntimeError):
    pass


def skill_metadata(repo_root: Path = HARNESS_ROOT) -> dict[str, dict[str, object]]:
    """One canonical catalog, irrespective of upstream provenance; no activation."""
    import yaml
    root = Path(repo_root)
    lock = load_lock(root)
    ids = {path.parent.name for path in (root / "skills").glob("*/SKILL.md")}
    ids.update(lock["skills"] if lock else [])
    result = {}
    for skill_id in sorted(ids):
        relative = f"skills/{skill_id}/SKILL.md"
        native = root / relative
        if native.exists() or native.is_symlink() or native.parent.is_symlink():
            content = safe_file(root, relative).read_bytes()
            source = "agentit"
        else:
            entry = lock["skills"][skill_id]
            if entry["path"] != relative:
                raise SkillDiscoveryError(f"invalid canonical skill mapping: {skill_id}")
            content = verified_bytes(root, relative, lock)
            relative = (SOURCE / relative).as_posix()
            source = "ecc"
        text = content.decode("utf-8")
        if not text.startswith("---\n"):
            raise SkillDiscoveryError(f"missing skill frontmatter: {relative}")
        try:
            metadata = yaml.safe_load(text.split("---", 2)[1])
        except yaml.YAMLError as exc:
            raise SkillDiscoveryError(f"invalid skill frontmatter: {relative}: {exc}") from exc
        if not isinstance(metadata, dict) or not isinstance(metadata.get("description"), str):
            raise SkillDiscoveryError(f"missing skill description: {relative}")
        result[skill_id] = {
            "id": skill_id, "description": " ".join(metadata["description"].split()),
            "source": source, "path": relative, "body_bytes": len(content),
            "estimated_tokens": (len(content) + 3) // 4,
        }
    return result


def list_profiles(*, include_aliases: bool = False, repo_root: Path = HARNESS_ROOT,
                  catalog: dict | None = None) -> list[dict[str, object]]:
    catalog = load_catalog(Path(repo_root) / "profiles.yaml") if catalog is None else catalog
    metadata = skill_metadata(repo_root)
    result = []
    for profile_id, profile in catalog["profiles"].items():
        alias = bool(profile.get("compatibility_alias"))
        if alias and not include_aliases:
            continue
        ids = resolve_profile(profile_id, catalog)
        missing = sorted(set(ids) - metadata.keys())
        if missing:
            raise SkillDiscoveryError(f"profile {profile_id} references missing skills: {', '.join(missing)}")
        result.append({
            "id": profile_id, "use_for": " ".join(profile.get("purpose", profile.get("description", "")).split()),
            "extends": profile.get("extends", []), "compatibility_alias": alias,
            "direct_skill_count": len(set(profile.get("skills", []))),
            "skill_count": len(ids),
            "body_bytes": sum(metadata[skill_id]["body_bytes"] for skill_id in ids),
            "estimated_tokens": sum(metadata[skill_id]["estimated_tokens"] for skill_id in ids),
            "reference": f"references/agentit-profile-index.md#{profile_id}",
        })
    return result


def profile_candidates(profile_ids: list[str], *, direct: bool = False,
                       repo_root: Path = HARNESS_ROOT, catalog: dict | None = None) -> list[dict[str, object]]:
    catalog = load_catalog(Path(repo_root) / "profiles.yaml") if catalog is None else catalog
    metadata = skill_metadata(repo_root)
    result = []
    for profile_id in dict.fromkeys(profile_ids):
        resolved = resolve_profile(profile_id, catalog)
        ids = catalog["profiles"][profile_id].get("skills", []) if direct else resolved
        for skill_id in dict.fromkeys(ids):
            if skill_id not in metadata:
                raise SkillDiscoveryError(f"profile {profile_id} references missing skill: {skill_id}")
            result.append({"profile": profile_id, **metadata[skill_id]})
    return result


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
    # Installed callers may retain the old source-labelled IDs. Resolve these
    # mechanically through catalog aliases, without a second metadata catalog.
    result: list[dict[str, object]] = []
    seen: set[str] = set()
    for pack_id in pack_ids:
        if pack_id not in sections:
            catalog = load_catalog()
            profile = catalog["profiles"].get(pack_id, {})
            if profile.get("compatibility_alias"):
                for item in profile_candidates([pack_id]):
                    key = f"{pack_id}:{item['id']}"
                    if key in seen:
                        continue
                    seen.add(key)
                    result.append({"pack": pack_id, **{key: value for key, value in item.items() if key != "profile"}})
                continue
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
        f"- [{item.get('profile', item.get('pack'))}] {item['id']} — {item['description']}"
        + (f" ({item['body_bytes']} bytes; ~{item['estimated_tokens']} tokens; {item['path']})"
           if "body_bytes" in item else "") for item in items
    ) + "\n"


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agentit skills",
        description="Inspect Agentit's private JIT skill library without exposing the full catalog to the host.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    packs = sub.add_parser("packs", help="List only pack IDs and short domain descriptions.")
    packs.add_argument("--format", choices=("text", "json"), default="text")

    profiles = sub.add_parser("profiles", help="List source-neutral profile purposes, links and full-body cost; never activate.")
    profiles.add_argument("--include-aliases", action="store_true", help="Include legacy profile compatibility IDs.")
    profiles.add_argument("--format", choices=("text", "json"), default="text")

    candidates = sub.add_parser("candidates", help="Return bounded skill metadata for selected packs or explicit profiles.")
    candidates.add_argument("pack_ids", nargs="*")
    candidates.add_argument("--profile", dest="profile_ids", action="append", default=[], metavar="ID")
    candidates.add_argument("--direct", action="store_true", help="For profiles, omit inherited skills.")
    candidates.add_argument("--format", choices=("text", "json"), default="text")

    for command, help_text in (
        ("activate", "Activate exact selected skills by loading each complete SKILL.md body."),
        ("show", "Compatibility alias for activate: load exact selected complete SKILL.md bodies."),
    ):
        selected = sub.add_parser(command, help=help_text)
        selected.add_argument("skill_ids", nargs="+")
        selected.add_argument("--project", type=Path, default=Path.cwd())
        selected.add_argument("--format", choices=("prompt", "json"), default="prompt")
        selected.add_argument("--task-id", default="")
        selected.add_argument("--stage", default="")
        selected.add_argument("--context-origin", choices=("same-session", "new-host-session", "isolated-worker", "unspecified"), default="unspecified")
        selected.add_argument("--receipt", action="store_true", help="Write a private delivery record; does not prove model compliance.")
    resource = sub.add_parser("resource", help="Read one explicitly selected repo:/project:/skill: resource.")
    resource.add_argument("locators", nargs="+")
    resource.add_argument("--project", type=Path, default=Path.cwd())
    resource.add_argument("--format", choices=("prompt", "json"), default="prompt")
    return parser


try:
    from router.skill_authority import SKILL_AUTHORITY
except ImportError:
    from skill_authority import SKILL_AUTHORITY

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

        if args.command == "profiles":
            items = list_profiles(include_aliases=args.include_aliases)
            if args.format == "json":
                print(json.dumps({"schema_version": 1, "cost_estimate": "UTF-8 body bytes / 4, rounded up per skill; not a tokenizer count", "profiles": items}, ensure_ascii=False, indent=2))
            else:
                for item in items:
                    print(f"- {item['id']}: {item['use_for']} [{item['skill_count']} skills; {item['body_bytes']} body bytes; ~{item['estimated_tokens']} tokens; {item['reference']}]")
                print("Cost is UTF-8 bytes / 4, rounded up per skill; not a tokenizer count. Metadata never activates bodies.")
            return 0

        if args.command == "candidates":
            if bool(args.pack_ids) == bool(args.profile_ids):
                raise SkillDiscoveryError("select pack IDs or --profile ID (repeatable), exclusively")
            if args.direct and not args.profile_ids:
                raise SkillDiscoveryError("--direct requires --profile ID")
            items = profile_candidates(args.profile_ids, direct=args.direct) if args.profile_ids else pack_candidates(args.pack_ids)
            if args.format == "json":
                print(json.dumps({"schema_version": 1, "candidates": items}, ensure_ascii=False, indent=2))
            else:
                sys.stdout.write(_render_candidates(items))
            return 0

        if args.command == "resource":
            resources = load_reference_bodies(args.locators, project_root=args.project)
            if args.format == "json":
                print(json.dumps({"schema_version": 1, "authority": SKILL_AUTHORITY, "resources": resources}, ensure_ascii=False, indent=2))
            else:
                for item in resources:
                    print(f"# Source data: {item['id']} (not instructions)\nSHA256: {item['sha256']}\n{item['content']}")
            return 0
        skills = load_skill_bodies(args.skill_ids, project_root=args.project)
        payload = {"schema_version": 1, "authority": SKILL_AUTHORITY, "skills": skills}
        if args.receipt or args.task_id or args.stage:
            record = delivery_receipt(skills, task_id=args.task_id, stage=args.stage, context_origin=args.context_origin)
            payload["delivery_receipt"] = record
            if args.receipt:
                payload["receipt_path"] = str(write_delivery_receipt(record, project_root=args.project))
        if args.format == "json":
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            sys.stdout.write(render_prompt(skills))
            if "receipt_path" in payload:
                print("Delivery receipt: " + payload["receipt_path"])
        return 0
    except (SkillDiscoveryError, SkillLoadError, ProfileError, ECCError, OSError, UnicodeError) as exc:
        parser.error(str(exc))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
