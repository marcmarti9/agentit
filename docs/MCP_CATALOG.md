# Agentit MCP Catalog & Runtime

Curated MCP servers **plus mid-session enable/disable** for every major coding agent.

The core rule is: **configured/visible is not selected**. MCP configuration may persist in a host, but every new Agentit session makes a fresh tool decision and treats non-selected MCPs as inactive for the current task.

| Provider | Config surface |
|----------|----------------|
| Claude Code | project `.mcp.json` (+ Claude MCP UI) |
| Cursor | `.cursor/mcp.json` |
| Codex | `~/.codex/config.toml` `[mcp_servers.*]` |
| Grok Build | `~/.grok/config.toml` `[mcp_servers.*]` + `enabled` |
| Antigravity | `~/.gemini/config/mcp_config.json` |
| Portable project | `.mcp.json` |

## Agent workflow

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

## Session lifecycle

Agentit uses a **semantic cold start** rather than assuming provider configuration is ephemeral.

At the beginning of a new session:

1. Only Agentit's core skills are assumed active.
2. Run/inspect MCP status only if tool selection matters.
3. Ignore previously enabled third-party MCPs unless the new `TASK_DECISION` selects them again.
4. Enable only the smallest server/stack set justified by this task.
5. Record which MCPs this task itself enabled so cleanup has an owner.

At completion:

- disable MCPs that **this task added** when the provider supports safe toggling and the project/user did not ask to keep them available;
- do not blanket-remove unrelated user MCPs or servers another concurrent session may be using;
- leave `agentit-manager` as the optional persistent meta-control plane when installed;
- if a provider requires restart/reconnect to unload a server, document that limitation and still treat the next session as logically clean until the MCP is explicitly re-selected.

This distinction is intentional:

```text
installed/configured = available
selected in TASK_DECISION = authorized for this task
enabled = provider runtime state
used = actual task action
```

Those are not synonyms.

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

`developer_core` is a named convenience stack, **not** an always-on runtime bundle. A coding task may need none, one, or several of those servers.

Situational mobile research lives in stack `mobile_design` (`appllama` + `context7`). It is **not** part of the session core. Enable only for Expo/React Native product UI when that research materially helps; the library is credit-metered.

```bash
agentit mcp enable-stack developer_core --apply
agentit mcp enable-stack mobile_design --apply   # mobile tasks only
```

## Risk gates

| Risk | Rule |
|------|------|
| RISK_1 / RISK_2 | Agent may enable with `--apply` when selected by the current plan |
| RISK_3 / RISK_4 | Requires `--force` (DB/prod-class) plus reviewed justification |

Secrets stay in env vars (`${GITHUB_PERSONAL_ACCESS_TOKEN}`, etc.), never committed.

## Session reload reality

| Client | After enable/disable |
|--------|----------------------|
| **agentit-manager tools** | Immediate in same session |
| **Grok** | `enabled` flag; often picks up on config reload |
| **Claude / Cursor / Codex / Antigravity** | May need new session or MCP reconnect for *backend* tools |

Meta management always works via CLI or agentit-manager; third-party tool surfaces depend on the host client.

A stale tool surface after disable is not permission to keep using it. Conversely, a selected MCP that has not appeared after enable is not available yet: reconnect/reload or choose another route.

## Profiles, stacks and sessions

Do not confuse the three layers:

- Agentit **skill profiles** classify/install available skill packages.
- MCP **stacks** are named server sets the primary AI may choose.
- The current **session selection** is the exact subset of skills/MCPs actually justified now.

Neither a profile nor a stack auto-activates its members merely by existing.

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
- Do not use cleanup as an excuse to mutate unrelated/global MCP configuration.
- Track task-added enablement so the task can clean up only what it owns.

## Optional Google Ads reporting

