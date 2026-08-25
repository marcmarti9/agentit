"""Curated MCP catalog for Agentit.

Opt-in only: list named stacks/servers, show entries, and emit provider snippets.
Never installs packages, never writes client configs, never activates servers,
and never infers a tool stack from natural-language task text.

The first-party catalog may be extended by small files under ``mcp/catalog.d``.
Overlays are mechanical data extensions: they may append named servers to named
stacks, but they do not perform semantic routing.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = REPO_ROOT / "mcp" / "catalog.yaml"
DEFAULT_OVERLAY_DIR = REPO_ROOT / "mcp" / "catalog.d"

VALID_PROVIDERS = ("claude", "cursor", "codex", "json")


class McpCatalogError(ValueError):
    """Invalid catalog path, server id, stack, provider, or overlay."""


def _load_yaml(path: Path, *, require_servers: bool = True) -> dict[str, Any]:
    if yaml is None:
        raise McpCatalogError("PyYAML is required to load MCP catalog YAML")
    if not path.is_file() or path.is_symlink():
        raise McpCatalogError(f"MCP catalog not found or symlink rejected: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise McpCatalogError("MCP catalog root must be a mapping")
    if require_servers and not isinstance(data.get("servers"), list):
        raise McpCatalogError("MCP catalog must define a servers list")
    return data


def _merge_overlay(catalog: dict[str, Any], overlay: dict[str, Any], *, source: Path) -> None:
    if overlay.get("schema_version") != 1:
        raise McpCatalogError(f"MCP overlay must use schema_version: 1: {source}")

    existing_servers = {
        str(item.get("id")): item
        for item in catalog.get("servers", [])
        if isinstance(item, dict) and item.get("id")
    }
    new_servers = overlay.get("servers") or []
    if not isinstance(new_servers, list):
        raise McpCatalogError(f"MCP overlay servers must be a list: {source}")
    for server in new_servers:
        if not isinstance(server, dict) or not server.get("id"):
            raise McpCatalogError(f"MCP overlay server must have an id: {source}")
        server_id = str(server["id"])
        if server_id in existing_servers:
            raise McpCatalogError(f"duplicate MCP server id '{server_id}' from overlay {source}")
        catalog.setdefault("servers", []).append(server)
        existing_servers[server_id] = server

    stacks = catalog.get("stacks") or {}
    if not isinstance(stacks, dict):
        raise McpCatalogError("MCP catalog stacks must be a mapping")
    overlay_stacks = overlay.get("stacks") or {}
    if not isinstance(overlay_stacks, dict):
        raise McpCatalogError(f"MCP overlay stacks must be a mapping: {source}")
    for stack_id, patch in overlay_stacks.items():
        if stack_id not in stacks:
            raise McpCatalogError(f"MCP overlay references unknown stack '{stack_id}': {source}")
        if not isinstance(patch, dict):
            raise McpCatalogError(f"MCP overlay stack patch must be a mapping: {source}")
        append_servers = patch.get("append_servers") or []
        if not isinstance(append_servers, list) or not all(
            isinstance(item, str) for item in append_servers
        ):
            raise McpCatalogError(f"MCP overlay append_servers must be a string list: {source}")
        unknown = [server_id for server_id in append_servers if server_id not in existing_servers]
        if unknown:
            raise McpCatalogError(
                f"MCP overlay stack '{stack_id}' references unknown servers {unknown}: {source}"
            )
        current = stacks[stack_id].get("servers") or []
        for server_id in append_servers:
            if server_id not in current:
                current.append(server_id)
        stacks[stack_id]["servers"] = current


def load_catalog(path: Path | None = None) -> dict[str, Any]:
    target = path or DEFAULT_CATALOG
    data = _load_yaml(target)
    # Custom test/consumer catalogs stay self-contained. Only the canonical Agentit
    # catalog receives first-party overlays from mcp/catalog.d.
    if path is None and DEFAULT_OVERLAY_DIR.is_dir() and not DEFAULT_OVERLAY_DIR.is_symlink():
        for overlay_path in sorted(DEFAULT_OVERLAY_DIR.glob("*.yaml")):
            overlay = _load_yaml(overlay_path, require_servers=False)
            _merge_overlay(data, overlay, source=overlay_path)
    return data


def _servers_by_id(catalog: dict[str, Any]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for item in catalog.get("servers", []):
        if not isinstance(item, dict) or not item.get("id"):
            continue
        out[str(item["id"])] = item
    return out


def list_servers(
    catalog: dict[str, Any] | None = None,
    *,
    tier: str | None = None,
    category: str | None = None,
    max_risk: str | None = None,
) -> list[dict[str, Any]]:
    data = catalog or load_catalog()
    risk_order = {"RISK_1": 1, "RISK_2": 2, "RISK_3": 3, "RISK_4": 4}
    max_level = risk_order.get(max_risk or "", 99)
    rows: list[dict[str, Any]] = []
    for server in data.get("servers", []):
        if not isinstance(server, dict):
            continue
        if tier and server.get("tier") != tier:
            continue
        if category and server.get("category") != category:
            continue
        risk = str(server.get("risk", "RISK_2"))
        if risk_order.get(risk, 99) > max_level:
            continue
        rows.append(
            {
                "id": server.get("id"),
                "name": server.get("name"),
                "tier": server.get("tier"),
                "category": server.get("category"),
                "risk": risk,
                "requires_secret": bool(server.get("requires_secret")),
                "write_capable": bool(server.get("write_capable")),
                "summary": server.get("summary"),
            }
        )
    tier_rank = {"core": 0, "recommended": 1, "situational": 2}
    rows.sort(key=lambda r: (tier_rank.get(str(r.get("tier")), 9), str(r.get("id"))))
    return rows


def get_server(server_id: str, catalog: dict[str, Any] | None = None) -> dict[str, Any]:
    data = catalog or load_catalog()
    server = _servers_by_id(data).get(server_id)
    if not server:
        known = ", ".join(sorted(_servers_by_id(data)))
        raise McpCatalogError(f"unknown MCP server '{server_id}'; known: {known}")
    return server


def list_stacks(catalog: dict[str, Any] | None = None) -> dict[str, Any]:
    data = catalog or load_catalog()
    stacks = data.get("stacks") or {}
    if not isinstance(stacks, dict):
        return {}
    return stacks


def recommend_stack(stack_name: str, catalog: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return one explicitly selected named stack.

    The caller (normally the AI after TASK_DECISION/review) chooses the stack.
    This function only resolves catalog metadata mechanically.
    """
    data = catalog or load_catalog()
    stacks = list_stacks(data)
    if stack_name not in stacks:
        known = ", ".join(sorted(stacks))
        raise McpCatalogError(f"unknown stack '{stack_name}'; known: {known}")
    stack = stacks[stack_name]
    ids = list(stack.get("servers") or [])
    servers = [get_server(sid, data) for sid in ids]
    return {
        "stack": stack_name,
        "description": stack.get("description"),
        "policy": data.get("policy"),
        "servers": [
            {
                "id": s.get("id"),
                "name": s.get("name"),
                "risk": s.get("risk"),
                "requires_secret": bool(s.get("requires_secret")),
                "write_capable": bool(s.get("write_capable")),
                "summary": s.get("summary"),
            }
            for s in servers
        ],
        "activation": "opt-in only; Agentit does not enable MCP automatically",
    }


