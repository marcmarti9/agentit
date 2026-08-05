"""Adversarial tests for Worker Context Contract (GSD #671 class failures)."""

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


class DiscoverInstructionsTests(unittest.TestCase):
    def test_root_agents_and_claude_discovered(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "AGENTS.md").write_text("Never use React.\n", encoding="utf-8")
            (root / "CLAUDE.md").write_text("Always parameterize SQL.\n", encoding="utf-8")
            found = discover_project_instructions(root)
            basenames = {i.basename for i in found}
            self.assertEqual({"AGENTS.md", "CLAUDE.md"}, basenames)
            self.assertTrue(all(i.scope == "root" for i in found))

    def test_subdir_agents_discovered_with_work_subdir(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "AGENTS.md").write_text("Root rule A.\n", encoding="utf-8")
            pkg = root / "packages" / "web"
            pkg.mkdir(parents=True)
            (pkg / "AGENTS.md").write_text("Subdir rule B.\n", encoding="utf-8")
            found = discover_project_instructions(root, work_subdir="packages/web")
            paths = {i.path for i in found}
            self.assertIn("AGENTS.md", paths)
            self.assertIn("packages/web/AGENTS.md", paths)
            scopes = {i.path: i.scope for i in found}
            self.assertEqual("root", scopes["AGENTS.md"])
            self.assertEqual("subdir", scopes["packages/web/AGENTS.md"])

    def test_missing_instruction_files_are_ok(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            found = discover_project_instructions(root)
            self.assertEqual([], found)

    def test_symlink_project_root_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            real = Path(tmp) / "real"
            real.mkdir()
            link = Path(tmp) / "link"
            link.symlink_to(real)
            with self.assertRaises(WorkerContextError):
                discover_project_instructions(link)


class SkillsProjectionTests(unittest.TestCase):
    def test_task_skills_only_not_full_catalog(self):
        catalog = [f"skill-{i}" for i in range(31)]
        projected = resolve_skills_projected(
            task_skills=["security-and-hardening", "frontend-ui-engineering"],
            manifest_skills=catalog,
            include_manifest_skills=True,
            known_repository_skills=catalog
            + ["security-and-hardening", "frontend-ui-engineering"],
        )
        self.assertEqual(
            ["security-and-hardening", "frontend-ui-engineering"],
            projected,
        )
        self.assertLess(len(projected), 31)

    def test_unknown_skill_fails_closed(self):
        with self.assertRaises(WorkerContextError):
            resolve_skills_projected(
                task_skills=["does-not-exist"],
                manifest_skills=[],
                include_manifest_skills=False,
                known_repository_skills={"security-and-hardening"},
            )

    def test_manifest_only_when_requested_and_no_task_skills(self):
        projected = resolve_skills_projected(
            task_skills=[],
            manifest_skills=["a", "b"],
            include_manifest_skills=True,
        )
        self.assertEqual(["a", "b"], projected)

    def test_empty_skills_allowed_for_mechanical_task(self):
        projected = resolve_skills_projected(
            task_skills=[],
            manifest_skills=["a", "b"],
            include_manifest_skills=False,
        )
        self.assertEqual([], projected)


class PreferenceProjectionTests(unittest.TestCase):
    def test_projects_style_preferences_only(self):
        prefs = {
            "user_style_preferences": {
                "testing_framework": "pytest",
                "response_style": "terse",
                "api_key": "should-not-appear",
            },
            "other": "ignored",
        }
        projected = project_preferences(prefs)
        self.assertEqual("pytest", projected["testing_framework"])
        self.assertEqual("terse", projected["response_style"])
        self.assertNotIn("api_key", projected)

    def test_secret_shaped_values_dropped(self):
        prefs = {
            "user_style_preferences": {
                "preferred_language": "es",
                "code_style": "sk-abcdefghijklmnopqrstuvwxyz012345",
            }
        }
        projected = project_preferences(prefs)
        self.assertEqual({"preferred_language": "es"}, projected)


class Adversarial671Tests(unittest.TestCase):
    """Prove projection prevents fresh negligence; absence fails the gate."""

    def _fixture_project(self, root: Path) -> None:
        (root / "AGENTS.md").write_text(
            "# Project rules\n\nNever use React.\n"
            "All database queries must be parameterized.\n",
            encoding="utf-8",
        )
        (root / ".agentit").mkdir()
        manifest = {
            "profiles": ["frontend", "core"],
            "skills": {
                "security-and-hardening": {"managed": True},
                "frontend-ui-engineering": {"managed": True},
                "test-driven-development": {"managed": True},
            },
        }
        (root / ".agentit" / "skills-manifest.json").write_text(
            json.dumps(manifest), encoding="utf-8"
        )

    def test_worker_receives_project_instruction_never_use_react(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._fixture_project(root)
            payload = build_and_validate(
                WorkerTaskSpec(
                    objective="Add a settings page",
                    skills=["security-and-hardening", "frontend-ui-engineering"],
                    verification="pytest -q",
                    risk="RISK_2",
                ),
                project_root=root,
                preferences={
                    "user_style_preferences": {
                        "testing_framework": "pytest",
                        "response_style": "terse",
                    }
                },
                require_project_instructions=True,
                known_repository_skills={
                    "security-and-hardening",
                    "frontend-ui-engineering",
                    "test-driven-development",
                },
            )
            ctx = payload["worker_context"]
            joined = "\n".join(i["content"] for i in ctx["project_instructions"])
            self.assertIn("Never use React", joined)
            self.assertIn("parameterized", joined.lower())
            prompt = render_worker_prompt(payload)
            self.assertIn("Never use React", prompt)
            self.assertIn("security-and-hardening", prompt)
            self.assertEqual(
                ["security-and-hardening", "frontend-ui-engineering"],
                ctx["skills_projected"],
            )
            self.assertEqual("pytest", ctx["preferences_projected"]["testing_framework"])
            self.assertIn("no commits", ctx["constraints"])

    def test_skip_projection_fails_assert_and_spawn_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._fixture_project(root)
            payload = build_worker_context(
                WorkerTaskSpec(objective="Add a settings page", skills=["security-and-hardening"]),
                project_root=root,
                known_repository_skills={"security-and-hardening"},
                skip_project_instructions=True,
            )
            with self.assertRaises(WorkerContextError) as cm:
                assert_projection_complete(payload)
            self.assertIn("fresh negligence", str(cm.exception).lower())
            with self.assertRaises(WorkerContextError):
                validate_for_spawn(payload, require_project_instructions=True)

    def test_does_not_project_all_thirty_one_skills(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._fixture_project(root)
            full_catalog = [f"skill-{i:02d}" for i in range(31)]
            full_catalog.extend(
                ["security-and-hardening", "frontend-ui-engineering", "test-driven-development"]
            )
            payload = build_and_validate(
                WorkerTaskSpec(
                    objective="Harden login form",
                    skills=["security-and-hardening"],
                ),
                project_root=root,
                known_repository_skills=full_catalog,
                repository_skill_count=len(set(full_catalog)),
                max_skills=12,
            )
            skills = payload["worker_context"]["skills_projected"]
            self.assertEqual(["security-and-hardening"], skills)
            self.assertLess(len(skills), 31)

    def test_full_catalog_dump_rejected_by_spawn_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "AGENTS.md").write_text("ok\n", encoding="utf-8")
            catalog = [f"skill-{i}" for i in range(20)]
            payload = build_worker_context(
                WorkerTaskSpec(objective="x", skills=catalog),
                project_root=root,
                known_repository_skills=catalog,
            )
            with self.assertRaises(WorkerContextError) as cm:
                validate_for_spawn(payload, repository_skill_count=20)
            self.assertIn("full-catalog", str(cm.exception))


class PrecedenceTests(unittest.TestCase):
    def test_precedence_order_encoded(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "AGENTS.md").write_text("Always use React.\n", encoding="utf-8")
            payload = build_worker_context(
                WorkerTaskSpec(
                    objective="UI tweak",
                    explicit_user_instructions=["Never use React for this task"],
                    safety_constraints=["do not exfiltrate secrets"],
                    skills=[],
                ),
                project_root=root,
            )
            layers = payload["worker_context"]["effective_directives"]
            self.assertEqual(
                [
                    "safety",
                    "explicit_user_instruction",
                    "project_instruction",
                    "preferences",
                    "defaults",
                ],
                layers["precedence"],
            )
            self.assertIn(
                "Never use React for this task",
                layers["layers"]["explicit_user_instruction"],
            )
            self.assertTrue(
                any("Always use React" in x for x in layers["layers"]["project_instruction"])
            )
            self.assertIn("do not exfiltrate secrets", layers["layers"]["safety"])
            prompt = render_worker_prompt(payload)
            self.assertIn(
                "safety > explicit user instruction > project instruction",
                prompt,
            )


class ConflictAndRoleTests(unittest.TestCase):
    def test_root_vs_subdir_conflict_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "AGENTS.md").write_text("Never use React.\n", encoding="utf-8")
            sub = root / "apps" / "ui"
            sub.mkdir(parents=True)
            (sub / "AGENTS.md").write_text("Always use React.\n", encoding="utf-8")
            found = discover_project_instructions(root, work_subdir="apps/ui")
            conflicts = detect_instruction_conflicts(found)
            self.assertTrue(conflicts)
            payload = build_worker_context(
                WorkerTaskSpec(
                    objective="Change button",
                    work_subdir="apps/ui",
                    skills=[],
                ),
                project_root=root,
            )
            self.assertTrue(payload["worker_context"]["instruction_conflicts"])

    def test_reviewer_is_read_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "AGENTS.md").write_text("Secure coding required.\n", encoding="utf-8")
            payload = build_worker_context(
                WorkerTaskSpec(
                    objective="Review auth diff",
                    role="reviewer",
                    skills=["security-and-hardening"],
                ),
                project_root=root,
                known_repository_skills={"security-and-hardening"},
            )
            constraints = payload["worker_context"]["constraints"]
            self.assertTrue(any("read-only" in c for c in constraints))
            self.assertTrue(any("review only" in c for c in constraints))

    def test_implementer_vs_reviewer_roles_differ(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "AGENTS.md").write_text("x\n", encoding="utf-8")
            impl = build_worker_context(
                WorkerTaskSpec(objective="impl", role="implementer"),
                project_root=root,
            )
            rev = build_worker_context(
                WorkerTaskSpec(objective="rev", role="reviewer"),
                project_root=root,
            )
            self.assertEqual("implementer", impl["worker_context"]["role"])
            self.assertEqual("reviewer", rev["worker_context"]["role"])
            self.assertNotEqual(
                impl["worker_context"]["constraints"],
                rev["worker_context"]["constraints"],
            )


