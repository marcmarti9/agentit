import json
import subprocess
import tempfile
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[1]


def sample_decision():
    return {
        "schema_version": 1,
        "intent": "implement",
        "category": "testing",
        "complexity": "bounded",
        "risk": "RISK_2",
        "reversible": True,
        "topology": "direct",
        "domain_pack": "engineering",
        "public_visual": False,
        "greenfield_or_total_redesign": False,
        "craft_depth": None,
        "craft_depth_overridden": False,
        "destructive_data_operation": False,
        "skills": [],
        "specialists": [],
        "capabilities": {"required": [], "preferred": []},
        "delegation": {"parallelism": 1, "reason": ""},
        "verification": {
            "tests_required": True,
            "browser_required": False,
            "independent_review": False,
            "dry_run_required": False,
            "backup_required": False,
            "rollback_plan_required": False,
            "post_check_required": False,
        },
        "critic_required": False,
        "evidence_signals": [],
        "reasons": ["Classified by the host model from full context."],
    }


class TraceWriterTests(unittest.TestCase):
    def test_write_trace_without_decision_persists_request_not_fake_classification(self):
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
            body = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(body["schema_version"], 2)
            self.assertEqual(body["kind"], "decision_request")
            self.assertEqual(body["summary"]["status"], "decision_required")
            self.assertNotIn("risk", body["summary"])

    def test_write_trace_can_persist_validated_host_decision(self):
        from router.trace import write_trace

        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            payload = write_trace(
                "Implement tests",
                project_root=project,
                decision=sample_decision(),
                registry_path=REPOSITORY / "registry.yaml",
            )
            self.assertEqual("validated_decision", payload["kind"])
            self.assertEqual("RISK_2", payload["summary"]["risk"])
            self.assertEqual("testing", payload["summary"]["category"])


class TraceCliTests(unittest.TestCase):
    def test_agentit_trace_cli_writes_decision_request(self):
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
            self.assertIn("status: decision_required", completed.stdout)
            self.assertIn("classification_owner: host_llm", completed.stdout)
            traces = list((project / ".agentit" / "traces").glob("*.json"))
            self.assertEqual(1, len(traces))


if __name__ == "__main__":
    unittest.main()
