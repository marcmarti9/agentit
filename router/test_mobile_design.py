"""Regression tests for the optional native-mobile Agentit surface."""

from __future__ import annotations

import unittest
from pathlib import Path

from router.profiles import load_catalog, resolve_profile

REPOSITORY = Path(__file__).resolve().parents[1]


class MobileDesignProfileTests(unittest.TestCase):
    def test_mobile_skill_is_opt_in_and_not_core(self) -> None:
        catalog = load_catalog(REPOSITORY / "profiles.yaml")
        core = resolve_profile("core", catalog, repo_root=REPOSITORY)
        mobile = resolve_profile("mobile", catalog, repo_root=REPOSITORY)

        self.assertIn("appllama-app-design-skill", mobile)
        self.assertNotIn("appllama-app-design-skill", core)
        self.assertIn("frontend-ui-engineering", mobile)


if __name__ == "__main__":
    unittest.main()
