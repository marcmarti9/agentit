"""Offline integration tests: two independent machines, one private bare Git remote."""

import json
import stat
import sys
import subprocess
import tempfile
import unittest
from pathlib import Path

try:
    from .continuity import ContinuityError, ensure_state_file
    from .continuity_sync import link_remote, sync_state, unlink_remote, _validate_remote, _key_for_project
except ImportError:
    from continuity import ContinuityError, ensure_state_file
    from continuity_sync import link_remote, sync_state, unlink_remote, _validate_remote, _key_for_project


class CrossMachineContinuityTests(unittest.TestCase):
    def git(self, *args, cwd=None):
        return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=True).stdout.strip()

    def setup_remote(self, root):
        remote = root / "private-state.git"
        self.git("init", "--bare", "--initial-branch=main", str(remote))
        return remote

    def make_project(self, root, name, *, goal="Ship feature"):
        project = root / name
        project.mkdir()
        ensure_state_file(project, goal=goal)
        return project

    def append(self, project, value):
        path = project / ".agentit/STATE.md"
        path.write_text(path.read_text() + "\n" + value + "\n", encoding="utf-8")

    def test_two_machines_exchange_without_project_git_tracking(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            remote = self.setup_remote(root)
            a = self.make_project(root, "laptop")
            b = root / "server"
            b.mkdir()
            self.assertEqual("pushed", link_remote(a, str(remote), project_key="app-one")["sync"]["status"])
            self.assertEqual("pulled", link_remote(b, str(remote), project_key="app-one")["sync"]["status"])
            self.assertEqual((a/".agentit/STATE.md").read_bytes(), (b/".agentit/STATE.md").read_bytes())
            self.append(b, "Completed on server")
            self.assertEqual("pushed", sync_state(b)["status"])
            self.assertEqual("pulled", sync_state(a)["status"])
            self.assertIn("Completed on server", (a/".agentit/STATE.md").read_text())
            self.assertEqual(0o600, stat.S_IMODE((b/".agentit/continuity-sync.json").stat().st_mode))
            self.assertFalse((a/"projects").exists())

    def test_cli_reconciles_on_checkpoint_and_cold_status(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            remote = self.setup_remote(root)
            a = self.make_project(root, "first")
            b = root / "second"
            b.mkdir()
            cli = Path(__file__).resolve().parents[1] / "agentit"

            def run(project, *args):
                call = subprocess.run(
                    [sys.executable, str(cli), "continuity", *args, "--project", str(project)],
                    capture_output=True, text=True, check=True,
                )
                return json.loads(call.stdout)

            planned = run(a, "link", str(remote), "shared")
            self.assertEqual("plan", planned["mode"])
            self.assertFalse((a / ".agentit/continuity-sync.json").exists())
            self.assertEqual("pushed", run(a, "link", str(remote), "shared", "--apply")["sync"]["status"])
            self.assertEqual("pulled", run(b, "link", str(remote), "shared", "--apply")["sync"]["status"])
            self.append(b, "Progress on new machine")
            self.assertEqual("pushed", run(b, "checkpoint", "done")["sync"]["status"])
            result = run(a, "status")
            self.assertEqual("pulled", result["sync"]["status"])
            self.assertIn("Progress on new machine", (a / ".agentit/STATE.md").read_text())
            self.assertEqual("offline", run(a, "status", "--offline")["sync"]["status"])

    def test_conflicting_edits_stop_without_overwriting(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            remote = self.setup_remote(root)
            a, b = self.make_project(root, "one"), self.make_project(root, "two")
            link_remote(a, str(remote), project_key="same")
            link_remote(b, str(remote), project_key="same")
            self.append(a, "A's change")
            self.append(b, "B's change")
            sync_state(a)
            before = (b/".agentit/STATE.md").read_bytes()
            with self.assertRaisesRegex(ContinuityError, "conflict"):
                sync_state(b)
            self.assertEqual(before, (b/".agentit/STATE.md").read_bytes())
            self.assertIn("A's change", (a/".agentit/STATE.md").read_text())

    def test_explicit_resolution_keeps_private_backups(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            remote = self.setup_remote(root)
            a, b = self.make_project(root, "one"), self.make_project(root, "two")
            link_remote(a, str(remote), project_key="same")
            link_remote(b, str(remote), project_key="same")
            self.append(a, "Remote choice")
            self.append(b, "Discarded local work")
            sync_state(a)
            pulled = sync_state(b, resolve="remote")
            self.assertEqual("resolved-pulled", pulled["status"])
            self.assertIn("Discarded local work", Path(pulled["backup"]).read_text())
            self.assertIn("Remote choice", (b/".agentit/STATE.md").read_text())
            self.append(a, "Discarded remote work")
            self.append(b, "Local choice")
            sync_state(a)
            pushed = sync_state(b, resolve="local")
            self.assertEqual("resolved-pushed", pushed["status"])
            self.assertIn("Discarded remote work", Path(pushed["backup"]).read_text())
            self.assertEqual("pulled", sync_state(a)["status"])
            self.assertIn("Local choice", (a/".agentit/STATE.md").read_text())

    def test_unlink_does_not_delete_state(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            remote = self.setup_remote(root)
            a = self.make_project(root, "laptop")
            link_remote(a, str(remote), project_key="same")
            self.assertEqual("unlinked", unlink_remote(a)["status"])
            self.assertTrue((a/".agentit/STATE.md").is_file())
            self.assertEqual("disabled", sync_state(a)["status"])

    def test_rejects_credential_and_unsafe_remote(self):
        for url in ("https://user:token@github.com/org/private.git", "http://github.com/org/private.git",
                    "ext::echo fail", "--upload-pack=evil", "file://remote/data"):
            with self.subTest(url=url), self.assertRaises(ContinuityError):
                _validate_remote(url)

    def test_empty_remote_without_state(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            remote = self.setup_remote(root)
            project = root / "empty-project"
            project.mkdir()
            result = link_remote(project, str(remote), project_key="empty")
            self.assertEqual("up-to-date", result["sync"]["status"])
            self.assertFalse((project/".agentit/STATE.md").exists())

    def test_public_project_git_must_ignore_private_state(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            remote = self.setup_remote(root)
            project = self.make_project(root, "git-project")
            self.git("init", str(project))
            with self.assertRaisesRegex(ContinuityError, "not ignored"):
                link_remote(project, str(remote), project_key="safe")
            (project / ".gitignore").write_text(".agentit/\n", encoding="utf-8")
            self.assertEqual("pushed", link_remote(project, str(remote), project_key="safe")["sync"]["status"])
            (project / ".gitignore").write_text("", encoding="utf-8")
            with self.assertRaisesRegex(ContinuityError, "not ignored"):
                sync_state(project)

    def test_origin_derives_same_key_for_https_and_ssh(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            a, b = root / "a", root / "b"
            for project, url in ((a, "https://github.com/Digitem-Tech/Natursun.git"), (b, "git@github.com:digitem-tech/natursun.git")):
                project.mkdir()
                self.git("init", str(project))
                self.git("-C", str(project), "remote", "add", "origin", url)
            self.assertEqual(_key_for_project(a), _key_for_project(b))


if __name__ == "__main__":
    unittest.main()
