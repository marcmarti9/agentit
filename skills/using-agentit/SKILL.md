---
name: using-agentit
description: Lightweight provider-neutral entry point for material agent work. Decide bare vs Agentit first; prefer Agentit when it materially improves reliability, then use domain packs only to discover and load the concrete skills/tools/references the primary AI decides are worth their context cost.
---

# Using Agentit

Agentit is a **provider/model-neutral** reliability/orchestration protocol for capable AI agents. It should improve a task **without filling the context window with its whole framework** or binding general workflows to one model vendor.

The active model owns semantic judgment. Programs remain mechanical: state, files, receipts, manifests, commands and other deterministic execution support.

## First-prompt dispatch

A fresh agent should make one semantic choice before loading the rest of Agentit:

```text
DISPATCH_DECISION: bare | agentit
```

### `bare`

Use bare execution only when Agentit would add no material value. Typical conditions:

- trivial/conversational answer;
- tiny obvious mechanical edit;
- negligible risk and blast radius;
- no useful domain skill/reference/tool/delegation decision;
- no meaningful continuity, multi-step orchestration or independent review need;
- verification is obvious and local.

Bare does **not** mean careless. System/user/project rules still apply.

### `agentit`

Use Agentit for material work: non-trivial implementation, debugging, design, research, source-sensitive/current domains, multi-step changes, ambiguous product decisions, tool/MCP decisions, high-risk work, long-running work, or anything where JIT expertise/review/verification materially improves the outcome.

**When genuinely uncertain between `bare` and `agentit`, prefer `agentit`.** The minimal bootstrap exists so the safer path does not require preloading the whole framework.

An explicit natural-language request to use Agentit always selects `agentit` unless impossible or conflicting with a higher-priority rule.

## Minimal bootstrap

A globally discoverable Agentit installation should expose only:

- `using-agentit` — this dispatcher/protocol;
- `task-router` — full semantic `TASK_DECISION` once Agentit is selected;
- `using-agent-skills` — semantic pack discovery and JIT skill projection.

Everything else is JIT.

Do **not** globally preload debugging, TDD, security, planning, code review, design, references, MCP fit, orchestration, long-horizon recovery or verification specialist skills. Load them only when the current task/stage actually needs them.

## Agentit path after dispatch

When `DISPATCH_DECISION=agentit`:

```text
inspect context
-> load task-router + using-agent-skills
-> TASK_DECISION
-> inspect relevant semantic pack(s)
-> primary AI chooses any justified skill subset
-> choose references/tools only if material
-> choose compatible model endpoint(s) only if model routing itself matters
-> cheap independent audit
-> strong review if risk/disagreement requires it
-> execute through Loop/Graph contracts
-> fresh verification
-> durable docs/state where warranted
-> PR-first for repository changes
```

The user should not need to know or type Agentit CLI commands. Mechanical commands are agent-facing implementation details.

## Provider/model-neutral invariant

General Agentit behavior must not depend on Claude, Codex, Gemini, Kimi, or any other named model/provider.

A compatible model can use Agentit when it can:

- receive/read the relevant Agentit instructions/skill bodies;
- access the context and files required by the task;
- use the required tools/modalities when the task needs them;
- obey the applicable permissions/safety boundaries;
- produce evidence that satisfies the verifier.

Named providers/models are valid in **provider-specific adapters, endpoint configuration, current evaluation evidence, or provenance**. They are not valid as hidden requirements inside a general skill merely because the source article used that model.

When a source teaches a useful workflow with one named model, extract the workflow and keep the model-specific wording only as provenance unless the technique genuinely relies on a provider-specific capability.

When model selection itself matters, inspect the `models` pack and use `local-model-routing` JIT. Despite the legacy skill ID, that procedure compares compatible **local or remote** endpoints and routes by task evidence rather than brand.

## Packs: maps, not levels

Canonical runtime map: `skills/using-agent-skills/references/packs.md`.

Packs such as `engineering`, `frontend`, `design`, `backend`, `data`, `product`, `marketing`, `seo`, `research`, `writing`, `models`, `release`, and `agency` exist to answer:

> **What capabilities/skills live around this domain, and when might each one help?**

They do **not** answer:

- how many skills must be loaded;
- which skill must come first;
- what “level” the task belongs to;
- whether every skill in the pack should be used.

There are no pack tiers such as `essential / standard / deep` and no fixed minimum/maximum skill count.

The primary AI may select zero, one, or many skills from one or more packs. It should select only skills it can justify for the current stage.

