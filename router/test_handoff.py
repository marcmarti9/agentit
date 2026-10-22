"""Actual Git clone round trips and untrusted-package boundaries."""
import hashlib
import json
from pathlib import Path
import shutil
import stat
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from router import handoff
from router.continuity import default_state_markdown


class HandoffTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.origin = self.base / "origin.git"
        self.git(self.base, "init", "--bare", str(self.origin))
        self.source = self.base / "machine-one"
        self.git(self.base, "clone", str(self.origin), str(self.source))
        (self.source / ".gitignore").write_text(".agentit/\n")
        (self.source / "code.txt").write_text("actual Git code\n")
        (self.source / "proof.md").write_text("Verified local milestone.\n")
        self.git(self.source, "add", ".")
        self.git(self.source, "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "fixture")
        self.git(self.source, "push", "origin", "HEAD")
        self.dest = self.base / "different" / "machine-two"
        self.dest.parent.mkdir()
        self.git(self.base, "clone", str(self.origin), str(self.dest))
        (self.source / ".agentit").mkdir()
        self.state = default_state_markdown(goal="Resume portable task").replace("## Next actions\n1.", "## Next actions\n1. Verify the transferred milestone and continue implementation.").encode()
        (self.source / ".agentit/STATE.md").write_bytes(self.state)
        self.harness = self.base / "harness"
        for name in (*handoff.CORE_IDS, "focused-skill"):
            directory = self.harness / "skills" / name
            directory.mkdir(parents=True)
            (directory / "SKILL.md").write_text(f"# {name}\nExact fixture body.\n")
        (self.harness / "profiles.yaml").write_text(json.dumps({"schema_version": 1, "default_profile": "core", "global_profiles": ["core"], "profiles": {"core": {"skills": list(handoff.CORE_IDS)}, "engineering": {"extends": ["core"], "skills": ["focused-skill"]}}}))
        self.package = self.base / "private-transfer"

    @staticmethod
    def git(root, *args):
        return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, check=True).stdout.strip()

    def prepare(self, **kwargs):
        return handoff.prepare_handoff(self.source, self.package, harness_root=self.harness, profile_ids=("engineering",), skill_ids=("focused-skill",), artifact_paths=("proof.md",), **kwargs)

    def resume(self, **kwargs):
        return handoff.resume_handoff(self.dest, self.package, harness_root=self.harness, **kwargs)

    def export(self):
        result = self.prepare(apply=True)
        self.assertTrue(result["ready"], result)
        self.assertTrue(result["applied"])
        return result

    def edit_manifest(self, edit):
        path = self.package / "manifest.json"
        manifest = json.loads(path.read_bytes())
        edit(manifest)
        path.write_text(json.dumps(manifest))

    def assert_blocked_unchanged(self, **kwargs):
        target = self.dest / ".agentit/STATE.md"
        before = target.read_bytes() if target.exists() else None
        result = self.resume(apply=True, **kwargs)
        self.assertFalse(result["ready"], result)
        self.assertFalse(result["applied"])
        self.assertEqual(before, target.read_bytes() if target.exists() else None)
        return result

    def test_two_actual_clone_roots_preview_copy_apply_and_idempotence(self):
        preview = self.prepare()
        self.assertTrue(preview["ready"], preview)
        self.assertFalse(self.package.exists())
        exported = self.export()
        moved = self.base / "destination-transfer"
        shutil.copytree(self.package, moved)
        self.package = moved
        preview = self.resume()
        self.assertTrue(preview["ready"], preview)
        self.assertFalse((self.dest / ".agentit").exists())
        result = self.resume(apply=True)
        self.assertTrue(result["ready"], result)
        self.assertEqual((self.dest / ".agentit/STATE.md").read_bytes(), self.state)
        received = Path(result["received_path"])
        self.assertEqual((received / "artifacts/proof.md").read_text(), "Verified local milestone.\n")
        self.assertEqual((self.dest / "proof.md").read_text(), "Verified local milestone.\n")
        self.assertTrue(self.resume(apply=True)["ready"])
        self.assertFalse(self.resume(apply=True)["state_changed"])
        for path in moved.rglob("*"):
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o700 if path.is_dir() else 0o600)
        metadata = json.dumps(exported["manifest"])
        self.assertNotIn(str(self.source), metadata)
        self.assertNotIn("Exact fixture body", metadata)
        self.assertIn("fresh host task decision", result["warning"])

    def test_wrong_commit_wrong_project_and_dirty_destination(self):
        self.export()
        (self.dest / "code.txt").write_text("other commit")
        self.git(self.dest, "add", ".")
        self.git(self.dest, "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "new")
        self.assertIn("commit mismatch", self.assert_blocked_unchanged()["blockers"][0])
        self.git(self.dest, "reset", "--hard", "HEAD~1")
        self.git(self.dest, "remote", "set-url", "origin", "https://example.invalid/wrong.git")
        self.assertIn("Wrong Git project", self.assert_blocked_unchanged()["blockers"][0])
        self.git(self.dest, "remote", "set-url", "origin", str(self.origin))
        (self.dest / "untracked.py").write_text("untracked")
        self.assertIn("modified or untracked", self.assert_blocked_unchanged()["blockers"][0])

    def test_dirty_source_tracked_and_untracked(self):
        for path in (self.source / "code.txt", self.source / "new.py"):
            previous = path.read_bytes() if path.exists() else None
            path.write_text("dirty")
            result = self.prepare(apply=True)
            self.assertFalse(result["ready"])
            self.assertIn("commit and publish", result["blockers"][0])
            self.assertFalse(self.package.exists())
            path.unlink() if previous is None else path.write_bytes(previous)

    def test_stale_core_selected_and_profile_resolution(self):
        self.export()
        for name in (handoff.CORE_IDS[0], "focused-skill"):
            path = self.harness / "skills" / name / "SKILL.md"
            before = path.read_bytes()
            path.write_text("Changed body")
            self.assertIn("missing/stale", self.assert_blocked_unchanged()["blockers"][0])
            path.write_bytes(before)
        self.edit_manifest(lambda m: m["selection"]["profile_resolutions"]["engineering"].append("invented"))
        self.assertIn("missing/stale", self.assert_blocked_unchanged()["blockers"][0])

    def test_missing_selected_skill(self):
        self.export()
        (self.harness / "skills/focused-skill/SKILL.md").unlink()
        self.assert_blocked_unchanged()

    def test_corrupt_missing_file_and_schema(self):
        self.export()
        artifact = self.package / "artifacts/proof.md"
        before = artifact.read_bytes()
        artifact.write_text("tampered")
        self.assert_blocked_unchanged()
        artifact.unlink()
        self.assert_blocked_unchanged()
        artifact.write_bytes(before)
        self.edit_manifest(lambda m: m.update(schema_version=99))
        self.assertIn("Unsupported", self.assert_blocked_unchanged()["blockers"][0])

    def test_source_destination_and_package_symlinks(self):
        state = self.source / ".agentit/STATE.md"
        state.unlink()
        external = self.base / "state.md"
        external.write_bytes(self.state)
        state.symlink_to(external)
        self.assertFalse(self.prepare(apply=True)["ready"])
        state.unlink()
        state.write_bytes(self.state)
        self.export()
        (self.dest / ".agentit").symlink_to(self.source / ".agentit", target_is_directory=True)
        self.assert_blocked_unchanged()
        (self.dest / ".agentit").unlink()
        artifact = self.package / "artifacts/proof.md"
        artifact.unlink()
        artifact.symlink_to(self.source / "proof.md")
        self.assert_blocked_unchanged()

    def test_project_root_and_output_ancestor_symlink(self):
        alias = self.base / "alias"
        alias.symlink_to(self.source, target_is_directory=True)
        self.assertFalse(handoff.prepare_handoff(alias, self.package, harness_root=self.harness)["ready"])
        directory = self.base / "elsewhere"
        directory.mkdir()
        link = self.base / "output-link"
        link.symlink_to(directory, target_is_directory=True)
        self.assertFalse(handoff.prepare_handoff(self.source, link / "capsule", harness_root=self.harness, apply=True)["ready"])
        self.assertEqual(list(directory.iterdir()), [])

    def test_secret_state_and_forbidden_artifact_paths_without_echo(self):
        secret = "sk-" + "a" * 32
        (self.source / ".agentit/STATE.md").write_bytes(self.state + secret.encode())
        result = self.prepare(apply=True)
        self.assertFalse(result["ready"])
        self.assertNotIn(secret, json.dumps(result))
        (self.source / ".agentit/STATE.md").write_bytes(self.state)
        for name in ("../outside.md", ".env", ".git/config", "credentials.json", "store.sqlite", ".agentit/providers.json", "transcript.txt", "skills/example/SKILL.md", ".agentit/skills-manifest.json", "database.json", "private-key.json"):
            result = handoff.prepare_handoff(self.source, self.package, artifact_paths=(name,), harness_root=self.harness, apply=True)
            self.assertFalse(result["ready"], name)
        self.assertFalse(self.package.exists())

    def test_secret_artifact_and_incomplete_state(self):
        artifact = self.source / ".agentit/artifacts/receipt.txt"
        artifact.parent.mkdir()
        artifact.write_text("password=supersecretvalue")
        result = handoff.prepare_handoff(self.source, self.package, artifact_paths=(".agentit/artifacts/receipt.txt",), harness_root=self.harness)
        self.assertFalse(result["ready"])
        (self.source / ".agentit/STATE.md").write_text("# partial")
        self.assertFalse(self.prepare()["ready"])

    def test_traversal_and_unexpected_file(self):
        self.export()
        self.edit_manifest(lambda m: m["artifacts"][0].update(source="../outside.md", path="artifacts/../outside.md"))
        self.assert_blocked_unchanged()
        shutil.rmtree(self.package)
        self.export()
        (self.package / "payload.py").write_text("raise Exception('never executed')")
        self.assert_blocked_unchanged()

    def test_conflict_backup_and_idempotence_validate_actual_content(self):
        self.export()
        (self.dest / ".agentit").mkdir()
        previous = default_state_markdown(goal="Other local task").encode()
        target = self.dest / ".agentit/STATE.md"
        target.write_bytes(previous)
        self.assertIn("replace_state", self.assert_blocked_unchanged()["blockers"][0])
        result = self.resume(apply=True, replace_state=True)
        self.assertTrue(result["ready"], result)
        self.assertEqual(Path(result["backup_path"]).read_bytes(), previous)
        self.assertEqual(target.read_bytes(), self.state)
        self.assertTrue(self.resume(apply=True)["ready"])
        received = Path(result["received_path"]) / "artifacts/proof.md"
        received.write_text("changed after receipt")
        self.assert_blocked_unchanged()

    def test_retains_exact_manifest_without_transfer_media_and_validates_repeat(self):
        self.export()
        original = (self.package / "manifest.json").read_bytes()
        result = self.resume(apply=True)
        self.assertTrue(result["ready"], result)
        retained = Path(result["received_path"]) / "handoff-manifest.json"
        self.assertEqual(retained.read_bytes(), original)
        self.assertEqual(stat.S_IMODE(retained.stat().st_mode), 0o600)
        metadata = json.loads(retained.read_bytes())
        self.assertEqual(metadata["project"]["head"], self.git(self.dest, "rev-parse", "HEAD"))
        self.assertEqual(metadata["selection"]["skills"]["focused-skill"]["sha256"], hashlib.sha256((self.harness / "skills/focused-skill/SKILL.md").read_bytes()).hexdigest())
        self.assertEqual(set(metadata["selection"]["core"]), set(handoff.CORE_IDS))
        # A later session retains exact evidence even after the USB copy leaves.
        saved = self.base / "saved-transfer"
        shutil.copytree(self.package, saved)
        shutil.rmtree(self.package)
        self.assertEqual(retained.read_bytes(), original)
        self.package = saved
        retained.write_bytes(original + b"\n")
        self.assert_blocked_unchanged()

    def test_existing_export_refused_and_state_must_be_ignored(self):
        self.export()
        self.assertFalse(self.prepare(apply=True)["ready"])
        (self.dest / ".gitignore").write_text("")
        self.git(self.dest, "add", ".gitignore")
        self.git(self.dest, "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "unignore")
        self.assert_blocked_unchanged()

    def test_size_count_and_symlink_selected_skill(self):
        result = handoff.prepare_handoff(self.source, self.package, artifact_paths=tuple("proof.md" for _ in range(33)), harness_root=self.harness)
        self.assertFalse(result["ready"])
        path = self.harness / "skills/focused-skill/SKILL.md"
        path.unlink()
        path.symlink_to(self.harness / "skills" / handoff.CORE_IDS[0] / "SKILL.md")
        self.assertFalse(self.prepare()["ready"])
        path.unlink()
        path.write_bytes(b"x" * (handoff.MAX_FILE_BYTES + 1))
        self.assertFalse(self.prepare()["ready"])

    def test_normalized_origin_does_not_serialize_embedded_credentials(self):
        self.git(self.source, "remote", "set-url", "origin", "https://someone:privatevalue@example.invalid/org/project.git?token=privatequery")
        self.git(self.dest, "remote", "set-url", "origin", "git@example.invalid:org/project.git")
        result = self.export()
        self.assertNotIn("privatevalue", json.dumps(result))
        self.assertNotIn("privatequery", json.dumps(result))
        self.assertTrue(self.resume(apply=True)["ready"])

    def test_package_total_size_limit_and_source_artifact_symlink(self):
        # Use the real small-file path while lowering the aggregate bound to
        # exercise the package budget without creating large test fixtures.
        with patch.object(handoff, "MAX_TOTAL_BYTES", len(self.state) + 10):
            self.assertFalse(self.prepare(apply=True)["ready"])
        external = self.base / "artifact.md"
        external.write_text("External evidence")
        path = self.source / ".agentit/artifacts/proof.md"
        path.parent.mkdir()
        path.symlink_to(external)
        result = handoff.prepare_handoff(self.source, self.package, artifact_paths=(".agentit/artifacts/proof.md",), harness_root=self.harness)
        self.assertFalse(result["ready"])

    def test_unignored_received_path_exception_blocks_before_restore(self):
        self.export()
        # Ignored probe files alone must not authorize the actual received path.
        (self.dest / ".gitignore").write_text(".agentit/*\n!.agentit/received/\n.agentit/received/probe\n")
        self.git(self.dest, "add", ".gitignore")
        self.git(self.dest, "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "narrow ignore")
        # Re-export from the identical clean Git commit, then set source state.
        self.git(self.dest, "push", "origin", "HEAD")
        self.git(self.source, "fetch", "origin")
        self.git(self.source, "reset", "--hard", self.git(self.dest, "rev-parse", "HEAD"))
        shutil.rmtree(self.package)
        self.export()
        self.assert_blocked_unchanged()
        self.assertFalse((self.dest / ".agentit").exists())

    def test_github_ssh_https_case_default_port_identity(self):
        self.git(self.source, "remote", "set-url", "origin", "https://someone:privatevalue@github.com:443/Company/Project.git")
        self.git(self.dest, "remote", "set-url", "origin", "git@github.com:company/project.git")
        self.export()
        self.assertTrue(self.resume(apply=True)["ready"])

    def test_same_selected_bytes_across_harness_and_managed_cache(self):
        self.export()
        body = (self.harness / "skills/focused-skill/SKILL.md").read_bytes()
        path = self.dest / ".agentit/profile-skills/focused-skill/SKILL.md"
        path.parent.mkdir(parents=True)
        path.write_bytes(body)
        digest = hashlib.sha256(body).hexdigest()
        metadata = {"schema_version": 1, "skills": {"focused-skill": {"managed": True, "destination": ".agentit/profile-skills/focused-skill/SKILL.md", "installed_sha256": digest, "source_sha256": digest}}}
        (self.dest / ".agentit/skills-manifest.json").write_text(json.dumps(metadata))
        self.assertTrue(self.resume(apply=True)["ready"])
        path.write_text("Stale cached body")
        self.assert_blocked_unchanged()

    def test_project_owned_skill_absent_from_harness(self):
        for root in (self.source, self.dest):
            path = root / ".agents/skills/project-only/SKILL.md"
            path.parent.mkdir(parents=True)
            path.write_text("# Intentional project-owned skill\n")
            self.git(root, "add", ".agents")
            self.git(root, "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "project skill")
        # Independently created commit metadata can differ. The destination gets
        # the actual source code commit via normal Git, outside the capsule API.
        self.git(self.source, "push", "origin", "HEAD")
        self.git(self.dest, "fetch", "origin")
        self.git(self.dest, "reset", "--hard", self.git(self.source, "rev-parse", "HEAD"))
        result = handoff.prepare_handoff(self.source, self.package, skill_ids=("project-only",), apply=True, harness_root=self.harness)
        self.assertTrue(result["ready"], result)
        self.assertTrue(self.resume(apply=True)["ready"])

    def test_transfer_rejects_empty_goal_and_next_action_templates(self):
        path = self.source / ".agentit/STATE.md"
        for content in (default_state_markdown(), default_state_markdown(goal="Concrete goal"), self.state.decode().replace("Resume portable task", "(unset)")):
            path.write_text(content)
            self.assertFalse(self.prepare()["ready"])
        path.write_bytes(self.state)
        self.assertTrue(self.prepare()["ready"])

    def test_concurrent_state_edit_before_write_is_preserved(self):
        self.export()
        original = handoff._package
        count = 0
        changed = default_state_markdown(goal="Concurrent task").encode()
        def package_with_edit(path):
            nonlocal count
            count += 1
            result = original(path)
            if count == 2:
                target = self.dest / ".agentit/STATE.md"
                target.write_bytes(changed)
            return result
        with patch.object(handoff, "_package", package_with_edit):
            result = self.resume(apply=True)
        self.assertFalse(result["ready"], result)
        self.assertEqual((self.dest / ".agentit/STATE.md").read_bytes(), changed)


if __name__ == "__main__":
    unittest.main()
