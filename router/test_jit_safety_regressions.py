from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from router.bootstrap import BootstrapError, apply_rollback, rollback_plan
from router.host_skill_hygiene import (
    HostSkillHygieneError,
    apply_host_skill_hygiene,
    plan_host_skill_hygiene,
)
from router.profile_jit_cli import (
    PRIVATE_SKILL_ROOT,
    _apply_planned_removal,
    _build_payload,
    _private_cleanup_plan,
    _read_manifest,
)
from router.profiles import ProfileError, load_catalog


REPOSITORY = Path(__file__).resolve().parents[1]
SKILL_ID = "supabase-postgres-best-practices"
REFERENCE = Path("references") / "_sections.md"


class HostSkillHygieneSafetyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.home = self.root / "home"
        self.home.mkdir()
        self.manifest = json.loads(
            (REPOSITORY / "bootstrap-manifest.json").read_text(encoding="utf-8")
        )
        self.destination = self.home / ".agents" / "skills" / SKILL_ID
        self.destination.parent.mkdir(parents=True)
        shutil.copytree(REPOSITORY / "skills" / SKILL_ID, self.destination)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def plan(self):
        return plan_host_skill_hygiene(
            home=self.home,
            source_root=REPOSITORY,
            manifest=self.manifest,
            providers=["codex"],
        )

    def test_host_cleanup_revalidates_exact_planned_tree_before_deletion(self) -> None:
        operations = self.plan()
        self.assertEqual(1, len(operations))
        body = self.destination / "SKILL.md"
        body.write_text(body.read_text(encoding="utf-8") + "\nuser edit\n", encoding="utf-8")

        with self.assertRaisesRegex(HostSkillHygieneError, "changed after planning"):
            apply_host_skill_hygiene(
                operations,
                home=self.home,
                backup_root=self.root / "backup",
            )

        self.assertTrue(self.destination.is_dir())
        self.assertIn("user edit", body.read_text(encoding="utf-8"))

    def test_host_cleanup_retains_permission_only_changes(self):
        body = self.destination / "SKILL.md"
        body.chmod(0o600)
        self.assertEqual(self.plan(), [])
        self.assertEqual(body.stat().st_mode & 0o777, 0o600)

    def test_host_cleanup_retains_added_empty_directory(self):
        empty = self.destination / "user-empty-directory"
        empty.mkdir()
        self.assertEqual(self.plan(), [])
        self.assertTrue(empty.is_dir())

    def test_destructive_cleanup_writes_rollback_receipt_before_final_bootstrap_receipt(self) -> None:
        backup_root = self.root / "backup"
        records = apply_host_skill_hygiene(
            self.plan(),
            home=self.home,
            backup_root=backup_root,
        )
        self.assertEqual(1, len(records))
        self.assertFalse(self.destination.exists())

        manifest_path = backup_root / "manifest.json"
        receipt = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertTrue(receipt["recovery_only"])
        self.assertEqual("agentit.bootstrap.receipt", receipt["kind"])
        self.assertEqual("removed_skill_tree", receipt["records"][0]["kind"])

        plan = rollback_plan(manifest_path)
        self.assertEqual("restore-tree", plan["operations"][0]["action"])
        result = apply_rollback(manifest_path)
        self.assertEqual("rolled-back", result["status"])
        self.assertTrue((self.destination / "SKILL.md").is_file())

    def two_tree_plan(self):
        second = self.destination.parent / "interview-me"
        shutil.copytree(REPOSITORY / "skills/interview-me", second)
        operations = self.plan()
        self.assertEqual(len(operations), 2)
        return operations, [Path(op["destination"]) for op in operations]

    def test_failed_second_backup_does_not_block_recovery_of_first_removed_tree(self):
        operations, (first, second) = self.two_tree_plan()
        originals = {p: {f.relative_to(p): f.read_bytes() for f in p.rglob("*") if f.is_file()} for p in (first, second)}
        backup_root = self.root / "backup"
        real_copy = shutil.copytree

        def fail_second(source, *args, **kwargs):
            if Path(source) == second:
                raise OSError("injected second tree backup failure")
            return real_copy(source, *args, **kwargs)

        with patch("router.host_skill_hygiene.shutil.copytree", side_effect=fail_second):
            with self.assertRaisesRegex(OSError, "second tree"):
                apply_host_skill_hygiene(operations, home=self.home, backup_root=backup_root)
        self.assertFalse(first.exists())
        result = apply_rollback(backup_root / "manifest.json")
        self.assertEqual(result["changed_files"], 1)
        for path in (first, second):
            self.assertEqual({f.relative_to(path): f.read_bytes() for f in path.rglob("*") if f.is_file()}, originals[path])

    def test_recovery_preserves_tree_changed_during_backup(self):
        operations, (first, second) = self.two_tree_plan()
        backup_root = self.root / "backup"
        real_copy = shutil.copytree

        def copy_then_edit(source, *args, **kwargs):
            result = real_copy(source, *args, **kwargs)
            if Path(source) == second:
                (second / "user-edit.txt").write_text("preserve user change\n")
            return result

        with patch("router.host_skill_hygiene.shutil.copytree", side_effect=copy_then_edit):
            with self.assertRaisesRegex(HostSkillHygieneError, "changed during backup"):
                apply_host_skill_hygiene(operations, home=self.home, backup_root=backup_root)
        with self.assertRaisesRegex(BootstrapError, "recreated"):
            apply_rollback(backup_root / "manifest.json")
        self.assertEqual((second / "user-edit.txt").read_text(), "preserve user change\n")
        self.assertFalse(first.exists())
        self.assertTrue((backup_root / "removed-skill-trees" / first.relative_to(self.home)).is_dir())

    def test_partial_tree_deletion_is_preserved_and_refused_during_recovery(self):
        backup_root = self.root / "backup"

        def partially_remove(path, *args, **kwargs):
            (Path(path) / "SKILL.md").unlink()
            raise OSError("injected partial tree deletion")

        with patch("router.host_skill_hygiene.shutil.rmtree", side_effect=partially_remove):
            with self.assertRaisesRegex(OSError, "partial tree"):
                apply_host_skill_hygiene(self.plan(), home=self.home, backup_root=backup_root)
        with self.assertRaisesRegex(BootstrapError, "recreated"):
            apply_rollback(backup_root / "manifest.json")
        self.assertTrue(self.destination.is_dir())
        self.assertFalse((self.destination / "SKILL.md").exists())
        self.assertTrue((backup_root / "removed-skill-trees" / self.destination.relative_to(self.home) / "SKILL.md").is_file())

    def test_recovery_does_not_skip_permission_drift_during_backup(self):
        backup_root = self.root / "backup"
        real_copy = shutil.copytree

        def copy_then_chmod(source, *args, **kwargs):
            result = real_copy(source, *args, **kwargs)
            if Path(source) == self.destination:
                (self.destination / "SKILL.md").chmod(0o600)
            return result

        with patch("router.host_skill_hygiene.shutil.copytree", side_effect=copy_then_chmod):
            with self.assertRaisesRegex(HostSkillHygieneError, "changed during backup"):
                apply_host_skill_hygiene(self.plan(), home=self.home, backup_root=backup_root)
        with self.assertRaisesRegex(BootstrapError, "recreated"):
            apply_rollback(backup_root / "manifest.json")
        self.assertEqual((self.destination / "SKILL.md").stat().st_mode & 0o777, 0o600)

    def test_hash_only_legacy_receipt_restores_absent_tree_but_cannot_certify_retry(self):
        backup_root = self.root / "backup"
        apply_host_skill_hygiene(self.plan(), home=self.home, backup_root=backup_root)
        manifest_path = backup_root / "manifest.json"
        data = json.loads(manifest_path.read_text())
        for record in data["records"]:
            record.pop("tree_metadata_version")
            record.pop("tree_metadata")
        manifest_path.write_text(json.dumps(data))
        apply_rollback(manifest_path)
        self.assertTrue((self.destination / "SKILL.md").exists())
        with self.assertRaisesRegex(BootstrapError, "recreated"):
            apply_rollback(manifest_path)

    def test_recovery_refuses_backup_permission_drift(self):
        backup_root = self.root / "backup"
        apply_host_skill_hygiene(self.plan(), home=self.home, backup_root=backup_root)
        backup_body = backup_root / "removed-skill-trees" / self.destination.relative_to(self.home) / "SKILL.md"
        backup_body.chmod(0o600)
        with self.assertRaisesRegex(BootstrapError, "backup metadata changed"):
            apply_rollback(backup_root / "manifest.json")
        self.assertFalse(self.destination.exists())
        self.assertEqual(backup_body.stat().st_mode & 0o777, 0o600)


class PrivateProfileCacheSafetyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.repository = self.root / "repository"
        self.project = self.root / "project"
        self.project.mkdir()
        shutil.copytree(
            REPOSITORY,
            self.repository,
            symlinks=True,
            ignore=shutil.ignore_patterns(".git", "__pycache__", "backups"),
        )

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def run_agentit(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                str(self.repository / "agentit"),
                *args,
                "--repo-root",
                str(self.repository),
                "--project",
                str(self.project),
            ],
            cwd=self.repository,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )

    def test_profile_refresh_removes_reference_deleted_from_source_and_manifest(self) -> None:
        enabled = self.run_agentit("enable", "supabase", "--apply")
        self.assertEqual(0, enabled.returncode, enabled.stdout)

        private_reference = self.project / PRIVATE_SKILL_ROOT / SKILL_ID / REFERENCE
        source_reference = self.repository / "skills" / SKILL_ID / REFERENCE
        self.assertTrue(private_reference.is_file())
        self.assertTrue(source_reference.is_file())
        source_reference.unlink()

        refreshed = self.run_agentit("enable", "supabase", "--apply")
        self.assertEqual(0, refreshed.returncode, refreshed.stdout)
        self.assertFalse(private_reference.exists())

        manifest = _read_manifest(self.project)
        self.assertIsNotNone(manifest)
        assert manifest is not None
        files = manifest["skills"][SKILL_ID]["files"]
        self.assertNotIn(REFERENCE.as_posix(), files)

    def test_private_cleanup_revalidates_hash_immediately_before_removal(self) -> None:
        enabled = self.run_agentit("enable", "supabase", "--apply")
        self.assertEqual(0, enabled.returncode, enabled.stdout)
        old = _read_manifest(self.project)
        self.assertIsNotNone(old)
        assert old is not None

        catalog = load_catalog(self.repository / "profiles.yaml")
        payload = _build_payload([], catalog=catalog, repo_root=self.repository)
        cleanup = _private_cleanup_plan(
            project=self.project,
            old_manifest=old,
            payload=payload,
        )
        target = next(item for item in cleanup if item["path"].endswith("/SKILL.md"))
        path = Path(target["path"])
        path.write_text(path.read_text(encoding="utf-8") + "\nuser edit\n", encoding="utf-8")

        with self.assertRaisesRegex(ProfileError, "changed after planning"):
            _apply_planned_removal(
                target,
                project=self.project,
                stop=self.project / PRIVATE_SKILL_ROOT,
                label="managed private profile file",
            )
        self.assertTrue(path.is_file())
        self.assertIn("user edit", path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
