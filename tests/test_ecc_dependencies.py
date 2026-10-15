from __future__ import annotations
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from router.ecc import ECCError
from scripts.install_ecc_dependencies import restore_manifest


class NativeDependencySourceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.manifest = self.root / 'vendor/ecc/package.json'
        self.manifest.parent.mkdir(parents=True)
        self.original = b'{"scripts":{"welcome":"echo It\\u00f4"},"enabled":true}\n'
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
        for changed in (b'{"scripts":{"welcome":"execute something else"},"enabled":true}',
                        b'{"scripts":{"welcome":"echo It\\u00f4"},"enabled":1}'):
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


if __name__ == '__main__':
    unittest.main()
