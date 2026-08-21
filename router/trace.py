"""Persist Agentit decision requests or validated host-model decisions.

Tracing is diagnostic only. It never classifies natural language itself.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

try:
    from router.decision_contract import build_decision_request, validate_decision
except ImportError:  # pragma: no cover
    from decision_contract import build_decision_request, validate_decision  # type: ignore


class TraceError(RuntimeError):
    """Raised when a trace cannot be written safely."""


def _assert_safe_path(path: Path, *, root: Path) -> Path:
    resolved = path.resolve()
    root_resolved = root.resolve()
    try:
        resolved.relative_to(root_resolved)
    except ValueError as exc:
        raise TraceError(f"path escapes project root: {path}") from exc
    for parent in [resolved, *resolved.parents]:
        if parent == root_resolved:
            break
        if parent.is_symlink():
            raise TraceError(f"symlink rejected in path: {parent}")
    return resolved


def _slug(text: str, *, max_len: int = 48) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower()).strip("-")
    return (cleaned or "task")[:max_len]


def write_trace(
    prompt: str,
    *,
    project_root: Path,
    decision: dict[str, Any] | None = None,
    registry_path: Path | None = None,
    home: Path | None = None,
    explicit_risk: str | None = None,
    provider_host: str = "local",
    available_providers: Iterable[str] | None = None,
) -> dict[str, Any]:
    """Persist a decision request or a validated decision under `.agentit/traces/`."""
    root = Path(project_root).resolve()
    if not root.is_dir() or root.is_symlink():
        raise TraceError(f"project root must be a regular directory: {root}")

    if decision is None:
        result = build_decision_request(
            prompt,
            explicit_risk=explicit_risk,
            registry_path=registry_path,
            home=home,
            project_root=root,
            provider_host=provider_host,
            available_providers=available_providers,
        )
        trace_kind = "decision_request"
        summary = {
            "status": result["status"],
            "classification_owner": result["classification_owner"],
            "task": result["task"],
            "project_size": (result.get("project_signals") or {}).get("size_class"),
        }
    else:
        result = validate_decision(
            decision,
            explicit_risk=explicit_risk,
            registry_path=registry_path,
            home=home,
            provider_host=provider_host,
            available_providers=available_providers,
        )
        trace_kind = "validated_decision"
        decided = result["decision"]
        summary = {
            "status": result["status"],
            "classification_owner": result["classification_owner"],
            "risk": decided["risk"],
            "category": decided["category"],
            "domain_pack": decided["domain_pack"],
            "topology": decided["topology"],
            "critic_required": decided["critic_required"],
            "skills_available": result["skill_inventory"]["available"],
            "skills_recommended_missing": result["skill_inventory"]["missing"],
            "capability_status": result["capability_envelope"].get("status"),
            "execution_ready": result["execution_ready"],
        }

    now = datetime.now(timezone.utc)
    digest = hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:10]
    stamp = now.strftime("%Y%m%dT%H%M%SZ")
    name = f"{stamp}-{digest}-{_slug(prompt)}.json"
    traces_dir = _assert_safe_path(root / ".agentit" / "traces", root=root)
    traces_dir.mkdir(parents=True, exist_ok=True)
    os.chmod(traces_dir, stat.S_IRWXU)
    destination = _assert_safe_path(traces_dir / name, root=root)

    payload = {
        "schema_version": 2,
        "created_at": now.isoformat(),
        "kind": trace_kind,
        "prompt": prompt,
        "project_root": str(root),
        "result": result,
        "summary": summary,
    }

    fd, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.tmp-", dir=traces_dir, text=True
    )
    temporary_path = Path(temporary_name)
    try:
        os.fchmod(fd, stat.S_IRUSR | stat.S_IWUSR)
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(payload, stream, ensure_ascii=False, indent=2, sort_keys=True)
            stream.write("\n")
        os.replace(temporary_path, destination)
        os.chmod(destination, stat.S_IRUSR | stat.S_IWUSR)
    finally:
        temporary_path.unlink(missing_ok=True)

    return {
        "path": str(destination),
        "kind": trace_kind,
        "summary": summary,
        "result": result,
    }


def format_trace_summary(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") or {}
    lines = [
        f"kind: {payload.get('kind')}",
        f"status: {summary.get('status')}",
        f"classification_owner: {summary.get('classification_owner')}",
    ]
    for field in (
        "risk",
        "category",
        "domain_pack",
        "topology",
        "critic_required",
        "execution_ready",
        "project_size",
    ):
        if field in summary:
            lines.append(f"{field}: {summary.get(field)}")
    if summary.get("skills_available") is not None:
        lines.append(f"skills: {', '.join(summary.get('skills_available') or []) or '(none)'}")
    if summary.get("skills_recommended_missing") is not None:
        lines.append(
            f"missing: {', '.join(summary.get('skills_recommended_missing') or []) or '(none)'}"
        )
    if summary.get("task"):
        lines.append(f"task: {summary['task']}")
    if payload.get("path"):
        lines.append(f"trace: {payload['path']}")
    return "\n".join(lines)
