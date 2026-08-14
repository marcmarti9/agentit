from __future__ import annotations

import copy
import unittest

from graph_runtime import GraphRuntimeError, complete_node, new_graph, ready_nodes, validate_graph
from loop_runtime import loop_receipt, new_loop, record_attempt


class GraphRuntimeTests(unittest.TestCase):
    def _loop(self, node_id: str):
        loop = new_loop(goal=f"Complete {node_id}", verifier="pytest -q", stop_condition=f"{node_id} verified")
        passed = record_attempt(loop, passed=True, strategy=f"execute {node_id}", evidence=f"{node_id}: verifier passed", verifier_exit_code=0)
        return loop, loop_receipt(passed)

    def _node(self, node_id: str, *, deps=None, write_paths=None, expected_artifacts=None):
        loop, receipt = self._loop(node_id)
        return {
            "id": node_id,
            "deps": deps or [],
            "write_paths": write_paths or [],
            "expected_artifacts": expected_artifacts or [],
            "loop_contract_sha256": loop["contract_sha256"],
        }, receipt

    def test_fan_out_then_join_readiness(self):
        a, a_receipt = self._node("research-a")
        b, b_receipt = self._node("research-b")
        judge, _ = self._node("judge", deps=["research-a", "research-b"])
        graph = new_graph([a, b, judge])
        self.assertEqual(["research-a", "research-b"], ready_nodes(graph))
        graph = complete_node(graph, node_id="research-a", loop_receipt=a_receipt)
        self.assertEqual(["research-b"], ready_nodes(graph))
        graph = complete_node(graph, node_id="research-b", loop_receipt=b_receipt)
        self.assertEqual(["judge"], ready_nodes(graph))

    def test_cycle_is_rejected(self):
        a, _ = self._node("a", deps=["b"])
        b, _ = self._node("b", deps=["a"])
        with self.assertRaises(GraphRuntimeError):
            new_graph([a, b])

    def test_unknown_dependency_is_rejected(self):
        a, _ = self._node("a", deps=["missing"])
        with self.assertRaises(GraphRuntimeError):
            new_graph([a])

    def test_overlapping_write_ownership_is_rejected(self):
        a, _ = self._node("writer-a", write_paths=["src"])
        b, _ = self._node("writer-b", write_paths=["src/page.tsx"])
        with self.assertRaises(GraphRuntimeError):
            new_graph([a, b])

    def test_dependency_cannot_be_skipped(self):
        research, _ = self._node("research")
        implement, implement_receipt = self._node("implement", deps=["research"])
        graph = new_graph([research, implement])
        with self.assertRaises(GraphRuntimeError):
            complete_node(graph, node_id="implement", loop_receipt=implement_receipt)

    def test_expected_artifact_is_required(self):
        direction, receipt = self._node("direction", expected_artifacts=["DESIGN_DIRECTION.md"])
        graph = new_graph([direction])
        with self.assertRaises(GraphRuntimeError):
            complete_node(graph, node_id="direction", loop_receipt=receipt, artifacts=[])
        graph = complete_node(graph, node_id="direction", loop_receipt=receipt, artifacts=["DESIGN_DIRECTION.md"])
        self.assertEqual("passed", graph["status"])

    def test_receipt_from_another_node_cannot_complete_target(self):
        a, a_receipt = self._node("a")
        b, _ = self._node("b")
        graph = new_graph([a, b])
        with self.assertRaises(GraphRuntimeError):
            complete_node(graph, node_id="b", loop_receipt=a_receipt)

    def test_manually_completed_node_with_pending_dependency_is_rejected(self):
        research, _ = self._node("research")
        implement, implement_receipt = self._node("implement", deps=["research"])
        graph = new_graph([research, implement])
        tampered = copy.deepcopy(graph)
        tampered["node_states"]["implement"] = {
            "status": "completed",
            "loop_receipt": implement_receipt,
            "artifacts": [],
        }
        with self.assertRaises(GraphRuntimeError):
            validate_graph(tampered)


if __name__ == "__main__":
    unittest.main()
