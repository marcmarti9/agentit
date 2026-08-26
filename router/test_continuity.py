import stat
import tempfile
import unittest
from pathlib import Path

try:
    from .continuity import ensure_state_file, list_checkpoints, parse_state, resume_report, write_checkpoint
    from .project_signals import collect_project_signals
    from .verify import evaluate_done_claims
except ImportError:
    from continuity import ensure_state_file, list_checkpoints, parse_state, resume_report, write_checkpoint
    from project_signals import collect_project_signals
    from verify import evaluate_done_claims


class ContinuityAndProjectSignalTests(unittest.TestCase):
    def test_state_init_and_resume(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = ensure_state_file(root, goal="Ship continuity")
            self.assertEqual(root / ".agentit" / "STATE.md", path)
            self.assertTrue(path.is_file())
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)
            self.assertTrue(parse_state(path)["complete"])
            self.assertTrue(resume_report(root)["resumable"])

    def test_state_init_does_not_invent_semantic_defaults(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            body = ensure_state_file(root, goal="Sensitive task not yet decided").read_text(encoding="utf-8")
            for value in ("- Relevant packs: (unset)", "- Complexity: (unset)", "- Risk: (unset)", "- Topology: (unset)", "- Strong independent review required: (unset)"):
                self.assertIn(value, body)
            self.assertNotIn("- Topology: direct", body)

    def test_state_init_persists_explicit_ai_decision_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            body = ensure_state_file(root, goal="Implement auth boundary", decision={"relevant_packs": ["backend", "engineering"], "complexity": "substantial", "risk": "RISK_3", "topology": "writer_reviewer", "strong_review_required": True}).read_text(encoding="utf-8")
            self.assertIn("- Relevant packs: backend, engineering", body)
            self.assertIn("- Complexity: substantial", body)
            self.assertIn("- Risk: RISK_3", body)
            self.assertIn("- Topology: writer_reviewer", body)
            self.assertIn("- Strong independent review required: yes", body)

    def test_checkpoint_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = write_checkpoint(root, label="milestone", payload={"x": 1})
            self.assertTrue(path.is_file())
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)
            self.assertEqual(1, len(list_checkpoints(root)))

    def test_project_signals_detect_python_repo(self):
        signals = collect_project_signals(Path(__file__).resolve().parents[1])
        self.assertTrue(signals["available"])
        self.assertIn(signals["size_class"], {"tiny", "small", "medium", "large"})
        self.assertIn("python", signals["stack_markers"])

    def test_evaluate_done_claims_requires_receipt(self):
        denied = evaluate_done_claims(["done"], receipt=None)
        self.assertTrue(denied["applicable"])
        self.assertFalse(denied["allowed"])
        allowed = evaluate_done_claims(["done"], receipt={"mode": "apply", "passed": True, "blocking_failed": False, "receipt_path": "/tmp/r.json", "created_at": "now", "pending_checklists": []})
        self.assertTrue(allowed["allowed"])


if __name__ == "__main__":
    unittest.main()
