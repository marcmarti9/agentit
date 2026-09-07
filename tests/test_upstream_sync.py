"""Offline package-refresh tests with inert upstream fixtures."""

import importlib.util
import io
import json
import tarfile
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("upstream_sync", ROOT / "scripts/sync_upstream_skills.py")
sync = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sync)


class UpstreamSyncTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repo"
        self.root.mkdir()
        self.cache = Path(self.temp.name) / "cache"
        self.cache.mkdir()
        self.old_sha, self.new_sha = "a" * 40, "b" * 40
        self.lock = {"schema_version": 1, "mappings": [{"skill": "example", "repo": "example/skills", "path": "skills/example", "snapshot": self.old_sha}], "shared": []}
        self.package = self.root / "skills/example"
        self.package.mkdir(parents=True)
        (self.package / "SKILL.md").write_bytes(b"old body\n")
        (self.root / sync.LOCK).write_text(json.dumps(self.lock))
        self.archive(self.old_sha, {"skills/example/SKILL.md": b"old body\n", "LICENSE": b"license\n"})
        self.archive(self.new_sha, {"skills/example/SKILL.md": b"new body\n", "skills/example/scripts/never-run.sh": b"exit 99\n", "LICENSE": b"license\n"})

    def archive(self, sha, files):
        path = self.cache / f"example--skills@{sha}.tar.gz"
        with tarfile.open(path, "w:gz") as tar:
            for name, data in files.items():
                info = tarfile.TarInfo("snapshot/" + name)
                info.size = len(data)
                info.mode = 0o644
                tar.addfile(info, io.BytesIO(data))
        return path

    def candidate(self):
        return sync.build_candidate(self.root, self.lock, {"example/skills": self.new_sha}, self.cache, offline=True)

    def test_plan_is_read_only_apply_preserves_complete_package_and_is_idempotent(self):
        old, updated, desired = self.candidate()
        self.assertEqual((self.package / "SKILL.md").read_bytes(), b"old body\n")
        self.assertFalse((self.root / "vendor").exists())
        result = sync.apply_candidate(self.root, old, updated, desired)
        self.assertEqual(result["status"], "applied")
        self.assertEqual((self.package / "SKILL.md").read_bytes(), b"new body\n")
        self.assertEqual((self.package / "scripts/never-run.sh").read_bytes(), b"exit 99\n")
        self.assertEqual(sync.check_integrity(self.root, updated)["packages"], 1)
        self.assertEqual(sync.apply_candidate(self.root, updated, updated, desired)["changed_files"], 0)

    def test_initial_lock_requires_exact_old_upstream_bytes(self):
        (self.package / "SKILL.md").write_bytes(b"local edit\n")
        with self.assertRaisesRegex(sync.SyncError, "integrity differs"):
            self.candidate()
        self.assertEqual((self.package / "SKILL.md").read_bytes(), b"local edit\n")

    def test_extra_local_package_files_are_preserved_by_refusing_refresh(self):
        (self.package / "user-notes.md").write_bytes(b"retain me\n")
        with self.assertRaisesRegex(sync.SyncError, "integrity differs"):
            self.candidate()

    def test_unowned_license_destination_is_not_overwritten(self):
        old, updated, desired = self.candidate()
        license_path = self.root / "vendor/licenses/example--skills/LICENSE"
        license_path.parent.mkdir(parents=True)
        license_path.write_bytes(b"user-owned\n")
        with self.assertRaisesRegex(sync.SyncError, "unowned file"):
            sync.apply_candidate(self.root, old, updated, desired)
        self.assertEqual((self.package / "SKILL.md").read_bytes(), b"old body\n")

    def test_caught_write_failure_rolls_back_refresh(self):
        old, updated, desired = self.candidate()
        original_lock = (self.root / sync.LOCK).read_bytes()
        real_write = sync.atomic_write
        failures = []

        def fail_once(path, *args):
            if path == self.root / sync.LOCK and not failures:
                failures.append(True)
                raise OSError("injected refresh failure")
            return real_write(path, *args)

        with patch.object(sync, "atomic_write", side_effect=fail_once):
            with self.assertRaisesRegex(OSError, "injected"):
                sync.apply_candidate(self.root, old, updated, desired)
        self.assertEqual((self.package / "SKILL.md").read_bytes(), b"old body\n")
        self.assertEqual((self.root / sync.LOCK).read_bytes(), original_lock)
        self.assertFalse((self.package / "scripts/never-run.sh").exists())

    def test_traversal_archive_is_rejected_without_extraction(self):
        path = self.archive("c" * 40, {"../../outside": b"no\n"})
        with self.assertRaisesRegex(sync.SyncError, "unsafe relative path"):
            sync.read_archive(path)
        self.assertFalse((self.root.parent / "outside").exists())

    def test_nonregular_entries_inside_selected_packages_are_rejected(self):
        files = {"skills/example/SKILL.md": (b"body\n", 0o644), "skills/example/escape": (b"", -1)}
        with self.assertRaisesRegex(sync.SyncError, "non-regular"):
            sync.select_package(files, self.lock["mappings"][0])

    def test_integrity_covers_original_license_and_package_modes(self):
        old, updated, desired = self.candidate()
        sync.apply_candidate(self.root, old, updated, desired)
        (self.package / "SKILL.md").chmod(0o600)
        with self.assertRaisesRegex(sync.SyncError, "integrity differs"):
            sync.check_integrity(self.root, updated)

    def test_overlapping_normalized_package_destinations_are_rejected(self):
        self.lock["mappings"].append({**self.lock["mappings"][0], "skill": "second-owner", "destination": "skills/./example"})
        with self.assertRaisesRegex(sync.SyncError, "overlap"):
            self.candidate()

    def test_current_directory_is_not_a_file_destination(self):
        for relative in (".", "./", ""):
            with self.subTest(relative=relative), self.assertRaises(sync.SyncError):
                sync.relative_path(relative)

    def test_shared_manifest_cannot_overlap_a_package(self):
        self.lock["shared"] = [{"destination": "shared/references", "manifest": "skills/./example/SKILL.md"}]
        with self.assertRaisesRegex(sync.SyncError, "overlap"):
            self.candidate()

    def test_post_write_integrity_failure_restores_prior_files(self):
        old, updated, desired = self.candidate()
        real_check = sync.check_integrity
        calls = []

        def fail_final_check(root, lock):
            calls.append(True)
            if len(calls) == 2:
                raise sync.SyncError("injected post-write integrity failure")
            return real_check(root, lock)

        with patch.object(sync, "check_integrity", side_effect=fail_final_check):
            with self.assertRaisesRegex(sync.SyncError, "post-write"):
                sync.apply_candidate(self.root, old, updated, desired)
        self.assertEqual((self.package / "SKILL.md").read_bytes(), b"old body\n")
        self.assertEqual(json.loads((self.root / sync.LOCK).read_text()), self.lock)

    def test_recovery_preserves_concurrent_edit_instead_of_overwriting_it(self):
        old, updated, desired = self.candidate()
        real_write = sync.atomic_write
        failures = []

        def fail_once_with_concurrent_edit(path, *args):
            if path == self.root / sync.LOCK and not failures:
                failures.append(True)
                (self.package / "SKILL.md").write_bytes(b"concurrent user edit\n")
                raise OSError("injected after another writer changed a file")
            return real_write(path, *args)

        with patch.object(sync, "atomic_write", side_effect=fail_once_with_concurrent_edit):
            with self.assertRaisesRegex(sync.SyncError, "preserved modified"):
                sync.apply_candidate(self.root, old, updated, desired)
        self.assertEqual((self.package / "SKILL.md").read_bytes(), b"concurrent user edit\n")


if __name__ == "__main__":
    unittest.main()
