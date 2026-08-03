import unittest

try:
    from .route import route_task
except ImportError:  # unittest discover with router as the start directory
    from route import route_task


class RouterSafetyTests(unittest.TestCase):
    def test_informal_explanation_uses_terse_safe_without_skills(self):
        result = route_task("Explícame qué es un hash de forma sencilla")

        self.assertEqual(result["risk"], "RISK_0")
        self.assertEqual(result["output_profile"], "TERSE_SAFE")
        self.assertEqual(result["skills"], [])
        self.assertFalse(result["compression"]["semantic"])

    def test_trivial_css_change_stays_reversible_and_has_no_subagents(self):
        result = route_task("Cambia el color del botón en este CSS")

        self.assertEqual(result["risk"], "RISK_1")
        self.assertEqual(result["complexity"], "trivial")
        self.assertEqual(result["subagents"]["max"], 0)
        self.assertNotIn("semantic", result["compression"]["allowed"])

    def test_auth_feature_requires_security_and_fuller_context(self):
        result = route_task("Implementa el login y la expiración de sesiones")

        self.assertEqual(result["risk"], "RISK_3")
        self.assertIn("security-hardening", result["skills"])
        self.assertTrue(result["verification"]["independent_review"])
        self.assertFalse(result["compression"]["enabled"])

    def test_destructive_production_database_task_is_risk_four(self):
        result = route_task("Elimina la tabla de producción y restaura el backup")

        self.assertEqual(result["risk"], "RISK_4")
        self.assertEqual(result["output_profile"], "VERBOSE_ALLOWED")
        self.assertEqual(result["compression"]["mode"], "FULL_FIDELITY")
        self.assertTrue(result["verification"]["backup_required"])
        self.assertTrue(result["verification"]["dry_run_required"])
        self.assertTrue(result["verification"]["independent_review"])
        self.assertIn("pipelines", result["compression"]["deny_reasons"])

    def test_explicit_low_risk_cannot_lower_inferred_high_risk(self):
        result = route_task("Haz DROP DATABASE en producción", explicit_risk="RISK_0")

        self.assertEqual(result["risk"], "RISK_4")
        self.assertTrue(any("no puede reducir" in reason for reason in result["reasons"]))

    def test_pipeline_and_diff_are_never_compressed(self):
        result = route_task("Revisa este git diff y el pipeline antes del commit")

        self.assertIn("diff", result["content_types"])
        self.assertIn("pipelines", result["content_types"])
        self.assertFalse(result["compression"]["enabled"])

    def test_marketing_task_selects_specialized_skill(self):
        result = route_task("Audita el CRO y el copy de la landing")

        self.assertEqual(result["category"], "marketing")
        self.assertEqual(result["skills"], ["marketingskills"])

    def test_high_risk_marketing_keeps_security_gate(self):
        result = route_task("Audita pagos y datos personales en el funnel de marketing")

        self.assertEqual(result["risk"], "RISK_3")
        self.assertIn("security-hardening", result["skills"])
        self.assertIn("marketingskills", result["skills"])
        self.assertIsNone(result["reversible"])

    def test_single_agent_is_default_even_for_standard_development(self):
        result = route_task("Implementa una feature pequeña de perfiles")

        self.assertEqual(result["topology"], "direct")
        self.assertEqual(result["subagents"]["recommended"], 0)
        self.assertEqual(result["subagents"]["max"], 0)

    def test_explicit_independent_work_gets_bounded_fan_out_budget(self):
        result = route_task("Investiga en paralelo dos hipótesis independientes del bug")

        self.assertEqual(result["topology"], "probe")
        self.assertEqual(result["subagents"]["max"], 3)
        self.assertTrue(result["subagents"]["requires_justification"])


if __name__ == "__main__":
    unittest.main()
