"""Bounded skill profiles and safe project-local activation.

The profile catalog controls which repository skills are visible globally. The
project commands are deliberately plan-first and only remove files recorded in
the local manifest when their contents still match the installed hash.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import sys
import tempfile
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover - covered by the installer error path
    yaml = None


DEFAULT_CATALOG_PATH = Path(__file__).resolve().parents[1] / "profiles.yaml"
MANIFEST_RELATIVE_PATH = Path(".agentit") / "skills-manifest.json"


class ProfileError(RuntimeError):
    """Raised when a profile or a project activation is unsafe or invalid."""


def load_catalog(catalog_path: Path | None = None) -> dict[str, Any]:
    path = Path(catalog_path) if catalog_path is not None else DEFAULT_CATALOG_PATH
    if yaml is None:
        raise ProfileError("PyYAML is required to load profiles.yaml")
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ProfileError(f"cannot read profile catalog {path}: {exc}") from exc
    except yaml.YAMLError as exc:
        raise ProfileError(f"invalid YAML in profile catalog {path}: {exc}") from exc
    if not isinstance(raw, dict) or raw.get("schema_version") != 1:
        raise ProfileError("profile catalog must use schema_version: 1")
    profiles = raw.get("profiles")
    if not isinstance(profiles, dict) or not profiles:
        raise ProfileError("profile catalog must contain profiles")
    default_profile = raw.get("default_profile")
    global_profiles = raw.get("global_profiles")
    if not isinstance(default_profile, str) or default_profile not in profiles:
        raise ProfileError("default_profile must name a known profile")
    if not isinstance(global_profiles, list) or not all(
        isinstance(name, str) and name in profiles for name in global_profiles
    ):
        raise ProfileError("global_profiles must contain known profile names")
    for name, profile in profiles.items():
        if not isinstance(profile, dict):
            raise ProfileError(f"profile {name} must be a mapping")
        for field in ("skills", "extends"):
            value = profile.get(field, [])
            if not isinstance(value, list) or not all(
                isinstance(item, str) and item.strip() for item in value
            ):
                raise ProfileError(f"{field} for profile {name} must be a string list")
        for parent in profile.get("extends", []):
            if parent not in profiles:
                raise ProfileError(f"profile {name} extends unknown profile {parent}")
    return raw


def repository_skill_ids(repo_root: Path) -> set[str]:
    root = Path(repo_root) / "skills"
    return {
        path.parent.name
        for path in root.glob("*/SKILL.md")
        if path.is_file() and not path.is_symlink() and not path.parent.is_symlink()
    }


def resolve_profile(
    profile_name: str,
    catalog: dict[str, Any],
    *,
    repo_root: Path | None = None,
) -> list[str]:
    profiles = catalog["profiles"]
    if profile_name not in profiles:
        raise ProfileError(f"unknown profile: {profile_name}")
    resolved: list[str] = []

    def visit(name: str, chain: tuple[str, ...]) -> None:
        if name in chain:
            raise ProfileError(f"profile inheritance cycle: {' -> '.join((*chain, name))}")
        profile = profiles[name]
        for parent in profile.get("extends", []):
            visit(parent, (*chain, name))
        for skill_id in profile.get("skills", []):
            if skill_id not in resolved:
                resolved.append(skill_id)

    visit(profile_name, ())
    if repo_root is not None:
        known = repository_skill_ids(Path(repo_root))
        unknown = sorted(set(resolved) - known)
        if unknown:
            raise ProfileError(
                f"profile {profile_name} references missing repository skills: {', '.join(unknown)}"
            )
    return resolved


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _assert_safe_path(path: Path, *, root: Path) -> None:
    root = root.resolve()
    if path.is_symlink():
        raise ProfileError(f"symlink rejected: {path}")
    try:
        resolved = path.resolve(strict=False)
        resolved.relative_to(root)
    except ValueError as exc:
        raise ProfileError(f"path escapes project root: {path}") from exc
    current = path
    while current != root and current != current.parent:
        if current.is_symlink():
            raise ProfileError(f"symlink path component rejected: {current}")
        current = current.parent


def _manifest_path(project_root: Path) -> Path:
    return project_root / MANIFEST_RELATIVE_PATH


def _read_manifest(project_root: Path) -> dict[str, Any] | None:
    path = _manifest_path(project_root)
    _assert_safe_path(path, root=project_root)
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ProfileError(f"invalid project skill manifest {path}: {exc}") from exc
    if not isinstance(payload, dict) or payload.get("schema_version") != 1:
        raise ProfileError("project skill manifest must use schema_version: 1")
    if not isinstance(payload.get("profiles"), list) or not all(
        isinstance(item, str) for item in payload["profiles"]
    ):
        raise ProfileError("project skill manifest profiles must be a string list")
    if not isinstance(payload.get("skills"), dict):
        raise ProfileError("project skill manifest skills must be a mapping")
    return payload


def _project_skill_path(project_root: Path, skill_id: str) -> Path:
    return project_root / ".agents" / "skills" / skill_id / "SKILL.md"


def _skill_source_dir(repo_root: Path, skill_id: str) -> Path:
    return Path(repo_root) / "skills" / skill_id


def _list_skill_package_files(skill_dir: Path) -> list[str]:
    """Relative paths under a skill dir: SKILL.md plus references/** regular files."""
    if not skill_dir.is_dir() or skill_dir.is_symlink():
        raise ProfileError(f"skill directory is not a regular directory: {skill_dir}")
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file() or skill_md.is_symlink():
        raise ProfileError(f"source skill is not a regular file: {skill_md}")
    files = ["SKILL.md"]
    references = skill_dir / "references"
    if references.exists():
        if not references.is_dir() or references.is_symlink():
            raise ProfileError(f"skill references must be a regular directory: {references}")
        for path in sorted(references.rglob("*")):
            if path.is_symlink():
                raise ProfileError(f"skill package rejects symlinks: {path}")
            if path.is_file():
                files.append(path.relative_to(skill_dir).as_posix())
    return files


def _manifest_payload(
    profiles: list[str],
    skill_ids: list[str],
    *,
    repo_root: Path,
    existing_manifest: dict[str, Any] | None = None,
    managed_overrides: dict[str, bool] | None = None,
    file_managed_overrides: dict[str, dict[str, bool]] | None = None,
) -> dict[str, Any]:
    skills: dict[str, Any] = {}
    existing_skills = existing_manifest.get("skills", {}) if existing_manifest else {}
    managed_overrides = managed_overrides or {}
    file_managed_overrides = file_managed_overrides or {}
    for skill_id in skill_ids:
        source_dir = _skill_source_dir(repo_root, skill_id)
        package_files = _list_skill_package_files(source_dir)
        source = source_dir / "SKILL.md"
        destination = _project_skill_path(Path("."), skill_id).as_posix()
        previous = existing_skills.get(skill_id, {})
        if not isinstance(previous, dict):
            raise ProfileError(f"invalid manifest entry for {skill_id}")
        previous_files = previous.get("files")
        if not isinstance(previous_files, dict):
            previous_files = {}
        per_file_managed = file_managed_overrides.get(skill_id, {})
        file_entries: dict[str, dict[str, Any]] = {}
        for relative in package_files:
            source_file = source_dir / relative
            prev_entry = previous_files.get(relative)
            if (
                isinstance(prev_entry, dict)
                and isinstance(prev_entry.get("installed_sha256"), str)
            ):
                installed = prev_entry["installed_sha256"]
            else:
                installed = _sha256(source_file)
            if relative in per_file_managed:
                file_managed = per_file_managed[relative]
            elif isinstance(prev_entry, dict) and isinstance(
                prev_entry.get("managed"), bool
            ):
                file_managed = bool(prev_entry["managed"])
            elif relative == "SKILL.md" and previous and "managed" in previous:
                file_managed = bool(previous.get("managed", True))
            else:
                file_managed = True
            file_entries[relative] = {
                "source_sha256": _sha256(source_file),
                "installed_sha256": installed,
                "managed": file_managed,
            }
        installed_sha256 = file_entries["SKILL.md"]["installed_sha256"]
        skill_managed = managed_overrides.get(
            skill_id,
            any(entry["managed"] for entry in file_entries.values())
            if file_entries
            else bool(previous.get("managed", True)),
        )
        skills[skill_id] = {
            "destination": destination,
            "source_sha256": _sha256(source),
            "installed_sha256": installed_sha256,
            "managed": skill_managed,
            "files": file_entries,
        }
    return {
        "schema_version": 1,
        "profiles": profiles,
        "skills": skills,
    }


def _write_manifest(path: Path, payload: dict[str, Any], *, project_root: Path) -> None:
    _assert_safe_path(path, root=project_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    _assert_safe_path(path.parent, root=project_root)
    fd, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.tmp-", dir=path.parent, text=True
    )
    temporary_path = Path(temporary_name)
    try:
        os.fchmod(fd, stat.S_IRUSR | stat.S_IWUSR)
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(payload, stream, ensure_ascii=False, indent=2, sort_keys=True)
            stream.write("\n")
        os.replace(temporary_path, path)
    finally:
        temporary_path.unlink(missing_ok=True)


def _copy_skill_file(source: Path, destination: Path, *, project_root: Path) -> None:
    _assert_safe_path(destination, root=project_root)
    destination.parent.mkdir(parents=True, exist_ok=True)
    _assert_safe_path(destination.parent, root=project_root)
    fd, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.tmp-", dir=destination.parent
    )
    temporary_path = Path(temporary_name)
    os.close(fd)
    try:
        shutil.copy2(source, temporary_path)
        os.replace(temporary_path, destination)
    finally:
        temporary_path.unlink(missing_ok=True)


def _copy_skill(source: Path, destination: Path, *, project_root: Path) -> None:
    """Backward-compatible single-file skill copy."""
    _copy_skill_file(source, destination, project_root=project_root)


def _package_files(metadata: dict[str, Any]) -> list[str]:
    files = metadata.get("files")
    if isinstance(files, dict) and files:
        return sorted(str(key) for key in files)
    return ["SKILL.md"]


def _managed_package_files(metadata: dict[str, Any]) -> list[str]:
    files = metadata.get("files")
    if isinstance(files, dict) and files:
        managed: list[str] = []
        for relative, entry in files.items():
            if isinstance(entry, dict) and entry.get("managed") is False:
                continue
            managed.append(str(relative))
        if managed:
            return sorted(managed)
        return []
    if metadata.get("managed", True):
        return ["SKILL.md"]
    return []


def _skill_file_installed_hash(metadata: dict[str, Any], relative: str) -> str | None:
    files = metadata.get("files")
    if isinstance(files, dict):
        entry = files.get(relative)
        if isinstance(entry, dict) and isinstance(entry.get("installed_sha256"), str):
            return entry["installed_sha256"]
    if relative == "SKILL.md" and isinstance(metadata.get("installed_sha256"), str):
        return metadata["installed_sha256"]
    return None


def _active_skill_ids(
    profiles: list[str], catalog: dict[str, Any], *, repo_root: Path
) -> list[str]:
    active: list[str] = []
    for profile in profiles:
        for skill_id in resolve_profile(profile, catalog, repo_root=repo_root):
            if skill_id not in active:
                active.append(skill_id)
    return active


def _check_enable(
    project_root: Path,
    profile_name: str,
    *,
    catalog: dict[str, Any],
    repo_root: Path,
) -> tuple[dict[str, Any], list[str]]:
    if not project_root.is_dir() or project_root.is_symlink():
        raise ProfileError(f"project root must be a regular directory: {project_root}")
    _assert_safe_path(project_root, root=project_root)
    manifest = _read_manifest(project_root)
    profiles = list(manifest["profiles"]) if manifest else []
    if profile_name not in profiles:
        profiles.append(profile_name)
    for name in profiles:
        if name not in catalog["profiles"]:
            raise ProfileError(f"unknown profile in project manifest: {name}")
    skill_ids = _active_skill_ids(profiles, catalog, repo_root=repo_root)
    operations: list[str] = []
    managed_overrides: dict[str, bool] = {}
    file_managed_overrides: dict[str, dict[str, bool]] = {}
    for skill_id in skill_ids:
        source_dir = _skill_source_dir(repo_root, skill_id)
        package_files = _list_skill_package_files(source_dir)
        skill_destination = _project_skill_path(project_root, skill_id)
        skill_root = skill_destination.parent
        _assert_safe_path(skill_destination, root=project_root)
        previous = manifest.get("skills", {}).get(skill_id) if manifest else None
        previous_files = (
            previous.get("files")
            if isinstance(previous, dict) and isinstance(previous.get("files"), dict)
            else {}
        )
        per_file: dict[str, bool] = {}
        for path in skill_root.rglob("*") if skill_root.exists() else []:
            if not path.is_file():
                continue
            relative = path.relative_to(skill_root).as_posix()
            if relative not in package_files:
                raise ProfileError(
                    f"refusing to install into skill directory with extra files: {path}"
                )
            if _sha256(path) != _sha256(source_dir / relative):
                raise ProfileError(
                    f"refusing to overwrite modified skill package file: {path}"
                )
        for relative in package_files:
            dest = skill_root / relative
            if dest.exists():
                operations.append(f"keep: {dest}")
                prev_entry = previous_files.get(relative)
                if isinstance(prev_entry, dict) and isinstance(
                    prev_entry.get("managed"), bool
                ):
                    per_file[relative] = bool(prev_entry["managed"])
                elif (
                    relative == "SKILL.md"
                    and isinstance(previous, dict)
                    and "managed" in previous
                ):
                    per_file[relative] = bool(previous.get("managed", True))
                elif previous is None:
                    per_file[relative] = False
                else:
                    per_file[relative] = True
            else:
                operations.append(f"install: {dest}")
                per_file[relative] = True
        file_managed_overrides[skill_id] = per_file
        managed_overrides[skill_id] = any(per_file.values())
    return (
        _manifest_payload(
            profiles,
            skill_ids,
            repo_root=repo_root,
            existing_manifest=manifest,
            managed_overrides=managed_overrides,
            file_managed_overrides=file_managed_overrides,
        ),
        operations,
    )


def _check_disable(
    project_root: Path,
    profile_name: str,
    *,
    catalog: dict[str, Any],
    repo_root: Path,
) -> tuple[dict[str, Any], list[str]]:
    manifest = _read_manifest(project_root)
    if manifest is None:
        raise ProfileError("cannot disable a profile without an Agentit project manifest")
    profiles = list(manifest["profiles"])
    if profile_name not in profiles:
        raise ProfileError(f"profile is not enabled in this project: {profile_name}")
    profiles.remove(profile_name)
    desired = set(_active_skill_ids(profiles, catalog, repo_root=repo_root))
    operations: list[str] = []
    for skill_id, metadata in manifest["skills"].items():
        if skill_id in desired:
            continue
        if not isinstance(metadata, dict) or not isinstance(
            metadata.get("destination"), str
        ):
            raise ProfileError(f"invalid manifest entry for {skill_id}")
        managed_files = _managed_package_files(metadata)
        if not managed_files:
            continue
        skill_root = (project_root / metadata["destination"]).parent
        _assert_safe_path(skill_root, root=project_root)
        known_files = set(_package_files(metadata))
        for relative in managed_files:
            destination = skill_root / relative
            _assert_safe_path(destination, root=project_root)
            if not destination.is_file() or destination.is_symlink():
                raise ProfileError(
                    f"managed skill destination is not a regular file: {destination}"
                )
            expected = _skill_file_installed_hash(metadata, relative)
            if expected is None or expected != _sha256(destination):
                raise ProfileError(
                    f"refusing to remove modified managed skill: {destination}"
                )
            operations.append(f"remove: {destination}")
        for path in skill_root.rglob("*"):
            if path.is_file():
                relative = path.relative_to(skill_root).as_posix()
                if relative not in known_files:
                    raise ProfileError(
                        f"refusing to remove skill directory with extra files: {path}"
                    )
    return (
        _manifest_payload(
            profiles,
            _active_skill_ids(profiles, catalog, repo_root=repo_root),
            repo_root=repo_root,
            existing_manifest=manifest,
        ),
        operations,
    )


def enable_profile(
    profile_name: str,
    *,
    project_root: Path,
    repo_root: Path,
    catalog_path: Path | None = None,
    apply: bool = False,
) -> list[str]:
    catalog = load_catalog(catalog_path)
    payload, operations = _check_enable(
        project_root, profile_name, catalog=catalog, repo_root=repo_root
    )
    if not apply:
        return ["MODO PLAN: no se escribirán archivos.", *operations]
    for skill_id, metadata in payload["skills"].items():
        source_dir = _skill_source_dir(repo_root, skill_id)
        skill_root = (project_root / metadata["destination"]).parent
        for relative in _package_files(metadata):
            destination = skill_root / relative
            if not destination.exists():
                _copy_skill_file(
                    source_dir / relative, destination, project_root=project_root
                )
    for skill_id, metadata in payload["skills"].items():
        skill_root = (project_root / metadata["destination"]).parent
        files = metadata.get("files")
        if not isinstance(files, dict):
            continue
        for relative, file_meta in files.items():
            if not isinstance(file_meta, dict):
                continue
            path = skill_root / relative
            if path.is_file() and not path.is_symlink():
                digest = _sha256(path)
                file_meta["installed_sha256"] = digest
                if relative == "SKILL.md":
                    metadata["installed_sha256"] = digest
    _write_manifest(_manifest_path(project_root), payload, project_root=project_root)
    return ["Perfil activado.", *operations]


def disable_profile(
    profile_name: str,
    *,
    project_root: Path,
    repo_root: Path,
    catalog_path: Path | None = None,
    apply: bool = False,
) -> list[str]:
    catalog = load_catalog(catalog_path)
    payload, operations = _check_disable(
        project_root, profile_name, catalog=catalog, repo_root=repo_root
    )
    if not apply:
        return ["MODO PLAN: no se escribirán archivos.", *operations]
    for operation in operations:
        destination = Path(operation.removeprefix("remove: "))
        destination.unlink()
        current = destination.parent
        while current != project_root and current != current.parent:
            try:
                current.rmdir()
            except OSError:
                break
            current = current.parent
    _write_manifest(_manifest_path(project_root), payload, project_root=project_root)
    return ["Perfil desactivado.", *operations]


def project_status(*, project_root: Path) -> dict[str, Any]:
    manifest = _read_manifest(project_root)
    if manifest is None:
        return {"profiles": [], "skills": [], "managed": False}
    return {
        "profiles": manifest["profiles"],
        "skills": sorted(manifest["skills"]),
        "managed": True,
    }


def _is_file_safe(path_str: str | None) -> bool:
    if not path_str or "\n" in path_str or "\r" in path_str or len(path_str) > 255:
        return False
    try:
        p = Path(path_str)
        return p.is_file() and not p.is_symlink()
    except Exception:
        return False


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Manage bounded Agentit skill profiles, context engines, incubator scout, and MCP catalog."
    )
    parser.add_argument(
        "command",
        nargs="?",
        choices=(
            "enable",
            "activate",
            "disable",
            "status",
            "artifact",
            "context",
            "scout",
            "worker",
            "mcp",
            "verify",
            "continuity",
            "capabilities",
        ),
    )
    parser.add_argument("subcommand", nargs="?")
    parser.add_argument("target", nargs="?")
    parser.add_argument("extra_arg", nargs="?")
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--catalog", type=Path)
    parser.add_argument("--project", type=Path, default=Path.cwd())
    parser.add_argument("--profile")
    parser.add_argument("--format", choices=("ids", "json", "text"), default="ids")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--session", default="default")
    parser.add_argument("--description", default="CLI context artifact")
    parser.add_argument("--lines", help="Line range N:M for artifact read")
    parser.add_argument("--reason", default="Rejected during evaluation")
    parser.add_argument(
        "--provider",
        choices=("claude", "cursor", "codex", "json"),
        default="json",
        help="MCP snippet provider format (mcp command only)",
    )
    parser.add_argument(
        "--tier",
        choices=("core", "recommended", "situational"),
        help="Filter MCP catalog by tier",
    )
    parser.add_argument(
        "--category",
        help="Filter MCP catalog by category (e.g. browser, documentation)",
    )
    parser.add_argument(
        "--max-risk",
        dest="max_risk",
        choices=("RISK_1", "RISK_2", "RISK_3", "RISK_4"),
        help="Filter MCP servers at or below this risk level",
    )
    parser.add_argument(
        "--providers",
        help="Comma-separated MCP providers (claude,cursor,codex,grok,antigravity,project) or all",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Allow RISK_3/RISK_4 MCP enable",
    )
    parser.add_argument("--host", default="local", help="Capability provider host")
    parser.add_argument(
        "--available",
        help="Comma-separated explicit capability provider inventory",
    )
    parser.add_argument("--required", help="Comma-separated required capability IDs")
    parser.add_argument("--preferred", help="Comma-separated preferred capability IDs")
    parser.add_argument(
        "--specialist",
        action="append",
        default=[],
        help="Semantic specialist ID whose capabilities should be included (repeatable)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    try:
        repo_root = args.repo_root.resolve()
        catalog = load_catalog(args.catalog)
        if args.command is None:
            profile_name = args.profile or catalog["default_profile"]
            skill_ids = resolve_profile(profile_name, catalog, repo_root=repo_root)
            if args.format == "json":
                print(json.dumps(skill_ids, ensure_ascii=False, indent=2))
            else:
                print("\n".join(skill_ids))
            return 0

        project_root = args.project.absolute()
        if project_root.is_symlink():
            raise ProfileError(f"project root symlink rejected: {project_root}")

        if args.command == "capabilities":
            try:
                from router.capabilities import (
                    CapabilityCatalogError,
                    load_capability_catalog,
                    resolve_capabilities,
                    specialist_capability_requirements,
                )
            except ImportError:
                from capabilities import (
                    CapabilityCatalogError,
                    load_capability_catalog,
                    resolve_capabilities,
                    specialist_capability_requirements,
                )

            def comma_list(value: str | None) -> list[str]:
                return [item.strip() for item in (value or "").split(",") if item.strip()]

            try:
                capability_catalog = load_capability_catalog(
                    repo_root / "capabilities" / "catalog.yaml"
                )
                sub = args.subcommand or "list"
                if sub == "list":
                    payload = {
                        "policy": capability_catalog["policy"],
                        "capabilities": sorted(capability_catalog["capabilities"]),
                        "providers": sorted(capability_catalog["providers"]),
                    }
                elif sub == "show":
                    if not args.target:
                        parser.error("capabilities show requires a capability ID")
                    capability = capability_catalog["capabilities"].get(args.target)
                    if capability is None:
                        raise CapabilityCatalogError(
                            f"unknown capability: {args.target}"
                        )
                    payload = {"id": args.target, **capability}
                elif sub == "resolve":
                    requirements = specialist_capability_requirements(
                        args.specialist,
                        capability_catalog=capability_catalog,
                    )
                    required = list(
                        dict.fromkeys(
                            [*requirements["required"], *comma_list(args.required)]
                        )
                    )
                    preferred = [
                        capability
                        for capability in dict.fromkeys(
                            [*requirements["preferred"], *comma_list(args.preferred)]
                        )
                        if capability not in required
                    ]
                    payload = resolve_capabilities(
                        required=required,
                        preferred=preferred,
                        available_providers=(
                            comma_list(args.available)
                            if args.available is not None
                            else None
                        ),
                        host=args.host,
                        catalog=capability_catalog,
                    )
                else:
                    parser.error("capabilities requires list, show, or resolve")
            except CapabilityCatalogError as exc:
                raise ProfileError(str(exc)) from exc
            print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
            return 0

        if args.command == "verify":
            prompt_parts = [
                part
                for part in (args.subcommand, args.target, args.extra_arg)
                if part
            ]
            task_text = " ".join(prompt_parts).strip()
            try:
                from router.verify import VerifyError, apply_verification, format_plan, plan_verification
            except ImportError:
                from verify import VerifyError, apply_verification, format_plan, plan_verification
            try:
                if args.apply:
                    payload = apply_verification(
                        project_root,
                        task_text=task_text,
                    )
                else:
                    payload = plan_verification(
                        project_root,
                        task_text=task_text,
                    )
            except VerifyError as exc:
                raise ProfileError(str(exc)) from exc
            if args.format == "json":
                print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
            else:
                print(format_plan(payload))
            return 0

        if args.command == "continuity":
            sub = args.subcommand or "status"
            try:
                from router.continuity import (
                    ContinuityError,
                    ensure_state_file,
                    list_checkpoints,
                    resume_report,
                    write_checkpoint,
                )
            except ImportError:
                from continuity import (
                    ContinuityError,
                    ensure_state_file,
                    list_checkpoints,
                    resume_report,
                    write_checkpoint,
                )
            try:
                if sub == "init":
                    goal = " ".join(
                        p for p in (args.target, args.extra_arg) if p
                    ).strip()
                    path = ensure_state_file(
                        project_root,
                        goal=goal,
                        overwrite=bool(args.apply),
                    )
                    payload = {"action": "init", "path": str(path)}
                elif sub == "status":
                    payload = resume_report(project_root)
                    payload["checkpoints"] = list_checkpoints(project_root)
                elif sub == "checkpoint":
                    label = args.target or "manual"
                    note = args.extra_arg or ""
                    path = write_checkpoint(
                        project_root,
                        label=label,
                        payload={"note": note, "project": str(project_root)},
                    )
                    payload = {"action": "checkpoint", "path": str(path)}
                else:
                    parser.error("continuity subcomando: init|status|checkpoint")
                    return 2
            except ContinuityError as exc:
                raise ProfileError(str(exc)) from exc
            print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
            return 0

        if args.command == "artifact":
            sub = args.subcommand
            uri = args.target
            if not sub or not uri:
                parser.error("artifact requiere subcomando (get|read|grep) y URI (agentit://artifacts/...)")

            try:
                from router.artifact_ref import resolve_agentit_uri
            except ImportError:
                from artifact_ref import resolve_agentit_uri

            path = resolve_agentit_uri(uri, project_root=project_root)

            if sub in {"get", "read"}:
                text = path.read_text(encoding="utf-8")
                if args.lines and ":" in args.lines:
                    parts = args.lines.split(":", 1)
                    start = int(parts[0]) - 1 if parts[0].isdigit() else 0
                    end = int(parts[1]) if parts[1].isdigit() else len(text.splitlines())
                    lines = text.splitlines()[start:end]
                    print("\n".join(lines))
                else:
                    print(text)
                return 0

            if sub == "grep":
                pattern = args.extra_arg
                if not pattern:
                    parser.error("artifact grep requiere un patrón")
                text = path.read_text(encoding="utf-8")
                rgx = re.compile(pattern, re.IGNORECASE)
                for line_no, line in enumerate(text.splitlines(), 1):
                    if rgx.search(line):
                        print(f"{line_no}:{line}")
                return 0

            parser.error(f"subcomando artifact desconocido: {sub}")

        if args.command == "context":
            sub = args.subcommand
            file_or_text = args.target
            content = ""
            if file_or_text and _is_file_safe(file_or_text):
                content = Path(file_or_text).read_text(encoding="utf-8")
            elif file_or_text:
                content = file_or_text
            else:
                content = sys.stdin.read()

            artifact_dir = project_root / ".agentit" / "artifacts"

            if sub == "filter":
                try:
                    from router.tool_filter import filter_tool_output
                except ImportError:
                    from tool_filter import filter_tool_output
                res = filter_tool_output(content, artifact_dir=artifact_dir)
                print(res["content"])
                return 0

            if sub == "archive":
                try:
                    from router.artifact_ref import create_artifact_reference
                except ImportError:
                    from artifact_ref import create_artifact_reference
                res = create_artifact_reference(content, description=args.description, artifact_dir=artifact_dir)
                print(json.dumps(res, ensure_ascii=False, indent=2))
                return 0

            if sub == "dedup":
                try:
                    from router.dedup import ContextDeduplicator
                except ImportError:
                    from dedup import ContextDeduplicator
                deduper = ContextDeduplicator(session_id=args.session, project_dir=project_root)
                res = deduper.process_block(content)
                print(res["content"])
                return 0

            parser.error(f"subcomando context desconocido: {sub}")

        if args.command == "worker":
            try:
                from router.worker_context import (
                    WorkerContextError,
                    WorkerTaskSpec,
                    build_worker_context,
                    render_worker_prompt,
                    validate_for_spawn,
                )
            except ImportError:
                from worker_context import (
                    WorkerContextError,
                    WorkerTaskSpec,
                    build_worker_context,
                    render_worker_prompt,
                    validate_for_spawn,
                )

            sub = args.subcommand or "build"
            if sub not in {"build", "render", "validate"}:
                parser.error("worker requiere subcomando build|render|validate")

            objective = args.target or ""
            if not objective:
                parser.error(
                    "worker build requiere un objetivo "
                    '(ej: agentit worker build "Add settings page" --skill security-and-hardening)'
                )

            skills: list[str] = []
            if args.extra_arg:
                skills = [s.strip() for s in args.extra_arg.split(",") if s.strip()]

            try:
                try:
                    from router.preferences import load_preferences
                except ImportError:
                    from preferences import load_preferences
                prefs = load_preferences()

                spec = WorkerTaskSpec(
                    objective=objective,
                    skills=tuple(skills),
                    risk="RISK_2",
                    role="implementer",
                    specialist_ids=tuple(args.specialist),
                    required_capabilities=tuple(
                        item.strip()
                        for item in (args.required or "").split(",")
                        if item.strip()
                    ),
                    preferred_capabilities=tuple(
                        item.strip()
                        for item in (args.preferred or "").split(",")
                        if item.strip()
                    ),
                    available_providers=(
                        tuple(
                            item.strip()
                            for item in args.available.split(",")
                            if item.strip()
                        )
                        if args.available is not None
                        else None
                    ),
                    provider_host=args.host,
                )
                payload = build_worker_context(
                    spec,
                    project_root=project_root,
                    preferences=prefs,
                )
                validate_for_spawn(
                    payload,
                    require_project_instructions=False,
                )
            except WorkerContextError as exc:
                raise ProfileError(str(exc)) from exc

            if sub == "render" or args.format == "text":
                print(render_worker_prompt(payload), end="")
            else:
                print(json.dumps(payload, ensure_ascii=False, indent=2))
            return 0

        if args.command == "mcp":
            try:
                from router.mcp_catalog import (
                    McpCatalogError,
                    catalog_summary,
                    get_server,
                    list_servers,
                    list_stacks,
                    load_catalog as load_mcp_catalog,
                    plan_stack,
                    recommend_for_task,
                    recommend_stack,
                    snippet_for_server,
                )
                from router.mcp_runtime import (
                    McpRuntimeError,
                    bootstrap_gateway,
                    disable_server,
                    enable_server,
                    enable_stack,
                    resolve_providers_arg,
                    runtime_status,
                )
            except ImportError:
                from mcp_catalog import (
                    McpCatalogError,
                    catalog_summary,
                    get_server,
                    list_servers,
                    list_stacks,
                    load_catalog as load_mcp_catalog,
                    plan_stack,
                    recommend_for_task,
                    recommend_stack,
                    snippet_for_server,
                )
                from mcp_runtime import (
                    McpRuntimeError,
                    bootstrap_gateway,
                    disable_server,
                    enable_server,
                    enable_stack,
                    resolve_providers_arg,
                    runtime_status,
                )

            sub = args.subcommand or "status"
            try:
                mcp_catalog = load_mcp_catalog(repo_root / "mcp" / "catalog.yaml")
                provs = resolve_providers_arg(args.providers)

                if sub in {"status", "available", "active"}:
                    payload = runtime_status(project_root=project_root, providers=provs)
                    if sub == "available":
                        print(json.dumps({"servers": payload["available"]}, ensure_ascii=False, indent=2))
                    elif sub == "active":
                        print(
                            json.dumps(
                                {
                                    "desired_enabled": payload["desired_enabled"],
                                    "active_union": payload["active_union"],
                                },
                                ensure_ascii=False,
                                indent=2,
                            )
                        )
                    else:
                        print(json.dumps(payload, ensure_ascii=False, indent=2))
                    return 0

                if sub == "list":
                    if args.format == "text":
                        rows = list_servers(
                            mcp_catalog,
                            tier=args.tier,
                            category=args.category,
                            max_risk=args.max_risk,
                        )
                        for row in rows:
                            print(
                                f"{row['id']}\t{row['tier']}\t{row['risk']}\t"
                                f"{row['category']}\t{row['summary']}"
                            )
                    else:
                        print(
                            json.dumps(
                                catalog_summary(mcp_catalog)
                                if not any((args.tier, args.category, args.max_risk))
                                else {
                                    "servers": list_servers(
                                        mcp_catalog,
                                        tier=args.tier,
                                        category=args.category,
                                        max_risk=args.max_risk,
                                    )
                                },
                                ensure_ascii=False,
                                indent=2,
                            )
                        )
                    return 0

                if sub == "stacks":
                    print(json.dumps(list_stacks(mcp_catalog), ensure_ascii=False, indent=2))
                    return 0

                if sub == "show":
                    server_id = args.target
                    if not server_id:
                        parser.error("mcp show requiere un id de servidor")
                    print(json.dumps(get_server(server_id, mcp_catalog), ensure_ascii=False, indent=2))
                    return 0

                if sub == "recommend":
                    target = args.target or "developer_core"
                    stacks = list_stacks(mcp_catalog)
                    if target in stacks:
                        payload = recommend_stack(target, mcp_catalog)
                    else:
                        payload = recommend_for_task(target, mcp_catalog)
                    print(json.dumps(payload, ensure_ascii=False, indent=2))
                    return 0

                if sub == "snippet":
                    server_id = args.target
                    if not server_id:
                        parser.error("mcp snippet requiere un id de servidor")
                    payload = snippet_for_server(
                        server_id,
                        provider=args.provider,
                        catalog=mcp_catalog,
                        project_root=str(project_root),
                    )
                    if args.format == "text" and payload.get("command"):
                        print(payload["command"])
                    elif args.format == "text" and payload.get("snippet"):
                        print(payload["snippet"])
                    else:
                        print(json.dumps(payload, ensure_ascii=False, indent=2))
                    return 0

                if sub == "plan":
                    stack_name = args.target or "developer_core"
                    payload = plan_stack(
                        stack_name,
                        provider=args.provider,
                        catalog=mcp_catalog,
                        project_root=str(project_root),
                    )
                    print(json.dumps(payload, ensure_ascii=False, indent=2))
                    return 0

                if sub == "enable":
                    server_id = args.target
                    if not server_id:
                        parser.error("mcp enable requiere un id (o stack con enable-stack)")
                    payload = enable_server(
                        server_id,
                        project_root=project_root,
                        providers=provs,
                        apply=args.apply,
                        force=args.force,
                    )
                    print(json.dumps(payload, ensure_ascii=False, indent=2))
                    return 0

                if sub == "disable":
                    server_id = args.target
                    if not server_id:
                        parser.error("mcp disable requiere un id de servidor")
                    payload = disable_server(
                        server_id,
                        project_root=project_root,
                        providers=provs,
                        apply=args.apply,
                    )
                    print(json.dumps(payload, ensure_ascii=False, indent=2))
                    return 0

                if sub in {"enable-stack", "stack-enable"}:
                    stack_name = args.target or "developer_core"
                    known_stacks = list_stacks(mcp_catalog)
                    if stack_name not in known_stacks:
                        raise McpRuntimeError(
                            f"unknown MCP stack '{stack_name}'; known: {', '.join(known_stacks)}"
                        )
                    payload = enable_stack(
                        stack_name,
                        project_root=project_root,
                        providers=provs,
                        apply=args.apply,
                        force=args.force,
                    )
                    print(json.dumps(payload, ensure_ascii=False, indent=2))
                    return 0

                if sub in {"install-gateway", "gateway"}:
                    payload = bootstrap_gateway(
                        project_root=project_root,
                        repo_root=repo_root,
                        providers=provs,
                        apply=args.apply,
                    )
                    print(json.dumps(payload, ensure_ascii=False, indent=2))
                    return 0

                parser.error(
                    "mcp: status|available|active|list|stacks|show|recommend|snippet|plan|"
                    "enable|disable|enable-stack|install-gateway"
                )
            except (McpCatalogError, McpRuntimeError) as exc:
                raise ProfileError(str(exc)) from exc

        if args.command == "scout":
            try:
                from router.scout import add_candidate, inspect_candidate, load_candidates, load_rejected, reject_candidate
            except ImportError:
                from scout import add_candidate, inspect_candidate, load_candidates, load_rejected, reject_candidate

            sub = args.subcommand or "status"
            if sub == "status":
                cand_data = load_candidates()
                rej_data = load_rejected()
                status_payload = {
                    "active_candidates": len(cand_data.get("candidates", [])),
                    "rejected_candidates": len(rej_data.get("rejected", [])),
                    "candidates": cand_data.get("candidates", []),
                }
                print(json.dumps(status_payload, ensure_ascii=False, indent=2))
                return 0

            if sub == "add":
                url_or_claim = args.target
                if not url_or_claim:
                    parser.error("scout add requiere un URL o claim")
                item = add_candidate(url_or_claim)
                print(json.dumps(item, ensure_ascii=False, indent=2))
                return 0

            if sub == "inspect":
                cand_id = args.target
                if not cand_id:
                    parser.error("scout inspect requiere un ID de candidato")
                item = inspect_candidate(cand_id)
                if not item:
                    print(f"Candidato '{cand_id}' no encontrado.", file=sys.stderr)
                    return 1
                print(json.dumps(item, ensure_ascii=False, indent=2))
                return 0

            if sub == "reject":
                cand_id = args.target
                if not cand_id:
                    parser.error("scout reject requiere un ID de candidato")
                ok = reject_candidate(cand_id, reason=args.reason)
                if ok:
                    print(f"Candidato '{cand_id}' rechazado.")
                    return 0
                print(f"Candidato '{cand_id}' no encontrado.", file=sys.stderr)
                return 1

            parser.error(f"subcomando scout desconocido: {sub}")

        if args.command in {"enable", "activate", "disable"} and not args.subcommand:
            parser.error(f"{args.command} requiere un nombre de perfil")

        target_name = args.subcommand
        if args.command in {"enable", "activate"}:
            lines = enable_profile(
                target_name,
                project_root=project_root,
                repo_root=repo_root,
                catalog_path=args.catalog,
                apply=args.apply,
            )
        elif args.command == "disable":
            lines = disable_profile(
                target_name,
                project_root=project_root,
                repo_root=repo_root,
                catalog_path=args.catalog,
                apply=args.apply,
            )
        else:
            status = project_status(project_root=project_root)
            if args.format == "json":
                print(json.dumps(status, ensure_ascii=False, indent=2, sort_keys=True))
            else:
                print(f"profiles: {', '.join(status['profiles']) or '(none)'}")
                print(f"skills: {len(status['skills'])}")
                print(f"managed: {'yes' if status['managed'] else 'no'}")
            return 0
        print("\n".join(lines))
        return 0
    except (ProfileError, ValueError, PermissionError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
