from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from runtime_cli import main


class RuntimeCLITests(unittest.TestCase):
    def test_loop_cli_persists_and_requires_pass_for_check(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "loop.json"
            self.assertEqual(0, main(["loop-init", "--state", str(state), "--goal", "Do work", "--verifier", "pytest -q", "--stop", "tests pass"]))
            self.assertEqual(2, main(["loop-check", "--state", str(state)]))
            self.assertEqual(0, main(["loop-attempt", "--state", str(state), "--result", "pass", "--strategy", "implement", "--evidence", "1 passed", "--exit-code", "0"]))
            self.assertEqual(0, main(["loop-check", "--state", str(state)]))
            persisted = json.loads(state.read_text(encoding="utf-8"))
            self.assertEqual("passed", persisted["status"])

    def test_graph_cli_advances_only_after_loop_receipt(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            spec = root / "graph-spec.json"
            graph = root / "graph.json"
            loop = root / "loop.json"
            receipt_file = root / "receipt.json"
            spec.write_text(json.dumps({"nodes": [{"id": "research"}, {"id": "implement", "deps": ["research"]}]}), encoding="utf-8")
            self.assertEqual(0, main(["graph-init", "--state", str(graph), "--spec", str(spec)]))
            self.assertEqual(0, main(["loop-init", "--state", str(loop), "--goal", "Research", "--verifier", "evidence review", "--stop", "evidence exists"]))
            self.assertEqual(0, main(["loop-attempt", "--state", str(loop), "--result", "pass", "--strategy", "read sources", "--evidence", "sourced synthesis complete"]))
            loop_state = json.loads(loop.read_text(encoding="utf-8"))
            from loop_runtime import loop_receipt
            receipt_file.write_text(json.dumps(loop_receipt(loop_state)), encoding="utf-8")
            self.assertEqual(0, main(["graph-complete", "--state", str(graph), "--node", "research", "--loop-receipt", str(receipt_file)]))
            graph_state = json.loads(graph.read_text(encoding="utf-8"))
            self.assertEqual("completed", graph_state["node_states"]["research"]["status"])
            self.assertEqual("pending", graph_state["node_states"]["implement"]["status"])


if __name__ == "__main__":
    unittest.main()
