---
name: using-agentit
description: Activate Agentit end-to-end. The primary AI decides from full context, a cheap independent AI reviews the decision, then Agentit interviews, loads real skills, delegates intelligently, verifies, and ships PR-first.
---

# Using Agentit

Agentit is an operating protocol for capable AI agents. It is not a natural-language classifier implemented in code.

The primary model owns context recovery, task interpretation, planning, skill/tool selection, delegation, integration and verification. A second model checks the proposed decision before material execution.

## Activation

Natural language that means use/usa/utilise Agentit activates this playbook for the session. No other powerwords are required.

## Stable harness locations

- harness root: `~/code/agentit` when using the normal checkout;
- decision protocol: `~/code/agentit/skills/task-router/SKILL.md`;
- economy reviewer contract: `~/code/agentit/skills/task-router/references/economy-reviewer.md`;
- skills: `~/code/agentit/skills/<id>/SKILL.md`;
- runtime CLI: `~/code/agentit/router/runtime_cli.py` for mechanical Loop/Graph state only;
- specialist catalog: `~/code/agentit/agents/catalog.yaml`;
- profiles: `~/code/agentit/profiles.yaml`;
- continuity: `<project>/docs/agentit/STATE.md`.

There is intentionally no semantic `route.py` or programmatic decision contract. Mechanical utilities may manage files/state/tests, but they do not interpret user intent.

## Core protocol

1. **Inspect context.** Recover relevant conversation, repository, files, project rules, tools and current state before asking the user to repeat information.
2. **Decide with the primary AI.** Apply `task-router` and form `TASK_DECISION` from the full context.
3. **Review with another AI.** Before material execution, send the proposed decision to the cheapest capable independent reviewer; ordinarily use semantic tier `fast`.
4. **Revise or block.** `REVISE` requires correction; `BLOCK` stops execution until the issue is resolved. Ordinary review is bounded to two revision cycles.
5. **Escalate when consequences are high.** RISK_3/RISK_4, destructive/irreversible work, auth/payments/PII/production and large structural plans additionally require a stronger critic/judgment review.
6. **Interview product decisions.** For product-affecting work, inspect discoverable facts first and ask all currently material user decisions in one useful batch.
7. **Persist durable state.** Keep `docs/agentit/STATE.md` or the project's canonical equivalent current on substantial/long work.
8. **Load real skill bodies.** IDs alone are not activation. Load only the smallest useful set.
9. **Select tools deliberately.** Use MCPs/tools only when they materially improve the chosen plan and keep least privilege.
10. **Execute the reviewed plan.** Delegate where specialization, independence, isolation, breadth, latency or fresh judgment adds value.
11. **Verify.** No completion claim without fresh evidence appropriate to the task.
12. **Git PR-first.** Repository changes default to a work branch and pull request unless explicitly overridden.

## `TASK_DECISION`

The primary model must decide, at minimum:

- user intent and desired outcome;
- established facts;
- material unknowns;
- domain/category;
- complexity;
- `RISK_0..RISK_4` and rationale;
- reversibility and external effects;
- skills and tools;
- execution topology;
- worker/specialist roles when useful;
- dependency/ownership boundaries;
- concrete implementation or investigation plan;
- verification evidence;
- backup/dry-run/rollback/post-check requirements where relevant.

The decision may remain internal if surfacing it would add noise, but the review worker must receive it.

## Mandatory economy reviewer

For ordinary material work, always request a read-only second opinion from the cheapest model/endpoint that is still competent to understand the bounded decision.

Prefer the semantic `fast` tier. When similarly cheap, diversity is useful: a different model family from the primary agent is preferable because correlated mistakes are less valuable as a review.

The reviewer receives only the bounded context necessary to judge the proposal:

- exact request and relevant constraints;
- project facts already established;
- proposed `TASK_DECISION`;
- applicable Agentit decision rules.

It does not need write permissions and must not execute the task.

Use `task-router/references/economy-reviewer.md`. Expected verdict:

```text
VERDICT: APPROVE | REVISE | BLOCK
ISSUES:
- ...
REQUIRED_CHANGES:
- ...
CONFIDENCE: low | medium | high
```

The primary agent must treat the reviewer as an adversarial checker, not a ceremonial rubber stamp.

If no worker can be spawned, use a fresh/isolated context. If that is impossible too, perform an explicit adversarial self-review and record that the check was not independent.

## Strong-review escalation

The economy reviewer is the default preflight check, not the final authority for high-consequence work.

Use a stronger independent `critic` or `judgment` tier in addition when any of these apply:

- RISK_3 or RISK_4;
- auth/authorization/session boundaries;
- payments/billing/financial effects;
- secrets/credentials;
- PII or sensitive user data;
- production infrastructure/deployments;
- destructive or significant data/schema migrations;
- difficult rollback;
- large structural architecture or product plan.

