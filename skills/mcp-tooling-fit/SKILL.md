---
name: mcp-tooling-fit
description: Select the smallest useful MCP/tool set for the current Agentit task, based on repository facts, explicit capability needs, least privilege, and current availability.
---

# MCP Tooling Fit

Choose tools for the reviewed task, not because they are popular or globally installed. The primary AI owns the semantic choice; deterministic code may resolve an explicit server/stack ID and enforce risk gates.

## When to use

Load this skill JIT when the task materially depends on MCP/tool selection, when the current tool inventory is noisy, or when an important capability appears missing.

Do not load it for ordinary work whose existing tools are already sufficient.

## Protocol

### 1. Inspect current state

Agent-facing helpers include:

```bash
agentit mcp status --project .
agentit mcp available --project .
agentit mcp active --project .
```

The agentit-manager MCP can expose the equivalent inventory/enable/disable operations.

Record only what matters for the current task:

- explicit current availability;
- required permissions/capabilities;
- write vs read-only behavior;
- secrets/env requirements;
- risk classification.

Catalog presence is not runtime availability.

### 2. Infer needs from task and repository facts

Inspect manifests, frameworks, DB/config, browser/UI surfaces, design sources, CI/deployment and external integrations. Do not ask the user for facts already visible in the project.

Example curated stacks may include:

| Need | Candidate stack |
|---|---|
| repository/docs/browser baseline | `developer_core` |
| frontend/browser verification | `frontend` |
| design inspection | `design_studio` |
| backend/data work | `backend_data` |
| current-source research | `research` |
| product operations | `product_ops` |

These names are discovery conveniences, not semantic routing rules. The primary AI decides whether a stack actually fits.

### 3. Prefer the minimum useful set

Keep or enable only tools that earn their permission/context/coordination cost. Disable unrelated always-on noise when doing so is safe and useful.

Plan mutations before applying them. Higher-risk write-capable tools require the applicable human/review gate.

### 4. Discover gaps when necessary

If Agentit's catalog does not cover a required capability:

1. prefer official/maintained providers;
2. check source, maintenance, scopes and secret handling;
3. compare a small number of realistic candidates;
4. do not silently install or authorize external software.

Current-source discovery belongs in the task's reference/tool plan, not in a permanent global preload.

### 5. Persist only operationally useful state

When a substantial task needs continuity, record the selected MCP/tool set and pending approvals in local `.agentit/STATE.md`. Do not publish transient tool enablement decisions as tracked project documentation unless they are a durable architectural/operational contract.

## Safety

- least privilege by default;
- secrets through environment/provider secret stores, never repository files;
- verify current auth/availability before depending on a mutable external service;
- RISK_3/RISK_4 or destructive external actions require the applicable human and independent-review gate;
- disabling/re-enabling tools is allowed when reversible and authorized.

## Anti-patterns

- enabling every MCP "just in case";
- treating a stack name as a natural-language router;
- assuming catalog presence means authenticated availability;
- silently installing third-party servers;
- asking for stack facts that the repository exposes;
- writing secrets or mutable tool state into public docs;
- using powerwords to activate tooling.

## Verification

- [ ] current inventory was inspected when material;
- [ ] selected tools map to explicit task capabilities;
- [ ] unnecessary permission/context noise was avoided;
- [ ] external installs/actions respected risk and consent gates;
- [ ] substantial continuity notes, if needed, remain in `.agentit/STATE.md` by default.
