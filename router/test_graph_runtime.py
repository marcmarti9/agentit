from __future__ import annotations

import unittest

from graph_runtime import GraphRuntimeError, complete_node, new_graph, ready_nodes
from loop_runtime import loop_receipt, new_loop, record_attempt


class GraphRuntimeTests(unittest.TestCase):
    def _passed_receipt(self):
        loop = new_loop(goal="Do bounded work", verifier="pytest -q", stop_condition="tests pass")
        loop = record_attempt(loop, passed=True, strategy="implement", evidence="1 passed", verifier_exit_code=0)
        return loop_receipt(loop)

    def test_fan_out_then_join_readiness(self):
        graph = new_graph([
            {"id": "research-a", "deps": []},
            {"id": "research-b", "deps": []},
            {"id": "judge", "deps": ["research-a", "research-b"]},
        ])
        self.assertEqual(["research-a", "research-b"], ready_nodes(graph))
        graph = complete_node(graph, node_id="research-a", loop_receipt=self._passed_receipt())
        self.assertEqual(["research-b"], ready_nodes(graph))
        graph = complete_node(graph, node_id="research-b", loop_receipt=self._passed_receipt())
        self.assertEqual(["judge"], ready_nodes(graph))

    def test_cycle_is_rejected(self):
        with self.assertRaises(GraphRuntimeError):
            new_graph([
                {"id": "a", "deps": ["b"]},
                {"id": "b", "deps": ["a"]},
            ])

    def test_unknown_dependency_is_rejected(self):
        with self.assertRaises(GraphRuntimeError):
            new_graph([{"id": "a", "deps": ["missing"]}])

    def test_overlapping_write_ownership_is_rejected(self):
        with self.assertRaises(GraphRuntimeError):
            new_graph([
                {"id": "writer-a", "write_paths": ["src"]},
                {"id": "writer-b", "write_paths": ["src/page.tsx"]},
            ])

    def test_dependency_cannot_be_skipped(self):
        graph = new_graph([
            {"id": "research"},
            {"id": "implement", "deps": ["research"]},
        ])
        with self.assertRaises(GraphRuntimeError):
            complete_node(graph, node_id="implement", loop_receipt=self._passed_receipt())

    def test_expected_artifact_is_required(self):
        graph = new_graph([{"id": "direction", "expected_artifacts": ["DESIGN_DIRECTION.md"]}])
        with self.assertRaises(GraphRuntimeError):
            complete_node(graph, node_id="direction", loop_receipt=self._passed_receipt(), artifacts=[])
        graph = complete_node(graph, node_id="direction", loop_receipt=self._passed_receipt(), artifacts=["DESIGN_DIRECTION.md"])
        self.assertEqual("passed", graph["status"])


if __name__ == "__main__":
    unittest.main()
