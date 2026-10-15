"""CI scopes: don't run installers for documentation-only skill changes."""

import unittest

from scripts.ci_change_scope import content_only_path, needs_full_suite


class SkillChangeScopeTests(unittest.TestCase):
    def test_plain_skill_and_references_use_lightweight_checks(self):
        paths = [
            "skills/image-to-code/SKILL.md",
            "skills/playwright-cli/references/tracing.md",
            "skills/design-taste-frontend/library/directions.json",
            "skills/UPSTREAM_LOCK.json",
            "skills/UPSTREAM_SOURCES.md",
            "profiles.yaml",
            "references/agentit-skill-packs.md",
        ]
        self.assertTrue(all(map(content_only_path, paths)))
        self.assertFalse(needs_full_suite(paths))

    def test_readme_or_other_docs_do_not_require_full_installers(self):
        self.assertFalse(needs_full_suite(["README.md", "docs/JIT_SKILL_LOADING.md"]))

    def test_core_skill_edits_run_full_suite(self):
        for name in ("using-agentit", "task-router", "using-agent-skills"):
            with self.subTest(name=name):
                self.assertTrue(needs_full_suite([f"skills/{name}/SKILL.md"]))

    def test_executable_skill_content_runs_full_suite(self):
        for path in ("skills/example/scripts/setup.sh", "skills/example/scripts/lint.mjs", "skills/example/run.py"):
            with self.subTest(path=path):
                self.assertTrue(needs_full_suite([path]))

    def test_runtime_installers_ecc_and_workflows_run_full_suite(self):
        for path in (
            "router/skill_loader.py",
            "bootstrap.py",
            ".github/workflows/ci.yml",
            "vendor/ecc/skills/api-design/SKILL.md",
            "scripts/sync_upstream_skills.py",
        ):
            with self.subTest(path=path):
                self.assertTrue(needs_full_suite(["skills/safe/SKILL.md", path]))

    def test_empty_diff_fails_closed_to_full_suite(self):
        self.assertTrue(needs_full_suite([]))


if __name__ == "__main__":
    unittest.main()
