import tempfile
import unittest
from pathlib import Path

try:
    from .route import route_task
except ImportError:  # unittest discover with router as the start directory
    from route import route_task


class RouterSafetyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.home = Path(cls.temp_dir.name) / "home"
        for relative_path in (
            ".agents/skills/architect-orchestrator/SKILL.md",
            ".agents/skills/security-and-hardening/SKILL.md",
            ".agents/skills/frontend-ui-engineering/SKILL.md",
            ".agents/skills/supabase-postgres-best-practices/SKILL.md",
        ):
            skill_file = cls.home / relative_path
            skill_file.parent.mkdir(parents=True, exist_ok=True)
            skill_file.write_text("fixture\n", encoding="utf-8")

    @classmethod
    def tearDownClass(cls):
        cls.temp_dir.cleanup()

    def route(self, prompt, explicit_risk=None):
        return route_task(prompt, explicit_risk, home=self.home)

    def assert_destructive_gates_disabled(self, result):
        self.assertFalse(result["verification"]["backup_required"])
        self.assertFalse(result["verification"]["dry_run_required"])
        self.assertFalse(result["verification"]["independent_review"])
        self.assertFalse(result["verification"]["post_check_required"])

    def assert_skill_compatibility(self, result):
        self.assertEqual(result["skills"], result["skills_available"])
        self.assertFalse(
            set(result["skills_available"])
            & set(result["skills_recommended_missing"])
        )

    def test_informal_explanation_uses_terse_safe_without_skills(self):
        result = self.route("Explícame qué es un hash de forma sencilla")

        self.assertEqual(result["risk"], "RISK_0")
        self.assertEqual(result["output_profile"], "TERSE_SAFE")
        self.assertEqual(result["skills"], [])
        self.assertFalse(result["compression"]["semantic"])

    def test_trivial_css_change_stays_reversible_and_has_no_subagents(self):
        result = self.route("Cambia el color del botón en este CSS")

        self.assertEqual(result["risk"], "RISK_1")
        self.assertEqual(result["complexity"], "trivial")
        self.assertEqual(result["subagents"]["max"], 0)
        self.assertNotIn("semantic", result["compression"]["allowed"])

    def test_auth_feature_requires_security_and_fuller_context(self):
        result = self.route("Implementa el login y la expiración de sesiones")

        self.assertEqual(result["risk"], "RISK_3")
        self.assertIn("security-hardening", result["skills"])
        self.assertTrue(result["verification"]["independent_review"])
        self.assertFalse(result["compression"]["enabled"])

    def test_destructive_production_database_task_is_risk_four(self):
        result = self.route("Elimina la tabla de producción y restaura el backup")

        self.assertEqual(result["risk"], "RISK_4")
        self.assertEqual(result["output_profile"], "VERBOSE_ALLOWED")
        self.assertEqual(result["compression"]["mode"], "FULL_FIDELITY")
        self.assertTrue(result["verification"]["backup_required"])
        self.assertTrue(result["verification"]["dry_run_required"])
        self.assertTrue(result["verification"]["independent_review"])
        self.assertTrue(result["verification"]["post_check_required"])
        self.assertIn("pipelines", result["compression"]["deny_reasons"])

    def test_explaining_a_backup_does_not_trigger_operational_backup_gates(self):
        result = self.route("Explícame cómo funciona un backup.")

        self.assertEqual(result["risk"], "RISK_0")
        self.assertEqual(result["category"], "explanation")
        self.assert_destructive_gates_disabled(result)

    def test_documenting_chmod_does_not_trigger_permission_change_gates(self):
        result = self.route("Documenta cómo funciona chmod.")

        self.assertEqual(result["risk"], "RISK_1")
        self.assertEqual(result["category"], "documentation")
        self.assert_destructive_gates_disabled(result)

    def test_deliver_is_not_mistaken_for_the_live_environment_keyword(self):
        result = self.route("Deliver a landing page for a gym.")

        self.assertEqual(result["risk"], "RISK_2")
        self.assertEqual(result["category"], "marketing")
        self.assert_destructive_gates_disabled(result)

    def test_landing_for_backup_service_is_marketing_not_a_restore_operation(self):
        result = self.route("Diseña una landing para un servicio de backups.")

        self.assertEqual(result["risk"], "RISK_2")
        self.assertEqual(result["category"], "marketing")
        self.assert_destructive_gates_disabled(result)

    def test_explicitly_rejected_restore_does_not_trigger_execution_gates(self):
        result = self.route("Do not restore the backup; explain the policy instead.")

        self.assertEqual(result["risk"], "RISK_0")
        self.assert_destructive_gates_disabled(result)

    def test_later_destructive_clause_overrides_explanatory_prefix(self):
        prompts = (
            "Explain what a hash is, then drop the production database",
            "Document chmod, then execute chmod 777 on /etc/app.conf",
            "Do not restore the backup; instead drop the production database",
            "chmod 777 /etc/app.conf",
        )
        for prompt in prompts:
            with self.subTest(prompt=prompt):
                result = self.route(prompt)
                self.assertEqual(result["risk"], "RISK_4")
                self.assertTrue(result["verification"]["dry_run_required"])

    def test_live_reload_and_delete_button_mentions_are_not_operations(self):
        prompts = (
            "Run the live-reload development server",
            "Review the UI text that mentions a delete button",
            "Delete button copy from this interface",
            "Add a CSS drop shadow to the card",
            "Truncate this label to twenty characters",
            "Explain what data loss means",
            "Deploy a production-like local environment",
            "Create a backup of the development database",
        )
        for prompt in prompts:
            with self.subTest(prompt=prompt):
                result = self.route(prompt)
                self.assertNotEqual(result["risk"], "RISK_4")
                self.assertFalse(result["verification"]["backup_required"])
                self.assertFalse(result["verification"]["dry_run_required"])

    def test_verified_production_restore_requires_the_complete_safety_gate(self):
        result = self.route(
            "Restaura el backup verificado en la base de datos de producción."
        )

        self.assertEqual(result["risk"], "RISK_4")
        self.assertTrue(result["verification"]["backup_required"])
        self.assertTrue(result["verification"]["dry_run_required"])
        self.assertTrue(result["verification"]["independent_review"])
        self.assertTrue(result["verification"]["post_check_required"])
        self.assertTrue(result["verification"]["full_suite"])
        self.assertEqual(result["compression"]["mode"], "FULL_FIDELITY")

    def test_explicit_low_risk_cannot_lower_inferred_high_risk(self):
        result = self.route("Haz DROP DATABASE en producción", explicit_risk="RISK_0")

        self.assertEqual(result["risk"], "RISK_4")
        self.assertTrue(any("no puede reducir" in reason for reason in result["reasons"]))

    def test_pipeline_and_diff_are_never_compressed(self):
        result = self.route("Revisa este git diff y el pipeline antes del commit")

        self.assertIn("diff", result["content_types"])
        self.assertIn("pipelines", result["content_types"])
        self.assertFalse(result["compression"]["enabled"])

    def test_marketing_task_selects_specialized_skill(self):
        result = self.route("Audita el CRO y el copy de la landing.")

        self.assertEqual(result["category"], "marketing")
        self.assertEqual(result["skills_available"], [])
        self.assertEqual(result["skills_recommended_missing"], ["marketingskills"])
        self.assert_skill_compatibility(result)

    def test_visual_redesign_reports_unavailable_hallmark_recommendation(self):
        result = self.route("Rediseña visualmente esta interfaz.")

        self.assertEqual(result["category"], "design")
        self.assertEqual(result["skills_available"], ["frontend-ui-engineering"])
        self.assertEqual(result["skills_recommended_missing"], ["hallmark"])
        self.assert_skill_compatibility(result)

    def test_sqlite_does_not_select_postgres_specific_guidance(self):
        result = self.route("Optimiza esta consulta SQLite.")

        selected_or_missing = set(result["skills_available"]) | set(
            result["skills_recommended_missing"]
        )
        self.assertEqual(result["category"], "database")
        self.assertNotIn("supabase-postgres-best-practices", selected_or_missing)
        self.assert_skill_compatibility(result)

    def test_postgresql_supabase_selects_installed_database_guidance(self):
        result = self.route("Optimiza esta consulta PostgreSQL en Supabase.")

        self.assertEqual(result["category"], "database")
        self.assertEqual(
            result["skills_available"], ["supabase-postgres-best-practices"]
        )
        self.assertEqual(result["skills_recommended_missing"], [])
        self.assert_skill_compatibility(result)

    def test_high_risk_marketing_keeps_security_gate(self):
        result = self.route("Audita pagos y datos personales en el funnel de marketing")

        self.assertEqual(result["risk"], "RISK_3")
        self.assertIn("security-hardening", result["skills_available"])
        self.assertIn("architect-orchestrator", result["skills_available"])
        self.assertIn("marketingskills", result["skills_recommended_missing"])
        self.assert_skill_compatibility(result)
        self.assertIsNone(result["reversible"])

    def test_single_agent_is_default_even_for_standard_development(self):
        result = self.route("Implementa una feature pequeña de perfiles")

        self.assertEqual(result["topology"], "direct")
        self.assertEqual(result["subagents"]["recommended"], 0)
        self.assertEqual(result["subagents"]["max"], 0)

    def test_explicit_independent_work_gets_bounded_fan_out_budget(self):
        result = self.route("Investiga en paralelo dos hipótesis independientes del bug")

        self.assertEqual(result["topology"], "probe")
        self.assertEqual(result["subagents"]["max"], 3)
        self.assertTrue(result["subagents"]["requires_justification"])


if __name__ == "__main__":
    unittest.main()
