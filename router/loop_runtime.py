"""Runtime-enforced bounded execution loops for Agentit workers.

Loop Engineering enforces an explicit evidence contract. Legacy/manual evidence
is labelled reported, never confused with an executed command. Hashes detect
accidental mutation; they are not signatures or proof of model honesty.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from datetime import datetime, timezone
import os
import signal
import subprocess
import tempfile
import time
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
    verifier_argv: Sequence[str] | None = None,
    verifier_cwd: str | None = None,
    subject_paths: Sequence[str] = (),
) -> dict[str, Any]:
    if type(max_attempts) is not int or not 1 <= max_attempts <= 8:
        raise LoopRuntimeError("max_attempts must be an integer between 1 and 8")
    contract = {
        "goal": _text(goal, "goal"),
        "verifier": _text(verifier, "verifier"),
        "stop_condition": _text(stop_condition, "stop_condition"),
        "max_attempts": max_attempts,
        "escalation_condition": _text(escalation_condition, "escalation_condition"),
    }
    if verifier_argv is None and subject_paths:
        raise LoopRuntimeError("subject_paths require an executable verifier")
    contract["evidence_requirement"] = "command" if verifier_argv is not None else "reported"
    if verifier_argv is not None:
        _validate_command(verifier_argv, verifier_cwd, subject_paths)
        contract["verifier_argv"] = list(verifier_argv)
        contract["verifier_cwd"] = str(Path(verifier_cwd).resolve())
        contract["subject_paths"] = list(subject_paths)
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
    if type(max_attempts) is not int or not 1 <= max_attempts <= 8:
        raise LoopRuntimeError("invalid max_attempts")
    requirement = contract.get("evidence_requirement", "reported")
    if requirement not in {"reported", "command"}:
        raise LoopRuntimeError("invalid evidence requirement")
    if requirement == "command":
        _validate_command(contract.get("verifier_argv"), contract.get("verifier_cwd"), contract.get("subject_paths", []))
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
        if exit_code is not None and type(exit_code) is not int:
            raise LoopRuntimeError("verifier_exit_code must be an integer or null")
        if attempt.get("result") == "pass" and exit_code not in (None, 0):
            raise LoopRuntimeError("passing attempt cannot have a non-zero verifier exit code")
        if attempt.get("evidence_source", "reported") == "command":
            execution = attempt.get("execution")
            _validate_execution(execution, passed=attempt["result"] == "pass")
            if execution["argv"] != contract.get("verifier_argv") or execution["cwd"] != contract.get("verifier_cwd"):
                raise LoopRuntimeError("execution does not match the bound verifier")
            if execution["exit_code"] != exit_code:
                raise LoopRuntimeError("execution exit code mismatch")
        elif requirement == "command" and attempt.get("result") == "pass":
            raise LoopRuntimeError("command-evidence contract cannot pass on self-report")
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
    _execution: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    validate_loop(loop)
    if type(passed) is not bool:
        raise LoopRuntimeError("passed must be boolean")
    if passed and loop["contract"].get("evidence_requirement") == "command" and _execution is None:
        raise LoopRuntimeError("execute the bound verifier; self-report cannot satisfy this contract")
    if loop.get("status") in TERMINAL:
        raise LoopRuntimeError(f"cannot append attempt to terminal loop: {loop.get('status')}")
    result = copy.deepcopy(dict(loop))
    attempts = result["attempts"]
    max_attempts = result["contract"]["max_attempts"]
    if len(attempts) >= max_attempts:
        raise LoopRuntimeError("attempt budget exhausted")
    strategy_text = _text(strategy, "strategy")
    evidence_text = _text(evidence, "evidence")
    if verifier_exit_code is not None and type(verifier_exit_code) is not int:
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
        "evidence_source": "command" if _execution is not None else "reported",
    }
    if _execution is not None:
        attempt["execution"] = dict(_execution)
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
        "evidence_source": attempts[-1].get("evidence_source", "reported") if attempts else "none",
        "execution": attempts[-1].get("execution") if attempts else None,
        "evidence_requirement": loop["contract"].get("evidence_requirement", "reported"),
    }
    receipt["receipt_sha256"] = _hash(receipt)
    return receipt


def validate_loop_receipt(receipt: Mapping[str, Any], *, require_passed: bool = True, require_command: bool = False) -> None:
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
    if require_command or receipt.get("evidence_requirement") == "command":
        if receipt.get("evidence_source") != "command":
            raise LoopRuntimeError("executed command evidence required; this is reported evidence")
        _validate_execution(receipt.get("execution"), passed=receipt.get("status") == "passed")



def _validate_command(argv: Any, cwd: Any, subject_paths: Any) -> None:
    if not isinstance(argv, (list, tuple)) or not argv or any(not isinstance(a, str) or not a or "\x00" in a for a in argv):
        raise LoopRuntimeError("verifier_argv must be a non-empty string sequence, not shell text")
    if not isinstance(cwd, str) or not Path(cwd).is_absolute() or Path(cwd).is_symlink():
        raise LoopRuntimeError("verifier_cwd must be an explicit absolute directory")
    if not isinstance(subject_paths, (list, tuple)) or any(not isinstance(p, str) or not p or Path(p).is_absolute() or ".." in Path(p).parts for p in subject_paths):
        raise LoopRuntimeError("subject_paths must be explicit project-relative paths")


def _subject(contract: Mapping[str, Any]) -> str | None:
    paths = contract.get("subject_paths") or []
    if not paths:
        return None  # honest: command observed, but no source snapshot bound
    root = Path(contract["verifier_cwd"])
    files: dict[str, str] = {}
    for relative in paths:
        selected = root / relative
        for ancestor in (selected, *selected.parents):
            if ancestor == root:
                break
            if ancestor.is_symlink():
                raise LoopRuntimeError(f"symlink subject rejected: {ancestor}")
        if not selected.exists():
            raise LoopRuntimeError(f"subject path unavailable: {relative}")
        candidates = sorted(selected.rglob("*")) if selected.is_dir() else [selected]
        for path in candidates:
            rel = path.relative_to(root)
            if any(p in {".git", ".agentit", "__pycache__"} for p in rel.parts):
                continue
            if path.is_symlink():
                raise LoopRuntimeError(f"symlink subject rejected: {path}")
            if path.is_file():
                files[rel.as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return _hash(files)


def _validate_execution(execution: Any, *, passed: bool) -> None:
    if not isinstance(execution, dict):
        raise LoopRuntimeError("execution observation missing")
    for key in ("argv", "cwd", "started_at", "duration_seconds", "output_sha256", "exit_code", "timed_out"):
        if key not in execution:
            raise LoopRuntimeError(f"execution observation missing {key}")
    if type(execution["exit_code"]) is not int:
        raise LoopRuntimeError("invalid observed exit code")
    if passed and (execution["exit_code"] != 0 or execution["timed_out"]):
        raise LoopRuntimeError("failed/timed-out process cannot pass")
    if passed and execution.get("subject_before") != execution.get("subject_after"):
        raise LoopRuntimeError("subject changed during verifier execution")


def validate_current_subject(loop: Mapping[str, Any]) -> None:
    validate_loop(loop)
    if loop["contract"].get("evidence_requirement") == "command" and loop.get("status") == "passed":
        execution = loop["attempts"][-1].get("execution") or {}
        if execution.get("subject_after") != _subject(loop["contract"]):
            raise LoopRuntimeError("stale evidence: source changed since verification; start a fresh loop")


def run_verifier(loop: Mapping[str, Any], *, timeout: float = 300) -> dict[str, Any]:
    """Execute only contract-bound argv, shell=False. This is NOT a sandbox.

    The host must authorize the command and its capabilities. Output is streamed
    to a temporary file, hashed fully and excerpted to 64 KiB. POSIX timeouts kill
    the process group; other hosts must enforce their own child-process limits.
    """
    validate_loop(loop)
    contract = loop["contract"]
    if loop.get("status") in TERMINAL or contract.get("evidence_requirement") != "command":
        raise LoopRuntimeError("an open command-evidence loop is required")
    if isinstance(timeout, bool) or not isinstance(timeout, (int, float)) or not 0 < timeout <= 600:
        raise LoopRuntimeError("timeout must be between 0 and 600 seconds")
    cwd = Path(contract["verifier_cwd"])
    if not cwd.is_dir() or cwd.is_symlink():
        raise LoopRuntimeError("verifier directory is missing or a symlink")
    before = _subject(contract)
    started = datetime.now(timezone.utc).isoformat(); clock = time.monotonic()
    timed_out = False
    with tempfile.TemporaryFile() as output:
        try:
            process = subprocess.Popen(contract["verifier_argv"], cwd=cwd, stdin=subprocess.DEVNULL,
                                       stdout=output, stderr=subprocess.STDOUT, shell=False,
                                       start_new_session=(os.name == "posix"))
            try:
                exit_code = process.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                timed_out = True
                if os.name == "posix":
                    os.killpg(process.pid, signal.SIGKILL)
                else:
                    process.kill()
                process.wait(); exit_code = 124
        except OSError as exc:
            output.write(str(exc).encode("utf-8")); exit_code = 127
        output.seek(0); digest = hashlib.sha256()
        while chunk := output.read(65536):
            digest.update(chunk)
        size = output.tell(); output.seek(max(0, size - 65536))
        excerpt = output.read(65536).decode("utf-8", errors="replace")
    after = _subject(contract)
    execution = {"argv": contract["verifier_argv"], "cwd": str(cwd), "started_at": started,
                 "duration_seconds": time.monotonic()-clock, "exit_code": exit_code,
                 "timed_out": timed_out, "output_sha256": digest.hexdigest(), "output_bytes": size,
                 "output_excerpt": excerpt, "subject_before": before, "subject_after": after,
                 "sandbox_enforced": False}
    return record_attempt(loop, passed=(exit_code == 0 and not timed_out and before == after),
                          strategy="execute contract-bound verifier", evidence=json.dumps(execution, sort_keys=True),
                          verifier_exit_code=exit_code, _execution=execution)


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
