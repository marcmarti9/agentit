---
name: reliable-coding
description: Consolidated coding discipline for capable agents. Enforces thinking before coding, simplicity first, surgical changes, and goal-driven verification with fresh evidence. Combines Agentit BUILDER/REVIEW modes, minimum-solution ladder, adversarial doubt, and the iron law of verification. Use for non-trivial implementation, refactors, bug fixes, and reviews. Prefer this over loading multiple overlapping skills (anti-overengineering, doubt-driven-development, verification-before-completion, code-simplification).
---

# Reliable Coding

Behavioral and process contract for material coding work. Bias toward caution and evidence over speed and assumption. For trivial one-line obvious edits, use judgment and stay light.

This skill owns the core coding discipline. Load it when implementing, fixing, refactoring, or reviewing non-trivial code. It absorbs and supersedes the overlapping guidance from anti-overengineering, doubt-driven-development, verification-before-completion, and code-simplification for most cases.

## Core principles (always active)

1. **Think before coding**  
   Do not assume. Surface assumptions, tradeoffs, and confusion explicitly. If uncertain, ask or present alternatives. Do not pick silently when multiple interpretations exist. Push back when a simpler path exists.

2. **Simplicity first**  
   Minimum code that solves the actual problem. Nothing speculative. No features beyond the request. No abstractions for single use. No configurability that was not asked for. If you write 200 lines that could be 50, rewrite.

3. **Surgical changes**  
   Touch only what you must. Clean up only the mess you create. Do not "improve" adjacent code, comments, or formatting. Do not refactor things that are not broken. Match existing style. Every changed line should trace directly to the request.

4. **Goal-driven execution with fresh evidence**  
   Define verifiable success criteria before claiming done. Loop until you have fresh evidence. No completion claims without running the proving command and reading the output. Weak criteria ("make it work") require constant clarification.

## Development modes

```text
DEVELOPMENT_MODE: BUILDER | REVIEW
```

Risk is separate from mode. BUILDER is not permission to ignore high-impact boundaries (auth, payments, destructive data, secrets, migrations, concurrency).

### BUILDER mode (default while functionality is incomplete)

**Goal:** Complete the requested feature set with the smallest viable diff and the cheapest relevant checks.

Default loop:
```text
implement
→ cheapest relevant check
→ fix demonstrated breakage
→ continue
```

#### Minimum-solution ladder
After understanding the real flow and requirement, stop at the first option that correctly solves it:

1. Do we need new behavior at all? Skip speculative requirements.
2. Does this codebase already solve it? Reuse existing helper/type/pattern.
3. Does the standard library solve it? Prefer that.
4. Does the platform/framework already provide it natively? Prefer the native primitive.
5. Does an already-installed dependency solve it cleanly? Reuse before adding another.
6. Can a small direct implementation solve it? Write that.
7. Only then: introduce the minimum new structure required.

This is a decision reflex. Read the affected flow first. A tiny fix at the wrong layer is still a bad fix. For bugs, prefer the smallest root-cause fix at the shared seam over duplicating guards across callers.

#### Verification budget in BUILDER
Use the smallest signal that can catch an obvious mistake in the code just changed:
- compile/typecheck the affected surface when relevant;
- one focused test or directly related test group for meaningful logic;
- targeted browser/runtime smoke for UI/integration;
- inspect the actual changed path;
- immediate targeted check on any affected high-risk boundary.

Then continue. Do not run the full suite after every edit.

#### Do not do by default in BUILDER
- Full repository test suite after every feature or edit.
- Full lint + typecheck + build + E2E repeatedly.
- Broad security/performance/accessibility audits unrelated to current risk.
- New tests for trivial wrappers, static copy, or already-covered behavior.
- Reviewer/subagent committees for bounded implementation.
- Unrelated refactors, formatting sweeps, or "while I'm here" cleanup.
- Architecture redesign because current code is not aesthetically ideal.
- Documentation churn after each slice.
- Commit/review ceremony after every tiny change.

A failed targeted check is evidence. Fix it and rerun the relevant check. Do not widen the surface unless the failure shows wider blast radius.

### REVIEW mode

**Goal:** Deeply validate and simplify the completed implementation without expanding feature scope.

Entering REVIEW freezes requested functionality. You may fix defects, regressions, security issues, performance problems, and unnecessary complexity. You do not invent new product features.

Default loop:
```text
inspect complete diff/system
→ run broad required gates
→ identify concrete findings
→ fix in batches
→ targeted recheck
→ rerun broad final gate
→ report evidence
```

Review surfaces justified by the change: acceptance criteria, full required test suite, build/type/lint, integration/E2E, runtime behavior, security/trust boundaries, migrations, performance where relevant, accessibility for affected flows, docs drift, and the complete diff for dead code or unrelated churn.

Findings need concrete evidence or a clear violated contract. Batch fixes. Do not chase speculative edge cases whose preconditions cannot occur. Non-blocking nice-to-haves become follow-up work.

## Hard justification rule

