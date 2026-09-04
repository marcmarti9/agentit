"""Regression tests for Agentit's JIT executive profile."""

from __future__ import annotations

import unittest
from pathlib import Path

import yaml

from router.profiles import load_catalog as load_profile_catalog, resolve_profile


REPOSITORY = Path(__file__).resolve().parents[1]

EXECUTIVE_SKILLS = {
    "executive-orchestration",
    "executive-strategy",
    "executive-finance",
    "executive-people",
    "executive-legal",
    "executive-operations",
    "executive-marketing",
    "executive-product",
    "executive-board",
    "executive-chief-of-staff",
}

EXECUTIVE_SPECIALISTS = {
    "executive-strategist",
    "finance-executive",
    "people-executive",
    "legal-executive",
    "operations-executive",
    "marketing-executive",
    "product-executive",
    "board-executive",
    "executive-chief-of-staff",
}


class ExecutiveProfileTests(unittest.TestCase):
    def test_executive_profile_is_discoverable_but_not_global_core(self) -> None:
        catalog = load_profile_catalog()
        self.assertEqual(catalog["global_profiles"], ["core"])

        core = set(resolve_profile("core", catalog, repo_root=REPOSITORY))
        executive = set(resolve_profile("executive", catalog, repo_root=REPOSITORY))
        all_skills = set(resolve_profile("all", catalog, repo_root=REPOSITORY))

        self.assertEqual(
            core,
            {"using-agentit", "task-router", "using-agent-skills"},
        )
        self.assertTrue(EXECUTIVE_SKILLS <= executive)
        self.assertTrue(EXECUTIVE_SKILLS <= all_skills)
        self.assertTrue(EXECUTIVE_SKILLS.isdisjoint(core))

    def test_every_executive_skill_has_a_body(self) -> None:
        for skill in EXECUTIVE_SKILLS:
            path = REPOSITORY / "skills" / skill / "SKILL.md"
            self.assertTrue(path.is_file(), skill)
            text = path.read_text(encoding="utf-8")
            self.assertIn(f"name: {skill}", text)
            self.assertIn("Provenance", text)
            self.assertIn("OpenExecutive", text)

    def test_executive_specialists_reference_real_executive_skills(self) -> None:
        catalog_path = REPOSITORY / "agents" / "catalog.yaml"
        catalog = yaml.safe_load(catalog_path.read_text(encoding="utf-8"))
        specialists = {item["id"]: item for item in catalog["specialists"]}

        self.assertTrue(EXECUTIVE_SPECIALISTS <= set(specialists))
        for specialist_id in EXECUTIVE_SPECIALISTS:
            selected = set(specialists[specialist_id].get("skills", []))
            self.assertTrue(selected & EXECUTIVE_SKILLS, specialist_id)

    def test_executive_pack_preserves_installation_vs_activation_boundary(self) -> None:
        text = (REPOSITORY / "references" / "agentit-skill-packs.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("## executive", text)
        self.assertIn("executive-orchestration", text)
        self.assertIn("profile is deliberately broad", text)
        self.assertIn("does **not** activate", text)

    def test_durable_executive_architecture_doc_exists(self) -> None:
        text = (REPOSITORY / "docs" / "EXECUTIVE_PROFILE.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Runtime context must remain narrow", text)
        self.assertIn("single parent synthesis", text)
        self.assertIn("Authority", text)


if __name__ == "__main__":
    unittest.main()
