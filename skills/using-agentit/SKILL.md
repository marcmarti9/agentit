---
name: using-agentit
description: Activate Agentit end-to-end. Classify with the host LLM, validate hard policy, interview, load real skills, enforce Loop/Graph runtime, delegate intelligently, verify, and ship PR-first.
---

# Using Agentit

Agentit is an operating protocol for capable AI agents. Prompt quality must not
become the quality ceiling. The active model owns context recovery, semantic
classification, planning, skill/tool selection, delegation, integration and
verification.

## Activation

Natural language that means use/usa/utilise Agentit activates this playbook for
the session. No other powerwords are required.

## Stable harness locations

- harness root: `~/code/agentit` when using the normal checkout;
- decision contract: `~/code/agentit/router/decision_contract.py`;
- compatibility adapter: `~/code/agentit/router/route.py`;
- decision protocol skill: `~/code/agentit/skills/task-router/SKILL.md`;
- skills: `~/code/agentit/skills/<id>/SKILL.md`;
- runtime CLI: `~/code/agentit/router/runtime_cli.py`;
- specialist catalog: `~/code/agentit/agents/catalog.yaml`;
- profiles: `~/code/agentit/profiles.yaml`;
- continuity: `<project>/docs/agentit/STATE.md`.

Provider-installed/project-local equivalents are fine when they resolve to the
same protocol/skill bodies.

## Core protocol

1. Inspect available conversation/project/tool context before asking the user to repeat facts.
2. Classify the task **yourself** using `task-router`'s stable rubric. Do this for every task before execution.
3. For product-affecting work, use `interview-me`: inspect discoverable facts first, then ask all currently material user decisions in one useful batch.
4. Persist confirmed intent in `docs/agentit/STATE.md` before substantial implementation.
5. Validate deterministic hard policy when a structured decision is materialized. Python may reject an unsafe/inconsistent decision; Python must not reinterpret the prompt.
6. Load actual `SKILL.md` bodies for the selected stage. Skill IDs alone are not activation.
7. Select tools/MCPs only when they materially fit the current stage and capability requirements.
8. Materialize Loop runtime for every executable unit; materialize Graph runtime for multi-node work.
9. Execute with intelligent delegation where independence, specialization, isolation, breadth or fresh review helps.
10. Use an independent critic for structural/high-impact plans and the design cases that require one.
11. Accept completion only from fresh evidence + applicable runtime receipts.
12. Use branch + PR by default for repository changes unless the user explicitly overrides that workflow.
13. Keep continuity state current on long or multi-stage work.

## The model is the semantic router

Do not run prompt regexes or keyword trees to decide what the user means. The
active model has the conversation, repository and tool state and should use that
context directly.

Apply the same decision framework every time, but allow context to change the
answer. A follow-up such as “fix it” may be impossible for a standalone script
to classify and trivial for the active model that knows what “it” refers to.

`router/route.py` is now only a compatibility/adapter boundary. Calling it with
natural language returns `status=decision_required`; it does not invent risk,
category or topology. `router/decision_contract.py` validates structured host
model decisions and deterministic invariants.

## Domain packs

Choose one primary family per task/stage: engineering, frontend, design, backend,
data, product, writing, release, research, or a role-scoped pack. Load the
smallest useful family + core, not the entire catalog.

Craft depth Standard/Polished/Studio applies only to public/visual design work.
Lean/normal/thorough may describe non-design rigor separately.

## Runtime enforcement: Loop + Graph Engineering

### Loop Engineering

Every executable unit declares before action:

- observable goal;
- verifier;
- stop condition;
- bounded attempt budget (default 2 total attempts = 1 automatic retry);
- escalation boundary.

Persist loop state under ignored `.agentit/runtime/loops/` using
`router/runtime_cli.py`. Every attempt records pass/fail, strategy and empirical
evidence. A retry needs fresh evidence or a different strategy. Never weaken the
verifier to manufacture a pass.

`loop-check` must pass before that unit is complete. Narrative claims are not a
replacement for the Loop Receipt.

### Graph Engineering

When work has more than one execution node, materialize a DAG under
`.agentit/runtime/` before spawning. Each node declares dependencies, exclusive
write ownership and expected handoff artifacts where relevant.

`graph-init` must validate before execution. The runtime rejects cycles,
unknown/self dependencies, unsafe paths and overlapping write ownership. Spawn
only nodes returned by `graph-ready`.

