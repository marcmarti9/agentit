#!/usr/bin/env python3
"""Agentit MCP Manager — always-on meta MCP for mid-session enable/disable.

Exposes tools so agents in Claude / Grok / Cursor / Codex / Antigravity can:
  - see catalog + active servers
  - enable / disable catalog servers across providers
  - get stack recommendations

Does NOT auto-start every backend MCP. It writes provider configs and desired
state; clients may need a reconnect for third-party tools to appear. Meta tools
work immediately in the same session.

Protocol: minimal MCP over stdio (JSON-RPC 2.0, Content-Length framing optional
via newline-delimited JSON which most coding clients accept for stdio).
"""

from __future__ import annotations

import argparse
import json
import sys
import traceback
from pathlib import Path
from typing import Any

REPO_DEFAULT = Path(__file__).resolve().parents[1]
if str(REPO_DEFAULT) not in sys.path:
    sys.path.insert(0, str(REPO_DEFAULT))

from router.mcp_runtime import (  # noqa: E402
    McpRuntimeError,
    bootstrap_gateway,
    disable_server,
    enable_server,
    enable_stack,
    runtime_status,
)
from router.mcp_catalog import list_servers, recommend_for_task  # noqa: E402


SERVER_INFO = {"name": "agentit-manager", "version": "0.1.0"}

TOOLS = [
    {
        "name": "mcp_status",
        "description": (
            "Show available MCP catalog servers, desired enabled set, and per-provider "
            "config state (Claude, Cursor, Codex, Grok, Antigravity, project)."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    },
    {
        "name": "mcp_list_available",
        "description": "List curated MCP servers the agent may enable (id, tier, risk, summary).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "tier": {
                    "type": "string",
                    "enum": ["core", "recommended", "situational"],
                },
                "max_risk": {
                    "type": "string",
                    "enum": ["RISK_1", "RISK_2", "RISK_3", "RISK_4"],
                },
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "mcp_list_active",
        "description": "List currently desired/active MCP server ids for this project/user.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    },
    {
        "name": "mcp_enable",
        "description": (
            "Enable a catalog MCP server across detected providers. "
            "Writes client configs when apply=true (default true for this tool). "
            "RISK_3/4 requires force=true."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "server_id": {"type": "string"},
                "apply": {"type": "boolean", "default": True},
                "force": {"type": "boolean", "default": False},
                "providers": {
                    "type": "string",
                    "description": "Comma list or 'all' (default all detected).",
                },
            },
            "required": ["server_id"],
            "additionalProperties": False,
        },
    },
    {
        "name": "mcp_disable",
        "description": "Disable an MCP server across providers (apply=true by default).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "server_id": {"type": "string"},
                "apply": {"type": "boolean", "default": True},
                "providers": {"type": "string"},
            },
            "required": ["server_id"],
            "additionalProperties": False,
        },
    },
    {
        "name": "mcp_recommend",
        "description": "Recommend an MCP stack for a task description or stack name.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "task": {"type": "string"},
                "enable": {
                    "type": "boolean",
                    "description": "If true, also enable the stack (apply=true).",
                    "default": False,
                },
                "force": {"type": "boolean", "default": False},
            },
            "required": ["task"],
            "additionalProperties": False,
        },
    },
]


