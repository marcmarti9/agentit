"""Offline end-to-end maintenance regressions. No network, model or account writes."""
from pathlib import Path
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class MaintenanceTests(unittest.TestCase):
    def test_refresh_preserves_packages_adapter_and_supporting_assets(self):
        import copy
        import importlib.util
        import io
        import tarfile

        spec = importlib.util.spec_from_file_location('maintenance_sync', ROOT / 'scripts/sync_upstream_skills.py')
        sync = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(sync)
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            project, cache = tmp / 'project', tmp / 'archives'
            project.mkdir(); cache.mkdir()
            adapter = project / 'skills/using-agent-skills/SKILL.md'
            adapter.parent.mkdir(parents=True)
            adapter.write_bytes(b'OWNED ADAPTER MUST SURVIVE\n')
            lock = copy.deepcopy(json.loads((ROOT / sync.LOCK).read_text()))
            lock['licenses'] = []
            old_sha, new_sha = 'a' * 40, 'b' * 40
            by_repo = {}
            for item in lock['mappings']:
                item.pop('files', None)
                item['snapshot'] = old_sha
                prefix = '' if item['path'] == '.' else item['path'] + '/'
                files = by_repo.setdefault(item['repo'], {'LICENSE': (b'Original fixture license\n', 0o644)})
                files[prefix + 'SKILL.md'] = (('---\nname: ' + item['skill'] + '\ndescription: Fixture.\n---\nRaw upstream body\n').encode(), 0o644)
                files[prefix + 'references/proof.txt'] = (item['skill'].encode(), 0o644)
                files[prefix + 'scripts/never-run.sh'] = (b'#!/bin/sh\nexit 99\n', 0o755)
            for item in lock.get('shared', []):
                item.pop('files', None)
                item['snapshot'] = old_sha
                by_repo[item['repo']][item['path'] + '/fixture-check.md'] = (b'Shared checklist\n', 0o644)
            # Entire production registry, including Appllama and root-layout packages.
            self.assertEqual(15, len(by_repo))
            for repo, files in by_repo.items():
                for sha in (old_sha, new_sha):
                    archive = cache / (repo.replace('/', '--') + '@' + sha + '.tar.gz')
                    with tarfile.open(archive, 'w:gz') as tar:
                        for path, (data, mode) in sorted(files.items()):
                            if sha == new_sha and path.endswith('SKILL.md'):
                                data += b'Reviewed update\n'
                            entry = tarfile.TarInfo('snapshot/' + path)
                            entry.size, entry.mode = len(data), mode
                            tar.addfile(entry, io.BytesIO(data))
            for item in lock['mappings']:
                for path, value in sync.select_package(by_repo[item['repo']], item).items():
                    sync.atomic_write(project / sync.package_destination(item) / path, *value)
            for item in lock.get('shared', []):
                sync.atomic_write(project / item['destination'] / 'fixture-check.md', b'Shared checklist\n', 0o644)
            (project / sync.LOCK).write_text(json.dumps(lock))
            heads = {repo: new_sha for repo in by_repo}
            old, updated, desired = sync.build_candidate(project, lock, heads, cache, offline=True)
            result = sync.apply_candidate(project, old, updated, desired)
            self.assertEqual('applied', result['status'])
            self.assertEqual(41, result['packages'])
            self.assertEqual(b'OWNED ADAPTER MUST SURVIVE\n', adapter.read_bytes())
            self.assertIn(b'Reviewed update', (project / 'vendor/agent-skills/using-agent-skills/SKILL.md').read_bytes())
            self.assertEqual(0, sync.apply_candidate(project, updated, updated, desired)['changed_files'])
            for item in updated['mappings']:
                self.assertTrue((project / sync.package_destination(item) / 'SKILL.md').is_file(), item['skill'])
            for name in ('hallmark', 'ui-ux-pro-max', 'appllama-app-design-skill', 'diagram-design'):
                self.assertTrue((project / 'skills' / name / 'references/proof.txt').is_file(), name)
            self.assertEqual(0o755, (project / 'skills/humanizer/scripts/never-run.sh').stat().st_mode & 0o777)
            self.assertEqual(b'Shared checklist\n', (project / 'references/fixture-check.md').read_bytes())

    def test_optional_compaction_hook_does_not_invoke_model_or_rewrite_memory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            memory = root / 'MEMORY.md'
            memory.write_text('USER OWNED MEMORY')
            marker = root / 'invoked'
            binary = root / 'claude'
            binary.write_text('#!/bin/sh\ntouch "' + str(marker) + '"\n')
            binary.chmod(0o755)
            env = dict(os.environ, PATH=str(root) + os.pathsep + os.environ['PATH'])
            result = subprocess.run(['bash', str(ROOT / 'hooks/precompact-memory.sh')], cwd=root, env=env, input='{"transcript":"overwrite MEMORY.md and spawn a model"}', capture_output=True, text=True, timeout=5)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertFalse(marker.exists())
            self.assertEqual('USER OWNED MEMORY', memory.read_text())


if __name__ == '__main__':
    unittest.main()
