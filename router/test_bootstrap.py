from __future__ import annotations

import json
import subprocess
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
CORE = {"using-agentit", "task-router", "using-agent-skills"}


class PortableBootstrapTests(unittest.TestCase):
    def test_bootstrap_manifest_core_matches_profile_catalog(self):
        manifest = json.loads((ROOT / "bootstrap-manifest.json").read_text(encoding="utf-8"))
        catalog = load_catalog(ROOT / "profiles.yaml")
        self.assertEqual(manifest["core_skills"], resolve_profile("core", catalog, repo_root=ROOT))

    def test_provider_paths_match_current_host_surfaces(self):
        manifest = json.loads((ROOT / "bootstrap-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["providers"]["claude"]["skills_root"], ".claude/skills")
        self.assertEqual(manifest["providers"]["codex"]["skills_root"], ".agents/skills")
        self.assertEqual(manifest["providers"]["grok"]["skills_root"], ".grok/skills")
        self.assertEqual(manifest["providers"]["gemini"]["skills_root"], ".gemini/skills")
        self.assertEqual(
            manifest["providers"]["antigravity"]["skills_root"],
            ".gemini/config/skills",
        )

    def test_plan_is_read_only_and_contains_agent_cli(self):
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            plan = build_install_plan(home=home, source_root=ROOT, provider="codex")
            self.assertEqual(plan["mode"], "plan")
            self.assertEqual(plan["providers"], ["codex"])
            self.assertFalse((home / ".agentit").exists())
            self.assertFalse((home / ".agents").exists())
            self.assertFalse((home / ".local" / "bin" / "agentit").exists())
            destinations = {item["destination"] for item in plan["operations"]}
            self.assertIn(str(home / ".local" / "bin" / "agentit"), destinations)
            self.assertIn(
                str(home / ".agents" / "skills" / "using-agentit" / "SKILL.md"),
                destinations,
            )

    def test_every_provider_projects_exactly_core_but_keeps_private_library(self):
        manifest = json.loads((ROOT / "bootstrap-manifest.json").read_text(encoding="utf-8"))
        for provider, config in manifest["providers"].items():
            with self.subTest(provider=provider):
                with tempfile.TemporaryDirectory() as temporary:
                    home = Path(temporary)
                    plan = build_install_plan(home=home, source_root=ROOT, provider=provider)
                    provider_ops = [
                        item for item in plan["operations"]
                        if item.get("category") == f"provider:{provider}:skill"
                        and item["destination"].endswith("SKILL.md")
                    ]
                    visible = {Path(item["destination"]).parent.name for item in provider_ops}
                    self.assertEqual(visible, CORE)
                    runtime = {
                        item["destination"] for item in plan["operations"]
                        if item.get("category") == "runtime"
                    }
                    self.assertIn(
                        str(home / ".agentit" / "runtime" / "skills" / "architect-orchestrator" / "SKILL.md"),
                        runtime,
                    )
                    root = home / config["skills_root"]
                    self.assertTrue(all(str(root) in item["destination"] for item in provider_ops))

    def test_antigravity_uses_its_dedicated_global_skill_path(self):
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            plan = build_install_plan(home=home, source_root=ROOT, provider="antigravity")
            destinations = {item["destination"] for item in plan["operations"]}
            canonical = home / ".gemini" / "config" / "skills" / "using-agentit" / "SKILL.md"
            gemini_cli = home / ".gemini" / "skills" / "using-agentit" / "SKILL.md"
            self.assertIn(str(canonical), destinations)
            self.assertNotIn(str(gemini_cli), destinations)

    def test_apply_installs_runtime_provider_surfaces_and_cli(self):
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            plan = build_install_plan(home=home, source_root=ROOT, provider="codex")
            result = apply_install_plan(plan, skip_dependencies=True)

            self.assertEqual(result["status"], "applied")
            self.assertTrue((home / ".agentit" / "runtime" / "router" / "entrypoint.py").is_file())
            self.assertTrue((home / ".agentit" / "runtime" / "skills" / "security-and-hardening" / "SKILL.md").is_file())
            self.assertTrue((home / ".agents" / "skills" / "using-agentit" / "SKILL.md").is_file())
            self.assertFalse((home / ".agents" / "skills" / "security-and-hardening").exists())
            self.assertTrue((home / ".codex" / "agents" / "luna-worker.toml").is_file())

            cli = home / ".local" / "bin" / "agentit"
            completed = subprocess.run(
                [str(cli), "skills", "packs"],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stdout)
            self.assertIn("engineering", completed.stdout)

            receipt = Path(result["backup_manifest"])
            payload = json.loads(receipt.read_text(encoding="utf-8"))
            self.assertEqual(payload["kind"], "agentit.bootstrap.receipt")

    def test_legacy_exact_non_core_copy_is_pruned_and_rollback_restores_it(self):
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            old_skill = "api-and-interface-design"
            legacy = home / ".codex" / "skills" / old_skill
            legacy.mkdir(parents=True)
            source = ROOT / "skills" / old_skill
            for path in source.rglob("*"):
                if path.is_file():
                    destination = legacy / path.relative_to(source)
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    destination.write_bytes(path.read_bytes())

            plan = build_install_plan(home=home, source_root=ROOT, provider="codex")
            removals = [item for item in plan["operations"] if item["action"] == "remove-managed-skill-tree"]
            self.assertEqual([old_skill], [item["skill_id"] for item in removals])
            result = apply_install_plan(plan, skip_dependencies=True)
            self.assertFalse(legacy.exists())

            rollback = rollback_plan(Path(result["backup_manifest"]))
            self.assertTrue(any(item["action"] == "restore-tree" for item in rollback["operations"]))
            applied = apply_rollback(Path(result["backup_manifest"]))
            self.assertEqual(applied["status"], "rolled-back")
            self.assertTrue((legacy / "SKILL.md").is_file())

    def test_modified_same_id_skill_is_never_auto_pruned(self):
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            candidate = home / ".codex" / "skills" / "api-and-interface-design" / "SKILL.md"
            candidate.parent.mkdir(parents=True)
            candidate.write_text("user-owned or modified\n", encoding="utf-8")
            plan = build_install_plan(home=home, source_root=ROOT, provider="codex")
            self.assertFalse(
                any(
                    item.get("action") == "remove-managed-skill-tree"
                    and item.get("skill_id") == "api-and-interface-design"
                    for item in plan["operations"]
                )
            )
            apply_install_plan(plan, skip_dependencies=True)
            self.assertEqual("user-owned or modified\n", candidate.read_text(encoding="utf-8"))

    def test_existing_file_is_backed_up_and_safe_rollback_restores_it(self):
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            destination = home / ".agents" / "skills" / "using-agentit" / "SKILL.md"
            destination.parent.mkdir(parents=True)
            original = b"custom pre-agentit file\n"
            destination.write_bytes(original)

            plan = build_install_plan(home=home, source_root=ROOT, provider="codex")
            result = apply_install_plan(plan, skip_dependencies=True)
            self.assertNotEqual(destination.read_bytes(), original)

            applied = apply_rollback(Path(result["backup_manifest"]))
            self.assertEqual(applied["status"], "rolled-back")
            self.assertEqual(destination.read_bytes(), original)

    def test_rollback_refuses_post_install_user_changes(self):
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            plan = build_install_plan(home=home, source_root=ROOT, provider="codex")
            result = apply_install_plan(plan, skip_dependencies=True)
            destination = home / ".agents" / "skills" / "using-agentit" / "SKILL.md"
            destination.write_text("changed after install\n", encoding="utf-8")
            with self.assertRaises(BootstrapError):
                rollback_plan(Path(result["backup_manifest"]))

    def test_machine_local_settings_come_only_from_explicit_template(self):
        self.assertFalse((ROOT / "settings.local.json").exists())
        template = ROOT / "templates" / "claude" / "settings.local.example.json"
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
