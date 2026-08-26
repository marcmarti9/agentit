"""Tests for curated MCP catalog (opt-in, no auto-activate)."""

from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

from router.mcp_catalog import (
    McpCatalogError,
    catalog_summary,
    get_server,
    list_servers,
    list_stacks,
    load_catalog,
    plan_stack,
    recommend_for_task,
    recommend_stack,
    snippet_for_server,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
AGENTIT_CLI = REPO_ROOT / "agentit"


class McpCatalogTestCase(unittest.TestCase):
    def test_load_and_list_core(self) -> None:
        catalog = load_catalog()
        self.assertFalse(catalog["policy"]["auto_activate"])
        rows = list_servers(catalog, tier="core")
        ids = {r["id"] for r in rows}
        self.assertTrue({"agentit-manager", "context7", "github", "playwright"}.issubset(ids))

    def test_recommend_developer_core(self) -> None:
        rec = recommend_stack("developer_core")
        self.assertEqual(rec["stack"], "developer_core")
        self.assertIn("opt-in", rec["activation"])
        ids = [s["id"] for s in rec["servers"]]
        self.assertEqual(ids, ["agentit-manager", "context7", "github", "playwright"])

    def test_mobile_design_stack_is_opt_in_remote_research(self) -> None:
        rec = recommend_stack("mobile_design")
        self.assertEqual(rec["stack"], "mobile_design")
        self.assertEqual([s["id"] for s in rec["servers"]], ["appllama", "context7"])

        server = get_server("appllama")
        self.assertEqual(server["risk"], "RISK_1")
        self.assertFalse(server["requires_secret"])
        self.assertFalse(server["write_capable"])

        snip = snippet_for_server("appllama", provider="json")
        self.assertEqual(
            snip["mcpServers"]["appllama"]["url"],
            "https://mcp.appllama.io/mcp",
        )
        self.assertFalse(snip["auto_activate"])

    def test_free_text_task_recommendation_is_rejected(self) -> None:
        with self.assertRaises(McpCatalogError):
            recommend_for_task("implement figma design in react")
        with self.assertRaises(McpCatalogError):
            recommend_for_task("inspect supabase schema")

    def test_snippet_context7_json(self) -> None:
        snip = snippet_for_server("context7", provider="json")
        self.assertIn("mcpServers", snip)
        self.assertIn("context7", snip["mcpServers"])
        self.assertFalse(snip["auto_activate"])

    def test_snippet_claude_text(self) -> None:
        snip = snippet_for_server("playwright", provider="claude")
        self.assertIn("claude mcp add", snip["command"])
        self.assertIn("playwright", snip["command"])

    def test_plan_merges_json(self) -> None:
        plan = plan_stack("developer_core", provider="json")
        self.assertIsNotNone(plan["mcpServers"])
        self.assertIn("agentit-manager", plan["mcpServers"])
        self.assertIn("context7", plan["mcpServers"])
        self.assertIn("github", plan["mcpServers"])
        self.assertIn("playwright", plan["mcpServers"])

    def test_unknown_server(self) -> None:
        with self.assertRaises(McpCatalogError):
            get_server("not-a-real-mcp")

    def test_max_risk_filter(self) -> None:
        rows = list_servers(max_risk="RISK_1")
        self.assertTrue(rows)
        self.assertTrue(all(r["risk"] == "RISK_1" for r in rows))

    def test_catalog_summary(self) -> None:
        summary = catalog_summary()
        self.assertGreaterEqual(summary["server_count"], 10)
        self.assertIn("developer_core", summary["stacks"])
        self.assertIn("mobile_design", summary["stacks"])
        self.assertGreaterEqual(len(list_stacks()), 5)

    def test_cli_list(self) -> None:
        proc = subprocess.run(
            [str(AGENTIT_CLI), "mcp", "list", "--format", "json"],
            capture_output=True,
            text=True,
            check=True,
            cwd=str(REPO_ROOT),
        )
        data = json.loads(proc.stdout)
        self.assertIn("servers", data)
        self.assertFalse(data["policy"]["auto_activate"])

    def test_cli_recommend_named_stack(self) -> None:
        proc = subprocess.run(
            [str(AGENTIT_CLI), "mcp", "recommend", "developer_core"],
            capture_output=True,
            text=True,
            check=True,
            cwd=str(REPO_ROOT),
        )
        data = json.loads(proc.stdout)
        self.assertEqual(data["stack"], "developer_core")

    def test_cli_recommend_rejects_free_text(self) -> None:
        proc = subprocess.run(
            [str(AGENTIT_CLI), "mcp", "recommend", "implement figma design"],
            capture_output=True,
            text=True,
            check=False,
            cwd=str(REPO_ROOT),
        )
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("AI must choose an explicit named stack", proc.stderr)

    def test_cli_snippet(self) -> None:
        proc = subprocess.run(
            [
                str(AGENTIT_CLI),
                "mcp",
                "snippet",
                "context7",
                "--provider",
                "claude",
                "--format",
                "text",
            ],
            capture_output=True,
            text=True,
            check=True,
            cwd=str(REPO_ROOT),
        )
        self.assertIn("claude mcp add context7", proc.stdout)


if __name__ == "__main__":
    unittest.main()
