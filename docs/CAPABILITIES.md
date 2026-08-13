# Provider-neutral capabilities

Agentit routes stable capability IDs instead of binding semantic specialists to
ChatGPT apps, MCP servers, or local tools.

```text
task -> semantic specialist -> required/preferred capabilities
     -> explicit host inventory -> ordered provider binding
     -> least-privilege capability envelope
```

The capability catalog is [`capabilities/catalog.yaml`](../capabilities/catalog.yaml).
Specialist requirements live beside the existing skill bundles in
[`agents/catalog.yaml`](../agents/catalog.yaml). The deterministic resolver is
[`router/capabilities.py`](../router/capabilities.py).

## Availability is explicit

Catalog presence is not runtime availability. Agentit does not assume that an app
is installed, authenticated, workspace-enabled, callable from the current host, or
authorized for the current task.

The host supplies an inventory of provider IDs that are callable **and authorized**
in the current session. Omitting inventory produces `inventory_required`, not a
false unavailable result and not a grant.

```bash
./agentit capabilities resolve \
  --specialist frontend-developer \
  --host codex \
  --available mcp.github,local.filesystem,mcp.playwright
```

The same inventory can be passed to routing:

```bash
./agentit route "Implement a responsive React interface" \
  --host codex \
  --available mcp.github,local.filesystem,mcp.playwright \
  --format json
```

Useful inspection commands:

```bash
./agentit capabilities list
./agentit capabilities show repository.read
./agentit capabilities resolve \
  --required repository.read \
  --preferred design.inspect \
  --host chatgpt \
  --available chatgpt.github,chatgpt.figma
```

These commands only plan. They do not install apps, enable MCP servers, authenticate,
or execute provider actions.

## Fallbacks

Each capability has an ordered `implementations` list. The resolver selects the
first provider that is both host-compatible and present in the explicit inventory.
Every candidate remains in `resolution.<capability>.candidates` with an explanation:

- `host_incompatible`
- `provider_unavailable`
- `selected`
- `higher_priority_selected`
- `inventory_not_provided`

For example, `repository.read` can prefer the GitHub ChatGPT app on ChatGPT, use
GitHub MCP on coding hosts, then fall back to `git` or a scoped local filesystem.

## Least-privilege envelopes

A resolved grant contains only:

- the requested capability;
- the one selected provider binding;
- the permissions needed for that binding;
- whether the capability was required or preferred.

Delegated worker contexts include this envelope. When an explicit inventory cannot
resolve a required capability, `validate_for_spawn()` fails closed. Preferred gaps
degrade the plan but do not block it. When inventory is omitted,
`validate_for_spawn()` rejects execution until host inventory is supplied; planning
and prompt projection may continue without grants.

The envelope is a runtime contract. A host adapter must enforce it when exposing
tools to a worker. It cannot retroactively narrow credentials or tools that a host
has already exposed with broader privileges.

## Add a capability or provider

1. Add a provider under `providers` with `kind`, display `name`, and compatible
   `hosts`. Do not add credentials or machine-specific paths.
2. Add or update a stable capability ID with ordered provider implementations and
   capability-scoped permissions.
3. Declare the capability as `required` or `preferred` on relevant specialists.
4. Add resolver tests for host compatibility, fallback order, missing required
   behavior, and least-privilege permissions.

Provider IDs may change or grow without changing specialist contracts. A specialist
must never declare `chatgpt.*`, `mcp.*`, `cli.*`, or `local.*` as a capability.
