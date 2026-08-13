"Focused tests for real skill-body projection into delegated workers."

from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from worker_context import (
    WorkerContextError,
    WorkerTaskSpec,
    assert_projection_complete,
    build_and_validate,
    build_worker_context,
    render_worker_prompt,
    validate_for_spawn,
)


class WorkerSkillBodyProjectionTests(unittest.TestCase):
    def test_harness_skill_body_is_loaded_hashed_and_rendered(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            payload = build_and_validate(
                WorkerTaskSpec(
                    objective="Review the application boundary",
                    skills=("security-and-hardening",),
                ),
                project_root=root,
                known_repository_skills={"security-and-hardening"},
            )

        ctx = payload["worker_context"]
        self.assertEqual(["security-and-hardening"], ctx["skills_projected"])
        self.assertEqual([], ctx["skills_missing_bodies"])
        self.assertEqual(1, len(ctx["skill_bodies_projected"]))
        body = ctx["skill_bodies_projected"][0]
        self.assertEqual("security-and-hardening", body["id"])
        self.assertEqual("harness", body["source"])
        self.assertEqual(64, len(body["sha256"]))
        self.assertIn("# Security", body["content"])

        receipt = ctx["projection"]["skill_load_receipt"][0]
        self.assertEqual(body["sha256"], receipt["sha256"])
        rendered = render_worker_prompt(payload)
        self.assertIn("### Skill: security-and-hardening", rendered)
        self.assertIn(body["sha256"], rendered)
        self.assertIn("# Security", rendered)

    def test_project_local_skill_body_overrides_harness_body(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill = root / ".agents" / "skills" / "security-and-hardening"
            skill.mkdir(parents=True)
            local_body = "# Project Security Override\n\nUse the project-specific review workflow.\n"
            (skill / "SKILL.md").write_text(local_body, encoding="utf-8")

            payload = build_and_validate(
                WorkerTaskSpec(
                    objective="Review the application boundary",
                    skills=("security-and-hardening",),
                ),
                project_root=root,
                known_repository_skills={"security-and-hardening"},
            )

        body = payload["worker_context"]["skill_bodies_projected"][0]
        self.assertEqual("project", body["source"])
        self.assertEqual(local_body, body["content"])
        self.assertIn(".agents/skills/security-and-hardening/SKILL.md", body["path"])

    def test_missing_selected_skill_body_fails_spawn_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            payload = build_worker_context(
                WorkerTaskSpec(objective="Use a custom workflow", skills=("custom-missing",)),
                project_root=root,
                known_repository_skills={"custom-missing"},
            )

        ctx = payload["worker_context"]
        self.assertEqual(["custom-missing"], ctx["skills_projected"])
        self.assertEqual(["custom-missing"], ctx["skills_missing_bodies"])
        with self.assertRaises(WorkerContextError) as cm:
            validate_for_spawn(payload)
        self.assertIn("skill bodies unavailable", str(cm.exception))

    def test_skill_body_hash_tampering_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            payload = build_worker_context(
                WorkerTaskSpec(
                    objective="Review the application boundary",
                    skills=("security-and-hardening",),
                ),
                project_root=root,
                known_repository_skills={"security-and-hardening"},
            )

        payload["worker_context"]["skill_bodies_projected"][0]["content"] += "\nchanged"
        with self.assertRaises(WorkerContextError) as cm:
            assert_projection_complete(payload)
        self.assertIn("hash mismatch", str(cm.exception))

    def test_symlinked_project_skill_is_rejected_instead_of_followed(self):
        if not hasattr(os, "symlink"):
            self.skipTest("symlinks unavailable")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            real = root / "real-skill"
            real.mkdir()
            (real / "SKILL.md").write_text("# Local body\n", encoding="utf-8")
            target = root / ".agents" / "skills"
            target.mkdir(parents=True)
            try:
                (target / "security-and-hardening").symlink_to(real, target_is_directory=True)
            except OSError as exc:
                self.skipTest(f"symlink creation unavailable: {exc}")

            with self.assertRaises(WorkerContextError):
                build_worker_context(
                    WorkerTaskSpec(
                        objective="Review the application boundary",
                        skills=("security-and-hardening",),
                    ),
                    project_root=root,
                    known_repository_skills={"security-and-hardening"},
                )


if __name__ == "__main__":
    unittest.main()
