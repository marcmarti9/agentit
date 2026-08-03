"""Generate an ignored, machine-local inventory from the portable catalog."""

from __future__ import annotations

import argparse
import hashlib
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

try:
    from .route import DEFAULT_REGISTRY_PATH, RegistryError, load_registry, resolve_registry_path
except ImportError:  # direct execution from router/
    from route import DEFAULT_REGISTRY_PATH, RegistryError, load_registry, resolve_registry_path


DEFAULT_OUTPUT_PATH = DEFAULT_REGISTRY_PATH.parent / "reports" / "local" / "inventory.yaml"


def _file_digest(path: Path) -> str | None:
    if not path.is_file() or path.is_symlink():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_inventory(registry_path: Path, home: Path) -> dict[str, Any]:
    entries = load_registry(registry_path)
    raw = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
    providers = []
    for provider in raw.get("providers", []):
        names = provider.get("executable_names", [])
        if not isinstance(names, list) or not all(isinstance(name, str) for name in names):
            raise RegistryError("provider executable_names must be a string list")
        providers.append(
            {
                "id": provider.get("id"),
                "executables": [
                    {"name": name, "path": shutil.which(name), "version": None}
                    for name in names
                ],
                "target_roots": [
                    str(
                        resolve_registry_path(
                            template, registry_path=registry_path, home=home
                        )
                    )
                    for template in provider.get("target_roots", [])
                ],
            }
        )

    observed_entries: dict[str, Any] = {}
    for skill_id, entry in entries.items():
        observations = []
        for template in entry["paths"]:
            path = resolve_registry_path(
                template, registry_path=registry_path, home=home
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
        observed_entries[skill_id] = {
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
    temporary = output.with_name(f".{output.name}.tmp-{os.getpid()}")
    try:
        temporary.write_text(
            yaml.safe_dump(inventory, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )
        temporary.chmod(0o600)
        os.replace(temporary, output)
    finally:
        if temporary.exists():
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
    except (RegistryError, OSError, yaml.YAMLError) as exc:
        parser.error(str(exc))
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
