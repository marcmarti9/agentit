#!/usr/bin/env python3
"""Agentit LLM-native decision boundary.

This file intentionally does not classify natural language. The host LLM owns
semantic classification using the Agentit protocol; Python only emits the
contract and validates a structured decision against deterministic invariants.

`route_task()` remains as a compatibility name for callers that previously used
the deterministic router. It now returns a decision request with
`status=decision_required` and never fabricates risk/category/topology fields.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Iterable

try:
    from router.decision_contract import (
        DecisionContractError,
        build_decision_request,
        decision_protocol,
        validate_decision,
        validate_decision_file,
    )
    from router.registry import (
        AVAILABLE_REGISTRY_STATES,
        DEFAULT_REGISTRY_PATH,
        KNOWN_REGISTRY_STATES,
        RegistryError,
        load_registry,
        resolve_registry_path,
        resolve_requested_skills,
    )
except ImportError:  # pragma: no cover - direct script execution
    from decision_contract import (  # type: ignore
        DecisionContractError,
        build_decision_request,
        decision_protocol,
        validate_decision,
        validate_decision_file,
    )
    from registry import (  # type: ignore
        AVAILABLE_REGISTRY_STATES,
        DEFAULT_REGISTRY_PATH,
        KNOWN_REGISTRY_STATES,
        RegistryError,
        load_registry,
        resolve_registry_path,
        resolve_requested_skills,
    )


# Kept for import compatibility. No heuristic code consumes these values.
RISK_ORDER = {f"RISK_{level}": level for level in range(5)}
TOPOLOGIES = ("direct", "probe", "fan_out", "pipeline", "writer_reviewer", "audit")


def route_task(
    prompt: str,
    explicit_risk: str | None = None,
    *,
    registry_path: Path | None = None,
    home: Path | None = None,
    project_root: Path | None = None,
    provider_host: str = "local",
    available_providers: Iterable[str] | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Compatibility shim: return the contract the host LLM must decide.

    Despite the historical name, this function does not route or classify the
    prompt. Its output deliberately omits inferred semantic fields.
    """
    return build_decision_request(
        prompt,
        explicit_risk=explicit_risk,
        registry_path=registry_path,
        home=home,
        project_root=project_root,
        provider_host=provider_host,
        available_providers=available_providers,
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Emit Agentit's LLM decision contract or validate a host-model decision. "
            "No natural-language heuristics are run."
        )
    )
    parser.add_argument("task", nargs="*", help="Task text kept verbatim for the host model")
    parser.add_argument("--risk", dest="explicit_risk")
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY_PATH)
    parser.add_argument("--home", type=Path, default=Path.home())
    parser.add_argument("--project-root", type=Path)
    parser.add_argument("--host", default="local")
    parser.add_argument("--available", help="Comma-separated explicit provider inventory")
    parser.add_argument(
        "--decision",
        type=Path,
        help="JSON decision produced by the host LLM. When supplied, validate instead of emitting a request.",
    )
    parser.add_argument(
        "--protocol",
        action="store_true",
        help="Print only the stable decision protocol.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    available = (
        [item.strip() for item in args.available.split(",") if item.strip()]
        if args.available is not None
        else None
    )
    task = " ".join(args.task).strip()
    try:
        if args.protocol:
            payload = decision_protocol()
        elif args.decision is not None:
            payload = validate_decision_file(
                args.decision,
                explicit_risk=args.explicit_risk,
                registry_path=args.registry,
                home=args.home,
                provider_host=args.host,
                available_providers=available,
            )
        else:
            if not task:
                raise DecisionContractError("task is required unless --protocol or --decision is used")
            payload = route_task(
                task,
                explicit_risk=args.explicit_risk,
                registry_path=args.registry,
                home=args.home,
                project_root=args.project_root,
                provider_host=args.host,
                available_providers=available,
            )
    except (DecisionContractError, RegistryError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
