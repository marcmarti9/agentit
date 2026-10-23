"""Temporary installation/migration checks for obsolete runtime file ownership."""

import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from router import bootstrap

# Exact public preimage from 8b472f8^, retained inline so tests need no Git CLI.
RETIRED_SKILL_BYTES = """---
name: anti-ai-slop-design
description: Prevent generic AI design slop (purple glows, generic cards, boring typography, lifeless layouts). Enforce brand-authentic visual identity, curated color systems, and responsive typography.
---

# Anti-AI-Slop Design System

## Core Directive

Reject cookie-cutter AI aesthetic tropes. Design UIs that reflect the specific brand identity, product context, and audience needs rather than applying repetitive AI visual clichés.

## Principles Over Dogma

1. **Context Over Trends**: Do not blindly apply glassmorphism, dark modes, or specific font pairs (e.g. Space Grotesk) to every product. A medical dashboard needs high contrast and legibility; a gaming app needs vibrant energy.
2. **Intentional Hierarchy**: Use visual scale, whitespace, and font weight to guide the user's eye naturally to the primary action.
3. **Responsive Micro-Interactions**: Use subtle motion to confirm user intent without causing distraction or layout shifts.

## Anti-Patterns to Avoid

| Slop Pattern | Why it Feels AI-Generated | Better Alternative |
|---|---|---|
| **Purple/Indigo Glow Overuse** | Linear `#6366f1` gradient buttons on dark backgrounds | Brand-curated HSL/OKLCH color themes matched to product identity |
| **Identical Rounded Cards** | Generic `border-radius: 12px` cards with standard heavy shadows | Layout structures tailored to the content type and visual hierarchy |
| **Default Inter Typography** | Using browser default Inter without font weight contrast | Intentional font pairing and scale tailored to readability and brand voice |
| **Lifeless Hero Sections** | Centered text + generic CTA button + floating laptop mock | Product-relevant interactive previews, live data, or functional widgets |
| **Static State Feedback** | Instant hover states without transition curves | Smooth micro-interactions (`transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1)`) |

## Design Checklist

- [ ] **Brand Authenticity**: Does the visual theme match the specific product domain?
- [ ] **Color Contrast**: Is WCAG AA contrast satisfied across light and dark modes?
- [ ] **Visual Hierarchy**: Is the primary call-to-action distinct from secondary controls?
- [ ] **Micro-Interactions**: Do interactive elements provide instant tactile feedback?

## See Also

For landings, portfolios, redesign audits, motion dials, and full pre-flight taste discipline, use `design-taste-frontend` instead of stretching this short checklist.
""".encode("utf-8")



class RuntimeInventoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.home = self.base / "home"
        self.home.mkdir()
        self.source = self.base / "source"
        (self.source / "payload").mkdir(parents=True)
        (self.source / "payload/old.txt").write_bytes(b"original old file\n")
        (self.source / "payload/old.txt").chmod(0o640)
        (self.source / "payload/keep.txt").write_bytes(b"keep\n")
        for skill in ("using-agentit", "task-router", "using-agent-skills"):
            folder = self.source / "skills" / skill
            folder.mkdir(parents=True)
            (folder / "SKILL.md").write_text("# " + skill + "\n")
        manifest = {"schema_version": 1, "runtime_paths": ["payload", "skills"], "python_dependencies": [], "core_skills": ["using-agentit", "task-router", "using-agent-skills"], "providers": {"codex": {"skills_root": ".agents/skills"}}}
        (self.source / "bootstrap-manifest.json").write_text(json.dumps(manifest))
        self.installed_old = self.home / ".agentit/runtime/payload/old.txt"
        self.inventory = self.home / ".agentit/runtime-inventory.json"
        self.apply(self.plan())

    def plan(self):
        return bootstrap.build_install_plan(home=self.home, source_root=self.source, provider="codex")

    def apply(self, plan, **kwargs):
        with patch.object(bootstrap, "_install_dependencies"):
            return bootstrap.apply_install_plan(plan, **kwargs)

    def retire_source_file(self):
        (self.source / "payload/old.txt").unlink()

    def test_update_retires_exact_owned_file_and_rollback_restores_file_and_inventory(self):
        original_inventory = self.inventory.read_bytes()
        self.retire_source_file()
        plan = self.plan()
        removed = [op for op in plan["operations"] if op["action"] == "remove-obsolete-runtime-file"]
        self.assertEqual([op["destination"] for op in removed], [str(self.installed_old)])
        result = self.apply(plan)
        self.assertFalse(self.installed_old.exists())
        self.assertTrue(all(op["action"] == "keep" for op in self.plan()["operations"]))
        bootstrap.apply_rollback(Path(result["backup_manifest"]))
        self.assertEqual(self.installed_old.read_bytes(), b"original old file\n")
        self.assertEqual(self.installed_old.stat().st_mode & 0o777, 0o640)
        self.assertEqual(self.inventory.read_bytes(), original_inventory)

    def test_modified_obsolete_and_unowned_files_survive_update(self):
        self.retire_source_file()
        self.installed_old.write_bytes(b"user edit\n")
        unknown = self.installed_old.with_name("user.txt")
        unknown.write_bytes(b"unowned\n")
        plan = self.plan()
        self.assertEqual(plan["retained_modified_runtime_files"], ["payload/old.txt"])
        self.assertEqual(plan["retained_unmanaged_runtime_files"], ["payload/user.txt"])
        self.apply(plan)
        self.assertEqual(self.installed_old.read_bytes(), b"user edit\n")
        self.assertEqual(unknown.read_bytes(), b"unowned\n")

    def test_permission_only_drift_preserves_obsolete_file(self):
        self.retire_source_file()
        self.installed_old.chmod(0o600)
        plan = self.plan()
        self.assertEqual(plan["retained_modified_runtime_files"], ["payload/old.txt"])
        self.apply(plan)
        self.assertEqual(self.installed_old.stat().st_mode & 0o777, 0o600)

    def test_legacy_successful_receipt_can_establish_exact_ownership(self):
        self.inventory.unlink()
        self.retire_source_file()
        self.apply(self.plan())
        self.assertFalse(self.installed_old.exists())

    def test_legacy_without_receipt_retains_and_reports_unproven_file(self):
        self.inventory.unlink()
        shutil.rmtree(self.home / ".agentit/backups")
        self.retire_source_file()
        plan = self.plan()
        self.assertEqual(plan["retained_unmanaged_runtime_files"], ["payload/old.txt"])
        self.apply(plan)
        self.assertTrue(self.installed_old.exists())

    def historical_file(self):
        path = self.home / ".agentit/runtime/skills/anti-ai-slop-design/SKILL.md"
        path.parent.mkdir(parents=True)
        path.write_bytes(RETIRED_SKILL_BYTES)
        path.chmod(0o644)
        self.assertEqual(bootstrap.RETIRED_UNOWNED_RUNTIME_FILES["skills/anti-ai-slop-design/SKILL.md"],
                         bootstrap._sha256_file(path))
        return path

    def test_reviewed_unowned_retirement_is_backed_up_idempotent_and_preserves_custom_and_private_files(self):
        historical = self.historical_file()
        preserved = {
            "skills/impeccable-design/SKILL.md": b"customized skill, not historical bytes\n",
            "docs/agentit/STATE.md": b"private continuity\n",
            "docs/agentit/LLM_NATIVE_ROUTING_REFACTOR.md": b"private planning\n",
        }
        for relative, content in preserved.items():
            path = self.home / ".agentit/runtime" / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
        plan = self.plan()
        retired = [operation["destination"] for operation in plan["operations"]
                   if operation["action"] == "remove-obsolete-runtime-file"]
        self.assertEqual([str(historical)], retired)
        self.assertEqual(sorted(preserved), plan["retained_unmanaged_runtime_files"])
        result = self.apply(plan)
        self.assertFalse(historical.exists())
        receipt = json.loads(Path(result["backup_manifest"]).read_text())
        record = next(record for record in receipt["records"] if record["destination"] == str(historical))
        self.assertEqual(RETIRED_SKILL_BYTES, Path(record["backup_path"]).read_bytes())
        self.assertTrue(all(operation["action"] == "keep" for operation in self.plan()["operations"]))
        for relative, content in preserved.items():
            self.assertEqual(content, (self.home / ".agentit/runtime" / relative).read_bytes())
        bootstrap.apply_rollback(Path(result["backup_manifest"]))
        self.assertEqual(RETIRED_SKILL_BYTES, historical.read_bytes())
        self.assertEqual(0o644, historical.stat().st_mode & 0o777)

    def test_reviewed_path_with_custom_bytes_or_mode_is_preserved(self):
        historical = self.historical_file()
        for content, mode in ((b"customized content\n", 0o644), (RETIRED_SKILL_BYTES, 0o600)):
            with self.subTest(mode=mode):
                historical.write_bytes(content)
                historical.chmod(mode)
                plan = self.plan()
                self.assertIn("skills/anti-ai-slop-design/SKILL.md", plan["retained_unmanaged_runtime_files"])
                self.apply(plan)
                self.assertEqual(content, historical.read_bytes())
                self.assertEqual(mode, historical.stat().st_mode & 0o777)

    def test_reviewed_retirement_still_rejects_changes_after_plan(self):
        historical = self.historical_file()
        plan = self.plan()
        historical.write_bytes(b"changed after plan\n")
        with self.assertRaisesRegex(bootstrap.BootstrapError, "destination changed after planning"):
            self.apply(plan)
        self.assertEqual(b"changed after plan\n", historical.read_bytes())

    def test_reviewed_file_is_not_retired_if_it_still_exists_in_source(self):
        historical = self.historical_file()
        source = self.source / "skills/anti-ai-slop-design/SKILL.md"
        source.parent.mkdir(parents=True)
        source.write_bytes(RETIRED_SKILL_BYTES)
        # Exercise even when the source file is excluded from runtime copying.
        manifest_path = self.source / "bootstrap-manifest.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["runtime_paths"] = ["payload"]
        manifest_path.write_text(json.dumps(manifest))
        plan = self.plan()
        self.assertIn("skills/anti-ai-slop-design/SKILL.md", plan["retained_unmanaged_runtime_files"])
        self.apply(plan)
        self.assertEqual(RETIRED_SKILL_BYTES, historical.read_bytes())

    def test_inventory_path_traversal_is_rejected_before_mutation(self):
        data = json.loads(self.inventory.read_text())
        data["files"]["../../outside"] = {"sha256": "a" * 64, "mode": 0o644}
        self.inventory.write_text(json.dumps(data))
        with self.assertRaisesRegex(bootstrap.BootstrapError, "unsafe relative path"):
            self.plan()
        self.assertTrue(self.installed_old.exists())

    def test_inventory_alias_collisions_are_rejected_before_retirement(self):
        self.retire_source_file()
        original = self.inventory.read_text()
        for alias in ("payload/./old.txt", "payload//old.txt", "./payload/old.txt"):
            with self.subTest(alias=alias):
                data = json.loads(original)
                data["files"][alias] = data["files"]["payload/old.txt"]
                self.inventory.write_text(json.dumps(data))
                with self.assertRaisesRegex(bootstrap.BootstrapError, "duplicate runtime inventory path"):
                    self.plan()
                self.assertTrue(self.installed_old.exists())

    def test_inventory_repeated_json_keys_are_rejected_before_retirement(self):
        self.retire_source_file()
        record = json.loads(self.inventory.read_text())["files"]["payload/old.txt"]
        entry = '"payload/old.txt":' + json.dumps(record)
        self.inventory.write_text('{"kind":"agentit.runtime.inventory","schema_version":1,"files":{' + entry + ',' + entry + '}}')
        with self.assertRaisesRegex(bootstrap.BootstrapError, "duplicate runtime inventory key"):
            self.plan()
        self.assertTrue(self.installed_old.exists())

    def test_inventory_symlink_is_rejected(self):
        target = self.base / "unrelated.json"
        self.inventory.rename(target)
        self.inventory.symlink_to(target)
        with self.assertRaisesRegex(bootstrap.BootstrapError, "symlink"):
            self.plan()

    def test_forged_legacy_receipt_cannot_target_outside_private_runtime(self):
        self.inventory.unlink()
        receipt_path = next((self.home / ".agentit/backups").glob("install-*/manifest.json"))
        data = json.loads(receipt_path.read_text())
        data["records"][0]["destination"] = str(self.home / "outside.txt")
        receipt_path.write_text(json.dumps(data))
        with self.assertRaisesRegex(bootstrap.BootstrapError, "escapes private runtime"):
            self.plan()

    def test_interruption_immediately_after_delete_is_recoverable(self):
        self.retire_source_file()
        backup = self.home / "interrupted"
        real_unlink = Path.unlink
        interrupted = []

        def unlink_then_fail(path, *args, **kwargs):
            result = real_unlink(path, *args, **kwargs)
            if path == self.installed_old and not interrupted:
                interrupted.append(True)
                raise OSError("injected after obsolete deletion")
            return result

        with patch.object(Path, "unlink", side_effect=None, autospec=True) as mocked:
            mocked.side_effect = unlink_then_fail
            with self.assertRaisesRegex(OSError, "injected"):
                self.apply(self.plan(), backup_dir=backup)
        self.assertFalse(self.installed_old.exists())
        receipt = backup / "manifest.json"
        self.assertTrue(json.loads(receipt.read_text())["recovery_only"])
        bootstrap.apply_rollback(receipt)
        self.assertEqual(self.installed_old.read_bytes(), b"original old file\n")


if __name__ == "__main__":
    unittest.main()
