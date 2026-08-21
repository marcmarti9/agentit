import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

try:
    from .decision_contract import DecisionContractError, validate_decision
    from .route import route_task
except ImportError:  # unittest discover with router as start directory
    from decision_contract import DecisionContractError, validate_decision
    from route import route_task


REPOSITORY = Path(__file__).resolve().parents[1]


def decision(**overrides):
    payload = {
        "schema_version": 1,
        "intent": "implement",
        "category": "engineering",
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
        "reasons": ["Host model classified the task from full context."],
    }
    for key, value in overrides.items():
        payload[key] = value
    return payload


class LlmNativeDecisionTests(unittest.TestCase):
    def test_route_task_no_longer_classifies_prompt_semantics(self):
        result = route_task("Elimina la tabla de producción y restaura el backup")

        self.assertEqual("decision_required", result["status"])
        self.assertEqual("host_llm", result["classification_owner"])
        self.assertEqual("Elimina la tabla de producción y restaura el backup", result["task"])
        self.assertNotIn("risk", result)
        self.assertNotIn("category", result)
        self.assertNotIn("topology", result)
        self.assertIn("risk_rubric", result["protocol"])

    def test_same_protocol_is_used_without_forcing_same_answer(self):
        first = route_task("Explain backups")
        second = route_task("Drop the production database")

        self.assertEqual(first["protocol"], second["protocol"])
        self.assertNotEqual(first["task"], second["task"])

    def test_explicit_risk_is_a_floor_for_host_decision(self):
        request = route_task("Do the thing", explicit_risk="RISK_3")
        self.assertEqual("RISK_3", request["explicit_risk_floor"])

        with self.assertRaises(DecisionContractError):
            validate_decision(decision(risk="RISK_2"), explicit_risk="RISK_3")

    def test_valid_bounded_decision_passes(self):
        result = validate_decision(decision())

        self.assertEqual("valid", result["status"])
        self.assertEqual("host_llm", result["classification_owner"])
        self.assertEqual("RISK_2", result["decision"]["risk"])
        self.assertEqual([], result["policy_violations"])

    def test_risk_three_requires_independent_review(self):
        bad = decision(risk="RISK_3")
        with self.assertRaisesRegex(DecisionContractError, "independent_review"):
            validate_decision(bad)

        good = decision(risk="RISK_3")
        good["verification"]["independent_review"] = True
        self.assertEqual("valid", validate_decision(good)["status"])

    def test_risk_four_requires_operational_safety_gates(self):
        bad = decision(risk="RISK_4", reversible=False)
        bad["verification"]["independent_review"] = True
        with self.assertRaisesRegex(DecisionContractError, "RISK_4 requires"):
            validate_decision(bad)

        good = decision(risk="RISK_4", reversible=False)
        good["verification"].update(
            {
                "independent_review": True,
                "dry_run_required": True,
                "rollback_plan_required": True,
                "post_check_required": True,
            }
        )
        self.assertEqual("valid", validate_decision(good)["status"])

    def test_destructive_data_operation_requires_backup_and_risk_four(self):
        bad = decision(destructive_data_operation=True, reversible=False)
        with self.assertRaises(DecisionContractError):
            validate_decision(bad)

        good = decision(
            risk="RISK_4",
            reversible=False,
            destructive_data_operation=True,
        )
        good["verification"].update(
            {
                "independent_review": True,
                "dry_run_required": True,
                "backup_required": True,
                "rollback_plan_required": True,
                "post_check_required": True,
            }
        )
        self.assertEqual("valid", validate_decision(good)["status"])

    def test_public_visual_work_is_design_primary(self):
        bad = decision(public_visual=True, craft_depth="Polished")
        bad["verification"]["browser_required"] = True
        with self.assertRaisesRegex(DecisionContractError, "domain_pack=design"):
            validate_decision(bad)

        good = decision(
            intent="design",
            category="design",
            domain_pack="design",
            public_visual=True,
            craft_depth="Polished",
        )
        good["verification"]["browser_required"] = True
        self.assertEqual("valid", validate_decision(good)["status"])

    def test_greenfield_public_visual_defaults_to_studio_unless_overridden(self):
        bad = decision(
            intent="design",
            category="design",
            domain_pack="design",
            public_visual=True,
            greenfield_or_total_redesign=True,
            craft_depth="Polished",
        )
        bad["verification"]["browser_required"] = True
        with self.assertRaisesRegex(DecisionContractError, "defaults to Studio"):
            validate_decision(bad)

        bad["craft_depth_overridden"] = True
        self.assertEqual("valid", validate_decision(bad)["status"])

    def test_structural_work_requires_critic(self):
        with self.assertRaisesRegex(DecisionContractError, "critic_required"):
            validate_decision(decision(complexity="structural"))

        self.assertEqual(
            "valid",
            validate_decision(decision(complexity="structural", critic_required=True))["status"],
        )

    def test_fan_out_requires_real_parallelism_and_reason(self):
        with self.assertRaises(DecisionContractError):
            validate_decision(decision(topology="fan_out"))

        good = decision(
            topology="fan_out",
            delegation={"parallelism": 2, "reason": "Two independent repository investigations."},
        )
        self.assertEqual("valid", validate_decision(good)["status"])


class DecisionCliTests(unittest.TestCase):
    def test_cli_emits_decision_request_not_invented_route(self):
        completed = subprocess.run(
            [sys.executable, str(REPOSITORY / "router" / "route.py"), "Implement auth"],
            cwd=REPOSITORY,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertEqual("decision_required", payload["status"])
        self.assertNotIn("risk", payload)

    def test_cli_validates_host_decision(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "decision.json"
            path.write_text(json.dumps(decision()), encoding="utf-8")
            completed = subprocess.run(
                [
                    sys.executable,
                    str(REPOSITORY / "router" / "route.py"),
                    "--decision",
                    str(path),
                ],
                cwd=REPOSITORY,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
        self.assertEqual(0, completed.returncode, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertEqual("valid", payload["status"])


if __name__ == "__main__":
    unittest.main()
