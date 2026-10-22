import unittest
from pathlib import Path

from router.profiles import load_catalog, resolve_profile


REPOSITORY = Path(__file__).resolve().parents[1]
SKILL_ID = "adversarial-idea-review"


class AdversarialIdeaReviewTests(unittest.TestCase):
    def test_skill_is_available_in_idea_profiles_but_not_core(self) -> None:
        catalog = load_catalog(REPOSITORY / "profiles.yaml")

        core = resolve_profile("core", catalog, repo_root=REPOSITORY)
        product = resolve_profile("product", catalog, repo_root=REPOSITORY)
        research = resolve_profile("research", catalog, repo_root=REPOSITORY)
        executive = resolve_profile("executive", catalog, repo_root=REPOSITORY)
        all_skills = resolve_profile("all", catalog, repo_root=REPOSITORY)

        self.assertNotIn(SKILL_ID, core)
        self.assertIn(SKILL_ID, product)
        self.assertIn(SKILL_ID, research)
        self.assertIn(SKILL_ID, executive)
        self.assertIn(SKILL_ID, all_skills)

    def test_owned_policy_requires_adversarial_review_without_modifying_canonical_source(self) -> None:
        router = (REPOSITORY / "skills/task-router/SKILL.md").read_text()
        specialist = (REPOSITORY / "skills/adversarial-idea-review/SKILL.md").read_text()
        self.assertIn("Select `adversarial-idea-review` before converging", router)
        self.assertIn("consequential or materially uncertain proposals", router)
        self.assertIn("KILL", specialist)
        self.assertIn("PROCEED_WITH_GATES", specialist)
        import hashlib, json
        lock = json.loads((REPOSITORY / "skills/UPSTREAM_LOCK.json").read_text())
        item = next(m for m in lock["mappings"] if m["skill"] == "idea-refine")
        body = (REPOSITORY / "skills/idea-refine/SKILL.md").read_bytes()
        self.assertEqual(hashlib.sha256(body).hexdigest(), item["files"]["SKILL.md"]["sha256"])

    def test_mechanical_adapter_leaves_semantic_review_selection_to_router(self) -> None:
        meta_skill = (
            REPOSITORY / "skills" / "using-agent-skills" / "SKILL.md"
        ).read_text(encoding="utf-8")

        self.assertNotIn("adversarial-idea-review", meta_skill)
        self.assertIn("`task-router` selects procedures and review depth", meta_skill)
        router = (REPOSITORY / "skills/task-router/SKILL.md").read_text()
        self.assertIn("A routine fix need not invoke a separate adversarial procedure or worker", router)

    def test_canonical_refresh_has_no_native_policy_overlay(self) -> None:
        self.assertFalse((REPOSITORY / "scripts/apply-agentit-skill-overlays.py").exists())
        import json
        lock = json.loads((REPOSITORY / "skills/UPSTREAM_LOCK.json").read_text())
        destinations = [m.get("destination", "skills/" + m["skill"]) for m in lock["mappings"]]
        self.assertNotIn("skills/using-agent-skills", destinations)
        self.assertIn("vendor/agent-skills/using-agent-skills", destinations)

    def test_skill_has_evidence_and_kill_gate_contracts(self) -> None:
        skill = (
            REPOSITORY / "skills" / SKILL_ID / "SKILL.md"
        ).read_text(encoding="utf-8")

        for marker in (
            "FACT",
            "SIGNAL",
            "ANECDOTE",
            "HYPOTHESIS",
            "ASSUMPTION",
            "KILL GATES",
            "Minimum Viable Replacement",
            "services trap",
        ):
            self.assertIn(marker, skill)


if __name__ == "__main__":
    unittest.main()
