---
name: anti-overengineering
description: Prevents implementation work from expanding into speculative architecture, unnecessary tests, repeated full-suite verification, unrelated refactors, documentation churn, or review loops. Use during feature development, refactors, implementation planning, and code review when delivery speed matters and correctness can be protected with phase-appropriate checks. Enforces build-first, verify-proportionally, review-deeply-at-the-end discipline while preserving stronger gates for security, data loss, migrations, payments, auth, concurrency, and other high-risk boundaries.
---

# Anti-Overengineering

## Objective

Ship the **smallest correct implementation of the current requirement** without turning development into an infinite sequence of tests, refactors, abstractions, reviews, and speculative safeguards.

Simplicity is not permission to lower correctness or safety. It is a rule about **where complexity is allowed to exist and when verification is worth its cost**.

## The hard rule

Every new line of production code, test, abstraction, dependency, document, worker, review pass, or verification command must be justified by at least one of:

1. a current explicit requirement;
2. an observed bug or regression;
3. an established project invariant or contract;
4. a real risk boundary affected by the change.

If none applies, do not add or run it.

"Could be useful", "best practice", "future-proof", "more flexible", and "just to be safe" are not sufficient reasons.

## Phase-aware development

Do not apply release-grade validation to every edit.

### BUILD

Goal: finish the functionality without accumulating obvious breakage.

Use the cheapest relevant signal only:
- compile/typecheck the affected surface when needed;
- run one focused test or existing related test group when behavior is non-trivial;
- do a targeted browser/runtime smoke check for UI or integration behavior;
- inspect the actual changed path.

Then continue implementing.

During BUILD, do **not** by default:
- run the whole repository test suite after each slice;
- run full lint + build + typecheck + E2E after every small edit;
- create tests for trivial wrappers, static content, framework behavior, or already-covered behavior;
- spawn reviewers/subagents for bounded changes;
- rewrite adjacent code because it could be cleaner;
- stop after every tiny slice for documentation or commit ceremony.

A failed focused check is evidence: fix the demonstrated problem and rerun the relevant check. Do not widen the verification surface unless the failure suggests wider impact.

### FEATURE CHECKPOINT

When a coherent feature is actually usable end-to-end, verify the feature contract:
- exercise the main user path;
- run the smallest relevant regression set;
- add a durable test only where the behavior is important enough to regress;
- verify changed trust boundaries if any.

If the feature works, continue to the next feature. Do not turn the checkpoint into a repository-wide audit unless the change is genuinely cross-cutting.

### MILESTONE / PRODUCT COMPLETE

This is where broad validation belongs.

Before declaring the milestone/product ready for PR, review, release, or handoff:
- run the repository's full required test suite once;
- run required build/type/lint gates once;
- perform integration/E2E checks that represent critical flows;
- run the security/release gates justified by the affected surface;
- inspect the complete diff for accidental complexity and unrelated churn;
- simplify only demonstrated or obvious waste without redesigning working code.

The principle is:

```text
BUILD: implement -> spot-check -> continue
FEATURE: targeted acceptance -> continue
MILESTONE: full verification -> simplify -> handoff
```

## Verification budget

Verification should be proportional to **risk and blast radius**, not to the amount of ceremony available.

| Situation | During BUILD | At final gate |
|---|---|---|
| Copy/style/static UI | visual/affected smoke check | normal project gate if required |
| Bounded feature logic | focused related tests | full required suite once |
| Cross-module integration | targeted integration check | full suite + critical E2E |
| Auth / payments / permissions | affected boundary tests immediately | full security/release verification |
| Migration / destructive data change | prove rollback + targeted migration checks before continuing | full migration/release gate |
| Concurrency / distributed state | focused race/failure-path checks early | broader reliability verification |

High-risk work is the exception to deferred breadth. A cheap local change at a dangerous boundary is still dangerous.

## Testing rules

Tests exist to buy confidence, not to maximize test count.

