"""Separate-process and stale-evidence probes, not behavioral LLM evaluations."""
from pathlib import Path
import copy
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from router import graph_runtime, loop_runtime, skill_loader, worker_context

ROOT = Path(__file__).resolve().parents[1]


def cli(project, *args):
    return subprocess.run([sys.executable, str(ROOT / 'agentit'), *args], cwd=project,
                          capture_output=True, text=True, timeout=30)


class JitIntegrationTests(unittest.TestCase):
    def test_separate_processes_deliver_only_their_selected_skill(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in ('first-stage', 'second-stage'):
                package = root / '.agents/skills' / name
                package.mkdir(parents=True)
                (package / 'SKILL.md').write_text(f'---\nname: {name}\ndescription: Isolated fixture.\n---\nSECRET_SENTINEL_{name}\n')
            first = cli(root, 'worker', 'build', '--project', tmp, '--objective', 'First stage', '--skill', 'first-stage')
            second = cli(root, 'worker', 'build', '--project', tmp, '--objective', 'Second stage', '--skill', 'second-stage')
            self.assertEqual(0, first.returncode, first.stderr)
            self.assertEqual(0, second.returncode, second.stderr)
            self.assertIn('SECRET_SENTINEL_first-stage', first.stdout)
            self.assertNotIn('SECRET_SENTINEL_first-stage', second.stdout)
            self.assertIn('SECRET_SENTINEL_second-stage', second.stdout)
            self.assertNotIn('SECRET_SENTINEL_second-stage', first.stdout)

    def test_real_profile_cache_is_readable_and_tampering_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            enabled = cli(root, 'enable', 'core', '--project', tmp, '--apply')
            self.assertEqual(0, enabled.returncode, enabled.stderr + enabled.stdout)
            bodies = skill_loader.load_skill_bodies(['task-router'], project_root=root)
            self.assertEqual('project-agentit-profile', bodies[0]['source'])
            body = root / '.agentit/profile-skills/task-router/SKILL.md'
            body.write_text(body.read_text() + '\nUNOWNED CHANGE\n')
            with self.assertRaisesRegex(skill_loader.SkillLoadError, 'hash mismatch'):
                skill_loader.load_skill_bodies(['task-router'], project_root=root)

    def test_source_drift_in_cache_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); harness = root / 'harness'; project = root / 'project'
            project.mkdir(); canonical = harness / 'skills/task-router/SKILL.md'
            canonical.parent.mkdir(parents=True); canonical.write_text('NEW SOURCE')
            cached = project / '.agentit/profile-skills/task-router/SKILL.md'
            cached.parent.mkdir(parents=True); cached.write_text('OLD SOURCE')
            sha = hashlib.sha256(b'OLD SOURCE').hexdigest()
            (project / '.agentit/skills-manifest.json').write_text(json.dumps({
                'schema_version': 1, 'skills': {'task-router': {
                    'managed': True, 'destination': '.agentit/profile-skills/task-router/SKILL.md',
                    'installed_sha256': sha, 'source_sha256': sha}}}))
            with patch.object(skill_loader, 'HARNESS_ROOT', harness):
                with self.assertRaisesRegex(skill_loader.SkillLoadError, 'source is stale'):
                    skill_loader.load_skill_bodies(['task-router'], project_root=project)

    def test_worker_contains_reference_data_not_just_a_locator(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); (root / 'proof.md').write_text('EVIDENCE_SENTINEL_812')
            payload = worker_context.build_and_validate(worker_context.WorkerTaskSpec(
                objective='Read evidence', references=['project:proof.md']), project_root=root)
            self.assertIn('EVIDENCE_SENTINEL_812', worker_context.render_worker_prompt(payload))
            payload['worker_context']['reference_bodies'][0]['content'] = 'ALTERED'
            with self.assertRaises(worker_context.WorkerContextError):
                worker_context.validate_for_spawn(payload)

    def test_stale_source_cannot_reuse_command_receipt(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); source = root / 'source.py'; source.write_text('version = 1\n')
            loop = loop_runtime.new_loop(goal='verify source', verifier='fixture', stop_condition='zero',
                verifier_argv=[sys.executable, '-c', 'pass'], verifier_cwd=tmp, subject_paths=['source.py'])
            passed = loop_runtime.run_verifier(loop, timeout=5)
            loop_runtime.validate_current_subject(passed)
            source.write_text('version = 2\n')
            with self.assertRaisesRegex(loop_runtime.LoopRuntimeError, 'stale evidence'):
                loop_runtime.validate_current_subject(passed)

    def test_verifier_mutating_its_subject_does_not_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); (root / 'source.txt').write_text('before')
            loop = loop_runtime.new_loop(goal='verify', verifier='mutating fixture', stop_condition='unchanged',
                verifier_argv=[sys.executable, '-c', 'from pathlib import Path; Path("source.txt").write_text("after")'],
                verifier_cwd=tmp, subject_paths=['source.txt'])
            result = loop_runtime.run_verifier(loop, timeout=5)
            self.assertEqual('retryable', result['status'])
            self.assertEqual(0, result['attempts'][0]['execution']['exit_code'])

    def test_graph_requires_observed_command_when_its_contract_says_so(self):
        loop = loop_runtime.new_loop(goal='test', verifier='manual', stop_condition='review')
        receipt = loop_runtime.loop_receipt(loop_runtime.record_attempt(loop, passed=True,
            strategy='manual', evidence='reported only'))
        graph = graph_runtime.new_graph(nodes=[{
            'id': 'step', 'goal': 'test', 'loop_contract_sha256': loop['contract_sha256'],
            'evidence_requirement': 'command'}])
        with self.assertRaises((graph_runtime.GraphRuntimeError, loop_runtime.LoopRuntimeError)):
            graph_runtime.complete_node(graph, node_id='step', loop_receipt=receipt)

    def test_state_symlink_is_rejected_without_overwriting_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); target = root / 'user.json'; target.write_text('USER DATA')
            (root / 'state.json').symlink_to(target)
            result = cli(root, 'runtime', 'loop-init', '--state', str(root / 'state.json'),
                         '--goal', 'probe', '--verifier', 'manual', '--stop', 'done')
            self.assertNotEqual(0, result.returncode)
            self.assertEqual('USER DATA', target.read_text())


if __name__ == '__main__':
    unittest.main()
