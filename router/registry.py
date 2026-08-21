"""Deterministic registry validation and skill availability.

This module deliberately does not interpret user language. The host model decides
which skills are relevant; this code only verifies that requested skill IDs are
known, in an available registry state, have loadable paths, satisfy explicit
signal requirements, and have their essential dependencies available.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

try:
    import yaml
except ImportError:  # pragma: no cover - CI installs PyYAML
    yaml = None


DEFAULT_REGISTRY_PATH = Path(__file__).resolve().parents[1] / "registry.yaml"
KNOWN_REGISTRY_STATES = {
    "ACTIVE_GLOBAL",
    "DUPLICATED",
    "AVAILABLE_ON_DEMAND",
    "NOT_INSTALLED",
    "DISABLED",
    "ARCHIVED",
    "BROKEN",
    "SECURITY_REVIEW_REQUIRED",
    "UNKNOWN",
}
AVAILABLE_REGISTRY_STATES = {"ACTIVE_GLOBAL", "DUPLICATED"}


class RegistryError(RuntimeError):
    """Raised when registry metadata is unavailable, malformed, or unsafe."""


def load_registry(registry_path: Path | None = None) -> dict[str, dict[str, Any]]:
    """Load and validate registry.yaml, indexed by unique entry ID."""
    path = Path(registry_path) if registry_path is not None else DEFAULT_REGISTRY_PATH
    if yaml is None:
        raise RegistryError("PyYAML is required to load registry.yaml")
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise RegistryError(f"cannot read registry {path}: {exc}") from exc
    except yaml.YAMLError as exc:
        raise RegistryError(f"invalid YAML in registry {path}: {exc}") from exc

    if not isinstance(raw, dict) or raw.get("schema_version") != 1:
        raise RegistryError("registry root must be a mapping with schema_version: 1")
    entries = raw.get("entries")
    if not isinstance(entries, list):
        raise RegistryError("registry entries must be a list")

    indexed: dict[str, dict[str, Any]] = {}
    for position, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise RegistryError(f"registry entry {position} must be a mapping")
        entry_id = entry.get("id")
        state = entry.get("state")
        paths = entry.get("paths")
        dependencies = entry.get("essential_dependencies", [])
        required_signals = entry.get("requires_signals_any", [])
        conflicts_with = entry.get("conflicts_with", [])

        if not isinstance(entry_id, str) or not entry_id.strip():
            raise RegistryError(f"registry entry {position} has an invalid id")
        if entry_id in indexed:
            raise RegistryError(f"duplicate registry id: {entry_id}")
        if state not in KNOWN_REGISTRY_STATES:
            raise RegistryError(f"unknown registry state for {entry_id}: {state!r}")
        if not isinstance(paths, list) or not all(isinstance(item, str) for item in paths):
            raise RegistryError(f"registry paths for {entry_id} must be a string list")
        for template in paths:
            if not (
                template == "${HOME}"
                or template.startswith("${HOME}/")
                or template == "${REPO_ROOT}"
                or template.startswith("${REPO_ROOT}/")
            ):
                raise RegistryError(
                    f"registry path for {entry_id} must use ${{HOME}} or ${{REPO_ROOT}}: {template}"
                )
            suffix = template.split("/", 1)[1] if "/" in template else ""
            if ".." in Path(suffix).parts:
                raise RegistryError(f"registry path for {entry_id} escapes its root: {template}")
        if not isinstance(dependencies, list) or not all(
            isinstance(item, str) and item for item in dependencies
        ):
            raise RegistryError(f"essential_dependencies for {entry_id} must be an ID list")
        if not isinstance(required_signals, list) or not all(
            isinstance(item, str) and item for item in required_signals
        ):
            raise RegistryError(f"requires_signals_any for {entry_id} must be a string list")
        if not isinstance(conflicts_with, list) or not all(
            isinstance(item, str) and item for item in conflicts_with
        ):
            raise RegistryError(f"conflicts_with for {entry_id} must be an ID list")
        for field in ("priority", "context_cost", "execution_cost", "trigger", "avoid_when"):
            value = entry.get(field)
            if value is not None and (not isinstance(value, str) or not value.strip()):
                raise RegistryError(f"{field} for {entry_id} must be a non-empty string")
        conflicts = entry.get("conflicts", [])
        if not isinstance(conflicts, list) or not all(isinstance(item, str) for item in conflicts):
            raise RegistryError(f"conflicts for {entry_id} must be a string list")

        normalized = dict(entry)
        normalized["essential_dependencies"] = list(dependencies)
        normalized["requires_signals_any"] = list(required_signals)
        normalized["conflicts_with"] = list(conflicts_with)
        indexed[entry_id] = normalized

    for entry_id, entry in indexed.items():
        for reference in entry["essential_dependencies"] + entry["conflicts_with"]:
            if reference not in indexed:
                raise RegistryError(f"registry reference for {entry_id} is absent: {reference}")
    return indexed


def resolve_registry_path(template: str, *, registry_path: Path, home: Path) -> Path:
    """Resolve a validated portable template without generic env expansion."""
    repo_root = Path(registry_path).resolve().parent
    home_root = Path(home).resolve()
    if template == "${HOME}":
        root, relative = home_root, ""
    elif template.startswith("${HOME}/"):
        root, relative = home_root, template.removeprefix("${HOME}/")
    elif template == "${REPO_ROOT}":
        root, relative = repo_root, ""
    elif template.startswith("${REPO_ROOT}/"):
        root, relative = repo_root, template.removeprefix("${REPO_ROOT}/")
    else:
        raise RegistryError(f"unsupported registry path template: {template}")
    candidate = root / relative
    if not candidate.resolve(strict=False).is_relative_to(root):
        raise RegistryError(f"registry path escapes its resolved root: {template}")
    return candidate


def _path_is_loadable(entry: dict[str, Any], path: Path) -> bool:
    try:
        if path.is_symlink():
            return False
        kind = str(entry.get("kind", "skill"))
        if "skill" not in kind and kind not in {"plugin", "bundle"}:
            return path.is_file()
        skill_file = path if path.is_file() else path / "SKILL.md"
        return skill_file.is_file() and not skill_file.is_symlink()
    except OSError:
        return False


def _availability(
    entry_id: str,
    *,
    entries: dict[str, dict[str, Any]],
    registry_path: Path,
    home: Path,
    signals: set[str],
    visiting: tuple[str, ...] = (),
) -> tuple[bool, str]:
    if entry_id not in entries:
        return False, "unknown_registry_id"
    if entry_id in visiting:
        raise RegistryError(f"essential dependency cycle: {' -> '.join((*visiting, entry_id))}")

    entry = entries[entry_id]
    if entry.get("state") not in AVAILABLE_REGISTRY_STATES:
        return False, f"state={entry.get('state')}"

    required = {str(item).lower() for item in entry.get("requires_signals_any", [])}
    if required and not (required & signals):
        return False, "required_signal_missing"

    loadable = any(
        _path_is_loadable(
            entry,
            resolve_registry_path(template, registry_path=registry_path, home=home),
        )
        for template in entry.get("paths", [])
    )
    if not loadable:
        return False, "no_loadable_path"

    for dependency in entry.get("essential_dependencies", []):
        ok, reason = _availability(
            dependency,
            entries=entries,
            registry_path=registry_path,
            home=home,
            signals=signals,
            visiting=(*visiting, entry_id),
        )
        if not ok:
            return False, f"dependency:{dependency}:{reason}"
    return True, "available"


def resolve_requested_skills(
    skill_ids: Iterable[str],
    *,
    registry_path: Path | None = None,
    home: Path | None = None,
    signals: Iterable[str] = (),
) -> dict[str, Any]:
    """Verify model-selected skills without deciding which skills should be selected."""
    path = Path(registry_path) if registry_path is not None else DEFAULT_REGISTRY_PATH
    home_path = Path(home) if home is not None else Path.home()
    entries = load_registry(path)
    normalized_ids: list[str] = []
    for skill_id in skill_ids:
        if not isinstance(skill_id, str) or not skill_id.strip():
            raise RegistryError("requested skill IDs must be non-empty strings")
        if skill_id not in normalized_ids:
            normalized_ids.append(skill_id)

    signal_set = {str(item).strip().lower() for item in signals if str(item).strip()}
    available: list[str] = []
    missing: list[str] = []
    details: dict[str, dict[str, Any]] = {}
    for skill_id in normalized_ids:
        ok, reason = _availability(
            skill_id,
            entries=entries,
            registry_path=path,
            home=home_path,
            signals=signal_set,
        )
        details[skill_id] = {"available": ok, "reason": reason}
        (available if ok else missing).append(skill_id)

    return {
        "requested": normalized_ids,
        "available": available,
        "missing": missing,
        "details": details,
    }
