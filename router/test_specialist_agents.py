import unittest
from pathlib import Path

import yaml


REPOSITORY = Path(__file__).resolve().parents[1]
CATALOG_PATH = REPOSITORY / "agents" / "catalog.yaml"
SKILLS_DIR = REPOSITORY / "skills"
POLICY_DOC = REPOSITORY / "docs" / "AGENTIT_INTERVIEW_AND_PROVIDER_POLICY.md"
CONTINUITY_DOC = REPOSITORY / "docs" / "PROJECT_CONTINUITY.md"
EFFORT_PATH = REPOSITORY / "effort" / "levels.yaml"
PROFILES_PATH = REPOSITORY / "profiles.yaml"
INTERVIEW_SKILL = SKILLS_DIR / "interview-me" / "SKILL.md"
UIUX_SKILL = SKILLS_DIR / "ui-ux-pro-max-intelligence" / "SKILL.md"


class SpecialistAgentCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = yaml.safe_load(CATALOG_PATH.read_text(encoding="utf-8"))
        cls.specialists = cls.catalog["specialists"]
        cls.effort = yaml.safe_load(EFFORT_PATH.read_text(encoding="utf-8"))
        cls.profiles = yaml.safe_load(PROFILES_PATH.read_text(encoding="utf-8"))

    def test_catalog_has_unique_specialist_ids(self):
        ids = [item["id"] for item in self.specialists]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertGreaterEqual(len(ids), 10)

    def test_specialists_have_valid_mode_and_contract(self):
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

    def test_design_specialists_cover_research_intelligence_direction_tools_delight_and_spatial(self):
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

    def test_policy_preserves_intelligent_delegation(self):
        policy = self.catalog["policy"]
        self.assertIn(policy["default"], {"direct", "intelligent"})
        self.assertTrue(policy["specialist_spawn_requires_benefit"])
        self.assertTrue(policy["one_writer_per_file"])
        self.assertTrue(policy["architect_integrates"])
        self.assertTrue(policy.get("no_hard_subagent_caps", True))
        self.assertTrue(policy.get("critic_required_for_large_structural_plans", True))
        self.assertLessEqual(policy["max_design_competition_concepts"], 3)

    def test_policy_is_provider_neutral_and_degrades_gracefully(self):
        policy = self.catalog["policy"]
        self.assertTrue(policy["provider_neutral"])
        self.assertTrue(policy["graceful_degradation_to_parent"])
        self.assertTrue(policy["interview_for_all_product_work"])
        self.assertTrue(
            policy.get("craft_depth_design_only")
            or policy.get("effort_level_required_for_product_work") is False
            or policy.get("effort_catalog") == "effort/levels.yaml"
        )
        self.assertEqual("effort/levels.yaml", policy["effort_catalog"])
        self.assertTrue(POLICY_DOC.is_file())
        text = POLICY_DOC.read_text(encoding="utf-8").lower()
        for provider in ("openai", "anthropic", "google", "xai"):
            self.assertIn(provider, text)
        self.assertTrue(
            "multi-agent execution is an optimization" in text
            or "intelligent delegation" in text
            or "spawn when beneficial" in text
        )

    def test_interview_batches_all_current_material_questions(self):
        policy = self.catalog["policy"]
        self.assertTrue(policy["interview_batch_all_current_questions"])
        text = INTERVIEW_SKILL.read_text(encoding="utf-8").lower()
        self.assertIn("all material questions", text)
        self.assertIn("one numbered batch", text)
        self.assertIn("follow-up batch", text)
        self.assertIn("genuinely new material decisions", text)

    def test_continuity_is_required_and_resumable(self):
        policy = self.catalog["policy"]
        self.assertTrue(policy["continuity_required_for_product_work"])
        self.assertEqual("docs/PROJECT_CONTINUITY.md", policy["continuity_policy"])
        self.assertTrue(CONTINUITY_DOC.is_file())
        text = CONTINUITY_DOC.read_text(encoding="utf-8").lower()
        self.assertIn("docs/agentit/state.md", text)
        self.assertIn("token exhaustion", text)
        self.assertIn("machine switch", text)
        self.assertIn("resume protocol", text)

    def test_pr_first_is_default_but_explicit_override_is_allowed(self):
        policy = self.catalog["policy"]
        self.assertTrue(policy["pr_first_repository_changes"])
        self.assertTrue(policy["direct_default_branch_requires_explicit_override"])
        text = CONTINUITY_DOC.read_text(encoding="utf-8").lower()
        self.assertIn("branch + pull request workflow by default", text)
        self.assertIn("unless the user explicitly asks", text)

    def test_ui_ux_pro_max_intelligence_is_jit_and_in_design_profile(self):
        self.assertTrue(UIUX_SKILL.is_file())
        text = UIUX_SKILL.read_text(encoding="utf-8").lower()
        self.assertIn("nextlevelbuilder/ui-ux-pro-max-skill", text)
        self.assertIn("searchable design-intelligence source", text)
        self.assertIn("do not dump the full database", text)
        design_skills = self.profiles["profiles"]["design"]["skills"]
        self.assertIn("ui-ux-pro-max-intelligence", design_skills)

    def test_effort_catalog_is_design_craft_depth_with_domain_packs(self):
        self.assertTrue(EFFORT_PATH.is_file())
        levels = self.effort["levels"]
        self.assertEqual({"standard", "polished", "studio"}, set(levels))
        policy = self.effort["policy"]
        self.assertTrue(policy["craft_depth_design_only"])
        self.assertTrue(policy["interview_required_for_product_work"])
        self.assertTrue(policy["mechanical_bypass_allowed"])
        self.assertTrue(policy["no_hard_subagent_caps"])
        self.assertTrue(policy["token_estimates_are_project_aware"])
        self.assertIn("domain_packs", self.effort)
        self.assertIn("design", self.effort["domain_packs"])
        for level_id in ("standard", "polished", "studio"):
            level = levels[level_id]
            self.assertTrue(level["typical_total_token_range"])
            self.assertTrue(level["result_expectation"])
            self.assertTrue(level["relative_cost"])

    def test_effort_selection_is_design_aware_and_project_tokenized(self):
        protocol = self.effort["selection_protocol"]
        self.assertTrue(protocol["required_interview_question"])
        self.assertTrue(protocol["recommendation_required"])
        self.assertTrue(protocol["craft_depth_question_only_for_design_visual"])
        self.assertTrue(protocol["user_must_confirm_craft_depth_for_design"])
        self.assertTrue(protocol["do_not_pretend_precision"])
        self.assertTrue(protocol["no_powerwords_required"])
        required_explanations = set(protocol["must_explain"])
        self.assertIn("project-aware rough token estimate and what drives it", required_explanations)
        self.assertIn("why the recommended domain pack fits the task", required_explanations)

    def test_mechanical_bypass_is_narrow_and_excludes_product_choices(self):
        bypass = self.effort["mechanical_bypass"]
        self.assertIn("create explicitly named directories or files", bypass["examples"])
        never = set(bypass["never_bypass_when"])
        self.assertIn("changing product functionality", never)
        self.assertIn("choosing UX or visual behavior", never)
        self.assertIn("creating a new product, feature, page, workflow, or design", never)


if __name__ == "__main__":
    unittest.main()
