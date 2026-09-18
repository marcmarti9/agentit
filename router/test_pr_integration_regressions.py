"""Adversarial PR review: fail closed without confusing availability with selection.

These probes exercise byte transport and evidence freshness, not model obedience.
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from router import loop_runtime, skill_loader, worker_context


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class PrIntegrationRegressions(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.project = self.root / 'project'
        self.harness = self.root / 'harness'
        self.project.mkdir()
        self.harness.mkdir()

    def native(self, data=b'Native procedure\n'):
        path = self.project / '.agents/skills/example/SKILL.md'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def cached(self, data=b'Cached procedure\n', *, canonical=True):
        relative = '.agentit/profile-skills/example/SKILL.md'
        path = self.project / relative
        path.parent.mkdir(parents=True)
        path.write_bytes(data)
        meta = dict(managed=True, destination=relative, installed_sha256=digest(data), source_sha256=digest(data))
        manifest = {'schema_version': 1, 'skills': {'example': meta}}
        (self.project / '.agentit/skills-manifest.json').write_text(json.dumps(manifest))
        if canonical:
            source = self.harness / 'skills/example/SKILL.md'
            source.parent.mkdir(parents=True)
            source.write_bytes(data)
        return path, manifest

    def worker(self):
        return worker_context.build_and_validate(
            worker_context.WorkerTaskSpec(objective='Review the explicit procedure', skills=['example']),
            project_root=self.project,
        )

    def command(self):
        return loop_runtime.new_loop(goal='Check the source', verifier='Run observed fixture',
            stop_condition='exit zero and source unchanged',
            verifier_argv=[sys.executable, '-c', 'print("observed")'],
            verifier_cwd=str(self.project), subject_paths=['src'])

    def test_retired_canonical_skill_cannot_survive_as_private_cache(self):
        self.cached(canonical=False)
        with patch.object(skill_loader, 'HARNESS_ROOT', self.harness):
            with self.assertRaises(skill_loader.SkillLoadError):
                skill_loader.load_skill_bodies(['example'], project_root=self.project)

    def test_deleted_canonical_reference_cannot_survive_as_private_cache(self):
        path, manifest = self.cached()
        resource = path.parent / 'references/removed.md'
        resource.parent.mkdir()
        resource.write_bytes(b'Retired reference\n')
        meta = manifest['skills']['example']
        meta['files'] = {'SKILL.md': {k: meta[k] for k in ('managed', 'installed_sha256', 'source_sha256')},
                         'references/removed.md': dict(managed=True, installed_sha256=digest(resource.read_bytes()), source_sha256=digest(resource.read_bytes()))}
        (self.project / '.agentit/skills-manifest.json').write_text(json.dumps(manifest))
        with patch.object(skill_loader, 'HARNESS_ROOT', self.harness):
            with self.assertRaises(skill_loader.SkillLoadError):
                skill_loader.load_reference_bodies(['skill:example/references/removed.md'], project_root=self.project)

    def test_native_crlf_bytes_are_delivered_without_newline_translation(self):
        path = self.native(b'First line\r\nSecond line\r\n')
        body = skill_loader.load_skill_bodies(['example'], project_root=self.project)[0]
        self.assertEqual(body['content'].encode('utf-8'), path.read_bytes())
        self.assertEqual(body['sha256'], digest(path.read_bytes()))
        self.assertEqual(body['bytes'], len(path.read_bytes()))

    def test_rendered_prompt_preserves_the_entire_selected_body(self):
        self.native(b'Procedure with terminal whitespace\r\n\r\n  ')
        bodies = skill_loader.load_skill_bodies(['example'], project_root=self.project)
        self.assertIn(bodies[0]['content'], skill_loader.render_prompt(bodies))

    def test_worker_rejects_a_removed_authority_envelope(self):
        self.native()
        payload = self.worker()
        payload['worker_context'].pop('skill_authority', None)
        with self.assertRaises(worker_context.WorkerContextError):
            worker_context.validate_for_spawn(payload)

    def test_valid_crlf_cache_is_not_rejected_as_corrupt(self):
        path, _ = self.cached(b'First line\r\nSecond line\r\n')
        with patch.object(skill_loader, 'HARNESS_ROOT', self.harness):
            body = skill_loader.load_skill_bodies(['example'], project_root=self.project)[0]
        self.assertEqual(body['content'].encode(), path.read_bytes())

    def test_unselected_broken_manifest_cannot_block_native_worker(self):
        self.native()
        (self.project / '.agentit').mkdir()
        (self.project / '.agentit/skills-manifest.json').write_text('{broken')
        self.assertEqual(self.worker()['worker_context']['skills_projected'], ['example'])

    def test_selected_broken_cache_manifest_still_fails_closed(self):
        self.cached()
        (self.project / '.agentit/skills-manifest.json').write_text('{broken')
        with patch.object(skill_loader, 'HARNESS_ROOT', self.harness):
            with self.assertRaises(worker_context.WorkerContextError):
                self.worker()

    def test_worker_rejects_mutated_project_instruction(self):
        self.native()
        (self.project / 'AGENTS.md').write_text('Do not alter production settings.\n')
        payload = self.worker()
        payload['worker_context']['project_instructions'][0]['content'] = 'Alter production settings.'
        with self.assertRaises(worker_context.WorkerContextError):
            worker_context.validate_for_spawn(payload)

    def test_worker_rejects_dropped_project_instruction(self):
        self.native()
        (self.project / 'AGENTS.md').write_text('Preserve project constraints.\n')
        payload = self.worker()
        payload['worker_context']['project_instructions'] = []
        with self.assertRaises(worker_context.WorkerContextError):
            worker_context.validate_for_spawn(payload)

    def test_passed_source_evidence_expires_on_executable_mode_change(self):
        (self.project / 'src').mkdir()
        script = self.project / 'src/check.sh'
        script.write_text('#!/bin/sh\nexit 0\n')
        script.chmod(0o644)
        result = loop_runtime.run_verifier(self.command(), timeout=3)
        self.assertEqual(result['status'], 'passed')
        script.chmod(0o755)
        with self.assertRaises(loop_runtime.LoopRuntimeError):
            loop_runtime.validate_current_subject(result)

    def test_passed_source_evidence_expires_on_empty_directory_change(self):
        (self.project / 'src').mkdir()
        result = loop_runtime.run_verifier(self.command(), timeout=3)
        self.assertEqual(result['status'], 'passed')
        (self.project / 'src/new-directory').mkdir()
        with self.assertRaises(loop_runtime.LoopRuntimeError):
            loop_runtime.validate_current_subject(result)

    @unittest.skipUnless(hasattr(os, 'mkfifo'), 'POSIX FIFO fixture')
    def test_special_source_file_is_rejected_not_silently_ignored(self):
        (self.project / 'src').mkdir()
        os.mkfifo(self.project / 'src/pipe')
        with self.assertRaises(loop_runtime.LoopRuntimeError):
            loop_runtime.run_verifier(self.command(), timeout=3)


if __name__ == '__main__':
    unittest.main()
