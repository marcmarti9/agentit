"""Long-horizon continuity: project STATE, checkpoints, resume protocol.

Chat is disposable. Meaningful work must resume from repository state. This
module persists mechanical state only; semantic task decisions belong to the AI.
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


STATE_RELATIVE = Path("docs/agentit/STATE.md")
CHECKPOINT_DIR = Path(".agentit/checkpoints")

REQUIRED_SECTIONS = (
    "Goal",
    "Confirmed intent",
    "Domain pack",
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


def default_state_markdown(
    *,
    goal: str = "",
    domain_pack: str | None = None,
    craft_depth: str | None = None,
    effort: str | None = None,
    topology: str | None = None,
    strong_review_required: bool | None = None,
    status: str = "not started",
    branch: str = "",
    extra: dict[str, Any] | None = None,
) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    pack = domain_pack or "(unset)"
    craft = craft_depth or "(unset)"
    effort_value = effort or "(unset)"
    topology_value = topology or "(unset)"
    if strong_review_required is None:
        strong_review = "(unset)"
    else:
        strong_review = "yes" if strong_review_required else "no"
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

## Domain pack
- Pack: {pack}
- Craft depth: {craft}
- Effort: {effort_value}
- Topology: {topology_value}
- Strong independent review required: {strong_review}

## Current status
- Complete:
- In progress:
- Blocked:
- Not started:

## Decisions
- TASK_DECISION summary:
- Economy reviewer verdict:
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
- Resume: read this file → inspect branch/diff → verify assumptions → continue next action
- If scope/risk materially changed: rebuild TASK_DECISION with current context and run the AI review again before executing the changed plan.
"""
    if extra:
        body += "\n## Extra\n"
        for key, value in extra.items():
            body += f"- {key}: {value}\n"
    return body


def ensure_state_file(
    project_root: Path,
    *,
    goal: str = "",
    decision: dict[str, Any] | None = None,
    overwrite: bool = False,
) -> Path:
    """Create STATE.md if missing (or overwrite when requested).

    `decision` is optional model-produced metadata supplied by the caller. This
    function stores it mechanically and never derives semantic fields from the
    natural-language goal. Missing semantic fields remain visibly unset rather
    than being replaced with invented routing defaults.
    """
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

    strong_review_required = (
        bool(decision["strong_review_required"])
        if "strong_review_required" in decision
        else None
    )
    content = default_state_markdown(
        goal=goal,
        domain_pack=optional_text("domain_pack"),
        craft_depth=optional_text("craft_depth"),
        effort=optional_text("effort"),
        topology=optional_text("topology"),
        strong_review_required=strong_review_required,
        status="in progress" if goal else "not started",
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    _atomic_write_text(path, content)
    return path


def parse_state(path: Path) -> dict[str, Any]:
    """Best-effort section parse of STATE.md."""
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
    return {
        "path": str(path),
        "sections": sections,
        "missing_sections": missing,
        "complete": not missing,
        "raw_length": len(text),
    }


def resume_report(project_root: Path) -> dict[str, Any]:
    """What a fresh agent should do before asking the user to repeat decisions."""
    root = Path(project_root).resolve()
    path = state_path(root)
    if not path.is_file():
        return {
            "resumable": False,
            "reason": "no STATE.md",
            "actions": [
                "create docs/agentit/STATE.md via agentit continuity init",
                "or inspect context + decide + review + persist before continuing substantial work",
            ],
        }
    parsed = parse_state(path)
    next_actions = parsed["sections"].get("Next actions", "")
    blockers = parsed["sections"].get("Open questions / blockers", "")
    return {
        "resumable": parsed["complete"],
        "path": str(path),
        "missing_sections": parsed["missing_sections"],
        "next_actions_preview": next_actions[:500],
        "blockers_preview": blockers[:500],
        "protocol": [
            "read STATE.md before re-interviewing",
            "inspect branch/PR/diff referenced in state",
            "verify assumptions still true",
            "repair stale state before new work",
            "rebuild and review TASK_DECISION if scope/risk materially changed",
            "continue from Next actions",
        ],
    }


def write_checkpoint(
    project_root: Path,
    *,
    label: str,
    payload: dict[str, Any],
) -> Path:
    """Write a JSON checkpoint under .agentit/checkpoints/ (gitignored-friendly)."""
    root = Path(project_root).resolve()
    if not root.is_dir() or root.is_symlink():
        raise ContinuityError(f"project root must be a regular directory: {root}")
    directory = root / CHECKPOINT_DIR
    directory.mkdir(parents=True, exist_ok=True)
    os.chmod(directory, stat.S_IRWXU)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", label.strip().lower()).strip("-")[:40] or "checkpoint"
    destination = directory / f"{stamp}-{slug}.json"
    body = {
        "schema_version": 1,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "label": label,
        "payload": payload,
    }
    _atomic_write_text(
        destination,
        json.dumps(body, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    )
    os.chmod(destination, stat.S_IRUSR | stat.S_IWUSR)
    return destination


def list_checkpoints(project_root: Path, *, limit: int = 20) -> list[str]:
    root = Path(project_root).resolve()
    directory = root / CHECKPOINT_DIR
    if not directory.is_dir():
        return []
    files = sorted(directory.glob("*.json"), reverse=True)
    return [str(path) for path in files[:limit]]


def mid_task_decision_advice(decision: dict[str, Any] | None = None) -> list[str]:
    advice = [
        "If scope, risk, or independence changed mid-task, rebuild TASK_DECISION from current context.",
        "Run the independent AI preflight again before executing a materially changed plan.",
        "Update STATE.md Next actions before any handoff or context limit.",
    ]
    if decision and decision.get("strong_review_required"):
        advice.append("The current decision requires a strong independent critic/judgment review.")
    if decision and decision.get("topology") in {"fan_out", "pipeline", "writer_reviewer"}:
        advice.append("Keep one writer per shared path/state unless isolation is explicit.")
    return advice


def _atomic_write_text(path: Path, content: str) -> None:
    parent = path.parent
    parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.tmp-", dir=parent, text=True
    )
    temporary_path = Path(temporary_name)
    try:
        os.fchmod(fd, stat.S_IRUSR | stat.S_IWUSR)
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_path, path)
        os.chmod(path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
    finally:
        temporary_path.unlink(missing_ok=True)