def recommend_for_task(task: str, catalog: dict[str, Any] | None = None) -> dict[str, Any]:
    """Backward-compatible exact-stack resolver with no task-text inference.

    Older callers still import this name. Treat the argument only as an exact
    stack id; arbitrary natural-language text is rejected explicitly instead of
    being classified.
    """
    data = catalog or load_catalog()
    stacks = list_stacks(data)
    if task not in stacks:
        known = ", ".join(sorted(stacks))
        raise McpCatalogError(
            "free-text MCP routing was removed; the AI must choose an explicit "
            f"named stack; unknown stack '{task}'; known: {known}"
        )
    return recommend_stack(task, data)


def _mcp_json_entry(server: dict[str, Any]) -> dict[str, Any]:
    if "mcp_json" in server and isinstance(server["mcp_json"], dict):
        return dict(server["mcp_json"])
    remote = server.get("mcp_json_remote")
    if isinstance(remote, dict) and remote.get("url"):
        return {"url": remote["url"]}
    raise McpCatalogError(
        f"server '{server.get('id')}' has no mcp_json / mcp_json_remote snippet"
    )


def snippet_for_server(
    server_id: str,
    *,
    provider: str = "json",
    catalog: dict[str, Any] | None = None,
    project_root: str = "${PROJECT_ROOT}",
) -> dict[str, Any]:
    provider = provider.lower()
    if provider not in VALID_PROVIDERS:
        raise McpCatalogError(f"provider must be one of {VALID_PROVIDERS}")
    data = catalog or load_catalog()
    server = get_server(server_id, data)
    policy = data.get("policy") or {}

    payload: dict[str, Any] = {
        "id": server_id,
        "provider": provider,
        "risk": server.get("risk"),
        "requires_secret": bool(server.get("requires_secret")),
        "secret_env": server.get("secret_env"),
        "write_capable": bool(server.get("write_capable")),
        "safety_notes": server.get("safety_notes") or [],
        "homepage": server.get("homepage"),
        "auto_activate": False,
        "policy_note": policy.get("notes", "").strip() if isinstance(policy.get("notes"), str) else "",
    }

    if provider == "claude":
        cmd = server.get("claude_add")
        if not cmd:
            raise McpCatalogError(f"no claude_add snippet for '{server_id}'")
        payload["command"] = str(cmd).replace("${PROJECT_ROOT}", project_root)
        return payload

    if provider == "codex":
        toml = server.get("codex_toml") or server.get("codex_note")
        if not toml:
            entry = _mcp_json_entry(server)
            payload["snippet"] = (
                f"# Manual Codex config for {server_id}\n"
                f"# See homepage: {server.get('homepage')}\n"
                f"# Suggested transport config (adapt to config.toml):\n"
                f"{json.dumps(entry, indent=2)}\n"
            )
            return payload
        payload["snippet"] = str(toml).replace("${PROJECT_ROOT}", project_root)
        return payload

    entry = _mcp_json_entry(server)
    rendered = json.loads(
        json.dumps(entry).replace("${PROJECT_ROOT}", project_root)
    )
    payload["mcpServers"] = {server_id: rendered}
    payload["snippet"] = json.dumps({"mcpServers": {server_id: rendered}}, indent=2)
    return payload


