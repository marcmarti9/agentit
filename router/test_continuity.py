import os
import stat
import subprocess
import tempfile
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest import mock

try:
    from .continuity import ContinuityError, _atomic_write_text, default_state_markdown, ensure_state_file, list_checkpoints, parse_state, resume_report, write_checkpoint
    from .project_signals import collect_project_signals
    from .verify import evaluate_done_claims
except ImportError:
    from continuity import ContinuityError, _atomic_write_text, default_state_markdown, ensure_state_file, list_checkpoints, parse_state, resume_report, write_checkpoint
    from project_signals import collect_project_signals
    from verify import evaluate_done_claims


class ContinuityAndProjectSignalTests(unittest.TestCase):
    def test_state_init_and_resume(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = ensure_state_file(root, goal="Ship continuity")
            self.assertEqual(root / ".agentit" / "STATE.md", path)
            self.assertTrue(path.is_file())
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)
            self.assertTrue(parse_state(path)["complete"])
            self.assertTrue(resume_report(root)["resumable"])
            self.assertFalse(resume_report(root)["cross_machine_verified"])
            self.assertEqual("local-state-structure", resume_report(root)["verification_scope"])

    def test_state_init_does_not_invent_semantic_defaults(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            body = ensure_state_file(root, goal="Sensitive task not yet decided").read_text(encoding="utf-8")
            for value in ("- Relevant packs: (unset)", "- Complexity: (unset)", "- Risk: (unset)", "- Topology: (unset)", "- Strong independent review required: (unset)"):
                self.assertIn(value, body)
            self.assertNotIn("- Topology: direct", body)

    def test_state_init_persists_explicit_ai_decision_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            body = ensure_state_file(root, goal="Implement auth boundary", decision={"relevant_packs": ["backend", "engineering"], "complexity": "substantial", "risk": "RISK_3", "topology": "writer_reviewer", "strong_review_required": True}).read_text(encoding="utf-8")
            self.assertIn("- Relevant packs: backend, engineering", body)
            self.assertIn("- Complexity: substantial", body)
            self.assertIn("- Risk: RISK_3", body)
            self.assertIn("- Topology: writer_reviewer", body)
            self.assertIn("- Strong independent review required: yes", body)

    def test_checkpoint_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = write_checkpoint(root, label="milestone", payload={"x": 1})
            self.assertTrue(path.is_file())
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)
            self.assertEqual(1, len(list_checkpoints(root)))

    def test_project_signals_detect_python_repo(self):
        signals = collect_project_signals(Path(__file__).resolve().parents[1])
        self.assertTrue(signals["available"])
        self.assertIn(signals["size_class"], {"tiny", "small", "medium", "large"})
        self.assertIn("python", signals["stack_markers"])

    def test_evaluate_done_claims_requires_receipt(self):
        denied = evaluate_done_claims(["done"], receipt=None)
        self.assertTrue(denied["applicable"])
        self.assertFalse(denied["allowed"])
        allowed = evaluate_done_claims(["done"], receipt={"mode": "apply", "passed": True, "blocking_failed": False, "receipt_path": "/tmp/r.json", "created_at": "now", "pending_checklists": []})
        self.assertTrue(allowed["allowed"])


