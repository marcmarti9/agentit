import unittest
from pathlib import Path

import yaml


REPOSITORY = Path(__file__).resolve().parents[1]
CATALOG_PATH = REPOSITORY / "agents" / "catalog.yaml"
SKILLS_DIR = REPOSITORY / "skills"
POLICY_DOC = REPOSITORY / "docs" / "AGENTIT_INTERVIEW_AND_PROVIDER_POLICY.md"
EFFORT_PATH = REPOSITORY / "effort" / "levels.yaml"


class SpecialistAgentCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = yaml.safe_load(CATALOG_PATH.read_text(encoding="utf-8"))
        cls.specialists = cls.catalog["specialists"]
        cls.effort = yaml.safe_load(EFFORT_PATH.read_text(encoding="utf-8"))

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

    def test_design_specialists_cover_research_direction_tools_delight_and_spatial(self):
        ids = {item["id"] for item in self.specialists}
        required = {
            "ui-researcher",
            "creative-tool-scout",
            "visual-storytelling-director",
            "spatial-experience-designer",
            "delight-and-whimsy",
            "design-critic",
            "performance-benchmarker",
        }
        self.assertTrue(required.issubset(ids), required - ids)

    def test_policy_preserves_single_agent_first(self):
        policy = self.catalog["policy"]
        self.assertEqual("direct", policy["default"])
        self.assertTrue(policy["specialist_spawn_requires_benefit"])
        self.assertTrue(policy["one_writer_per_file"])
        self.assertTrue(policy["architect_integrates"])
        self.assertLessEqual(policy["max_design_competition_concepts"], 3)

    def test_policy_is_provider_neutral_and_degrades_gracefully(self):
        policy = self.catalog["policy"]
        self.assertTrue(policy["provider_neutral"])
        self.assertTrue(policy["graceful_degradation_to_parent"])
        self.assertTrue(policy["interview_for_all_product_work"])
        self.assertTrue(policy["effort_level_required_for_product_work"])
        self.assertEqual("effort/levels.yaml", policy["effort_catalog"])
        self.assertTrue(POLICY_DOC.is_file())
        text = POLICY_DOC.read_text(encoding="utf-8").lower()
        for provider in ("openai", "anthropic", "google", "xai"):
            self.assertIn(provider, text)
        self.assertIn("multi-agent execution is an optimization", text)

    def test_effort_catalog_has_three_ordered_levels_and_budget_metadata(self):
        self.assertTrue(EFFORT_PATH.is_file())
        levels = self.effort["levels"]
        self.assertEqual({"standard", "polished", "studio"}, set(levels))
        self.assertEqual("standard", self.effort["policy"]["default_level"])
        self.assertTrue(self.effort["policy"]["interview_required_for_product_work"])
        self.assertTrue(self.effort["policy"]["mechanical_bypass_allowed"])
        for level_id in ("standard", "polished", "studio"):
            level = levels[level_id]
            self.assertTrue(level["typical_total_token_range"])
            self.assertTrue(level["result_expectation"])
            self.assertTrue(level["relative_cost"])

    def test_effort_selection_requires_recommendation_and_user_confirmation(self):
        protocol = self.effort["selection_protocol"]
        self.assertTrue(protocol["required_interview_question"])
        self.assertTrue(protocol["recommendation_required"])
        self.assertTrue(protocol["user_must_confirm_level"])
        self.assertTrue(protocol["do_not_pretend_precision"])
        required_explanations = set(protocol["must_explain"])
        self.assertIn("rough total token envelope and relative cost", required_explanations)
        self.assertIn("why the recommended level fits the task", required_explanations)

    def test_mechanical_bypass_is_narrow_and_excludes_product_choices(self):
        bypass = self.effort["mechanical_bypass"]
        self.assertIn("create explicitly named directories or files", bypass["examples"])
        never = set(bypass["never_bypass_when"])
        self.assertIn("changing product functionality", never)
        self.assertIn("choosing UX or visual behavior", never)
        self.assertIn("creating a new product, feature, page, workflow, or design", never)


if __name__ == "__main__":
    unittest.main()