Add or strengthen a test when at least one is true:
- the behavior contains meaningful logic;
- the bug should never return;
- the change modifies a public contract;
- the path is business-critical;
- the code is hard to verify manually;
- the risk boundary demands durable evidence.

Usually do not add a new test when:
- behavior is trivial and already covered by a higher-level test;
- the test would only assert implementation details;
- it duplicates another test with no new failure mode;
- it tests framework/library behavior rather than project behavior;
- it exists only to increase coverage percentage;
- it requires a large mock/fixture system for a tiny change.

Never weaken, delete, skip, or rewrite a valid failing test merely to get green.

When a test fails, first assume the failure is useful evidence. Change the test only when the requirement or contract proves the test is wrong.

## Architecture rules

Prefer direct code over speculative structure.

Do not add by default:
- interfaces with one real implementation;
- factories/registries/plugin systems with one current consumer;
- generic event buses for one interaction;
- new service layers that only forward calls;
- config flags for fixed behavior;
- compatibility shims for unreleased behavior;
- new dependencies for a small local problem;
- caches, queues, services, databases, or background workers without a current need;
- helpers extracted solely because two lines look similar.

Use the rule of three as a bias, not a law: duplication can remain until repetition and the correct abstraction are both evident.

A feature flag is justified when incomplete work must be merged/shared safely, staged rollout is required, or production control is a real requirement. Do not add one merely because the feature was implemented in slices on an isolated branch.

## Scope rules

- Touch the fewest files that correctly solve the requirement.
- Reuse current architecture and conventions before inventing a new seam.
- Do not clean unrelated code "while here".
- Do not add documentation unrelated to a changed public contract, durable decision, or operational requirement.
- Do not plan for hypothetical scale without measured pressure.
- Do not broaden the task because a reviewer found a non-blocking improvement nearby; record it separately if useful.

## Agent rules

- Default to one accountable implementer for bounded work.
- Do not create a review committee for a small feature.
- Do not rerun the same successful command without intervening code changes.
- Do not re-plan after every small edit.
- Do not audit the whole repository to validate a local change.
- Do not ask the user to decide reversible implementation trivia when project conventions already answer it.
- Stop when the current phase's evidence exists.

## Interaction with other Agentit skills

When selected with `incremental-implementation`, this skill owns **verification cadence**. Interpret "test/verify each slice" as the smallest relevant check needed to keep the slice sane, not as permission to run the full repository suite/build/lint after every increment.

When selected with `test-driven-development`, use strict red/green where it materially improves correctness: bug regressions, non-trivial logic, contracts, and high-risk behavior. Do not apply ceremonial TDD to trivial glue, static content, or purely presentational changes.

When selected with `verification-before-completion`, "fresh verification" means evidence appropriate to the claim. A feature-level claim needs feature-level evidence; a whole-product "ready" claim needs the full final gate.

When selected with `constraint-driven-development`, preserve the project's declared constraints, but place expensive checks at the lifecycle stage where they provide value instead of running everything everywhere.

## Anti-patterns

Stop and simplify if the implementation starts doing any of these:

- one feature generates a framework;
- one endpoint generates a new architecture layer;
- every edit triggers the full suite;
- every helper gets its own test regardless of behavior;
- tests outnumber meaningful behaviors because every branch was mechanically covered;
- a reviewer keeps finding "nice to have" work and extending the loop;
- the agent adds defensive branches for states the real callers cannot produce;
- the diff expands into unrelated renames, formatting, docs, or refactors;
- more time is spent proving the process than finishing the product.

## Completion criteria

This skill has been followed when:
- current requested functionality is implemented directly;
- no speculative subsystem or abstraction was added without present evidence;
- build-time verification stayed targeted unless risk required more;
- meaningful behavior and affected risk boundaries received appropriate tests/checks;
- the comprehensive repository/release gate ran at the actual final completion boundary, not repeatedly during every small slice;
- the final diff contains no unrelated cleanup or ceremony.
