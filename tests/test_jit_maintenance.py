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
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            project = tmp / 'project'
            (project / 'scripts').mkdir(parents=True)
            (project / 'skills/using-agent-skills').mkdir(parents=True)
            (project / 'references').mkdir()
            adapter = project / 'skills/using-agent-skills/SKILL.md'
            adapter.write_text('OWNED ADAPTER MUST SURVIVE')
            shutil.copy2(ROOT / 'scripts/sync-upstream-skills.sh', project / 'scripts')
            lock = json.loads((ROOT / 'skills/UPSTREAM_LOCK.json').read_text())
            fixture = tmp / 'upstreams'
            for item in lock['mappings']:
                package = fixture / item['repo'] / item['path']
                package.mkdir(parents=True, exist_ok=True)
                name = 'taste-skill' if item['skill'] == 'design-taste-frontend' else item['skill']
                (package / 'SKILL.md').write_text(f'---\nname: {name}\ndescription: Test package.\n---\nBody {name}\n')
                (package / 'references').mkdir(exist_ok=True)
                (package / 'references/proof.txt').write_text(item['skill'])
                (package / 'scripts').mkdir(exist_ok=True)
                (package / 'scripts/proof.txt').write_text(item['skill'])
            shared = fixture / 'addyosmani/agent-skills/references'
            shared.mkdir(parents=True)
            (shared / 'fixture-check.md').write_text('shared checklist')
            # Upstream may still carry its old meta-skill. It must not replace ours.
            unwanted = fixture / 'addyosmani/agent-skills/skills/using-agent-skills'
            unwanted.mkdir()
            (unwanted / 'SKILL.md').write_text('DO NOT COPY')
            bin_dir = tmp / 'bin'
            bin_dir.mkdir()
            fake_git = bin_dir / 'git'
            fake_git.write_text('#!' + sys.executable + '\n' + r'''
import os, shutil, sys
from pathlib import Path
a = sys.argv[1:]
if a[0] == 'clone':
    slug = a[-2].removeprefix('https://github.com/').removesuffix('.git')
    shutil.copytree(Path(os.environ['FIXTURE_ROOT']) / slug, a[-1])
elif a[-2:] == ['rev-parse', 'HEAD']:
    print('a' * 40)
elif a[-2:] == ['status', '--porcelain']:
    pass
else:
    raise SystemExit('unexpected git operation: ' + repr(a))
''')
            fake_git.chmod(0o755)
            env = dict(os.environ, PATH=str(bin_dir) + os.pathsep + os.environ['PATH'], FIXTURE_ROOT=str(fixture))
            result = subprocess.run(['bash', str(project / 'scripts/sync-upstream-skills.sh')], env=env, capture_output=True, text=True, timeout=45)
            self.assertEqual(0, result.returncode, result.stderr)
            current = json.loads((project / 'skills/UPSTREAM_LOCK.json').read_text())
            self.assertEqual('OWNED ADAPTER MUST SURVIVE', adapter.read_text())
            self.assertNotIn('using-agent-skills', [m['skill'] for m in current['mappings']])
            for item in current['mappings']:
                self.assertTrue((project / 'skills' / item['skill'] / 'SKILL.md').is_file(), item)
            for name in ('hallmark', 'ui-ux-pro-max', 'appllama-app-design-skill', 'diagram-design'):
                self.assertTrue((project / 'skills' / name / 'references/proof.txt').is_file())
            self.assertTrue((project / 'skills/humanizer/scripts/proof.txt').is_file())
            self.assertIn('name: design-taste-frontend', (project / 'skills/design-taste-frontend/SKILL.md').read_text())
            self.assertEqual('shared checklist', (project / 'references/fixture-check.md').read_text())

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