`google-ads` registers Google's official [Google Ads MCP](https://github.com/googleads/google-ads-mcp) as a situational reporting server. It is excluded from the default developer stack. The reviewed source is pinned to `9a78cbdceebae71a6bc8483bdec333695834ef9c` (package version `0.0.5`); that version exposes only `customers_list_accessible_customers`, `metadata_get_resource_metadata` and `search_search`, with no campaign/budget mutation tools.

Install Python 3.10+ and [pipx](https://pipx.pypa.io/), then install the pinned server separately from enabling its client configuration:

```bash
pipx install 'git+https://github.com/googleads/google-ads-mcp.git@9a78cbdceebae71a6bc8483bdec333695834ef9c'
pipx runpip google-ads-mcp install 'fastmcp==4.0.6' 'mcp[cli]==2.0.0'
agentit mcp enable google-ads --providers codex --project /absolute/project
agentit mcp enable google-ads --providers codex --project /absolute/project --apply
```

The documented stdio setup was verified with FastMCP `4.0.6` and MCP SDK `2.0.0`; the second command pins those transport dependencies inside the isolated environment. The `google-ads-mcp` executable must be on the client's PATH. The catalog's `package` records the reviewed installation spec; enabling does not install the package or enforce the installed version. Recheck its tools before upgrading. Reload/reconnect Codex after registration and use `customers_list_accessible_customers` to verify authenticated access.

For local stdio authentication, follow the upstream ADC instructions: enable the Google Ads API in your Google Cloud project, create/download your own OAuth desktop client and authorize a user with access to the intended Ads accounts:

```bash
gcloud auth application-default login \
  --scopes https://www.googleapis.com/auth/adwords,https://www.googleapis.com/auth/cloud-platform \
  --client-id-file=/absolute/private/path/oauth-client.json
```

Keep OAuth files and ADC credentials outside Git. Standard ADC discovery uses the user's gcloud credentials directory; set `GOOGLE_APPLICATION_CREDENTIALS` only when using another supported credential file. If required by the API/account, provide `GOOGLE_ADS_DEVELOPER_TOKEN` through the client's process environment. `GOOGLE_ADS_LOGIN_CUSTOMER_ID` optionally selects a manager account, and can also be passed per tool call. `GOOGLE_CLOUD_PROJECT`/`GOOGLE_PROJECT_ID` are optional project settings. Codex's catalog adapter emits these **names** in `env_vars`; secret values are never copied into `config.toml`. Other clients use normal ADC discovery and their private environment/secret settings for optional values.

This catalog entry uses stdio. Do not supply `GOOGLE_ADS_MCP_OAUTH_CLIENT_ID` and `GOOGLE_ADS_MCP_OAUTH_CLIENT_SECRET` to it: upstream switches to an HTTP server when both exist. A shared OAuth HTTP service is a separate deployment and authentication decision. Google has no dedicated read-only Ads OAuth scope, so the read boundary comes from this pinned server's tools and the Google user's account permissions. Installation and tool discovery can pass before authenticated Ads queries work; report those outcomes separately.

To undo this setup, disable the entry with `agentit mcp disable google-ads --providers codex --project /absolute/project --apply`, then `pipx uninstall google-ads-mcp` if no other client uses the local executable. Provider config backups are created on apply.

## Optional ClickUp team tracking

ClickUp is available as the opt-in `clickup` server (named stack: `team_tracking`), not a global always-on tool. Its official remote MCP endpoint is `https://mcp.clickup.com/mcp` and authentication is performed by the client's OAuth flow, not by committing a token. For the human-identity, task-deduplication, privacy, status, and error-handling rules, see [ClickUp tracking](CLICKUP_TRACKING.md). On Codex, one supported setup path is `codex mcp add clickup --url https://mcp.clickup.com/mcp`, then `codex mcp login clickup` and a session reload when necessary. The alternative `agentit mcp enable clickup --providers codex --apply` writes the same remote server configuration (plan first if uncertain), but does not complete OAuth.
