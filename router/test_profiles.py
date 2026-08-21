import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[1]


class ProfileCatalogTests(unittest.TestCase):
    def test_growth_and_agency_profiles_add_real_skill_bodies(self):
        from router.profiles import load_catalog, resolve_profile

        catalog = load_catalog(REPOSITORY / "profiles.yaml")
        product = resolve_profile("product", catalog, repo_root=REPOSITORY)
        growth = resolve_profile("growth", catalog, repo_root=REPOSITORY)
        agency = resolve_profile("agency", catalog, repo_root=REPOSITORY)

        self.assertGreater(len(growth), len(product))
        self.assertIn("shipping-and-launch", growth)
        self.assertGreater(len(agency), len(growth))
        self.assertIn("incremental-implementation", agency)
        self.assertIn("git-workflow-and-versioning", agency)

    def test_core_profile_is_bounded_and_all_repository_skills_remain_catalogued(self):
        completed = subprocess.run(
            [
                "python3",
                str(REPOSITORY / "router" / "profiles.py"),
                "--repo-root",
                str(REPOSITORY),
                "--profile",
                "core",
                "--format",
                "json",
            ],
            cwd=REPOSITORY,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

        self.assertEqual(0, completed.returncode, completed.stderr)
        core = json.loads(completed.stdout)
        self.assertEqual(12, len(core))
        self.assertIn("using-agentit", core)
        self.assertIn("verification-gauntlet", core)
        self.assertIn("task-router", core)
        self.assertIn("using-agent-skills", core)

        all_skills = {
            path.parent.name
            for path in (REPOSITORY / "skills").rglob("SKILL.md")
        }
        self.assertGreater(len(all_skills), 30)

    def test_agency_profile_installs_its_distinct_operating_skills(self):
        applied = self.run_cli("enable", "agency", "--apply")

        self.assertEqual(0, applied.returncode, applied.stdout)
        skill_root = self.project / ".agents" / "skills"
        self.assertTrue((skill_root / "shipping-and-launch" / "SKILL.md").is_file())
        self.assertTrue((skill_root / "incremental-implementation" / "SKILL.md").is_file())
        self.assertTrue((skill_root / "git-workflow-and-versioning" / "SKILL.md").is_file())

    def test_enable_without_profile_name_emits_clean_error(self):
        result = self.run_cli("enable")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("enable requiere un nombre de perfil", result.stdout)
        self.assertNotIn("AttributeError", result.stdout)

    def test_disable_does_not_remove_unmanaged_or_modified_files(self):
        self.assertEqual(0, self.run_cli("enable", "supabase", "--apply").returncode)
        unmanaged = self.project / ".agents" / "skills" / "unmanaged" / "SKILL.md"
        unmanaged.parent.mkdir(parents=True)
        unmanaged.write_text("keep me\n", encoding="utf-8")
        managed = (
            self.project
            / ".agents"
            / "skills"
            / "supabase-postgres-best-practices"
            / "SKILL.md"
        )
        managed.write_text("modified by user\n", encoding="utf-8")

        disabled = self.run_cli("disable", "supabase", "--apply")

        self.assertNotEqual(0, disabled.returncode)
