"""Unit tests for user preferences memory and dotted key handling."""

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
        self.prefs_file = Path(self.tmpdir.name) / ".agentit" / "preferences.yaml"

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

    def test_router_integration_with_preferences(self) -> None:
        # Save custom preferences
        save_preferences(
            {
                "auto_jit_profiles": False,
                "auto_plan_mode": False,
                "user_style_preferences": {
                    "preferred_language": "en",
                    "testing_framework": "unittest",
                    "ui_styling": "custom_css",
                },
            },
            preferences_path=self.prefs_file,
        )

        res = route_task("optimiza esta consulta de base de datos", home=Path(self.tmpdir.name))
        self.assertIn("applied_preferences", res)
        self.assertEqual(res["applied_preferences"]["preferred_language"], "en")
        self.assertEqual(res["applied_preferences"]["testing_framework"], "unittest")
        self.assertEqual(res["jit_profile_recommendations"], [])


if __name__ == "__main__":
    unittest.main()
