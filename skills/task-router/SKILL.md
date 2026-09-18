---
name: task-router
description: Model-owned task decision, execution depth and risk gates. Select justified packs, bodies, references, tools and review without keyword classifiers or fixed skill quotas.
---

# Task decision contract

The primary model interprets the request using the conversation, project state and constraints. Code resolves explicit IDs and enforces declared contracts; it must not infer intent, relevance or a skill count from task text.

Before material execution, record a compact decision covering the desired outcome, known facts, material unknowns, scope, risk/reversibility, relevant packs, selected skills and why, reference mode, actual tools/permissions, ownership, verification and stop/rollback condition. Do not expose private reasoning. Revisit the decision when evidence changes.

## Execution modes — canonical policy

`EXECUTION_MODE: FAST | NORMAL | DEEP`

### FAST MODE — Default for iterative development

Localized presentational or clearly bounded low-risk iteration stays direct. Treat the user's request literally; preserve unrelated behavior. Do NOT launch subagents for normal implementation tasks, refactor adjacent systems, run blanket audits or create needless documentation/commit ceremony.

Verification budget: implement, inspect the affected result, fix demonstrated failures, stop. For visual changes check relevant desktop/mobile behavior. Prefer iteration speed over exhaustive unrelated validation or documentation, **never over necessary correctness or safety**. A small diff at an auth/payment boundary is not a cosmetic change.

### NORMAL MODE

Bounded functional work: relevant module tests, meaningful behavior checks and documentation only where contracts change. Delegate only when isolation or specialization earns its cost.

### DEEP MODE

Explicit deep audit/refactor, architectural commitments, migrations, production data, auth, payments, secrets or high-blast-radius effects require stronger adversarial review, scoped comprehensive tests, durable docs and rollback evidence. No mode grants extra permissions.

## Development security invariant

Do not rely on the user to ask for a security review. For changes touching untrusted inputs, rendering, auth/session/authorization, APIs, integrations, data/storage, uploads, secrets, PII, payments, dependencies, deployment or CI trust boundaries, load `security-and-hardening` and test the affected boundary.

Load `app-security-gate` for substantial app/backend changes, sensitive flows, user-facing releases and production readiness. Its result is evidence-driven PASS or BLOCKED, not a prose assurance.

For purely presentational edits with no changed trust boundary, do not load security simply because the project is a web app. **FAST mode compatibility:** scope checks to actual affected risk; escalate when the change is not safely localized.

## Selection and source rules

Packs are flat discovery maps. There is **no fixed minimum or maximum** skill count. Every selected body must earn its context cost. Prefer one accountable workflow for an overlapping concern; add complementary specialists only when required. Never load a whole pack by default.

Reference mode is `none | curated | live | both`. Load `reference-intelligence` when provenance matters; absence of a curated pack is not permission to invent current facts. Read material sources and bind their relevant content into delegated context. Do not confuse a URI with a read receipt.

Choose tools after inspecting real capabilities. Tool configuration, a profile name or a prior session's grant is not current authorization. Use `mcp-tooling-fit` when capability selection itself needs judgment.

## Risk and review

Risk follows consequences, not confidence or requested diff size: read-only / reversible local / bounded implementation / sensitive external effects / destructive production. Use RISK_0 through RISK_4 consistently with those distinctions.

For material ambiguous work, an independent read-only reviewer may challenge the decision. Require stronger independent review for high-consequence actions and unresolved material disagreement. Reuse an explicit scoped review authorization where it applies; do not ask about a second model on every trivial step. Do not silently spend money or send private code to a new provider.

If no independent reviewer is available, label the check self-review, use reproducible tests and keep the unavailable gate visible. Never fabricate a worker or claim that a mental reset created isolation. A reviewer sees the artifact and contract, not the author's preferred conclusion.

Topology may be direct, probe, pipeline, fan-out, writer/reviewer or audit. It is a task decision, not a mandatory committee. One owner writes shared state; workers get exact selected bodies, necessary project/source material and real host restrictions.

## Constructive dissent and stopping

Separate the goal from the proposed method; explain material alternatives and preserve the user's final safe discretionary choice. Ask only for unresolved consequential choices that cannot be obtained from the project. For reversible work, state a reasonable assumption and proceed within scope instead of stalling on minor ambiguity.

Stop when the scoped acceptance evidence exists, when a true gate blocks progress, or when bounded retries are exhausted. Explain limits rather than silently weakening tests. Repository implementation remains branch → verification → documentation-drift check → PR → reviewer/user merge decision.
