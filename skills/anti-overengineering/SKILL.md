---
name: anti-overengineering
description: Enforces Agentit's two-mode development discipline. Use for feature implementation, refactors, coding plans and code review to prevent speculative architecture, test proliferation, repeated full-suite verification, unrelated cleanup and review loops. BUILDER mode completes requested features with the minimum relevant checks; REVIEW mode freezes feature scope and deeply validates the finished implementation. Risk boundaries still require immediate targeted safety checks.
---

# Anti-Overengineering

## Objective

Finish useful software without turning implementation into an endless sequence of tests, abstractions, refactors, reviewers and audits.

This skill has exactly two development modes:

```text
DEVELOPMENT_MODE: BUILDER | REVIEW
```

Risk is separate from mode. BUILDER is not permission to ignore auth, payments, destructive data operations, secrets, migrations, concurrency or other high-impact boundaries.

## Hard justification rule

Every new production abstraction, test, dependency, document, worker, review pass or verification command must be justified by at least one of:

1. a current explicit requirement;
2. an observed bug/regression;
3. an established project contract/invariant;
4. a real risk boundary affected by the change.

"Could be useful", "best practice", "future-proof", "more flexible" and "just to be safe" are not enough.

# BUILDER MODE

## Goal

**Complete the requested feature set.**

Builder optimizes for implementation throughput while keeping the changed path sane. Do not repeatedly stop development to perform release-grade validation.

Default loop:

```text
implement feature
→ run the cheapest relevant check
→ fix demonstrated breakage
→ continue to the next feature
```

## Builder verification budget

Use the smallest signal that can catch an obvious mistake in the code just changed:

- compile/typecheck the affected surface when relevant;
- run one focused test or directly related test group for meaningful logic;
- use a targeted browser/runtime smoke check for UI/integration work;
- inspect the actual changed path;
- verify an affected high-risk boundary immediately.

Then continue.

### Do not do this by default in BUILDER

- full repository test suite after every feature or edit;
- full lint + typecheck + build + E2E repeatedly;
- broad security/performance/accessibility audits unrelated to the current risk;
- new tests for trivial wrappers, static copy, framework behavior or behavior already covered;
- reviewer/subagent committees for bounded implementation;
- unrelated refactors, formatting sweeps or "while I'm here" cleanup;
- architecture redesign because the current code is not aesthetically ideal;
- documentation churn after each slice;
- commit/review ceremony after every tiny change;
- rerunning the same successful command without intervening relevant changes.

A failed targeted check is evidence. Fix the demonstrated issue and rerun the relevant check. Do not widen the verification surface unless the failure shows a wider blast radius.

## Builder testing rule

Add or strengthen a test when it buys durable confidence:

- meaningful business logic;
- a bug that must not return;
- a changed public contract;
- a business-critical path;
- behavior difficult to verify manually;
- a risk boundary that needs persistent evidence.

Usually do not add a test when it would only:

- duplicate an existing failure mode;
- assert implementation details;
- test framework/library behavior;
- increase coverage percentage without new confidence;
- require a large mock/fixture system for a tiny behavior.

Never weaken/delete/skip a valid failing test merely to obtain green.

## Builder architecture rule

Prefer direct code over speculative structure.

Do not add by default:

- interfaces with one real implementation;
- factories/registries/plugin systems for one consumer;
- generic event buses for one interaction;
- service layers that only forward calls;
- configuration for behavior that is currently fixed;
- compatibility layers for unreleased behavior;
- dependencies for a small local problem;
- caches, queues, services, databases or workers without a present need;
- helpers extracted only because a few lines look similar.

Duplication is allowed until repetition **and the correct abstraction** are both evident.

## Builder stop condition

Builder stops when:

- every requested feature is functionally implemented;
- the main paths have enough targeted evidence to continue safely;
- no known blocker prevents REVIEW.

Builder does **not** claim production readiness.

# REVIEW MODE

## Goal

**Deeply validate and simplify the completed implementation without expanding feature scope.**

Entering REVIEW freezes requested functionality. Review may fix defects, regressions, security issues, performance problems, integration gaps and unnecessary complexity discovered during review. It does not invent new product features.

