"""Long-horizon continuity: project STATE, checkpoints, resume protocol.

Chat is disposable. Meaningful work must resume from repository state.
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
    domain_pack: str = "engineering",
    craft_depth: str | None = None,
    spend: str = "normal",
    token_estimate: str = "",
    topology: str = "direct",
    critic_required: bool = False,
    status: str = "not started",
    branch: str = "",
    extra: dict[str, Any] | None = None,
) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    craft = craft_depth or "n/a (not design/visual)"
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
- Pack: {domain_pack}
- Craft depth: {craft}
- Spend: {spend}
- Token estimate: {token_estimate or "(from router, project-aware)"}
- Topology: {topology}
- Critic required: {"yes" if critic_required else "no"}

## Current status
- Complete:
- In progress:
- Blocked:
- Not started:

## Decisions
(stable product/technical/design decisions and why)

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
- Mid-task re-route: run `agentit trace "<current goal>" --project .` if scope changed
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
    route: dict[str, Any] | None = None,
    overwrite: bool = False,
) -> Path:
    """Create STATE.md if missing (or overwrite when requested)."""
    root = Path(project_root).resolve()
    if not root.is_dir() or root.is_symlink():
        raise ContinuityError(f"project root must be a regular directory: {root}")
    path = state_path(root)
    if path.exists() and not overwrite:
        return path
    route = route or {}
    content = default_state_markdown(
        goal=goal or str(route.get("reasons") or ""),
        domain_pack=str(route.get("domain_pack") or "engineering"),
        craft_depth=route.get("craft_depth"),
        spend=str(route.get("spend") or "normal"),
        token_estimate=(route.get("token_estimate") or {}).get("display", ""),
        topology=str(route.get("topology") or "direct"),
        critic_required=bool(route.get("critic_required")),
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
                "or run interview + persist before continuing product work",
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
    _atomic_write_text(destination, json.dumps(body, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    os.chmod(destination, stat.S_IRUSR | stat.S_IWUSR)
    return destination


def list_checkpoints(project_root: Path, *, limit: int = 20) -> list[str]:
    root = Path(project_root).resolve()
    directory = root / CHECKPOINT_DIR
    if not directory.is_dir():
        return []
    files = sorted(directory.glob("*.json"), reverse=True)
    return [str(path) for path in files[:limit]]


def mid_task_reroute_advice(route: dict[str, Any] | None = None) -> list[str]:
    advice = [
        "If scope, risk, or independence changed mid-task, re-run agentit trace with the current goal.",
        "Update STATE.md Next actions before any handoff or context limit.",
        "If critic_required and plan changed, re-run independent critic before more implementation.",
    ]
    if route and route.get("critic_required"):
        advice.append("Current route still marks critic_required=true.")
    if route and int((route.get("subagents") or {}).get("recommended") or 0) >= 2:
        advice.append("Parallel units still recommended; keep one writer per path.")
    return advice


def _atomic_write_text(path: Path, content: str) -> None:
    parent = path.parent
    parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.tmp-", dir=parent, text=True)
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
