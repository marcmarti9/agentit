---
name: using-agentit
description: Activate Agentit end-to-end. The primary AI owns task understanding and strategy, a cheap independent AI audits that decision, strong AI arbitrates high-risk/disputed cases, then Agentit interviews, loads skills, delegates, executes through mandatory Loop/Graph runtime contracts, documents durable system knowledge, verifies, and ships PR-first.
---

# Using Agentit

Agentit is an operating protocol for capable AI agents. It is not a natural-language classifier implemented in code.

The primary model owns context recovery, task interpretation, planning, skill/tool selection, delegation, integration, documentation and verification. A cheap second model audits the proposed decision before material execution; it does not become the router. High-risk or materially disputed decisions escalate to a stronger independent critic/judgment model.

## Activation

Natural language that means use/usa/utilise Agentit activates this playbook for the session. No other powerwords are required.

## Stable harness locations

- harness root: `~/code/agentit` when using the normal checkout;
- decision protocol: `~/code/agentit/skills/task-router/SKILL.md`;
- economy audit contract: `~/code/agentit/skills/task-router/references/economy-reviewer.md`;
- skills: `~/code/agentit/skills/<id>/SKILL.md`;
- runtime CLI: `~/code/agentit/router/runtime_cli.py` for mechanical Loop/Graph state only;
- specialist catalog: `~/code/agentit/agents/catalog.yaml`;
- profiles: `~/code/agentit/profiles.yaml`;
- continuity: `<project>/docs/agentit/STATE.md`;
- durable documentation contract: `~/code/agentit/docs/DOCUMENTATION_CONTRACT.md`.

There is intentionally no semantic `route.py` or programmatic decision contract. Mechanical utilities may manage files/state/tests, but they do not interpret user intent.

## Core protocol

1. **Inspect context.** Recover relevant conversation, repository, files, project rules, tools and current state before asking the user to repeat information.
2. **Primary decides.** Apply `task-router` and form `TASK_DECISION` from the full context. Do not hand this semantic ownership to a cheaper worker.
3. **Cheap audit.** Before material execution, send the proposed decision to the cheapest capable independent audit model, ordinarily semantic tier `fast`.
4. **Reconsider or escalate.** `CHALLENGE` makes the primary reconsider; `ESCALATE` or unresolved material disagreement goes to a stronger critic. The cheap model never arbitrates the final semantic decision.
5. **Strong review when consequences are high.** `RISK_3/RISK_4`, destructive/irreversible work, auth/payments/PII/production and large structural plans require a stronger `critic`/`judgment` review before execution.
6. **Interview product decisions.** For product-affecting work, inspect discoverable facts first and ask all currently material user decisions in one useful batch.
7. **Persist durable state.** Keep `docs/agentit/STATE.md` or the project's canonical equivalent current on substantial/long work.
8. **Load real skill bodies.** IDs alone are not activation. Load only the smallest useful set.
9. **Select tools deliberately.** Use MCPs/tools only when they materially improve the chosen plan and keep least privilege.
10. **Execute the reviewed plan through runtime contracts.** Every executable unit with a verifiable outcome gets a Loop Contract; multi-node work additionally gets a Graph Contract before spawning.
11. **Document durable knowledge as part of execution.** Keep architecture, components, contracts, decisions, operations and troubleshooting Markdown aligned with the implementation. `STATE.md` does not replace permanent system documentation.
12. **Verify through receipts + fresh evidence.** Direct/single-unit executable work requires fresh verifier evidence and a passed Loop Receipt. Multi-node work requires a passed Graph Receipt backed by passed node Loop Receipts. Substantial repository work additionally requires a documentation-drift check.
13. **Git PR-first.** Repository changes default to a work branch and pull request unless explicitly overridden.

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

The decision may remain internal if surfacing it would add noise, but the audit worker must receive it.

## Mandatory economy audit

For ordinary material work, request a read-only second opinion from the cheapest model/endpoint that is still competent to audit the bounded decision.

Prefer the semantic `fast` tier. When similarly cheap, diversity is useful: a different model family from the primary agent is preferable because correlated mistakes are less useful as a check.

The auditor receives only the bounded context necessary to judge the proposal:

- exact request and relevant constraints;
- project facts already established;
- proposed `TASK_DECISION`;
- applicable Agentit decision rules.

It does not need write permissions and must not execute the task or generate an authoritative replacement plan.

Use `task-router/references/economy-reviewer.md`. Expected output:

```text
AUDIT: CLEAR | CHALLENGE | ESCALATE
FINDINGS:
- ...
SUGGESTED_CHECKS:
- ...
CONFIDENCE: low | medium | high
```

The primary agent treats this as an adversarial check, not a ceremonial rubber stamp and not a transfer of decision ownership.

`CLEAR` means no material objection was found.

`CHALLENGE` means the primary must reconsider the finding. It may revise the decision or retain it with explicit evidence-based reasoning. If material disagreement remains after reconsideration, escalate.

`ESCALATE` means use a stronger independent model. The cheap auditor does not resolve the dispute itself.

If no cheap worker can be spawned, use a fresh/isolated context when possible. For high-risk work, a same-context self-audit is not equivalent to an independent strong review.

## Strong-review escalation

A stronger independent `critic` or `judgment` tier is mandatory when any of these apply:

