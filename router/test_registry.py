import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

try:
    from .route import (
        AVAILABLE_REGISTRY_STATES,
        DEFAULT_REGISTRY_PATH,
        RegistryError,
        load_registry,
        resolve_registry_path,
        route_task,
    )
except ImportError:  # unittest discover with router as the start directory
    try:
        from route import (
            AVAILABLE_REGISTRY_STATES,
            DEFAULT_REGISTRY_PATH,
            RegistryError,
            load_registry,
            resolve_registry_path,
            route_task,
        )
    except ImportError:  # keep discovery alive so a missing public API is a RED test
        try:
            from . import route as route_module
        except ImportError:
            import route as route_module

        route_task = route_module.route_task
        RegistryError = getattr(route_module, "RegistryError", None)


class RegistryRouteTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo_root = Path(self.temp_dir.name)
        self.home = self.repo_root / "home"
        self.home.mkdir()
        self.registry_path = self.repo_root / "registry.yaml"

    def tearDown(self):
        self.temp_dir.cleanup()

    def write_registry(self, entries):
        # Marketing/design routes recommend companion skill ids; keep fixtures complete.
        normalized = list(entries)
        known = {entry.get("id") for entry in normalized}
        for skill_id in (
            "design-taste-frontend",
            "marketing-and-growth",
            "verification-before-completion",
            "verification-gauntlet",
            "test-driven-development",
            "anti-ai-slop-writing",
            "using-agentit",
        ):
            if skill_id not in known:
                normalized.append(
                    self.entry(
                        skill_id=skill_id,
                        state="NOT_INSTALLED",
                        paths=[],
                    )
                )
        payload = {"schema_version": 1, "entries": normalized}
        self.registry_path.write_text(json.dumps(payload), encoding="utf-8")

    def install_skill(self, relative="skill"):
        skill_file = self.home / relative / "SKILL.md"
        skill_file.parent.mkdir(parents=True, exist_ok=True)
        skill_file.write_text("fixture\n", encoding="utf-8")
        return skill_file

    def entry(
        self,
        *,
        state="ACTIVE_GLOBAL",
        paths=None,
        essential_dependencies=None,
        skill_id="marketingskills",
    ):
        return {
            "id": skill_id,
            "kind": "skill",
            "state": state,
            "paths": paths if paths is not None else ["${HOME}/skill"],
            "essential_dependencies": (
                essential_dependencies
                if essential_dependencies is not None
                else []
            ),
        }

    def route_marketing(self):
        return route_task(
            "Audita el CRO y el copy de la landing.",
            registry_path=self.registry_path,
            home=self.home,
        )

    def assert_registry_error(self):
        if RegistryError is None:
            self.fail("route.RegistryError must be part of the public router API")
        return self.assertRaises(RegistryError)

    def assert_available(self, result):
        self.assertEqual(result["skills_available"], ["marketingskills"])
        missing = set(result["skills_recommended_missing"])
        self.assertIn("design-taste-frontend", missing)
        self.assertIn("marketing-and-growth", missing)
        self.assertEqual(result["skills"], result["skills_available"])

    def assert_missing(self, result):
        self.assertEqual(result["skills_available"], [])
        missing = set(result["skills_recommended_missing"])
        self.assertIn("marketingskills", missing)
        self.assertIn("design-taste-frontend", missing)
        self.assertIn("marketing-and-growth", missing)
        self.assertEqual(result["skills"], result["skills_available"])

    def test_registry_error_is_public_exception_type(self):
        self.assertIsNotNone(RegistryError)
        self.assertTrue(issubclass(RegistryError, Exception))

    def test_duplicate_entry_ids_are_rejected(self):
        self.install_skill()
        self.write_registry([self.entry(), self.entry(state="DUPLICATED")])

        with self.assert_registry_error():
            self.route_marketing()

    def test_arbitrary_registry_state_is_rejected(self):
        self.install_skill()
        self.write_registry([self.entry(state="READY_WHENEVER")])

        with self.assert_registry_error():
            self.route_marketing()

    def test_missing_registry_file_is_rejected(self):
        missing_path = self.repo_root / "missing-registry.yaml"

        with self.assert_registry_error():
            route_task(
                "Audita el CRO y el copy de la landing.",
                registry_path=missing_path,
                home=self.home,
            )

    def test_malformed_yaml_is_rejected(self):
        self.registry_path.write_text("entries: [unterminated", encoding="utf-8")

        with self.assert_registry_error():
            self.route_marketing()

    def test_registry_state_mutation_changes_missing_skill_to_available(self):
        self.install_skill()
        self.write_registry([self.entry(state="AVAILABLE_ON_DEMAND")])
        self.assert_missing(self.route_marketing())

        self.write_registry([self.entry(state="ACTIVE_GLOBAL")])
        self.assert_available(self.route_marketing())

    def test_active_entry_with_no_observed_path_is_reported_missing(self):
        self.write_registry(
            [self.entry(state="ACTIVE_GLOBAL", paths=["${HOME}/does-not-exist"])]
        )

        self.assert_missing(self.route_marketing())

    def test_active_entry_with_missing_essential_dependency_is_reported_missing(self):
        self.install_skill()
        self.write_registry(
            [
                self.entry(
                    essential_dependencies=["required-helper"]
                ),
                self.entry(
                    skill_id="required-helper",
                    state="NOT_INSTALLED",
                    paths=[],
                ),
            ]
        )

        self.assert_missing(self.route_marketing())

    def test_known_states_have_explicit_availability_semantics(self):
        self.install_skill()
        available_states = ("ACTIVE_GLOBAL", "DUPLICATED")
        incompatible_states = (
            "AVAILABLE_ON_DEMAND",
            "NOT_INSTALLED",
            "DISABLED",
            "ARCHIVED",
            "BROKEN",
            "SECURITY_REVIEW_REQUIRED",
            "UNKNOWN",
        )

        for state in available_states:
            with self.subTest(state=state):
                self.write_registry([self.entry(state=state)])
                self.assert_available(self.route_marketing())
        for state in incompatible_states:
            with self.subTest(state=state):
                self.write_registry([self.entry(state=state)])
                self.assert_missing(self.route_marketing())

    def test_home_and_repo_root_path_templates_are_portable(self):
        home_skill = self.home / "skill"
        repo_skill = self.repo_root / "repo-skill"
        self.install_skill()
        repo_skill.mkdir()
        (repo_skill / "SKILL.md").write_text("fixture\n", encoding="utf-8")

        for path_template in ("${HOME}/skill", "${REPO_ROOT}/repo-skill"):
            with self.subTest(path_template=path_template):
                self.write_registry([self.entry(paths=[path_template])])
                self.assert_available(self.route_marketing())

    def test_path_template_cannot_escape_its_portable_root(self):
        self.write_registry([self.entry(paths=["${HOME}/../other-user/skill"])])

        with self.assert_registry_error():
            self.route_marketing()

    def test_empty_directory_is_not_a_loadable_skill(self):
        (self.home / "skill").mkdir()
        self.write_registry([self.entry()])

        self.assert_missing(self.route_marketing())

    def test_symlinked_skill_file_is_not_loadable(self):
        outside = self.repo_root / "outside-SKILL.md"
        outside.write_text("fixture\n", encoding="utf-8")
        skill_dir = self.home / "skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").symlink_to(outside)
        self.write_registry([self.entry()])

        self.assert_missing(self.route_marketing())

    def test_resolved_path_cannot_escape_root_through_symlink(self):
        outside = self.repo_root / "outside"
        outside.mkdir()
        (outside / "SKILL.md").write_text("fixture\n", encoding="utf-8")
        (self.home / "skill").symlink_to(outside, target_is_directory=True)
        self.write_registry([self.entry()])

        with self.assert_registry_error():
            self.route_marketing()

    def test_malformed_operational_metadata_is_rejected(self):
        self.install_skill()
        malformed = self.entry()
        malformed["conflicts_with"] = "frontend-ui-engineering"
        self.write_registry([malformed])

        with self.assert_registry_error():
            self.route_marketing()

    def test_registry_conflict_suppresses_lower_priority_available_skill(self):
        for relative in ("frontend", "taste"):
            self.install_skill(relative)
        frontend = self.entry(
            skill_id="frontend-ui-engineering",
            paths=["${HOME}/frontend"],
        )
        frontend["priority"] = "on_demand"
        taste = self.entry(
            skill_id="design-taste-frontend",
            paths=["${HOME}/taste"],
        )
        taste["priority"] = "specialized"
        taste["conflicts_with"] = ["frontend-ui-engineering"]
        self.write_registry([frontend, taste])

        result = route_task(
            "Rediseña visualmente esta interfaz.",
            registry_path=self.registry_path,
            home=self.home,
        )

        self.assertEqual(result["skills_available"], ["frontend-ui-engineering"])
        self.assertEqual(
            result["skills_suppressed_conflicts"], ["design-taste-frontend"]
        )

        frontend["priority"] = "specialized"
        taste["priority"] = "core"
        self.write_registry([frontend, taste])
        inverse = route_task(
            "Rediseña visualmente esta interfaz.",
            registry_path=self.registry_path,
            home=self.home,
        )
        self.assertEqual(inverse["skills_available"], ["design-taste-frontend"])
        self.assertEqual(
            inverse["skills_suppressed_conflicts"], ["frontend-ui-engineering"]
        )

    def test_real_catalog_available_outputs_have_compatible_state_and_path(self):
        entries = load_registry(DEFAULT_REGISTRY_PATH)
        prompts = (
            "Implementa el login y la expiración de sesiones",
            "Rediseña visualmente esta interfaz.",
            "Optimiza esta consulta PostgreSQL en Supabase.",
            "Corrige este bug",
        )

        for prompt in prompts:
            with self.subTest(prompt=prompt):
                result = route_task(prompt)
                for skill_id in result["skills_available"]:
                    entry = entries[skill_id]
                    self.assertIn(entry["state"], AVAILABLE_REGISTRY_STATES)
                    self.assertTrue(
                        any(
                            resolve_registry_path(
                                template,
                                registry_path=DEFAULT_REGISTRY_PATH,
                                home=Path.home(),
                            ).exists()
                            for template in entry["paths"]
                        ),
                        skill_id,
                    )

    def test_cli_registry_failure_emits_no_invented_route_json(self):
        missing_path = self.repo_root / "missing.yaml"
        completed = subprocess.run(
            [
                sys.executable,
                str(Path(__file__).with_name("route.py")),
                "--registry",
                str(missing_path),
                "Audita el CRO de la landing",
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

        self.assertNotEqual(completed.returncode, 0)
        self.assertEqual(completed.stdout, "")
        self.assertIn("cannot read registry", completed.stderr)


if __name__ == "__main__":
    unittest.main()
