"""Tests for the provenance-aware reference catalog."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml

from router.reference_catalog import (
    ReferenceCatalogError,
    catalog_summary,
    get_pack,
    get_source,
    list_sources,
    load_catalog,
    validate_catalog,
)


ROOT = Path(__file__).resolve().parents[1]
AGENTIT_CLI = ROOT / "agentit"


class ReferenceCatalogTests(unittest.TestCase):
    def test_catalog_contains_original_bookmark_batch(self) -> None:
        catalog = load_catalog()
        summary = catalog_summary(catalog)
        self.assertEqual(summary["source_count"], 27)
        self.assertGreaterEqual(summary["pack_count"], 7)
        self.assertEqual(catalog["policy"]["semantic_selection_owner"], "primary_ai")
        self.assertEqual(catalog["policy"]["software_role"], "mechanical_index_only")

    def test_pack_resolves_only_explicit_ids(self) -> None:
        pack = get_pack("web-design-studio")
        ids = {source["id"] for source in pack["sources"]}
        self.assertIn("ericksky-hallmark", ids)
        self.assertIn("monokern-21st-dev", ids)
        with self.assertRaises(ReferenceCatalogError):
            get_pack("build me a premium landing page")

    def test_sources_can_be_filtered_mechanically(self) -> None:
        design = list_sources(domain="design")
        self.assertTrue(design)
        self.assertTrue(all("design" in row["domains"] for row in design))
        canonical = list_sources(evidence_level="canonical")
        self.assertTrue(any(row["id"] == "monokern-21st-dev" for row in canonical))

    def test_unknown_source_rejected(self) -> None:
        with self.assertRaises(ReferenceCatalogError):
            get_source("not-a-real-reference")

    def test_duplicate_source_rejected(self) -> None:
        catalog = load_catalog()
        duplicate = dict(catalog["sources"][0])
        catalog["sources"] = [*catalog["sources"], duplicate]
        with self.assertRaises(ReferenceCatalogError):
            validate_catalog(catalog)

    def test_pack_with_unknown_source_rejected(self) -> None:
        catalog = load_catalog()
        catalog["packs"]["broken"] = {"description": "broken", "sources": ["missing-source"]}
        with self.assertRaises(ReferenceCatalogError):
            validate_catalog(catalog)

    def test_invalid_policy_rejected(self) -> None:
        catalog = load_catalog()
        catalog["policy"]["semantic_selection_owner"] = "python-router"
        with self.assertRaises(ReferenceCatalogError):
            validate_catalog(catalog)

    def test_symlink_catalog_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            original = root / "catalog.yaml"
            original.write_text("schema_version: 1\n", encoding="utf-8")
            symlink = root / "linked.yaml"
            try:
                symlink.symlink_to(original)
            except (OSError, NotImplementedError):
                self.skipTest("symlinks unavailable")
            with self.assertRaises(ReferenceCatalogError):
                load_catalog(symlink)

    def test_cli_summary_and_pack(self) -> None:
        summary = subprocess.run(
            [str(AGENTIT_CLI), "refs", "summary", "--format", "json"],
            capture_output=True,
            text=True,
            check=True,
            cwd=str(ROOT),
        )
        payload = json.loads(summary.stdout)
        self.assertEqual(payload["source_count"], 27)

        pack = subprocess.run(
            [str(AGENTIT_CLI), "refs", "pack", "engineering-discipline", "--format", "json"],
            capture_output=True,
            text=True,
            check=True,
            cwd=str(ROOT),
        )
        pack_payload = json.loads(pack.stdout)
        self.assertEqual(pack_payload["id"], "engineering-discipline")

    def test_catalog_yaml_is_plain_data(self) -> None:
        data = yaml.safe_load((ROOT / "references" / "catalog.yaml").read_text(encoding="utf-8"))
        self.assertIsInstance(data, dict)
        self.assertIn("sources", data)


if __name__ == "__main__":
    unittest.main()
