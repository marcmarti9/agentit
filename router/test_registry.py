import json
import tempfile
import unittest
from pathlib import Path

try:
    from .registry import (
        AVAILABLE_REGISTRY_STATES,
        DEFAULT_REGISTRY_PATH,
        RegistryError,
        load_registry,
        resolve_registry_path,
        resolve_requested_skills,
    )
except ImportError:  # unittest discover with router as start directory
    from registry import (
        AVAILABLE_REGISTRY_STATES,
        DEFAULT_REGISTRY_PATH,
        RegistryError,
        load_registry,
        resolve_registry_path,
        resolve_requested_skills,
    )


class RegistryInventoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.home = self.root / "home"
        self.home.mkdir()
        self.registry = self.root / "registry.yaml"

    def tearDown(self):
        self.tmp.cleanup()

    def skill(self, name: str) -> Path:
        path = self.home / name / "SKILL.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("fixture\n", encoding="utf-8")
        return path

    def entry(
        self,
        entry_id: str,
        *,
        state: str = "ACTIVE_GLOBAL",
        paths=None,
        dependencies=None,
        signals=None,
    ):
        return {
            "id": entry_id,
            "kind": "skill",
            "state": state,
            "paths": paths if paths is not None else [f"${{HOME}}/{entry_id}"],
            "essential_dependencies": dependencies or [],
            "requires_signals_any": signals or [],
            "conflicts_with": [],
        }

    def write(self, entries):
        self.registry.write_text(
            json.dumps({"schema_version": 1, "entries": entries}),
            encoding="utf-8",
        )

    def test_registry_rejects_duplicate_ids(self):
        self.write([self.entry("x"), self.entry("x")])
        with self.assertRaisesRegex(RegistryError, "duplicate registry id"):
            load_registry(self.registry)

    def test_registry_rejects_unknown_state(self):
        self.write([self.entry("x", state="MAGIC")])
        with self.assertRaisesRegex(RegistryError, "unknown registry state"):
            load_registry(self.registry)

    def test_missing_registry_is_an_explicit_error(self):
        with self.assertRaisesRegex(RegistryError, "cannot read registry"):
            load_registry(self.root / "missing.yaml")

    def test_path_template_cannot_escape_portable_root(self):
        self.write([self.entry("x", paths=["${HOME}/../escape"])])
        with self.assertRaisesRegex(RegistryError, "escapes its root"):
            load_registry(self.registry)

    def test_resolve_registry_path_is_portable_and_bounded(self):
        self.write([self.entry("x")])
        load_registry(self.registry)
        resolved = resolve_registry_path(
            "${HOME}/x",
            registry_path=self.registry,
            home=self.home,
        )
        self.assertEqual(self.home / "x", resolved)

    def test_model_selected_skill_is_verified_not_selected_by_python(self):
        self.skill("frontend-ui-engineering")
        self.write([self.entry("frontend-ui-engineering")])

        result = resolve_requested_skills(
            ["frontend-ui-engineering"],
            registry_path=self.registry,
            home=self.home,
        )

        self.assertEqual(["frontend-ui-engineering"], result["requested"])
        self.assertEqual(["frontend-ui-engineering"], result["available"])
        self.assertEqual([], result["missing"])

    def test_unavailable_state_is_reported_missing(self):
        self.skill("x")
        self.write([self.entry("x", state="AVAILABLE_ON_DEMAND")])
        result = resolve_requested_skills(["x"], registry_path=self.registry, home=self.home)
        self.assertEqual([], result["available"])
        self.assertEqual(["x"], result["missing"])
        self.assertIn("state=AVAILABLE_ON_DEMAND", result["details"]["x"]["reason"])

    def test_empty_or_symlinked_skill_is_not_loadable(self):
        empty = self.home / "empty"
        empty.mkdir()
        outside = self.root / "outside.md"
        outside.write_text("fixture\n", encoding="utf-8")
        symlink_dir = self.home / "linked"
        symlink_dir.mkdir()
        (symlink_dir / "SKILL.md").symlink_to(outside)
        self.write([self.entry("empty"), self.entry("linked")])

        result = resolve_requested_skills(
            ["empty", "linked"], registry_path=self.registry, home=self.home
        )
        self.assertEqual(["empty", "linked"], result["missing"])

    def test_required_signal_is_checked_against_model_evidence(self):
        self.skill("postgres")
        self.write([self.entry("postgres", signals=["postgres", "supabase"])])

        missing = resolve_requested_skills(
            ["postgres"], registry_path=self.registry, home=self.home, signals=[]
        )
        self.assertEqual(["postgres"], missing["missing"])

        available = resolve_requested_skills(
            ["postgres"],
            registry_path=self.registry,
            home=self.home,
            signals=["postgres"],
        )
        self.assertEqual(["postgres"], available["available"])

    def test_essential_dependency_must_also_be_available(self):
        self.skill("main")
        self.write(
            [
                self.entry("main", dependencies=["helper"]),
                self.entry("helper", state="NOT_INSTALLED", paths=[]),
            ]
        )
        result = resolve_requested_skills(["main"], registry_path=self.registry, home=self.home)
        self.assertEqual(["main"], result["missing"])
        self.assertIn("dependency:helper", result["details"]["main"]["reason"])

    def test_unknown_requested_id_is_visible_not_invented(self):
        self.write([])
        result = resolve_requested_skills(["does-not-exist"], registry_path=self.registry, home=self.home)
        self.assertEqual(["does-not-exist"], result["missing"])
        self.assertEqual("unknown_registry_id", result["details"]["does-not-exist"]["reason"])

    def test_real_registry_loads_and_known_available_states_are_explicit(self):
        entries = load_registry(DEFAULT_REGISTRY_PATH)
        self.assertGreater(len(entries), 10)
        self.assertEqual({"ACTIVE_GLOBAL", "DUPLICATED"}, AVAILABLE_REGISTRY_STATES)


if __name__ == "__main__":
    unittest.main()
