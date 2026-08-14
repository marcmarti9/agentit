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
            receipt = Path(tmp) / "receipt.json"
            self.assertEqual(0, main(["loop-init", "--state", str(state), "--goal", "Do work", "--verifier", "pytest -q", "--stop", "tests pass"]))
            self.assertEqual(2, main(["loop-check", "--state", str(state)]))
            self.assertEqual(0, main(["loop-attempt", "--state", str(state), "--result", "pass", "--strategy", "implement", "--evidence", "1 passed", "--exit-code", "0"]))
            self.assertEqual(0, main(["loop-check", "--state", str(state), "--receipt", str(receipt)]))
            persisted = json.loads(state.read_text(encoding="utf-8"))
            saved_receipt = json.loads(receipt.read_text(encoding="utf-8"))
            self.assertEqual("passed", persisted["status"])
            self.assertEqual(persisted["contract_sha256"], saved_receipt["contract_sha256"])

    def test_graph_cli_binds_nodes_to_loop_states_and_advances(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            spec = root / "graph-spec.json"
            graph = root / "graph.json"
            research_loop = root / "research-loop.json"
            implement_loop = root / "implement-loop.json"
            research_receipt = root / "research-receipt.json"

            self.assertEqual(0, main(["loop-init", "--state", str(research_loop), "--goal", "Research", "--verifier", "evidence review", "--stop", "evidence exists"]))
            self.assertEqual(0, main(["loop-init", "--state", str(implement_loop), "--goal", "Implement", "--verifier", "pytest -q", "--stop", "tests pass"]))
            spec.write_text(
                json.dumps({
                    "nodes": [
                        {"id": "research", "loop_state": "research-loop.json"},
                        {"id": "implement", "deps": ["research"], "loop_state": "implement-loop.json"},
                    ]
                }),
                encoding="utf-8",
            )
            self.assertEqual(0, main(["graph-init", "--state", str(graph), "--spec", str(spec)]))
            self.assertEqual(0, main(["loop-attempt", "--state", str(research_loop), "--result", "pass", "--strategy", "read sources", "--evidence", "sourced synthesis complete"]))
            self.assertEqual(0, main(["loop-check", "--state", str(research_loop), "--receipt", str(research_receipt)]))
            self.assertEqual(0, main(["graph-complete", "--state", str(graph), "--node", "research", "--loop-receipt", str(research_receipt)]))
            graph_state = json.loads(graph.read_text(encoding="utf-8"))
            self.assertEqual("completed", graph_state["node_states"]["research"]["status"])
            self.assertEqual("pending", graph_state["node_states"]["implement"]["status"])

    def test_graph_cli_rejects_receipt_for_wrong_node(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            spec = root / "graph-spec.json"
            graph = root / "graph.json"
            a_loop = root / "a-loop.json"
            b_loop = root / "b-loop.json"
            a_receipt = root / "a-receipt.json"
            self.assertEqual(0, main(["loop-init", "--state", str(a_loop), "--goal", "A", "--verifier", "check a", "--stop", "a good"]))
            self.assertEqual(0, main(["loop-init", "--state", str(b_loop), "--goal", "B", "--verifier", "check b", "--stop", "b good"]))
            spec.write_text(json.dumps({"nodes": [{"id": "a", "loop_state": "a-loop.json"}, {"id": "b", "loop_state": "b-loop.json"}]}), encoding="utf-8")
            self.assertEqual(0, main(["graph-init", "--state", str(graph), "--spec", str(spec)]))
            self.assertEqual(0, main(["loop-attempt", "--state", str(a_loop), "--result", "pass", "--strategy", "do a", "--evidence", "a passed"]))
            self.assertEqual(0, main(["loop-check", "--state", str(a_loop), "--receipt", str(a_receipt)]))
            self.assertEqual(2, main(["graph-complete", "--state", str(graph), "--node", "b", "--loop-receipt", str(a_receipt)]))


if __name__ == "__main__":
    unittest.main()
