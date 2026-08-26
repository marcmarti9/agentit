# Agentit MCP Catalog & Runtime

Curated MCP servers **plus mid-session enable/disable** for every major coding agent:

| Provider | Config surface |
|----------|----------------|
| Claude Code | project `.mcp.json` (+ Claude MCP UI) |
| Cursor | `.cursor/mcp.json` |
| Codex | `~/.codex/config.toml` `[mcp_servers.*]` |
| Grok Build | `~/.grok/config.toml` `[mcp_servers.*]` + `enabled` |
| Antigravity | `~/.gemini/config/mcp_config.json` |
| Portable project | `.mcp.json` |

## Agent workflow (what you wanted)

In any session the agent can:

```bash
# What can I enable? What is on?
agentit mcp status
agentit mcp available
agentit mcp active

# Toggle (plan first, then apply)
agentit mcp enable context7 --providers all
agentit mcp enable context7 --providers all --apply
agentit mcp disable playwright --providers project --apply

# Stack selected explicitly by the primary AI
agentit mcp recommend developer_core
agentit mcp enable-stack developer_core --apply

# Always-on meta MCP so tools work without shell
agentit mcp install-gateway --apply
```

### MCP tools (after `install-gateway`)

Connect **agentit-manager** once. The agent then calls:

| Tool | Purpose |
|------|---------|
| `mcp_status` | Catalog + desired + per-provider state |
| `mcp_list_available` | Curated servers (filter tier/risk) |
| `mcp_list_active` | Currently enabled ids |
| `mcp_enable` | Enable server (`apply` default true; `force` for RISK_3+) |
| `mcp_disable` | Disable server |
| `mcp_recommend` | Inspect an explicit `stack_id`; optional `enable=true` |

`mcp_recommend` does **not** accept a natural-language task description. The primary AI chooses the stack from the full task context, then the manager resolves that named stack mechanically.

## Bootstrap (once per machine)

```bash
cd ~/code/agentit   # or any project
agentit mcp install-gateway --apply
# Restart or reconnect MCP in each client once
```

That writes `agentit-manager` into detected providers so every agent can self-manage MCPs.

## Starter stack

| Id | Role |
|----|------|
| **agentit-manager** | Meta toggle (install first) |
| **context7** | Live library docs |
| **github** | Issues/PRs (OAuth preferred) |
| **playwright** | Browser smoke tests |

Situational mobile research lives in stack `mobile_design` (`appllama` + `context7`). It is **not** part of `developer_core`. Enable only for Expo/React Native product UI; the library is credit-metered.

```bash
agentit mcp enable-stack developer_core --apply
agentit mcp enable-stack mobile_design --apply   # mobile tasks only
```

## Risk gates

| Risk | Rule |
|------|------|
| RISK_1 / RISK_2 | Agent may enable with `--apply` |
| RISK_3 / RISK_4 | Requires `--force` (DB/prod-class) |

Secrets stay in env vars (`${GITHUB_PERSONAL_ACCESS_TOKEN}`, etc.), never committed.

## Session reload reality

| Client | After enable/disable |
|--------|----------------------|
| **agentit-manager tools** | Immediate in same session |
| **Grok** | `enabled` flag; often picks up on config reload |
| **Claude / Cursor / Codex / Antigravity** | May need new session or MCP reconnect for *backend* tools |

Meta management always works via CLI or agentit-manager; third-party tool surfaces depend on the host client.

## About “Notch MCP”

- **Agent Notch** ([realfishsam/agent-notch](https://github.com/realfishsam/agent-notch)): Mac menu-bar session visibility for Claude/Codex — not a tool MCP.
- **Notch Manual MCP**: docs for the Notch product — not a coding stack.
- Agentit focuses on **runtime catalog + enable/disable** instead of a notch UI.

## Maintenance

| Path | Role |
|------|------|
| `mcp/catalog.yaml` | Curated servers + stacks |
| `router/mcp_catalog.py` | Read/resolve named stacks/snippets |
| `router/mcp_runtime.py` | Desired state + enable/disable |
| `router/mcp_providers.py` | Multi-client config writers |
| `mcp/gateway.py` | stdio MCP manager |
| `agentit mcp …` | CLI |

## Safety

- Plan-first by default on CLI (`--apply` to write).
- Backups: `.<file>.agentit-bak-<timestamp>` next to mutated configs.
- No symlink writes; mode `0600` on state files.
- Prefer official packages; pin when you can.
