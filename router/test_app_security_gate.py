"""Regression tests for Agentit's development security invariant."""

from __future__ import annotations

import unittest
from pathlib import Path

from router.profiles import load_catalog, resolve_profile

REPOSITORY = Path(__file__).resolve().parents[1]
SKILL = REPOSITORY / "skills" / "app-security-gate" / "SKILL.md"
STACK_REFERENCE = REPOSITORY / "skills" / "app-security-gate" / "references" / "stack-specific.md"
ROUTER_SKILL = REPOSITORY / "skills" / "task-router" / "SKILL.md"


class AppSecurityGateProfileTests(unittest.TestCase):
    def test_security_is_development_scoped_not_global_core(self) -> None:
        catalog = load_catalog(REPOSITORY / "profiles.yaml")
        core = resolve_profile("core", catalog, repo_root=REPOSITORY)
        frontend = resolve_profile("frontend", catalog, repo_root=REPOSITORY)
        backend = resolve_profile("backend", catalog, repo_root=REPOSITORY)
        supabase = resolve_profile("supabase", catalog, repo_root=REPOSITORY)
        release = resolve_profile("release", catalog, repo_root=REPOSITORY)
        all_skills = resolve_profile("all", catalog, repo_root=REPOSITORY)

        self.assertNotIn("security-and-hardening", core)
        self.assertNotIn("app-security-gate", core)

        for profile in (frontend, backend, supabase):
            self.assertIn("security-and-hardening", profile)
            self.assertIn("app-security-gate", profile)

        self.assertIn("security-and-hardening", release)
        self.assertIn("app-security-gate", release)
        self.assertIn("app-security-gate", all_skills)

    def test_router_defines_development_security_invariant(self) -> None:
        body = ROUTER_SKILL.read_text(encoding="utf-8")

        self.assertIn("## Development security invariant", body)
        self.assertIn("Do not rely on the user to ask for a security review", body)
        self.assertIn("For purely presentational edits", body)
        self.assertIn("Load `app-security-gate`", body)
        self.assertIn("FAST mode compatibility", body)

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
