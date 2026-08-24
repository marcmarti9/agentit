import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from router.verify_cli import main


class VerifyCliTests(unittest.TestCase):
    def _run_json(self, *args: str) -> dict:
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            code = main([*args, "--format", "json"])
        self.assertEqual(code, 0)
        return json.loads(stream.getvalue())

    def test_explicit_auth_signal_reaches_auth_probe(self):
        with tempfile.TemporaryDirectory() as tmp:
            payload = self._run_json(
                "changed login flow",
                "--project",
                tmp,
                "--signal",
                "auth",
            )
        self.assertIn("auth", payload["explicit_signals"])
        probe_ids = {probe["id"] for probe in payload["probes"]}
        self.assertIn("auth-boundary", probe_ids)

    def test_task_text_is_not_used_as_semantic_router(self):
        with tempfile.TemporaryDirectory() as tmp:
            payload = self._run_json(
                "changed auth login jwt flow",
                "--project",
                tmp,
            )
        self.assertEqual(payload["explicit_signals"], [])
        probe_ids = {probe["id"] for probe in payload["probes"]}
        self.assertNotIn("auth-boundary", probe_ids)

    def test_repeated_signals_are_supported(self):
        with tempfile.TemporaryDirectory() as tmp:
            payload = self._run_json(
                "changed API login flow",
                "--project",
                tmp,
                "--signal",
                "AUTH",
                "--signal",
                "api",
            )
        self.assertEqual(payload["explicit_signals"], ["api", "auth"])
        probe_ids = {probe["id"] for probe in payload["probes"]}
        self.assertIn("auth-boundary", probe_ids)
        self.assertIn("http-smoke", probe_ids)


if __name__ == "__main__":
    unittest.main()