Every new production abstraction, test, dependency, document, worker, review pass, or verification command must be justified by at least one of:

1. a current explicit requirement;
2. an observed bug/regression;
3. an established project contract/invariant;
4. a real risk boundary affected by the change.

"Could be useful", "best practice", "future-proof", "more flexible", and "just to be safe" are not enough.

## Think before coding (doubt and assumptions)

Before implementing:
- State assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them.
- If a simpler approach exists, say so and push back when warranted.
- If something is unclear, stop. Name what is confusing.

For non-trivial decisions (branching logic, cross-boundary effects, unverifiable properties, high blast radius):
- Formalize the decision as an explicit claim with rationale.
- Isolate the smallest reviewable unit (diff, function, or proposal) plus its contract.
- Subject it to adversarial scrutiny in fresh context when possible (ask "how would this fail?" rather than "is this good?").
- Bound the doubt cycles. Escalate to the user if substantive issues persist after a couple of rounds.

Trivial formatting, renames, or obvious fixes do not require this ceremony.

## Surgical changes

When editing existing code:
- Do not improve adjacent code, comments, or formatting.
- Do not refactor things that are not broken.
- Match existing style even if you would do it differently.
- If you notice unrelated dead code, mention it; do not delete it unless asked.

When your changes create orphans:
- Remove imports, variables, or functions that *your* changes made unused.
- Do not remove pre-existing dead code unless asked.

The test: every changed line should trace directly to the user's request.

## Goal-driven verification (iron law)

**No completion claims without fresh verification evidence.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass."
- "Fix the bug" → "Write a test that reproduces it, then make it pass."
- "Refactor X" → "Ensure tests pass before and after."

Gate process before any success claim:
1. Identify the command that proves the claim.
2. Run the full command freshly.
3. Read the output, check exit code, count failures.
4. Confirm the output actually supports the claim.
5. Only then claim success, citing the evidence. Otherwise state the actual status.

Red flags that mean you are not verifying:
- Words like "should", "probably", "I think it works".
- Expressing satisfaction ("Great!", "Done!") before evidence.
- Committing or opening a PR without verification.
- Trusting another agent's report without independent check.
- Relying on partial checks or stale output.

Strong success criteria let you loop independently. Weak criteria require constant clarification.

## Risk override

Regardless of mode, verify dangerous boundaries early enough to avoid compounding damage:
- auth/session/authorization;
- payments/financial effects;
- destructive migrations or irreversible writes;
- secrets/credentials;
- production data;
- concurrency/distributed state;
- externally visible irreversible actions.

The override is targeted to the risk. It does not automatically turn BUILDER into a full REVIEW.

## Mode transitions

Enter **BUILDER** when implementing a new feature, continuing incomplete work, fixing construction issues, or the user says build/implement/finish/create/continue. BUILDER is the default for active implementation.

Enter **REVIEW** when the requested feature set is functionally complete and being prepared for handoff/PR/release, or the user explicitly asks for review/audit/hardening/production readiness. Do not oscillate after every feature. Finish the planned build first unless a genuine blocking risk requires intervention.

## Interaction with other skills

When this skill is loaded, it owns coding discipline, verification cadence, and the default stance on simplicity and surgical changes.

- Prefer this skill over separately loading `anti-overengineering`, `doubt-driven-development`, `verification-before-completion`, or `code-simplification` for ordinary implementation work.
- `test-driven-development`: use strict red/green for bugs, non-trivial logic, contracts, and high-risk behavior. Do not apply ceremonial TDD to trivial glue or presentational work.
- `verification-gauntlet`: load additionally when the project supports Agentit's external probes and you need the full anti-greenwash gauntlet.
- `spec-driven-development` / `constraint-driven-development`: respect project constraints and specs, but place expensive checks in REVIEW unless the constraint explicitly requires them earlier.
- Specialist skills (security, performance, etc.) still load JIT when the surface actually applies.

## Anti-patterns

Stop and simplify if:
- one feature creates a framework;
- every edit triggers the full suite;
- every helper gets a test regardless of behavior;
- reviewers keep extending scope with nice-to-haves;
- defensive branches appear for impossible states;
- the diff expands into unrelated cleanup;
- more time is spent proving process compliance than finishing the requested product;
- assumptions are hidden and the agent runs ahead;
- "done" is claimed without fresh command evidence.

## Completion criteria

The skill is followed when:
- assumptions and tradeoffs were surfaced before implementation;
- the solution stopped at the first sufficient option on the minimum-solution ladder;
- the diff is surgical and every changed line traces to the request;
- BUILDER used proportional targeted checks and did not claim production readiness;
- REVIEW (when entered) performed deep validation with fresh broad evidence;
- high-risk boundaries received timely targeted verification;
- no completion claim was made without fresh evidence from the proving command;
- tests and abstractions exist because they buy current value, not future speculation.

These guidelines are working if: fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, clarifying questions come before implementation rather than after mistakes, and "done" is backed by observable evidence.
