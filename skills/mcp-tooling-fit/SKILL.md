---
name: mcp-tooling-fit
description: Audit installed MCPs, fit them to the project, disable unused ones, and discover useful servers from the Agentit catalog, marketplaces, and the web. Use at session start for non-trivial projects or when tooling gaps appear.
---

# MCP Tooling Fit

Choose the right MCP servers for **this project**, not a default kitchen sink. Prefer least privilege. Plan before applying. Never write secrets into the repo.

## When to use

- After Agentit activation on a real codebase
- When the task needs docs, browser, GitHub, DB, design, or search tools
- When many MCPs are enabled but unused (context and permission noise)
- When the user asks what tools should be connected

## Protocol

### 1. Inventory what is already there

```bash
agentit mcp status --project .
agentit mcp available --project .
agentit mcp active --project .
```

Or via agentit-manager MCP tools: `mcp_status`, `mcp_list_available`, `mcp_list_active`.

Record:

- enabled vs available
- risk tier of each server
- whether secrets/env vars are required

### 2. Infer project needs from facts

Inspect the repo (not the user) for stack signals:

- package manifests, lockfiles, frameworks
- DB / Supabase / Docker / CI
- design sources (Figma links, design tokens)
- browser/UI surfaces
- external SaaS (Linear, Slack, Notion)

Map needs to Agentit stacks when possible:

| Need | Stack / servers |
|---|---|
| coding baseline | `developer_core` (agentit-manager, context7, github, playwright) |
| frontend/UI verify | `frontend` / playwright, chrome-devtools, figma |
| design craft | `design_studio` |
| data/schema | `backend_data` (staging/read-only creds only) |
| research | `research` |
| product ops | `product_ops` |

### 3. Fit: enable useful, disable noise

Propose a minimal set:

1. keep or enable servers that unblock the current domain pack
2. disable servers that are unrelated and always-on without benefit
3. never enable RISK_3/RISK_4 without explicit user force/consent

```bash
# plan first (no --apply)
agentit mcp enable-stack developer_core --project .
agentit mcp disable <unused-id> --project .

# apply only after user OK (or clear standing policy)
agentit mcp enable context7 --project . --apply
agentit mcp disable <unused-id> --project . --apply
```

### 4. Discover gaps beyond the local catalog

If the project needs a capability not covered:

1. Search the Agentit curated catalog (`mcp/catalog.yaml` / `agentit mcp available`)
2. Search skill/MCP marketplaces and the open web for maintained servers (prefer official vendors)
3. Check install count, repo activity, trust, required scopes, and secret handling
4. Present 1–3 candidates with: purpose, risk, trust, install command, secrets needed

Do **not** silently install from the internet. Always:

- dry-run / plan first
- ask the user before `--apply`
- refuse or escalate for high-risk write-capable tools without clear need

### 5. Persist the decision

Write compact notes into project continuity (`docs/agentit/STATE.md` or equivalent):

- enabled MCP set for this project
- why each is needed
- disabled-as-noise list
- pending installs awaiting user approval

## Output contract

```text
MCP FIT
Project needs: ...
Keep/enable: ...
Disable: ...
Gaps / candidates: ...
Apply plan: (commands)
User approval required: yes/no
Risk notes: ...
```

## Safety

- Secrets only via env vars / provider secret stores — never committed
- Prefer read-only and official servers
- RISK_3+ needs `--force` and human confirmation
- Disabling a server mid-session is fine; re-enable when a later task needs it

## Anti-patterns

- enabling every popular MCP “just in case”
- installing unknown GitHub MCP servers without review
- treating catalog absence as “cannot help” without a short marketplace/web check
- asking the user for stack facts already visible in the repo
- powerwords or secret jargon — ordinary “what tools do we need?” is enough

## Verification

- [ ] `agentit mcp status` inspected
- [ ] recommendations match repo facts + current domain pack
- [ ] unused always-on servers proposed for disable
- [ ] external installs are plan-first with user approval
- [ ] continuity notes updated when the MCP set changes
