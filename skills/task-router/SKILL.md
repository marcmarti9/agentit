---
name: task-router
description: Model-owned scope, JIT expertise, BUILDER/REVIEW cadence, risk and bounded verification; no semantic classifier.
---

# Task decision contract

The model interprets user/project context; code resolves explicit IDs, never semantic relevance or counts. Record outcome, facts/unknowns, scope, risk, profiles/packs, selected skills/reasons, references, real tools/permissions, ownership, verification and stop/rollback. Revisit on new evidence; omit private reasoning.

## Development modes — canonical policy

For repository implementation state `DEVELOPMENT_MODE: BUILDER | REVIEW` at entry and material transitions. Mode and risk are separate. This core owns cadence; selected procedures add detail without overriding mode or scope.

### BUILDER — complete requested functionality

Finish all requested behavior: implement → cheapest relevant check → fix demonstrated failure → continue. Use sufficient expertise; fewer reads is not success. Avoid repeated full-suite runs, blanket audits, unrelated refactors, speculative architecture, docs churn, trivial tests or committees. Reuse existing/platform primitives before abstractions/dependencies. Focused evidence is not whole-product readiness.

### REVIEW — validate the completed change

Enter for completed functionality or explicit audit. Freeze feature scope. Inspect the full diff; run required broad gates and relevant integration/E2E/security/data/dependency/performance/accessibility/docs checks. Batch concrete fixes with focused rechecks, then rerun broad gates after material fixes. No speculative features/infinite reviews. Check the complete requested scope; report blockers.

### Development economy invariant

Verify affected auth/payment/destructive writes/secrets/production data/concurrency early even in BUILDER without forcing whole-repository REVIEW. Choose one JIT procedure per overlapping concern; `reliable-coding` is the lean general coding companion.

## Development security invariant

Do not rely on the user to ask for a security review. Load `security-and-hardening` for changed untrusted input/rendering, auth/session/authorization, APIs/integrations, storage/uploads, secrets/PII, payments/dependencies or deployment/CI trust boundaries; test the affected boundary. Load `app-security-gate` for substantial app/backend changes, sensitive flows, user-facing releases and production readiness; evidence determines PASS or BLOCKED. Purely presentational edits without changed trust boundaries need no security procedure merely because they are web work. Scope checks to affected risk.

## Selection and source rules

Scan all purpose pointers in `using-agentit`, then inspect matching profile metadata. Discovery needs no profile installation. Packs are flat discovery maps; there is **no fixed minimum or maximum** skill count. Select enough expertise for every material requirement at this stage; choose one primary procedure per overlapping concern. Never load a whole pack by default.

A full profile is justified only when all members apply, combined body size fits context, and conflicting procedures have a clear owner. Explicitly select its IDs and read every selected body completely. Otherwise stage or delegate relevant expertise. A profile name is not a read; minimize irrelevance, not necessary expertise. Reselect when requirements/risk change.

Check local skills first; use `skillfinder-external-scout` only for a genuine local gap or explicit ecosystem research, never auto-install its results. Reference mode: `none | curated | live | both`. Use `reference-intelligence` when provenance matters. Read material current sources; bind actual content, not unread URLs, into workers. Tool/profile configuration and past grants are not current authorization. Use `mcp-tooling-fit` when tooling selection itself needs judgment.

## Risk and review

RISK_0–RISK_4 respectively mean read-only, reversible local, bounded implementation, sensitive external effects, destructive production. Consequences determine risk. Use independent critique for material ambiguity; require stronger evidence for high consequences/disagreement. Reuse scoped authorization; never silently spend/send private code to new providers.

Select `adversarial-idea-review` before converging on consequential or materially uncertain proposals, or when requested. A routine fix need not invoke a separate adversarial procedure or worker.

Choose topology by independence/dependencies. One writer per shared state; workers receive bodies, sources, project instructions and real restrictions. Missing reviewers mean labelled self-review and a visible unavailable gate. Stop at acceptance, true blockers or bounded exhausted attempts; never weaken tests.

## Constructive dissent and stopping

Challenge material weaknesses with evidence; explain trade-offs and preserve the user's final safe discretionary choice. Ask only consequential unknowns unavailable from project/session evidence; resolve reversible details autonomously. Branch → verification → documentation-drift check → PR → authorized merge.

Web work follows `references/web-quality-baseline.md`; substantial design/audits may select `hallmark` JIT.
