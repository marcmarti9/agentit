"""Regression tests for first-party MCP catalog overlays."""

from __future__ import annotations

import unittest
from pathlib import Path

import yaml

from router.mcp_catalog import (
    McpCatalogError,
    get_server,
    list_stacks,
    load_catalog,
    snippet_for_server,
    _merge_overlay,
)


class McpCatalogOverlayTests(unittest.TestCase):
    def test_21st_overlay_is_loaded_into_frontend_and_design_studio(self) -> None:
        catalog = load_catalog()
        server = get_server("21st", catalog)
        self.assertEqual(server["remote_url"], "https://21st.dev/api/mcp")
        self.assertEqual(server["secret_env"], "API_KEY_21ST")
        stacks = list_stacks(catalog)
        self.assertIn("21st", stacks["frontend"]["servers"])
        self.assertIn("21st", stacks["design_studio"]["servers"])

    def test_21st_generic_snippet_never_embeds_secret(self) -> None:
        snippet = snippet_for_server("21st", provider="json")
        rendered = snippet["snippet"]
        self.assertIn("https://21st.dev/api/mcp", rendered)
        self.assertNotIn("21st_sk_", rendered)
        self.assertTrue(snippet["requires_secret"])

    def test_overlay_rejects_duplicate_server_ids(self) -> None:
        catalog = load_catalog(Path(__file__).resolve().parents[1] / "mcp" / "catalog.yaml")
        overlay = {
            "schema_version": 1,
            "servers": [{"id": "context7"}],
        }
        with self.assertRaises(McpCatalogError):
            _merge_overlay(catalog, overlay, source=Path("duplicate.yaml"))

    def test_overlay_rejects_unknown_stack(self) -> None:
        catalog = load_catalog(Path(__file__).resolve().parents[1] / "mcp" / "catalog.yaml")
        overlay = {
            "schema_version": 1,
            "servers": [{"id": "new-server"}],
            "stacks": {"missing": {"append_servers": ["new-server"]}},
        }
        with self.assertRaises(McpCatalogError):
            _merge_overlay(catalog, overlay, source=Path("unknown-stack.yaml"))

    def test_overlay_file_is_plain_yaml(self) -> None:
        root = Path(__file__).resolve().parents[1]
        data = yaml.safe_load((root / "mcp" / "catalog.d" / "21st.yaml").read_text(encoding="utf-8"))
        self.assertEqual(data["schema_version"], 1)


if __name__ == "__main__":
    unittest.main()
