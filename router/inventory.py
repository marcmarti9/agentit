"""Generate an ignored, machine-local inventory from the portable catalog.

This module performs only mechanical catalog/path inspection. It does not infer
user intent, task risk, topology, skill relevance, or any other semantic route.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


DEFAULT_REGISTRY_PATH = Path(__file__).resolve().parents[1] / "registry.yaml"
DEFAULT_OUTPUT_PATH = DEFAULT_REGISTRY_PATH.parent / "reports" / "local" / "inventory.yaml"
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


class InventoryError(RuntimeError):
    """Raised when the portable inventory cannot be inspected safely."""


def _load_catalog(path: Path) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise InventoryError(f"cannot read registry {path}: {exc}") from exc
    except yaml.YAMLError as exc:
        raise InventoryError(f"invalid YAML in registry {path}: {exc}") from exc

    if not isinstance(raw, dict) or raw.get("schema_version") != 1:
        raise InventoryError("registry must use schema_version: 1")
    entries = raw.get("entries")
    if not isinstance(entries, list):
        raise InventoryError("registry entries must be a list")

    indexed: dict[str, dict[str, Any]] = {}
    for position, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise InventoryError(f"registry entry {position} must be a mapping")
        item_id = entry.get("id")
        paths = entry.get("paths")
        state = entry.get("state")
        if not isinstance(item_id, str) or not item_id:
            raise InventoryError(f"registry entry {position} has an invalid id")
        if item_id in indexed:
            raise InventoryError(f"duplicate registry id: {item_id}")
        if state not in KNOWN_REGISTRY_STATES:
            raise InventoryError(f"unknown registry state for {item_id}: {state!r}")
        if not isinstance(paths, list) or not all(isinstance(value, str) for value in paths):
            raise InventoryError(f"registry paths for {item_id} must be a string list")
        indexed[item_id] = entry
    return raw, indexed


def _resolve_catalog_path(template: str, *, registry_path: Path, home: Path) -> Path:
    repo_root = registry_path.resolve().parent
    if template == "${HOME}":
        root, relative = home.resolve(), ""
    elif template.startswith("${HOME}/"):
        root, relative = home.resolve(), template.removeprefix("${HOME}/")
    elif template == "${REPO_ROOT}":
        root, relative = repo_root, ""
    elif template.startswith("${REPO_ROOT}/"):
        root, relative = repo_root, template.removeprefix("${REPO_ROOT}/")
    else:
        raise InventoryError(
            f"catalog path must use ${{HOME}} or ${{REPO_ROOT}}: {template}"
        )
    if ".." in Path(relative).parts:
        raise InventoryError(f"catalog path escapes portable root: {template}")
    candidate = root / relative
    if not candidate.resolve(strict=False).is_relative_to(root):
        raise InventoryError(f"catalog path escapes resolved root: {template}")
    return candidate


def _file_digest(path: Path) -> str | None:
    if not path.is_file() or path.is_symlink():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_inventory(registry_path: Path, home: Path) -> dict[str, Any]:
    raw, entries = _load_catalog(registry_path)
    providers = []
    for provider in raw.get("providers", []):
        if not isinstance(provider, dict):
            raise InventoryError("provider entries must be mappings")
        names = provider.get("executable_names", [])
        if not isinstance(names, list) or not all(isinstance(name, str) for name in names):
            raise InventoryError("provider executable_names must be a string list")
        target_roots = provider.get("target_roots", [])
        if not isinstance(target_roots, list) or not all(
            isinstance(template, str) for template in target_roots
        ):
            raise InventoryError("provider target_roots must be a string list")
        providers.append(
            {
                "id": provider.get("id"),
                "executables": [
                    {"name": name, "path": shutil.which(name), "version": None}
                    for name in names
                ],
                "target_roots": [
                    str(
                        _resolve_catalog_path(
                            template,
                            registry_path=registry_path,
                            home=home,
                        )
                    )
                    for template in target_roots
                ],
            }
        )

    observed_entries: dict[str, Any] = {}
    for item_id, entry in entries.items():
        observations = []
        for template in entry["paths"]:
            path = _resolve_catalog_path(
                template,
                registry_path=registry_path,
                home=home,
            )
            observation = {
                "path": str(path),
                "exists": path.exists(),
                "kind": "directory" if path.is_dir() else "file" if path.is_file() else None,
            }
            digest = _file_digest(path)
            if digest is not None:
                observation["sha256"] = digest
            observations.append(observation)
        observed_entries[item_id] = {
            "catalog_state": entry["state"],
            "paths": observations,
        }

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "catalog": str(registry_path.resolve()),
        "home": str(home.resolve()),
        "providers": providers,
        "entries": observed_entries,
    }


def write_inventory(output: Path, inventory: dict[str, Any]) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=output.parent,
            prefix=f".{output.name}.tmp-",
            delete=False,
        ) as handle:
            temporary = Path(handle.name)
            yaml.safe_dump(
                inventory,
                handle,
                sort_keys=False,
                allow_unicode=True,
            )
        temporary.chmod(0o600)
        os.replace(temporary, output)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY_PATH)
    parser.add_argument("--home", type=Path, default=Path.home())
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    args = parser.parse_args()
    try:
        inventory = build_inventory(args.registry, args.home)
        write_inventory(args.output, inventory)
    except (InventoryError, OSError, yaml.YAMLError) as exc:
        parser.error(str(exc))
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
