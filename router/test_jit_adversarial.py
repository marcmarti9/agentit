"""Behavioral regressions from the 2026-09-18 adversarial audit.

No model calls: these test delivery/enforcement, not semantic routing accuracy.
"""
from __future__ import annotations
import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import yaml
from router import skill_loader, worker_context, loop_runtime
from router.skills_cli import list_packs, pack_candidates

ROOT = Path(__file__).resolve().parents[1]

def local_skill(root: Path, name='test-procedure', text='UNIQUE_PROCEDURE_749: preserve the audit sentinel.'):
    path = root / '.agents/skills' / name / 'SKILL.md'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return path

class DeliveryRegressionTests(unittest.TestCase):
    def test_worker_contains_selected_body_not_just_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); body=local_skill(root)
            p=worker_context.build_and_validate(worker_context.WorkerTaskSpec(objective='Review sentinel',skills=['test-procedure']),project_root=root)
            self.assertIn(body.read_text(),worker_context.render_worker_prompt(p))
            self.assertEqual(hashlib.sha256(body.read_bytes()).hexdigest(),p['worker_context']['skill_bodies'][0]['sha256'])

    def test_worker_rejects_missing_or_tampered_body(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); local_skill(root)
            p=worker_context.build_and_validate(worker_context.WorkerTaskSpec(objective='Review',skills=['test-procedure']),project_root=root)
            stripped=copy.deepcopy(p); stripped['worker_context'].pop('skill_bodies',None)
            with self.assertRaises(worker_context.WorkerContextError): worker_context.validate_for_spawn(stripped)
            p['worker_context']['skill_bodies'][0]['content']='altered instruction'
            with self.assertRaises(worker_context.WorkerContextError): worker_context.validate_for_spawn(p)

    def test_availability_never_becomes_selection(self):
        result=worker_context.resolve_skills_projected(task_skills=[],manifest_skills=['unselected'],include_manifest_skills=True)
        self.assertEqual([],result)

    def test_intermediate_instructions_reach_worker(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); (root/'packages/web').mkdir(parents=True)
            for path,text in [('AGENTS.md','root'),('packages/AGENTS.md','intermediate'),('packages/web/AGENTS.md','leaf')]: (root/path).write_text(text)
            p=worker_context.build_and_validate(worker_context.WorkerTaskSpec(objective='Review',work_subdir='packages/web'),project_root=root)
            self.assertEqual(['AGENTS.md','packages/AGENTS.md','packages/web/AGENTS.md'],p['worker_context']['project_instruction_paths'])

    def test_no_arbitrary_twelve_skill_cap(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); names=[f'bounded-{i}' for i in range(13)]
            for name in names: local_skill(root,name,'one brief required rule')
            p=worker_context.build_and_validate(worker_context.WorkerTaskSpec(objective='Explicitly compare 13 short procedures',skills=names),project_root=root)
            self.assertEqual(names,p['worker_context']['skills_projected'])

    def test_unread_references_do_not_pass_spawn(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=worker_context.build_worker_context(worker_context.WorkerTaskSpec(objective='Read source',references=['https://example.test/not-yet-read']),project_root=Path(tmp))
            with self.assertRaises(worker_context.WorkerContextError): worker_context.validate_for_spawn(p)

    def test_separate_worker_does_not_inherit_previous_selection(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); local_skill(root,'first','FIRST_CONTEXT_ONLY'); local_skill(root,'second','SECOND_CONTEXT_ONLY')
            for name,other in [('first','SECOND_CONTEXT_ONLY'),('second','FIRST_CONTEXT_ONLY')]:
                p=worker_context.build_and_validate(worker_context.WorkerTaskSpec(objective=name,skills=[name]),project_root=root)
                self.assertNotIn(other,worker_context.render_worker_prompt(p))

class LoaderRegressionTests(unittest.TestCase):
    def test_symlink_root_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp); (p/'real').mkdir(); (p/'link').symlink_to(p/'real',target_is_directory=True)
            with self.assertRaises(skill_loader.SkillLoadError): skill_loader.load_skill_bodies(['task-router'],project_root=p/'link')

    def test_dangling_skill_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); p=root/'.agents/skills/task-router'; p.mkdir(parents=True); (p/'SKILL.md').symlink_to(root/'absent')
            with self.assertRaises(skill_loader.SkillLoadError): skill_loader.load_skill_bodies(['task-router'],project_root=root)

    def test_unmanaged_cache_does_not_override_harness(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); p=root/'.agentit/profile-skills/task-router'; p.mkdir(parents=True); (p/'SKILL.md').write_text('UNOWNED OVERRIDE')
            with self.assertRaises(skill_loader.SkillLoadError): skill_loader.load_skill_bodies(['task-router'],project_root=root)

    def test_resources_use_explicit_roots_and_reject_traversal(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); local_skill(root); p=root/'.agents/skills/test-procedure/references'; p.mkdir(); (p/'one.md').write_text('RESOURCE_749')
            resources=skill_loader.load_reference_bodies(['skill:test-procedure/references/one.md'],project_root=root)
            self.assertEqual('RESOURCE_749',resources[0]['content'])
            with self.assertRaises(skill_loader.SkillLoadError): skill_loader.load_reference_bodies(['project:../outside.md'],project_root=root)

    def test_cli_receipt_is_bound_to_explicit_task_and_stage(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); local_skill(root)
            result=subprocess.run([sys.executable,str(ROOT/'agentit'),'skills','show','test-procedure','--project',str(root),'--task-id','audit-749','--stage','implementation','--receipt','--format','json'],capture_output=True,text=True)
            self.assertEqual(0,result.returncode,result.stderr)
            data=json.loads(result.stdout); receipt=data['delivery_receipt']
            self.assertEqual('audit-749',receipt['task_id']); self.assertEqual('implementation',receipt['stage'])
            self.assertFalse(receipt['proves_model_compliance']); self.assertTrue(Path(data['receipt_path']).is_file())

