---
name: task-router
description: Compact AI-native decision protocol used after Agentit dispatch. The primary model chooses pack/depth, JIT skills/tools/references, risk and topology; cheap AI audits and strong AI arbitrates high-risk or unresolved disagreement.
---

# AI-native task decision protocol

This skill runs **after** `using-agentit` has selected `DISPATCH_DECISION=agentit`.

Agentit has no programmatic semantic router. Do not use Python, regexes, keyword tables, scoring code or a cheap model to decide what the request means. The active primary model owns semantic interpretation because it has the richest task/project context.

## Inspect first

Use materially available context before deciding or asking:

- exact request and prior conversation;
- repository/project state and local instructions;
- relevant files/docs already inspected;
- tools/capabilities actually available;
- current deployment/environment state;
- unresolved assumptions.

Anything quickly discoverable from the project should normally be inspected instead of turned into a user question.

## `TASK_DECISION`

Before material execution, decide at least:

```text
intent / desired outcome
known_facts
material_unknowns
pack
pack_depth: essential | standard | deep
complexity: trivial | bounded | substantial | structural
risk: RISK_0..RISK_4
reversibility / external_effects
selected_skills
selected_tools
reference_plan
execution_topology
workers / ownership / parallelism
plan
verification
safety / rollback / post-check
user_method_assessment
```

### Pack + depth

Read `skills/using-agent-skills/references/packs.md` only when pack discovery detail is needed.

The pack is the domain search scope. The depth expands the **candidate pool**, never the automatic context payload.

Prefer one primary pack per stage. Add a secondary pack only for a real cross-domain need.

Select the smallest concrete skill set that materially improves the stage. Do not load every skill up to the chosen depth.

Examples:

```text
pack: engineering
pack_depth: essential
selected_skills:
- debugging-and-error-recovery
```

```text
pack: design
pack_depth: deep
selected_skills:
- design-inspiration-research
- scrollytelling-web
- browser-testing-with-devtools
```

A `deep` task with three selected skills is healthier than a `standard` task that dumps twelve bodies into context.

## Reference plan

Decide:

```text
reference_plan.mode: none | curated | live | both
```

Use `none` when external/current knowledge would not materially improve correctness or quality.

Use `curated` for relevant Agentit/project reference material, `live` for current/domain-specific authoritative sources, and `both` when each contributes something distinct.

If mode is not `none`, load `reference-intelligence` JIT. It is intentionally not part of the global core.

The absence of a curated pack is not permission to use stale model memory for current tax/legal/API/regulatory/platform facts.

Do not research for ceremony and do not load irrelevant references merely because Agentit has them.

## Tools

Choose tools/MCPs only after the semantic task/pack decision. Load `mcp-tooling-fit` JIT when tool selection itself needs judgment. Prefer least privilege and current verified setup.

## Risk

- `RISK_0` — read-only explanation/inspection with no meaningful mutation.
- `RISK_1` — tiny clearly reversible local mutation.
- `RISK_2` — meaningful but bounded implementation/product change.
- `RISK_3` — auth/security/payments/secrets/PII/significant data/infrastructure/external side effects.
- `RISK_4` — destructive production action, plausible data loss, irreversible/high-blast-radius operation.

Confidence never lowers the actual risk floor.

## Topology

- `direct` — one owner; delegation adds no real value.
- `probe` — investigate first, then decide.
- `fan_out` — independent branches benefit from isolation/parallelism.
- `pipeline` — dependent stages with explicit handoffs.
- `writer_reviewer` — one implementation owner + independent review.
- `audit` — inspection/critique is the task.

Do not force agents for show. Do not avoid useful delegation just because the primary model is strong.

## Constructive dissent

Separate the user's desired outcome from a suggested implementation method.

If a realistic alternative is materially better for correctness, simplicity, cost, maintenance, security, UX, performance or reversibility:

1. explain the concrete issue;
2. recommend the alternative;
3. compare the material trade-off;
4. preserve the user's final safe discretionary choice.

Do not manufacture disagreement for personality.

## Cheap independent audit

Before material execution, give the proposed `TASK_DECISION` to the cheapest competent independent read-only model, normally semantic tier `fast`.

Use `references/economy-reviewer.md` for the detailed contract.

The auditor should challenge:

- misunderstood intent or hidden constraints;
- risk classified too low;
- wrong pack or unjustified depth;
- too many or too few selected skills;
- full-pack/context dumping;
- missing relevant references or unnecessary reference overload;
- stale/current-source mistakes or creator claims promoted to facts;
- wrong/excessive tools or permissions;
- unnecessary/missing delegation;
- unsafe write ownership;
- weak verification/rollback;
- uncritical acceptance of a materially worse proposed method.

Expected result:

```text
AUDIT: CLEAR | CHALLENGE | ESCALATE
FINDINGS:
- ...
SUGGESTED_CHECKS:
- ...
CONFIDENCE: low | medium | high
```

`CHALLENGE` makes the primary reconsider; it does not transfer decision ownership. If material disagreement remains, escalate.

## Strong review

Use an independent `critic`/`judgment` tier before execution for:

- `RISK_3/RISK_4`;
- destructive/difficult rollback work;
- auth/payments/secrets/PII/production;
- large structural architecture/product commitments;
- an auditor `ESCALATE`;
- unresolved material disagreement.

Require backup/rollback/post-check where relevant; use preview/dry-run for `RISK_4` when technically meaningful.

## Worker context

When spawning, project only bounded task context plus:

```text
role/objective
pack + depth
selected skill bodies
selected references if any
allowed tools/permissions
read/write ownership
expected handoff
verification / stop condition
```

The parent keeps broader context and integration responsibility.

## Mechanical boundary

Programs may resolve explicit IDs, copy files, manage state/manifests, run tests and enforce Loop/Graph contracts. They must not infer semantic pack/skill/reference/tool choices from natural-language task text.

> **Primary AI decides; cheap AI audits; strong AI arbitrates when warranted; software performs the reviewed mechanical plan.**
