#!/usr/bin/env python3
"""Offline maintenance checks; never select skills or claim behavioral quality."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path, PurePosixPath

import yaml

ROOT = Path(__file__).resolve().parents[1]
CORE = {"using-agentit", "task-router", "using-agent-skills"}
# Licenses reviewed for this manifest schema; expansion requires source/license review.
REVIEWED_LICENSES = {"MIT", "Apache-2.0", "CC-BY-4.0", "CC-BY-SA-4.0"}


def checked_file(root: Path, relative: str) -> Path:
    path = PurePosixPath(relative)
    if not relative or path.is_absolute() or ".." in path.parts or "\\" in relative:
        raise ValueError(f"unsafe curation path: {relative}")
    target = root
    for part in path.parts:
        target /= part
        if target.is_symlink():
            raise ValueError(f"symlink in curation path: {relative}")
    if not target.is_file():
        raise ValueError(f"missing curation file: {relative}")
    return target


def check_sources(root: Path, manifest: dict) -> int:
    if manifest.get("schema_version") != 1 or not manifest.get("sources"):
        raise ValueError("invalid adaptation source manifest")
    seen = set()
    for item in manifest["sources"]:
        repo, revision = item["repo"], item["revision"]
        if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo):
            raise ValueError(f"invalid source repository: {repo}")
        if not re.fullmatch(r"[0-9a-f]{40}", revision):
            raise ValueError(f"unfixed source revision: {repo}")
        if (repo, revision) in seen:
            raise ValueError(f"duplicate source record: {repo}")
        seen.add((repo, revision))
        # New records explicitly declare path provenance mandatory. Older
        # records predate that contract; do not invent retroactive source paths.
        if item.get("source_paths_required") or "source_paths" in item:
            paths = item.get("source_paths")
            if not isinstance(paths, list) or not paths:
                raise ValueError(f"missing inspected source paths: {repo}")
            for relative in paths:
                if not isinstance(relative, str):
                    raise ValueError(f"invalid inspected source path: {repo}")
                path = PurePosixPath(relative)
                if (not relative or relative == "." or path.is_absolute()
                        or ".." in path.parts or "\\" in relative
                        or path.as_posix() != relative):
                    raise ValueError(f"unsafe inspected source path: {repo}: {relative}")
            if len(paths) != len(set(paths)):
                raise ValueError(f"duplicate inspected source path: {repo}")
        if not item.get("source_license") or not item.get("adaptation_license") or not item.get("targets"):
            raise ValueError(f"incomplete source license/targets: {repo}")
        for field in ("source_license", "adaptation_license"):
            if item[field] not in REVIEWED_LICENSES:
                raise ValueError(f"unreviewed license identifier: {repo}: {item[field]}")
        for kind in ("license", "notice"):
            if kind == "notice" and "notice_path" not in item:
                continue
            path = checked_file(root, item[f"{kind}_path"])
            if hashlib.sha256(path.read_bytes()).hexdigest() != item[f"{kind}_sha256"]:
                raise ValueError(f"changed retained {kind}: {repo}")
        for target in item["targets"]:
            checked_file(root, target)
    return len(seen)


def check_catalog(root: Path = ROOT) -> dict:
    # This checks explicit inventory equality, not natural-language relevance.
    from router.profiles import load_catalog, repository_skill_ids, resolve_profile

    catalog = load_catalog(root / "profiles.yaml")
    known = repository_skill_ids(root)
    if set(resolve_profile("core", catalog, repo_root=root)) != CORE:
        raise ValueError("core must remain exactly the three navigation bodies")
    if catalog["default_profile"] != "core" or catalog["global_profiles"] != ["core"]:
        raise ValueError("unexpected global profile expansion")
    if set(resolve_profile("all", catalog, repo_root=root)) != known:
        raise ValueError("all profile differs from installable skill inventory")
    for name, profile in catalog["profiles"].items():
        if len(profile.get("skills", [])) != len(set(profile.get("skills", []))):
            raise ValueError(f"duplicate explicit profile membership: {name}")
        resolve_profile(name, catalog, repo_root=root)

    text = checked_file(root, "references/agentit-skill-packs.md").read_text()
    discovered = set()
    for section in re.split(r"(?m)^## [a-z0-9][a-z0-9_-]*\s*$", text):
        ids = re.findall(r"(?m)^- `([^`]+)` —", section)
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate skill in one discovery pack")
        discovered.update(ids)
    if known - CORE - discovered or discovered - known:
        raise ValueError(f"pack inventory differs: missing={sorted(known-CORE-discovered)}, unknown={sorted(discovered-known)}")
    manifest = json.loads(checked_file(root, "skills/ADAPTATION_SOURCES.json").read_text())
    sources = check_sources(root, manifest)
    # Decode frontmatter of newly curated bodies; renamed canonical sources are
    # intentionally outside this name check and retain upstream bytes.
    target_bodies = {t for s in manifest["sources"] for t in s["targets"] if t.endswith("/SKILL.md")}
    for relative in target_bodies:
        body = checked_file(root, relative).read_text()
        if not body.startswith("---\n") or "\n---\n" not in body:
            raise ValueError(f"missing frontmatter: {relative}")
        header = yaml.safe_load(body.split("\n---\n", 1)[0][4:])
        if not isinstance(header, dict):
            raise ValueError(f"invalid frontmatter mapping: {relative}")
        if header.get("name") != Path(relative).parent.name or not header.get("description"):
            raise ValueError(f"invalid new skill identity/description: {relative}")
        source_records = [s for s in manifest["sources"] if relative in s["targets"]]
        if any(s["adaptation_license"] != header.get("license") for s in source_records):
            raise ValueError(f"adaptation license differs from frontmatter: {relative}")
    return {"status": "verified", "evidence": "offline catalog/provenance structure only; no model-quality claim",
            "profiles": len(catalog["profiles"]), "skills": len(known), "adaptation_sources": sources}


if __name__ == "__main__":
    # Script invocation from repository root matches CI's existing convention.
    import sys

    sys.path.insert(0, str(ROOT))
    try:
        print(json.dumps(check_catalog(), indent=2))
    except (ValueError, KeyError, OSError, yaml.YAMLError) as error:
        print(f"curation check failed: {error}", file=sys.stderr)
        raise SystemExit(1)
