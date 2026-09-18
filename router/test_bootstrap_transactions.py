"""Fault-injection checks for bootstrap's file transaction and rollback boundary."""

from __future__ import annotations

import json
import stat
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from router import bootstrap


class BootstrapTransactionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.backup = self.home / "backup"
        self.manifest = self.backup / "manifest.json"

    def plan(self, count=2):
        specs = []
        operations = []
        for index in range(count):
            destination = self.home / f"file-{index}"
            specs.append(bootstrap.CopySpec(destination, content=b"new\n", mode=0o755))
            present = destination.exists()
            operations.append({
                "destination": str(destination),
                "action": "replace-with-backup" if present else "install",
                "sha256": bootstrap._sha256_bytes(b"new\n"),
                "mode": "0o755",
                "before_sha256": bootstrap._sha256_file(destination) if present else None,
                "before_mode": stat.S_IMODE(destination.stat().st_mode) if present else None,
            })
        return {
            "home": str(self.home), "source_root": str(self.home),
            "providers": [], "python_dependencies": [],
            "runtime_root": str(self.home / "runtime"), "cli_path": str(self.home / "cli"),
            "operations": operations, "_specs": specs, "_hygiene": [],
        }

    def apply(self, plan):
        with patch.object(bootstrap, "_install_dependencies"):
            return bootstrap.apply_install_plan(plan, backup_dir=self.backup)

    def test_failure_after_first_file_leaves_complete_recoverable_journal(self):
        first, second = self.home / "file-0", self.home / "file-1"
        first.write_bytes(b"original\n")
        first.chmod(0o640)
        real_write = bootstrap._atomic_write

        def interrupted(destination, *args, **kwargs):
            if destination == second:
                raise OSError("injected second-file failure")
            return real_write(destination, *args, **kwargs)

        with patch.object(bootstrap, "_atomic_write", side_effect=interrupted):
            with self.assertRaisesRegex(OSError, "injected"):
                self.apply(self.plan())
        self.assertEqual(first.read_bytes(), b"new\n")
        self.assertFalse(second.exists())
        self.assertTrue(self.manifest.is_file(), "partial writes must always have a receipt")
        bootstrap.apply_rollback(self.manifest)
        self.assertEqual(first.read_bytes(), b"original\n")
        self.assertEqual(stat.S_IMODE(first.stat().st_mode), 0o640)
        self.assertFalse(second.exists())

    def test_failure_after_atomic_replace_is_recoverable(self):
        first = self.home / "file-0"
        real_write = bootstrap._atomic_write

        def interrupted(destination, *args, **kwargs):
            result = real_write(destination, *args, **kwargs)
            if destination == first:
                raise OSError("injected after replace")
            return result

        with patch.object(bootstrap, "_atomic_write", side_effect=interrupted):
            with self.assertRaisesRegex(OSError, "injected"):
                self.apply(self.plan(count=1))
        self.assertTrue(first.exists())
        bootstrap.apply_rollback(self.manifest)
        self.assertFalse(first.exists())

    def test_user_edit_after_plan_is_preserved_before_any_install(self):
        destination = self.home / "file-1"
        destination.write_bytes(b"original\n")
        plan = self.plan()
        destination.write_bytes(b"user edit\n")
        with self.assertRaisesRegex(bootstrap.BootstrapError, "changed after planning"):
            self.apply(plan)
        self.assertEqual(destination.read_bytes(), b"user edit\n")
        self.assertFalse((self.home / "file-0").exists())

    def test_source_change_after_plan_is_rejected(self):
        source = self.home / "source"
        source.write_bytes(b"new\n")
        plan = self.plan(count=1)
        plan["_specs"] = [bootstrap.CopySpec(self.home / "file-0", source=source, mode=0o755)]
        source.write_bytes(b"unreviewed source\n")
        with self.assertRaisesRegex(bootstrap.BootstrapError, "source changed after planning"):
            self.apply(plan)
        self.assertFalse((self.home / "file-0").exists())

    def test_mode_only_update_is_applied_and_rollback_restores_old_mode(self):
        destination = self.home / "file-0"
        destination.write_bytes(b"new\n")
        destination.chmod(0o644)
        self.apply(self.plan(count=1))
        self.assertEqual(stat.S_IMODE(destination.stat().st_mode), 0o755)
        bootstrap.apply_rollback(self.manifest)
        self.assertEqual(stat.S_IMODE(destination.stat().st_mode), 0o644)

    def test_rollback_preserves_post_install_permission_changes(self):
        destination = self.home / "file-0"
        self.apply(self.plan(count=1))
        destination.chmod(0o600)
        with self.assertRaisesRegex(bootstrap.BootstrapError, "changed after install"):
            bootstrap.rollback_plan(self.manifest)
        self.assertEqual(stat.S_IMODE(destination.stat().st_mode), 0o600)

    def test_interrupted_rollback_can_be_retried(self):
        first, second = self.home / "file-0", self.home / "file-1"
        first.write_bytes(b"original first\n")
        second.write_bytes(b"original second\n")
        self.apply(self.plan())
        real_write = bootstrap._atomic_write

        def interrupted(destination, *args, **kwargs):
            if destination == first:
                raise OSError("injected during rollback")
            return real_write(destination, *args, **kwargs)

        with patch.object(bootstrap, "_atomic_write", side_effect=interrupted):
            with self.assertRaisesRegex(OSError, "injected"):
                bootstrap.apply_rollback(self.manifest)
        self.assertEqual(second.read_bytes(), b"original second\n")
        bootstrap.apply_rollback(self.manifest)
        self.assertEqual(first.read_bytes(), b"original first\n")
        self.assertEqual(second.read_bytes(), b"original second\n")

    def test_user_edit_after_rollback_plan_is_preserved(self):
        destination = self.home / "file-0"
        self.apply(self.plan(count=1))
        real_plan = bootstrap.rollback_plan

        def edited_after_plan(manifest):
            result = real_plan(manifest)
            destination.write_bytes(b"user edit\n")
            return result

        with patch.object(bootstrap, "rollback_plan", side_effect=edited_after_plan):
            with self.assertRaisesRegex(bootstrap.BootstrapError, "changed after install"):
                bootstrap.apply_rollback(self.manifest)
        self.assertEqual(destination.read_bytes(), b"user edit\n")


if __name__ == "__main__":
    unittest.main()
