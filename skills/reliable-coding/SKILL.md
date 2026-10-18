---
name: reliable-coding
description: Practical coding discipline for material implementation, bug fixes, refactors and reviews. One JIT owner for simplicity, surgical changes, bounded adversarial thinking and fresh verification evidence. Prefer it to stacking anti-overengineering, doubt-driven-development, verification-before-completion and code-simplification for ordinary coding tasks.
---

# Reliable Coding

A lightweight execution companion to Agentit's three-skill global core. The canonical BUILDER/REVIEW policy, transitions, security gates and authority boundaries stay in `skills/task-router/SKILL.md`. This skill adds concrete working habits; it never overrides the core or automatically loads other skills.

Use it for non-trivial implementation or code review. Skip it for obvious one-line edits when no special process is needed. A selected skill must be loaded JIT; profile installation alone does not load it.

## Four operating rules

1. **Think before editing.** Read the affected code and its contract. Surface consequential assumptions. Ask only when a material choice cannot be resolved from the project; for small reversible ambiguity, state a reasonable assumption and proceed.
2. **Ship the minimum sufficient solution.** Solve the present requirement; do not build for hypothetical future cases. Prefer a native primitive or existing helper over new layers.
3. **Make surgical changes.** Match local conventions. Avoid drive-by refactors, extra configuration, unnecessary tests and documentation churn. Remove the unused artifacts that *your own change* creates.
4. **Verify before claiming success.** Use freshly observed checks that actually prove the scoped claim. Report what was tested and what remains unverified. A passed unit test does not prove production behavior.

## Minimum-solution ladder

After understanding the behavior and failure path, take the first solution that genuinely addresses the root cause:

1. Is any code change needed, or is the requested behavior already present?
2. Does the repository already provide the capability?
3. Can the standard library or platform/framework do it natively?
4. Does an installed dependency provide a suitable implementation?
5. Can a small direct implementation solve it?
6. Only then introduce the smallest justified new abstraction or dependency.

A tiny patch in the wrong layer is not a minimal fix. Do not duplicate guards across callers when one shared root-cause repair is correct.

## BUILDER: execute, check, continue

BUILDER applies while requested functionality is unfinished. Follow the core's policy and keep the loop small:

`inspect affected path → implement → cheapest relevant check → fix demonstrated failure → continue`

- Focused tests for meaningful logic; compile/typecheck for touched surfaces; browser/runtime smoke when UI or integration behavior changed.
- Do not repeatedly run the entire suite, create reviewer committees or audit unrelated code between small edits.
- Tests are justified by behavior, a reported regression, a contract, or a real risk boundary. Do not test trivial wrappers just to raise coverage.
- Security-sensitive paths (credentials, auth, money, irreversible writes, production data, concurrency) need timely targeted verification even during BUILDER.
- Finish implementation before extensive REVIEW unless an actual blocker makes continuing unsafe.

## REVIEW: verify the completed scope

When the user asks for a review, or the feature is ready for handoff, freeze new feature scope and inspect the whole relevant diff. Apply the repository's broad required tests/build gates, relevant integration or user-flow checks, and affected risk boundaries.

- Classify findings by demonstrated defect, violated contract or reproducible risk; avoid speculative refactors.
- Fix related issues in batches, rerun focused checks, then the required final broad gate.
- Keep unproven or environment-dependent claims explicitly qualified.
- Do not treat your own second read as an independent reviewer or claim a deployed result from local tests.
- Security/QA specialists remain available JIT when their distinct expertise actually changes the result.

## Doubt without ceremony

For material branching decisions, uncertain cross-service contracts or irreversible effects, record a short claim and ask: *What concrete condition would make this wrong?* Check against the actual code, tests or an authorized independent reviewer where justified.

Do not require an adversarial worker, repeated confirmations or a cross-model consultation for routine changes. Stop the doubt cycle once the decision has adequate evidence or a genuine unresolved blocker is identified.

## Scope and evidence

Every new production abstraction, dependency, document, worker or expensive verification pass needs a present requirement, demonstrated regression, binding project contract or affected real risk. “Future-proof” is not a reason.

Before reporting completion:

- Inspect the final diff and ensure each change serves the request.
- Run the commands or direct observations that prove the specific claims you will make; read exit status and meaningful output.
- Distinguish targeted BUILDER checks from final REVIEW evidence.
- State outstanding risks, unavailable credentials and external actions not actually performed.
- Follow the core's branch/PR, documentation-drift and user-authorization boundaries.

## Relationship with other skills

This is the usual JIT owner for general coding discipline, not a replacement for specialists. Avoid simultaneously loading `anti-overengineering`, `verification-before-completion`, `doubt-driven-development` and `code-simplification` merely to repeat the same baseline. Select an original specialist *instead* when its deeper, distinct procedure is the actual task (for example, dedicated behavior-preserving simplification or formal adversarial review).

For meaningful logic or regression work, `test-driven-development` may add red/green evidence. For release gates, `verification-gauntlet` and `app-security-gate` remain separate when justified. The core `task-router` is authoritative whenever instruction wording differs.

The desired outcome is fewer unnecessary changes, faster implementation, proportionate tests and truthful evidence—without giving up correctness.
