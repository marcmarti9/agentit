import os
import shutil
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[1]


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


class ScriptRegressionTests(unittest.TestCase):
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

    def test_antigravity_install_can_immediately_drive_update_plan(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            home = Path(temporary_directory) / "home"
            home.mkdir()
            install_backup = home / "antigravity-install-backup"

            install_result = run_script(
                REPOSITORY / "install.sh",
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

            update_result = run_script(
                REPOSITORY / "update.sh", home, "--provider", "antigravity"
            )

            self.assertEqual(0, update_result.returncode, update_result.stdout)

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