Default loop:

```text
inspect complete diff/system
→ run broad required gates
→ identify concrete findings
→ fix findings in batches
→ targeted recheck while fixing
→ rerun broad final gate
→ report evidence
```

## Review surfaces

Review the surfaces justified by the project and change:

- acceptance criteria for the whole requested feature set;
- full repository-required test suite;
- build/type/lint gates;
- integration and critical E2E flows;
- runtime/browser behavior;
- security and trust boundaries;
- migrations/data integrity/rollback where relevant;
- dependency/supply-chain changes;
- performance where the change could materially affect it;
- accessibility for affected user-facing flows;
- docs/configuration drift;
- complete diff for dead code, accidental complexity and unrelated churn.

Use specialist skills only for surfaces that actually apply.

## Review discipline

A deep review is not an excuse for infinite review loops.

- Findings need concrete evidence or a clear violated contract.
- Batch related fixes before rerunning expensive global checks.
- During fixes, use targeted checks.
- Run the comprehensive gate again after the material fix set, not after every line.
- Do not chase speculative edge cases whose preconditions cannot occur.
- Non-blocking nice-to-haves become separate follow-up work instead of extending review indefinitely.

## Review completion

REVIEW is complete when:

- requested features satisfy their acceptance contract;
- required broad checks have fresh evidence;
- applicable high-risk boundaries have been verified;
- concrete review findings are fixed or explicitly recorded as blockers/follow-ups;
- the final diff contains no unjustified architecture or unrelated churn;
- the work can be truthfully handed off with its limitations.

# Mode transitions

## Enter BUILDER when

- implementing a new feature/product;
- continuing an incomplete implementation;
- fixing issues found during construction;
- the user says build, implement, finish, create or continue.

BUILDER is the default for active implementation.

## Enter REVIEW when

- the requested feature set is functionally complete and is being prepared for handoff/PR/release;
- the user explicitly asks for review, audit, hardening, production readiness or comprehensive validation;
- an existing implementation is being assessed rather than extended.

Do not oscillate modes after every feature. Finish the planned build first unless a genuine blocking risk requires intervention.

# Risk override

Regardless of mode, verify dangerous boundaries early enough to avoid compounding damage:

- auth/session/authorization;
- payments/financial effects;
- destructive migrations or irreversible writes;
- secrets/credentials;
- production data;
- concurrency/distributed state;
- externally visible irreversible actions.

The override should be **targeted to the risk**. It does not automatically turn BUILDER into a whole-repository REVIEW.

# Interaction with other Agentit skills

When this skill is selected, it owns **development verification cadence**.

- `incremental-implementation`: slices remain useful for implementation/rollback, but "test each slice" means the minimum relevant check in BUILDER, not the full suite.
- `test-driven-development`: strict red/green is appropriate for bugs, non-trivial logic, contracts and high-risk behavior; do not apply ceremonial TDD to trivial glue/static/presentational work.
- `verification-before-completion`: the evidence must match the claim. BUILDER can claim a feature path was smoke-checked; only REVIEW can claim the completed implementation passed its comprehensive gate.
- `constraint-driven-development`: never weaken project constraints, but place expensive checks in REVIEW unless the constraint explicitly requires them earlier.
- `code-review-and-quality`: normally REVIEW mode, not a mandatory interruption after every BUILDER slice.

# Anti-patterns

Stop and simplify if:

- one feature creates a framework;
- every edit triggers the full suite;
- every helper gets a test regardless of behavior;
- reviewers keep extending scope with nice-to-haves;
- the agent adds defensive branches for impossible states;
- the diff expands into unrelated cleanup;
- more time is spent proving process compliance than finishing the requested product.

# Completion criteria

The skill is followed when:

- BUILDER completes requested functionality with proportional targeted checks;
- REVIEW performs the deep validation once the implementation is ready;
- high-risk boundaries receive timely targeted evidence;
- tests and abstractions exist because they buy current value;
- comprehensive checks are not repeated after every small change;
- feature scope does not grow during REVIEW.
