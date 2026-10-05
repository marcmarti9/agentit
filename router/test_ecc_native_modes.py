"""Regression: Yarn adds exec bits only to declared package binaries."""
import os
from pathlib import Path
import shutil
import tempfile
import unittest
from router import ecc

ROOT = Path(__file__).resolve().parents[1]

@unittest.skipIf(os.name == 'nt', 'POSIX executable-mode boundary')
class ECCNativeInstallModesTests(unittest.TestCase):
    def test_only_verified_declared_bin_can_gain_exec_after_install(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for rel in ('references/ecc-policy.json', 'vendor/ecc.lock.json',
                        'vendor/ecc/package.json', 'vendor/ecc/scripts/memory-mcp.mjs',
                        'vendor/ecc/agents/architect.md'):
                target = root / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / rel, target)
            binary = root / 'vendor/ecc/scripts/memory-mcp.mjs'
            expected = binary.read_bytes()
            binary.chmod(binary.stat().st_mode | 0o111)
            with self.assertRaisesRegex(ecc.ECCError, 'executable-mode mismatch'):
                ecc.verified_bytes(root, 'scripts/memory-mcp.mjs')
            (root / 'vendor/ecc/node_modules').mkdir()
            self.assertEqual(ecc.verified_bytes(root, 'scripts/memory-mcp.mjs'), expected)
            other = root / 'vendor/ecc/agents/architect.md'
            other.chmod(other.stat().st_mode | 0o111)
            with self.assertRaisesRegex(ecc.ECCError, 'executable-mode mismatch'):
                ecc.verified_bytes(root, 'agents/architect.md')
            binary.write_bytes(expected + b'// unauthorized edit\n')
            with self.assertRaisesRegex(ecc.ECCError, 'integrity mismatch'):
                ecc.verified_bytes(root, 'scripts/memory-mcp.mjs')

if __name__ == '__main__':
    unittest.main()
