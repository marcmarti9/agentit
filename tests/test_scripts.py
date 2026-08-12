import os
import shutil
import stat
import subprocess
import tempfile
import tomllib
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[1]
CODEX_PROFILE_NAMES = ("luna-worker.toml", "terra-worker.toml")


def run_script(script, home, *arguments):
    environment = os.environ.copy()
    environment["HOME"] = str(home)
    return subprocess.run(
        ["bash", str(script), *arguments, "--home", str(home)],
        cwd=script.parent,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=30,
        check=False,
        umask=0o022,
    )


def snapshot_tree(root):
    snapshot = {}
    for path in sorted(root.rglob("*")):
        relative_path = path.relative_to(root).as_posix()
        metadata = path.lstat()
        mode = stat.S_IMODE(metadata.st_mode)
        if path.is_symlink():
            snapshot[relative_path] = ("symlink", mode, os.readlink(path))
        elif path.is_file():
            snapshot[relative_path] = ("file", mode, path.read_bytes())
        elif path.is_dir():
            snapshot[relative_path] = ("directory", mode)
        else:
            snapshot[relative_path] = ("other", mode)
    return snapshot


def file_mode(path):
    return stat.S_IMODE(path.stat().st_mode)


def copy_codex_profiles(destination):
    destination.mkdir(parents=True, exist_ok=True)
    for profile_name in CODEX_PROFILE_NAMES:
        shutil.copy2(
            REPOSITORY / ".codex" / "agents" / profile_name,
            destination / profile_name,
        )


