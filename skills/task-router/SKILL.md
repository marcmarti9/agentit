---
name: task-router
description: Model-owned task decision, execution depth and risk gates. Select justified packs, bodies, references, tools and review without keyword classifiers or fixed skill quotas.
---

# Task decision contract

The primary model interprets the request using the conversation, project state and constraints. Code resolves explicit IDs and enforces declared contracts; it must not infer intent, relevance or a skill count from task text.

Before material execution, record a compact decision covering the desired outcome, known facts, material unknowns, scope, risk/reversibility, relevant packs, selected skills and why, reference mode, actual tools/permissions, ownership, verification and stop/rollback condition. Do not expose private reasoning. Revisit the decision when evidence changes.

## Development modes — canonical policy

For repository implementation work, use exactly:

```text
DEVELOPMENT_MODE: BUILDER | REVIEW
```

### BUILDER — default while functionality is incomplete

The objective is to complete the requested feature set. Use direct implementation, the smallest justified skill/tool set and targeted checks that prevent obvious breakage. Do not interrupt ordinary construction with blanket audits, full-suite repetition, unrelated refactors, documentation churn or review committees.

BUILDER verification budget: implement -> cheapest relevant check -> fix demonstrated failure -> continue.

Do not claim whole-product readiness from BUILDER evidence.

### REVIEW — deep validation after construction

Use REVIEW when the requested implementation is functionally complete and is being prepared for handoff/PR/release, or when the user explicitly requests review/audit/hardening.

Freeze feature scope. Review the complete change, run the repository-required broad gates, inspect relevant integration/E2E/security/data/dependency/performance/accessibility/documentation surfaces, fix concrete findings, then rerun the broad final gate after the material fix set.

REVIEW is deep but bounded: evidence-backed findings only, no speculative feature expansion and no infinite audit/fix loop.

### Development economy invariant

Mode and risk are separate. Auth, payments, destructive writes/migrations, production data, secrets, concurrency and other high-impact boundaries may require immediate targeted verification during BUILDER. That risk override does not automatically trigger a repository-wide REVIEW.

When `anti-overengineering` is selected, it owns development verification cadence and scopes generic per-slice testing/review guidance from overlapping skills.

## Development security invariant

Do not rely on the user to ask for a security review. For changes touching untrusted inputs, rendering, auth/session/authorization, APIs, integrations, data/storage, uploads, secrets, PII, payments, dependencies, deployment or CI trust boundaries, load `security-and-hardening` and test the affected boundary.

Load `app-security-gate` for substantial app/backend changes, sensitive flows, user-facing releases and production readiness. Its result is evidence-driven PASS or BLOCKED, not a prose assurance.

For purely presentational edits with no changed trust boundary, do not load security simply because the project is a web app. **FAST mode compatibility:** scope checks to actual affected risk; escalate when the change is not safely localized.

## Selection and source rules

Packs are flat discovery maps. There is **no fixed minimum or maximum** skill count. Every selected body must earn its context cost. Prefer one accountable workflow for an overlapping concern; add complementary specialists only when required. Never load a whole pack by default.

Check Agentit's local skills first. Select `skillfinder-external-scout` only when no credible local owner exists or the user explicitly asks for ecosystem-wide discovery; never auto-install its results.

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

Web edits inherit the compact anti-slop baseline from `using-agentit`; for substantial design/audits consider `hallmark` JIT, not for merely restating that baseline.
