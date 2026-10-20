"""Publication cleanup boundaries; all fixtures are disposable local projects."""

import contextlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from router import cleanup


class CleanupTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name)
        self.git("init", "-q")
        (self.project / ".gitignore").write_text(".agentit/\n")
        (self.project / "source.txt").write_text("source\n")
        self.git("add", ".")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-qm", "fixture")
        (self.project / ".agentit").mkdir()
        self.ledger_path = self.project / ".agentit" / "ledger.json"
        self.ledger = cleanup.ledger_template("fixture")
        self.ledger.update(inventory_complete=True,
                           no_local_resources_reason="Source-only task; no task artifacts created",
                           no_remote_resources_reason="No remote task artifacts created")

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.project, check=True,
                              capture_output=True, text=True).stdout.strip()

    def review(self):
        self.ledger_path.write_text(json.dumps(self.ledger))
        return cleanup.review(self.project, self.ledger_path)

    def test_missing_review_is_not_a_pass(self):
        result = cleanup.check(self.project)
        self.assertFalse(result["allowed"])
        self.assertIn("review_missing", result["blocking_reasons"])

    def test_omitted_or_nontext_remote_scope_reason_never_means_none_used(self):
        for value in (None, False, [], ""):
            self.ledger["no_remote_resources_reason"] = value
            self.assertIn("remote_scope_not_reviewed", self.review()["blocking_reasons"])

    def test_source_only_review_and_private_receipt(self):
        self.assertTrue(self.review()["allowed"])
        result = cleanup.check(self.project)
        self.assertTrue(result["allowed"], result)
        receipt_path = self.project / cleanup.RECEIPT
        self.assertEqual(0o600, receipt_path.stat().st_mode & 0o777)
        self.assertNotIn(str(self.project), json.dumps(result))
        self.assertEqual(0, result["retained_resources"])

    def test_commit_change_and_dirty_source_invalidate_review(self):
        self.review()
        (self.project / "source.txt").write_text("changed\n")
        self.assertFalse(cleanup.check(self.project)["allowed"])
        self.git("add", "source.txt")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-qm", "change")
        self.assertIn("source_changed", cleanup.check(self.project)["blocking_reasons"])

    def test_declared_concurrent_wip_is_preserved_without_blocking_publication(self):
        path = self.project / "peer-work"
        path.mkdir()
        (path / "partial.py").write_text("unfinished\n")
        self.ledger["retained_source_paths"] = [{"path": "peer-work", "owner": "peer-worker",
                                                 "reason": "Concurrent task owns unfinished sources"}]
        result = self.review()
        self.assertTrue(result["allowed"], result)
        self.assertEqual("REVIEWED_WITH_RETAINED", result["status"])
        (path / "partial.py").write_text("peer is still working\n")
        self.assertTrue(cleanup.check(self.project)["allowed"])
        (self.project / "unexplained.txt").write_text("must account for this\n")
        self.assertIn("source_dirty", cleanup.check(self.project)["blocking_reasons"])

    def test_retained_source_cannot_cover_entire_repo_or_omit_owner(self):
        for item in ({"path": ".", "owner": "peer", "reason": "too broad"},
                     {"path": "peer", "reason": "no ownership"}):
            self.ledger["retained_source_paths"] = [item]
            with self.assertRaises(cleanup.CleanupError):
                self.review()

    def test_malformed_replacement_review_invalidates_old_pass(self):
        self.review()
        self.ledger_path.write_text("{broken")
        with self.assertRaises(ValueError):
            cleanup.review(self.project, self.ledger_path)
        self.assertFalse(cleanup.check(self.project)["allowed"])

    def test_unignored_state_and_duplicate_capacity_devices_rejected(self):
        self.ledger["capacity"].append(dict(self.ledger["capacity"][0]))
        with self.assertRaises(cleanup.CleanupError):
            self.review()
        (self.project / ".gitignore").write_text("")
        with self.assertRaises(cleanup.CleanupError):
            self.review()

    def test_stale_and_future_receipts_rejected(self):
        self.review()
        receipt_path = self.project / cleanup.RECEIPT
        receipt = json.loads(receipt_path.read_text())
        for stamp in ("2000-01-01T00:00:00+00:00", "2100-01-01T00:00:00+00:00"):
            receipt["reviewed_at"] = stamp
            receipt_path.write_text(json.dumps(receipt))
            self.assertIn("review_expired", cleanup.check(self.project)["blocking_reasons"])

    def test_capacity_uses_available_blocks_and_peak_plus_reserve(self):
        fs = type("FS", (), {"f_bavail": 10, "f_bfree": 10000, "f_frsize": 1024, "f_blocks": 100000})()
        with patch("router.cleanup.os.statvfs", return_value=fs):
            result = cleanup.local_capacity(self.project, planned_peak_bytes=9000, reserve_bytes=2000)
        self.assertFalse(result["allowed"])
        self.assertEqual(10240, result["available_bytes"])
        self.assertEqual(11000, result["required_bytes"])

    def test_shared_production_reserve_cannot_be_lowered(self):
        result = cleanup.capacity_result(available_bytes=99 * cleanup.GIB,
                                         total_bytes=1000 * cleanup.GIB,
                                         planned_peak_bytes=0, reserve_bytes=0,
                                         shared_production=True)
        self.assertFalse(result["allowed"])
        self.assertEqual(100 * cleanup.GIB, result["reserve_bytes"])
        result = cleanup.capacity_result(available_bytes=150 * cleanup.GIB,
                                         total_bytes=2000 * cleanup.GIB,
                                         planned_peak_bytes=0, reserve_bytes=0,
                                         shared_production=True)
        self.assertEqual(200 * cleanup.GIB, result["reserve_bytes"])

    def test_capacity_rechecked_at_publication(self):
        self.review()
        fs = type("FS", (), {"f_bavail": 0, "f_frsize": 4096, "f_blocks": 100000})()
        with patch("router.cleanup.os.statvfs", return_value=fs):
            result = cleanup.check(self.project)
        self.assertFalse(result["allowed"])
        self.assertIn("insufficient_capacity", result["blocking_reasons"])

    def add_local_resource(self, **overrides):
        scope = self.project / ".agentit" / "artifacts"
        scope.mkdir(exist_ok=True)
        (scope / "qa.bin").write_bytes(b"private fixture")
        resource = {"name": "qa.bin", "ownership": "task", "disposition": "retained",
                    "retention": "active", "reason": "QA still running"}
        resource.update(overrides)
        self.ledger["local_scopes"] = [{"path": str(scope), "resources": [resource]}]
        return scope

    def test_known_active_private_resources_preserved_and_reported(self):
        scope = self.add_local_resource()
        result = self.review()
        self.assertTrue(result["allowed"], result)
        self.assertEqual("REVIEWED_WITH_RETAINED", result["status"])
        self.assertEqual(1, result["retained_resources"])
        self.assertTrue((scope / "qa.bin").exists())
        self.assertNotIn("QA still running", json.dumps(result))

    def test_unknown_retention_and_unlisted_resources_block(self):
        scope = self.add_local_resource(retention="unknown")
        result = self.review()
        self.assertFalse(result["allowed"])
        self.assertIn("unresolved_resource", result["blocking_reasons"])
        self.ledger["local_scopes"][0]["resources"][0]["retention"] = "active"
        (scope / "forgotten-copy").mkdir()
        self.assertIn("unlisted_local_resource", self.review()["blocking_reasons"])

    def test_local_inventory_drift_and_ledger_edits_invalidate_review(self):
        scope = self.add_local_resource()
        self.review()
        (scope / "new.bin").write_bytes(b"new")
        self.assertIn("local_inventory_changed", cleanup.check(self.project)["blocking_reasons"])
        self.ledger_path.write_text(self.ledger_path.read_text() + "\n")
        self.assertIn("ledger_changed", cleanup.check(self.project)["blocking_reasons"])

    def test_removed_requires_owned_resource_and_actual_absence(self):
        scope = self.add_local_resource(disposition="removed")
        self.assertIn("removed_resource_still_present", self.review()["blocking_reasons"])
        (scope / "qa.bin").unlink()
        self.assertTrue(self.review()["allowed"])
        self.ledger["local_scopes"][0]["resources"][0]["ownership"] = "unknown"
        self.assertIn("unowned_removal", self.review()["blocking_reasons"])

    def test_declared_remote_requires_fresh_inventory_and_capacity(self):
        self.ledger["remote_scopes"] = [{"id": "qa-host", "evidence": ".agentit/remote.json"}]
        self.assertFalse(self.review()["allowed"])
        evidence = {"scope_id": "qa-host", "observed_at": cleanup.now_iso(),
                    "inventory_complete": True, "resources": [],
                    "capacity": {"available_bytes": 500 * cleanup.GIB,
                                 "total_bytes": 1000 * cleanup.GIB,
                                 "planned_peak_bytes": 0, "reserve_bytes": 0,
                                 "shared_production": True}}
        path = self.project / ".agentit/remote.json"
        path.write_text(json.dumps(evidence))
        self.assertTrue(self.review()["allowed"])
        evidence["observed_at"] = "2000-01-01T00:00:00+00:00"
        path.write_text(json.dumps(evidence))
        self.assertIn("remote_inventory_expired", self.review()["blocking_reasons"])

    def test_private_path_and_resource_symlinks_refused(self):
        other = self.project / "public.json"
        other.write_text(json.dumps(self.ledger))
        with self.assertRaises(cleanup.CleanupError):
            cleanup.review(self.project, other)
        scope = self.add_local_resource()
        (scope / "qa.bin").unlink()
        (scope / "qa.bin").symlink_to(self.project / "source.txt")
        self.assertIn("unsafe_local_scope", self.review()["blocking_reasons"])

    def test_publication_verification_cannot_skip_cleanup_or_exit_success(self):
        from router.verify import apply_verification, plan_verification
        from router.verify_cli import main
        plan = plan_verification(self.project, explicit_signals=["publication"])
        self.assertIn("publication-cleanup", plan["blocking_ids"])
        result = apply_verification(self.project, explicit_signals=["publication"], run_project_commands=False)
        self.assertTrue(result["blocking_failed"])
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(1, main(["--project", str(self.project), "--signal", "publication", "--apply"]))
        self.review()
        result = apply_verification(self.project, explicit_signals=["publication"], run_project_commands=False)
        self.assertFalse(result["blocking_failed"], result)

    def test_publication_rejects_artifact_created_by_real_test_and_cli_exits_nonzero(self):
        from router.verify import apply_verification
        tests = self.project / "tests"
        tests.mkdir()
        (self.project / ".gitignore").write_text(".agentit/\n__pycache__/\n")
        (tests / "test_artifact.py").write_text(
            "import unittest\nfrom pathlib import Path\n"
            "class Artifact(unittest.TestCase):\n"
            "    def test_create(self):\n"
            "        Path('.agentit/artifacts/new.bin').write_bytes(b'new output')\n")
        self.git("add", ".gitignore", "tests")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-qm", "artifact test")
        scope = self.project / ".agentit/artifacts"
        scope.mkdir()
        self.ledger["local_scopes"] = [{"path": str(scope), "resources": []}]
        self.assertTrue(self.review()["allowed"])
        result = apply_verification(self.project, explicit_signals=["publication"])
        self.assertFalse(cleanup.check(self.project)["allowed"])
        self.assertTrue(result["blocking_failed"], result)
        self.assertFalse(json.loads(Path(result["receipt_path"]).read_text())["passed"])
        (scope / "new.bin").unlink()
        self.assertTrue(self.review()["allowed"])
        completed = subprocess.run(
            [sys.executable, str(Path(__file__).resolve().parents[1] / "agentit"),
             "verify", "--project", str(self.project), "--signal", "publication", "--apply", "--format", "json"],
            capture_output=True, text=True)
        self.assertEqual(1, completed.returncode, completed.stdout + completed.stderr)
        self.assertTrue(json.loads(completed.stdout)["blocking_failed"])
        self.assertFalse(cleanup.check(self.project)["allowed"])

    def test_publication_rejects_inventory_drift_from_its_own_receipt_write(self):
        from router.verify import apply_verification
        scope = self.project / ".agentit/verify"
        scope.mkdir()
        self.ledger["local_scopes"] = [{"path": str(scope), "resources": []}]
        self.assertTrue(self.review()["allowed"])
        result = apply_verification(self.project, explicit_signals=["publication"], run_project_commands=False)
        self.assertFalse(cleanup.check(self.project)["allowed"])
        self.assertTrue(result["blocking_failed"], result)
        self.assertFalse(json.loads(Path(result["receipt_path"]).read_text())["passed"])


if __name__ == "__main__":
    unittest.main()