class ScriptRegressionTests(unittest.TestCase):
    def test_codex_profile_plan_does_not_write_install_or_update(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            install_home = temporary_root / "install-home"
            install_home.mkdir()
            install_before = snapshot_tree(install_home)
            install_result = run_script(
                REPOSITORY / "install.sh",
                install_home,
                "--provider",
                "codex",
                "--backup-dir",
                str(install_home / "install-backup"),
            )
            self.assertEqual(0, install_result.returncode, install_result.stdout)
            self.assertEqual(install_before, snapshot_tree(install_home))

            repository_fixture = temporary_root / "repository-fixture"
            shutil.copytree(
                REPOSITORY,
                repository_fixture,
                symlinks=True,
                ignore=shutil.ignore_patterns(".git", "__pycache__", "backups"),
            )
            update_home = temporary_root / "update-home"
            copy_codex_profiles(update_home / ".codex" / "agents")
            repository_before = snapshot_tree(repository_fixture)
            update_result = run_script(
                repository_fixture / "update.sh",
                update_home,
                "--provider",
                "codex",
                "--backup-dir",
                str(repository_fixture / "update-backup"),
            )
            self.assertEqual(0, update_result.returncode, update_result.stdout)
            self.assertEqual(repository_before, snapshot_tree(repository_fixture))

    def test_codex_apply_installs_both_profiles_and_manifest(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            home = temporary_root / "home"
            home.mkdir()
            backup_root = temporary_root / "install-backup"
            result = run_script(
                REPOSITORY / "install.sh",
                home,
                "--apply",
                "--provider",
                "codex",
                "--backup-dir",
                str(backup_root),
            )
            self.assertEqual(0, result.returncode, result.stdout)
            for profile_name in CODEX_PROFILE_NAMES:
                installed = home / ".codex" / "agents" / profile_name
                self.assertEqual(
                    (REPOSITORY / ".codex" / "agents" / profile_name).read_bytes(),
                    installed.read_bytes(),
                )
            manifest = backup_root / "manifest.txt"
            self.assertTrue(manifest.is_file())
            self.assertIn("provider=codex", manifest.read_text(encoding="utf-8"))

    def test_codex_apply_installs_only_the_bounded_core_skill_profile(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            home = temporary_root / "home"
            home.mkdir()
            result = run_script(
                REPOSITORY / "install.sh",
                home,
                "--apply",
                "--provider",
                "codex",
                "--backup-dir",
                str(temporary_root / "install-backup"),
            )
            self.assertEqual(0, result.returncode, result.stdout)
            installed = {
                path.parent.name
                for path in (home / ".codex" / "skills").glob("*/SKILL.md")
            }
            self.assertEqual(
                {
                    "using-agentit",
                    "task-router",
                    "architect-orchestrator",
                    "debugging-and-error-recovery",
                    "code-review-and-quality",
                    "test-driven-development",
                    "security-and-hardening",
                    "source-driven-development",
                    "mcp-tooling-fit",
                    "planning-and-task-breakdown",
                    "using-agent-skills",
                    "verification-gauntlet",
                },
                installed,
            )

    def test_codex_prune_on_demand_removes_only_exact_agentit_copies(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            home = temporary_root / "home"
            home.mkdir()
            codex_skills = home / ".codex" / "skills"
            old_skill = "api-and-interface-design"
            old_destination = codex_skills / old_skill / "SKILL.md"
            old_destination.parent.mkdir(parents=True)
            old_destination.write_bytes(
                (REPOSITORY / "skills" / old_skill / "SKILL.md").read_bytes()
            )
            unrelated = codex_skills / "user-managed" / "SKILL.md"
            unrelated.parent.mkdir(parents=True)
            unrelated.write_text("keep this skill\n", encoding="utf-8")
            backup_root = temporary_root / "install-backup"

            result = run_script(
                REPOSITORY / "install.sh",
                home,
                "--apply",
                "--provider",
                "codex",
                "--prune-on-demand",
                "--backup-dir",
                str(backup_root),
            )

            self.assertEqual(0, result.returncode, result.stdout)
            self.assertFalse(old_destination.exists())
            self.assertEqual("keep this skill\n", unrelated.read_text(encoding="utf-8"))
            self.assertEqual(
                (backup_root / "codex" / "skills" / old_skill / "SKILL.md").read_bytes(),
                (REPOSITORY / "skills" / old_skill / "SKILL.md").read_bytes(),
            )

    def test_codex_prune_plan_does_not_remove_exact_agentit_copies(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            home = temporary_root / "home"
            home.mkdir()
            old_skill = "api-and-interface-design"
            old_destination = home / ".codex" / "skills" / old_skill / "SKILL.md"
            old_destination.parent.mkdir(parents=True)
            old_destination.write_bytes(
                (REPOSITORY / "skills" / old_skill / "SKILL.md").read_bytes()
            )
            before = snapshot_tree(home)
            backup_root = temporary_root / "install-backup"

            result = run_script(
                REPOSITORY / "install.sh",
                home,
                "--provider",
                "codex",
                "--prune-on-demand",
                "--backup-dir",
                str(backup_root),
            )

            self.assertEqual(0, result.returncode, result.stdout)
            self.assertEqual(before, snapshot_tree(home))
            self.assertFalse(backup_root.exists())

    def test_codex_prune_refuses_modified_on_demand_skill_before_backup(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            home = temporary_root / "home"
            home.mkdir()
            modified = (
                home / ".codex" / "skills" / "api-and-interface-design" / "SKILL.md"
            )
            modified.parent.mkdir(parents=True)
            modified.write_text("user modification\n", encoding="utf-8")
            backup_root = temporary_root / "install-backup"

            result = run_script(
                REPOSITORY / "install.sh",
                home,
                "--apply",
                "--provider",
                "codex",
                "--prune-on-demand",
                "--backup-dir",
                str(backup_root),
            )

            self.assertNotEqual(0, result.returncode, result.stdout)
            self.assertFalse(backup_root.exists())
            self.assertEqual("user modification\n", modified.read_text(encoding="utf-8"))

    def test_codex_existing_profiles_are_backed_up_before_install(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            home = temporary_root / "home"
            existing_profiles = home / ".codex" / "agents"
            existing_profiles.mkdir(parents=True)
            old_contents = {}
            for profile_name in CODEX_PROFILE_NAMES:
                old_contents[profile_name] = f"old {profile_name}\n"
                (existing_profiles / profile_name).write_text(
                    old_contents[profile_name], encoding="utf-8"
                )
            backup_root = temporary_root / "install-backup"
            result = run_script(
                REPOSITORY / "install.sh",
                home,
                "--apply",
                "--provider",
                "codex",
                "--backup-dir",
                str(backup_root),
            )
            self.assertEqual(0, result.returncode, result.stdout)
            manifest = (backup_root / "manifest.txt").read_text(encoding="utf-8")
            for profile_name in CODEX_PROFILE_NAMES:
                backup = backup_root / "codex" / "agents" / profile_name
                self.assertEqual(old_contents[profile_name], backup.read_text())
                self.assertIn(str(backup), manifest)

    def test_codex_profile_symlinks_are_rejected_before_backup(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)

            install_home = temporary_root / "install-home"
            install_home.mkdir()
            install_external = temporary_root / "install-external"
            install_external.mkdir()
            (install_home / ".codex").symlink_to(
                install_external, target_is_directory=True
            )
            install_backup = temporary_root / "install-backup"
            install_result = run_script(
                REPOSITORY / "install.sh",
                install_home,
                "--apply",
                "--provider",
                "codex",
                "--backup-dir",
                str(install_backup),
            )
            self.assertNotEqual(0, install_result.returncode, install_result.stdout)
            self.assertFalse(install_backup.exists())
            self.assertEqual([], list(install_external.iterdir()))

            repository_fixture = temporary_root / "repository-fixture"
            shutil.copytree(
                REPOSITORY,
                repository_fixture,
                symlinks=True,
                ignore=shutil.ignore_patterns(".git", "__pycache__", "backups"),
            )
            update_home = temporary_root / "update-home"
            source_profiles = update_home / ".codex" / "agents"
            copy_codex_profiles(source_profiles)
            update_external = temporary_root / "update-external.toml"
            update_external.write_text("must not be imported\n", encoding="utf-8")
            (source_profiles / "luna-worker.toml").unlink()
            (source_profiles / "luna-worker.toml").symlink_to(update_external)
            update_backup = temporary_root / "update-backup"
            repository_before = snapshot_tree(repository_fixture)
            update_result = run_script(
                repository_fixture / "update.sh",
                update_home,
                "--apply",
                "--provider",
                "codex",
                "--backup-dir",
                str(update_backup),
            )
            self.assertNotEqual(0, update_result.returncode, update_result.stdout)
            self.assertFalse(update_backup.exists())
            self.assertEqual(repository_before, snapshot_tree(repository_fixture))

    def test_unknown_codex_toml_is_not_imported(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)

            repository_fixture = temporary_root / "repository-fixture"
            shutil.copytree(
                REPOSITORY,
                repository_fixture,
                symlinks=True,
                ignore=shutil.ignore_patterns(".git", "__pycache__", "backups"),
            )
            unknown_repository_profile = (
                repository_fixture / ".codex" / "agents" / "unknown.toml"
            )
            unknown_repository_profile.write_text(
                'name = "unknown"\n', encoding="utf-8"
            )
            install_home = temporary_root / "install-home"
            install_home.mkdir()
            install_result = run_script(
                repository_fixture / "install.sh",
                install_home,
                "--apply",
                "--provider",
                "codex",
                "--backup-dir",
                str(temporary_root / "install-backup"),
            )
            self.assertEqual(0, install_result.returncode, install_result.stdout)
            self.assertFalse(
                (install_home / ".codex" / "agents" / "unknown.toml").exists()
            )
            unknown_repository_profile.unlink()

            update_home = temporary_root / "update-home"
            source_profiles = update_home / ".codex" / "agents"
            copy_codex_profiles(source_profiles)
            (source_profiles / "unknown.toml").write_text(
                'name = "machine-only"\n', encoding="utf-8"
            )
            update_result = run_script(
                repository_fixture / "update.sh",
                update_home,
                "--apply",
                "--provider",
                "codex",
                "--backup-dir",
                str(temporary_root / "update-backup"),
            )
            self.assertEqual(0, update_result.returncode, update_result.stdout)
            self.assertFalse(
                (repository_fixture / ".codex" / "agents" / "unknown.toml").exists()
            )

    def test_claude_and_antigravity_do_not_receive_codex_profiles(self):
        for provider in ("claude", "antigravity"):
            with self.subTest(provider=provider):
                with tempfile.TemporaryDirectory() as temporary_directory:
                    temporary_root = Path(temporary_directory)
                    home = temporary_root / "home"
                    home.mkdir()
                    result = run_script(
                        REPOSITORY / "install.sh",
                        home,
                        "--apply",
                        "--provider",
                        provider,
                        "--backup-dir",
                        str(temporary_root / "install-backup"),
                    )
                    self.assertEqual(0, result.returncode, result.stdout)
                    self.assertEqual([], list(home.rglob("luna-worker.toml")))
                    self.assertEqual([], list(home.rglob("terra-worker.toml")))

    def test_codex_worker_profiles_are_valid_toml(self):
        for profile_name in CODEX_PROFILE_NAMES:
            with self.subTest(profile=profile_name):
                profile = REPOSITORY / ".codex" / "agents" / profile_name
                parsed = tomllib.loads(profile.read_text(encoding="utf-8"))
                self.assertIn("name", parsed)
                self.assertIn("model", parsed)

    def test_incompatible_settings_are_rejected_before_install_or_update_writes(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)

            install_home = temporary_root / "install-home"
            install_home.mkdir()
            install_backup = install_home / "incompatible-install-backup"
            install_result = run_script(
                REPOSITORY / "install.sh",
                install_home,
                "--apply",
                "--provider",
                "codex",
                "--with-settings",
                "--backup-dir",
                str(install_backup),
            )

            repository_fixture = temporary_root / "repository-fixture"
            shutil.copytree(
                REPOSITORY,
                repository_fixture,
                symlinks=True,
                ignore=shutil.ignore_patterns(".git", "__pycache__", "backups"),
            )
            update_home = temporary_root / "update-home"
            source_skill = (
                update_home
                / ".codex"
                / "skills"
                / "architect-orchestrator"
                / "SKILL.md"
            )
            source_skill.parent.mkdir(parents=True)
            source_skill.write_text(
                "fixture content that must never be imported\n", encoding="utf-8"
            )
            update_backup = repository_fixture / "backups" / "incompatible-update"
            repository_before = snapshot_tree(repository_fixture)
            update_result = run_script(
                repository_fixture / "update.sh",
                update_home,
                "--apply",
                "--provider",
                "codex",
                "--with-settings",
                "--backup-dir",
                str(update_backup),
            )
            repository_after = snapshot_tree(repository_fixture)

            violations = []
            if install_result.returncode == 0:
                violations.append("install accepted codex --with-settings")
            if (install_home / ".codex").exists():
                violations.append("install partially deployed .codex")
            if install_backup.exists():
                violations.append("install created a backup before rejecting options")
            if update_result.returncode == 0:
                violations.append("update accepted codex --with-settings")
            if repository_after != repository_before:
                violations.append("update changed the copied repository fixture")
            if update_backup.exists():
                violations.append("update created a backup before rejecting options")

            self.assertEqual(
                [],
                violations,
                "\n".join(
                    [
                        *violations,
                        "install output:",
                        install_result.stdout,
                        "update output:",
                        update_result.stdout,
                    ]
                ),
            )

    def test_unsafe_destinations_are_rejected_before_creating_backups(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)

            install_home = temporary_root / "install-home"
            install_home.mkdir()
            install_external = temporary_root / "install-external"
            install_external.mkdir()
            (install_home / ".codex").symlink_to(
                install_external, target_is_directory=True
            )
            install_backup = install_home / "unsafe-install-backup"
            install_before = snapshot_tree(install_home)

            install_result = run_script(
                REPOSITORY / "install.sh",
                install_home,
                "--apply",
                "--provider",
                "codex",
                "--backup-dir",
                str(install_backup),
            )

            repository_fixture = temporary_root / "repository-fixture"
            shutil.copytree(
                REPOSITORY,
                repository_fixture,
                symlinks=True,
                ignore=shutil.ignore_patterns(".git", "__pycache__", "backups"),
            )
            update_home = temporary_root / "update-home"
            source_skill = (
                update_home
                / ".codex"
                / "skills"
                / "architect-orchestrator"
                / "SKILL.md"
            )
            source_skill.parent.mkdir(parents=True)
            source_skill.write_text("unsafe destination fixture\n", encoding="utf-8")
            update_external = temporary_root / "update-external.md"
            update_external.write_text("must remain unchanged\n", encoding="utf-8")
            unsafe_destination = (
                repository_fixture
                / "skills"
                / "architect-orchestrator"
                / "SKILL.md"
            )
            unsafe_destination.unlink()
            unsafe_destination.symlink_to(update_external)
            update_backup = temporary_root / "unsafe-update-backup"
            repository_before = snapshot_tree(repository_fixture)

            update_result = run_script(
                repository_fixture / "update.sh",
                update_home,
                "--apply",
                "--provider",
                "codex",
                "--backup-dir",
                str(update_backup),
            )

            violations = []
            if install_result.returncode == 0:
                violations.append("install accepted a symlink provider destination")
            if snapshot_tree(install_home) != install_before:
                violations.append("install changed HOME before rejecting the destination")
            if install_backup.exists():
                violations.append("install created a backup before destination validation")
            if list(install_external.iterdir()):
                violations.append("install wrote through the .codex symlink")
            if update_result.returncode == 0:
                violations.append("update accepted a symlink repository destination")
            if snapshot_tree(repository_fixture) != repository_before:
                violations.append("update changed the repository before rejection")
            if update_backup.exists():
                violations.append("update created a backup before destination validation")
            if update_external.read_text(encoding="utf-8") != "must remain unchanged\n":
                violations.append("update wrote through the repository symlink")

            self.assertEqual(
                [],
                violations,
                "\n".join(
                    [
                        *violations,
                        "install output:",
                        install_result.stdout,
                        "update output:",
                        update_result.stdout,
                    ]
                ),
            )

    def test_antigravity_round_trip_imports_only_allowlisted_skill_files(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            repository_fixture = temporary_root / "repository-fixture"
            shutil.copytree(
                REPOSITORY,
                repository_fixture,
                symlinks=True,
                ignore=shutil.ignore_patterns(".git", "__pycache__", "backups"),
            )
            home = temporary_root / "home"
            home.mkdir()
            install_backup = home / "antigravity-install-backup"

            install_result = run_script(
                repository_fixture / "install.sh",
                home,
                "--apply",
                "--provider",
                "antigravity",
                "--backup-dir",
                str(install_backup),
            )
            self.assertEqual(0, install_result.returncode, install_result.stdout)
            self.assertTrue(
                (home / ".agents" / "skills" / "task-router" / "SKILL.md").is_file()
            )
            self.assertFalse((home / ".gemini" / "antigravity-cli").exists())

            installed_skill = (
                home
                / ".agents"
                / "skills"
                / "architect-orchestrator"
                / "SKILL.md"
            )
            round_trip_content = "antigravity round-trip fixture\n"
            installed_skill.write_text(round_trip_content, encoding="utf-8")
            unallowlisted_source = installed_skill.parent / "NOT_ALLOWLISTED.md"
            unallowlisted_source.write_text(
                "must not be imported\n", encoding="utf-8"
            )
            repository_before = snapshot_tree(repository_fixture)
            update_backup = home / "antigravity-update-backup"
            update_result = run_script(
                repository_fixture / "update.sh",
                home,
                "--apply",
                "--provider",
                "antigravity",
                "--backup-dir",
                str(update_backup),
            )
            self.assertEqual(0, update_result.returncode, update_result.stdout)
            imported_skill = (
                repository_fixture
                / "skills"
                / "architect-orchestrator"
                / "SKILL.md"
            )
            self.assertEqual(round_trip_content, imported_skill.read_text(encoding="utf-8"))
            self.assertFalse(
                (
                    repository_fixture
                    / "skills"
                    / "architect-orchestrator"
                    / "NOT_ALLOWLISTED.md"
                ).exists()
            )
            repository_after = snapshot_tree(repository_fixture)
            changed_paths = {
                path
                for path in repository_before.keys() | repository_after.keys()
                if repository_before.get(path) != repository_after.get(path)
            }
            self.assertEqual(
                {"skills/architect-orchestrator/SKILL.md"}, changed_paths
            )

    def test_existing_backup_roots_are_rejected_before_apply(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)

            install_home = temporary_root / "install-home"
            install_home.mkdir()
            install_backup = temporary_root / "install-backup"
            install_backup.mkdir()
            install_result = run_script(
                REPOSITORY / "install.sh",
                install_home,
                "--apply",
                "--provider",
                "codex",
                "--backup-dir",
                str(install_backup),
            )

            repository_fixture = temporary_root / "repository-fixture"
            shutil.copytree(
                REPOSITORY,
                repository_fixture,
                symlinks=True,
                ignore=shutil.ignore_patterns(".git", "__pycache__", "backups"),
            )
            update_home = temporary_root / "update-home"
            source_skill = (
                update_home
                / ".codex"
                / "skills"
                / "architect-orchestrator"
                / "SKILL.md"
            )
            source_skill.parent.mkdir(parents=True)
            source_skill.write_text("fixture\n", encoding="utf-8")
            update_backup = temporary_root / "update-backup"
            update_backup.mkdir()
            repository_before = snapshot_tree(repository_fixture)
            update_result = run_script(
                repository_fixture / "update.sh",
                update_home,
                "--apply",
                "--provider",
                "codex",
                "--backup-dir",
                str(update_backup),
            )

            hardening_home = temporary_root / "hardening-home"
            hardening_home.mkdir()
            (hardening_home / ".bashrc").write_text(
                "export EDITOR=vi\n", encoding="utf-8"
            )
            hardening_backup = temporary_root / "hardening-backup"
            hardening_backup.mkdir()
            hardening_result = run_script(
                REPOSITORY / "security" / "harden-local.sh",
                hardening_home,
                "--apply",
                "--backup-dir",
                str(hardening_backup),
            )

            self.assertNotEqual(0, install_result.returncode, install_result.stdout)
            self.assertFalse((install_backup / "manifest.txt").exists())
            self.assertFalse((install_home / ".codex").exists())
            self.assertNotEqual(0, update_result.returncode, update_result.stdout)
            self.assertFalse((update_backup / "manifest.txt").exists())
            self.assertEqual(repository_before, snapshot_tree(repository_fixture))
            self.assertNotEqual(0, hardening_result.returncode, hardening_result.stdout)
            self.assertFalse((hardening_backup / "manifest.txt").exists())
            self.assertEqual(
                "export EDITOR=vi\n",
                (hardening_home / ".bashrc").read_text(encoding="utf-8"),
            )

    def test_hardening_secures_backup_directories_and_credentials(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            home = Path(temporary_directory) / "home"
            home.mkdir()
            bashrc = home / ".bashrc"
            bashrc.write_text("export EDITOR=vi\n", encoding="utf-8")
            os.chmod(bashrc, 0o644)

            credential = home / ".cursor" / "profiles" / "test" / "mcp_auth.json"
            credential.parent.mkdir(parents=True)
            credential.write_text('{"fixture": true}\n', encoding="utf-8")
            os.chmod(credential, 0o644)

            backup_parent = home / "backups"
            backup_root = backup_parent / "hardening"
            result = run_script(
                REPOSITORY / "security" / "harden-local.sh",
                home,
                "--apply",
                "--backup-dir",
                str(backup_root),
            )
            self.assertEqual(0, result.returncode, result.stdout)

            backup_credential = (
                backup_root / ".cursor" / "profiles" / "test" / "mcp_auth.json"
            )
            protected_directories = [
                backup_parent,
                backup_root,
                backup_root / ".cursor",
                backup_root / ".cursor" / "profiles",
                backup_root / ".cursor" / "profiles" / "test",
            ]
            violations = [
                f"{path} mode is {file_mode(path):04o}, expected 0700"
                for path in protected_directories
                if file_mode(path) != 0o700
            ]
            for path in (backup_credential, credential):
                if file_mode(path) != 0o600:
                    violations.append(
                        f"{path} mode is {file_mode(path):04o}, expected 0600"
                    )

            self.assertEqual([], violations, "\n".join([*violations, result.stdout]))


if __name__ == "__main__":
    unittest.main()
