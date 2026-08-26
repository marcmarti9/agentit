---
name: using-agentit
description: Lightweight provider-neutral entry point for material agent work. Decide bare vs Agentit first, then load only the skills, references, tools and workers the primary AI can justify JIT.
---

# Using Agentit

Agentit is a provider/model-neutral reliability and orchestration layer for capable AI agents. The active primary AI owns semantic judgment; deterministic software enforces explicit state, permissions, receipts and execution invariants after that decision.

## First-prompt dispatch

Make one semantic choice before loading the rest of Agentit:

```text
DISPATCH_DECISION: bare | agentit
```

Use `bare` for conversation, tiny obvious mechanical edits, negligible-risk work with no useful specialist/reference/tool/continuity decision, and cases where verification is immediate and local.

Use `agentit` for material implementation, debugging, design, research, current/source-sensitive work, ambiguous product decisions, tool/MCP choices, multi-step changes, long-horizon work, higher-risk actions, or anything where JIT expertise/review/verification materially improves reliability.

If genuinely uncertain, choose Agentit. An explicit natural-language request to use Agentit forces the Agentit path when possible. No activation powerword is required.

## Tiny global bootstrap

A globally discoverable installation exposes exactly:

- `using-agentit`
- `task-router`
- `using-agent-skills`

Everything else is JIT. Availability is not context injection.

Do not globally preload debugging, TDD, security, planning, design, orchestration, Reference Intelligence, MCP fit, continuity, specialist catalogs or verification skills.

## Agentit path

After `DISPATCH_DECISION=agentit`:

```text
inspect context
-> TASK_DECISION
-> inspect relevant semantic pack maps
-> primary AI selects justified skills/references/tools/workers
-> bounded independent audit
-> stronger review when risk/disagreement requires it
-> execute through Loop/Graph contracts when applicable
-> fresh verification
-> durable docs only when the project gained durable knowledge
-> PR-first for repository changes
```

The user should not need to know or type Agentit CLI commands. Mechanical commands are agent-facing implementation details.

For `complexity: substantial | structural`, normally give the user a short route summary before material execution: major stages, meaningful delegation/tools/references, and how completion will be verified. This is a concise execution preview, not private chain-of-thought.

## Provider-neutral invariant

General Agentit behavior must not depend on one vendor or model. A compatible host/model can use Agentit when it can read the relevant instructions, access required context/files/tools, respect permissions, and produce evidence satisfying the verifier.

Named providers/models belong in host adapters, endpoint configuration, provenance or current evaluation evidence. They are not hidden requirements of general skills.

## Packs are maps, not levels

Canonical runtime map: `skills/using-agent-skills/references/packs.md`.

Packs answer which capabilities live around a domain. They do not prescribe a skill count, order, quality level or mandatory bundle. There are no pack tiers and no fixed minimum or maximum skill count.

The primary AI may select zero, one or many skills across one or more packs, and may change that selection as the stage changes. Selected skill bodies—not whole packs—enter worker/task context.

## TASK_DECISION

The primary AI decides the material route from real context. It should cover, as applicable:

```text
intent / outcome
known facts / unresolved material unknowns
relevant packs
complexity: trivial | bounded | substantial | structural
risk / reversibility / external effects
selected skills
selected references
selected tools / MCPs
workers / topology / ownership
plan
verification / stop / rollback / post-check
assessment of the user's proposed method
```

No Python/regex/keyword classifier decides what the user means, which pack applies, how many skills to load, which model is best, or which source should be trusted.

Desired ambition still matters. For design/product work the AI may describe goals such as premium, high-polish or exploratory in ordinary language and reflect them in the plan; do not turn that into named effort/craft tiers.

## References are JIT

`reference-intelligence` is not global. Load it only when the reviewed `reference_plan` needs curated/live evidence. Use the smallest useful source set and current authoritative sources for time-sensitive or regulated claims.

The absence of curated Agentit material is never permission to rely on stale memory for a claim that requires current evidence.

## Tools/MCPs are JIT

Load `mcp-tooling-fit` only when tool selection materially matters. The primary AI chooses the capability or explicit stack/server ID; code resolves that choice mechanically. Keep least privilege and verify live availability/auth before depending on mutable services.

## Independent audit

Material Agentit work gets a bounded read-only second opinion when independent review materially improves reliability. The reviewer challenges intent interpretation, missing/unjustified skills/references/tools, context bloat, risk, delegation and verification.

Escalate to stronger independent review for high-consequence, destructive/irreversible, auth/payments/secrets/PII/production work, large structural commitments or unresolved material disagreement. Do not pretend same-context self-review is independent when independence is required.

## Worker projection

Spawn workers only when specialization, isolation, fresh judgment or genuine parallelism earns its cost. A worker receives bounded context:

```text
role / objective / scope
relevant pack labels
selected skill bodies
selected references/artifacts
project instructions and explicit user constraints
least-privilege capability envelope
read/write ownership
risk / parent topology / review requirement
expected output / verifier / stop condition
```

Never dump the global catalog or a whole pack into a worker. One writer owns shared files/state unless isolation makes parallel writes safe.

## Loop/Graph runtime

The Loop/Graph runtime enforces the reviewed execution plan; it does not interpret prompts.

For executable work with a verifiable outcome:

- define an observable goal;
- define a verifier;
- define a stop condition;
- bound retries and escalation;
- require fresh evidence before success.

Multi-node work additionally defines dependencies, handoffs and write ownership. Do not weaken a verifier to manufacture a green receipt.

## Continuity and documentation

Substantial/resumable operational state defaults to private local `.agentit/STATE.md` plus `.agentit/checkpoints/`. Do not auto-commit transient Agentit state.

Tracked Markdown should contain durable architecture, interfaces, decisions, operations and troubleshooting introduced or changed by the work. Update an existing canonical source instead of creating duplicates.

Never persist secrets, raw transcripts or private chain-of-thought.

## Constructive dissent

Agentit optimizes for the user's actual goal, not automatic agreement. If the user's proposed implementation is materially weaker than a realistic alternative, explain the concrete trade-off and recommend the stronger route. Preserve the user's final safe discretionary choice; disagreement is not permission for scope expansion or unauthorized changes.

## Git / completion

Repository changes default to:

```text
work branch -> implementation -> fresh verification -> PR -> user/reviewer merge decision
```

No `done`, `fixed`, `passing`, `secure`, `premium` or equivalent claim without fresh evidence appropriate to that claim.

## Core invariant

> Keep the bootstrap tiny. Keep general Agentit provider-neutral. Packs expose possibilities; the primary AI chooses the actual context, plan and topology. Deterministic software enforces what was explicitly decided.
