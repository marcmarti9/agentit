# Agentit interview, domain packs, craft depth, and provider-neutral execution

Agentit owns the work protocol. Providers own only the execution primitive.

## 1. Product work interviews by default

Any task that creates or changes product behavior or a meaningful implementation decision must pass `interview-me` before planning or implementation.

Mechanical bypass only for exact chores with no product decision.

## 2. Batch every currently identifiable material question

After inspecting facts, ask **all material user decisions** in one numbered batch with recommendations. Follow-up only for genuinely new decisions.

## 3. Domain packs replace universal Studio tax

Machine catalog: `effort/levels.yaml` + `profiles.yaml`.

The agent recommends a **domain pack** (skill family): engineering, frontend, design, backend, data, product, writing, release, research, or a user role.

Load only always_core + that family’s task skills. Never load the design studio stack for pure backend work.

## 4. Craft depth is design/visual only

Standard / Polished / Studio apply **only** when the task is visual/design craft.

They do **not** gate ordinary APIs, infra, pure logic, or docs.

Optional soft spend for non-design: lean / normal / thorough (thoroughness, not multi-agent quotas).

## 5. Project-aware token estimates

Do not present fixed 15k–80k / 50k–250k / 150k–800k tables as authoritative bills.

Use router `token_estimate` (risk, complexity, domain, topology, specialists/critic, craft depth, project signals). Always label as rough.

## 6. No powerwords

Only natural Agentit activation in the user’s language is special. Task routing uses ordinary language. Multi-agent requests may be declined with reason if they lack independence.

## 7. Intelligent delegation and critic

- Spawn specialists when beneficial; no hard min/max caps.
- Large structural plans require an independent critic before implementation commitment.
- Multi-agent execution is an optimization, never a correctness dependency.

## 8. Continuity

Chat is disposable. Persist `docs/agentit/STATE.md` (or equivalent) per `docs/PROJECT_CONTINUITY.md`.

Include domain pack, craft depth if any, spend, token estimate, critic/specialist plan, branch/PR, verification, next actions.

## 9. PR-first

`work branch → commits → verification → PR → user merge` unless explicitly overridden for that task.

## 10. Provider-neutral specialist contract

Catalog roles are logical bundles. Fallback: native subagent → isolated call → fresh context → parent + same skills.

## 11. MCP fit

Use `mcp-tooling-fit` and `agentit mcp` to inventory, enable/disable, and discover servers (catalog + marketplace + web). Installs plan-first with user approval; RISK_3+ needs force/consent.

## 12. Cross-provider compatibility

Shared policy describes semantic capabilities for OpenAI, Anthropic, Google, xAI, and compatible clients — not one vendor’s API.

## 13. Non-interactive execution

Do not fake interviews. Block rather than guess unresolved product decisions or craft depth when design work needs it.