Example:

```text
packs:
- design
- frontend
selected_skills:
- design-inspiration-research
- browser-testing-with-devtools
```

Another design task might legitimately select six skills; a small one might select one. **The agent decides.**

## `TASK_DECISION`

After Agentit activation, the primary AI uses `task-router` and decides at least:

```text
intent / outcome
known facts / material unknowns
relevant pack(s)
complexity
risk / reversibility / external effects
selected skills
selected tools
reference_plan
execution topology / workers
plan
verification
safety / rollback / post-check
user-method assessment
```

Semantic ownership stays with the primary AI. No Python/regex/keyword router decides what the task means, which pack applies, how many skills to load, which skill is relevant, which model is universally best, or which source should be trusted.

## References are JIT

`reference-intelligence` is deliberately **not** part of the global core.

If `TASK_DECISION.reference_plan.mode != none`, load it JIT and inspect the smallest useful curated/live source set.

Examples:

- trivial rename -> no references;
- web design -> relevant design/production references + current implementation docs where material;
- SEO -> SEO/growth references + live search/platform evidence;
- current Spanish tax report -> current authoritative tax/legal sources, regardless of whether Agentit already has a tax pack.

The absence of curated Agentit material is never permission to rely on stale model memory for a current/domain-specific claim.

## Tools/MCPs are JIT

`mcp-tooling-fit` and external tools are selected only when they materially improve the reviewed plan. Keep least privilege and verify current setup/auth before depending on changing external services.

## Independent audit

For material Agentit work, the reviewed `TASK_DECISION` gets a bounded read-only second opinion from the cheapest competent independent model, normally semantic tier `fast`.

The auditor is a critic, not the router or implementation owner. It looks for misunderstood intent, wrong/missing packs, unjustified or missing skills, context bloat, risk underestimation, weak verification, unsafe effects, bad reference/source choices, model-routing assumptions when material, and unnecessary or missing delegation.

Use `task-router/references/economy-reviewer.md` for the detailed contract.

Escalate to a stronger independent critic/judgment model for `RISK_3/RISK_4`, destructive/irreversible work, auth/payments/secrets/PII/production, large structural plans, or unresolved material disagreement.

## Worker projection

Spawn specialists only when isolation, expertise, independent judgment, breadth or parallelism provides a concrete benefit.

A worker receives bounded context:

```text
role/objective
relevant pack(s) as discovery labels
selected skill bodies
selected references if any
project constraints
allowed tools/permissions
read/write ownership
expected handoff
verification / stop condition
```

Never dump the global catalog or whole pack into a worker. One writer owns shared files/state unless branch/worktree isolation makes parallel writes safe.

The worker contract is provider-neutral. Provider-specific worker spawning mechanics may differ, but that must not change the semantic role, bounded context, ownership or verification contract.

## Runtime enforcement

Agentit's Loop/Graph runtime enforces the AI's reviewed execution plan; it does not interpret prompts.

For executable work with a verifiable outcome:

- define observable goal;
- define verifier;
- define stop condition;
- bound retries;
- define escalation;
- require fresh evidence before success.

Multi-node work additionally defines dependencies, handoffs and write ownership through a Graph Contract.

Do not weaken a verifier to manufacture a green receipt.

## Continuity and durable docs

Use `docs/agentit/STATE.md` (or an existing project equivalent) for substantial/resumable work. Keep it compact: objective, constraints, decisions, status, branch/PR, latest verification, blockers and next steps.

For substantial repository changes, keep canonical Markdown documentation aligned with changed architecture/components/contracts/operations/troubleshooting. Do not create duplicate docs when an existing source of truth should be updated.

Do not persist secrets, full transcripts or private chain-of-thought.

## Constructive dissent

Agentit optimizes for the user's actual goal, not agreement with every proposed method.

If the user's suggested implementation is materially weaker than a realistic alternative, explain the concrete trade-off and recommend the better path. Preserve the user's final safe discretionary choice; do not use disagreement as permission for scope expansion or unauthorized changes.

## Git / completion

Repository changes default to:

```text
work branch -> implementation -> fresh verification -> PR -> user/reviewer merge decision
```

No `done`, `fixed`, `passing`, `premium`, `secure` or equivalent claim without fresh evidence appropriate to that claim.

## Core invariant

> **Keep the bootstrap tiny. Keep general Agentit model-neutral. Prefer Agentit for material work. Packs expose options; the primary AI decides the actual skill set and its size.**
