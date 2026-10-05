"""Unified source delivery, deduplication and real changed trust boundaries."""
from __future__ import annotations
import hashlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from contextlib import redirect_stdout, redirect_stderr
from unittest.mock import patch

from router import ecc, skill_loader
from router.bootstrap import _tree_files
from router.profiles import load_catalog, repository_skill_ids, resolve_profile
from router.profile_jit_cli import _enable
from router.worker_context import WorkerTaskSpec, build_and_validate, render_worker_prompt

ROOT = Path(__file__).resolve().parents[1]


class ECCIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lock = ecc.load_lock(ROOT)

    def test_inventory_and_single_canonical_owner(self):
        self.assertIsNotNone(self.lock)
        native = {p.parent.name for p in (ROOT/'skills').glob('*/SKILL.md')}
        original = {p.parent.name for p in (ROOT/'vendor/ecc/skills').glob('*/SKILL.md')}
        aliases = self.lock['aliases']
        active = ecc.canonical_ids(ROOT)
        self.assertEqual(original, active | set(aliases))
        self.assertFalse(active & native)
        self.assertFalse(active & set(aliases))
        self.assertEqual(repository_skill_ids(ROOT), native | active)
        catalog=load_catalog()
        self.assertEqual(set(resolve_profile('all', catalog, repo_root=ROOT)), native | active)
        self.assertEqual(resolve_profile('core', catalog), ['using-agentit','task-router','using-agent-skills'])
        for name, entry in aliases.items():
            with self.assertRaisesRegex(ecc.ECCError, entry['canonical']):
                ecc.skill_dir(ROOT, name)

    def test_every_canonical_ecc_body_is_delivered_exactly_not_a_wrapper(self):
        with tempfile.TemporaryDirectory() as tmp:
            ids=sorted(self.lock['skills'])
            bodies=skill_loader.load_skill_bodies(ids, project_root=Path(tmp))
        skill_loader.validate_bodies(ids,bodies)
        for body in bodies:
            expected=(ROOT/'vendor/ecc/skills'/body['id']/'SKILL.md').read_bytes()
            self.assertEqual(body['content'].encode(),expected)
            self.assertEqual(body['sha256'],hashlib.sha256(expected).hexdigest())
            self.assertEqual(body['upstream_root'],str(ROOT/'vendor/ecc'))

    def test_project_override_remains_first(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); p=root/'.agents/skills/api-design/SKILL.md'
            p.parent.mkdir(parents=True); p.write_text('Local project API contract.\n')
            body=skill_loader.load_skill_bodies(['api-design'],project_root=root)[0]
            self.assertEqual(body['source'],'project')
            self.assertEqual(body['content'],p.read_text())

    def test_private_enable_is_idempotent_and_does_not_expose_host_skills(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); catalog=load_catalog()
            for _ in range(2):
                _enable('ecc-web',project=root,repo_root=ROOT,catalog=catalog,apply=True)
            self.assertFalse((root/'.agents/skills').exists())
            body=skill_loader.load_skill_bodies(['browser-qa'],project_root=root)[0]
            self.assertEqual(body['source'],'project-agentit-profile')
            self.assertEqual(body['content'].encode(),(ROOT/'vendor/ecc/skills/browser-qa/SKILL.md').read_bytes())
            p=root/'.agentit/profile-skills/browser-qa/SKILL.md'; p.write_text('tampered')
            with self.assertRaisesRegex(skill_loader.SkillLoadError,'hash mismatch'):
                skill_loader.load_skill_bodies(['browser-qa'],project_root=root)

    def test_shared_ecc_resource_is_explicit_and_worker_receives_full_bytes(self):
        locator='repo:vendor/ecc/agents/architect.md'
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            bodies=skill_loader.load_reference_bodies([locator],project_root=root)
            self.assertEqual(len(bodies),1)
            self.assertEqual(bodies[0]['content'].encode(),(ROOT/'vendor/ecc/agents/architect.md').read_bytes())
            payload=build_and_validate(WorkerTaskSpec(objective='Design an API contract',skills=('api-design',),references=(locator,)),project_root=root)
            text=render_worker_prompt(payload)
            self.assertIn((ROOT/'vendor/ecc/skills/api-design/SKILL.md').read_text(),text)
            self.assertIn(bodies[0]['content'],text)

    def test_paths_fail_closed(self):
        for relative in ('../LICENSE','/etc/passwd','skills\\api-design','skills//api-design/SKILL.md'):
            with self.subTest(relative=relative), self.assertRaises(ecc.ECCError):
                ecc.safe_file(ROOT,relative)
        with self.assertRaises(ecc.ECCError):
            ecc.skill_dir(ROOT,'../api-design')
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); (root/'x').symlink_to(ROOT/'LICENSE')
            with self.assertRaisesRegex(ecc.ECCError,'symlink'):
                ecc.safe_file(root,'x')

    def test_selected_source_and_reference_tampering_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for rel in ('references/ecc-policy.json','vendor/ecc.lock.json','vendor/ecc/skills/api-design/SKILL.md','vendor/ecc/agents/architect.md'):
                target=root/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/rel,target)
            with patch.object(skill_loader,'HARNESS_ROOT',root):
                target=root/'vendor/ecc/skills/api-design/SKILL.md';target.write_text('tampered')
                with self.assertRaisesRegex(skill_loader.SkillLoadError,'integrity mismatch'):
                    skill_loader.load_skill_bodies(['api-design'],project_root=root)
                target=root/'vendor/ecc/agents/architect.md';target.write_text('tampered')
                with self.assertRaisesRegex(skill_loader.SkillLoadError,'integrity mismatch'):
                    skill_loader.load_reference_bodies(['repo:vendor/ecc/agents/architect.md'],project_root=root)

    def test_import_checks_revision_and_cannot_write_through_vendor_symlink(self):
        from scripts.ecc_integrate import generate
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); (root/'references').mkdir()
            shutil.copy2(ROOT/'references/ecc-policy.json',root/'references/ecc-policy.json')
            with self.assertRaisesRegex(ecc.ECCError,'revision'):
                generate(root,ROOT/'vendor/ecc','0'*40)
            (root/'skills').mkdir()
            for alias in self.lock['aliases'].values():
                sid=alias['canonical']
                if (ROOT/'skills'/sid).exists():
                    shutil.copytree(ROOT/'skills'/sid,root/'skills'/sid)
            (root/'vendor').symlink_to(ROOT/'vendor',target_is_directory=True)
            with self.assertRaisesRegex(ecc.ECCError,'symlink vendor'):
                generate(root,ROOT/'vendor/ecc',self.lock['revision'])

    def test_discovery_does_not_execute_or_load_skill_bodies(self):
        with patch.object(ecc.subprocess,'run',side_effect=AssertionError('unexpected execution')):
            with redirect_stdout(io.StringIO()) as output:
                self.assertEqual(ecc.main(['list','--kind','skills']),0)
            result=json.loads(output.getvalue())
            self.assertNotIn('content',result['api-design'])
            self.assertNotIn('tdd-workflow',result)

    def test_native_execution_requires_explicit_boundary_and_blocks_updater(self):
        for args in (['run','--','setup'],['run','--allow-host-changes','--','auto-update']):
            with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as exc:
                ecc.main(args)
            self.assertEqual(exc.exception.code,2)

    def test_bootstrap_prunes_native_dependencies_before_symlink_inspection(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'keep').write_text('source')
            (root/'node_modules').mkdir();(root/'node_modules/linked').symlink_to('/nonexistent')
            self.assertEqual([p.name for p in _tree_files(root,excluded_names={'node_modules'})],['keep'])
            (root/'bad').symlink_to('/nonexistent')
            with self.assertRaisesRegex(Exception,'non-regular|symlink'):
                list(_tree_files(root,excluded_names={'node_modules'}))


if __name__=='__main__':
    unittest.main()
