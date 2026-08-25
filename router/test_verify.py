import json
import subprocess
import tempfile
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[1]


class VerifyPlannerTests(unittest.TestCase):
    def test_unittest_project_does_not_invent_pytest_dependency(self):
        from router.verify import plan_verification

        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            tests = project / "tests"
            tests.mkdir()
            (tests / "test_example.py").write_text(
                "import unittest\n\nclass Example(unittest.TestCase):\n    pass\n",
                encoding="utf-8",
            )

            plan = plan_verification(project, task_text="fix behavior")
            probe = next(p for p in plan["probes"] if p["id"] == "project-test-suite")

            self.assertEqual(
                ["python3", "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"],
                probe["command"],
            )

    def test_pytest_config_takes_precedence_over_unittest_fallback(self):
        from router.verify import plan_verification

        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            (project / "tests").mkdir()
            (project / "pytest.ini").write_text("[pytest]\n", encoding="utf-8")

            plan = plan_verification(project, task_text="fix behavior")
            probe = next(p for p in plan["probes"] if p["id"] == "project-test-suite")

            self.assertEqual(["python3", "-m", "pytest", "-q"], probe["command"])

    def test_plain_pyproject_does_not_imply_pytest(self):
        from router.verify import plan_verification

        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            (project / "tests").mkdir()
            (project / "pyproject.toml").write_text(
                "[project]\nname = 'unittest-project'\n",
                encoding="utf-8",
            )

            plan = plan_verification(project, task_text="fix behavior")
            probe = next(p for p in plan["probes"] if p["id"] == "project-test-suite")

            self.assertEqual(
                ["python3", "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"],
                probe["command"],
            )

    def test_detects_python_and_plans_generic_blocking_probes(self):
        from router.verify import plan_verification

        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            (project / "pyproject.toml").write_text("[project]\nname='x'\n", encoding="utf-8")
            (project / "tests").mkdir()
            plan = plan_verification(project, task_text="implement feature with tests")
            ids = {p["id"] for p in plan["probes"]}
            self.assertIn("any", plan["signals"])
            self.assertIn("python", plan["signals"])
            self.assertIn("change-contract-red-green", ids)
            self.assertIn("acceptance-criteria", ids)
            self.assertIn("project-test-suite", ids)
            self.assertIn("no-secrets-in-diff", ids)
            self.assertEqual("none", plan["reference_gate"]["mode"])
            self.assertFalse(plan["reference_gate"]["required"])

    def test_tests_directory_without_pytest_config_uses_unittest(self):
        from router.verify import plan_verification

        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            (project / "tests").mkdir()
            plan = plan_verification(project, task_text="implement feature with tests")
            probe = next(
                item for item in plan["probes"] if item["id"] == "project-test-suite"
            )
            self.assertEqual(
                ["python3", "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"],
                probe["command"],
            )

    def test_free_text_does_not_create_semantic_signals(self):
        from router.verify import plan_verification

        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            plan = plan_verification(
                project,
                task_text="Add Supabase RLS auth frontend browser endpoint",
            )
            ids = {p["id"] for p in plan["probes"]}
            self.assertNotIn("postgres", plan["signals"])
            self.assertNotIn("auth", plan["signals"])
            self.assertNotIn("frontend", plan["signals"])
            self.assertNotIn("postgres-rls-discipline", ids)
            self.assertNotIn("auth-boundary", ids)
            self.assertNotIn("browser-smoke", ids)
            self.assertEqual("none", plan["reference_gate"]["mode"])

    def test_explicit_ai_signal_selects_postgres_probe(self):
        from router.verify import plan_verification

        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            plan = plan_verification(
                project,
                task_text="opaque human-readable receipt label",
                explicit_signals=["postgres"],
            )
            ids = {p["id"] for p in plan["probes"]}
            self.assertIn("postgres-rls-discipline", ids)
            self.assertIn("postgres", plan["signals"])
            self.assertEqual(["postgres"], plan["explicit_signals"])

    def test_reference_mode_is_explicit_not_inferred_from_task_text(self):
        from router.verify import plan_verification

        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            plan = plan_verification(
                project,
                task_text="prepare current Spanish tax report and premium website",
            )
            self.assertEqual("none", plan["reference_gate"]["mode"])
            self.assertFalse(plan["reference_gate"]["required"])

            explicit = plan_verification(
                project,
                task_text="opaque receipt label",
                reference_mode="live",
                reference_sources=["https://example.gov/current-rule"],
                reference_provenance_required=True,
            )
            self.assertEqual("live", explicit["reference_gate"]["mode"])
            self.assertTrue(explicit["reference_gate"]["required"])
            self.assertEqual(
                ["https://example.gov/current-rule"],
                explicit["reference_gate"]["selected_sources"],
            )
            self.assertTrue(explicit["reference_gate"]["provenance_required"])

    def test_reference_sources_rejected_when_mode_none(self):
        from router.verify import VerifyError, plan_verification

        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            with self.assertRaises(VerifyError):
                plan_verification(
                    project,
                    reference_mode="none",
                    reference_sources=["web-design-studio"],
                )

    def test_apply_runs_secret_script_and_writes_receipt(self):
        from router.verify import apply_verification

        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            (project / "README.md").write_text("ok\n", encoding="utf-8")
            receipt = apply_verification(
                project,
                task_text="docs only",
                run_project_commands=False,
            )
            self.assertTrue(Path(receipt["receipt_path"]).is_file())
            body = json.loads(Path(receipt["receipt_path"]).read_text(encoding="utf-8"))
            self.assertEqual(body["mode"], "apply")
            self.assertIn("pending_checklists", body)
            statuses = {p["id"]: p.get("status") for p in body["probes"]}
            self.assertEqual(statuses.get("secrets-scan-tree"), "passed")
            self.assertTrue(body["reference_gate"]["passed"])
            self.assertEqual("not_required", body["reference_gate"]["status"])

    def test_apply_blocks_selected_references_without_inspection_evidence(self):
        from router.verify import apply_verification

        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            (project / "README.md").write_text("ok\n", encoding="utf-8")
            receipt = apply_verification(
                project,
                task_text="reference-driven docs change",
                run_project_commands=False,
                reference_mode="catalog",
                reference_sources=["web-design-studio"],
            )
            self.assertFalse(receipt["passed"])
            self.assertTrue(receipt["blocking_failed"])
            self.assertEqual("failed", receipt["reference_gate"]["status"])
            self.assertTrue(
                any("no inspected-source evidence" in item for item in receipt["reference_gate"]["violations"])
            )

    def test_apply_reference_gate_passes_with_source_evidence_and_required_provenance(self):
        from router.verify import apply_verification

        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            (project / "README.md").write_text("ok\n", encoding="utf-8")
            receipt = apply_verification(
                project,
                task_text="reference-driven docs change",
                run_project_commands=False,
                reference_mode="mixed",
                reference_sources=[
                    "web-design-studio",
                    "https://example.com/current-docs",
                ],
                reference_evidence=[
                    "Inspected the web-design-studio pack and extracted structural-variety guidance",
                    "Verified current implementation constraints in official docs",
                ],
                reference_provenance_required=True,
                reference_provenance="docs/agentit/REFERENCES.md",
            )
            self.assertTrue(receipt["reference_gate"]["passed"])
            self.assertEqual("passed", receipt["reference_gate"]["status"])
            self.assertEqual("docs/agentit/REFERENCES.md", receipt["reference_gate"]["provenance"])

    def test_done_claim_gate_surfaces_reference_failure(self):
        from router.verify import evaluate_done_claims

        receipt = {
            "mode": "apply",
            "blocking_failed": True,
            "passed": False,
            "created_at": "2026-08-25T00:00:00+00:00",
            "pending_checklists": [],
            "reference_gate": {
                "required": True,
                "passed": False,
                "violations": ["no inspected-source evidence was recorded"],
            },
        }
        result = evaluate_done_claims(["done"], receipt=receipt)
        self.assertFalse(result["allowed"])
        self.assertTrue(any("reference gate" in item for item in result["violations"]))


