"""Unit tests for tool_filter, artifact_ref, and dedup context engines."""

import tempfile
import unittest
from pathlib import Path

from router.artifact_ref import create_artifact_reference
from router.dedup import ContextDeduplicator
from router.tool_filter import filter_tool_output


class ContextEnginesTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.tmpdir = tempfile.TemporaryDirectory()
        self.artifact_dir = Path(self.tmpdir.name) / ".agentit" / "artifacts"

    def tearDown(self) -> None:
        self.tmpdir.cleanup()

    def test_tool_filter_preserves_failures_and_summaries(self) -> None:
        raw_output = "\n".join([f"line {i}" for i in range(100)]) + "\n" + (
            "FAIL: test_something (test_mod.TestClass)\n"
            "Traceback (most recent call last):\n"
            "  File 'test.py', line 10, in test_something\n"
            "    self.assertEqual(1, 2)\n"
            "AssertionError: 1 != 2\n"
            "----------------------------------------------------------------------\n"
            "Ran 100 tests in 1.2s\n"
            "FAILED (failures=1)\n"
        )

        res = filter_tool_output(raw_output, artifact_dir=self.artifact_dir, max_lines=40)
        self.assertTrue(res["filtered"])
        self.assertIn("FAIL: test_something", res["content"])
        self.assertIn("AssertionError: 1 != 2", res["content"])
        self.assertIn("Ran 100 tests in 1.2s", res["content"])
        self.assertTrue(Path(res["full_log_path"]).is_file())

    def test_artifact_reference_creation(self) -> None:
        large_content = "\n".join([f"line content {i}" for i in range(200)])
        res = create_artifact_reference(
            large_content,
            description="Migration script",
            artifact_dir=self.artifact_dir,
            min_lines=150,
        )
        self.assertTrue(res["archived"])
        self.assertTrue(res["content_ref"].startswith("agentit://artifacts/"))
        self.assertTrue(Path(res["retrieval_path"]).is_file())

    def test_exact_deduplication(self) -> None:
        deduper = ContextDeduplicator(min_block_length=50)
        block = "This is a repeated context block with enough length to hash." * 3

        res1 = deduper.process_block(block)
        self.assertFalse(res1["duplicate"])

        res2 = deduper.process_block(block)
        self.assertTrue(res2["duplicate"])
        self.assertIn("Exact duplicate context omitted", res2["content"])


if __name__ == "__main__":
    unittest.main()
