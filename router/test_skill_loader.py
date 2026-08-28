from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from skill_loader import SkillLoadError, load_skill_bodies, render_prompt


class WorkerSkillLoaderTests(unittest.TestCase):
    def test_harness_skill_is_loaded_and_rendered(self):
        with tempfile.TemporaryDirectory() as tmp:
            skills = load_skill_bodies(["design-taste-frontend"], project_root=Path(tmp))
        skill = skills[0]
        self.assertEqual("harness", skill["source"])
        self.assertEqual(64, len(skill["sha256"]))
        self.assertIn("Anti-default discipline", skill["content"])
        rendered = render_prompt(skills)
        self.assertIn("Skill IDs alone do not count as activation", rendered)
        self.assertIn(skill["sha256"], rendered)

    def test_project_local_skill_wins(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            local = root / ".agents" / "skills" / "design-taste-frontend"
            local.mkdir(parents=True)
            body = "# Project design skill\n\nUse this local direction.\n"
            (local / "SKILL.md").write_text(body, encoding="utf-8")
            skills = load_skill_bodies(["design-taste-frontend"], project_root=root)
        self.assertEqual("project", skills[0]["source"])
        self.assertEqual(body, skills[0]["content"])

    def test_private_agentit_profile_cache_precedes_harness_but_not_project_native(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            private = root / ".agentit" / "profile-skills" / "design-taste-frontend"
            private.mkdir(parents=True)
            private_body = "# Private Agentit profile skill\n\nUse the enabled project profile.\n"
            (private / "SKILL.md").write_text(private_body, encoding="utf-8")

            skills = load_skill_bodies(["design-taste-frontend"], project_root=root)
            self.assertEqual("project-agentit-profile", skills[0]["source"])
            self.assertEqual(private_body, skills[0]["content"])

            local = root / ".agents" / "skills" / "design-taste-frontend"
            local.mkdir(parents=True)
            local_body = "# Project-native skill\n\nProject instructions win.\n"
            (local / "SKILL.md").write_text(local_body, encoding="utf-8")

            skills = load_skill_bodies(["design-taste-frontend"], project_root=root)
            self.assertEqual("project", skills[0]["source"])
            self.assertEqual(local_body, skills[0]["content"])

    def test_missing_skill_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(SkillLoadError):
                load_skill_bodies(["does-not-exist"], project_root=Path(tmp))


if __name__ == "__main__":
    unittest.main()
