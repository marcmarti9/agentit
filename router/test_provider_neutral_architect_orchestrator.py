"""Regression tests for provider-neutral architect/orchestrator discovery."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from router.bootstrap import SOURCE_ROOT, build_install_plan


CORE_SKILLS = {"using-agentit", "task-router", "using-agent-skills"}
PROVIDERS = ("claude", "codex", "antigravity")


class ProviderNeutralArchitectOrchestratorTests(unittest.TestCase):
    def test_architect_orchestrator_lives_in_shared_runtime_for_every_provider(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            for provider in PROVIDERS:
                with self.subTest(provider=provider):
                    plan = build_install_plan(home=home, provider=provider)
                    destinations = {
                        Path(item["destination"]).as_posix()
                        for item in plan["operations"]
                    }
                    self.assertTrue(
                        any(
                            path.endswith(
                                "/.agentit/runtime/skills/architect-orchestrator/SKILL.md"
                            )
                            for path in destinations
                        ),
                        provider,
                    )

    def test_no_provider_gets_semantic_architect_roles_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            for provider in PROVIDERS:
                with self.subTest(provider=provider):
                    plan = build_install_plan(home=home, provider=provider)
                    categories = {item["category"] for item in plan["operations"]}
                    self.assertFalse(
                        any(category == "provider:claude:agent" for category in categories)
                    )

    def test_provider_global_skill_projection_remains_exactly_core(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            for provider in PROVIDERS:
                with self.subTest(provider=provider):
                    plan = build_install_plan(home=home, provider=provider)
                    projected = set()
                    marker = f"provider:{provider}:skill"
                    for item in plan["operations"]:
                        if item["category"] != marker:
                            continue
                        destination = Path(item["destination"])
                        parts = destination.parts
                        if "skills" in parts:
                            index = len(parts) - 1 - list(reversed(parts)).index("skills")
                            if index + 1 < len(parts):
                                projected.add(parts[index + 1])
                    self.assertEqual(projected, CORE_SKILLS)
                    self.assertNotIn("architect-orchestrator", projected)

    def test_legacy_installer_does_not_project_claude_only_semantic_agents(self) -> None:
        text = (SOURCE_ROOT / "install.sh").read_text(encoding="utf-8")
        self.assertNotIn(
            'copy_tree "$REPO_DIR/agents" "$USER_HOME/.claude/agents"',
            text,
        )
        self.assertIn("architect-orchestrator", text)
        self.assertIn("ningún host recibe una jerarquía semántica extra", text)


if __name__ == "__main__":
    unittest.main()
