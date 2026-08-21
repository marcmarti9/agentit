import tempfile
import unittest
from pathlib import Path

try:
    from .continuity import (
        ensure_state_file,
        list_checkpoints,
        parse_state,
        resume_report,
        write_checkpoint,
    )
    from .project_signals import collect_project_signals
    from .verify import evaluate_done_claims
except ImportError:
    from continuity import (
        ensure_state_file,
        list_checkpoints,
        parse_state,
        resume_report,
        write_checkpoint,
    )
    from project_signals import collect_project_signals
    from verify import evaluate_done_claims


class ContinuityAndProjectSignalTests(unittest.TestCase):
    def test_state_init_and_resume(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = ensure_state_file(root, goal="Ship continuity")
            self.assertTrue(path.is_file())
            parsed = parse_state(path)
            self.assertTrue(parsed["complete"])
            report = resume_report(root)
            self.assertTrue(report["resumable"])
            self.assertIn("protocol", report)

    def test_checkpoint_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = write_checkpoint(root, label="milestone", payload={"x": 1})
            self.assertTrue(path.is_file())
            listed = list_checkpoints(root)
            self.assertEqual(1, len(listed))

    def test_project_signals_detect_python_repo(self):
        signals = collect_project_signals(Path(__file__).resolve().parents[1])
        self.assertTrue(signals["available"])
        self.assertIn(signals["size_class"], {"tiny", "small", "medium", "large"})
        self.assertIn("python", signals["stack_markers"])

    def test_evaluate_done_claims_requires_receipt(self):
        denied = evaluate_done_claims(["done"], receipt=None)
        self.assertTrue(denied["applicable"])
        self.assertFalse(denied["allowed"])
        allowed = evaluate_done_claims(
            ["done"],
            receipt={
                "mode": "apply",
                "passed": True,
                "blocking_failed": False,
                "receipt_path": "/tmp/r.json",
                "created_at": "now",
                "pending_checklists": [],
            },
        )
        self.assertTrue(allowed["allowed"])


if __name__ == "__main__":
    unittest.main()