class ArtifactAndSecretTests(unittest.TestCase):
    def test_artifact_uri_projected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "AGENTS.md").write_text("ok\n", encoding="utf-8")
            payload = build_worker_context(
                WorkerTaskSpec(
                    objective="Continue from handoff",
                    artifact_uris=["agentit://artifacts/ref-abc123.txt"],
                ),
                project_root=root,
            )
            self.assertEqual(
                ["agentit://artifacts/ref-abc123.txt"],
                payload["worker_context"]["artifact_uris"],
            )
            prompt = render_worker_prompt(payload)
            self.assertIn("agentit://artifacts/ref-abc123.txt", prompt)

    def test_secret_shaped_artifact_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "AGENTS.md").write_text("ok\n", encoding="utf-8")
            with self.assertRaises(WorkerContextError):
                build_worker_context(
                    WorkerTaskSpec(
                        objective="x",
                        artifact_uris=["sk-abcdefghijklmnopqrstuvwxyz012345"],
                    ),
                    project_root=root,
                )

    def test_auditable_json_shape(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "AGENTS.md").write_text("Never use React.\n", encoding="utf-8")
            payload = build_and_validate(
                WorkerTaskSpec(
                    objective="Add form",
                    skills=["security-and-hardening", "frontend-ui-engineering"],
                    risk="RISK_2",
                    extra_constraints=["no dependency changes"],
                ),
                project_root=root,
                preferences={
                    "user_style_preferences": {
                        "testing_framework": "pytest",
                        "response_style": "terse",
                    }
                },
                known_repository_skills={
                    "security-and-hardening",
                    "frontend-ui-engineering",
                },
            )
            ctx = payload["worker_context"]
            self.assertEqual(1, ctx["schema_version"])
            self.assertEqual(["AGENTS.md"], ctx["project_instruction_paths"])
            self.assertEqual(
                ["security-and-hardening", "frontend-ui-engineering"],
                ctx["skills_projected"],
            )
            self.assertEqual("RISK_2", ctx["risk"])
            self.assertIn("no commits", ctx["constraints"])
            # JSON serializable audit object
            json.dumps(payload)


class CliTests(unittest.TestCase):
    def test_cli_build_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "AGENTS.md").write_text("Never use React.\n", encoding="utf-8")
            completed = subprocess.run(
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
            self.assertEqual(0, completed.returncode, completed.stderr)
            payload = json.loads(completed.stdout)
            self.assertIn("worker_context", payload)
            self.assertIn(
                "Never use React",
                payload["worker_context"]["project_instructions"][0]["content"],
            )

    def test_cli_skip_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "AGENTS.md").write_text("Never use React.\n", encoding="utf-8")
            completed = subprocess.run(
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
            self.assertNotEqual(0, completed.returncode)
            self.assertIn("fresh negligence", completed.stderr.lower())


if __name__ == "__main__":
    unittest.main()
