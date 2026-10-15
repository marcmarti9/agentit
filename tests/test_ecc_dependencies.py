from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from router.ecc import ECCError, verified_bytes
from router.bootstrap import build_install_plan
from scripts.install_ecc_dependencies import ROOT, install_invocation, restore_manifest


class NativeDependencySourceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.manifest = self.root / 'vendor/ecc/package.json'
        self.manifest.parent.mkdir(parents=True)
        self.original = b'{"scripts":{"welcome":"echo It\\u00f4"},"enabled":true,"bin":{"native":"tool.js"}}\n'
        self.manifest.write_bytes(self.original)
        other = self.root / 'vendor/ecc/tool.js'
        other.write_bytes(b'original tool\n')
        files = {}
        for path in (self.manifest, other):
            path.chmod(0o644)
            data = path.read_bytes()
            files[path.name] = {'sha256': hashlib.sha256(data).hexdigest(),
                                'bytes': len(data), 'executable': False}
        pin = {'schema_version': 1, 'repository': 'example/ecc', 'revision': 'a' * 40}
        (self.root / 'references').mkdir()
        (self.root / 'references/ecc-policy.json').write_text(json.dumps(pin))
        lock = dict(pin, files=files, skills={}, aliases={})
        (self.root / 'vendor/ecc.lock.json').write_text(json.dumps(lock))

    def test_yarn_unicode_formatting_restores_original_bytes(self):
        self.manifest.write_text(json.dumps(json.loads(self.original), ensure_ascii=False, indent=2))
        result = restore_manifest(self.root, self.original)
        self.assertTrue(result['format_only_restoration'])
        self.assertEqual(self.original, self.manifest.read_bytes())
        self.assertEqual(2, result['source']['verified_files'])

    def test_unchanged_manifest_remains_exact(self):
        self.assertFalse(restore_manifest(self.root, self.original)['format_only_restoration'])

    def test_semantic_type_or_command_changes_are_preserved_and_rejected(self):
        command = json.loads(self.original)
        command['scripts']['welcome'] = 'execute something else'
        scalar = json.loads(self.original)
        scalar['enabled'] = 1
        for changed in (json.dumps(command).encode(), json.dumps(scalar).encode()):
            with self.subTest(changed=changed):
                self.manifest.write_bytes(changed)
                with self.assertRaisesRegex(ECCError, 'semantics'):
                    restore_manifest(self.root, self.original)
                self.assertEqual(changed, self.manifest.read_bytes())

    def test_duplicate_keys_are_rejected(self):
        self.manifest.write_bytes(b'{"enabled":false,"enabled":true,"scripts":{"welcome":"echo It\\u00f4"}}')
        with self.assertRaisesRegex(ECCError, 'duplicate'):
            restore_manifest(self.root, self.original)

    def test_other_source_tampering_blocks_manifest_restoration(self):
        self.manifest.write_text(json.dumps(json.loads(self.original), ensure_ascii=False))
        observed = self.manifest.read_bytes()
        (self.root / 'vendor/ecc/tool.js').write_bytes(b'changed tool\n')
        with self.assertRaisesRegex(ECCError, 'integrity'):
            restore_manifest(self.root, self.original)
        self.assertEqual(observed, self.manifest.read_bytes())

    def test_declared_bin_mode_uses_authenticated_original_manifest(self):
        self.manifest.write_text(json.dumps(json.loads(self.original), ensure_ascii=False))
        (self.root / 'vendor/ecc/tool.js').chmod(0o755)
        result = restore_manifest(self.root, self.original)
        self.assertEqual(['tool.js'], result['source']['installed_declared_bin_modes'])
        self.assertEqual(self.original, self.manifest.read_bytes())

    def test_unpinned_manifest_cannot_authorize_executable_mode(self):
        (self.root / 'vendor/ecc/tool.js').chmod(0o755)
        with self.assertRaisesRegex(ECCError, 'manifest integrity'):
            verified_bytes(self.root, 'tool.js', package_manifest=b'{"bin":{"native":"tool.js"}}')

    def test_inherited_corepack_overrides_cannot_replace_pinned_manager(self):
        manager = 'yarn@4.9.2+sha512.' + 'a' * 128
        with patch.dict(os.environ, {'COREPACK_ENABLE_PROJECT_SPEC': '0',
                                    'COREPACK_ENABLE_STRICT': '0',
                                    'COREPACK_ENV_FILE': '/tmp/override.env',
                                    'COREPACK_INTEGRITY_KEYS': '0',
                                    'YARN_ENABLE_SCRIPTS': 'true'}):
            command, env = install_invocation(manager)
        self.assertEqual(['corepack', manager, 'install', '--immutable', '--mode=skip-build'], command)
        self.assertEqual('1', env['COREPACK_ENABLE_PROJECT_SPEC'])
        self.assertEqual('1', env['COREPACK_ENABLE_STRICT'])
        self.assertEqual('0', env['COREPACK_ENV_FILE'])
        self.assertEqual('false', env['YARN_ENABLE_SCRIPTS'])
        self.assertNotIn('COREPACK_INTEGRITY_KEYS', env)

    def test_unpinned_or_incomplete_manager_is_rejected(self):
        for manager in ('yarn', 'yarn@4.9.2', 'yarn@4.9.2+sha512.abcd', None):
            with self.subTest(manager=manager), self.assertRaises(ECCError):
                install_invocation(manager)

    def test_portable_runtime_includes_native_installer(self):
        (self.root / 'home').mkdir()
        plan = build_install_plan(home=self.root / 'home', source_root=ROOT, provider='codex')
        destination = str(self.root / 'home/.agentit/runtime/scripts/install_ecc_dependencies.py')
        self.assertIn(destination, {item['destination'] for item in plan['operations']})


if __name__ == '__main__':
    unittest.main()
