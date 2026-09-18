"""Keep provider-visible Agentit skill roots limited to the tiny global core.

Provider CLIs commonly advertise installed skill metadata to the model before a
skill body is activated. Agentit's non-core library therefore stays private
under ~/.agentit/runtime/skills and must not be projected into host discovery
roots. This module detects exact, unmodified legacy Agentit copies left in
those roots and removes them reversibly during bootstrap.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import stat
import tempfile
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


def _tree_metadata(root: Path) -> dict[str, dict[str, Any]]:
    """Versioned ownership metadata, including empty directories and modes."""
    if not root.is_dir() or root.is_symlink():
        raise HostSkillHygieneError(f"skill tree must be a regular directory: {root}")
    result = {".": {"kind": "directory", "mode": stat.S_IMODE(root.stat().st_mode)}}
    for base, dirnames, filenames in os.walk(root, followlinks=False):
        for name in [*dirnames, *filenames]:
            path = Path(base) / name
            if path.is_symlink() or not (path.is_dir() or path.is_file()):
                raise HostSkillHygieneError(f"non-regular entry rejected in skill tree: {path}")
            result[path.relative_to(root).as_posix()] = {
                "kind": "directory" if path.is_dir() else "file",
                "mode": stat.S_IMODE(path.stat().st_mode),
            }
    return result


def _record_metadata_matches(record: dict[str, Any], root: Path) -> bool:
    version = record.get("tree_metadata_version")
    if version is None and "tree_metadata" not in record:
        return False
    if type(version) is not int or version != 1 or not isinstance(record.get("tree_metadata"), dict):
        raise HostSkillHygieneError("unsupported or invalid removed skill tree metadata")
    return _tree_metadata(root) == record["tree_metadata"]


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


def _write_recovery_receipt(
    *, home: Path, backup_root: Path, records: list[dict[str, Any]]
) -> None:
    """Persist a rollback-compatible journal before a destructive cleanup step.

    The normal bootstrap overwrites this file with its complete receipt after a
    successful install. If bootstrap fails after host-skill cleanup, this
    recovery-only receipt still gives the ordinary rollback command enough
    information to restore every removed tree.
    """

    payload = {
        "schema_version": 1,
        "kind": "agentit.bootstrap.receipt",
        "recovery_only": True,
        "home": str(home),
        "records": records,
    }
    backup_root.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(prefix=".agentit-recovery-", dir=backup_root)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(payload, stream, ensure_ascii=False, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, backup_root / "manifest.json")
    finally:
        temporary.unlink(missing_ok=True)


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
    source_metadata = {}
    for child in skills_root.iterdir():
        if child.is_dir() and not child.is_symlink() and child.name not in core:
            source_manifests[child.name] = _tree_manifest(child)
            source_metadata[child.name] = _tree_metadata(child)

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
                metadata = _tree_metadata(candidate)
            except HostSkillHygieneError:
                continue
            if not _matches_agentit_source(current, source_manifests[candidate.name]):
                continue
            expected_metadata = source_metadata[candidate.name]
            if current != source_manifests[candidate.name]:
                expected_metadata = {key: value for key, value in expected_metadata.items() if key in {".", "SKILL.md"}}
            if metadata != expected_metadata:
                continue
            operations.append(
                {
                    "action": "remove-managed-skill-tree",
                    "category": f"provider:{provider}:legacy-skill",
                    "skill_id": candidate.name,
                    "destination": str(candidate),
                    # Bind apply to the exact tree approved during planning.
                    # Without this, a user edit between plan/apply could be
                    # backed up and then deleted despite the fail-closed rule.
                    "planned_tree_manifest": current,
                    "planned_tree_metadata": metadata,
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
        planned = operation.get("planned_tree_manifest")
        metadata = _tree_metadata(destination)
        if not isinstance(planned, dict) or tree_before != planned or metadata != operation.get("planned_tree_metadata"):
            raise HostSkillHygieneError(
                f"legacy skill changed after planning; refusing cleanup: {destination}"
            )

        backup = backup_root / "removed-skill-trees" / rel
        if backup.exists() or backup.is_symlink():
            raise HostSkillHygieneError(f"legacy skill backup already exists: {backup}")

        record = {
            "kind": "removed_skill_tree",
            "category": operation["category"],
            "skill_id": operation["skill_id"],
            "destination": str(destination),
            "backup_path": str(backup),
            "tree_manifest": tree_before,
            "tree_metadata_version": 1,
            "tree_metadata": metadata,
        }

        # Journal the intended destructive operation first. If the process dies
        # after the directory is removed but before bootstrap writes its final
        # receipt, the ordinary rollback path still has a durable record.
        _write_recovery_receipt(home=home, backup_root=backup_root, records=[*records, record])

        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(destination, backup, symlinks=False)
        if _tree_manifest(backup) != tree_before or _tree_metadata(backup) != metadata:
            raise HostSkillHygieneError(f"legacy skill backup mismatch: {destination}")

        # Revalidate immediately before deletion as a second TOCTOU barrier.
        if _tree_manifest(destination) != tree_before or _tree_metadata(destination) != metadata:
            raise HostSkillHygieneError(
                f"legacy skill changed during backup; refusing cleanup: {destination}"
            )
        shutil.rmtree(destination)
        records.append(record)
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
    if ("tree_metadata_version" in record or "tree_metadata" in record) and not _record_metadata_matches(record, backup):
        raise HostSkillHygieneError(f"removed skill backup metadata changed: {backup}")
    return destination, backup


def removed_tree_is_restored(record: dict[str, Any], *, home: Path) -> bool:
    """Recognize an exact original tree in an interrupted install or rollback.

    Legacy hash-only receipts cannot prove restored modes or directory shape;
    those receipts can still restore an absent destination from their backup.
    """
    destination = Path(str(record["destination"]))
    try:
        relative = destination.relative_to(home)
    except ValueError as exc:
        raise HostSkillHygieneError(f"rollback destination escapes home: {destination}") from exc
    if ".." in relative.parts:
        raise HostSkillHygieneError(f"unsafe rollback destination: {destination}")
    current = destination
    while current != home:
        if current.is_symlink():
            raise HostSkillHygieneError(f"symlink rollback path rejected: {current}")
        current = current.parent
    return destination.is_dir() and _tree_manifest(destination) == record.get("tree_manifest") and _record_metadata_matches(record, destination)


def restore_removed_tree(record: dict[str, Any], *, home: Path) -> None:
    destination, backup = validate_removed_tree_record(record, home=home)
    # Check ancestor paths before creating a sibling staging directory.
    removed_tree_is_restored(record, home=home)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".agentit-restore-", dir=destination.parent) as temporary:
        staged = Path(temporary) / "tree"
        shutil.copytree(backup, staged, symlinks=False)
        if _tree_manifest(staged) != (record.get("tree_manifest") or {}):
            raise HostSkillHygieneError(f"restored skill tree mismatch: {destination}")
        if ("tree_metadata_version" in record or "tree_metadata" in record) and not _record_metadata_matches(record, staged):
            raise HostSkillHygieneError(f"restored skill tree metadata mismatch: {destination}")
        validate_removed_tree_record(record, home=home)
        os.replace(staged, destination)
