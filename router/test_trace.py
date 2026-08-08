import json
import subprocess
import tempfile
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[1]


class TraceWriterTests(unittest.TestCase):
    def test_write_trace_persists_summary_under_project(self):
        from router.trace import write_trace

        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            payload = write_trace(
                "Implementa tests TDD para el servicio de backups",
                project_root=project,
                registry_path=REPOSITORY / "registry.yaml",
                home=Path.home(),
            )
            path = Path(payload["path"])
            self.assertTrue(path.is_file())
            self.assertEqual(path.parent.name, "traces")
            body = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(body["schema_version"], 1)
            self.assertEqual(body["summary"]["category"], "testing")
            self.assertIn("test-driven-development", body["summary"]["skills_available"])


class TraceCliTests(unittest.TestCase):
    def test_agentit_trace_cli_writes_file(self):
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            completed = subprocess.run(
                [
                    str(REPOSITORY / "agentit"),
                    "trace",
                    "Añade el comando agentit trace",
                    "--project",
                    str(project),
                    "--repo-root",
                    str(REPOSITORY),
                ],
                cwd=REPOSITORY,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=False,
            )
            self.assertEqual(0, completed.returncode, completed.stdout)
            self.assertIn("topology:", completed.stdout)
            self.assertIn("direct", completed.stdout)
            traces = list((project / ".agentit" / "traces").glob("*.json"))
            self.assertEqual(1, len(traces))


if __name__ == "__main__":
    unittest.main()
