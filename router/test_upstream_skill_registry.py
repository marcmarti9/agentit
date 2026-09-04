import json
import tempfile
import unittest
from pathlib import Path

from router.profile_jit_cli import _package_files, _shared_reference_files
from router.profiles import load_catalog, resolve_profile

ROOT = Path(__file__).resolve().parents[1]


class UpstreamSkillRegistryTests(unittest.TestCase):
    def test_every_canonical_mapping_exists_as_complete_skill_package(self):
        lock = json.loads((ROOT / "skills" / "UPSTREAM_LOCK.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(lock["mappings"]), 39)
        for item in lock["mappings"]:
            skill = ROOT / "skills" / item["skill"]
            self.assertTrue((skill / "SKILL.md").is_file(), item["skill"])

    def test_retired_compact_aliases_are_absent(self):
        for skill_id in (
            "anti-ai-slop-design",
            "anti-ai-slop-writing",
            "ui-ux-pro-max-intelligence",
            "mobile-native-app-design",
            "diagram-and-architecture-visuals",
        ):
            self.assertFalse((ROOT / "skills" / skill_id).exists(), skill_id)

    def test_multifile_private_jit_package_includes_every_regular_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill = Path(tmp) / "skill"
            (skill / "scripts").mkdir(parents=True)
            (skill / "assets").mkdir()
            (skill / "agents").mkdir()
            (skill / "SKILL.md").write_text("# skill\n", encoding="utf-8")
            (skill / "scripts" / "x.mjs").write_text("export {};\n", encoding="utf-8")
            (skill / "assets" / "x.txt").write_text("asset\n", encoding="utf-8")
            (skill / "agents" / "x.toml").write_text('name="x"\n', encoding="utf-8")
            self.assertEqual(
                _package_files(skill),
                ["SKILL.md", "agents/x.toml", "assets/x.txt", "scripts/x.mjs"],
            )

    def test_addy_shared_reference_manifest_resolves(self):
        refs = _shared_reference_files(ROOT)
        self.assertTrue(refs)
        self.assertIn("definition-of-done.md", refs)
        for relative in refs:
            self.assertTrue((ROOT / "references" / relative).is_file())

    def test_profiles_resolve_canonical_replacements(self):
        catalog = load_catalog(ROOT / "profiles.yaml")
        resolved = resolve_profile("all", catalog, repo_root=ROOT)
        for skill_id in (
            "humanizer",
            "stop-slop",
            "hallmark",
            "ui-ux-pro-max",
            "appllama-app-design-skill",
            "appllama-usage",
            "diagram-design",
        ):
            self.assertIn(skill_id, resolved)


if __name__ == "__main__":
    unittest.main()
