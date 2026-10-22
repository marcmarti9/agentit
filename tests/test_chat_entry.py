"""Portable chat delivery must retain complete core bytes and no implicit bodies."""
from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("build_chat_entry", ROOT / "scripts/build_chat_entry.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class ChatEntryTests(unittest.TestCase):
    def test_exact_core_bytes_survive_materialization(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for skill_id in builder.CORE:
                path = root / "skills" / skill_id / "SKILL.md"
                path.parent.mkdir(parents=True)
                path.write_bytes(f"---\r\nname: {skill_id}\r\n---\r\n\nFull body  \r\n".encode())
            output = builder.render(root).encode()
            for skill_id in builder.CORE:
                expected = (root / "skills" / skill_id / "SKILL.md").read_bytes()
                start = f"<!-- core-body:{skill_id}:start -->\n".encode()
                end = f"\n<!-- core-body:{skill_id}:end -->".encode()
                actual = output.split(start, 1)[1].split(end, 1)[0]
                self.assertEqual(expected, actual)

    def test_missing_core_fails_instead_of_generating_partial_entry(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(FileNotFoundError):
                builder.render(Path(directory))

    def test_committed_entry_has_no_drift(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts/build_chat_entry.py"), "--check"],
                                capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stderr)

    def test_only_core_is_embedded_and_access_limits_are_explicit(self):
        entry = builder.render()
        self.assertEqual(len(builder.CORE), entry.count("<!-- core-body:") // 2)
        self.assertIn("linked domain skills are not included", entry)
        self.assertIn("User instructions and host safety/permissions take precedence", entry)
        for skill_id in builder.CORE:
            body = (ROOT / "skills" / skill_id / "SKILL.md").read_text()
            self.assertIn(body, entry)


if __name__ == "__main__":
    unittest.main()
