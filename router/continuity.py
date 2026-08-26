"""Long-horizon Agentit continuity with private local state by default.

Semantic task decisions belong to the active AI. This module only persists and
reads explicit state supplied by the caller.
"""

from __future__ import annotations

import json
import os
import re
import stat
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class ContinuityError(RuntimeError):
    """Raised when continuity state cannot be written or read safely."""


STATE_RELATIVE = Path(".agentit/STATE.md")
CHECKPOINT_DIR = Path(".agentit/checkpoints")

REQUIRED_SECTIONS = (
    "Goal",
    "Confirmed intent",
    "Execution decision",
    "Current status",
    "Decisions",
    "Important files and artifacts",
    "Verification",
    "Next actions",
    "Open questions / blockers",
    "Recovery",
)


def state_path(project_root: Path) -> Path:
    return Path(project_root) / STATE_RELATIVE


def _format_packs(value: Any) -> str:
    if value is None:
        return "(unset)"
    if isinstance(value, str):
        return value.strip() or "(unset)"
    if isinstance(value, (list, tuple)):
        items = [str(item).strip() for item in value if str(item).strip()]
        return ", ".join(items) if items else "(unset)"
    return str(value)


def default_state_markdown(
    *,
    goal: str = "",
    relevant_packs: Any = None,
    complexity: str | None = None,
    risk: str | None = None,
    topology: str | None = None,
    strong_review_required: bool | None = None,
    status: str = "not started",
    branch: str = "",
    extra: dict[str, Any] | None = None,
) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    strong_review = "(unset)" if strong_review_required is None else ("yes" if strong_review_required else "no")
    body = f"""# Agentit state

**Updated:** {now}
**Status:** {status}
**Branch:** {branch or "(unset)"}
**PR:** (unset)

## Goal
{goal or "(describe what is being built/changed and why)"}

## Confirmed intent
- Audience:
- Success criteria:
- Constraints:
- Non-goals:

## Execution decision
- Relevant packs: {_format_packs(relevant_packs)}
- Complexity: {complexity or "(unset)"}
- Risk: {risk or "(unset)"}
- Topology: {topology or "(unset)"}
- Selected skills/tools/references:
- Worker ownership:
- Strong independent review required: {strong_review}

## Current status
- Complete:
- In progress:
- Blocked:
- Not started:

## Decisions
- TASK_DECISION summary:
- Independent audit verdict:
- Strong reviewer verdict (when required):
- Stable product/technical/design decisions:

## Important files and artifacts
- Paths:
- Artifacts / receipts:
- MCP set (if relevant):

## Verification
- Commands:
- Latest results:
- Still needed:

## Next actions
1.

## Open questions / blockers
-

## Recovery
- Last checkpoint:
- Resume: read this file -> inspect branch/diff -> verify assumptions -> continue next action
- If scope/risk materially changed: rebuild TASK_DECISION with current context and run the required review before executing the changed plan.
"""
    if extra:
        body += "\n## Extra\n"
        for key, value in extra.items():
            body += f"- {key}: {value}\n"
    return body


def ensure_state_file(project_root: Path, *, goal: str = "", decision: dict[str, Any] | None = None, overwrite: bool = False) -> Path:
    """Create private local `.agentit/STATE.md` if missing."""
    root = Path(project_root).resolve()
    if not root.is_dir() or root.is_symlink():
        raise ContinuityError(f"project root must be a regular directory: {root}")
    path = state_path(root)
    if path.exists() and not overwrite:
        return path
    decision = decision or {}
    def optional_text(key: str) -> str | None:
        value = decision.get(key)
        return str(value) if value is not None else None
    strong_review_required = bool(decision["strong_review_required"]) if "strong_review_required" in decision else None
    content = default_state_markdown(
        goal=goal,
        relevant_packs=decision.get("relevant_packs"),
        complexity=optional_text("complexity"),
        risk=optional_text("risk"),
        topology=optional_text("topology"),
        strong_review_required=strong_review_required,
        status="in progress" if goal else "not started",
    )
    _atomic_write_text(path, content, private=True)
    return path


