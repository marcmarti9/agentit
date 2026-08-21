"""Agent-facing MCP runtime: list available, enable/disable across providers.

Canonical desired state lives in ~/.agentit/mcp/state.json (user) and
optionally .agentit/mcp-state.json (project overlay).

Agents in any session should:
  1. agentit mcp status
  2. agentit mcp enable <id> --apply   (or MCP tools on agentit-manager)
  3. use the newly enabled server tools after client refresh / via gateway proxy
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any

try:
    from router.mcp_catalog import (
        McpCatalogError,
        get_server,
        list_servers,
        load_catalog,
        recommend_stack,
    )
    from router.mcp_providers import (
        ALL_PROVIDERS,
        McpProviderError,
        detect_providers,
        install_gateway,
        provider_status,
        set_server_enabled,
    )
except ImportError:  # pragma: no cover
    from mcp_catalog import (  # type: ignore
        McpCatalogError,
        get_server,
        list_servers,
        load_catalog,
        recommend_stack,
    )
    from mcp_providers import (  # type: ignore
        ALL_PROVIDERS,
        McpProviderError,
        detect_providers,
        install_gateway,
        provider_status,
        set_server_enabled,
    )

USER_STATE_DIR = Path.home() / ".agentit" / "mcp"
USER_STATE_PATH = USER_STATE_DIR / "state.json"


class McpRuntimeError(ValueError):
    pass


def _project_state_path(project_root: Path) -> Path:
    return project_root / ".agentit" / "mcp-state.json"


def _read_state(path: Path) -> dict[str, Any]:
    if not path.is_file() or path.is_symlink():
        return {"version": 1, "enabled": [], "updated_at": None}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"version": 1, "enabled": [], "updated_at": None}
    if not isinstance(data, dict):
        return {"version": 1, "enabled": [], "updated_at": None}
    enabled = data.get("enabled") or []
    if not isinstance(enabled, list):
        enabled = []
    return {
        "version": int(data.get("version") or 1),
        "enabled": [str(x) for x in enabled],
        "updated_at": data.get("updated_at"),
    }


def _write_state(path: Path, enabled: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": 1,
        "enabled": sorted(set(enabled)),
        "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    tmp = path.with_name(f".{path.name}.tmp-{os.getpid()}")
    try:
        tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        os.chmod(tmp, 0o600)
        os.replace(tmp, path)
        os.chmod(path, 0o600)
    finally:
        tmp.unlink(missing_ok=True)


def load_desired_enabled(project_root: Path | None = None) -> list[str]:
    """Project overlay wins when present; else user state."""
    if project_root is not None:
        p = _project_state_path(project_root)
        if p.is_file() and not p.is_symlink():
            return list(_read_state(p)["enabled"])
    return list(_read_state(USER_STATE_PATH)["enabled"])


def save_desired_enabled(enabled: list[str], project_root: Path | None = None) -> Path:
    """Persist desired enabled set. Project scope writes only project state."""
    path = _project_state_path(project_root) if project_root is not None else USER_STATE_PATH
    _write_state(path, enabled)
    return path


def runtime_status(
    *,
    project_root: Path,
    providers: list[str] | None = None,
) -> dict[str, Any]:
    catalog = load_catalog()
    available = list_servers(catalog)
    desired = load_desired_enabled(project_root)
    present = detect_providers()
    provs = providers or [p for p, ok in present.items() if ok]
    provider_views = {}
    for p in provs:
        try:
            provider_views[p] = provider_status(p, project_root=project_root)
        except (McpProviderError, OSError) as exc:
            provider_views[p] = {"provider": p, "error": str(exc)}

    # Merge active: desired OR enabled in any provider config
    active_from_providers: set[str] = set()
    for view in provider_views.values():
        servers = view.get("servers") or {}
        if isinstance(servers, dict):
            for sid, meta in servers.items():
                if isinstance(meta, dict) and meta.get("enabled", True):
                    active_from_providers.add(sid)

    return {
        "policy": {
            "agent_may_toggle": True,
            "default_apply": False,
            "risk_gate": "RISK_3+ requires --force",
            "reload_note": (
                "After enable/disable, Claude/Cursor/Codex often need a new session "
                "or MCP refresh. Grok supports enable/disable flags; agentit-manager "
                "meta-tools work immediately in the same session."
            ),
        },
        "desired_enabled": desired,
        "available": available,
        "providers_detected": present,
        "providers": provider_views,
        "active_union": sorted(set(desired) | active_from_providers),
        "agent_workflow": [
            "agentit mcp status",
            "agentit mcp enable <id> --apply   # or agentit-manager MCP tool",
            "agentit mcp disable <id> --apply",
            "If tools missing: reload session / reconnect MCP",
        ],
    }


def enable_server(
    server_id: str,
    *,
    project_root: Path,
    providers: list[str] | None = None,
    apply: bool = False,
    force: bool = False,
) -> dict[str, Any]:
    try:
        server = get_server(server_id)
    except McpCatalogError as exc:
        raise McpRuntimeError(str(exc)) from exc

    risk = str(server.get("risk") or "RISK_2")
    if risk in {"RISK_3", "RISK_4"} and not force:
        raise McpRuntimeError(
            f"{server_id} is {risk} (secrets/write DB risk). Re-run with --force after review."
        )

    present = detect_providers()
    if providers is None:
        targets = [p for p, ok in present.items() if ok]
    else:
        targets = providers
    if not targets:
        targets = ["project"]

    plans = []
    for p in targets:
        try:
            plans.append(
                set_server_enabled(
                    p,
                    server_id,
                    enabled=True,
                    project_root=project_root,
                    apply=apply,
                )
            )
        except (McpProviderError, OSError) as exc:
            plans.append({"provider": p, "status": "error", "error": str(exc)})

    desired = load_desired_enabled(project_root)
    if apply:
        if server_id not in desired:
            desired.append(server_id)
        state_path = save_desired_enabled(desired, project_root)
    else:
        state_path = None

    return {
        "action": "enable",
        "server_id": server_id,
        "risk": risk,
        "apply": apply,
        "desired_enabled": desired if apply else sorted(set(desired) | {server_id}),
        "state_path": str(state_path) if state_path else None,
        "provider_results": plans,
        "next": (
            "Tools should appear after client MCP refresh. "
            "With agentit-manager installed, meta-tools work now; "
            "backend tools may need session reload unless proxied."
        ),
    }


def disable_server(
    server_id: str,
    *,
    project_root: Path,
    providers: list[str] | None = None,
    apply: bool = False,
) -> dict[str, Any]:
    # Allow disable even if not in catalog (orphan cleanup)
    try:
        get_server(server_id)
        known = True
    except McpCatalogError:
        known = False

    present = detect_providers()
    if providers is None:
        targets = [p for p, ok in present.items() if ok]
    else:
        targets = providers
    if not targets:
        targets = ["project"]

    plans = []
    for p in targets:
        try:
            plans.append(
                set_server_enabled(
                    p,
                    server_id,
                    enabled=False,
                    project_root=project_root,
                    apply=apply,
                )
            )
        except (McpProviderError, OSError) as exc:
            plans.append({"provider": p, "status": "error", "error": str(exc)})

    desired = load_desired_enabled(project_root)
    if apply:
        desired = [x for x in desired if x != server_id]
        state_path = save_desired_enabled(desired, project_root)
    else:
        state_path = None

    return {
        "action": "disable",
        "server_id": server_id,
        "known_catalog": known,
        "apply": apply,
        "desired_enabled": desired if apply else [x for x in desired if x != server_id],
        "state_path": str(state_path) if state_path else None,
        "provider_results": plans,
    }


def enable_stack(
    stack_id: str,
    *,
    project_root: Path,
    providers: list[str] | None = None,
    apply: bool = False,
    force: bool = False,
) -> dict[str, Any]:
    """Enable one explicit named stack selected by the AI.

    This function performs only catalog lookup and enablement. It never infers a
    stack from natural-language task text.
    """
    try:
        rec = recommend_stack(stack_id)
    except McpCatalogError as exc:
        raise McpRuntimeError(str(exc)) from exc

    results = []
    errors = []
    for s in rec.get("servers") or []:
        sid = s["id"] if isinstance(s, dict) else str(s)
        try:
            results.append(
                enable_server(
                    sid,
                    project_root=project_root,
                    providers=providers,
                    apply=apply,
                    force=force,
                )
            )
        except McpRuntimeError as exc:
            errors.append({"server_id": sid, "error": str(exc)})
    return {
        "action": "enable_stack",
        "stack": rec.get("stack"),
        "apply": apply,
        "results": results,
        "errors": errors,
    }


def bootstrap_gateway(
    *,
    project_root: Path,
    repo_root: Path,
    providers: list[str] | None = None,
    apply: bool = False,
) -> dict[str, Any]:
    present = detect_providers()
    targets = providers or [p for p, ok in present.items() if ok]
    plans = install_gateway(
        project_root=project_root,
        repo_root=repo_root,
        providers=targets,
        apply=apply,
    )
    return {
        "action": "install_gateway",
        "apply": apply,
        "providers": targets,
        "results": plans,
        "tools_exposed": [
            "mcp_list_available",
            "mcp_list_active",
            "mcp_enable",
            "mcp_disable",
            "mcp_status",
            "mcp_recommend",
        ],
        "note": (
            "agentit-manager is the always-on meta MCP. Agents call its tools mid-session "
            "to see the catalog and toggle servers. Install once per machine/project."
        ),
    }


def resolve_providers_arg(raw: str | None) -> list[str] | None:
    if not raw or raw in {"all", "*"}:
        return None
    parts = [p.strip().lower() for p in raw.split(",") if p.strip()]
    bad = [p for p in parts if p not in ALL_PROVIDERS]
    if bad:
        raise McpRuntimeError(f"unknown providers: {bad}; valid: {ALL_PROVIDERS}")
    return parts
