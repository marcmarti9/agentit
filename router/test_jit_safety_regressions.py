from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from router.bootstrap import apply_rollback, rollback_plan
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
