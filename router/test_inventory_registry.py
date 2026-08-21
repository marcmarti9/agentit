"""Mechanical registry/inventory safety tests.

These tests intentionally avoid task-language classification. They preserve the
portable catalog invariants that still matter after removing the semantic router.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import yaml

from router.inventory import (
    DEFAULT_REGISTRY_PATH,
    InventoryError,
    _load_catalog,
    _resolve_catalog_path,
    build_inventory,
)


class InventoryRegistryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)
        self.home = self.root / "home"
        self.home.mkdir()
        self.registry = self.root / "registry.yaml"

    def tearDown(self) -> None:
        self.tmpdir.cleanup()

    def write_registry(self, *, entries=None, providers=None) -> None:
        payload = {
            "schema_version": 1,
            "entries": entries if entries is not None else [],
        }
        if providers is not None:
            payload["providers"] = providers
        self.registry.write_text(
            yaml.safe_dump(payload, sort_keys=False),
            encoding="utf-8",
        )

    @staticmethod
    def entry(
        item_id: str = "example",
        *,
        state: str = "ACTIVE_GLOBAL",
        paths: list[str] | None = None,
    ) -> dict[str, object]:
        return {
            "id": item_id,
            "state": state,
            "paths": paths if paths is not None else ["${HOME}/skills/example"],
        }

    def test_checked_in_registry_builds_mechanical_inventory(self) -> None:
        inventory = build_inventory(DEFAULT_REGISTRY_PATH, self.home)
        self.assertTrue(inventory["entries"])
        self.assertEqual(str(DEFAULT_REGISTRY_PATH.resolve()), inventory["catalog"])

    def test_duplicate_ids_are_rejected(self) -> None:
        self.write_registry(entries=[self.entry(), self.entry()])
        with self.assertRaisesRegex(InventoryError, "duplicate registry id"):
            _load_catalog(self.registry)

    def test_unknown_state_is_rejected(self) -> None:
        self.write_registry(entries=[self.entry(state="READY_WHENEVER")])
        with self.assertRaisesRegex(InventoryError, "unknown registry state"):
            _load_catalog(self.registry)

    def test_missing_and_malformed_registry_are_rejected(self) -> None:
        with self.assertRaisesRegex(InventoryError, "cannot read registry"):
            _load_catalog(self.root / "missing.yaml")

        self.registry.write_text("entries: [unterminated", encoding="utf-8")
        with self.assertRaisesRegex(InventoryError, "invalid YAML"):
            _load_catalog(self.registry)

    def test_registry_requires_schema_and_entry_list(self) -> None:
        self.registry.write_text("schema_version: 2\nentries: []\n", encoding="utf-8")
        with self.assertRaisesRegex(InventoryError, "schema_version: 1"):
            _load_catalog(self.registry)

        self.registry.write_text("schema_version: 1\nentries: nope\n", encoding="utf-8")
        with self.assertRaisesRegex(InventoryError, "entries must be a list"):
            _load_catalog(self.registry)

    def test_catalog_paths_must_use_portable_roots(self) -> None:
        with self.assertRaisesRegex(InventoryError, "must use"):
            _resolve_catalog_path(
                "/tmp/skill",
                registry_path=self.registry,
                home=self.home,
            )

        with self.assertRaisesRegex(InventoryError, "escapes portable root"):
            _resolve_catalog_path(
                "${HOME}/../other-user/skill",
                registry_path=self.registry,
                home=self.home,
            )

    def test_symlink_escape_is_rejected(self) -> None:
        outside = self.root / "outside"
        outside.mkdir()
        (self.home / "linked").symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(InventoryError, "escapes resolved root"):
            _resolve_catalog_path(
                "${HOME}/linked/skill",
                registry_path=self.registry,
                home=self.home,
            )

    def test_provider_shapes_are_validated(self) -> None:
        self.write_registry(
            entries=[self.entry()],
            providers=[{"id": "broken", "executable_names": "python3"}],
        )
        with self.assertRaisesRegex(InventoryError, "executable_names"):
            build_inventory(self.registry, self.home)

        self.write_registry(
            entries=[self.entry()],
            providers=[
                {
                    "id": "broken",
                    "executable_names": [],
                    "target_roots": "${HOME}/skills",
                }
            ],
        )
        with self.assertRaisesRegex(InventoryError, "target_roots"):
            build_inventory(self.registry, self.home)


if __name__ == "__main__":
    unittest.main()