class VerifyCliTests(unittest.TestCase):
    def test_agentit_verify_plan_lists_generic_probes_without_parsing_task(self):
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            (project / "package.json").write_text('{"name":"x"}\n', encoding="utf-8")
            completed = subprocess.run(
                [
                    str(REPOSITORY / "agentit"),
                    "verify",
                    "landing page UI change",
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
            self.assertIn("mode: plan", completed.stdout)
            self.assertIn("references: none", completed.stdout)
            self.assertIn("acceptance-criteria", completed.stdout)
            self.assertNotIn("browser-smoke", completed.stdout)

    def test_agentit_verify_json_exposes_explicit_reference_plan(self):
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            completed = subprocess.run(
                [
                    str(REPOSITORY / "agentit"),
                    "verify",
                    "opaque task label",
                    "--project",
                    str(project),
                    "--reference-mode",
                    "catalog",
                    "--reference-source",
                    "web-design-studio",
                    "--format",
                    "json",
                ],
                cwd=REPOSITORY,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=False,
            )
            self.assertEqual(0, completed.returncode, completed.stdout)
            payload = json.loads(completed.stdout)
            self.assertEqual("catalog", payload["reference_gate"]["mode"])
            self.assertEqual(["web-design-studio"], payload["reference_gate"]["selected_sources"])


if __name__ == "__main__":
    unittest.main()
