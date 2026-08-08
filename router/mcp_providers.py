"""Provider adapters: read/write MCP enable state for multi-client support.

Supported clients:
  claude       — project .mcp.json + ~/.claude.json project keys (best-effort)
  cursor       — project .cursor/mcp.json or .mcp.json
  codex        — ~/.codex/config.toml [mcp_servers.*]
  grok         — ~/.grok/config.toml [mcp_servers.*] + enabled flag
  antigravity  — ~/.gemini/config/mcp_config.json
  project      — portable .mcp.json at project root

Dry-run by default at the runtime layer; adapters never prompt.
Backups written next to mutated files as .<name>.agentit-bak-<ts>.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import time
from pathlib import Path
from typing import Any, Callable

try:
    from router.mcp_catalog import get_server
except ImportError:  # pragma: no cover
    from mcp_catalog import get_server  # type: ignore

ALL_PROVIDERS = ("claude", "cursor", "codex", "grok", "antigravity", "project")

HOME = Path.home()


class McpProviderError(ValueError):
    pass


def _ts() -> str:
    return time.strftime("%Y%m%d%H%M%S")


def _backup(path: Path) -> Path | None:
    if not path.is_file() or path.is_symlink():
        return None
    # Avoid double-dot for names like ".mcp.json" → ".mcp.json.agentit-bak-…"
    bak = path.with_name(f"{path.name}.agentit-bak-{_ts()}")
    shutil.copy2(path, bak)
    os.chmod(bak, 0o600)
    return bak


def _atomic_write_text(path: Path, content: str, mode: int = 0o600) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.tmp-{os.getpid()}-{_ts()}")
    try:
        tmp.write_text(content, encoding="utf-8")
        os.chmod(tmp, mode)
        os.replace(tmp, path)
        os.chmod(path, mode)
    finally:
        tmp.unlink(missing_ok=True)


def _atomic_write_json(path: Path, data: dict[str, Any]) -> None:
    _atomic_write_text(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def server_config_entry(server_id: str, *, project_root: Path) -> dict[str, Any]:
    """Build a generic mcpServers entry from the catalog."""
    server = get_server(server_id)
    root = str(project_root)
    agentit_root = str(Path(__file__).resolve().parents[1])

    # First-party gateway: absolute paths so every client can spawn it.
    if server_id == "agentit-manager":
        return {
            "command": "python3",
            "args": [
                str(Path(agentit_root) / "mcp" / "gateway.py"),
                "--project",
                root,
                "--repo",
                agentit_root,
            ],
        }

    if isinstance(server.get("mcp_json"), dict):
        raw = json.dumps(server["mcp_json"])
        raw = raw.replace("${PROJECT_ROOT}", root).replace("${AGENTIT_ROOT}", agentit_root)
        return json.loads(raw)

    remote = server.get("mcp_json_remote")
    if isinstance(remote, dict) and remote.get("url"):
        return {"url": remote["url"]}

    raise McpProviderError(f"no installable config for server '{server_id}'")


def _json_mcp_root(data: dict[str, Any]) -> dict[str, Any]:
    if "mcpServers" not in data or not isinstance(data["mcpServers"], dict):
        data["mcpServers"] = {}
    return data["mcpServers"]


def _read_json(path: Path, *, allow_empty: bool = True) -> dict[str, Any]:
    if not path.is_file() or path.is_symlink():
        return {}
    raw = path.read_text(encoding="utf-8").strip()
    if not raw:
        if allow_empty:
            return {}
        raise McpProviderError(f"empty JSON config: {path}")
    try:
        data = json.loads(raw)
        return data if isinstance(data, dict) else {}
    except json.JSONDecodeError as exc:
        # Recover empty/whitespace-only or unusable stubs so install can proceed.
        if allow_empty and raw in {"", "{}", "null"}:
            return {}
        raise McpProviderError(f"invalid JSON: {path}: {exc}") from exc


# --- TOML helpers (stdlib-only, minimal for mcp_servers blocks) ---

_TOML_SECTION_RE = re.compile(
    r"^\[mcp_servers\.([A-Za-z0-9_-]+)\]\s*$", re.MULTILINE
)


def _parse_mcp_toml_enabled(text: str) -> dict[str, bool]:
    """Return {server_id: enabled} from codex/grok style toml."""
    result: dict[str, bool] = {}
    current: str | None = None
    for line in text.splitlines():
        m = _TOML_SECTION_RE.match(line.strip())
        if m:
            current = m.group(1)
            result.setdefault(current, True)
            continue
        if current is None:
            continue
        stripped = line.strip()
        if stripped.startswith("enabled"):
            # enabled = true|false
            if "=" in stripped:
                val = stripped.split("=", 1)[1].strip().lower()
                result[current] = val in {"true", "1", "yes"}
    return result


def _upsert_toml_mcp_server(
    text: str,
    server_id: str,
    *,
    enabled: bool,
    entry: dict[str, Any] | None,
) -> str:
    """Insert or update [mcp_servers.<id>] block. Preserves unrelated content."""
    section_header = f"[mcp_servers.{server_id}]"
    # Build new block
    lines = [section_header]
    if entry:
        if "command" in entry:
            lines.append(f'command = {_toml_str(entry["command"])}')
        if "args" in entry and isinstance(entry["args"], list):
            args_lit = ", ".join(_toml_str(a) for a in entry["args"])
            lines.append(f"args = [{args_lit}]")
        if "url" in entry:
            lines.append(f'url = {_toml_str(entry["url"])}')
        if "env" in entry and isinstance(entry["env"], dict):
            env_parts = []
            for k, v in entry["env"].items():
                env_parts.append(f"{k} = {_toml_str(str(v))}")
            lines.append("env = { " + ", ".join(env_parts) + " }")
    lines.append(f"enabled = {'true' if enabled else 'false'}")
    new_block = "\n".join(lines) + "\n"

    # Remove existing section if present
    pattern = re.compile(
        rf"^\[mcp_servers\.{re.escape(server_id)}\][^\n]*\n(?:(?!^\[).*\n)*",
        re.MULTILINE,
    )
    text2 = pattern.sub("", text)
    text2 = text2.rstrip() + "\n\n" + new_block
    return text2


def _toml_str(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def _remove_toml_mcp_server(text: str, server_id: str) -> str:
    pattern = re.compile(
        rf"^\[mcp_servers\.{re.escape(server_id)}\][^\n]*\n(?:(?!^\[).*\n)*",
        re.MULTILINE,
    )
    return pattern.sub("", text)


# --- Provider ops ---

def project_mcp_json_path(project_root: Path) -> Path:
    return project_root / ".mcp.json"


def cursor_mcp_json_path(project_root: Path) -> Path:
    cursor_dir = project_root / ".cursor"
    # Prefer .cursor/mcp.json when .cursor exists or for cursor-native layout
    return cursor_dir / "mcp.json"


def provider_status(
    provider: str,
    *,
    project_root: Path,
) -> dict[str, Any]:
    provider = provider.lower()
    if provider not in ALL_PROVIDERS:
        raise McpProviderError(f"unknown provider '{provider}'")

    if provider in {"project", "claude"}:
        path = project_mcp_json_path(project_root)
        data = _read_json(path)
        servers = _json_mcp_root(data) if data else {}
        return {
            "provider": provider,
            "config_path": str(path),
            "exists": path.is_file(),
            "servers": {
                k: {"enabled": not bool(v.get("disabled")) if isinstance(v, dict) else True}
                for k, v in servers.items()
            },
        }

    if provider == "cursor":
        path = cursor_mcp_json_path(project_root)
        alt = project_mcp_json_path(project_root)
        use = path if path.is_file() else alt
        data = _read_json(use)
        servers = data.get("mcpServers") if isinstance(data.get("mcpServers"), dict) else {}
        return {
            "provider": provider,
            "config_path": str(use),
            "exists": use.is_file(),
            "servers": {
                k: {"enabled": not bool(v.get("disabled")) if isinstance(v, dict) else True}
                for k, v in servers.items()
            },
        }

    if provider == "codex":
        path = HOME / ".codex" / "config.toml"
        text = path.read_text(encoding="utf-8") if path.is_file() and not path.is_symlink() else ""
        enabled_map = _parse_mcp_toml_enabled(text)
        return {
            "provider": provider,
            "config_path": str(path),
            "exists": path.is_file(),
            "servers": {k: {"enabled": v} for k, v in enabled_map.items()},
        }

    if provider == "grok":
        path = HOME / ".grok" / "config.toml"
        text = path.read_text(encoding="utf-8") if path.is_file() and not path.is_symlink() else ""
        enabled_map = _parse_mcp_toml_enabled(text)
        return {
            "provider": provider,
            "config_path": str(path),
            "exists": path.is_file(),
            "servers": {k: {"enabled": v} for k, v in enabled_map.items()},
        }

    if provider == "antigravity":
        path = HOME / ".gemini" / "config" / "mcp_config.json"
        data = _read_json(path)
        servers = data.get("mcpServers") if isinstance(data.get("mcpServers"), dict) else {}
        return {
            "provider": provider,
            "config_path": str(path),
            "exists": path.is_file(),
            "servers": {
                k: {"enabled": not bool(v.get("disabled")) if isinstance(v, dict) else True}
                for k, v in servers.items()
            },
        }

    raise McpProviderError(f"provider not implemented: {provider}")


def set_server_enabled(
    provider: str,
    server_id: str,
    *,
    enabled: bool,
    project_root: Path,
    apply: bool,
) -> dict[str, Any]:
    """Enable or disable a catalog server for one provider. Plan-first unless apply."""
    provider = provider.lower()
    entry = server_config_entry(server_id, project_root=project_root) if enabled else None

    if provider in {"project", "claude"}:
        path = project_mcp_json_path(project_root)
        return _set_json_mcp(path, server_id, enabled=enabled, entry=entry, apply=apply, provider=provider)

    if provider == "cursor":
        path = cursor_mcp_json_path(project_root)
        # Ensure parent exists on apply
        return _set_json_mcp(path, server_id, enabled=enabled, entry=entry, apply=apply, provider=provider)

    if provider == "antigravity":
        path = HOME / ".gemini" / "config" / "mcp_config.json"
        # Antigravity remote uses serverUrl key
        if entry and "url" in entry and "serverUrl" not in entry:
            entry = {**entry, "serverUrl": entry["url"]}
            entry.pop("url", None)
        return _set_json_mcp(path, server_id, enabled=enabled, entry=entry, apply=apply, provider=provider)

    if provider in {"codex", "grok"}:
        path = HOME / (".codex" if provider == "codex" else ".grok") / "config.toml"
        return _set_toml_mcp(path, server_id, enabled=enabled, entry=entry, apply=apply, provider=provider)

    raise McpProviderError(f"unknown provider '{provider}'")


def _set_json_mcp(
    path: Path,
    server_id: str,
    *,
    enabled: bool,
    entry: dict[str, Any] | None,
    apply: bool,
    provider: str,
) -> dict[str, Any]:
    data = _read_json(path)
    servers = _json_mcp_root(data)
    before = servers.get(server_id)

    if enabled:
        if entry is None:
            raise McpProviderError(f"missing entry for enable {server_id}")
        new_entry = dict(entry)
        new_entry.pop("disabled", None)
        servers[server_id] = new_entry
    else:
        if server_id in servers and isinstance(servers[server_id], dict):
            # Keep config, mark disabled when possible; else remove
            servers[server_id] = {**servers[server_id], "disabled": True}
        else:
            servers.pop(server_id, None)

    plan = {
        "provider": provider,
        "action": "enable" if enabled else "disable",
        "server_id": server_id,
        "config_path": str(path),
        "apply": apply,
        "before": before,
        "after": servers.get(server_id),
        "backup": None,
        "note": "Client may need session reload for tools to appear (except hot-reload clients).",
    }
    if not apply:
        plan["status"] = "planned"
        return plan

    bak = _backup(path) if path.is_file() else None
    plan["backup"] = str(bak) if bak else None
    _atomic_write_json(path, data)
    plan["status"] = "applied"
    return plan


def _set_toml_mcp(
    path: Path,
    server_id: str,
    *,
    enabled: bool,
    entry: dict[str, Any] | None,
    apply: bool,
    provider: str,
) -> dict[str, Any]:
    text = ""
    if path.is_file() and not path.is_symlink():
        text = path.read_text(encoding="utf-8")
    elif path.is_symlink():
        raise McpProviderError(f"symlink rejected: {path}")

    if enabled:
        new_text = _upsert_toml_mcp_server(text, server_id, enabled=True, entry=entry)
    else:
        # Prefer enabled=false over delete so re-enable is easy
        if entry is None and f"[mcp_servers.{server_id}]" in text:
            new_text = _upsert_toml_mcp_server(text, server_id, enabled=False, entry=None)
        elif entry is not None:
            new_text = _upsert_toml_mcp_server(text, server_id, enabled=False, entry=entry)
        else:
            new_text = _remove_toml_mcp_server(text, server_id)

    plan = {
        "provider": provider,
        "action": "enable" if enabled else "disable",
        "server_id": server_id,
        "config_path": str(path),
        "apply": apply,
        "backup": None,
        "note": "Restart or re-open session if tools do not refresh.",
        "diff_hint": f"toggle mcp_servers.{server_id}.enabled -> {enabled}",
    }
    if not apply:
        plan["status"] = "planned"
        return plan

    bak = _backup(path) if path.is_file() else None
    plan["backup"] = str(bak) if bak else None
    _atomic_write_text(path, new_text if new_text.endswith("\n") else new_text + "\n")
    plan["status"] = "applied"
    return plan


def install_gateway(
    *,
    project_root: Path,
    repo_root: Path,
    providers: list[str],
    apply: bool,
) -> list[dict[str, Any]]:
    """Register agentit-mcp-manager as always-on meta MCP across providers."""
    gateway_script = repo_root / "mcp" / "gateway.py"
    if not gateway_script.is_file():
        raise McpProviderError(f"gateway script missing: {gateway_script}")

    entry = {
        "command": "python3",
        "args": [str(gateway_script), "--project", str(project_root), "--repo", str(repo_root)],
    }
    results = []
    for provider in providers:
        # Special-case: write fixed entry id agentit-manager
        if provider in {"project", "claude", "cursor", "antigravity"}:
            if provider == "cursor":
                path = cursor_mcp_json_path(project_root)
            elif provider == "antigravity":
                path = HOME / ".gemini" / "config" / "mcp_config.json"
            else:
                path = project_mcp_json_path(project_root)
            data = _read_json(path)
            servers = _json_mcp_root(data)
            before = servers.get("agentit-manager")
            servers["agentit-manager"] = dict(entry)
            plan = {
                "provider": provider,
                "action": "install_gateway",
                "server_id": "agentit-manager",
                "config_path": str(path),
                "apply": apply,
                "before": before,
                "after": servers["agentit-manager"],
            }
            if apply:
                _backup(path) if path.is_file() else None
                _atomic_write_json(path, data)
                plan["status"] = "applied"
            else:
                plan["status"] = "planned"
            results.append(plan)
        elif provider in {"codex", "grok"}:
            path = HOME / (".codex" if provider == "codex" else ".grok") / "config.toml"
            text = path.read_text(encoding="utf-8") if path.is_file() and not path.is_symlink() else ""
            new_text = _upsert_toml_mcp_server(text, "agentit-manager", enabled=True, entry=entry)
            plan = {
                "provider": provider,
                "action": "install_gateway",
                "server_id": "agentit-manager",
                "config_path": str(path),
                "apply": apply,
            }
            if apply:
                if path.is_file():
                    _backup(path)
                _atomic_write_text(path, new_text if new_text.endswith("\n") else new_text + "\n")
                plan["status"] = "applied"
            else:
                plan["status"] = "planned"
            results.append(plan)
        else:
            results.append({"provider": provider, "status": "skipped", "reason": "unknown"})
    return results


def detect_providers() -> dict[str, bool]:
    """Which client homes appear present on this machine."""
    return {
        "claude": (HOME / ".claude.json").is_file() or shutil.which("claude") is not None,
        "cursor": (HOME / ".cursor").is_dir() or shutil.which("cursor") is not None,
        "codex": (HOME / ".codex").is_dir() or shutil.which("codex") is not None,
        "grok": (HOME / ".grok").is_dir() or shutil.which("grok") is not None,
        "antigravity": (HOME / ".gemini").is_dir(),
        "project": True,
    }
