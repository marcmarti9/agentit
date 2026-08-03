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
        payload = {"schema_version": 1, "entries": entries}
        self.registry_path.write_text(json.dumps(payload), encoding="utf-8")

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
        self.assertEqual(result["skills_recommended_missing"], [])
        self.assertEqual(result["skills"], result["skills_available"])

    def assert_missing(self, result):
        self.assertEqual(result["skills_available"], [])
        self.assertEqual(result["skills_recommended_missing"], ["marketingskills"])
        self.assertEqual(result["skills"], result["skills_available"])

    def test_registry_error_is_public_exception_type(self):
        self.assertIsNotNone(RegistryError)
        self.assertTrue(issubclass(RegistryError, Exception))

    def test_duplicate_entry_ids_are_rejected(self):
        (self.home / "skill").mkdir()
        self.write_registry([self.entry(), self.entry(state="DUPLICATED")])

        with self.assert_registry_error():
            self.route_marketing()

    def test_arbitrary_registry_state_is_rejected(self):
        (self.home / "skill").mkdir()
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
        (self.home / "skill").mkdir()
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
        (self.home / "skill").mkdir()
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
        (self.home / "skill").mkdir()
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
        home_skill.mkdir()
        repo_skill.mkdir()

        for path_template in ("${HOME}/skill", "${REPO_ROOT}/repo-skill"):
            with self.subTest(path_template=path_template):
                self.write_registry([self.entry(paths=[path_template])])
                self.assert_available(self.route_marketing())

    def test_path_template_cannot_escape_its_portable_root(self):
        self.write_registry([self.entry(paths=["${HOME}/../other-user/skill"])])

        with self.assert_registry_error():
            self.route_marketing()

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
