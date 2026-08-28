from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from router.bootstrap import (
    BootstrapError,
    apply_install_plan,
    apply_rollback,
    build_install_plan,
    rollback_plan,
)
from router.profiles import load_catalog, resolve_profile


ROOT = Path(__file__).resolve().parents[1]


class PortableBootstrapTests(unittest.TestCase):
    def test_bootstrap_manifest_core_matches_profile_catalog(self):
        manifest = json.loads((ROOT / "bootstrap-manifest.json").read_text(encoding="utf-8"))
        catalog = load_catalog(ROOT / "profiles.yaml")
        self.assertEqual(
            manifest["core_skills"],
            resolve_profile("core", catalog, repo_root=ROOT),
        )

    def test_plan_is_read_only_and_contains_agent_cli(self):
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            plan = build_install_plan(home=home, source_root=ROOT, provider="codex")
            self.assertEqual(plan["mode"], "plan")
            self.assertEqual(plan["providers"], ["codex"])
            self.assertFalse((home / ".agentit").exists())
            self.assertFalse((home / ".codex").exists())
            self.assertFalse((home / ".local" / "bin" / "agentit").exists())
            destinations = {item["destination"] for item in plan["operations"]}
            self.assertIn(str(home / ".local" / "bin" / "agentit"), destinations)
            self.assertIn(
                str(home / ".codex" / "skills" / "using-agentit" / "SKILL.md"),
                destinations,
            )

    def test_antigravity_uses_canonical_global_skill_discovery_path(self):
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            plan = build_install_plan(home=home, source_root=ROOT, provider="antigravity")
            destinations = {item["destination"] for item in plan["operations"]}
            canonical = home / ".gemini" / "config" / "skills" / "using-agentit" / "SKILL.md"
            legacy = home / ".agents" / "skills" / "using-agentit" / "SKILL.md"
            self.assertIn(str(canonical), destinations)
            self.assertNotIn(str(legacy), destinations)

    def test_grok_uses_canonical_global_skill_discovery_path(self):
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            plan = build_install_plan(home=home, source_root=ROOT, provider="grok")
            destinations = {item["destination"] for item in plan["operations"]}
            canonical = home / ".grok" / "skills" / "using-agentit" / "SKILL.md"
            self.assertIn(str(canonical), destinations)

    def test_apply_installs_runtime_provider_surfaces_and_cli(self):
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            plan = build_install_plan(home=home, source_root=ROOT, provider="codex")
            result = apply_install_plan(plan, skip_dependencies=True)

            self.assertEqual(result["status"], "applied")
            self.assertTrue((home / ".agentit" / "runtime" / "router" / "entrypoint.py").is_file())
            self.assertTrue((home / ".codex" / "skills" / "using-agentit" / "SKILL.md").is_file())
            self.assertTrue((home / ".codex" / "agents" / "luna-worker.toml").is_file())

            cli = home / ".local" / "bin" / "agentit"
            self.assertTrue(cli.is_file())
            cmd = [str(cli), "--help"] if os.name != "nt" else [sys.executable, str(cli), "--help"]
            completed = subprocess.run(
                cmd,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stdout)
            self.assertIn("Agentit", completed.stdout)

            receipt = Path(result["backup_manifest"])
            self.assertTrue(receipt.is_file())
            payload = json.loads(receipt.read_text(encoding="utf-8"))
            self.assertEqual(payload["kind"], "agentit.bootstrap.receipt")

    def test_existing_file_is_backed_up_and_safe_rollback_restores_it(self):
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            destination = home / ".codex" / "skills" / "using-agentit" / "SKILL.md"
            destination.parent.mkdir(parents=True)
            original = b"custom pre-agentit file\n"
            destination.write_bytes(original)

            plan = build_install_plan(home=home, source_root=ROOT, provider="codex")
            result = apply_install_plan(plan, skip_dependencies=True)
            self.assertNotEqual(destination.read_bytes(), original)

            rollback = rollback_plan(Path(result["backup_manifest"]))
            self.assertTrue(any(item["action"] == "restore" for item in rollback["operations"]))
            applied = apply_rollback(Path(result["backup_manifest"]))
            self.assertEqual(applied["status"], "rolled-back")
            self.assertEqual(destination.read_bytes(), original)

    def test_rollback_refuses_post_install_user_changes(self):
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            plan = build_install_plan(home=home, source_root=ROOT, provider="codex")
            result = apply_install_plan(plan, skip_dependencies=True)
            destination = home / ".codex" / "skills" / "using-agentit" / "SKILL.md"
            destination.write_text("changed after install\n", encoding="utf-8")
            with self.assertRaises(BootstrapError):
                rollback_plan(Path(result["backup_manifest"]))

    def test_machine_local_settings_come_only_from_explicit_template(self):
        self.assertFalse((ROOT / "settings.local.json").exists())
        template = ROOT / "templates" / "claude" / "settings.local.example.json"
        self.assertTrue(template.is_file())
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            plan = build_install_plan(
                home=home,
                source_root=ROOT,
                provider="claude",
                with_local_settings=True,
            )
            apply_install_plan(plan, skip_dependencies=True)
            installed = home / ".claude" / "settings.local.json"
            self.assertEqual(installed.read_bytes(), template.read_bytes())


if __name__ == "__main__":
    unittest.main()
