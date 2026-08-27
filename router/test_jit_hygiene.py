"""Regression tests for Agentit's cold-session JIT and documentation invariants."""

from __future__ import annotations

import unittest
from pathlib import Path

from router.mcp_catalog import load_catalog as load_mcp_catalog
from router.profiles import load_catalog as load_profile_catalog, resolve_profile


REPOSITORY = Path(__file__).resolve().parents[1]


class JitHygieneTests(unittest.TestCase):
    def test_global_core_stays_exactly_three_navigation_skills(self) -> None:
        catalog = load_profile_catalog()
        self.assertEqual(catalog["global_profiles"], ["core"])
        self.assertEqual(
            resolve_profile("core", catalog, repo_root=REPOSITORY),
            ["using-agentit", "task-router", "using-agent-skills"],
        )

    def test_all_profile_resolves_every_registered_skill(self) -> None:
        catalog = load_profile_catalog()
        resolved = resolve_profile("all", catalog, repo_root=REPOSITORY)
        self.assertIn("design-md-workflow", resolved)
        self.assertIn("diagram-and-architecture-visuals", resolved)
        self.assertIn("anti-ai-slop-writing", resolved)

    def test_mcp_catalog_never_auto_activates(self) -> None:
        catalog = load_mcp_catalog(REPOSITORY / "mcp" / "catalog.yaml")
        self.assertFalse(catalog["policy"]["auto_activate"])
        self.assertTrue(catalog["policy"]["agent_may_toggle"])

    def test_core_skill_contains_cold_start_and_minimum_docs_contract(self) -> None:
        text = (REPOSITORY / "skills" / "using-agentit" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Every new execution session is **semantically cold**", text)
        self.assertIn("Core documentation invariant", text)
        self.assertIn("documentation-drift check", text)
        self.assertIn("installed project profiles", text)
        self.assertIn("task-added MCP", text)

    def test_profiles_packs_and_selected_context_remain_distinct(self) -> None:
        text = (
            REPOSITORY / "skills" / "using-agent-skills" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Profiles vs packs vs active context", text)
        self.assertIn("Installation is not activation", text)
        self.assertIn("No cross-session semantic carry-over", text)

    def test_documentation_contract_requires_component_level_understanding(self) -> None:
        text = (REPOSITORY / "docs" / "DOCUMENTATION_CONTRACT.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("## Component-level rule", text)
        self.assertIn("purpose / ownership", text)
        self.assertIn("failure modes / retries / fallbacks", text)
        self.assertIn("without replaying the original chat", text)


if __name__ == "__main__":
    unittest.main()
