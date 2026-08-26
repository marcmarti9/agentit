"""Adversarial tests for the bounded Worker Context Contract."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from worker_context import (
    WorkerContextError,
    WorkerTaskSpec,
    assert_projection_complete,
    build_and_validate,
    build_worker_context,
    detect_instruction_conflicts,
    discover_project_instructions,
    project_preferences,
    render_worker_prompt,
    resolve_skills_projected,
    validate_for_spawn,
)

REPOSITORY = Path(__file__).resolve().parents[1]


class WorkerContextTests(unittest.TestCase):
    def test_project_instructions_and_subdir_scope_are_projected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "AGENTS.md").write_text("Root rule.\n", encoding="utf-8")
            sub = root / "packages" / "web"
            sub.mkdir(parents=True)
            (sub / "AGENTS.md").write_text("Subdir rule.\n", encoding="utf-8")
            found = discover_project_instructions(root, work_subdir="packages/web")
            self.assertEqual({"AGENTS.md", "packages/web/AGENTS.md"}, {item.path for item in found})

    def test_symlink_project_root_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            real = Path(tmp) / "real"
            real.mkdir()
            link = Path(tmp) / "link"
            link.symlink_to(real)
            with self.assertRaises(WorkerContextError):
                discover_project_instructions(link)

    def test_selected_skills_are_bounded_and_unknown_skill_fails_closed(self):
        catalog = [f"skill-{index}" for index in range(31)]
        projected = resolve_skills_projected(
            task_skills=["security-and-hardening"],
            manifest_skills=catalog,
            include_manifest_skills=True,
            known_repository_skills=[*catalog, "security-and-hardening"],
        )
        self.assertEqual(["security-and-hardening"], projected)
        with self.assertRaises(WorkerContextError):
            resolve_skills_projected(
                task_skills=["missing"],
                manifest_skills=[],
                include_manifest_skills=False,
                known_repository_skills={"known"},
            )

    def test_empty_skills_allowed(self):
        self.assertEqual(
            [],
            resolve_skills_projected(
                task_skills=[], manifest_skills=["a"], include_manifest_skills=False
            ),
        )

    def test_preferences_drop_secret_shaped_values(self):
        projected = project_preferences(
            {
                "user_style_preferences": {
                    "preferred_language": "es",
                    "testing_framework": "pytest",
                    "api_key": "nope",
                    "code_style": "sk-abcdefghijklmnopqrstuvwxyz012345",
                }
            }
        )
        self.assertEqual(
            {"preferred_language": "es", "testing_framework": "pytest"},
            projected,
        )

    def test_worker_projects_specialist_capabilities_least_privilege(self):
        with tempfile.TemporaryDirectory() as tmp:
            payload = build_worker_context(
                WorkerTaskSpec(
                    objective="Implement responsive account page",
                    specialist_ids=("frontend-developer",),
                    available_providers=("mcp.github", "local.filesystem"),
                    provider_host="codex",
                ),
                project_root=Path(tmp),
            )
        envelope = payload["worker_context"]["capability_envelope"]
        granted = {item["capability"]: item for item in envelope["grants"]}
        self.assertEqual("mcp.github", granted["repository.read"]["provider"])
        self.assertEqual(["repository:read"], granted["repository.read"]["permissions"])
        self.assertTrue(envelope["least_privilege"])

    def test_unresolved_or_uninventoried_capability_rejects_spawn(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            unresolved = build_worker_context(
                WorkerTaskSpec(
                    objective="Read repo",
                    required_capabilities=("repository.read",),
                    available_providers=(),
                    provider_host="codex",
                ),
                project_root=root,
            )
            with self.assertRaises(WorkerContextError):
                validate_for_spawn(unresolved)

            pending = build_worker_context(
                WorkerTaskSpec(
                    objective="Frontend task",
                    specialist_ids=("frontend-developer",),
                ),
                project_root=root,
            )
            self.assertEqual(
                "inventory_required",
                pending["worker_context"]["capability_envelope"]["status"],
            )
            with self.assertRaises(WorkerContextError):
                validate_for_spawn(pending)

    def test_tampered_permissions_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            payload = build_worker_context(
                WorkerTaskSpec(
                    objective="Read repo",
                    required_capabilities=("repository.read",),
                    available_providers=("mcp.github",),
                    provider_host="codex",
                ),
                project_root=Path(tmp),
            )
        payload["worker_context"]["capability_envelope"]["grants"][0]["permissions"].append(
            "repository:admin"
        )
        with self.assertRaises(WorkerContextError):
            validate_for_spawn(payload)

    def test_new_contract_projects_packs_references_without_legacy_tiers(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "AGENTS.md").write_text("Project rule.\n", encoding="utf-8")
            payload = build_worker_context(
                WorkerTaskSpec(
                    objective="Investigate and fix UI issue",
                    relevant_packs=("frontend", "engineering"),
                    skills=("debugging-and-error-recovery",),
                    references=("agentit://artifacts/ui-evidence.txt",),
                    parent_topology="writer_reviewer",
                    independent_review_required=True,
                ),
                project_root=root,
                known_repository_skills={"debugging-and-error-recovery"},
            )
        context = payload["worker_context"]
        self.assertEqual(2, context["schema_version"])
        self.assertEqual(["frontend", "engineering"], context["relevant_packs"])
        self.assertEqual(["agentit://artifacts/ui-evidence.txt"], context["references_projected"])
        self.assertNotIn("domain_pack", json.dumps(context))
        self.assertNotIn("craft_depth", json.dumps(context))
        self.assertNotIn("spend", context.get("orchestration", {}))
        prompt = render_worker_prompt(payload)
        self.assertIn("relevant_packs: frontend, engineering", prompt)
        self.assertIn("independent_review_required: true", prompt)

    def test_project_instructions_and_selected_skills_survive_projection(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "AGENTS.md").write_text(
                "Never use React.\nAll database queries must be parameterized.\n",
                encoding="utf-8",
            )
            payload = build_and_validate(
                WorkerTaskSpec(
                    objective="Add settings page",
                    skills=("security-and-hardening", "frontend-ui-engineering"),
                    verification="pytest -q",
                ),
                project_root=root,
                preferences={"user_style_preferences": {"testing_framework": "pytest"}},
                known_repository_skills={"security-and-hardening", "frontend-ui-engineering"},
                require_project_instructions=True,
            )
            context = payload["worker_context"]
            prompt = render_worker_prompt(payload)
            self.assertIn("Never use React", prompt)
            self.assertEqual(
                ["security-and-hardening", "frontend-ui-engineering"],
                context["skills_projected"],
            )
            self.assertIn("no commits", context["constraints"])

    def test_skip_project_instruction_projection_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "AGENTS.md").write_text("Rule.\n", encoding="utf-8")
            payload = build_worker_context(
                WorkerTaskSpec(objective="x"),
                project_root=root,
                skip_project_instructions=True,
            )
            with self.assertRaisesRegex(WorkerContextError, "fresh negligence"):
                assert_projection_complete(payload)

    def test_full_catalog_dump_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            catalog = [f"skill-{index}" for index in range(20)]
            payload = build_worker_context(
                WorkerTaskSpec(objective="x", skills=catalog),
                project_root=Path(tmp),
                known_repository_skills=catalog,
            )
            with self.assertRaisesRegex(WorkerContextError, "full-catalog"):
                validate_for_spawn(payload, repository_skill_count=20)

    def test_instruction_conflict_is_advisory_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "AGENTS.md").write_text("Never use React.\n", encoding="utf-8")
            sub = root / "ui"
            sub.mkdir()
            (sub / "AGENTS.md").write_text("Always use React.\n", encoding="utf-8")
            conflicts = detect_instruction_conflicts(
                discover_project_instructions(root, work_subdir="ui")
            )
            self.assertTrue(conflicts)

    def test_reviewer_is_read_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            payload = build_worker_context(
                WorkerTaskSpec(objective="Review diff", role="reviewer"),
                project_root=Path(tmp),
            )
        constraints = payload["worker_context"]["constraints"]
        self.assertTrue(any("read-only" in item for item in constraints))
        self.assertTrue(any("review only" in item for item in constraints))

    def test_secret_shaped_artifact_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(WorkerContextError):
                build_worker_context(
                    WorkerTaskSpec(
                        objective="x",
                        artifact_uris=("sk-abcdefghijklmnopqrstuvwxyz012345",),
                    ),
                    project_root=Path(tmp),
                )

    def test_cli_build_and_skip_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "AGENTS.md").write_text("Never use React.\n", encoding="utf-8")
            good = subprocess.run(
                [
                    "python3",
                    str(REPOSITORY / "router" / "worker_context.py"),
                    "build",
                    "--project",
                    str(root),
                    "--objective",
                    "Add settings page",
                    "--skill",
                    "security-and-hardening",
                    "--require-project-instructions",
                ],
                cwd=REPOSITORY,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(0, good.returncode, good.stderr)
            self.assertIn("worker_context", json.loads(good.stdout))

            bad = subprocess.run(
                [
                    "python3",
                    str(REPOSITORY / "router" / "worker_context.py"),
                    "build",
                    "--project",
                    str(root),
                    "--objective",
                    "Add settings page",
                    "--skip-project-instructions",
                ],
                cwd=REPOSITORY,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertNotEqual(0, bad.returncode)
            self.assertIn("fresh negligence", bad.stderr.lower())


if __name__ == "__main__":
    unittest.main()
