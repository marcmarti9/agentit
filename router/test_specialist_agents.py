import unittest
from pathlib import Path

import yaml


REPOSITORY = Path(__file__).resolve().parents[1]
CATALOG_PATH = REPOSITORY / "agents" / "catalog.yaml"
SKILLS_DIR = REPOSITORY / "skills"
POLICY_DOC = REPOSITORY / "docs" / "AGENTIT_INTERVIEW_AND_PROVIDER_POLICY.md"
CONTINUITY_DOC = REPOSITORY / "docs" / "PROJECT_CONTINUITY.md"
PROFILES_PATH = REPOSITORY / "profiles.yaml"
INTERVIEW_SKILL = SKILLS_DIR / "interview-me" / "SKILL.md"
UIUX_SKILL = SKILLS_DIR / "ui-ux-pro-max-intelligence" / "SKILL.md"
LEGACY_EFFORT_PATH = REPOSITORY / "effort" / "levels.yaml"


class SpecialistAgentCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = yaml.safe_load(CATALOG_PATH.read_text(encoding="utf-8"))
        cls.specialists = cls.catalog["specialists"]
        cls.profiles = yaml.safe_load(PROFILES_PATH.read_text(encoding="utf-8"))

    def test_catalog_has_unique_specialist_ids(self):
        ids = [item["id"] for item in self.specialists]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertGreaterEqual(len(ids), 10)

    def test_specialists_have_valid_model_readable_contract(self):
        valid_modes = {"implementer", "reviewer", "probe"}
        for item in self.specialists:
            self.assertIn(item["mode"], valid_modes, item["id"])
            self.assertTrue(item.get("description"), item["id"])
            self.assertTrue(item.get("triggers"), item["id"])
            self.assertTrue(item.get("skills"), item["id"])
            self.assertTrue(item.get("output"), item["id"])

    def test_catalog_skill_references_exist(self):
        missing = []
        for item in self.specialists:
            for skill_id in item.get("skills", []):
                if not (SKILLS_DIR / skill_id / "SKILL.md").is_file():
                    missing.append((item["id"], skill_id))
        self.assertEqual([], missing)

    def test_design_specialists_cover_research_direction_tools_delight_and_spatial(self):
        ids = {item["id"] for item in self.specialists}
        required = {
            "design-system-researcher",
            "ui-researcher",
            "creative-tool-scout",
            "visual-storytelling-director",
            "spatial-experience-designer",
            "delight-and-whimsy",
            "design-critic",
            "performance-benchmarker",
        }
        self.assertTrue(required.issubset(ids), required - ids)

    def test_policy_preserves_intelligent_optional_delegation(self):
        policy = self.catalog["policy"]
        self.assertIn(policy["default"], {"direct", "intelligent"})
        self.assertTrue(policy["specialist_spawn_requires_benefit"])
        self.assertTrue(policy["one_writer_per_file"])
        self.assertTrue(policy["parent_integrates"])
        self.assertTrue(policy["no_hard_subagent_caps"])
        self.assertTrue(policy["critic_required_for_large_structural_plans"])
        self.assertTrue(policy["semantic_complexity_owned_by_primary_ai"])
        self.assertTrue(policy["no_powerwords_required"])
        self.assertLessEqual(policy["max_parallel_design_concepts"], 3)

    def test_triggers_are_hints_not_programmatic_router(self):
        policy = self.catalog["policy"]
        notes = policy.get("notes", "").lower()
        self.assertIn("triggers are discovery hints only", notes)
        self.assertIn("must never use them as a natural-language router", notes)

    def test_policy_is_provider_neutral_and_degrades_gracefully(self):
        policy = self.catalog["policy"]
        self.assertTrue(policy["provider_neutral"])
        self.assertTrue(policy["graceful_degradation_to_parent"])
        self.assertTrue(policy["interview_only_for_unresolved_material_decisions"])
        self.assertTrue(POLICY_DOC.is_file())
        text = POLICY_DOC.read_text(encoding="utf-8").lower()
        self.assertIn("primary ai owns the semantic task decision", text)
        self.assertIn("specialists are optional capabilities", text)
        self.assertIn("provider-neutral", text)

    def test_interview_batches_all_current_material_questions(self):
        policy = self.catalog["policy"]
        self.assertTrue(policy["interview_batch_all_current_questions"])
        text = INTERVIEW_SKILL.read_text(encoding="utf-8").lower()
        self.assertIn("all material questions", text)
        self.assertIn("one numbered batch", text)
        self.assertIn("follow-up batch", text)
        self.assertIn("genuinely new material decisions", text)

    def test_continuity_is_private_by_default_and_resumable(self):
        policy = self.catalog["policy"]
        self.assertTrue(policy["continuity_for_substantial_work"])
        self.assertEqual("docs/PROJECT_CONTINUITY.md", policy["continuity_policy"])
        text = CONTINUITY_DOC.read_text(encoding="utf-8").lower()
        self.assertIn(".agentit/state.md", text)
        self.assertIn("context exhaustion", text)
        self.assertIn("resume protocol", text)
        self.assertNotIn("`docs/agentit/state.md`", text)

    def test_pr_first_is_default_but_explicit_override_is_allowed(self):
        policy = self.catalog["policy"]
        self.assertTrue(policy["pr_first_repository_changes"])
        self.assertTrue(policy["direct_default_branch_requires_explicit_override"])
        text = CONTINUITY_DOC.read_text(encoding="utf-8").lower()
        self.assertIn("work branch -> verification -> pr", text)
        self.assertIn("unless explicitly overridden", text)

    def test_ui_ux_intelligence_remains_jit_and_discoverable(self):
        self.assertTrue(UIUX_SKILL.is_file())
        text = UIUX_SKILL.read_text(encoding="utf-8").lower()
        self.assertIn("nextlevelbuilder/ui-ux-pro-max-skill", text)
        self.assertIn("searchable design-intelligence source", text)
        self.assertIn("do not dump the full database", text)
        design_skills = self.profiles["profiles"]["design"]["skills"]
        self.assertIn("ui-ux-pro-max-intelligence", design_skills)

    def test_legacy_effort_tier_catalog_is_removed(self):
        self.assertFalse(LEGACY_EFFORT_PATH.exists())
        policy = self.catalog["policy"]
        for key in (
            "effort_catalog",
            "craft_depth_design_only",
            "activation_phrase_only",
            "effort_level_required_for_product_work",
        ):
            self.assertNotIn(key, policy)


if __name__ == "__main__":
    unittest.main()
