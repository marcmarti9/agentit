"""Persist and summarize Agentit routing decisions for daily use.

Not a marketing benchmark tool: a local debug trail so you can see what the
router chose on real tasks and tighten heuristics over time.
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
from typing import Any

try:
    from router.route import RegistryError, route_task
except ImportError:  # pragma: no cover
    from route import RegistryError, route_task  # type: ignore


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
    registry_path: Path | None = None,
    home: Path | None = None,
    explicit_risk: str | None = None,
) -> dict[str, Any]:
    """Route a task and persist a JSON trace under `.agentit/traces/`."""
    root = Path(project_root).resolve()
    if not root.is_dir() or root.is_symlink():
        raise TraceError(f"project root must be a regular directory: {root}")

    result = route_task(
        prompt,
        explicit_risk=explicit_risk,
        registry_path=registry_path,
        home=home,
        project_root=root,
    )

    now = datetime.now(timezone.utc)
    digest = hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:10]
    stamp = now.strftime("%Y%m%dT%H%M%SZ")
    name = f"{stamp}-{digest}-{_slug(prompt)}.json"
    traces_dir = _assert_safe_path(root / ".agentit" / "traces", root=root)
    traces_dir.mkdir(parents=True, exist_ok=True)
    os.chmod(traces_dir, stat.S_IRWXU)
    destination = _assert_safe_path(traces_dir / name, root=root)

    payload = {
        "schema_version": 1,
        "created_at": now.isoformat(),
        "prompt": prompt,
        "project_root": str(root),
        "route": result,
        "summary": {
            "risk": result.get("risk"),
            "category": result.get("category"),
            "domain_pack": result.get("domain_pack"),
            "craft_depth": result.get("craft_depth"),
            "spend": result.get("spend"),
            "topology": result.get("topology"),
            "critic_required": result.get("critic_required"),
            "subagents": result.get("subagents"),
            "token_estimate": result.get("token_estimate"),
            "skills_available": result.get("skills_available"),
            "skills_recommended_missing": result.get("skills_recommended_missing"),
            "skill_budget": result.get("skill_budget"),
            "verification": result.get("verification"),
            "jit_profile_recommendations": result.get("jit_profile_recommendations"),
            "models": result.get("models"),
            "project_signals": {
                "size_class": (result.get("project_signals") or {}).get("size_class"),
                "stack_markers": (result.get("project_signals") or {}).get("stack_markers"),
            },
            "reasons": result.get("reasons"),
        },
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
        "summary": payload["summary"],
        "route": result,
    }


def format_trace_summary(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") or {}
    token = summary.get("token_estimate") or {}
    lines = [
        f"risk: {summary.get('risk')}",
        f"category: {summary.get('category')}",
        f"domain_pack: {summary.get('domain_pack')}",
        f"craft_depth: {summary.get('craft_depth')}",
        f"spend: {summary.get('spend')}",
        f"topology: {summary.get('topology')}",
        f"critic_required: {summary.get('critic_required')}",
        f"subagents: {summary.get('subagents')}",
        f"tokens: {token.get('display') or '(n/a)'}",
        f"skills: {', '.join(summary.get('skills_available') or []) or '(none)'}",
        f"missing: {', '.join(summary.get('skills_recommended_missing') or []) or '(none)'}",
        f"jit_profiles: {', '.join(summary.get('jit_profile_recommendations') or []) or '(none)'}",
    ]
    reasons = summary.get("reasons") or []
    if reasons:
        lines.append("reasons:")
        for reason in reasons:
            lines.append(f"  - {reason}")
    path = payload.get("path")
    if path:
        lines.append(f"trace: {path}")
    return "\n".join(lines)
