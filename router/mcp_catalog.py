"""Curated MCP catalog for Agentit.

Opt-in only: list named stacks/servers, show entries, and emit provider snippets.
Never installs packages, never writes client configs, never activates servers,
and never infers a tool stack from natural-language task text.
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

VALID_PROVIDERS = ("claude", "cursor", "codex", "json")


class McpCatalogError(ValueError):
    """Invalid catalog path, server id, stack, or provider."""


def _load_yaml(path: Path) -> dict[str, Any]:
    if yaml is None:
        raise McpCatalogError("PyYAML is required to load mcp/catalog.yaml")
    if not path.is_file() or path.is_symlink():
        raise McpCatalogError(f"MCP catalog not found or symlink rejected: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise McpCatalogError("MCP catalog root must be a mapping")
    if not isinstance(data.get("servers"), list):
        raise McpCatalogError("MCP catalog must define a servers list")
    return data


def load_catalog(path: Path | None = None) -> dict[str, Any]:
    return _load_yaml(path or DEFAULT_CATALOG)


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
    """Reject the removed free-text heuristic API.

    Kept temporarily as an explicit compatibility failure so old callers do not
    silently fall back to a keyword classifier. The active AI must choose a
    named stack after interpreting the task from full context, then call
    `recommend_stack`/`plan_stack` with that explicit stack ID.
    """
    del task, catalog
    raise McpCatalogError(
        "free-text MCP routing was removed; the AI must choose an explicit named stack"
    )


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
