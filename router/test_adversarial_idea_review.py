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

    def test_idea_refine_requires_adversarial_review_before_convergence(self) -> None:
        idea_refine = (
            REPOSITORY / "skills" / "idea-refine" / "SKILL.md"
        ).read_text(encoding="utf-8")

        self.assertIn("adversarial-idea-review", idea_refine)
        self.assertIn("before choosing a Recommended Direction", idea_refine)
        self.assertIn("KILL", idea_refine)
        self.assertIn("PROCEED_WITH_GATES", idea_refine)

    def test_meta_skill_routes_exploration_through_adversarial_gate(self) -> None:
        meta_skill = (
            REPOSITORY / "skills" / "using-agent-skills" / "SKILL.md"
        ).read_text(encoding="utf-8")

        self.assertIn("Any serious non-trivial candidate? → adversarial-idea-review BEFORE convergence", meta_skill)
        self.assertIn("Exploration is not complete until the serious candidate has survived attack", meta_skill)

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
