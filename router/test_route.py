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
        self.assertEqual(result["subagents"]["recommended"], 0)
        self.assertFalse(result["subagents"]["hard_cap"])
        self.assertNotIn("semantic", result["compression"]["allowed"])

    def test_presentation_only_payment_wording_does_not_raise_sensitive_risk(self):
        result = self.route("Cambia el color del botón de pago en este CSS")

        self.assertEqual(result["risk"], "RISK_1")
        self.assertEqual(result["topology"], "direct")
        self.assertIn("presentation-only scope", result["signals"])

    def test_real_payment_implementation_is_not_hidden_by_css_wording(self):
        result = self.route("Implementa el flujo de pagos y añade CSS")

        self.assertEqual(result["risk"], "RISK_3")
        self.assertEqual(result["topology"], "writer_reviewer")
        self.assertIn("payment/data boundary", result["signals"])

    def test_production_css_change_keeps_the_production_safety_gate(self):
        result = self.route("Cambia el CSS en producción")

        self.assertEqual(result["risk"], "RISK_4")
        self.assertTrue(result["verification"]["dry_run_required"])

    def test_how_to_questions_are_explanations_not_implementations(self):
        for prompt in (
            "How do I implement login and session expiration?",
            "¿Cómo implemento el pago?",
        ):
            with self.subTest(prompt=prompt):
                result = self.route(prompt)

                self.assertEqual(result["risk"], "RISK_0")
                self.assertEqual(result["category"], "explanation")
                self.assertEqual(result["topology"], "direct")
                self.assertFalse(result["verification"]["independent_review"])

    def test_later_implementation_overrides_an_explanatory_prefix(self):
        result = self.route(
            "Explain what authentication is, then implement login and session expiration"
        )

        self.assertEqual(result["risk"], "RISK_3")
        self.assertEqual(result["topology"], "writer_reviewer")

    def test_review_only_sensitive_work_uses_audit(self):
        result = self.route("Revisa solo la implementación de login")

        self.assertEqual(result["risk"], "RISK_3")
        self.assertEqual(result["topology"], "audit")
        self.assertIn("independent safety review", result["signals"][-1])

    def test_signals_include_each_sensitive_boundary_detected(self):
        result = self.route("Implementa login y procesa pagos")

        self.assertIn("authentication/session boundary", result["signals"])
        self.assertIn("payment/data boundary", result["signals"])

    def test_auth_implementation_explains_writer_reviewer_decision(self):
        result = self.route("Implementa el login y la expiración de sesiones")

        self.assertEqual(result["topology"], "writer_reviewer")
        self.assertGreaterEqual(result["confidence"], 0.70)
        self.assertFalse(result["confidence_calibrated"])
        self.assertTrue(
            any("authentication" in signal for signal in result["signals"])
        )
        self.assertIn("direct", result["rejected_topologies"])
        self.assertIn("fan_out", result["rejected_topologies"])
        self.assertIn("audit", result["rejected_topologies"])
        self.assertIn("independent verification", result["rejected_topologies"]["direct"])

    def test_explanation_keeps_topology_reasons_explicit(self):
        result = self.route("Explícame qué es un hash de forma sencilla")

        self.assertEqual(result["topology"], "direct")
        self.assertIn("no read-only investigation", result["rejected_topologies"]["probe"])
        self.assertIn("no independent work", result["rejected_topologies"]["fan_out"])

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
            "Explain what a hash is and drop the production database",
            "Explain what a hash is\nDrop the production database",
            "Document chmod, then execute chmod 777 on /etc/app.conf",
            "Do not restore the backup; instead drop the production database",
            "Explica el concepto y elimina la tabla de producción",
            "Explica el concepto: elimina la tabla de producción",
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
        available = result["skills_available"]
        self.assertIn("design-taste-frontend", available)
        self.assertIn("marketing-and-growth", available)
        self.assertIn("marketingskills", result["skills_recommended_missing"])
        self.assert_skill_compatibility(result)

    def test_visual_redesign_selects_design_taste_with_frontend_ui(self):
        result = self.route("Rediseña visualmente esta interfaz.")

        self.assertEqual(result["category"], "design")
        available = result["skills_available"]
        self.assertIn("frontend-ui-engineering", available)
        self.assertIn("design-taste-frontend", available)
        self.assertIn("verification-before-completion", available)
        self.assertEqual(result["skills_recommended_missing"], [])
        self.assert_skill_compatibility(result)

    def test_sqlite_does_not_select_postgres_specific_guidance(self):
        result = self.route("Optimiza esta consulta SQLite.")

        selected_or_missing = set(result["skills_available"]) | set(
            result["skills_recommended_missing"]
        )
        self.assertEqual(result["category"], "database")
        self.assertNotIn("supabase-postgres-best-practices", selected_or_missing)
        self.assert_skill_compatibility(result)

    def test_generic_database_task_recommends_inspecting_the_stack(self):
        result = self.route("Optimiza esta consulta de base de datos.")

        selected_or_missing = set(result["skills_available"]) | set(
            result["skills_recommended_missing"]
        )
        self.assertEqual(result["category"], "database")
        self.assertNotIn("supabase-postgres-best-practices", selected_or_missing)
        self.assertIn("inspect_database_stack", result["routing_advice"])

    def test_postgresql_supabase_selects_installed_database_guidance(self):
        result = self.route("Optimiza esta consulta PostgreSQL en Supabase.")

        self.assertEqual(result["category"], "database")
        self.assertIn(
            "supabase-postgres-best-practices", result["skills_available"]
        )
        self.assertIn("verification-before-completion", result["skills_available"])
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
        self.assertFalse(result["subagents"]["hard_cap"])
        self.assertIsNone(result["subagents"]["max"])
        self.assertFalse(result["craft_depth_applies"])

    def test_natural_parallel_investigation_gets_fan_out_without_powerwords(self):
        result = self.route("Investiga en paralelo dos hipótesis independientes del bug")

        self.assertEqual(result["topology"], "fan_out")
        self.assertGreaterEqual(result["subagents"]["recommended"], 2)
        self.assertFalse(result["subagents"]["hard_cap"])
        self.assertIsNone(result["subagents"]["max"])
        self.assertTrue(result["subagents"]["requires_justification"])

    def test_multi_path_bugs_fan_out_without_jargon(self):
        result = self.route("fix bugs in auth.ts and billing.ts")

        self.assertEqual(result["topology"], "fan_out")
        self.assertGreaterEqual(result["subagents"]["recommended"], 2)
        self.assertIn("parallelism", result)
        self.assertGreaterEqual(result["parallelism"]["score"], 0.35)

    def test_natural_multi_agent_phrase_is_understood(self):
        result = self.route("usa varios agentes: implementa frontend y backend del checkout")

        self.assertEqual(result["topology"], "fan_out")
        self.assertGreaterEqual(result["subagents"]["recommended"], 2)

    def test_design_gets_craft_depth_backend_does_not(self):
        design = self.route("Rediseña visualmente esta landing portfolio")
        backend = self.route("Implementa un endpoint de perfiles con tests")

        self.assertTrue(design["craft_depth_applies"])
        self.assertIn(design["craft_depth"], {"standard", "polished", "studio"})
        self.assertEqual(design["domain_pack"], "design")
        self.assertFalse(backend["craft_depth_applies"])
        self.assertIsNone(backend["craft_depth"])

    def test_skill_budget_does_not_dump_catalog(self):
        result = self.route("Implementa un endpoint de perfiles con tests")

        budget = result["skill_budget"]
        self.assertEqual(budget["do_not_load"], "full_catalog")
        self.assertLessEqual(len(budget["load_now"]), budget["max_task_skill_bodies"])
        self.assertIn("token_estimate", result)
        self.assertTrue(result["token_estimate"]["not_a_bill"])

    def test_agentit_activation_requires_affirmative_intent(self):
        for prompt in (
            "Do not use Agentit, just explain hashing",
            "No uses Agentit; explícame qué es un hash",
            "Explain what Agentit is without enabling it",
            "Agentit is a portable orchestration harness",
        ):
            with self.subTest(prompt=prompt):
                result = self.route(prompt)
                self.assertFalse(result["activation"]["requested"])
                self.assertNotIn(
                    "using-agentit",
                    set(result["skills_available"])
                    | set(result["skills_recommended_missing"]),
                )

    def test_natural_multilingual_agentit_activation_is_recognized(self):
        for prompt in (
            "Use Agentit to implement this endpoint",
            "Usa Agentit para implementar este endpoint",
            "Utilise Agentit pour implémenter cet endpoint",
            "Activa el modo Agentit",
        ):
            with self.subTest(prompt=prompt):
                result = self.route(prompt)
                self.assertTrue(result["activation"]["requested"])
                self.assertIn(
                    "using-agentit",
                    set(result["skills_available"])
                    | set(result["skills_recommended_missing"]),
                )

    def test_vendor_specific_database_tasks_do_not_activate_supabase_profile(self):
        for prompt in (
            "Implement a database schema for a MySQL service",
            "Optimiza esta consulta SQLite",
        ):
            with self.subTest(prompt=prompt):
                result = self.route(prompt)
                self.assertEqual(result["domain_pack"], "data")
                self.assertNotIn("supabase", result["jit_profile_recommendations"])
                self.assertIn("backend", result["jit_profile_recommendations"])

    def test_postgres_task_activates_supabase_profile(self):
        result = self.route("Optimiza esta consulta PostgreSQL en Supabase")

        self.assertIn("supabase", result["jit_profile_recommendations"])

    def test_generic_database_task_keeps_stack_probe_and_neutral_profile(self):
        result = self.route("Optimiza esta consulta de base de datos")

        self.assertIn("inspect_database_stack", result["routing_advice"])
        self.assertEqual(result["jit_profile_recommendations"], ["backend"])

    def test_structural_architecture_plan_requires_critic(self):
        result = self.route("Plantea la arquitectura del sistema de notificaciones")

        self.assertTrue(result["critic_required"])
        self.assertGreaterEqual(result["subagents"]["recommended"], 1)
        self.assertEqual(result["domain_pack"], "engineering")

    def test_tdd_for_backup_service_is_testing_not_database_ops(self):
        result = self.route(
            "Implementa tests TDD para el servicio de backups de Digitem"
        )

        self.assertEqual(result["category"], "testing")
        self.assertIn("test-driven-development", result["skills_available"])
        self.assertNotIn(
            "supabase-postgres-best-practices",
            set(result["skills_available"]) | set(result["skills_recommended_missing"]),
        )
        self.assert_skill_compatibility(result)

    def test_implement_feature_recommends_verification_skill(self):
        result = self.route("Implementa una feature de perfiles con tests")

        self.assertEqual(result["topology"], "direct")
        available = set(result["skills_available"]) | set(
            result["skills_recommended_missing"]
        )
        self.assertIn("test-driven-development", available)
        self.assertIn("verification-before-completion", available)
        self.assert_skill_compatibility(result)

    def test_agentit_trace_feature_work_is_not_probe_topology(self):
        result = self.route(
            "Añade el comando agentit trace y tests para el router"
        )

        self.assertEqual(result["topology"], "direct")
        self.assertNotEqual(result["topology"], "probe")

    def test_frontend_route_derives_capabilities_from_semantic_specialist(self):
        result = route_task(
            "Implementa una interfaz responsive en React",
            home=self.home,
            provider_host="codex",
            available_providers=["mcp.github", "local.filesystem"],
        )

        self.assertIn("frontend-developer", result["specialists"])
        self.assertIn("repository.read", result["capabilities"]["required"])
        self.assertEqual(
            "mcp.github",
            next(
                grant["provider"]
                for grant in result["capability_envelope"]["grants"]
                if grant["capability"] == "repository.read"
            ),
        )
        self.assertTrue(result["capability_envelope"]["least_privilege"])


if __name__ == "__main__":
    unittest.main()
