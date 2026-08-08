import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[1]


class ProfileCatalogTests(unittest.TestCase):
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
        self.assertEqual(11, len(core))
        self.assertIn("using-agentit", core)
        self.assertIn("task-router", core)
        self.assertIn("using-agent-skills", core)

        all_skills = {
            path.parent.name
            for path in (REPOSITORY / "skills").glob("*/SKILL.md")
        }
        all_result = subprocess.run(
            [
                "python3",
                str(REPOSITORY / "router" / "profiles.py"),
                "--repo-root",
                str(REPOSITORY),
                "--profile",
                "all",
                "--format",
                "json",
            ],
            cwd=REPOSITORY,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(0, all_result.returncode, all_result.stderr)
        self.assertEqual(all_skills, set(json.loads(all_result.stdout)))

    def test_unknown_profile_fails_closed(self):
        completed = subprocess.run(
            [
                "python3",
                str(REPOSITORY / "router" / "profiles.py"),
                "--repo-root",
                str(REPOSITORY),
                "--profile",
                "does-not-exist",
            ],
            cwd=REPOSITORY,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

        self.assertNotEqual(0, completed.returncode)
        self.assertEqual("", completed.stdout)
        self.assertIn("unknown profile", completed.stderr)


class ProjectProfileCliTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.project = Path(self.temporary_directory.name) / "project"
        self.project.mkdir()

    def tearDown(self):
        self.temporary_directory.cleanup()

    def run_cli(self, *args):
        environment = os.environ.copy()
        return subprocess.run(
            [
                str(REPOSITORY / "agentit"),
                *args,
                "--project",
                str(self.project),
            ],
            cwd=REPOSITORY,
            env=environment,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )

    def test_enable_is_plan_first_and_apply_creates_manifested_project_skills(self):
        plan = self.run_cli("enable", "supabase")
        self.assertEqual(0, plan.returncode, plan.stdout)
        self.assertIn("MODO PLAN", plan.stdout)
        self.assertFalse((self.project / ".agents").exists())

        applied = self.run_cli("enable", "supabase", "--apply")
        self.assertEqual(0, applied.returncode, applied.stdout)
        manifest = self.project / ".agentit" / "skills-manifest.json"
        self.assertTrue(manifest.is_file())
        payload = json.loads(manifest.read_text(encoding="utf-8"))
        self.assertEqual(["supabase"], payload["profiles"])
        self.assertTrue(
            (self.project / ".agents" / "skills" / "supabase-postgres-best-practices" / "SKILL.md").is_file()
        )
        self.assertTrue(
            (
                self.project
                / ".agents"
                / "skills"
                / "supabase-postgres-best-practices"
                / "references"
                / "_sections.md"
            ).is_file()
        )

    def test_activate_is_an_enable_alias(self):
        activated = self.run_cli("activate", "core")

        self.assertEqual(0, activated.returncode, activated.stdout)
        self.assertIn("MODO PLAN", activated.stdout)

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
        self.assertEqual("keep me\n", unmanaged.read_text(encoding="utf-8"))
        self.assertEqual("modified by user\n", managed.read_text(encoding="utf-8"))

    def test_disable_removes_only_unmodified_managed_profile_files(self):
        enabled = self.run_cli("enable", "frontend", "--apply")
        self.assertEqual(0, enabled.returncode, enabled.stdout)

        disabled = self.run_cli("disable", "frontend", "--apply")

        self.assertEqual(0, disabled.returncode, disabled.stdout)
        self.assertFalse((self.project / ".agents" / "skills").exists())
        manifest = self.project / ".agentit" / "skills-manifest.json"
        payload = json.loads(manifest.read_text(encoding="utf-8"))
        self.assertEqual([], payload["profiles"])
        self.assertEqual({}, payload["skills"])

    def test_matching_preexisting_skill_is_not_adopted_or_removed(self):
        preexisting = (
            self.project
            / ".agents"
            / "skills"
            / "supabase-postgres-best-practices"
            / "SKILL.md"
        )
        source = (
            REPOSITORY
            / "skills"
            / "supabase-postgres-best-practices"
            / "SKILL.md"
        )
        preexisting.parent.mkdir(parents=True)
        preexisting.write_bytes(source.read_bytes())

        self.assertEqual(0, self.run_cli("enable", "supabase", "--apply").returncode)
        self.assertEqual(0, self.run_cli("disable", "supabase", "--apply").returncode)

        self.assertTrue(preexisting.is_file())

    def test_matching_preexisting_skill_stays_unmanaged_across_profile_overlap(self):
        preexisting = self.project / ".agents" / "skills" / "task-router" / "SKILL.md"
        source = REPOSITORY / "skills" / "task-router" / "SKILL.md"
        preexisting.parent.mkdir(parents=True)
        preexisting.write_bytes(source.read_bytes())

        self.assertEqual(0, self.run_cli("enable", "core", "--apply").returncode)
        self.assertEqual(0, self.run_cli("enable", "frontend", "--apply").returncode)
        self.assertEqual(0, self.run_cli("disable", "frontend", "--apply").returncode)
        self.assertEqual(0, self.run_cli("disable", "core", "--apply").returncode)

        self.assertTrue(preexisting.is_file())

    def test_manifest_symlink_is_rejected_before_installing_project_skills(self):
        manifest = self.project / ".agentit" / "skills-manifest.json"
        manifest.parent.mkdir()
        manifest.symlink_to(self.project / "missing-manifest.json")
        before = {
            path.relative_to(self.project).as_posix()
            for path in self.project.rglob("*")
        }

        result = self.run_cli("enable", "core", "--apply")

        self.assertNotEqual(0, result.returncode, result.stdout)
        self.assertEqual(before, {
            path.relative_to(self.project).as_posix()
            for path in self.project.rglob("*")
        })
        self.assertTrue(manifest.is_symlink())

    def test_manifest_keeps_installed_hash_when_source_changes(self):
        repository = Path(self.temporary_directory.name) / "repository"
        shutil.copytree(
            REPOSITORY,
            repository,
            symlinks=True,
            ignore=shutil.ignore_patterns(".git", "__pycache__", "backups"),
        )

        def run_fixture(*args):
            return subprocess.run(
                [
                    str(repository / "agentit"),
                    *args,
                    "--repo-root",
                    str(repository),
                    "--project",
                    str(self.project),
                ],
                cwd=repository,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=False,
            )

        enabled = run_fixture("enable", "core", "--apply")
        self.assertEqual(0, enabled.returncode, enabled.stdout)
        enabled = run_fixture("enable", "frontend", "--apply")
        self.assertEqual(0, enabled.returncode, enabled.stdout)
        manifest = self.project / ".agentit" / "skills-manifest.json"
        before = json.loads(manifest.read_text(encoding="utf-8"))
        installed_hash = before["skills"]["task-router"]["installed_sha256"]
        source = repository / "skills" / "task-router" / "SKILL.md"
        source.write_text(source.read_text(encoding="utf-8") + "source update\n", encoding="utf-8")

        disabled = run_fixture("disable", "frontend", "--apply")

        self.assertEqual(0, disabled.returncode, disabled.stdout)
        after = json.loads(manifest.read_text(encoding="utf-8"))
        self.assertEqual(installed_hash, after["skills"]["task-router"]["installed_sha256"])
        self.assertNotEqual(installed_hash, after["skills"]["task-router"]["source_sha256"])
        self.assertEqual(0, run_fixture("disable", "core", "--apply").returncode)
