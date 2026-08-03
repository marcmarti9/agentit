"""Comprehensive unit tests for Agentit context engines and CLI commands."""

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from router.artifact_ref import create_artifact_reference, resolve_agentit_uri
from router.dedup import ContextDeduplicator
from router.tool_filter import filter_tool_output

REPO_ROOT = Path(__file__).resolve().parents[1]
AGENTIT_CLI = REPO_ROOT / "agentit"


class ContextEnginesTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.tmpdir = tempfile.TemporaryDirectory()
        self.project_dir = Path(self.tmpdir.name)
        self.artifact_dir = self.project_dir / ".agentit" / "artifacts"

    def tearDown(self) -> None:
        self.tmpdir.cleanup()

    def test_persistent_cross_process_deduplication(self) -> None:
        session_id = "test-session-123"
        block = "Exact duplicate string block spanning multiple lines to trigger hash tracking.\n" * 5

        # Process 1
        deduper1 = ContextDeduplicator(session_id=session_id, project_dir=self.project_dir, min_block_length=50)
        res1 = deduper1.process_block(block)
        self.assertFalse(res1["duplicate"])

        # Process 2 (simulated separate process/invocation reading from disk)
        deduper2 = ContextDeduplicator(session_id=session_id, project_dir=self.project_dir, min_block_length=50)
        res2 = deduper2.process_block(block)
        self.assertTrue(res2["duplicate"])
        self.assertIn("Exact duplicate context omitted", res2["content"])

        # Verify 0600 file permissions on dedup.json
        dedup_file = self.project_dir / ".agentit" / "sessions" / session_id / "dedup.json"
        self.assertTrue(dedup_file.is_file())
        st = os.stat(dedup_file)
        self.assertEqual(st.st_mode & 0o777, 0o600)

    def test_artifact_reference_creation_and_uri_resolver(self) -> None:
        large_content = "\n".join([f"line content {i} - unique text data" for i in range(200)])
        res = create_artifact_reference(
            large_content,
            description="Migration script",
            artifact_dir=self.artifact_dir,
            min_lines=150,
        )
        self.assertTrue(res["archived"])
        uri = res["content_ref"]
        self.assertTrue(uri.startswith("agentit://artifacts/ref-"))

        # Resolve URI securely
        resolved = resolve_agentit_uri(uri, project_root=self.project_dir)
        self.assertTrue(resolved.is_file())
        self.assertEqual(resolved.read_text(encoding="utf-8"), large_content)

        # Reject path traversal
        with self.assertRaises(ValueError):
            resolve_agentit_uri("agentit://artifacts/../secret.txt", project_root=self.project_dir)

    def test_protected_content_type_matrix(self) -> None:
        diff_content = "diff --git a/file.py b/file.py\n+new line\n-old line\n" * 10
        # Protected content type 'diff' must NEVER use lossy tool filtering
        filtered = filter_tool_output(diff_content, artifact_dir=self.artifact_dir, content_type="diff")
        self.assertFalse(filtered["filtered"])
        self.assertIn("protected from lossy filtering", filtered.get("reason", ""))

        # But protected types CAN use exact archiving
        archived = create_artifact_reference(
            diff_content,
            description="Git diff",
            artifact_dir=self.artifact_dir,
            content_type="diff",
        )
        self.assertTrue(archived["archived"])

    def test_format_aware_tool_filter_adapters(self) -> None:
        # pytest adapter
        pytest_log = (
            "============================= FAILURES =============================\n"
            "___________________________ test_feature ___________________________\n"
            "def test_feature():\n"
            ">       assert 1 == 2\n"
            "E       AssertionError: assert 1 == 2\n"
            "========================= 1 failed in 0.12s =========================\n"
        ) + "\n".join([f"passed item {i}" for i in range(100)])

        res = filter_tool_output(pytest_log, artifact_dir=self.artifact_dir, adapter="pytest", max_lines=20)
        self.assertTrue(res["filtered"])
        self.assertIn("AssertionError: assert 1 == 2", res["content"])

        # generic adapter MUST NOT delete lines with error signals
        generic_log = "\n".join([f"normal line {i}" for i in range(100)]) + "\nCRITICAL ERROR: memory limit exceeded!\n" + "\n".join([f"tail {i}" for i in range(50)])
        res_gen = filter_tool_output(generic_log, artifact_dir=self.artifact_dir, adapter="generic", max_lines=20)
        self.assertTrue(res_gen["filtered"])
        self.assertIn("CRITICAL ERROR: memory limit exceeded!", res_gen["content"])

    def test_cli_artifact_and_context_commands(self) -> None:
        # 1. Archive via CLI
        sample_text = "\n".join([f"log entry {i}" for i in range(200)])
        archive_proc = subprocess.run(
            [str(AGENTIT_CLI), "context", "archive", sample_text, "--project", str(self.project_dir)],
            capture_output=True,
            text=True,
            check=True,
        )
        data = json.loads(archive_proc.stdout)
        uri = data["content_ref"]

        # 2. Get via CLI
        get_proc = subprocess.run(
            [str(AGENTIT_CLI), "artifact", "get", uri, "--project", str(self.project_dir)],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertEqual(get_proc.stdout.strip(), sample_text.strip())

        # 3. Read range via CLI
        read_proc = subprocess.run(
            [str(AGENTIT_CLI), "artifact", "read", uri, "--lines", "1:3", "--project", str(self.project_dir)],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("log entry 0", read_proc.stdout)
        self.assertIn("log entry 2", read_proc.stdout)

        # 4. Grep via CLI
        grep_proc = subprocess.run(
            [str(AGENTIT_CLI), "artifact", "grep", uri, "entry 150", "--project", str(self.project_dir)],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("151:log entry 150", grep_proc.stdout)


if __name__ == "__main__":
    unittest.main()
