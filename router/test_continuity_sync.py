"""Offline integration tests: two independent machines, one private bare Git remote."""

import json
import os
import stat
import sys
import subprocess
import tempfile
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest import mock

try:
    from .continuity import ContinuityError, ensure_state_file
    from .continuity_sync import link_remote, sync_state, unlink_remote, _validate_remote, _key_for_project
    from . import continuity_sync as transport
except ImportError:
    from continuity import ContinuityError, ensure_state_file
    from continuity_sync import link_remote, sync_state, unlink_remote, _validate_remote, _key_for_project
    import continuity_sync as transport


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
            previews = list((b / ".agentit/conflicts").glob("REMOTE-*.md"))
            self.assertEqual(1, len(previews))
            self.assertEqual((a / ".agentit/STATE.md").read_bytes(), previews[0].read_bytes())
            self.assertEqual(0o600, stat.S_IMODE(previews[0].stat().st_mode))

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

    def test_unlinked_sync_does_not_create_private_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.assertEqual("disabled", sync_state(root)["status"])
            self.assertFalse((root / ".agentit").exists())

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

    def test_github_transport_aliases_have_one_identity(self):
        root = Path(".")
        origin = "https://github.com/Org/Repo.git"
        base = transport._remote_identity(origin, root)
        for remote in (
            "https://github.com/Org/Repo.git/../Repo.git",
            "https://www.github.com/org/repo.git",
            "ssh://git@ssh.github.com:443/Org/Repo.git",
            "git@www.github.com:Org/Repo.git",
        ):
            self.assertEqual(base, transport._remote_identity(remote, root), remote)
        self.assertNotEqual(base, transport._remote_identity("https://www.github.com/Org/Other.git", root))
        with self.assertRaisesRegex(ContinuityError, "identify"):
            transport._remote_identity("https://github.com/../Org/Repo.git", root)

    def test_origin_derives_same_key_for_https_and_ssh(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            a, b = root / "a", root / "b"
            for project, url in ((a, "https://github.com/Digitem-Tech/Natursun.git"), (b, "git@github.com:digitem-tech/natursun.git")):
                project.mkdir()
                self.git("init", str(project))
                self.git("-C", str(project), "remote", "add", "origin", url)
            self.assertEqual(_key_for_project(a), _key_for_project(b))

    def git_project(self, root, name, origin):
        project = self.make_project(root, name)
        self.git("init", str(project))
        (project / ".gitignore").write_text(".agentit/\n", encoding="utf-8")
        self.git("-C", str(project), "remote", "add", "origin", origin)
        return project

    def test_rejects_project_origin_for_link_and_legacy_sync(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for index, (origin, remote) in enumerate((
                ("https://user:secret@github.com/Org/Repo.git", "git@github.com:org/repo.git"),
                ("git@github.com:Org/Repo.git", "https://github.com/org/repo"),
                ("https://github.com/Org/Repo.git", "https://github.com/Org/Repo.git/../Repo.git"),
                ("https://github.com/Org/Repo.git", "https://www.github.com/org/repo.git"),
                ("git@github.com:Org/Repo.git", "ssh://git@ssh.github.com:443/Org/Repo.git"),
                (str(root / "project.git"), (root / "project.git").as_uri()),
            )):
                with self.subTest(origin=origin):
                    project = self.git_project(root, f"project-{index}", origin)
                    with mock.patch.object(transport, "_git", wraps=transport._git) as call:
                        with self.assertRaisesRegex(ContinuityError, "separate"):
                            link_remote(project, remote, project_key="app")
                        self.assertFalse(any(args[0][0] == "ls-remote" and "--get-url" not in args[0] for args in call.call_args_list))
                    config_path = project / ".agentit/continuity-sync.json"
                    self.assertFalse(config_path.exists())
                    config_path.write_text(json.dumps({"schema_version": 1, "remote": remote, "project_key": "app", "last_sha256": None}))
                    with self.assertRaisesRegex(ContinuityError, "separate"):
                        sync_state(project)
                    self.assertTrue(config_path.exists())

    def test_git_url_rewrite_cannot_bypass_separate_remote_requirement(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            project = self.git_project(root, "project", "git@github.com:Org/Repo.git")
            self.git("-C", str(project), "config", "url.https://github.com/Org/.insteadOf", "https://alias.example/")
            with self.assertRaisesRegex(ContinuityError, "separate"):
                link_remote(project, "https://alias.example/Repo.git", project_key="app")

    def test_inherited_push_destinations_cannot_export_state_to_project_origin(self):
        for setting in ("pushInsteadOf", "pushurl", "multiple-pushurls"):
            with self.subTest(setting=setting), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                project_remote = root / "project.git"
                self.git("init", "--bare", "--initial-branch=main", str(project_remote))
                project = self.git_project(root, "project", str(project_remote))
                (project / "README.md").write_text("Project history\n")
                self.git("-C", str(project), "add", "README.md", ".gitignore")
                self.git("-C", str(project), "-c", "user.name=Test", "-c", "user.email=test@localhost", "commit", "-m", "Project history")
                self.git("-C", str(project), "push", "origin", "HEAD:main")
                remote = root / "private.git"
                self.git("clone", "--bare", str(project_remote), str(remote))
                original_head = self.git("--git-dir", str(project_remote), "rev-parse", "HEAD")
                config = root / "gitconfig"
                if setting == "pushInsteadOf":
                    self.git("config", "--file", str(config), f"url.{project_remote}.pushInsteadOf", str(remote))
                else:
                    if setting == "multiple-pushurls":
                        self.git("config", "--file", str(config), "--add", "remote.origin.pushurl", str(remote))
                    self.git("config", "--file", str(config), "--add", "remote.origin.pushurl", str(project_remote))
                before = (project / ".agentit/STATE.md").read_bytes()
                with mock.patch.dict(os.environ, {"GIT_CONFIG_GLOBAL": str(config)}):
                    with self.assertRaisesRegex(ContinuityError, "push destination"):
                        link_remote(project, str(remote), project_key="same")
                config_path = project / ".agentit/continuity-sync.json"
                self.assertFalse(config_path.exists())
                self.assertEqual(before, (project / ".agentit/STATE.md").read_bytes())
                # Legacy links receive exactly the same transport guard.
                config_path.write_text(json.dumps({"schema_version": 1, "remote": str(remote), "project_key": "same", "last_sha256": None}))
                with mock.patch.dict(os.environ, {"GIT_CONFIG_GLOBAL": str(config)}):
                    with self.assertRaisesRegex(ContinuityError, "push destination"):
                        sync_state(project)
                self.assertEqual(original_head, self.git("--git-dir", str(project_remote), "rev-parse", "HEAD"))
                self.assertEqual(original_head, self.git("--git-dir", str(remote), "rev-parse", "HEAD"))
                self.assertEqual("", self.git("--git-dir", str(project_remote), "ls-tree", "HEAD", "--", "projects/same/STATE.md"))

    def test_project_keys_preserve_case_on_other_hosts(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            a = self.git_project(root, "a", "ssh://git@example.test/Org/Repo.git")
            b = self.git_project(root, "b", "https://example.test/org/repo.git")
            self.assertNotEqual(_key_for_project(a), _key_for_project(b))
            self.git("-C", str(b), "remote", "set-url", "origin", "https://example.test/Org/Repo.git")
            self.assertEqual(_key_for_project(a), _key_for_project(b))

    def test_file_remote_and_symlink_have_same_identity(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            remote = self.setup_remote(root)
            alias = root / "alias.git"
            alias.symlink_to(remote, target_is_directory=True)
            project = self.git_project(root, "project", str(alias))
            with self.assertRaisesRegex(ContinuityError, "separate"):
                link_remote(project, remote.as_uri(), project_key="app")

    def test_failed_initial_link_does_not_enable_future_sync(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            remote = self.setup_remote(root)
            a = self.make_project(root, "a", goal="Machine A")
            b = self.make_project(root, "b", goal="Different machine B")
            link_remote(a, str(remote), project_key="same")
            before = (b / ".agentit/STATE.md").read_bytes()
            with self.assertRaisesRegex(ContinuityError, "conflict"):
                link_remote(b, str(remote), project_key="same")
            self.assertFalse((b / ".agentit/continuity-sync.json").exists())
            self.assertEqual(before, (b / ".agentit/STATE.md").read_bytes())
            self.assertEqual("disabled", sync_state(b)["status"])

    def test_transport_never_runs_inherited_hooks(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            remote = self.setup_remote(root)
            project = self.make_project(root, "project")
            hooks = root / "hooks"
            hooks.mkdir()
            sentinel = root / "hook-executed"
            for hook_name in ("pre-commit", "post-checkout", "pre-push"):
                hook = hooks / hook_name
                hook.write_text(f"#!/bin/sh\ntouch '{sentinel}'\nexit 1\n")
                hook.chmod(0o700)
            config = root / "gitconfig"
            config.write_text(f"[core]\n\thooksPath = {hooks}\n")
            with mock.patch.dict(os.environ, {"GIT_CONFIG_GLOBAL": str(config)}):
                self.assertEqual("pushed", link_remote(project, str(remote), project_key="same")["sync"]["status"])
                self.append(project, "Next checkpoint")
                self.assertEqual("pushed", sync_state(project)["status"])
            self.assertFalse(sentinel.exists())

    def test_remote_attributes_cannot_execute_host_filters(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            remote = self.setup_remote(root)
            a = self.make_project(root, "first")
            link_remote(a, str(remote), project_key="same")
            seed = root / "seed"
            self.git("clone", str(remote), str(seed))
            attributes = "** filter=sentinel\n"
            (seed / ".gitattributes").write_text(attributes)
            (seed / "unrelated.txt").write_text("Preserve this remote file\n")
            self.git("-C", str(seed), "add", ".gitattributes", "unrelated.txt")
            self.git("-C", str(seed), "-c", "user.name=Test", "-c", "user.email=test@localhost", "commit", "-m", "Seed remote attributes")
            self.git("-C", str(seed), "push", "origin", "HEAD")
            sentinel = root / "filter-executed"
            config = root / "gitconfig"
            command = f"sh -c 'touch {sentinel}; cat'"
            for direction in ("clean", "smudge"):
                self.git("config", "--file", str(config), f"filter.sentinel.{direction}", command)
            b = root / "second"
            b.mkdir()
            redirects = {name: str(root / "invalid-git-context") for name in (
                "GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
                "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR", "GIT_PREFIX")}
            with mock.patch.dict(os.environ, {"GIT_CONFIG_GLOBAL": str(config), **redirects}):
                self.assertEqual("pulled", link_remote(b, str(remote), project_key="same")["sync"]["status"])
                self.append(b, "Synced without filters")
                self.assertEqual("pushed", sync_state(b)["status"])
            self.assertFalse(sentinel.exists())
            self.assertEqual(attributes.strip(), self.git("--git-dir", str(remote), "show", "HEAD:.gitattributes"))
            self.assertEqual("Preserve this remote file", self.git("--git-dir", str(remote), "show", "HEAD:unrelated.txt"))
            self.assertIn("Synced without filters", self.git("--git-dir", str(remote), "show", "HEAD:projects/same/STATE.md"))

    def test_link_and_unlink_wait_for_active_sync(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            remote = self.setup_remote(root)
            project = self.make_project(root, "project")
            link_remote(project, str(remote), project_key="same")
            original_sync = transport._sync_locked
            for operation in ("link", "unlink"):
                with self.subTest(operation=operation):
                    entered, release, finished = threading.Event(), threading.Event(), threading.Event()
                    outcomes = []

                    def held_sync(*args, **kwargs):
                        entered.set()
                        if not release.wait(5):
                            raise RuntimeError("test sync was never released")
                        return original_sync(*args, **kwargs)

                    def contender():
                        try:
                            if operation == "link":
                                link_remote(project, str(remote), project_key="other")
                            else:
                                unlink_remote(project)
                        except ContinuityError as exc:
                            outcomes.append(str(exc))
                        finally:
                            finished.set()

                    with mock.patch.object(transport, "_sync_locked", side_effect=held_sync):
                        with ThreadPoolExecutor(max_workers=2) as executor:
                            active = executor.submit(sync_state, project)
                            self.assertTrue(entered.wait(5))
                            pending = executor.submit(contender)
                            try:
                                self.assertFalse(finished.wait(0.1))
                            finally:
                                release.set()
                            active.result(timeout=5)
                            pending.result(timeout=5)
                    if operation == "link":
                        self.assertEqual(1, len(outcomes))
                        self.assertEqual("same", json.loads((project / ".agentit/continuity-sync.json").read_text())["project_key"])
                    else:
                        self.assertFalse((project / ".agentit/continuity-sync.json").exists())


if __name__ == "__main__":
    unittest.main()
