"""Runtime-enforced DAG orchestration for Agentit Graph Engineering.

The router may recommend a topology, but this module validates and advances the
actual execution graph. Dependencies cannot be skipped, cycles are rejected,
write ownership is exclusive, and a node can complete only with a passed Loop
Engineering receipt.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Mapping, Sequence

try:
    from router.loop_runtime import LoopRuntimeError, validate_loop_receipt
except ImportError:
    from loop_runtime import LoopRuntimeError, validate_loop_receipt  # type: ignore


class GraphRuntimeError(RuntimeError):
    pass


_NODE_ID = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._-]*$")


def _hash(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _clean_id(value: Any) -> str:
    node_id = str(value or "").strip()
    if not _NODE_ID.fullmatch(node_id):
        raise GraphRuntimeError(f"invalid node id: {node_id!r}")
    return node_id


def _clean_path(value: Any) -> str:
    text = str(value or "").strip().replace("\\", "/")
    if not text:
        raise GraphRuntimeError("write path cannot be empty")
    path = PurePosixPath(text)
    if path.is_absolute() or ".." in path.parts:
        raise GraphRuntimeError(f"unsafe write path: {text}")
    return path.as_posix()


def _paths_overlap(left: str, right: str) -> bool:
    a = PurePosixPath(left)
    b = PurePosixPath(right)
    return a == b or a in b.parents or b in a.parents


def _normalize_nodes(nodes: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for raw in nodes:
        if not isinstance(raw, Mapping):
            raise GraphRuntimeError("graph nodes must be objects")
        node_id = _clean_id(raw.get("id"))
        if node_id in seen:
            raise GraphRuntimeError(f"duplicate node id: {node_id}")
        seen.add(node_id)
        deps: list[str] = []
        for dep in raw.get("deps") or []:
            dep_id = _clean_id(dep)
            if dep_id not in deps:
                deps.append(dep_id)
        write_paths: list[str] = []
        for path in raw.get("write_paths") or []:
            clean = _clean_path(path)
            if clean not in write_paths:
                write_paths.append(clean)
        expected_artifacts = [str(item).strip() for item in raw.get("expected_artifacts") or [] if str(item).strip()]
        result.append({
            "id": node_id,
            "deps": deps,
            "write_paths": write_paths,
            "expected_artifacts": expected_artifacts,
            "objective": str(raw.get("objective") or "").strip(),
        })
    if not result:
        raise GraphRuntimeError("graph must contain at least one node")
    return result


def _validate_dependencies(nodes: Sequence[Mapping[str, Any]]) -> None:
    ids = {str(node["id"]) for node in nodes}
    for node in nodes:
        for dep in node["deps"]:
            if dep not in ids:
                raise GraphRuntimeError(f"node {node['id']} depends on unknown node {dep}")
            if dep == node["id"]:
                raise GraphRuntimeError(f"node {node['id']} cannot depend on itself")

    by_id = {str(node["id"]): node for node in nodes}
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node_id: str) -> None:
        if node_id in visiting:
            raise GraphRuntimeError(f"cycle detected at node {node_id}")
        if node_id in visited:
            return
        visiting.add(node_id)
        for dep in by_id[node_id]["deps"]:
            visit(dep)
        visiting.remove(node_id)
        visited.add(node_id)

    for node_id in by_id:
        visit(node_id)


def _validate_write_ownership(nodes: Sequence[Mapping[str, Any]]) -> None:
    claims: list[tuple[str, str]] = []
    for node in nodes:
        for path in node["write_paths"]:
            for owner, claimed in claims:
                if _paths_overlap(path, claimed):
                    raise GraphRuntimeError(
                        f"write ownership overlap: {node['id']}:{path} conflicts with {owner}:{claimed}"
                    )
            claims.append((str(node["id"]), str(path)))


def new_graph(nodes: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    normalized = _normalize_nodes(nodes)
    _validate_dependencies(normalized)
    _validate_write_ownership(normalized)
    contract = {"nodes": normalized}
    states = {
        node["id"]: {
            "status": "pending",
            "loop_receipt": None,
            "artifacts": [],
        }
        for node in normalized
    }
    graph = {
        "schema_version": 1,
        "kind": "agentit.graph",
        "contract": contract,
        "contract_sha256": _hash(contract),
        "status": "running",
        "node_states": states,
    }
    validate_graph(graph)
    return graph


def validate_graph(graph: Mapping[str, Any]) -> None:
    if graph.get("schema_version") != 1 or graph.get("kind") != "agentit.graph":
        raise GraphRuntimeError("invalid graph schema")
    contract = graph.get("contract")
    if not isinstance(contract, Mapping):
        raise GraphRuntimeError("graph contract must be an object")
    nodes = _normalize_nodes(contract.get("nodes") or [])
    _validate_dependencies(nodes)
    _validate_write_ownership(nodes)
    if graph.get("contract_sha256") != _hash({"nodes": nodes}):
        raise GraphRuntimeError("graph contract hash mismatch")
    states = graph.get("node_states")
    if not isinstance(states, Mapping):
        raise GraphRuntimeError("node_states must be an object")
    ids = {node["id"] for node in nodes}
    if set(states) != ids:
        raise GraphRuntimeError("node state ids do not match graph contract")
    completed = 0
    blocked = False
    for node_id, state in states.items():
        if not isinstance(state, Mapping) or state.get("status") not in {"pending", "completed", "blocked"}:
            raise GraphRuntimeError(f"invalid state for node {node_id}")
        if state.get("status") == "completed":
            receipt = state.get("loop_receipt")
            if not isinstance(receipt, Mapping):
                raise GraphRuntimeError(f"completed node {node_id} is missing loop receipt")
            try:
                validate_loop_receipt(receipt, require_passed=True)
            except LoopRuntimeError as exc:
                raise GraphRuntimeError(f"node {node_id} has invalid loop receipt: {exc}") from exc
            completed += 1
        if state.get("status") == "blocked":
            blocked = True
    status = graph.get("status")
    expected = "blocked" if blocked else ("passed" if completed == len(nodes) else "running")
    if status != expected:
        raise GraphRuntimeError(f"graph status mismatch: expected {expected}, got {status}")


def ready_nodes(graph: Mapping[str, Any]) -> list[str]:
    validate_graph(graph)
    if graph.get("status") != "running":
        return []
    nodes = {node["id"]: node for node in graph["contract"]["nodes"]}
    states = graph["node_states"]
    ready: list[str] = []
    for node_id, node in nodes.items():
        if states[node_id]["status"] != "pending":
            continue
        if all(states[dep]["status"] == "completed" for dep in node["deps"]):
            ready.append(node_id)
    return ready


def complete_node(
    graph: Mapping[str, Any],
    *,
    node_id: str,
    loop_receipt: Mapping[str, Any],
    artifacts: Sequence[str] = (),
) -> dict[str, Any]:
    validate_graph(graph)
    node_id = _clean_id(node_id)
    if graph.get("status") != "running":
        raise GraphRuntimeError(f"cannot complete node in terminal graph: {graph.get('status')}")
    nodes = {node["id"]: node for node in graph["contract"]["nodes"]}
    if node_id not in nodes:
        raise GraphRuntimeError(f"unknown node: {node_id}")
    if node_id not in ready_nodes(graph):
        raise GraphRuntimeError(f"node is not ready: {node_id}")
    try:
        validate_loop_receipt(loop_receipt, require_passed=True)
    except LoopRuntimeError as exc:
        raise GraphRuntimeError(f"node cannot complete without passed loop receipt: {exc}") from exc
    clean_artifacts = [str(item).strip() for item in artifacts if str(item).strip()]
    expected = set(nodes[node_id]["expected_artifacts"])
    if expected and not expected.issubset(clean_artifacts):
        missing = sorted(expected.difference(clean_artifacts))
        raise GraphRuntimeError(f"node {node_id} missing expected artifacts: {', '.join(missing)}")
    result = copy.deepcopy(dict(graph))
    result["node_states"][node_id] = {
        "status": "completed",
        "loop_receipt": copy.deepcopy(dict(loop_receipt)),
        "artifacts": clean_artifacts,
    }
    if all(state["status"] == "completed" for state in result["node_states"].values()):
        result["status"] = "passed"
    validate_graph(result)
    return result


def block_node(graph: Mapping[str, Any], *, node_id: str, reason: str) -> dict[str, Any]:
    validate_graph(graph)
    node_id = _clean_id(node_id)
    if node_id not in graph["node_states"]:
        raise GraphRuntimeError(f"unknown node: {node_id}")
    if graph["node_states"][node_id]["status"] != "pending":
        raise GraphRuntimeError(f"node is not pending: {node_id}")
    text = str(reason or "").strip()
    if not text:
        raise GraphRuntimeError("block reason is required")
    result = copy.deepcopy(dict(graph))
    result["node_states"][node_id] = {
        "status": "blocked",
        "loop_receipt": None,
        "artifacts": [],
        "reason": text,
    }
    result["status"] = "blocked"
    validate_graph(result)
    return result


def graph_receipt(graph: Mapping[str, Any]) -> dict[str, Any]:
    validate_graph(graph)
    receipt = {
        "schema_version": 1,
        "kind": "agentit.graph.receipt",
        "contract_sha256": graph["contract_sha256"],
        "status": graph["status"],
        "nodes": {
            node_id: {
                "status": state["status"],
                "loop_receipt_sha256": (state.get("loop_receipt") or {}).get("receipt_sha256"),
                "artifacts": list(state.get("artifacts") or []),
            }
            for node_id, state in graph["node_states"].items()
        },
    }
    receipt["receipt_sha256"] = _hash(receipt)
    return receipt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Agentit Graph Engineering DAG runtime")
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init")
    init.add_argument("--spec", type=Path, required=True, help="JSON file containing a nodes array")
    ready = sub.add_parser("ready")
    ready.add_argument("--state", type=Path, required=True)
    check = sub.add_parser("check")
    check.add_argument("--state", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            spec = json.loads(args.spec.read_text(encoding="utf-8"))
            output: Any = new_graph(spec.get("nodes") or [])
        else:
            state = json.loads(args.state.read_text(encoding="utf-8"))
            if args.command == "ready":
                output = {"ready": ready_nodes(state)}
            else:
                validate_graph(state)
                output = {"valid": True, "receipt": graph_receipt(state)}
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return 0
    except (GraphRuntimeError, OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