def plan_stack(
    stack_name: str,
    *,
    provider: str = "json",
    catalog: dict[str, Any] | None = None,
    project_root: str = "${PROJECT_ROOT}",
) -> dict[str, Any]:
    data = catalog or load_catalog()
    rec = recommend_stack(stack_name, data)
    snippets = [
        snippet_for_server(
            s["id"],
            provider=provider,
            catalog=data,
            project_root=project_root,
        )
        for s in rec["servers"]
    ]
    merged: dict[str, Any] = {}
    if provider in {"json", "cursor"}:
        for snip in snippets:
            merged.update(snip.get("mcpServers") or {})
    return {
        "stack": stack_name,
        "description": rec.get("description"),
        "provider": provider,
        "activation": "opt-in only; review secrets and scopes before enabling",
        "servers": rec["servers"],
        "snippets": snippets,
        "mcpServers": merged or None,
        "combined_snippet": (
            json.dumps({"mcpServers": merged}, indent=2) if merged else None
        ),
    }


def catalog_summary(catalog: dict[str, Any] | None = None) -> dict[str, Any]:
    data = catalog or load_catalog()
    servers = list_servers(data)
    stacks = list_stacks(data)
    return {
        "schema_version": data.get("schema_version"),
        "policy": data.get("policy"),
        "server_count": len(servers),
        "stack_count": len(stacks),
        "stacks": {
            name: {
                "description": meta.get("description"),
                "servers": meta.get("servers"),
            }
            for name, meta in stacks.items()
        },
        "servers": servers,
    }
