"""Unit tests for user preferences memory and LLM decision-request projection."""

import os
import tempfile
import unittest
from pathlib import Path

from router.preferences import (
    get_preference,
    load_preferences,
    save_preferences,
    set_preference,
)
from router.route import route_task


class PreferencesTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.tmpdir = tempfile.TemporaryDirectory()
        self.home = Path(self.tmpdir.name)
        self.prefs_file = self.home / ".agentit" / "preferences.yaml"

    def tearDown(self) -> None:
        self.tmpdir.cleanup()

    def test_dotted_key_get_and_set(self) -> None:
        set_preference("user_style_preferences.ui_styling", "vanilla_css_oklch", preferences_path=self.prefs_file)
        val = get_preference("user_style_preferences.ui_styling", preferences_path=self.prefs_file)
        self.assertEqual(val, "vanilla_css_oklch")

        set_preference("nested.deeply.key", "value_123", preferences_path=self.prefs_file)
        val2 = get_preference("nested.deeply.key", preferences_path=self.prefs_file)
        self.assertEqual(val2, "value_123")

    def test_atomic_file_permissions(self) -> None:
        save_preferences({"test": 1}, preferences_path=self.prefs_file)
        self.assertTrue(self.prefs_file.is_file())
        st = os.stat(self.prefs_file)
        self.assertEqual(st.st_mode & 0o777, 0o600)

    def test_decision_request_projects_safe_preferences_without_semantic_routing(self) -> None:
        save_preferences(
            {
                "auto_jit_profiles": False,
                "auto_plan_mode": False,
                "parallelism_preference": "high",
                "user_style_preferences": {
                    "preferred_language": "en",
                    "testing_framework": "unittest",
                    "ui_styling": "custom_css",
                    "response_style": "terse",
                },
            },
            preferences_path=self.prefs_file,
        )

        res = route_task("optimiza esta consulta de base de datos", home=self.home)
        prefs = res["applied_preferences"]
        self.assertEqual(prefs["preferred_language"], "en")
        self.assertEqual(prefs["testing_framework"], "unittest")
        self.assertEqual(prefs["ui_styling"], "custom_css")
        self.assertEqual(prefs["parallelism_preference"], "high")
        self.assertFalse(prefs["auto_jit_profiles"])
        self.assertFalse(prefs["auto_plan_mode"])
        self.assertEqual("decision_required", res["status"])
        self.assertNotIn("category", res)


if __name__ == "__main__":
    unittest.main()