class PrivateGitContinuityTests(unittest.TestCase):
    def git(self, root, *args):
        return subprocess.run(["git", "-C", str(root), *args], capture_output=True, check=True).stdout

    def init(self, root):
        self.git(root, "init", "-q")

    def test_fresh_private_state_and_checkpoints_cannot_be_accidentally_added(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init(root)
            ignore = root / ".gitignore"
            ignore.write_bytes(b"# Existing project policy\n")
            self.git(root, "add", ".gitignore")
            exclude = root / ".git/info/exclude"
            exclude.write_bytes(b"# Existing local policy without final newline")
            state = ensure_state_file(root, goal="private")
            checkpoint = write_checkpoint(root, label="safe", payload={"private": "context"})
            first_exclusion = exclude.read_bytes()
            ensure_state_file(root)
            self.assertEqual(first_exclusion, exclude.read_bytes())
            self.assertTrue(first_exclusion.startswith(b"# Existing local policy without final newline\n"))
            self.assertEqual(b"# Existing project policy\n", ignore.read_bytes())
            self.git(root, "check-ignore", str(state), str(checkpoint))
            self.git(root, "add", ".")
            self.assertEqual(b".gitignore\n", self.git(root, "ls-files"))
            self.assertTrue(resume_report(root)["resumable"])

    def test_reads_of_empty_project_do_not_create_private_files_or_exclusions(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init(root)
            exclude = root / ".git/info/exclude"
            before = exclude.read_bytes()
            self.assertFalse(resume_report(root)["resumable"])
            self.assertEqual([], list_checkpoints(root))
            self.assertFalse((root / ".agentit").exists())
            self.assertEqual(before, exclude.read_bytes())

    def test_existing_unignored_state_is_preserved_and_reads_do_not_repair_git(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init(root)
            state = root / ".agentit/STATE.md"
            state.parent.mkdir()
            state.write_text(default_state_markdown(goal="existing"))
            original = state.read_bytes()
            exclude = root / ".git/info/exclude"
            before = exclude.read_bytes()
            with self.assertRaisesRegex(ContinuityError, "not ignored"):
                parse_state(state)
            with self.assertRaisesRegex(ContinuityError, "not ignored"):
                resume_report(root)
            self.assertEqual(before, exclude.read_bytes())
            self.assertEqual(state, ensure_state_file(root))
            self.assertEqual(original, state.read_bytes())
            self.assertTrue(parse_state(state)["complete"])

    def test_tracked_private_content_rejects_every_entrypoint_without_changes(self):
        for tracked in ("STATE.md", "checkpoints/prior.json", "continuity-sync.json"):
            with self.subTest(tracked=tracked), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                self.init(root)
                state = root / ".agentit/STATE.md"
                state.parent.mkdir()
                state.write_text(default_state_markdown(goal="preserve"))
                target = state.parent / tracked
                target.parent.mkdir(exist_ok=True)
                if target != state:
                    target.write_bytes(b"private prior bytes")
                self.git(root, "add", str(target))
                exclude = root / ".git/info/exclude"
                before_exclude = exclude.read_bytes()
                before = {p: p.read_bytes() for p in state.parent.rglob("*") if p.is_file()}
                for action in (lambda: ensure_state_file(root), lambda: ensure_state_file(root, overwrite=True),
                               lambda: write_checkpoint(root, label="blocked", payload={}),
                               lambda: parse_state(state), lambda: resume_report(root),
                               lambda: _atomic_write_text(state.parent / "new.json", "private", private=True)):
                    with self.assertRaisesRegex(ContinuityError, "tracked"):
                        action()
                    self.assertEqual(before_exclude, exclude.read_bytes())
                    self.assertEqual(before, {p: p.read_bytes() for p in state.parent.rglob("*") if p.is_file()})

    def test_subdirectory_with_gitignore_metacharacters_uses_literal_exclusion(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init(root)
            project = root / "client [one]* space"
            project.mkdir()
            state = ensure_state_file(project)
            checkpoint = write_checkpoint(project, label="local", payload={})
            self.git(root, "check-ignore", str(state), str(checkpoint))
            sibling = root / "client o space"
            sibling.mkdir()
            (sibling / ".agentit").mkdir()
            (sibling / ".agentit/STATE.md").write_text("other project")
            self.git(root, "add", ".")
            self.assertEqual(b"client o space/.agentit/STATE.md\n", self.git(root, "ls-files"))

    def test_linked_worktree_resolves_local_git_exclude(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            root = base / "main"
            root.mkdir()
            self.init(root)
            self.git(root, "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "--allow-empty", "-qm", "initial")
            worktree = base / "linked"
            self.git(root, "worktree", "add", "--detach", str(worktree))
            state = ensure_state_file(worktree)
            self.git(worktree, "check-ignore", str(state))
            self.git(worktree, "add", ".")
            self.assertEqual(b"", self.git(worktree, "ls-files"))
            self.assertFalse((worktree / ".gitignore").exists())

    def test_override_of_local_exclusion_rejects_before_private_writes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init(root)
            (root / ".gitignore").write_text("!.agentit/\n")
            self.git(root, "add", ".gitignore")
            exclude = root / ".git/info/exclude"
            before = exclude.read_bytes()
            with self.assertRaisesRegex(ContinuityError, "override"):
                ensure_state_file(root)
            self.assertFalse((root / ".agentit").exists())
            self.assertEqual(before + b"/.agentit/\n", exclude.read_bytes())

    def test_failed_init_preserves_concurrent_project_exclusion(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init(root)
            blocked, protected = root / "blocked", root / "protected"
            blocked.mkdir()
            protected.mkdir()
            (blocked / ".gitignore").write_text("!.agentit/\n")
            self.git(root, "add", "blocked/.gitignore")
            appended = threading.Event()
            resume = threading.Event()
            checks = 0
            real_git = ensure_state_file.__globals__["_local_git"]

            def pause_after_append(project, *args):
                nonlocal checks
                if args[:1] == ("check-ignore",) and args[-1] == "blocked/.agentit/":
                    checks += 1
                    if checks == 2:
                        appended.set()
                        if not resume.wait(timeout=5):
                            raise AssertionError("Concurrent project did not finish initialization")
                return real_git(project, *args)

            with mock.patch(f"{ensure_state_file.__module__}._local_git", side_effect=pause_after_append):
                with ThreadPoolExecutor(max_workers=1) as executor:
                    failed = executor.submit(ensure_state_file, blocked)
                    try:
                        self.assertTrue(appended.wait(timeout=5), "Blocked init did not append its exclusion")
                        state = ensure_state_file(protected, goal="Keep private")
                        before = state.read_bytes()
                    finally:
                        resume.set()
                    with self.assertRaisesRegex(ContinuityError, "override"):
                        failed.result(timeout=5)
            self.assertFalse((blocked / ".agentit").exists())
            self.assertEqual(before, state.read_bytes())
            self.git(root, "check-ignore", str(state))
            self.git(root, "add", ".")
            self.assertEqual(b"blocked/.gitignore\n", self.git(root, "ls-files"))

    def test_global_config_override_uses_callers_actual_ignore_rules(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            root = base / "project"
            root.mkdir()
            self.init(root)
            xdg = base / "xdg"
            (xdg / "git").mkdir(parents=True)
            ignored = base / "default-ignore"
            ignored.write_text(".agentit/\n")
            (xdg / "git/config").write_text(f"[core]\n\texcludesFile = {ignored}\n")
            caller = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
            caller.update(XDG_CONFIG_HOME=str(xdg), GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1")
            with mock.patch.dict(os.environ, caller, clear=True):
                state = ensure_state_file(root, goal="Global config override")
                self.git(root, "check-ignore", str(state))
                self.git(root, "add", ".")
                self.assertEqual(b"", self.git(root, "ls-files"))
                self.assertIn(b"/.agentit/\n", (root / ".git/info/exclude").read_bytes())

    def test_config_count_override_uses_callers_actual_ignore_rules(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            root = base / "project"
            root.mkdir()
            self.init(root)
            ignored = base / "configured-ignore"
            ignored.write_text(".agentit/\n")
            self.git(root, "config", "core.excludesFile", str(ignored))
            caller = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
            caller.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_COUNT="1",
                          GIT_CONFIG_KEY_0="core.excludesFile", GIT_CONFIG_VALUE_0=os.devnull)
            with mock.patch.dict(os.environ, caller, clear=True):
                state = ensure_state_file(root, goal="Per-process config override")
                self.git(root, "check-ignore", str(state))
                self.git(root, "add", ".")
                self.assertEqual(b"", self.git(root, "ls-files"))
                self.assertIn(b"/.agentit/\n", (root / ".git/info/exclude").read_bytes())

    def test_repository_redirect_environment_cannot_change_privacy_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            root, other = base / "project", base / "other"
            root.mkdir()
            other.mkdir()
            self.init(root)
            self.init(other)
            before = (other / ".git/info/exclude").read_bytes()
            caller = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
            caller.update(GIT_DIR=str(other / ".git"), GIT_WORK_TREE=str(other),
                          GIT_INDEX_FILE=str(other / ".git/index"), GIT_OBJECT_DIRECTORY=str(other / ".git/objects"),
                          GIT_ALTERNATE_OBJECT_DIRECTORIES=str(other / ".git/objects"),
                          GIT_COMMON_DIR=str(other / ".git"), GIT_PREFIX="other/",
                          GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1")
            with mock.patch.dict(os.environ, caller, clear=True):
                state = ensure_state_file(root, goal="Actual project")
            self.assertEqual(before, (other / ".git/info/exclude").read_bytes())
            self.assertFalse((other / ".agentit").exists())
            self.git(root, "check-ignore", str(state))
            self.git(root, "add", ".")
            self.assertEqual(b"", self.git(root, "ls-files"))

    def test_symlinked_private_paths_reject_and_preserve_targets(self):
        for relative in (".agentit", ".agentit/STATE.md", ".agentit/checkpoints", ".git/info/exclude"):
            with self.subTest(relative=relative), tempfile.TemporaryDirectory() as tmp:
                base = Path(tmp)
                root = base / "project"
                root.mkdir()
                self.init(root)
                target = base / "outside"
                directory = relative in (".agentit", ".agentit/checkpoints")
                if directory:
                    target.mkdir()
                    protected = target / "keep.txt"
                else:
                    protected = target
                protected.write_bytes(b"preserve outside")
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.unlink(missing_ok=True)
                path.symlink_to(target, target_is_directory=directory)
                with self.assertRaisesRegex(ContinuityError, "symlink"):
                    ensure_state_file(root, overwrite=True)
                with self.assertRaisesRegex(ContinuityError, "symlink"):
                    write_checkpoint(root, label="blocked", payload={})
                self.assertEqual(b"preserve outside", protected.read_bytes())

    def test_deliberately_tracked_canonical_document_remains_readable(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init(root)
            canonical = root / "docs/STATE.md"
            canonical.parent.mkdir()
            canonical.write_text(default_state_markdown(goal="public handoff"))
            before = canonical.read_bytes()
            self.git(root, "add", "docs/STATE.md")
            self.assertTrue(parse_state(canonical)["complete"])
            self.assertEqual(before, canonical.read_bytes())

    def test_broken_git_marker_does_not_fall_back_to_non_git(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".git").write_text("gitdir: missing-directory\n")
            with self.assertRaisesRegex(ContinuityError, "Cannot verify project Git"):
                ensure_state_file(root)
            self.assertFalse((root / ".agentit").exists())

    def test_git_unavailable_preserves_non_git_but_refuses_a_git_project(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with mock.patch(f"{ensure_state_file.__module__}.shutil.which", return_value=None):
                self.assertTrue(ensure_state_file(root).is_file())
                self.assertTrue(resume_report(root)["resumable"])
                self.assertTrue(write_checkpoint(root, label="non-git", payload={}).is_file())
            self.init(root)
            before = (root / ".agentit/STATE.md").read_bytes()
            with mock.patch(f"{ensure_state_file.__module__}.shutil.which", return_value=None):
                with self.assertRaisesRegex(ContinuityError, "Git is unavailable"):
                    ensure_state_file(root, overwrite=True)
            self.assertEqual(before, (root / ".agentit/STATE.md").read_bytes())

    def test_root_and_checkpoint_file_symlinks_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            root = base / "project"
            root.mkdir()
            alias = base / "alias"
            alias.symlink_to(root, target_is_directory=True)
            with self.assertRaisesRegex(ContinuityError, "symlink"):
                ensure_state_file(alias)
            self.assertFalse((root / ".agentit").exists())
            state = ensure_state_file(root)
            checkpoints = root / ".agentit/checkpoints"
            checkpoints.mkdir()
            (checkpoints / "linked.json").symlink_to(state)
            with self.assertRaisesRegex(ContinuityError, "symlink"):
                list_checkpoints(root)


if __name__ == "__main__":
    unittest.main()
