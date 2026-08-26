from pathlib import Path
import unittest

from router.mcp_catalog import McpCatalogError, recommend_for_task

ROOT = Path(__file__).resolve().parents[1]


class ArchitecturePolicyTests(unittest.TestCase):
    def test_active_policy_files_do_not_reintroduce_programmatic_semantic_routing(self):
        active_files = [
            ROOT / "AGENTS.md",
            ROOT / "README.md",
            ROOT / "CONTRIBUTING.md",
            ROOT / "docs" / "AGENTIT_INTERVIEW_AND_PROVIDER_POLICY.md",
            ROOT / "docs" / "PROJECT_CONTINUITY.md",
            ROOT / "docs" / "REFERENCE_INTELLIGENCE.md",
            ROOT / "skills" / "using-agentit" / "SKILL.md",
            ROOT / "skills" / "using-agent-skills" / "SKILL.md",
            ROOT / "skills" / "specialist-agent-routing" / "SKILL.md",
        ]
        forbidden = (
            "router `token_estimate`",
            "Task routing uses ordinary language",
            "`router/route.py` como clasificador",
            "El router debe informar",
            "agentit trace",
        )
        for path in active_files:
            text = path.read_text(encoding="utf-8")
            for needle in forbidden:
                self.assertNotIn(needle, text, f"stale semantic routing policy in {path}: {needle}")

    def test_using_agentit_preserves_runtime_receipt_gate(self):
        text = (ROOT / "skills" / "using-agentit" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Loop/Graph runtime", text)
        self.assertIn("require fresh evidence before success", text)
        self.assertIn("Do not weaken a verifier", text)

    def test_agentit_is_agent_operated_not_human_cli_driven(self):
        harness = (ROOT / "skills" / "using-agentit" / "SKILL.md").read_text(encoding="utf-8")
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("The user should not need to know or type Agentit CLI commands", harness)
        self.assertIn("Mechanical commands are agent-facing implementation details", harness)
        self.assertIn("DISPATCH_DECISION: bare | agentit", agents)
        self.assertIn("If genuinely uncertain, choose Agentit", agents)

    def test_constructive_dissent_preserves_user_agency(self):
        harness = (ROOT / "skills" / "using-agentit" / "SKILL.md").read_text(encoding="utf-8")
        task_router = (ROOT / "skills" / "task-router" / "SKILL.md").read_text(encoding="utf-8")
        planning = (ROOT / "skills" / "planning-and-task-breakdown" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Constructive dissent", harness)
        self.assertIn("Preserve the user's final safe discretionary choice", harness)
        self.assertIn("Constructive dissent", task_router)
        self.assertIn("preserve the user's final safe discretionary choice", task_router)
        self.assertIn("Planning is not a rubber-stamp phase", planning)
        self.assertIn("let the user keep the original approach", planning)

    def test_runtime_packs_are_flat_and_skill_count_is_model_owned(self):
        paths = [
            ROOT / "AGENTS.md",
            ROOT / "agents" / "catalog.yaml",
            ROOT / "docs" / "REFERENCE_INTELLIGENCE.md",
            ROOT / "skills" / "using-agentit" / "SKILL.md",
            ROOT / "skills" / "using-agent-skills" / "SKILL.md",
            ROOT / "skills" / "using-agent-skills" / "references" / "packs.md",
            ROOT / "skills" / "task-router" / "SKILL.md",
            ROOT / "skills" / "specialist-agent-routing" / "SKILL.md",
        ]
        combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
        forbidden = (
            "pack_depth",
            "**essential candidates**",
            "**standard candidates**",
            "**deep candidates**",
            "choose depth:",
            "Usually 1–2",
            "Usually 2–4",
            "pack + depth",
        )
        for needle in forbidden:
            self.assertNotIn(needle, combined, f"rigid pack tier/count policy returned: {needle}")
        self.assertIn(
            "no fixed skill counts and no pack levels",
            (ROOT / "skills" / "using-agent-skills" / "SKILL.md").read_text(encoding="utf-8"),
        )
        self.assertIn(
            "no fixed minimum or maximum",
            (ROOT / "skills" / "task-router" / "SKILL.md").read_text(encoding="utf-8"),
        )

    def test_legacy_effort_and_public_working_state_are_absent(self):
        for path in (
            ROOT / "effort" / "levels.yaml",
            ROOT / "docs" / "PUBLIC_LAUNCH.md",
            ROOT / "docs" / "agentit" / "STATE.md",
            ROOT / "docs" / "agentit" / "LLM_NATIVE_ROUTING_REFACTOR.md",
            ROOT / "tasks" / "plan.md",
            ROOT / "tasks" / "todo.md",
            ROOT / "incubator" / "candidates.yaml",
            ROOT / "incubator" / "rejected.yaml",
        ):
            self.assertFalse(path.exists(), f"private/legacy artifact should not be public: {path}")

    def test_continuity_and_scout_are_private_local_state(self):
        continuity = (ROOT / "docs" / "PROJECT_CONTINUITY.md").read_text(encoding="utf-8")
        scout = (ROOT / "router" / "scout.py").read_text(encoding="utf-8")
        self.assertIn(".agentit/STATE.md", continuity)
        self.assertNotIn("`docs/agentit/STATE.md`", continuity)
        self.assertIn('".agentit" / "scout"', scout)
        self.assertNotIn(' / "incubator"', scout)

    def test_worker_contract_has_no_legacy_effort_fields(self):
        text = (ROOT / "router" / "worker_context.py").read_text(encoding="utf-8")
        for legacy in ("craft_depth", "domain_pack", "spend", "model_tier"):
            self.assertNotIn(legacy, text)
        self.assertIn("relevant_packs", text)
        self.assertIn("references_projected", text)

    def test_legacy_mcp_helper_is_exact_stack_only(self):
        self.assertEqual(recommend_for_task("developer_core")["stack"], "developer_core")
        with self.assertRaises(McpCatalogError):
            recommend_for_task("design a frontend and inspect the browser")


if __name__ == "__main__":
    unittest.main()
