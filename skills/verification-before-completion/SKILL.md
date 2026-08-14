---
name: verification-before-completion
description: Require fresh evidence before any done/fixed/passing claim. Under Agentit, also require the applicable Loop/Graph runtime receipt.
---

# Verification Before Completion

## Overview

**Evidence before claims, always.**

If you have not run the verification command in this turn and read its output, you cannot claim the work passes, is fixed, or is done.

When Agentit is active, fresh command evidence is necessary but not sufficient: the applicable runtime gate must also pass. Direct/single-unit executable work requires a passed **Loop Receipt**; multi-node work requires a passed **Graph Receipt**, whose nodes are themselves backed by bound Loop Receipts.

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

```text
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
AGENTIT ACTIVE => NO COMPLETION CLAIM WITHOUT THE APPLICABLE RUNTIME RECEIPT
```

Fresh means: executed in this turn (or since the last code change), full relevant command/output, exit code checked. Runtime receipt means produced from current `.agentit/runtime/` state after the last relevant change, not copied from another node/run.

## The Gate Function

Before claiming any status or expressing satisfaction:

1. **IDENTIFY** — What evidence proves this claim?
2. **RUN** — Execute the full verifier, not a partial recollection.
3. **READ** — Full relevant output, exit code, failure count.
4. **RECORD** — Under Agentit, record the attempt in the Loop runtime.
5. **RUNTIME CHECK** —
   - direct/single executable unit: `runtime_cli.py loop-check ...` must pass;
   - multi-node execution: each completed node must be accepted by `graph-complete`, then `runtime_cli.py graph-check ...` must pass at the end.
6. **VERIFY** — Does command evidence + runtime receipt confirm the claim?
   - If NO: state actual status with evidence.
   - If YES: state the claim with evidence/receipt summary.
7. **ONLY THEN** make the claim.

Skip any required step = unverified assertion, not verification.

## Claim → Evidence Map

| Claim | Requires | Not sufficient |
|-------|----------|----------------|
| Tests pass | Test command output: 0 failures | Previous run, "should pass", worker summary |
| Linter clean | Linter output: 0 errors | Partial path check |
| Build succeeds | Build command exit 0 | Types look fine |
| Bug fixed | Repro of original symptom now passes | Code changed, assumed fixed |
| Regression test works | Red then green observed | Test passes once without prior red |
| Agentit direct unit completed | Fresh verifier evidence + passed Loop Receipt | Agent/worker narrative success |
| Agentit graph completed | Passed Graph Receipt with bound node Loop Receipts | All workers separately saying "done" |
| Agent/worker completed | Diff + verification rerun by owner + required receipt under Agentit | Agent said "success" |
| Requirements met | Checklist against acceptance criteria + applicable receipt | "Looks good" |

## Agentit Runtime Receipt Gate

The runtime is the acceptance ledger, not a replacement for the actual verifier.

For direct work:

```bash
python3 ~/code/agentit/router/runtime_cli.py loop-check \
  --state .agentit/runtime/loops/<task-id>.json \
  --receipt .agentit/runtime/receipts/<task-id>.json
```

For multi-node work:

```bash
python3 ~/code/agentit/router/runtime_cli.py graph-check \
  --state .agentit/runtime/graph.json \
  --receipt .agentit/runtime/graph-receipt.json
```

Reject completion when:

- the receipt is missing, stale, malformed or for a different contract;
- a node receipt is reused for another node;
- expected artifacts are absent;
- a dependency is still pending/blocked;
- the graph or loop has exhausted its budget/escalated;
- the verifier was weakened/changed merely to obtain a pass.

## Red Flags — STOP

- "should", "probably", "seems to", "looks correct"
- Satisfaction language before verification ("Great!", "Perfect!", "Done!")
- Commit/PR without a verification command in this turn
- Agentit completion claim without Loop/Graph Receipt
- Trusting subagent success reports without re-checking
- Partial verification used as full proof
- Reusing evidence or receipts from a different node/contract
- "just this once" / fatigue as excuse
- Any wording that implies success without a command run after the last edit

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Should work now" | RUN the verification |
| "I'm confident" | Confidence ≠ evidence |
| "Worker said success" | Validate receipt and re-verify as required |
| "All agents finished" | Graph is not done until `graph-check` passes |
| "The tests passed once" | Receipt must match the current loop contract/state |
| "Linter passed" | Linter ≠ tests ≠ runtime |
| "I'm tired" | Exhaustion is not evidence |
| "Partial check is enough" | Partial proves nothing about the full claim |
| "Different words so the rule doesn't apply" | Spirit over letter |

## Interaction with Other Skills

- **`test-driven-development`**: TDD produces failing-then-passing evidence; this skill forbids claiming green without it.
- **`debugging-and-error-recovery`**: After a fix, re-run the repro before saying fixed.
- **`code-review-and-quality`**: Reviewers treat worker receipts as claims; demand evidence.
- **`architect-orchestrator`**: Architect accepts graph nodes only through bound Loop Receipts and re-verifies integrated state as appropriate.
- **Worker Context Contract**: workers receive verifier/stop conditions; Loop runtime records their attempts.
- **`runtime_cli.py`**: persistent enforcement surface for Loop/Graph state under `.agentit/runtime/`.

## Verification

Before any completion claim:

- [ ] The proving verifier was identified
- [ ] It ran after the last relevant change
- [ ] Output/evidence was actually read
- [ ] Under Agentit, the attempt was recorded in Loop runtime
- [ ] The applicable Loop/Graph check passed and receipt matches current state
- [ ] Subagent "success" was not accepted without receipt validation/owner re-check when appropriate
- [ ] The claim is stated with evidence, or withheld
