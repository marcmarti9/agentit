"""Actual CLI exchange between independent project copies, without network access."""
from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from router.continuity import ensure_state_file

ROOT = Path(__file__).resolve().parents[1]


class HandoffCliTests(unittest.TestCase):
    def git(self, *args, cwd=None):
        return subprocess.run(
            ["git", "-c", f"core.hooksPath={os.devnull}", "-c", "user.name=Fixture",
             "-c", "user.email=fixture@example.invalid", *map(str, args)],
            cwd=cwd, check=True, text=True, capture_output=True,
        )

    def fixture(self, base):
        sender, receiver = base / "laptop", base / "server-with-different-path"
        sender.mkdir()
        self.git("init", "--initial-branch=work", sender)
        (sender / ".gitignore").write_text(".agentit/\n")
        (sender / "proof.md").write_text("Synthetic verification: focused checks passed.\n")
        self.git("add", ".", cwd=sender)
        self.git("commit", "-m", "Synthetic code and evidence", cwd=sender)
        self.git("clone", sender, receiver)
        for project in (sender, receiver):
            result = subprocess.run(["git", "-C", str(project), "remote", "remove", "origin"],
                                    capture_output=True)
            self.git("remote", "add", "origin", "https://github.com/fixture/portable-project.git", cwd=project)
        state = ensure_state_file(sender, goal="Continue the synthetic implementation")
        state.write_text(state.read_text().replace("## Next actions\n1.", "## Next actions\n1. Inspect proof.md and continue the requested feature."))
        return sender, receiver

    def call(self, *args, expected=0):
        cli = os.environ.get("AGENTIT_TEST_CLI", str(ROOT / "agentit"))
        result = subprocess.run([sys.executable, cli, "continuity", *map(str, args)],
                                capture_output=True, text=True)
        self.assertEqual(expected, result.returncode, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def test_cli_preview_private_transfer_resume_and_repeat(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary).resolve()
            sender, receiver = self.fixture(base)
            package = sender / ".agentit/next-pc"
            args = ("handoff", "--project", sender, "--output", package,
                    "--skill", "long-horizon-recovery", "--artifact", "proof.md")
            self.assertTrue(self.call(*args)["ready"])
            self.assertFalse(package.exists())
            self.assertTrue(self.call(*args, "--apply")["applied"])
            transferred = base / "private-transfer"
            shutil.copytree(package, transferred)
            preview = self.call("inspect", transferred, "--project", receiver)
            self.assertTrue(preview["ready"])
            self.assertFalse((receiver / ".agentit/STATE.md").exists())
            applied = self.call("resume", transferred, "--project", receiver, "--apply")
            self.assertTrue(applied["applied"])
            self.assertEqual((sender / ".agentit/STATE.md").read_bytes(),
                             (receiver / ".agentit/STATE.md").read_bytes())
            restored = Path(applied["received_path"]) / "artifacts/proof.md"
            self.assertEqual((sender / "proof.md").read_bytes(), restored.read_bytes())
            self.assertTrue(self.call("resume", transferred, "--project", receiver, "--apply")["ready"])
            self.assertEqual("", self.git("status", "--porcelain", cwd=receiver).stdout.strip())

    def test_cli_mismatched_code_is_blocked_before_state_write(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary).resolve()
            sender, receiver = self.fixture(base)
            package = sender / ".agentit/next-pc"
            self.call("handoff", "--project", sender, "--output", package, "--apply")
            (receiver / "different-code.txt").write_text("Different committed code\n")
            self.git("add", ".", cwd=receiver)
            self.git("commit", "-m", "Destination diverged", cwd=receiver)
            blocked = self.call("resume", package, "--project", receiver, "--apply", expected=2)
            self.assertFalse(blocked["ready"])
            self.assertTrue(blocked["blockers"])
            self.assertFalse((receiver / ".agentit/STATE.md").exists())

    def test_cli_initial_state_stays_private_when_project_has_no_gitignore(self):
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary).resolve() / "unconfigured-project"
            project.mkdir()
            self.git("init", "--initial-branch=work", project)
            (project / "README.md").write_text("Synthetic project\n")
            self.call("init", "--project", project)
            self.assertTrue((project / ".agentit/STATE.md").is_file())
            self.assertFalse((project / ".gitignore").exists())
            self.git("add", ".", cwd=project)
            tracked = self.git("ls-files", cwd=project).stdout.splitlines()
            self.assertEqual(["README.md"], tracked)


if __name__ == "__main__":
    unittest.main()
