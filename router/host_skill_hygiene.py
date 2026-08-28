"""Keep provider-visible Agentit skill roots limited to the tiny global core.

Provider CLIs commonly advertise installed skill metadata to the model before a
skill body is activated. Agentit's non-core library therefore stays private
under ~/.agentit/runtime/skills and must not be projected into host discovery
roots. This module detects exact, unmodified legacy Agentit copies left in
those roots and removes them reversibly during bootstrap.
"""

from __future__ import annotations

import hashlib
import os
import shutil
from pathlib import Path
from typing import Any, Iterable


class HostSkillHygieneError(RuntimeError):
    pass


def _hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _tree_manifest(root: Path) -> dict[str, str]:
    if not root.is_dir() or root.is_symlink():
        raise HostSkillHygieneError(f"skill tree must be a regular directory: {root}")
    result: dict[str, str] = {}
    for base, dirnames, filenames in os.walk(root, followlinks=False):
        base_path = Path(base)
        for name in dirnames:
            candidate = base_path / name
            if candidate.is_symlink():
                raise HostSkillHygieneError(f"symlink rejected in skill tree: {candidate}")
        for name in filenames:
            candidate = base_path / name
            if not candidate.is_file() or candidate.is_symlink():
                raise HostSkillHygieneError(f"non-regular file rejected in skill tree: {candidate}")
            result[candidate.relative_to(root).as_posix()] = _hash_file(candidate)
    return result


def _matches_agentit_source(current: dict[str, str], source: dict[str, str]) -> bool:
    if current == source:
        return True
    # Some historical installers projected only SKILL.md even when the source
    # skill also contained references. That legacy shape is still safely
    # attributable when the sole body matches the current Agentit body exactly.
    return (
        set(current) == {"SKILL.md"}
        and "SKILL.md" in source
        and current["SKILL.md"] == source["SKILL.md"]
    )


def _provider_roots(home: Path, manifest: dict[str, Any], providers: Iterable[str]) -> list[tuple[str, Path]]:
    catalog = manifest.get("providers") or {}
    seen: set[Path] = set()
    roots: list[tuple[str, Path]] = []
    for provider in providers:
        config = catalog.get(provider) or {}
        values = [config.get("skills_root"), *(config.get("legacy_skill_roots") or [])]
        for raw in values:
            if not raw:
                continue
            root = (home / str(raw)).absolute()
            try:
                root.relative_to(home)
            except ValueError as exc:
                raise HostSkillHygieneError(f"provider skill root escapes home: {root}") from exc
            if root in seen:
                continue
            seen.add(root)
            roots.append((provider, root))
    return roots


def plan_host_skill_hygiene(
    *, home: Path, source_root: Path, manifest: dict[str, Any], providers: Iterable[str]
) -> list[dict[str, Any]]:
    """Return reversible removals for provably Agentit-managed non-core copies.

    Unknown/user-owned skills are never removed. A non-core directory is
    classified as Agentit-managed only when its whole tree matches the current
    source tree or when it is the historical SKILL.md-only projection and that
    body matches exactly. Same-ID but different content is left alone.
    """

    core = {str(item) for item in manifest.get("core_skills") or []}
    skills_root = source_root / "skills"
    if not skills_root.is_dir() or skills_root.is_symlink():
        raise HostSkillHygieneError(f"Agentit source skills root unavailable: {skills_root}")

    source_manifests: dict[str, dict[str, str]] = {}
    for child in skills_root.iterdir():
        if child.is_dir() and not child.is_symlink() and child.name not in core:
            source_manifests[child.name] = _tree_manifest(child)

    operations: list[dict[str, Any]] = []
    for provider, root in _provider_roots(home, manifest, providers):
        if not root.exists():
            continue
        if not root.is_dir() or root.is_symlink():
            raise HostSkillHygieneError(f"provider skill root is unsafe: {root}")
        for candidate in root.iterdir():
            if candidate.name in core or candidate.name not in source_manifests:
                continue
            if not candidate.is_dir() or candidate.is_symlink():
                continue
            try:
                current = _tree_manifest(candidate)
            except HostSkillHygieneError:
                continue
            if not _matches_agentit_source(current, source_manifests[candidate.name]):
                continue
            operations.append(
                {
                    "action": "remove-managed-skill-tree",
                    "category": f"provider:{provider}:legacy-skill",
                    "skill_id": candidate.name,
                    "destination": str(candidate),
                }
            )
    return operations


def apply_host_skill_hygiene(
    operations: list[dict[str, Any]], *, home: Path, backup_root: Path
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for operation in operations:
        destination = Path(str(operation["destination"]))
        try:
            rel = destination.relative_to(home)
        except ValueError as exc:
            raise HostSkillHygieneError(f"legacy skill destination escapes home: {destination}") from exc
        if not destination.is_dir() or destination.is_symlink():
            raise HostSkillHygieneError(f"legacy skill changed before cleanup: {destination}")
        tree_before = _tree_manifest(destination)
        backup = backup_root / "removed-skill-trees" / rel
        if backup.exists() or backup.is_symlink():
            raise HostSkillHygieneError(f"legacy skill backup already exists: {backup}")
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(destination, backup, symlinks=False)
        if _tree_manifest(backup) != tree_before:
            raise HostSkillHygieneError(f"legacy skill backup mismatch: {destination}")
        shutil.rmtree(destination)
        records.append(
            {
                "kind": "removed_skill_tree",
                "category": operation["category"],
                "skill_id": operation["skill_id"],
                "destination": str(destination),
                "backup_path": str(backup),
                "tree_manifest": tree_before,
            }
        )
    return records


def validate_removed_tree_record(record: dict[str, Any], *, home: Path) -> tuple[Path, Path]:
    destination = Path(str(record["destination"]))
    backup = Path(str(record["backup_path"]))
    try:
        destination.relative_to(home)
    except ValueError as exc:
        raise HostSkillHygieneError(f"rollback destination escapes home: {destination}") from exc
    if destination.exists() or destination.is_symlink():
        raise HostSkillHygieneError(
            f"refusing rollback because removed skill destination was recreated: {destination}"
        )
    expected = record.get("tree_manifest") or {}
    if not backup.is_dir() or backup.is_symlink() or _tree_manifest(backup) != expected:
        raise HostSkillHygieneError(f"removed skill backup missing or changed: {backup}")
    return destination, backup


def restore_removed_tree(record: dict[str, Any], *, home: Path) -> None:
    destination, backup = validate_removed_tree_record(record, home=home)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(backup, destination, symlinks=False)
    if _tree_manifest(destination) != (record.get("tree_manifest") or {}):
        raise HostSkillHygieneError(f"restored skill tree mismatch: {destination}")
