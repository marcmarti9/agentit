from pathlib import Path
import unittest

from router.profiles import load_catalog, resolve_profile


ROOT = Path(__file__).resolve().parents[1]


class AntiOverengineeringProfileTests(unittest.TestCase):
    def test_skill_is_discoverable_for_coding_profiles_but_not_global_core(self) -> None:
        catalog = load_catalog(ROOT / "profiles.yaml")

        core = resolve_profile("core", catalog, repo_root=ROOT)
        self.assertNotIn("anti-overengineering", core)

        for profile_name in ("frontend", "backend", "agency", "all"):
            with self.subTest(profile=profile_name):
                resolved = resolve_profile(profile_name, catalog, repo_root=ROOT)
                self.assertIn("anti-overengineering", resolved)

    def test_skill_package_exists(self) -> None:
        skill = ROOT / "skills" / "anti-overengineering" / "SKILL.md"
        self.assertTrue(skill.is_file())
        body = skill.read_text(encoding="utf-8")
        self.assertIn("## Phase-aware development", body)
        self.assertIn("MILESTONE / PRODUCT COMPLETE", body)
        self.assertIn("verification cadence", body)


if __name__ == "__main__":
    unittest.main()