def parse_state(path: Path) -> dict[str, Any]:
    if not path.is_file() or path.is_symlink():
        raise ContinuityError(f"state file missing or symlink: {path}")
    text = path.read_text(encoding="utf-8")
    sections: dict[str, str] = {}
    current = "_preamble"
    chunks: list[str] = []
    for line in text.splitlines():
        if line.startswith("## "):
            sections[current] = "\n".join(chunks).strip()
            current = line[3:].strip()
            chunks = []
        else:
            chunks.append(line)
    sections[current] = "\n".join(chunks).strip()
    missing = [name for name in REQUIRED_SECTIONS if name not in sections]
    return {"path": str(path), "sections": sections, "missing_sections": missing, "complete": not missing, "raw_length": len(text)}


def resume_report(project_root: Path) -> dict[str, Any]:
    root = Path(project_root).resolve()
    path = state_path(root)
    if not path.is_file():
        return {"resumable": False, "reason": "no .agentit/STATE.md", "actions": ["create local state via agentit continuity init", "or inspect context + decide + review before substantial work"]}
    parsed = parse_state(path)
    return {
        "resumable": parsed["complete"],
        "path": str(path),
        "missing_sections": parsed["missing_sections"],
        "next_actions_preview": parsed["sections"].get("Next actions", "")[:500],
        "blockers_preview": parsed["sections"].get("Open questions / blockers", "")[:500],
        "protocol": ["read local Agentit state before re-interviewing", "inspect branch/PR/diff referenced in state", "verify assumptions still true", "repair stale local state", "rebuild and review TASK_DECISION if scope/risk materially changed", "continue from Next actions"],
    }


def write_checkpoint(project_root: Path, *, label: str, payload: dict[str, Any]) -> Path:
    root = Path(project_root).resolve()
    if not root.is_dir() or root.is_symlink():
        raise ContinuityError(f"project root must be a regular directory: {root}")
    directory = root / CHECKPOINT_DIR
    _ensure_private_directory(directory)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", label.strip().lower()).strip("-")[:40] or "checkpoint"
    destination = directory / f"{stamp}-{slug}.json"
    body = {"schema_version": 1, "created_at": datetime.now(timezone.utc).isoformat(), "label": label, "payload": payload}
    _atomic_write_text(destination, json.dumps(body, ensure_ascii=False, indent=2, sort_keys=True) + "\n", private=True)
    return destination


def list_checkpoints(project_root: Path, *, limit: int = 20) -> list[str]:
    directory = Path(project_root).resolve() / CHECKPOINT_DIR
    if not directory.is_dir():
        return []
    return [str(path) for path in sorted(directory.glob("*.json"), reverse=True)[:limit]]


def mid_task_decision_advice(decision: dict[str, Any] | None = None) -> list[str]:
    advice = ["If scope, risk, or independence changed mid-task, rebuild TASK_DECISION from current context.", "Run the required independent review again before executing a materially changed plan.", "Update local .agentit/STATE.md before a handoff or context limit when recovery matters."]
    if decision and decision.get("strong_review_required"):
        advice.append("The current decision requires a strong independent critic/judgment review.")
    if decision and decision.get("topology") in {"fan_out", "pipeline", "writer_reviewer"}:
        advice.append("Keep one writer per shared path/state unless isolation is explicit.")
    return advice


def _ensure_private_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    if path.is_symlink() or not path.is_dir():
        raise ContinuityError(f"continuity directory must be a regular directory: {path}")
    os.chmod(path, stat.S_IRWXU)
    parent = path.parent
    if parent.name == ".agentit" and parent.is_dir() and not parent.is_symlink():
        os.chmod(parent, stat.S_IRWXU)


def _atomic_write_text(path: Path, content: str, *, private: bool = False) -> None:
    parent = path.parent
    if private:
        _ensure_private_directory(parent)
    else:
        parent.mkdir(parents=True, exist_ok=True)
    if parent.is_symlink():
        raise ContinuityError(f"refusing symlinked continuity directory: {parent}")
    fd, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.tmp-", dir=parent, text=True)
    temporary_path = Path(temporary_name)
    try:
        os.fchmod(fd, stat.S_IRUSR | stat.S_IWUSR)
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_path, path)
        mode = stat.S_IRUSR | stat.S_IWUSR if private else stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH
        os.chmod(path, mode)
    finally:
        temporary_path.unlink(missing_ok=True)
