"""Regression tests for the opt-in pre-deploy app security gate."""

from __future__ import annotations

import unittest
from pathlib import Path

from router.profiles import load_catalog, resolve_profile

REPOSITORY = Path(__file__).resolve().parents[1]
SKILL = REPOSITORY / "skills" / "app-security-gate" / "SKILL.md"
STACK_REFERENCE = REPOSITORY / "skills" / "app-security-gate" / "references" / "stack-specific.md"


class AppSecurityGateProfileTests(unittest.TestCase):
    def test_security_gate_is_release_opt_in_and_not_core(self) -> None:
        catalog = load_catalog(REPOSITORY / "profiles.yaml")
        core = resolve_profile("core", catalog, repo_root=REPOSITORY)
        release = resolve_profile("release", catalog, repo_root=REPOSITORY)
        all_skills = resolve_profile("all", catalog, repo_root=REPOSITORY)

        self.assertNotIn("app-security-gate", core)
        self.assertIn("app-security-gate", release)
        self.assertIn("app-security-gate", all_skills)

    def test_security_gate_package_contains_required_contract(self) -> None:
        body = SKILL.read_text(encoding="utf-8")

        self.assertTrue(body.startswith("---\nname: app-security-gate\n"))
        self.assertIn("SECURITY GATE: PASS | BLOCKED", body)
        self.assertIn("Adversarial Retest Matrix", body)
        self.assertIn("security-and-hardening", body)
        self.assertIn("references/stack-specific.md", body)
        self.assertTrue(STACK_REFERENCE.is_file())


if __name__ == "__main__":
    unittest.main()
