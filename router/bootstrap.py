"""Portable, agent-facing Agentit bootstrap for macOS and GNU/Linux.

Only Agentit's three core navigation skills are projected into provider-visible
skill roots. The full Agentit skill library remains private inside the Agentit
runtime and is loaded JIT through ``agentit skills``.

Semantic task decisions never happen here. This module is mechanical packaging,
provider-surface hygiene, backup and rollback only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import subprocess
import sys
import tempfile
import venv
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from router.host_skill_hygiene import (
    HostSkillHygieneError,
    apply_host_skill_hygiene,
    plan_host_skill_hygiene,
    restore_removed_tree,
    validate_removed_tree_record,
)


SOURCE_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_NAME = "bootstrap-manifest.json"


class BootstrapError(RuntimeError):
    """Raised when bootstrap cannot proceed without violating safety invariants."""


@dataclass(frozen=True)
class CopySpec:
    destination: Path
    source: Path | None = None
    content: bytes | None = None
    mode: int | None = None
    category: str = "managed"

    def payload(self) -> bytes:
        if self.content is not None:
            return self.content
        if self.source is None:
            raise BootstrapError(f"copy spec has no source/content: {self.destination}")
        return self.source.read_bytes()


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load_manifest(source_root: Path = SOURCE_ROOT) -> dict[str, Any]:
    path = source_root / MANIFEST_NAME
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise BootstrapError(f"cannot read {path}: {exc}") from exc
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise BootstrapError("bootstrap manifest must use schema_version: 1")
    return data


def _assert_relative(value: str) -> Path:
    path = Path(value)
    if path.is_absolute() or not value or any(part in {"", ".", ".."} for part in path.parts):
        raise BootstrapError(f"unsafe relative path in bootstrap manifest: {value!r}")
    return path


def _assert_no_symlink_components(path: Path, *, stop: Path | None = None) -> None:
    current = path.absolute()
    stop_abs = stop.absolute() if stop is not None else None
    while True:
        if current.is_symlink():
            raise BootstrapError(f"symlink component rejected: {current}")
        if stop_abs is not None and current == stop_abs:
            return
        parent = current.parent
        if parent == current:
            return
        current = parent


def _safe_home(raw: Path) -> Path:
    home = raw.expanduser().absolute()
    if not home.is_dir() or home.is_symlink():
        raise BootstrapError(f"home must be an existing regular directory: {home}")
    _assert_no_symlink_components(home)
    return home


def _destination(home: Path, relative: str | Path) -> Path:
    rel = _assert_relative(str(relative))
    destination = (home / rel).absolute()
    try:
        destination.relative_to(home)
    except ValueError as exc:
        raise BootstrapError(f"destination escapes home: {destination}") from exc
    _assert_no_symlink_components(destination, stop=home)
    return destination


def _source(source_root: Path, relative: str | Path) -> Path:
    rel = _assert_relative(str(relative))
    path = (source_root / rel).absolute()
    try:
        path.relative_to(source_root.absolute())
    except ValueError as exc:
        raise BootstrapError(f"source escapes repository: {path}") from exc
    _assert_no_symlink_components(path, stop=source_root)
    if not path.exists():
        raise BootstrapError(f"bootstrap source is missing: {path}")
    return path


def _excluded(relative: Path, manifest: dict[str, Any]) -> bool:
    names = {str(item) for item in manifest.get("runtime_exclude_names") or []}
    prefixes = tuple(str(item) for item in manifest.get("runtime_exclude_prefixes") or [])
    if any(part in names for part in relative.parts):
        return True
    return any(relative.as_posix().startswith(prefix) for prefix in prefixes)


def _tree_files(root: Path) -> Iterable[Path]:
    if root.is_symlink():
        raise BootstrapError(f"symlink source rejected: {root}")
    if root.is_file():
        yield root
        return
    if not root.is_dir():
        raise BootstrapError(f"bootstrap source is not file/directory: {root}")
    for base, dirnames, filenames in os.walk(root, followlinks=False):
        base_path = Path(base)
        for name in dirnames:
            candidate = base_path / name
            if candidate.is_symlink():
                raise BootstrapError(f"symlink in bootstrap source tree rejected: {candidate}")
        for name in filenames:
            candidate = base_path / name
            if not candidate.is_file() or candidate.is_symlink():
                raise BootstrapError(f"non-regular bootstrap source rejected: {candidate}")
            yield candidate


def _append_tree_specs(
    specs: list[CopySpec],
    *,
    source_base: Path,
    destination_base: Path,
    category: str,
    manifest: dict[str, Any] | None = None,
    manifest_relative_base: Path | None = None,
) -> None:
    for file_path in _tree_files(source_base):
        rel = file_path.relative_to(source_base) if source_base.is_dir() else Path(file_path.name)
        if manifest is not None and manifest_relative_base is not None:
            full_rel = manifest_relative_base / rel if source_base.is_dir() else manifest_relative_base
            if _excluded(full_rel, manifest):
                continue
        specs.append(
            CopySpec(
                source=file_path,
                destination=destination_base / rel if source_base.is_dir() else destination_base,
                mode=stat.S_IMODE(file_path.stat().st_mode),
                category=category,
            )
        )


def _runtime_specs(*, home: Path, source_root: Path, manifest: dict[str, Any]) -> list[CopySpec]:
    runtime_root = _destination(home, Path(".agentit") / "runtime")
    specs: list[CopySpec] = []
    for raw in manifest.get("runtime_paths") or []:
        rel = _assert_relative(str(raw))
        src = _source(source_root, rel)
        _append_tree_specs(
            specs,
            source_base=src,
            destination_base=runtime_root / rel,
            category="runtime",
            manifest=manifest,
            manifest_relative_base=rel,
        )
    return specs


def _provider_specs(
    *,
    home: Path,
    source_root: Path,
    manifest: dict[str, Any],
    providers: list[str],
    with_settings: bool,
    with_local_settings: bool,
    with_hook: bool,
) -> list[CopySpec]:
    specs: list[CopySpec] = []
    catalog = manifest.get("providers") or {}
    core_skills = [str(item) for item in manifest.get("core_skills") or []]

    for provider in providers:
        config = catalog.get(provider)
        if not isinstance(config, dict):
            raise BootstrapError(f"unknown provider in bootstrap manifest: {provider}")
        skills_root = _destination(home, str(config["skills_root"]))
        for skill_id in core_skills:
            if not skill_id or any(ch not in "abcdefghijklmnopqrstuvwxyz0123456789-" for ch in skill_id):
                raise BootstrapError(f"invalid core skill id: {skill_id!r}")
            src = _source(source_root, Path("skills") / skill_id)
            _append_tree_specs(
                specs,
                source_base=src,
                destination_base=skills_root / skill_id,
                category=f"provider:{provider}:skill",
            )

        if provider == "codex" and config.get("codex_agents_source"):
            destination_root = _destination(home, str(config["agents_root"]))
            for filename in manifest.get("codex_agent_profiles") or []:
                src = _source(source_root, Path(str(config["codex_agents_source"])) / str(filename))
                specs.append(
                    CopySpec(
                        source=src,
                        destination=destination_root / str(filename),
                        mode=stat.S_IMODE(src.stat().st_mode),
                        category="provider:codex:agent",
                    )
                )

    optionals = manifest.get("optional_templates") or {}
    if with_settings:
        specs.append(_optional_spec(home, source_root, optionals.get("claude_settings") or {}, "optional:claude-settings"))
    if with_local_settings:
        specs.append(_optional_spec(home, source_root, optionals.get("claude_local_settings") or {}, "optional:claude-local-settings"))
    if with_hook:
        specs.append(_optional_spec(home, source_root, optionals.get("claude_hook") or {}, "optional:claude-hook"))
    return specs


def _optional_spec(home: Path, source_root: Path, item: dict[str, Any], category: str) -> CopySpec:
    if not item.get("source") or not item.get("destination"):
        raise BootstrapError(f"invalid optional bootstrap item: {category}")
    src = _source(source_root, str(item["source"]))
    return CopySpec(
        source=src,
        destination=_destination(home, str(item["destination"])),
        mode=int(str(item["mode"]), 8) if item.get("mode") else stat.S_IMODE(src.stat().st_mode),
        category=category,
    )


def _venv_python(home: Path) -> Path:
    return _destination(home, Path(".agentit") / "venv" / "bin" / "python")


def _cli_spec(home: Path) -> CopySpec:
    runtime_agentit = _destination(home, Path(".agentit") / "runtime" / "agentit")
    python = _venv_python(home)
    script = (
        "#!/usr/bin/env python3\n"
        "import os\nimport sys\n"
        f"PYTHON = {str(python)!r}\nAGENTIT = {str(runtime_agentit)!r}\n"
        "os.execv(PYTHON, [PYTHON, AGENTIT, *sys.argv[1:]])\n"
    ).encode("utf-8")
    return CopySpec(
        content=script,
        destination=_destination(home, Path(".local") / "bin" / "agentit"),
        mode=0o755,
        category="cli",
    )


def _dedupe_specs(specs: list[CopySpec]) -> list[CopySpec]:
    by_destination: dict[Path, CopySpec] = {}
    for spec in specs:
        previous = by_destination.get(spec.destination)
        if previous is not None:
            if previous.payload() != spec.payload() or previous.mode != spec.mode:
                raise BootstrapError(f"conflicting bootstrap ownership: {spec.destination}")
            continue
        by_destination[spec.destination] = spec
    return list(by_destination.values())


def build_install_plan(
    *,
    home: Path,
    source_root: Path = SOURCE_ROOT,
    provider: str = "all",
    with_settings: bool = False,
    with_local_settings: bool = False,
    with_hook: bool = False,
) -> dict[str, Any]:
    home = _safe_home(home)
    source_root = source_root.absolute()
    _assert_no_symlink_components(source_root)
    manifest = _load_manifest(source_root)
    available = list((manifest.get("providers") or {}).keys())
    providers = available if provider == "all" else [provider]
    unknown = [item for item in providers if item not in available]
    if unknown:
        raise BootstrapError(f"unknown provider(s): {unknown}; valid: {available + ['all']}")
    if (with_settings or with_local_settings or with_hook) and "claude" not in providers:
        raise BootstrapError("Claude optional settings/hook require provider claude or all")

    specs = _runtime_specs(home=home, source_root=source_root, manifest=manifest)
    specs.extend(
        _provider_specs(
            home=home,
            source_root=source_root,
            manifest=manifest,
            providers=providers,
            with_settings=with_settings,
            with_local_settings=with_local_settings,
            with_hook=with_hook,
        )
    )
    specs.append(_cli_spec(home))
    specs = _dedupe_specs(specs)

    try:
        hygiene = plan_host_skill_hygiene(
            home=home, source_root=source_root, manifest=manifest, providers=providers
        )
    except HostSkillHygieneError as exc:
        raise BootstrapError(str(exc)) from exc

    operations: list[dict[str, Any]] = list(hygiene)
    for spec in specs:
        _assert_no_symlink_components(spec.destination, stop=home)
        desired_hash = _sha256_bytes(spec.payload())
        if spec.destination.exists():
            if not spec.destination.is_file() or spec.destination.is_symlink():
                raise BootstrapError(f"existing destination is not a regular file: {spec.destination}")
            action = "keep" if _sha256_file(spec.destination) == desired_hash else "replace-with-backup"
        else:
            action = "install"
        operations.append(
            {
                "action": action,
                "category": spec.category,
                "destination": str(spec.destination),
                "source": str(spec.source) if spec.source else "generated:cli",
                "sha256": desired_hash,
                "mode": oct(spec.mode) if spec.mode is not None else None,
            }
        )

    return {
        "schema_version": 1,
        "mode": "plan",
        "home": str(home),
        "source_root": str(source_root),
        "providers": providers,
        "python_dependencies": list(manifest.get("python_dependencies") or []),
        "venv": str(_destination(home, Path(".agentit") / "venv")),
        "runtime_root": str(_destination(home, Path(".agentit") / "runtime")),
        "cli_path": str(_destination(home, Path(".local") / "bin" / "agentit")),
        "operations": operations,
        "_specs": specs,
        "_hygiene": hygiene,
    }


def _ensure_parent(destination: Path, *, home: Path) -> None:
    _assert_no_symlink_components(destination.parent, stop=home)
    destination.parent.mkdir(parents=True, exist_ok=True)
    _assert_no_symlink_components(destination.parent, stop=home)


def _atomic_write(destination: Path, data: bytes, *, mode: int, home: Path) -> None:
    _ensure_parent(destination, home=home)
    fd, tmp_name = tempfile.mkstemp(prefix=".agentit-copy-", dir=str(destination.parent))
    tmp = Path(tmp_name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(tmp, mode)
        os.replace(tmp, destination)
        os.chmod(destination, mode)
    finally:
        tmp.unlink(missing_ok=True)


def _install_dependencies(*, home: Path, dependencies: list[str], skip_dependencies: bool) -> Path:
    venv_root = _destination(home, Path(".agentit") / "venv")
    if venv_root.exists() and venv_root.is_symlink():
        raise BootstrapError(f"venv root symlink rejected: {venv_root}")
    python = _venv_python(home)
    if not python.is_file():
        _ensure_parent(venv_root / "placeholder", home=home)
        venv.EnvBuilder(with_pip=True, symlinks=False).create(venv_root)
    if not python.is_file():
        raise BootstrapError(f"venv python was not created: {python}")
    if dependencies and not skip_dependencies:
        completed = subprocess.run(
            [str(python), "-m", "pip", "install", "--disable-pip-version-check", *dependencies],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        if completed.returncode != 0:
            raise BootstrapError("failed to install Agentit Python dependencies:\n" + completed.stdout[-4000:])
    return python


def apply_install_plan(
    plan: dict[str, Any], *, backup_dir: Path | None = None, skip_dependencies: bool = False
) -> dict[str, Any]:
    home = _safe_home(Path(plan["home"]))
    specs = plan.get("_specs")
    hygiene = plan.get("_hygiene")
    if not isinstance(specs, list) or not all(isinstance(item, CopySpec) for item in specs):
        raise BootstrapError("install plan does not contain validated copy specs")
    if not isinstance(hygiene, list):
        raise BootstrapError("install plan does not contain validated hygiene operations")

    _install_dependencies(
        home=home,
        dependencies=[str(item) for item in plan.get("python_dependencies") or []],
        skip_dependencies=skip_dependencies,
    )

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_root = (
        backup_dir.expanduser().absolute()
        if backup_dir is not None
        else _destination(home, Path(".agentit") / "backups" / f"install-{stamp}")
    )
    if backup_root.exists() or backup_root.is_symlink():
        raise BootstrapError(f"backup directory must be new: {backup_root}")
    _assert_no_symlink_components(backup_root, stop=home if backup_root.is_relative_to(home) else None)
    backup_root.mkdir(parents=True, mode=0o700)
    os.chmod(backup_root, 0o700)

    records: list[dict[str, Any]] = []
    try:
        records.extend(apply_host_skill_hygiene(hygiene, home=home, backup_root=backup_root))
    except HostSkillHygieneError as exc:
        raise BootstrapError(str(exc)) from exc

    for spec in specs:
        desired = spec.payload()
        desired_hash = _sha256_bytes(desired)
        destination = spec.destination
        _assert_no_symlink_components(destination, stop=home)
        if destination.exists():
            if not destination.is_file() or destination.is_symlink():
                raise BootstrapError(f"destination changed to unsafe type: {destination}")
            current_hash = _sha256_file(destination)
            if current_hash == desired_hash:
                continue
            before_state = "present"
            original_mode = stat.S_IMODE(destination.stat().st_mode)
            rel = destination.relative_to(home)
            backup_path = backup_root / "files" / rel
            _atomic_write(backup_path, destination.read_bytes(), mode=0o600, home=backup_root)
            backup_hash = _sha256_file(backup_path)
            original_hash = current_hash
        else:
            before_state = "absent"
            original_mode = None
            backup_path = None
            backup_hash = None
            original_hash = None

        mode = spec.mode if spec.mode is not None else 0o644
        _atomic_write(destination, desired, mode=mode, home=home)
        installed_hash = _sha256_file(destination)
        if installed_hash != desired_hash:
            raise BootstrapError(f"post-copy hash mismatch: {destination}")
        records.append(
            {
                "kind": "file",
                "category": spec.category,
                "destination": str(destination),
                "before_state": before_state,
                "original_mode": original_mode,
                "original_sha256": original_hash,
                "backup_path": str(backup_path) if backup_path else None,
                "backup_sha256": backup_hash,
                "installed_mode": mode,
                "installed_sha256": installed_hash,
            }
        )

    manifest_path = backup_root / "manifest.json"
    receipt = {
        "schema_version": 1,
        "kind": "agentit.bootstrap.receipt",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "home": str(home),
        "source_root": plan["source_root"],
        "providers": plan["providers"],
        "runtime_root": plan["runtime_root"],
        "cli_path": plan["cli_path"],
        "records": records,
    }
    _atomic_write(
        manifest_path,
        (json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8"),
        mode=0o600,
        home=backup_root,
    )
    return {
        "status": "applied",
        "providers": plan["providers"],
        "runtime_root": plan["runtime_root"],
        "cli_path": plan["cli_path"],
        "backup_manifest": str(manifest_path),
        "changed_files": len(records),
        "path_note": "The coding agent may call cli_path directly. ~/.local/bin need not be on the human user's PATH.",
    }


def load_rollback_manifest(path: Path) -> dict[str, Any]:
    if not path.is_file() or path.is_symlink():
        raise BootstrapError(f"rollback manifest must be a regular file: {path}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise BootstrapError(f"invalid rollback manifest: {exc}") from exc
    if payload.get("kind") != "agentit.bootstrap.receipt" or payload.get("schema_version") != 1:
        raise BootstrapError("not an Agentit bootstrap receipt")
    return payload


def rollback_plan(manifest_path: Path) -> dict[str, Any]:
    receipt = load_rollback_manifest(manifest_path)
    home = _safe_home(Path(receipt["home"]))
    operations: list[dict[str, Any]] = []
    for record in reversed(receipt.get("records") or []):
        if record.get("kind") == "removed_skill_tree":
            try:
                destination, backup = validate_removed_tree_record(record, home=home)
            except HostSkillHygieneError as exc:
                raise BootstrapError(str(exc)) from exc
            operations.append(
                {"action": "restore-tree", "destination": str(destination), "backup": str(backup)}
            )
            continue

        destination = Path(record["destination"])
        try:
            destination.relative_to(home)
        except ValueError as exc:
            raise BootstrapError(f"rollback destination escapes recorded home: {destination}") from exc
        _assert_no_symlink_components(destination, stop=home)
        if not destination.is_file() or destination.is_symlink():
            raise BootstrapError(f"rollback destination missing/unsafe: {destination}")
        if _sha256_file(destination) != record.get("installed_sha256"):
            raise BootstrapError(f"refusing rollback because destination changed after install: {destination}")
        if record.get("before_state") == "present":
            backup = Path(str(record.get("backup_path")))
            if not backup.is_file() or backup.is_symlink() or _sha256_file(backup) != record.get("backup_sha256"):
                raise BootstrapError(f"rollback backup missing or changed: {backup}")
            action = "restore"
        elif record.get("before_state") == "absent":
            backup = None
            action = "remove"
        else:
            raise BootstrapError(f"invalid before_state for {destination}")
        operations.append({"action": action, "destination": str(destination), "backup": str(backup) if backup else None})
    return {"status": "plan", "manifest": str(manifest_path), "home": str(home), "operations": operations}


def apply_rollback(manifest_path: Path) -> dict[str, Any]:
    plan = rollback_plan(manifest_path)
    receipt = load_rollback_manifest(manifest_path)
    home = _safe_home(Path(plan["home"]))
    record_by_destination = {str(record["destination"]): record for record in receipt.get("records") or []}
    changed = 0
    for operation in plan["operations"]:
        destination = Path(operation["destination"])
        record = record_by_destination[str(destination)]
        if operation["action"] == "restore-tree":
            try:
                restore_removed_tree(record, home=home)
            except HostSkillHygieneError as exc:
                raise BootstrapError(str(exc)) from exc
        elif operation["action"] == "restore":
            backup = Path(str(operation["backup"]))
            _atomic_write(destination, backup.read_bytes(), mode=int(record["original_mode"]), home=home)
            if _sha256_file(destination) != record.get("original_sha256"):
                raise BootstrapError(f"restored destination hash mismatch: {destination}")
        else:
            destination.unlink()
        changed += 1
    return {
        "status": "rolled-back",
        "manifest": str(manifest_path),
        "changed_files": changed,
        "note": "Private Agentit runtime/venv directories are intentionally not recursively deleted.",
    }


def _public_plan(plan: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in plan.items() if not key.startswith("_")}


def _parser() -> argparse.ArgumentParser:
    manifest = _load_manifest(SOURCE_ROOT)
    providers = tuple((manifest.get("providers") or {}).keys())
    parser = argparse.ArgumentParser(
        prog="agentit bootstrap",
        description="Plan/apply Agentit's portable core-only provider bootstrap.",
    )
    parser.add_argument("--provider", choices=("all", *providers), default="all")
    parser.add_argument("--home", type=Path, default=Path.home())
    parser.add_argument("--source-root", type=Path, default=SOURCE_ROOT)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--backup-dir", type=Path)
    parser.add_argument("--with-settings", action="store_true", help="Opt-in Claude settings.json replacement.")
    parser.add_argument("--with-local-settings", action="store_true", help="Opt-in machine-local Claude settings template.")
    parser.add_argument("--with-hook", action="store_true")
    parser.add_argument("--skip-dependencies", action="store_true", help="Testing/offline only.")
    parser.add_argument("--rollback", type=Path, help="Plan rollback for a prior bootstrap receipt.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    try:
        if args.rollback is not None:
            payload = apply_rollback(args.rollback) if args.apply else rollback_plan(args.rollback)
        else:
            plan = build_install_plan(
                home=args.home,
                source_root=args.source_root,
                provider=args.provider,
                with_settings=args.with_settings,
                with_local_settings=args.with_local_settings,
                with_hook=args.with_hook,
            )
            payload = (
                apply_install_plan(plan, backup_dir=args.backup_dir, skip_dependencies=args.skip_dependencies)
                if args.apply
                else _public_plan(plan)
            )
    except (BootstrapError, HostSkillHygieneError, OSError) as exc:
        parser.error(str(exc))
        return 2
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
