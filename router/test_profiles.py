import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[1]
PRIVATE_SKILL_ROOT = Path(".agentit") / "profile-skills"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


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

    def test_core_profile_is_minimal_and_all_repository_skills_remain_catalogued(self):
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
        self.assertEqual(["using-agentit", "task-router", "using-agent-skills"], core)

        all_skills = {
            path.parent.name for path in (REPOSITORY / "skills").glob("*/SKILL.md")
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
            [str(REPOSITORY / "agentit"), *args, "--project", str(self.project)],
            cwd=REPOSITORY,
            env=environment,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )

    def private_skill(self, skill_id: str) -> Path:
        return self.project / PRIVATE_SKILL_ROOT / skill_id / "SKILL.md"

    def test_enable_is_plan_first_and_apply_keeps_profile_skills_private(self):
        plan = self.run_cli("enable", "supabase")
        self.assertEqual(0, plan.returncode, plan.stdout)
        self.assertIn("MODO PLAN", plan.stdout)
        self.assertFalse((self.project / ".agents").exists())
        self.assertFalse((self.project / PRIVATE_SKILL_ROOT).exists())

        applied = self.run_cli("enable", "supabase", "--apply")
        self.assertEqual(0, applied.returncode, applied.stdout)
        manifest = self.project / ".agentit" / "skills-manifest.json"
        self.assertTrue(manifest.is_file())
        payload = json.loads(manifest.read_text(encoding="utf-8"))
        self.assertEqual(["supabase"], payload["profiles"])
        self.assertTrue(self.private_skill("supabase-postgres-best-practices").is_file())
        self.assertTrue(
            (
                self.project
                / PRIVATE_SKILL_ROOT
                / "supabase-postgres-best-practices"
                / "references"
                / "_sections.md"
            ).is_file()
        )
        self.assertFalse((self.project / ".agents").exists())
        self.assertTrue(
            payload["skills"]["supabase-postgres-best-practices"]["destination"].startswith(
                ".agentit/profile-skills/"
            )
        )

    def test_activate_is_an_enable_alias(self):
        activated = self.run_cli("activate", "core")
        self.assertEqual(0, activated.returncode, activated.stdout)
        self.assertIn("MODO PLAN", activated.stdout)

    def test_agency_profile_keeps_distinct_operating_skills_private(self):
        applied = self.run_cli("enable", "agency", "--apply")
        self.assertEqual(0, applied.returncode, applied.stdout)
        skill_root = self.project / PRIVATE_SKILL_ROOT
        self.assertTrue((skill_root / "shipping-and-launch" / "SKILL.md").is_file())
        self.assertTrue((skill_root / "incremental-implementation" / "SKILL.md").is_file())
        self.assertTrue((skill_root / "git-workflow-and-versioning" / "SKILL.md").is_file())
        self.assertFalse((self.project / ".agents").exists())

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
        managed = self.private_skill("supabase-postgres-best-practices")
        managed.write_text("modified by user\n", encoding="utf-8")

        disabled = self.run_cli("disable", "supabase", "--apply")
        self.assertNotEqual(0, disabled.returncode)
        self.assertEqual("keep me\n", unmanaged.read_text(encoding="utf-8"))
        self.assertEqual("modified by user\n", managed.read_text(encoding="utf-8"))

    def test_disable_removes_only_unmodified_private_profile_files(self):
        enabled = self.run_cli("enable", "frontend", "--apply")
        self.assertEqual(0, enabled.returncode, enabled.stdout)

        disabled = self.run_cli("disable", "frontend", "--apply")
        self.assertEqual(0, disabled.returncode, disabled.stdout)
        private_root = self.project / PRIVATE_SKILL_ROOT
        self.assertFalse(private_root.exists() and any(private_root.iterdir()))
        manifest = self.project / ".agentit" / "skills-manifest.json"
        payload = json.loads(manifest.read_text(encoding="utf-8"))
        self.assertEqual([], payload["profiles"])
        self.assertEqual({}, payload["skills"])
        self.assertFalse((self.project / ".agents").exists())

    def test_matching_preexisting_project_skill_is_not_adopted_or_removed(self):
        preexisting = (
            self.project
            / ".agents"
            / "skills"
            / "supabase-postgres-best-practices"
            / "SKILL.md"
        )
        source = REPOSITORY / "skills" / "supabase-postgres-best-practices" / "SKILL.md"
        preexisting.parent.mkdir(parents=True)
        preexisting.write_bytes(source.read_bytes())

        self.assertEqual(0, self.run_cli("enable", "supabase", "--apply").returncode)
        self.assertTrue(self.private_skill("supabase-postgres-best-practices").is_file())
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

    def test_legacy_agentit_profile_is_migrated_out_of_host_visible_root(self):
        skill_id = "supabase-postgres-best-practices"
        source = REPOSITORY / "skills" / skill_id / "SKILL.md"
        legacy = self.project / ".agents" / "skills" / skill_id / "SKILL.md"
        legacy.parent.mkdir(parents=True)
        legacy.write_bytes(source.read_bytes())
        digest = sha256(source)
        manifest = self.project / ".agentit" / "skills-manifest.json"
        manifest.parent.mkdir(parents=True)
        manifest.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "profiles": ["supabase"],
                    "skills": {
                        skill_id: {
                            "destination": f".agents/skills/{skill_id}/SKILL.md",
                            "source_sha256": digest,
                            "installed_sha256": digest,
                            "managed": True,
                            "files": {
                                "SKILL.md": {
                                    "source_sha256": digest,
                                    "installed_sha256": digest,
                                    "managed": True,
                                }
                            },
                        }
                    },
                }
            )
            + "\n",
            encoding="utf-8",
        )

        migrated = self.run_cli("enable", "supabase", "--apply")
        self.assertEqual(0, migrated.returncode, migrated.stdout)
        self.assertFalse(legacy.exists())
        self.assertTrue(self.private_skill(skill_id).is_file())
        payload = json.loads(manifest.read_text(encoding="utf-8"))
        self.assertTrue(payload["skills"][skill_id]["destination"].startswith(".agentit/profile-skills/"))

    def test_modified_legacy_agentit_profile_fails_closed(self):
        skill_id = "supabase-postgres-best-practices"
        source = REPOSITORY / "skills" / skill_id / "SKILL.md"
        legacy = self.project / ".agents" / "skills" / skill_id / "SKILL.md"
        legacy.parent.mkdir(parents=True)
        legacy.write_bytes(source.read_bytes())
        original_hash = sha256(source)
        legacy.write_text("modified legacy body\n", encoding="utf-8")
        manifest = self.project / ".agentit" / "skills-manifest.json"
        manifest.parent.mkdir(parents=True)
        manifest.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "profiles": ["supabase"],
                    "skills": {
                        skill_id: {
                            "destination": f".agents/skills/{skill_id}/SKILL.md",
                            "source_sha256": original_hash,
                            "installed_sha256": original_hash,
                            "managed": True,
                            "files": {
                                "SKILL.md": {
                                    "source_sha256": original_hash,
                                    "installed_sha256": original_hash,
                                    "managed": True,
                                }
                            },
                        }
                    },
                }
            )
            + "\n",
            encoding="utf-8",
        )

        result = self.run_cli("enable", "supabase", "--apply")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("refusing automatic JIT migration", result.stdout)
        self.assertEqual("modified legacy body\n", legacy.read_text(encoding="utf-8"))

    def test_manifest_symlink_is_rejected_before_installing_project_skills(self):
        manifest = self.project / ".agentit" / "skills-manifest.json"
        manifest.parent.mkdir()
        manifest.symlink_to(self.project / "missing-manifest.json")
        before = {path.relative_to(self.project).as_posix() for path in self.project.rglob("*")}

        result = self.run_cli("enable", "core", "--apply")
        self.assertNotEqual(0, result.returncode, result.stdout)
        self.assertEqual(
            before,
            {path.relative_to(self.project).as_posix() for path in self.project.rglob("*")},
        )
        self.assertTrue(manifest.is_symlink())

    def test_profile_cache_refreshes_unmodified_body_when_source_changes(self):
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
        old_hash = before["skills"]["task-router"]["installed_sha256"]
        source = repository / "skills" / "task-router" / "SKILL.md"
        source.write_text(source.read_text(encoding="utf-8") + "source update\n", encoding="utf-8")

        disabled = run_fixture("disable", "frontend", "--apply")
        self.assertEqual(0, disabled.returncode, disabled.stdout)
        after = json.loads(manifest.read_text(encoding="utf-8"))
        new_hash = after["skills"]["task-router"]["installed_sha256"]
        self.assertNotEqual(old_hash, new_hash)
        self.assertEqual(sha256(source), new_hash)
        self.assertEqual(0, run_fixture("disable", "core", "--apply").returncode)


if __name__ == "__main__":
    unittest.main()
