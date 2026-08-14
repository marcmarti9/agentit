"""Runtime-enforced bounded execution loops for Agentit workers.

Loop Engineering is a state machine, not a prompting convention. A loop cannot
claim success without a verifier result and evidence, retries are bounded, and
terminal receipts are auditable.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence


class LoopRuntimeError(RuntimeError):
    pass


TERMINAL = {"passed", "escalated"}


def _text(value: Any, name: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise LoopRuntimeError(f"{name} is required")
    return text


def _hash(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def new_loop(
    *,
    goal: str,
    verifier: str,
    stop_condition: str,
    max_attempts: int = 2,
    escalation_condition: str = "attempt budget exhausted or a material decision requires the parent/user",
) -> dict[str, Any]:
    if not isinstance(max_attempts, int) or not 1 <= max_attempts <= 8:
        raise LoopRuntimeError("max_attempts must be an integer between 1 and 8")
    contract = {
        "goal": _text(goal, "goal"),
        "verifier": _text(verifier, "verifier"),
        "stop_condition": _text(stop_condition, "stop_condition"),
        "max_attempts": max_attempts,
        "escalation_condition": _text(escalation_condition, "escalation_condition"),
    }
    return {
        "schema_version": 1,
        "kind": "agentit.loop",
        "contract": contract,
        "contract_sha256": _hash(contract),
        "status": "ready",
        "attempts": [],
    }


def validate_loop(loop: Mapping[str, Any]) -> None:
    if loop.get("schema_version") != 1 or loop.get("kind") != "agentit.loop":
        raise LoopRuntimeError("invalid loop schema")
    contract = loop.get("contract")
    if not isinstance(contract, dict):
        raise LoopRuntimeError("loop contract must be an object")
    for key in ("goal", "verifier", "stop_condition", "escalation_condition"):
        _text(contract.get(key), key)
    max_attempts = contract.get("max_attempts")
    if not isinstance(max_attempts, int) or not 1 <= max_attempts <= 8:
        raise LoopRuntimeError("invalid max_attempts")
    if loop.get("contract_sha256") != _hash(contract):
        raise LoopRuntimeError("loop contract hash mismatch")
    attempts = loop.get("attempts")
    if not isinstance(attempts, list) or len(attempts) > max_attempts:
        raise LoopRuntimeError("invalid attempt history")
    for index, attempt in enumerate(attempts, start=1):
        if not isinstance(attempt, dict) or attempt.get("attempt") != index:
            raise LoopRuntimeError("attempt history is not sequential")
        if attempt.get("result") not in {"pass", "fail"}:
            raise LoopRuntimeError("attempt result must be pass or fail")
        _text(attempt.get("strategy"), "attempt strategy")
        _text(attempt.get("evidence"), "attempt evidence")
        if attempt.get("evidence_sha256") != _hash(attempt.get("evidence")):
            raise LoopRuntimeError("attempt evidence hash mismatch")
        exit_code = attempt.get("verifier_exit_code")
        if exit_code is not None and not isinstance(exit_code, int):
            raise LoopRuntimeError("verifier_exit_code must be an integer or null")
        if attempt.get("result") == "pass" and exit_code not in (None, 0):
            raise LoopRuntimeError("passing attempt cannot have a non-zero verifier exit code")
    status = loop.get("status")
    if status not in {"ready", "retryable", "passed", "escalated"}:
        raise LoopRuntimeError("invalid loop status")
    if status == "passed" and (not attempts or attempts[-1].get("result") != "pass"):
        raise LoopRuntimeError("passed loop must end with a passing attempt")
    if status == "escalated" and len(attempts) < max_attempts and not loop.get("escalation_reason"):
        raise LoopRuntimeError("early escalation requires a reason")


def record_attempt(
    loop: Mapping[str, Any],
    *,
    passed: bool,
    strategy: str,
    evidence: str,
    verifier_exit_code: int | None = None,
    artifacts: Sequence[str] = (),
) -> dict[str, Any]:
    validate_loop(loop)
    if loop.get("status") in TERMINAL:
        raise LoopRuntimeError(f"cannot append attempt to terminal loop: {loop.get('status')}")
    result = copy.deepcopy(dict(loop))
    attempts = result["attempts"]
    max_attempts = result["contract"]["max_attempts"]
    if len(attempts) >= max_attempts:
        raise LoopRuntimeError("attempt budget exhausted")
    strategy_text = _text(strategy, "strategy")
    evidence_text = _text(evidence, "evidence")
    if verifier_exit_code is not None and not isinstance(verifier_exit_code, int):
        raise LoopRuntimeError("verifier_exit_code must be an integer or null")
    if passed and verifier_exit_code not in (None, 0):
        raise LoopRuntimeError("cannot pass with a non-zero verifier exit code")
    clean_artifacts = [str(item).strip() for item in artifacts if str(item).strip()]
    attempt = {
        "attempt": len(attempts) + 1,
        "result": "pass" if passed else "fail",
        "strategy": strategy_text,
        "evidence": evidence_text,
        "evidence_sha256": _hash(evidence_text),
        "verifier_exit_code": verifier_exit_code,
        "artifacts": clean_artifacts,
    }
    if attempts:
        previous = attempts[-1]
        if previous.get("result") == "fail":
            same_strategy = previous.get("strategy") == strategy_text
            same_evidence = previous.get("evidence_sha256") == attempt["evidence_sha256"]
            if same_strategy and same_evidence:
                raise LoopRuntimeError("retry requires fresh evidence or an alternative strategy")
    attempts.append(attempt)
    if passed:
        result["status"] = "passed"
    elif len(attempts) >= max_attempts:
        result["status"] = "escalated"
        result["escalation_reason"] = "attempt budget exhausted"
    else:
        result["status"] = "retryable"
    validate_loop(result)
    return result


def escalate(loop: Mapping[str, Any], *, reason: str) -> dict[str, Any]:
    validate_loop(loop)
    if loop.get("status") in TERMINAL:
        raise LoopRuntimeError(f"cannot escalate terminal loop: {loop.get('status')}")
    result = copy.deepcopy(dict(loop))
    result["status"] = "escalated"
    result["escalation_reason"] = _text(reason, "escalation reason")
    validate_loop(result)
    return result


def loop_receipt(loop: Mapping[str, Any]) -> dict[str, Any]:
    validate_loop(loop)
    attempts = list(loop.get("attempts") or [])
    receipt = {
        "schema_version": 1,
        "kind": "agentit.loop.receipt",
        "contract_sha256": loop["contract_sha256"],
        "status": loop["status"],
        "attempts_used": len(attempts),
        "max_attempts": loop["contract"]["max_attempts"],
        "verifier": loop["contract"]["verifier"],
        "stop_condition": loop["contract"]["stop_condition"],
        "last_evidence_sha256": attempts[-1]["evidence_sha256"] if attempts else None,
        "artifacts": attempts[-1].get("artifacts", []) if attempts else [],
        "escalation_reason": loop.get("escalation_reason"),
    }
    receipt["receipt_sha256"] = _hash(receipt)
    return receipt


def validate_loop_receipt(receipt: Mapping[str, Any], *, require_passed: bool = True) -> None:
    if receipt.get("schema_version") != 1 or receipt.get("kind") != "agentit.loop.receipt":
        raise LoopRuntimeError("invalid loop receipt schema")
    unsigned = dict(receipt)
    expected = unsigned.pop("receipt_sha256", None)
    if not expected or expected != _hash(unsigned):
        raise LoopRuntimeError("loop receipt hash mismatch")
    if require_passed and receipt.get("status") != "passed":
        raise LoopRuntimeError(f"loop receipt is not passed: {receipt.get('status')}")
    if receipt.get("status") == "passed" and not receipt.get("last_evidence_sha256"):
        raise LoopRuntimeError("passed receipt must contain verifier evidence")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Agentit bounded Loop Engineering runtime")
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init")
    init.add_argument("--goal", required=True)
    init.add_argument("--verifier", required=True)
    init.add_argument("--stop", required=True)
    init.add_argument("--max-attempts", type=int, default=2)
    attempt = sub.add_parser("attempt")
    attempt.add_argument("--state", type=Path, required=True)
    attempt.add_argument("--result", choices=("pass", "fail"), required=True)
    attempt.add_argument("--strategy", required=True)
    attempt.add_argument("--evidence", required=True)
    attempt.add_argument("--exit-code", type=int, default=None)
    attempt.add_argument("--artifact", action="append", default=[])
    check = sub.add_parser("check")
    check.add_argument("--state", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            output = new_loop(goal=args.goal, verifier=args.verifier, stop_condition=args.stop, max_attempts=args.max_attempts)
        else:
            state = json.loads(args.state.read_text(encoding="utf-8"))
            if args.command == "attempt":
                output = record_attempt(state, passed=args.result == "pass", strategy=args.strategy, evidence=args.evidence, verifier_exit_code=args.exit_code, artifacts=args.artifact)
            else:
                validate_loop(state)
                output = {"valid": True, "receipt": loop_receipt(state)}
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return 0
    except (LoopRuntimeError, OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
