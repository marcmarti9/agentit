"""Prove authority guidance is actually transported with selected raw bodies."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from router.skill_authority import SKILL_AUTHORITY
from router.skill_loader import load_skill_bodies, render_prompt
from router.worker_context import WorkerTaskSpec, build_worker_context, render_worker_prompt


ROOT = Path(__file__).resolve().parents[1]


class SkillAuthorityTests(unittest.TestCase):
    def test_cli_json_carries_authority_and_only_selected_raw_body(self):
        with tempfile.TemporaryDirectory() as directory:
            completed = subprocess.run([sys.executable, str(ROOT / "agentit"), "skills", "show", "interview-me", "--project", directory, "--format", "json"], check=True, capture_output=True, text=True)
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["authority"], SKILL_AUTHORITY)
        self.assertEqual([skill["id"] for skill in payload["skills"]], ["interview-me"])
        self.assertEqual(payload["skills"][0]["content"], (ROOT / "skills/interview-me/SKILL.md").read_text())

    def test_prompt_precedes_raw_guidance_with_single_authority_envelope(self):
        with tempfile.TemporaryDirectory() as directory:
            bodies = load_skill_bodies(["interview-me", "spec-driven-development"], project_root=Path(directory))
        prompt = render_prompt(bodies)
        self.assertEqual(prompt.count(SKILL_AUTHORITY.rstrip()), 1)
        self.assertLess(prompt.index(SKILL_AUTHORITY.rstrip()), prompt.index(bodies[0]["content"].rstrip()))
        self.assertIn("do not activate other skills", SKILL_AUTHORITY)

    def test_worker_payload_and_rendered_contract_include_authority(self):
        with tempfile.TemporaryDirectory() as directory:
            payload = build_worker_context(WorkerTaskSpec(objective="Review selected work", role="reviewer", skills=["interview-me"]), project_root=Path(directory))
        self.assertEqual(payload["worker_context"]["skill_authority"], SKILL_AUTHORITY)
        self.assertIn(SKILL_AUTHORITY.rstrip(), render_worker_prompt(payload))


if __name__ == "__main__":
    unittest.main()