A node unlocks dependents only through `graph-complete` with a passed Loop
Receipt. Missing expected artifacts block the handoff. Final multi-node
completion requires `graph-check` + Graph Receipt.

## Public visual quality floor

A landing, homepage, public company/brand site, portfolio, storefront, campaign
site or complete visual redesign is design-primary. The host model must classify
it that way even when implementation happens in React/Next/CSS.

For greenfield public visual work or a total redesign, recommend Studio by
default unless the user explicitly chooses a leaner depth. Normal shape:

`deep interview -> live inspiration research -> concept/direction -> implementation -> independent visual critique -> desktop/mobile browser QA`

For ordinary public-facing visual improvements, use at least Polished unless the
brief calls for a lean pass.

Before code, capture a concrete `DESIGN_DIRECTION` covering visual thesis,
composition/grid grammar, typography roles, color/material language, imagery,
copy/message strategy, signature mechanic, container policy, motion role,
preserve/replace choices, anti-goals and reference-to-decision links.

Live research must affect actual design choices. If the final design would have
looked the same without the research, the research failed.

## Skill activation contract

A decision/profile/worker listing `design-taste-frontend` has **not** used that
skill unless the executing model actually read the corresponding `SKILL.md` body
or received equivalent provider-native injection.

Before a stage that depends on skills:

1. resolve selected skill paths;
2. load the bodies into the executing context;
3. retain a lightweight receipt (ID + path + hash where supported);
4. project the same bodies/receipt to delegated workers that depend on them.

Registry code verifies availability only. It does not decide which skill is
semantically relevant.

## Tooling / capability fit

Inventory what is actually available, resolve semantic capability requirements,
choose only relevant providers and preserve least privilege. Do not enable a
universal noisy tool surface.

No provider inventory means no assumed grant. Missing required capability must
remain visible rather than being silently treated as available.

## Intelligent delegation

Stay single-agent when work is tightly coupled and delegation adds no concrete
benefit. Delegate when expertise, independence, tool separation, context
isolation, breadth or fresh judgment improves the result.

Examples:

- parallel read-only investigations of independent hypotheses;
- large-source research delegated to bounded readers while the parent preserves context for synthesis;
- separate frontend/backend packages with explicit ownership;
- independent correctness/security/performance review;
- 2–3 independent design concepts when genuine directional diversity helps;
- fresh-context design critique.

Do not spawn workers for show. Do not reject delegation merely because one model
could technically perform the whole task.

## Continuity

Chat sessions are disposable. Keep `docs/agentit/STATE.md` useful enough that a
fresh agent can recover objective, confirmed intent, constraints, decisions,
current status, branch/PR, important files/artifacts, latest verification, next
actions and blockers without asking the user to reconstruct history.

Do not persist secrets, credentials, private chain-of-thought, full chat logs or
giant raw tool dumps.

## Verification

No `done`, `fixed`, `passing`, `premium`, `beautiful` or equivalent claim without
fresh evidence and the applicable runtime receipt.

The LLM-native decision contract adds hard floors:

- RISK_3/RISK_4 -> independent review;
- RISK_4 -> preview/dry-run where meaningful + rollback plan + post-check;
- destructive data operation -> RISK_4 + verified backup;
- structural work -> independent critic;
- public visual -> rendered/browser evidence;
- fan-out -> at least two independent branches + concrete delegation reason.

Public visual work also requires comparison against `DESIGN_DIRECTION`, wide and
narrow viewport evidence, anti-cardification/structural-diversity review and
appropriate accessibility/performance sanity.

## Git ownership

Repository changes default to:

`work branch -> commits -> verification -> pull request -> review/user merge decision`

Do not write directly to `main`/`master` or auto-merge unless explicitly
authorized. One writer owns each file/shared state unless isolation by
branches/worktrees makes parallel writing safe.

## Provider fallback

Prefer native scoped workers when useful. If unavailable, use isolated delegated
calls/fresh contexts; if that is unavailable, continue in the parent with the
same scoped skill bodies and runtime contracts. Multi-agent may improve quality
or efficiency but must not become a correctness dependency.

## Safety and ownership

Explicit user instructions and project rules beat defaults. Safety beats all.
The Architect owns final acceptance and integration. Deterministic validators are
guardrails, not substitutes for model judgment.
