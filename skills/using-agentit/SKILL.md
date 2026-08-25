---
name: using-agentit
description: Lightweight default entry point for material agent work. Decide bare vs Agentit first; prefer Agentit when it materially improves reliability, then load task-router, one domain pack/depth and only the concrete skills/tools/references needed JIT.
---

# Using Agentit

Agentit is a reliability/orchestration protocol for capable AI agents. It should improve a task **without filling the context window with its whole framework**.

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

**When genuinely uncertain between `bare` and `agentit`, prefer `agentit`.** The point of the minimal bootstrap is to make Agentit cheap enough that the safer choice does not require loading 20 skills.

An explicit natural-language request to use Agentit always selects `agentit` unless impossible or conflicting with a higher-priority rule.

## Minimal bootstrap

A globally discoverable Agentit installation should expose only the minimum navigation skills:

- `using-agentit` — this dispatcher/protocol;
- `task-router` — full semantic `TASK_DECISION` once Agentit is selected;
- `using-agent-skills` — pack/depth discovery and JIT skill projection.

Everything else is JIT.

In particular, do **not** globally preload debugging, TDD, security, planning, code review, design, references, MCP fit, orchestration, long-horizon recovery or verification specialist skills. Load them only when the task/stage needs them.

## Agentit path after dispatch

When `DISPATCH_DECISION=agentit`:

```text
inspect context
-> load task-router + using-agent-skills
-> TASK_DECISION
-> choose pack + depth
-> choose smallest concrete skill set
-> choose references/tools only if material
-> cheap independent audit
-> strong review if risk/disagreement requires it
-> execute through Loop/Graph contracts
-> fresh verification
-> durable docs/state where warranted
-> PR-first for repository changes
```

The user should not need to know or type Agentit CLI commands. Mechanical commands are agent-facing implementation details.

## Pack + depth selection

Canonical runtime map: `skills/using-agent-skills/references/packs.md`.

Choose a primary semantic pack for the current stage, for example:

- engineering;
- frontend;
- design;
- backend;
- data;
- product;
- marketing;
- seo;
- research;
- writing;
- release;
- agency overlay.

Then choose depth:

- `essential` — minimum useful domain process;
- `standard` — normal production candidate pool;
- `deep` — advanced/high-risk/high-craft/niche candidate pool.

**A pack/depth is a discovery scope, not a context bundle.** Never inject every skill in the pack. Select only the concrete bodies needed by the current stage/worker.

Example:

```text
pack: design
depth: deep
selected_skills:
  - design-inspiration-research
  - scrollytelling-web
  - browser-testing-with-devtools
```

That worker gets those skills, not the entire design catalog.

## `TASK_DECISION`

After Agentit activation, the primary AI uses `task-router` and decides at least:

```text
intent / outcome
known facts / material unknowns
pack + depth
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

Semantic ownership stays with the primary AI. No Python/regex/keyword router decides what the task means, which pack applies, which skill is relevant, or which source should be trusted.

## References are JIT

`reference-intelligence` is deliberately **not** part of the global core.

If `TASK_DECISION.reference_plan.mode != none`, load it JIT and then inspect the smallest useful curated/live source set.

Examples:

- trivial rename -> no references;
- web design -> relevant design/production references + current implementation docs where material;
- SEO -> SEO/growth references + live search/platform evidence;
- current Spanish tax report -> current authoritative tax/legal sources, regardless of whether Agentit already has a tax pack.

The absence of a curated pack is never permission to rely on stale model memory for a current/domain-specific claim.

## Tools/MCPs are JIT

`mcp-tooling-fit` and external tools are selected only when they materially improve the reviewed plan. Keep least privilege and verify current setup/auth before depending on changing external services.

## Independent audit

For material Agentit work, the reviewed `TASK_DECISION` gets a bounded read-only second opinion from the cheapest competent independent model, normally semantic tier `fast`.

The auditor is a critic, not the router or implementation owner. It looks for misunderstood intent, wrong pack/depth, skill/context overload, missing expertise, risk underestimation, weak verification, unsafe effects, bad reference/source choices, and unnecessary or missing delegation.

Use `task-router/references/economy-reviewer.md` for the detailed contract.

Escalate to a stronger independent critic/judgment model for `RISK_3/RISK_4`, destructive/irreversible work, auth/payments/secrets/PII/production, large structural plans, or unresolved material disagreement.

## Worker projection

Spawn specialists only when isolation, expertise, independent judgment, breadth or parallelism provides a concrete benefit.

A worker receives bounded context:

```text
role/objective
pack + depth
selected skill bodies
selected references if any
project constraints
allowed tools/permissions
read/write ownership
expected handoff
verification / stop condition
```

Never dump the global catalog or whole pack into every worker. One writer owns shared files/state unless branch/worktree isolation makes parallel writes safe.

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

> **Keep the bootstrap tiny. Prefer Agentit for material work. Load domain knowledge, references, tools and specialists only when the task earns their token cost.**