class Gateway:
    def __init__(self, project_root: Path, repo_root: Path) -> None:
        self.project_root = project_root
        self.repo_root = repo_root

    def _providers(self, raw: str | None) -> list[str] | None:
        if not raw or raw == "all":
            return None
        return [p.strip() for p in raw.split(",") if p.strip()]

    def call_tool(self, name: str, arguments: dict[str, Any] | None) -> dict[str, Any]:
        args = arguments or {}
        if name == "mcp_status":
            return runtime_status(project_root=self.project_root)
        if name == "mcp_list_available":
            return {
                "servers": list_servers(
                    tier=args.get("tier"),
                    max_risk=args.get("max_risk"),
                )
            }
        if name == "mcp_list_active":
            st = runtime_status(project_root=self.project_root)
            return {
                "desired_enabled": st["desired_enabled"],
                "active_union": st["active_union"],
            }
        if name == "mcp_enable":
            sid = args.get("server_id")
            if not sid:
                raise McpRuntimeError("server_id required")
            return enable_server(
                str(sid),
                project_root=self.project_root,
                providers=self._providers(args.get("providers")),
                apply=bool(args.get("apply", True)),
                force=bool(args.get("force", False)),
            )
        if name == "mcp_disable":
            sid = args.get("server_id")
            if not sid:
                raise McpRuntimeError("server_id required")
            return disable_server(
                str(sid),
                project_root=self.project_root,
                providers=self._providers(args.get("providers")),
                apply=bool(args.get("apply", True)),
            )
        if name == "mcp_recommend":
            task = args.get("task") or ""
            rec = recommend_for_task(str(task))
            if args.get("enable"):
                en = enable_stack(
                    str(task),
                    project_root=self.project_root,
                    apply=True,
                    force=bool(args.get("force", False)),
                )
                return {"recommendation": rec, "enable_result": en}
            return rec
        raise McpRuntimeError(f"unknown tool: {name}")


def _respond(msg_id: Any, result: Any) -> None:
    payload = {"jsonrpc": "2.0", "id": msg_id, "result": result}
    sys.stdout.write(json.dumps(payload, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def _error(msg_id: Any, code: int, message: str) -> None:
    payload = {
        "jsonrpc": "2.0",
        "id": msg_id,
        "error": {"code": code, "message": message},
    }
    sys.stdout.write(json.dumps(payload, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def handle(gw: Gateway, message: dict[str, Any]) -> None:
    method = message.get("method")
    msg_id = message.get("id")
    params = message.get("params") or {}

    # Notifications (no id) — ignore
    if msg_id is None and method and method.startswith("notifications/"):
        return

    if method == "initialize":
        _respond(
            msg_id,
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": SERVER_INFO,
            },
        )
        return

    if method == "notifications/initialized":
        return

    if method == "ping":
        _respond(msg_id, {})
        return

    if method == "tools/list":
        _respond(msg_id, {"tools": TOOLS})
        return

    if method == "tools/call":
        name = params.get("name")
        arguments = params.get("arguments") or {}
        try:
            result = gw.call_tool(str(name), arguments if isinstance(arguments, dict) else {})
            text = json.dumps(result, ensure_ascii=False, indent=2)
            _respond(
                msg_id,
                {
                    "content": [{"type": "text", "text": text}],
                    "structuredContent": result,
                    "isError": False,
                },
            )
        except (McpRuntimeError, ValueError, OSError) as exc:
            _respond(
                msg_id,
                {
                    "content": [{"type": "text", "text": f"ERROR: {exc}"}],
                    "isError": True,
                },
            )
        except Exception as exc:  # pragma: no cover
            _respond(
                msg_id,
                {
                    "content": [
                        {
                            "type": "text",
                            "text": f"INTERNAL: {exc}\n{traceback.format_exc()}",
                        }
                    ],
                    "isError": True,
                },
            )
        return

    if method == "resources/list":
        _respond(msg_id, {"resources": []})
        return

    if method == "prompts/list":
        _respond(msg_id, {"prompts": []})
        return

    if msg_id is not None:
        _error(msg_id, -32601, f"Method not found: {method}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Agentit MCP Manager gateway")
    parser.add_argument("--project", type=Path, default=Path.cwd())
    parser.add_argument("--repo", type=Path, default=REPO_DEFAULT)
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run one tools/list cycle on stdout as JSON and exit",
    )
    args = parser.parse_args(argv)
    project_root = args.project.resolve()
    repo_root = args.repo.resolve()
    gw = Gateway(project_root=project_root, repo_root=repo_root)

    if args.self_test:
        print(json.dumps({"tools": [t["name"] for t in TOOLS], "ok": True}))
        return 0

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            message = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(message, dict):
            continue
        handle(gw, message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
