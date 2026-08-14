"""Persistent CLI for Agentit's Loop and Graph Engineering runtimes."""

from __future__ import annotations

import argparse
import copy
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any

try:
    from router.graph_runtime import (
        GraphRuntimeError,
        block_node,
        complete_node,
        graph_receipt,
        new_graph,
        ready_nodes,
        validate_graph,
    )
    from router.loop_runtime import (
        LoopRuntimeError,
        loop_receipt,
        new_loop,
        record_attempt,
        validate_loop,
        validate_loop_receipt,
    )
except ImportError:
    from graph_runtime import (  # type: ignore
        GraphRuntimeError,
        block_node,
        complete_node,
        graph_receipt,
        new_graph,
        ready_nodes,
        validate_graph,
    )
    from loop_runtime import (  # type: ignore
        LoopRuntimeError,
        loop_receipt,
        new_loop,
        record_attempt,
        validate_loop,
        validate_loop_receipt,
    )


class RuntimeCLIError(RuntimeError):
    pass


def _load(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise RuntimeCLIError(f"state must be a JSON object: {path}")
    return data


def _write_atomic(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(encoded)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, path)
    except Exception:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


def _print(payload: Any) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def _bind_graph_nodes(spec_path: Path, spec: dict[str, Any]) -> list[dict[str, Any]]:
    raw_nodes = spec.get("nodes") or []
    if not isinstance(raw_nodes, list):
        raise RuntimeCLIError("graph spec nodes must be a list")
    bound: list[dict[str, Any]] = []
    for raw in raw_nodes:
        if not isinstance(raw, dict):
            raise RuntimeCLIError("graph nodes must be objects")
        node = copy.deepcopy(raw)
        if node.get("loop_contract_sha256"):
            bound.append(node)
            continue
        loop_state = str(node.pop("loop_state", "") or "").strip()
        if not loop_state:
            raise RuntimeCLIError(f"graph node {node.get('id')} requires loop_state or loop_contract_sha256")
        loop_path = Path(loop_state)
        if not loop_path.is_absolute():
            loop_path = (spec_path.parent / loop_path).resolve()
        loop = _load(loop_path)
        validate_loop(loop)
        node["loop_contract_sha256"] = loop["contract_sha256"]
        bound.append(node)
    return bound


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Persistent Agentit Loop/Graph runtime")
    sub = parser.add_subparsers(dest="command", required=True)

    loop_init = sub.add_parser("loop-init")
    loop_init.add_argument("--state", type=Path, required=True)
    loop_init.add_argument("--goal", required=True)
    loop_init.add_argument("--verifier", required=True)
    loop_init.add_argument("--stop", required=True)
    loop_init.add_argument("--max-attempts", type=int, default=2)

    loop_attempt = sub.add_parser("loop-attempt")
    loop_attempt.add_argument("--state", type=Path, required=True)
    loop_attempt.add_argument("--result", choices=("pass", "fail"), required=True)
    loop_attempt.add_argument("--strategy", required=True)
    loop_attempt.add_argument("--evidence", required=True)
    loop_attempt.add_argument("--exit-code", type=int, default=None)
    loop_attempt.add_argument("--artifact", action="append", default=[])

    loop_check = sub.add_parser("loop-check")
    loop_check.add_argument("--state", type=Path, required=True)
    loop_check.add_argument("--receipt", type=Path, default=None)

    graph_init = sub.add_parser("graph-init")
    graph_init.add_argument("--state", type=Path, required=True)
    graph_init.add_argument("--spec", type=Path, required=True)

    graph_ready = sub.add_parser("graph-ready")
    graph_ready.add_argument("--state", type=Path, required=True)

    graph_complete = sub.add_parser("graph-complete")
    graph_complete.add_argument("--state", type=Path, required=True)
    graph_complete.add_argument("--node", required=True)
    graph_complete.add_argument("--loop-receipt", type=Path, required=True)
    graph_complete.add_argument("--artifact", action="append", default=[])

    graph_block = sub.add_parser("graph-block")
    graph_block.add_argument("--state", type=Path, required=True)
    graph_block.add_argument("--node", required=True)
    graph_block.add_argument("--reason", required=True)

    graph_check = sub.add_parser("graph-check")
    graph_check.add_argument("--state", type=Path, required=True)
    graph_check.add_argument("--receipt", type=Path, default=None)

    args = parser.parse_args(argv)
    try:
        if args.command == "loop-init":
            state = new_loop(
                goal=args.goal,
                verifier=args.verifier,
                stop_condition=args.stop,
                max_attempts=args.max_attempts,
            )
            _write_atomic(args.state, state)
            _print({"status": state["status"], "contract_sha256": state["contract_sha256"], "state": str(args.state)})
            return 0

        if args.command == "loop-attempt":
            state = _load(args.state)
            state = record_attempt(
                state,
                passed=args.result == "pass",
                strategy=args.strategy,
                evidence=args.evidence,
                verifier_exit_code=args.exit_code,
                artifacts=args.artifact,
            )
            _write_atomic(args.state, state)
            _print({"status": state["status"], "receipt": loop_receipt(state)})
            return 0

        if args.command == "loop-check":
            state = _load(args.state)
            validate_loop(state)
            receipt = loop_receipt(state)
            validate_loop_receipt(receipt, require_passed=True)
            if args.receipt:
                _write_atomic(args.receipt, receipt)
            _print({"passed": True, "receipt": receipt})
            return 0

        if args.command == "graph-init":
            spec = _load(args.spec)
            nodes = _bind_graph_nodes(args.spec.resolve(), spec)
            state = new_graph(nodes)
            _write_atomic(args.state, state)
            _print({"status": state["status"], "ready": ready_nodes(state), "contract_sha256": state["contract_sha256"], "state": str(args.state)})
            return 0

        if args.command == "graph-ready":
            state = _load(args.state)
            _print({"status": state.get("status"), "ready": ready_nodes(state)})
            return 0

        if args.command == "graph-complete":
            state = _load(args.state)
            receipt = _load(args.loop_receipt)
            state = complete_node(state, node_id=args.node, loop_receipt=receipt, artifacts=args.artifact)
            _write_atomic(args.state, state)
            _print({"status": state["status"], "ready": ready_nodes(state), "receipt": graph_receipt(state)})
            return 0

        if args.command == "graph-block":
            state = _load(args.state)
            state = block_node(state, node_id=args.node, reason=args.reason)
            _write_atomic(args.state, state)
            _print({"status": state["status"], "receipt": graph_receipt(state)})
            return 0

        if args.command == "graph-check":
            state = _load(args.state)
            validate_graph(state)
            if state.get("status") != "passed":
                raise RuntimeCLIError(f"graph is not passed: {state.get('status')}")
            receipt = graph_receipt(state)
            if args.receipt:
                _write_atomic(args.receipt, receipt)
            _print({"passed": True, "receipt": receipt})
            return 0

        raise RuntimeCLIError(f"unsupported command: {args.command}")
    except (RuntimeCLIError, LoopRuntimeError, GraphRuntimeError, OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
