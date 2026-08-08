---
name: verification-before-completion
description: Require fresh command evidence before any done/fixed/passing claim. Use before commits, PRs, or success statements; not for pure explanation.
---

# Verification Before Completion

## Overview

**Evidence before claims, always.**

If you have not run the verification command in this turn and read its output, you cannot claim the work passes, is fixed, or is done.

This skill is process law for every non-trivial change. It complements per-skill verification checklists and the Definition of Done.

## When to Use

- About to say tests pass, build is clean, bug is fixed, or feature is complete
- Before commit, PR, push, or handoff
- After a worker or subagent reports "success"
- After a fix that "should work"

**When NOT to use:**

- Pure explanation with no claim about the working tree
- The user only asked for analysis, not completion
- Mechanical renames already covered by an instantaneous, already-run check in the same turn

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

Fresh means: executed in this turn (or since the last code change), full command, full relevant output, exit code checked.

## The Gate Function

Before claiming any status or expressing satisfaction:

1. **IDENTIFY** — What command proves this claim?
2. **RUN** — Execute the full command (not a partial recollection).
3. **READ** — Full output, exit code, failure count.
4. **VERIFY** — Does the output confirm the claim?
   - If NO: state actual status with evidence.
   - If YES: state the claim **with** the evidence (command + summary of result).
5. **ONLY THEN** make the claim.

Skip any step = unverified assertion, not verification.

## Claim → Evidence Map

| Claim | Requires | Not sufficient |
|-------|----------|----------------|
| Tests pass | Test command output: 0 failures | Previous run, "should pass", worker summary |
| Linter clean | Linter output: 0 errors | Partial path check |
| Build succeeds | Build command exit 0 | Types look fine |
| Bug fixed | Repro of original symptom now passes | Code changed, assumed fixed |
| Regression test works | Red then green observed | Test passes once without prior red |
| Agent/worker completed | Diff + verification rerun by owner | Agent said "success" |
| Requirements met | Checklist against acceptance criteria | "Looks good" |

## Red Flags — STOP

- "should", "probably", "seems to", "looks correct"
- Satisfaction language before verification ("Great!", "Perfect!", "Done!")
- Commit/PR without a verification command in this turn
- Trusting subagent success reports without re-checking
- Partial verification used as full proof
- "just this once" / fatigue as excuse
- Any wording that implies success without a command run after the last edit

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Should work now" | RUN the verification |
| "I'm confident" | Confidence ≠ evidence |
| "Just this once" | No exceptions for completion claims |
| "Linter passed" | Linter ≠ tests ≠ runtime |
| "Worker said success" | Owner re-verifies |
| "I'm tired" | Exhaustion is not evidence |
| "Partial check is enough" | Partial proves nothing about the claim |
| "Different words so the rule doesn't apply" | Spirit over letter |

## Interaction with Other Skills

- **`test-driven-development`**: TDD produces the failing-then-passing evidence; this skill forbids claiming green without that evidence in-session.
- **`debugging-and-error-recovery`**: After a fix, re-run the repro command before saying fixed.
- **`code-review-and-quality`**: Reviewers treat worker receipts as claims; demand evidence.
- **`architect-orchestrator`**: Architect accepts packages only after re-running relevant verification on the real tree.
- **Worker Context Contract**: workers must list verification requirements; completion still needs evidence.

## Verification

Before any completion claim:

- [ ] The proving command was identified
- [ ] The command was run after the last relevant change
- [ ] Output was read (exit code / failure count)
- [ ] The claim is stated with that evidence, or the claim is withheld
- [ ] Subagent "success" was not accepted without owner re-check when risk ≥ RISK_2
