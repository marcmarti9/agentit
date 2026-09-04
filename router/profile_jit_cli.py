"""Private project profile management for true JIT Agentit skills.

Profiles are availability/discovery bundles, not host context bundles. Enabling a
profile stores Agentit-managed skill packages under ``.agentit/profile-skills``
instead of ``.agents/skills``. Older Agentit manifests that projected profile
skills into host-visible ``.agents/skills`` are migrated only when every managed
file can be proven unchanged.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import tempfile
from pathlib import Path
from typing import Any

from router.profiles import ProfileError, load_catalog, resolve_profile


MANIFEST_RELATIVE_PATH = Path(".agentit") / "skills-manifest.json"
PRIVATE_SKILL_ROOT = Path(".agentit") / "profile-skills"
LEGACY_HOST_ROOT = Path(".agents") / "skills"
PRIVATE_SHARED_REFERENCE_ROOT = Path(".agentit") / "references"
ADDY_SHARED_REFERENCE_MANIFEST = Path("references") / ".addy-agent-skills-files"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _assert_project_path(path: Path, *, project: Path) -> None:
    root = project.resolve()
    if path.is_symlink():
        raise ProfileError(f"symlink rejected: {path}")
    try:
        path.resolve(strict=False).relative_to(root)
    except ValueError as exc:
        raise ProfileError(f"path escapes project root: {path}") from exc
    current = path
    while current != root and current != current.parent:
        if current.is_symlink():
            raise ProfileError(f"symlink path component rejected: {current}")
        current = current.parent


def _manifest_path(project: Path) -> Path:
    return project / MANIFEST_RELATIVE_PATH


def _read_manifest(project: Path) -> dict[str, Any] | None:
    path = _manifest_path(project)
    _assert_project_path(path, project=project)
    if not path.exists():
        return None
    if not path.is_file() or path.is_symlink():
        raise ProfileError(f"project skill manifest must be a regular file: {path}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ProfileError(f"invalid project skill manifest {path}: {exc}") from exc
    if not isinstance(payload, dict) or payload.get("schema_version") != 1:
        raise ProfileError("project skill manifest must use schema_version: 1")
    profiles = payload.get("profiles")
    skills = payload.get("skills")
    if not isinstance(profiles, list) or not all(isinstance(item, str) for item in profiles):
        raise ProfileError("project skill manifest profiles must be a string list")
    if not isinstance(skills, dict):
        raise ProfileError("project skill manifest skills must be a mapping")
    return payload


def _atomic_json(path: Path, payload: dict[str, Any], *, project: Path) -> None:
    _assert_project_path(path, project=project)
    path.parent.mkdir(parents=True, exist_ok=True)
    _assert_project_path(path.parent, project=project)
    fd, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.tmp-", dir=path.parent, text=True)
    temporary = Path(temporary_name)
    try:
        os.fchmod(fd, stat.S_IRUSR | stat.S_IWUSR)
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(payload, stream, ensure_ascii=False, indent=2, sort_keys=True)
            stream.write("\n")
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def _package_files(source_dir: Path) -> list[str]:
    """Return every regular file in a complete skill package."""
    if not source_dir.is_dir() or source_dir.is_symlink():
        raise ProfileError(f"skill source is not a regular directory: {source_dir}")
    skill_md = source_dir / "SKILL.md"
    if not skill_md.is_file() or skill_md.is_symlink():
        raise ProfileError(f"skill source body missing: {skill_md}")
    files = ["SKILL.md"]
    for file_path in sorted(source_dir.rglob("*")):
        if file_path.is_symlink():
            raise ProfileError(f"skill package rejects symlinks: {file_path}")
        if file_path.is_file() and file_path != skill_md:
            files.append(file_path.relative_to(source_dir).as_posix())
    return files


def _shared_reference_files(repo_root: Path) -> list[str]:
    manifest = repo_root / ADDY_SHARED_REFERENCE_MANIFEST
    if not manifest.exists():
        return []
    if not manifest.is_file() or manifest.is_symlink():
        raise ProfileError(f"shared reference manifest is unsafe: {manifest}")
    result: list[str] = []
    for raw in manifest.read_text(encoding="utf-8").splitlines():
        relative = raw.strip()
        if not relative:
            continue
        rel = Path(relative)
        if rel.is_absolute() or ".." in rel.parts:
            raise ProfileError(f"unsafe shared reference path: {relative}")
        source = repo_root / "references" / rel
        if not source.is_file() or source.is_symlink():
            raise ProfileError(f"shared reference source missing or unsafe: {source}")
        result.append(rel.as_posix())
    return sorted(set(result))


def _sync_shared_references(*, project: Path, repo_root: Path) -> None:
    destination_root = project / PRIVATE_SHARED_REFERENCE_ROOT
    destination_manifest = destination_root / ".addy-agent-skills-files"
    if destination_manifest.exists():
        if not destination_manifest.is_file() or destination_manifest.is_symlink():
            raise ProfileError(
                f"private shared reference manifest is unsafe: {destination_manifest}"
            )
        for raw in destination_manifest.read_text(encoding="utf-8").splitlines():
            relative = raw.strip()
            if not relative:
                continue
            rel = Path(relative)
            if rel.is_absolute() or ".." in rel.parts:
                raise ProfileError(f"unsafe cached shared reference path: {relative}")
            stale = destination_root / rel
            _assert_project_path(stale, project=project)
            if stale.exists():
                if not stale.is_file() or stale.is_symlink():
                    raise ProfileError(f"private shared reference cache is unsafe: {stale}")
                stale.unlink()

    for relative in _shared_reference_files(repo_root):
        _copy_atomic(
            repo_root / "references" / relative,
            destination_root / relative,
            project=project,
        )

    source_manifest = repo_root / ADDY_SHARED_REFERENCE_MANIFEST
    if source_manifest.exists():
        _copy_atomic(source_manifest, destination_manifest, project=project)


def _source_dir(repo_root: Path, skill_id: str) -> Path:
    return repo_root / "skills" / skill_id


def _private_dir(project: Path, skill_id: str) -> Path:
    return project / PRIVATE_SKILL_ROOT / skill_id


def _managed_file_metadata(metadata: dict[str, Any]) -> dict[str, dict[str, Any]]:
    files = metadata.get("files")
    if isinstance(files, dict) and files:
        return {
            str(relative): entry
            for relative, entry in files.items()
            if isinstance(entry, dict) and entry.get("managed", True)
        }
    if metadata.get("managed", True):
        return {
            "SKILL.md": {
                "installed_sha256": metadata.get("installed_sha256"),
                "managed": True,
            }
        }
    return {}


def _legacy_cleanup_plan(
    *, project: Path, manifest: dict[str, Any] | None
) -> list[dict[str, str]]:
    """Plan removal of old Agentit-managed host-visible profile packages."""
    if manifest is None:
        return []
    operations: list[dict[str, str]] = []
    for skill_id, metadata in manifest.get("skills", {}).items():
        if not isinstance(metadata, dict):
            raise ProfileError(f"invalid manifest entry for {skill_id}")
        destination_raw = metadata.get("destination")
        if not isinstance(destination_raw, str):
            raise ProfileError(f"invalid manifest destination for {skill_id}")
        destination = Path(destination_raw)
        if not destination.parts[:2] == LEGACY_HOST_ROOT.parts:
            continue
        skill_root = (project / destination).parent
        _assert_project_path(skill_root, project=project)
        managed = _managed_file_metadata(metadata)
        if not managed:
            continue
        known = set(managed)
        if skill_root.exists():
            if not skill_root.is_dir() or skill_root.is_symlink():
                raise ProfileError(f"legacy profile skill root is unsafe: {skill_root}")
            for path in skill_root.rglob("*"):
                if path.is_symlink():
                    raise ProfileError(f"legacy profile skill contains symlink: {path}")
                if path.is_file() and path.relative_to(skill_root).as_posix() not in known:
                    raise ProfileError(
                        f"legacy Agentit profile skill has extra user files; manual review required: {path}"
                    )
        for relative, file_meta in managed.items():
            path = skill_root / relative
            if not path.exists():
                continue
            _assert_project_path(path, project=project)
            if not path.is_file() or path.is_symlink():
                raise ProfileError(f"legacy managed profile file is unsafe: {path}")
            expected = file_meta.get("installed_sha256")
            if not isinstance(expected, str) or _sha256(path) != expected:
                raise ProfileError(
                    f"legacy Agentit profile skill was modified; refusing automatic JIT migration: {path}"
                )
            operations.append(
                {
                    "action": "remove-legacy-host-file",
                    "path": str(path),
                    "skill_id": str(skill_id),
                    "expected_sha256": expected,
                }
            )
    return operations


def _active_skills(profiles: list[str], *, catalog: dict[str, Any], repo_root: Path) -> list[str]:
    result: list[str] = []
    for profile in profiles:
        for skill_id in resolve_profile(profile, catalog, repo_root=repo_root):
            if skill_id not in result:
                result.append(skill_id)
    return result


def _build_payload(
    profiles: list[str], *, catalog: dict[str, Any], repo_root: Path
) -> dict[str, Any]:
    skills: dict[str, Any] = {}
    for skill_id in _active_skills(profiles, catalog=catalog, repo_root=repo_root):
        source_dir = _source_dir(repo_root, skill_id)
        file_entries: dict[str, dict[str, Any]] = {}
        for relative in _package_files(source_dir):
            source_file = source_dir / relative
            digest = _sha256(source_file)
            file_entries[relative] = {
                "source_sha256": digest,
                "installed_sha256": digest,
                "managed": True,
            }
        skills[skill_id] = {
            "destination": (PRIVATE_SKILL_ROOT / skill_id / "SKILL.md").as_posix(),
            "source_sha256": file_entries["SKILL.md"]["source_sha256"],
            "installed_sha256": file_entries["SKILL.md"]["installed_sha256"],
            "managed": True,
            "files": file_entries,
        }
    return {"schema_version": 1, "profiles": profiles, "skills": skills}


def _validate_private_existing(
    *, project: Path, old_manifest: dict[str, Any] | None
) -> None:
    if old_manifest is None:
        return
    for skill_id, metadata in old_manifest.get("skills", {}).items():
        if not isinstance(metadata, dict):
            continue
        destination = metadata.get("destination")
        if not isinstance(destination, str) or not Path(destination).parts[:2] == PRIVATE_SKILL_ROOT.parts[:2]:
            continue
        root = (project / destination).parent
        managed = _managed_file_metadata(metadata)
        for relative, file_meta in managed.items():
            path = root / relative
            if not path.exists():
                continue
            if not path.is_file() or path.is_symlink():
                raise ProfileError(f"private managed profile file is unsafe: {path}")
            expected = file_meta.get("installed_sha256")
            if isinstance(expected, str) and _sha256(path) != expected:
                raise ProfileError(f"refusing to overwrite modified private profile skill: {path}")


def _private_cleanup_plan(
    *, project: Path, old_manifest: dict[str, Any] | None, payload: dict[str, Any]
) -> list[dict[str, str]]:
    """Return old managed private files that are no longer in the desired payload.

    This covers both removed references inside a still-enabled skill and entire
    skills that disappear because a profile was disabled or its catalog changed.
    Every removal is bound to the hash recorded by the old manifest so a user
    edit after planning fails closed instead of being deleted.
    """

    if old_manifest is None:
        return []
    desired_skills = payload.get("skills") or {}
    operations: list[dict[str, str]] = []
    for skill_id, metadata in old_manifest.get("skills", {}).items():
        if not isinstance(metadata, dict):
            continue
        destination = metadata.get("destination")
        if not isinstance(destination, str) or not Path(destination).parts[:2] == PRIVATE_SKILL_ROOT.parts[:2]:
            continue
        root = (project / destination).parent
        new_metadata = desired_skills.get(skill_id)
        desired_files = (
            set(_managed_file_metadata(new_metadata)) if isinstance(new_metadata, dict) else set()
        )
        for relative, file_meta in _managed_file_metadata(metadata).items():
            if relative in desired_files:
                continue
            path = root / relative
            if not path.exists():
                continue
            _assert_project_path(path, project=project)
            expected = file_meta.get("installed_sha256")
            if (
                not path.is_file()
                or path.is_symlink()
                or not isinstance(expected, str)
                or _sha256(path) != expected
            ):
                raise ProfileError(f"refusing to remove modified managed private profile skill: {path}")
            operations.append(
                {
                    "action": "remove-stale-private-file",
                    "path": str(path),
                    "skill_id": str(skill_id),
                    "expected_sha256": expected,
                }
            )
    return operations


def _copy_atomic(source: Path, destination: Path, *, project: Path) -> None:
    _assert_project_path(destination, project=project)
    destination.parent.mkdir(parents=True, exist_ok=True)
    _assert_project_path(destination.parent, project=project)
    fd, temporary_name = tempfile.mkstemp(prefix=f".{destination.name}.tmp-", dir=destination.parent)
    temporary = Path(temporary_name)
    os.close(fd)
    try:
        shutil.copy2(source, temporary)
        os.replace(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)


def _remove_file_and_empty_parents(path: Path, *, project: Path, stop: Path) -> None:
    path.unlink()
    current = path.parent
    while current != stop and current != project and current != current.parent:
        try:
            current.rmdir()
        except OSError:
            break
        current = current.parent


def _apply_planned_removal(
    item: dict[str, str], *, project: Path, stop: Path, label: str
) -> None:
    path = Path(item["path"])
    if not path.exists():
        return
    _assert_project_path(path, project=project)
    expected = item.get("expected_sha256")
    if (
        not path.is_file()
        or path.is_symlink()
        or not isinstance(expected, str)
        or _sha256(path) != expected
    ):
        raise ProfileError(f"{label} changed after planning; refusing removal: {path}")
    _remove_file_and_empty_parents(path, project=project, stop=stop)


def _enable(
    profile_name: str,
    *, project: Path,
    repo_root: Path,
    catalog: dict[str, Any],
    apply: bool,
) -> list[str]:
    if not project.is_dir() or project.is_symlink():
        raise ProfileError(f"project root must be a regular directory: {project}")
    old = _read_manifest(project)
    profiles = list(old.get("profiles", [])) if old else []
    if profile_name not in catalog["profiles"]:
        raise ProfileError(f"unknown profile: {profile_name}")
    if profile_name not in profiles:
        profiles.append(profile_name)
    for name in profiles:
        if name not in catalog["profiles"]:
            raise ProfileError(f"unknown profile in project manifest: {name}")

    _validate_private_existing(project=project, old_manifest=old)
    cleanup = _legacy_cleanup_plan(project=project, manifest=old)
    payload = _build_payload(profiles, catalog=catalog, repo_root=repo_root)
    stale = _private_cleanup_plan(project=project, old_manifest=old, payload=payload)
    shared_references = _shared_reference_files(repo_root)
    operations: list[str] = []
    operations.extend(
        f"sync shared reference: {project / PRIVATE_SHARED_REFERENCE_ROOT / relative}"
        for relative in shared_references
    )
    for skill_id, metadata in payload["skills"].items():
        root = _private_dir(project, skill_id)
        source = _source_dir(repo_root, skill_id)
        for relative in metadata["files"]:
            destination = root / relative
            verb = "replace" if destination.exists() else "install"
            operations.append(f"{verb}: {destination}")
    operations.extend(f"remove stale private cache: {item['path']}" for item in stale)
    operations.extend(f"remove legacy host exposure: {item['path']}" for item in cleanup)

    if not apply:
        return ["MODO PLAN: no se escribirán archivos.", *operations]

    for skill_id, metadata in payload["skills"].items():
        root = _private_dir(project, skill_id)
        source = _source_dir(repo_root, skill_id)
        for relative in metadata["files"]:
            _copy_atomic(source / relative, root / relative, project=project)

    _sync_shared_references(project=project, repo_root=repo_root)

    for item in stale:
        _apply_planned_removal(
            item,
            project=project,
            stop=project / PRIVATE_SKILL_ROOT,
            label="stale private profile file",
        )
    for item in cleanup:
        _apply_planned_removal(
            item,
            project=project,
            stop=project / LEGACY_HOST_ROOT,
            label="legacy host-visible profile file",
        )

    _atomic_json(_manifest_path(project), payload, project=project)
    return ["Perfil disponible en biblioteca JIT privada.", *operations]


def _disable(
    profile_name: str,
    *, project: Path,
    repo_root: Path,
    catalog: dict[str, Any],
    apply: bool,
) -> list[str]:
    old = _read_manifest(project)
    if old is None:
        raise ProfileError("cannot disable a profile without an Agentit project manifest")
    profiles = list(old["profiles"])
    if profile_name not in profiles:
        raise ProfileError(f"profile is not enabled in this project: {profile_name}")
    profiles.remove(profile_name)

    _validate_private_existing(project=project, old_manifest=old)
    cleanup = _legacy_cleanup_plan(project=project, manifest=old)
    payload = _build_payload(profiles, catalog=catalog, repo_root=repo_root)
    stale = _private_cleanup_plan(project=project, old_manifest=old, payload=payload)

    operations = [*(f"remove private cache: {item['path']}" for item in stale)]
    operations.extend(f"remove legacy host exposure: {item['path']}" for item in cleanup)
    if not apply:
        return ["MODO PLAN: no se escribirán archivos.", *operations]

    for item in stale:
        _apply_planned_removal(
            item,
            project=project,
            stop=project / PRIVATE_SKILL_ROOT,
            label="managed private profile file",
        )
    for item in cleanup:
        _apply_planned_removal(
            item,
            project=project,
            stop=project / LEGACY_HOST_ROOT,
            label="legacy host-visible profile file",
        )

    # Refresh still-desired private packages from source after validating they
    # were not modified; this keeps project availability current without host exposure.
    for skill_id, metadata in payload["skills"].items():
        root = _private_dir(project, skill_id)
        source = _source_dir(repo_root, skill_id)
        for relative in metadata["files"]:
            _copy_atomic(source / relative, root / relative, project=project)

    _atomic_json(_manifest_path(project), payload, project=project)
    return ["Perfil retirado de la biblioteca JIT privada.", *operations]


def _status(project: Path) -> dict[str, Any]:
    manifest = _read_manifest(project)
    if manifest is None:
        return {"profiles": [], "skills": [], "managed": False, "storage": "private-jit"}
    return {
        "profiles": manifest["profiles"],
        "skills": sorted(manifest["skills"]),
        "managed": True,
        "storage": "private-jit",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="agentit profile",
        description="Manage project profile availability without exposing non-core Agentit skills to the host.",
    )
    parser.add_argument("command", choices=("enable", "activate", "disable", "status"))
    parser.add_argument("profile", nargs="?")
    parser.add_argument("--project", type=Path, default=Path.cwd())
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--catalog", type=Path)
    parser.add_argument("--apply", action="store_true")
    args, unknown = parser.parse_known_args(argv)
    if unknown:
        parser.error(f"unrecognized arguments: {' '.join(unknown)}")

    project = args.project.absolute()
    repo_root = args.repo_root.resolve()
    try:
        catalog = load_catalog(args.catalog)
        if args.command == "status":
            print(json.dumps(_status(project), ensure_ascii=False, indent=2, sort_keys=True))
            return 0
        if not args.profile:
            raise ProfileError(f"{args.command} requiere un nombre de perfil")
        if args.command in {"enable", "activate"}:
            lines = _enable(
                args.profile,
                project=project,
                repo_root=repo_root,
                catalog=catalog,
                apply=args.apply,
            )
        else:
            lines = _disable(
                args.profile,
                project=project,
                repo_root=repo_root,
                catalog=catalog,
                apply=args.apply,
            )
        print("\n".join(lines))
        return 0
    except (ProfileError, OSError, UnicodeError) as exc:
        parser.error(str(exc))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
