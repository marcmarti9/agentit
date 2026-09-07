"""Temporary installation/migration checks for obsolete runtime file ownership."""

import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from router import bootstrap


class RuntimeInventoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.home = self.base / "home"
        self.home.mkdir()
        self.source = self.base / "source"
        (self.source / "payload").mkdir(parents=True)
        (self.source / "payload/old.txt").write_bytes(b"original old file\n")
        (self.source / "payload/old.txt").chmod(0o640)
        (self.source / "payload/keep.txt").write_bytes(b"keep\n")
        for skill in ("using-agentit", "task-router", "using-agent-skills"):
            folder = self.source / "skills" / skill
            folder.mkdir(parents=True)
            (folder / "SKILL.md").write_text("# " + skill + "\n")
        manifest = {"schema_version": 1, "runtime_paths": ["payload", "skills"], "python_dependencies": [], "core_skills": ["using-agentit", "task-router", "using-agent-skills"], "providers": {"codex": {"skills_root": ".agents/skills"}}}
        (self.source / "bootstrap-manifest.json").write_text(json.dumps(manifest))
        self.installed_old = self.home / ".agentit/runtime/payload/old.txt"
        self.inventory = self.home / ".agentit/runtime-inventory.json"
        self.apply(self.plan())

    def plan(self):
        return bootstrap.build_install_plan(home=self.home, source_root=self.source, provider="codex")

    def apply(self, plan, **kwargs):
        with patch.object(bootstrap, "_install_dependencies"):
            return bootstrap.apply_install_plan(plan, **kwargs)

    def retire_source_file(self):
        (self.source / "payload/old.txt").unlink()

    def test_update_retires_exact_owned_file_and_rollback_restores_file_and_inventory(self):
        original_inventory = self.inventory.read_bytes()
        self.retire_source_file()
        plan = self.plan()
        removed = [op for op in plan["operations"] if op["action"] == "remove-obsolete-runtime-file"]
        self.assertEqual([op["destination"] for op in removed], [str(self.installed_old)])
        result = self.apply(plan)
        self.assertFalse(self.installed_old.exists())
        self.assertTrue(all(op["action"] == "keep" for op in self.plan()["operations"]))
        bootstrap.apply_rollback(Path(result["backup_manifest"]))
        self.assertEqual(self.installed_old.read_bytes(), b"original old file\n")
        self.assertEqual(self.installed_old.stat().st_mode & 0o777, 0o640)
        self.assertEqual(self.inventory.read_bytes(), original_inventory)

    def test_modified_obsolete_and_unowned_files_survive_update(self):
        self.retire_source_file()
        self.installed_old.write_bytes(b"user edit\n")
        unknown = self.installed_old.with_name("user.txt")
        unknown.write_bytes(b"unowned\n")
        plan = self.plan()
        self.assertEqual(plan["retained_modified_runtime_files"], ["payload/old.txt"])
        self.assertEqual(plan["retained_unmanaged_runtime_files"], ["payload/user.txt"])
        self.apply(plan)
        self.assertEqual(self.installed_old.read_bytes(), b"user edit\n")
        self.assertEqual(unknown.read_bytes(), b"unowned\n")

    def test_permission_only_drift_preserves_obsolete_file(self):
        self.retire_source_file()
        self.installed_old.chmod(0o600)
        plan = self.plan()
        self.assertEqual(plan["retained_modified_runtime_files"], ["payload/old.txt"])
        self.apply(plan)
        self.assertEqual(self.installed_old.stat().st_mode & 0o777, 0o600)

    def test_legacy_successful_receipt_can_establish_exact_ownership(self):
        self.inventory.unlink()
        self.retire_source_file()
        self.apply(self.plan())
        self.assertFalse(self.installed_old.exists())

    def test_legacy_without_receipt_retains_and_reports_unproven_file(self):
        self.inventory.unlink()
        shutil.rmtree(self.home / ".agentit/backups")
        self.retire_source_file()
        plan = self.plan()
        self.assertEqual(plan["retained_unmanaged_runtime_files"], ["payload/old.txt"])
        self.apply(plan)
        self.assertTrue(self.installed_old.exists())

    def test_inventory_path_traversal_is_rejected_before_mutation(self):
        data = json.loads(self.inventory.read_text())
        data["files"]["../../outside"] = {"sha256": "a" * 64, "mode": 0o644}
        self.inventory.write_text(json.dumps(data))
        with self.assertRaisesRegex(bootstrap.BootstrapError, "unsafe relative path"):
            self.plan()
        self.assertTrue(self.installed_old.exists())

    def test_inventory_alias_collisions_are_rejected_before_retirement(self):
        self.retire_source_file()
        original = self.inventory.read_text()
        for alias in ("payload/./old.txt", "payload//old.txt", "./payload/old.txt"):
            with self.subTest(alias=alias):
                data = json.loads(original)
                data["files"][alias] = data["files"]["payload/old.txt"]
                self.inventory.write_text(json.dumps(data))
                with self.assertRaisesRegex(bootstrap.BootstrapError, "duplicate runtime inventory path"):
                    self.plan()
                self.assertTrue(self.installed_old.exists())

    def test_inventory_repeated_json_keys_are_rejected_before_retirement(self):
        self.retire_source_file()
        record = json.loads(self.inventory.read_text())["files"]["payload/old.txt"]
        entry = '"payload/old.txt":' + json.dumps(record)
        self.inventory.write_text('{"kind":"agentit.runtime.inventory","schema_version":1,"files":{' + entry + ',' + entry + '}}')
        with self.assertRaisesRegex(bootstrap.BootstrapError, "duplicate runtime inventory key"):
            self.plan()
        self.assertTrue(self.installed_old.exists())

    def test_inventory_symlink_is_rejected(self):
        target = self.base / "unrelated.json"
        self.inventory.rename(target)
        self.inventory.symlink_to(target)
        with self.assertRaisesRegex(bootstrap.BootstrapError, "symlink"):
            self.plan()

    def test_forged_legacy_receipt_cannot_target_outside_private_runtime(self):
        self.inventory.unlink()
        receipt_path = next((self.home / ".agentit/backups").glob("install-*/manifest.json"))
        data = json.loads(receipt_path.read_text())
        data["records"][0]["destination"] = str(self.home / "outside.txt")
        receipt_path.write_text(json.dumps(data))
        with self.assertRaisesRegex(bootstrap.BootstrapError, "escapes private runtime"):
            self.plan()

    def test_interruption_immediately_after_delete_is_recoverable(self):
        self.retire_source_file()
        backup = self.home / "interrupted"
        real_unlink = Path.unlink
        interrupted = []

        def unlink_then_fail(path, *args, **kwargs):
            result = real_unlink(path, *args, **kwargs)
            if path == self.installed_old and not interrupted:
                interrupted.append(True)
                raise OSError("injected after obsolete deletion")
            return result

        with patch.object(Path, "unlink", side_effect=None, autospec=True) as mocked:
            mocked.side_effect = unlink_then_fail
            with self.assertRaisesRegex(OSError, "injected"):
                self.apply(self.plan(), backup_dir=backup)
        self.assertFalse(self.installed_old.exists())
        receipt = backup / "manifest.json"
        self.assertTrue(json.loads(receipt.read_text())["recovery_only"])
        bootstrap.apply_rollback(receipt)
        self.assertEqual(self.installed_old.read_bytes(), b"original old file\n")


if __name__ == "__main__":
    unittest.main()
