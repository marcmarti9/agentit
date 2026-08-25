---
name: verification-gauntlet
description: Surround agent work with hard, signal-gated verification probes and anti-greenwash rules. Use before done claims, after implementations, or when tests look too easy; not for pure explanation.
---

# Verification Gauntlet

Inspired by craft practice (hard constraints over line-by-line code reading): agents write code **and** tests, but green self-tests alone are not proof. Agentit adds an external gauntlet.

## When to Use

- Before any done / fixed / shipping claim on non-trivial work
- After implementing behavior, auth, DB, API, or UI changes
- When the agent reports “N tests passed” but confidence is low
- RISK_2+ implementation, or whenever `verification-before-completion` applies

**Not for:** pure explanation with no working-tree claim.

## Layers

| Layer | What |
|-------|------|
| L0 | Project native suite (`pytest`, `flutter test`, `npm test`, …) |
| L1 | Change contract: acceptance criteria + red→green for behavior |
| L2 | Stack probes from `probes/catalog.yaml` (only if signals match) |
| L3 | Anti-greenwash rules (cannot skip to look good) |
| L4 | Human gate RISK_3/4 (existing router policy) |

## Process

### 1. Plan the gauntlet

```bash
agentit verify "short task description" --project .
# or JSON:
agentit verify "…" --project . --format json
```

Read: `signals`, blocking probes, runnable commands, checklists, `anti_greenwash`.

### 2. Apply runnable probes

```bash
agentit verify "…" --project . --apply
```

- Scripts and detectible project commands run automatically.
- Checklist probes stay `pending_agent_evidence` until you fill evidence in the close-out.
- Receipt: `.agentit/verify/<timestamp>-receipt.json`

### 3. Satisfy checklists with evidence

For each pending checklist (examples):

- **change-contract-red-green** — show red command then green command (or explicit pure-refactor waiver)
- **acceptance-criteria** — 3–7 task-specific checks, each pass/fail + proof
- **postgres-rls-discipline** — only if postgres/supabase signals
- **auth-boundary** — only if auth signals

Do **not** mark pass without a command, path, or observed behavior.

### 4. Anti-greenwash (non-negotiable)

- Do not delete, skip, or weaken probes to claim green
- Do not treat agent-authored unit tests as the whole gauntlet when other probes apply
- Do not accept subagent “success” as a receipt for RISK_2+; re-run blocking probes
- “200 tests passed” without receipt path / probe statuses is not completion
- If the working tree changed after tests, re-run verification on the **final** tree
- Router field `verification.claims_without_evidence: forbidden` applies to all done/fixed/passing claims
- Programmatic gate (optional): `router.verify.evaluate_done_claims(claims, receipt=…)`

### 5. Close-out shape

```
VERIFY:
- receipt: .agentit/verify/…
- blocking probes: pass/fail list
- checklists: evidence summary
- residual risk: …
```

Only then may you claim done (`verification-before-completion` still requires fresh command evidence for each claim).

## CLI reference

| Command | Effect |
|---------|--------|
| `agentit verify "task"` | Plan only (default) |
| `agentit verify "task" --apply` | Run runnable probes + write receipt |
| `agentit verify "task" --format json` | Machine-readable plan/receipt |

## Relation to other skills

- **`verification-before-completion`** — iron law of evidence; this skill defines *which* external gates exist
- **`test-driven-development`** — produces red→green for behavior; gauntlet checks you actually observed it
- **`security-and-hardening`** — deeper auth/secrets work; probes are minimum smoke
- **`using-agentit`** — session close-out should include verify receipt when this skill applied

## Red flags

- Skipping `agentit verify` on an implementation task
- Checklist marked pass with no evidence line
- Disabling RLS / auth to green tests
- Only running the happy-path tests the agent just invented
- Claiming browser polish with no build/serve/browser note

## Verification of this skill

- [ ] `agentit verify` plan run for the task
- [ ] `--apply` run when runnable probes exist
- [ ] Receipt path cited
- [ ] Every blocking checklist has evidence or an explicit residual gap
- [ ] No done claim while blocking probes failed
