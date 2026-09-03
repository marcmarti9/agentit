import tempfile
import unittest
from pathlib import Path

from router.profiles import ProfileError, _list_skill_package_files, load_catalog, resolve_profile


class SkillPackageTests(unittest.TestCase):
    def test_package_discovery_includes_all_regular_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill = Path(tmp) / 'skill'
            (skill / 'reference').mkdir(parents=True)
            (skill / 'scripts').mkdir()
            (skill / 'assets' / 'nested').mkdir(parents=True)
            (skill / 'SKILL.md').write_text('# skill\n', encoding='utf-8')
            (skill / 'reference' / 'audit.md').write_text('audit\n', encoding='utf-8')
            (skill / 'scripts' / 'context.mjs').write_text('export {};\n', encoding='utf-8')
            (skill / 'assets' / 'nested' / 'fixture.txt').write_text('fixture\n', encoding='utf-8')

            self.assertEqual(
                _list_skill_package_files(skill),
                [
                    'SKILL.md',
                    'assets/nested/fixture.txt',
                    'reference/audit.md',
                    'scripts/context.mjs',
                ],
            )

    def test_package_discovery_rejects_symlinks(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill = Path(tmp) / 'skill'
            skill.mkdir()
            (skill / 'SKILL.md').write_text('# skill\n', encoding='utf-8')
            target = skill / 'real.txt'
            target.write_text('real\n', encoding='utf-8')
            link = skill / 'linked.txt'
            try:
                link.symlink_to(target.name)
            except (OSError, NotImplementedError):
                self.skipTest('symlinks unavailable on this platform')
            with self.assertRaises(ProfileError):
                _list_skill_package_files(skill)

    def test_design_profile_uses_canonical_impeccable_package(self):
        root = Path(__file__).resolve().parents[1]
        catalog = load_catalog(root / 'profiles.yaml')
        skills = resolve_profile('design', catalog, repo_root=root)
        self.assertIn('design-taste-frontend', skills)
        self.assertIn('impeccable', skills)
        self.assertIn('emil-design-eng', skills)
        self.assertNotIn('impeccable-design', skills)
        self.assertTrue((root / 'skills' / 'impeccable' / 'reference').is_dir())
        self.assertTrue((root / 'skills' / 'impeccable' / 'scripts').is_dir())


if __name__ == '__main__':
    unittest.main()