class CatalogRegressionTests(unittest.TestCase):
    def test_every_skill_has_valid_discoverable_metadata(self):
        catalog=yaml.safe_load((ROOT/'profiles.yaml').read_text()); core=set(catalog['profiles']['core']['skills'])
        covered={i['id'] for i in pack_candidates([p['id'] for p in list_packs()])}
        for path in sorted((ROOT/'skills').glob('*/SKILL.md')):
            with self.subTest(skill=path.parent.name):
                meta=yaml.safe_load(path.read_text().split('---',2)[1])
                self.assertEqual(path.parent.name,meta['name'])
                self.assertIsInstance(meta['description'],str); self.assertTrue(0<len(meta['description'])<=1024)
                self.assertIn(path.parent.name,core|covered)

    def test_core_has_bounded_delivery_size(self):
        ids=('using-agentit','task-router','using-agent-skills')
        total=sum((ROOT/'skills'/i/'SKILL.md').stat().st_size for i in ids)
        # A measured product constraint for our bootstrap, NOT a task skill quota.
        self.assertLessEqual(total,16000)

class VerificationRegressionTests(unittest.TestCase):
    def test_command_contract_rejects_self_report(self):
        loop=loop_runtime.new_loop(goal='Test',verifier='python check',stop_condition='zero',verifier_argv=[sys.executable,'-c','pass'],verifier_cwd=str(ROOT))
        with self.assertRaises(loop_runtime.LoopRuntimeError): loop_runtime.record_attempt(loop,passed=True,strategy='claim',evidence='passed')

    def test_real_command_pass_failure_and_timeout(self):
        with tempfile.TemporaryDirectory() as tmp:
            for code,expected in [('print("observed")','passed'),('raise SystemExit(7)','retryable'),('import time;time.sleep(5)','retryable')]:
                with self.subTest(code=code):
                    loop=loop_runtime.new_loop(goal='Test',verifier='execute fixture',stop_condition='zero',verifier_argv=[sys.executable,'-c',code],verifier_cwd=tmp)
                    result=loop_runtime.run_verifier(loop,timeout=(0.15 if "time.sleep" in code else 3))
                    self.assertEqual(expected,result['status'])
                    receipt=loop_runtime.loop_receipt(result)
                    self.assertEqual('command',receipt['evidence_source'])
                    self.assertIn('started_at',result['attempts'][-1]['execution'])

    def test_reported_evidence_is_honestly_labelled(self):
        loop=loop_runtime.new_loop(goal='Visual check',verifier='human inspection',stop_condition='reviewed')
        receipt=loop_runtime.loop_receipt(loop_runtime.record_attempt(loop,passed=True,strategy='manual',evidence='human reports inspection'))
        self.assertEqual('reported',receipt['evidence_source'])
        with self.assertRaises(loop_runtime.LoopRuntimeError): loop_runtime.validate_loop_receipt(receipt,require_command=True)

if __name__=='__main__': unittest.main()
