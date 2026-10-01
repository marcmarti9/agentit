from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from router.skills_cli import list_packs, pack_candidates
from router.skill_loader import load_skill_bodies


ROOT = Path(__file__).resolve().parents[1]


class JitSkillsCliTests(unittest.TestCase):
    def test_pack_listing_is_metadata_only(self):
        packs = list_packs()
        ids = {item["id"] for item in packs}
        self.assertIn("engineering", ids)
        self.assertIn("design", ids)
        rendered = repr(packs)
        self.assertNotIn("# Active Agentit Skill Bodies", rendered)
        self.assertNotIn("## Contract", rendered)

    def test_candidates_are_bounded_to_requested_pack(self):
        engineering = pack_candidates(["engineering"])
        self.assertTrue(any(item["id"] == "debugging-and-error-recovery" for item in engineering))
        self.assertFalse(any(item["pack"] == "executive" for item in engineering))

    def test_cross_pack_candidates_dedupe_by_pack_and_skill(self):
        items = pack_candidates(["engineering", "backend"])
        pairs = [(item["pack"], item["id"]) for item in items]
        self.assertEqual(len(pairs), len(set(pairs)))
        self.assertIn(("engineering", "architect-orchestrator"), pairs)
        self.assertIn(("backend", "architect-orchestrator"), pairs)

    def test_selected_body_is_loaded_only_after_explicit_selection(self):
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            bodies = load_skill_bodies(["security-and-hardening"], project_root=project)
            self.assertEqual(["security-and-hardening"], [item["id"] for item in bodies])
            self.assertIn("content", bodies[0])
            self.assertNotIn("debugging-and-error-recovery", bodies[0]["content"][:200])

    def test_activate_delivers_exact_complete_body_and_no_neighbors(self):
        with tempfile.TemporaryDirectory() as temporary:
            completed = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "agentit"),
                    "skills",
                    "activate",
                    "interview-me",
                    "--project",
                    temporary,
                    "--format",
                    "json",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
        payload = json.loads(completed.stdout)
        self.assertEqual(["interview-me"], [item["id"] for item in payload["skills"]])
        expected = (ROOT / "skills" / "interview-me" / "SKILL.md").read_text(encoding="utf-8")
        self.assertEqual(expected, payload["skills"][0]["content"])
        self.assertEqual(len(expected.encode("utf-8")), payload["skills"][0]["bytes"])


if __name__ == "__main__":
    unittest.main()