- `RISK_3` or `RISK_4`;
- the cheap auditor asks to escalate;
- material disagreement survives primary reconsideration;
- auth/authorization/session boundaries;
- payments/billing/financial effects;
- secrets/credentials;
- PII or sensitive user data;
- production infrastructure/deployments;
- destructive or significant data/schema migrations;
- difficult rollback;
- large structural architecture or product plan.

The strong critic receives the primary `TASK_DECISION` plus relevant audit findings. It is not the implementation owner, but for these cases it is the independent judgment gate: execution waits until critical objections are resolved, the decision is revised, or required user input is obtained.

For destructive data operations, require verified backup, rollback plan and post-check. For `RISK_4`, use a preview/dry-run whenever technically meaningful.

## Domain packs

Choose one primary family per stage: engineering, frontend, design, backend, data, product, writing, release, research, or another clearly scoped pack.

Load the smallest useful family plus core. Do not dump the entire catalog into model context.

Craft depth Standard/Polished/Studio applies only to design/visual work.

## Skills are knowledge, not routing code

Profiles and registries are inventories. The primary AI reads enough metadata/context to choose useful skills. No script and no cheap auditor owns semantic skill selection.

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

Agentit's Loop/Graph runtime is **mandatory for executable work with a verifiable outcome**. It provides execution state, attempt budgets, dependency tracking, receipts and write ownership. It must not classify natural-language intent.

Removing the semantic router does not weaken the runtime acceptance gate. The runtime enforces a plan only after the AI has decided and reviewed that plan.

### Loop

Every executable unit with a verifiable outcome must define and persist:

- observable goal;
- verifier;
- stop condition;
- bounded attempt budget;
- escalation boundary.

A retry needs fresh evidence or a changed strategy. Do not weaken a verifier to manufacture success.

A direct/single-unit executable task is accepted only after the verifier has produced fresh evidence and `loop-check` has produced a passed **Loop Receipt** for the current contract/state.

### Graph

Every genuinely multi-node execution must materialize a DAG before spawning. Define dependencies, exclusive write ownership where relevant, expected handoff artifacts and each node's bound Loop Contract.

Spawn only ready nodes. Do not advance around a pending/blocked dependency and do not allow overlapping writers to shared state unless branches/worktrees provide explicit isolation.

Final multi-node acceptance requires `graph-check` and a passed **Graph Receipt** backed by the current passed Loop Receipts for completed nodes.

These mechanisms are execution infrastructure, not a semantic router.

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

## Mandatory durable documentation

Continuity answers **where the work is now**. It does not fully answer **how the system works**. For substantial repository work, apply `docs/DOCUMENTATION_CONTRACT.md` as an acceptance contract.

The documentation goal is that a fresh agent or engineer can understand the relevant system from the overall architecture down to each materially affected component without first reading the whole codebase.

During work, persist durable knowledge when it becomes stable rather than reconstructing it at the end. Update the project's canonical Markdown documentation for:

- architecture, layers, boundaries, dependencies and end-to-end data/control flow;
- each non-trivial affected component: responsibility, location, inputs/outputs, internal flow, dependencies, configuration, failure modes and verification;
- APIs, schemas, events, files, invariants and compatibility contracts;
- durable non-obvious decisions, including context, chosen option, realistic alternatives, consequences and conditions for revisiting;
- operational behavior such as startup, lifecycle, jobs, persistence, retries/fallbacks and observability;
- troubleshooting paths that connect symptom -> likely cause -> diagnostic evidence -> corrective action -> verification.

Reuse existing docs instead of creating duplicate sources of truth. Use ADR-style `.md` records when a decision would otherwise be expensive or risky to rediscover. Do not store private chain-of-thought; record the concise decision rationale and evidence needed by future maintainers.

Before declaring substantial repository work complete, perform a documentation-drift check. The work is not complete if relevant Markdown no longer matches the implementation, materially changed components/contracts are unexplained, new important failure modes lack diagnostic guidance, or the current `STATE.md` is stale.

## Verification

No `done`, `fixed`, `passing`, `premium`, `beautiful` or equivalent claim without fresh evidence appropriate to the claim **and the applicable runtime receipt**.

Examples:

- code change -> relevant tests/runtime checks + passed Loop Receipt;
- UI/visual claim -> rendered/browser evidence at relevant viewport sizes + applicable receipt;
- migration -> pre/post state plus rollback readiness + applicable receipt;
- bug fix -> reproduction before and verification after + applicable receipt;
- high-risk change -> independent strong review plus operational checks + applicable receipt;
- multi-node task -> passed Graph Receipt backed by node Loop Receipts;
- substantial repository change -> documentation-drift check against `docs/DOCUMENTATION_CONTRACT.md`.

The cheap decision audit happens **before** execution; Loop/Graph governs execution acceptance; documentation preserves durable system knowledge; verification checks the actual result. They solve different failure modes.

## Git ownership

Repository changes default to:

`work branch -> commits -> verification -> pull request -> review/user merge decision`

Do not write directly to `main`/`master` or auto-merge unless explicitly authorized.

## Provider fallback

Provider adapters may map `fast`, `coding`, `critic` and `judgment` to different concrete models. Do not hardcode one vendor into the portable protocol.

The active primary model owns semantic reasoning even when a cheaper model is available. Cost/latency matters for bounded auditing and repetitive delegated work; capability matters more for primary judgment and mandatory high-risk escalation.

## Safety and ownership

Explicit user instructions and project rules beat defaults. Safety beats all. The primary agent owns the task decision, final integration, documentation and user-facing result. It must not bypass required audit/escalation, durable documentation or runtime receipts merely because it is confident.