For destructive data operations, require verified backup, rollback plan and post-check. For RISK_4, use a preview/dry-run whenever technically meaningful.

## Domain packs

Choose one primary family per stage: engineering, frontend, design, backend, data, product, writing, release, research, or another clearly scoped pack.

Load the smallest useful family plus core. Do not dump the entire catalog into model context.

Craft depth Standard/Polished/Studio applies only to design/visual work.

## Skills are knowledge, not routing code

Profiles and registries are inventories. The AI reads enough metadata/context to choose useful skills. No script infers the semantic skill set from prompt words.

A skill is actually used only when the stage model reads its `SKILL.md` body or receives equivalent provider-native injection. A list of IDs is not evidence of skill use.

Domain-specific skills require real context. For example, a PostgreSQL-specific skill should be selected because the project is actually PostgreSQL/Supabase/psql, not because the request merely contains “database”.

## Intelligent delegation

Delegate when there is a concrete benefit:

- independent hypotheses can be investigated in parallel;
- a bounded cheap worker can read large source sets while the primary preserves context for synthesis;
- frontend/backend or other domains have clean ownership boundaries;
- fresh correctness/security/performance criticism is useful;
- design directions benefit from independent concepts;
- a cheaper capable model can handle bounded repetitive work.

Do not spawn workers merely for appearance. Do not refuse useful delegation merely because the primary model is strong.

One writer owns each file/shared state unless isolation through branches/worktrees makes parallel writes safe.

## Runtime: mechanical enforcement only

Agentit's Loop/Graph runtime may still be used for mechanical execution state, attempt budgets, dependency tracking, receipts and write ownership. It must not classify natural-language intent.

### Loop

For an executable unit with a verifiable outcome, define:

- observable goal;
- verifier;
- stop condition;
- bounded attempt budget;
- escalation boundary.

A retry needs fresh evidence or a changed strategy. Do not weaken a verifier to manufacture success.

### Graph

For genuinely multi-node execution, define dependencies, ownership and expected handoffs before spawning. Avoid overlapping writers to the same shared state.

These mechanisms enforce the plan **after the AI has decided it**; they are not a semantic router.

## Product interview

Do not turn missing context into silent invention. For product-affecting work, inspect what is discoverable first, then ask one consolidated round covering only material decisions that cannot be inferred safely.

Recommend defaults so the user can answer “use your recommendation” instead of being forced to design the solution from scratch.

## Public visual quality floor

A landing page, homepage, public company/brand site, portfolio, storefront, campaign site or complete visual redesign is design-primary even if implementation is React/Next/CSS.

For greenfield public visual work or a total redesign, Studio is the normal recommendation unless the user wants a leaner pass. Typical flow:

`interview -> live inspiration research -> design direction -> implementation -> independent visual critique -> desktop/mobile browser QA`

Before code, capture a concrete `DESIGN_DIRECTION` with visual thesis, layout/composition grammar, typography, color/material language, imagery, message/copy strategy, signature mechanic, motion role, preserve/replace choices and anti-goals.

Research must affect actual design choices rather than serving as decorative process documentation.

## Continuity

Chat sessions are disposable. Keep a compact canonical project state that allows a fresh agent to recover:

- objective and confirmed intent;
- constraints/non-goals;
- durable decisions;
- current status;
- branch/PR;
- important files/artifacts;
- latest verification;
- next actions/blockers.

Do not persist secrets, credentials, private chain-of-thought, full transcripts or giant tool dumps.

## Verification

No `done`, `fixed`, `passing`, `premium`, `beautiful` or equivalent claim without fresh evidence appropriate to the claim.

Examples:

- code change -> relevant tests/runtime checks;
- UI/visual claim -> rendered/browser evidence at relevant viewport sizes;
- migration -> pre/post state plus rollback readiness;
- bug fix -> reproduction before and verification after;
- high-risk change -> independent strong review plus operational checks.

The second-model decision review happens **before** execution; verification happens **after** execution. They solve different failure modes.

## Git ownership

Repository changes default to:

`work branch -> commits -> verification -> pull request -> review/user merge decision`

Do not write directly to `main`/`master` or auto-merge unless explicitly authorized.

## Provider fallback

Provider adapters may map `fast`, `coding`, `critic` and `judgment` to different concrete models. Do not hardcode one vendor into the portable protocol.

For an ordinary decision review, cost/latency matters: use the cheapest capable reviewer. For high-risk work, capability matters more than cheapness and the stronger escalation is mandatory.

## Safety and ownership

Explicit user instructions and project rules beat defaults. Safety beats all. The primary agent owns final integration and the user-facing result, but it must not bypass the required review just because it is confident.