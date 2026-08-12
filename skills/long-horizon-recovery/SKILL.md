---
name: long-horizon-recovery
description: Keep multi-session work resumable. Checkpoint STATE, resume without re-interviewing, mid-task re-route when scope changes. Use for long tasks, handoffs, or context pressure.
---

# Long-horizon recovery

Chat is disposable. Repository state is not.

## Canonical state

Maintain `docs/agentit/STATE.md` (see `docs/PROJECT_CONTINUITY.md`).

Minimum sections: Goal, Confirmed intent, Domain pack, Current status, Decisions, Important files, Verification, Next actions, Open questions, Recovery.

Domain pack fields replace universal Studio effort:

- pack / craft depth (design only) / spend / token estimate / topology / critic_required

## Commands

```bash
agentit continuity status --project .
agentit continuity init "goal text" --project .
agentit continuity init "goal text" --project . --apply   # overwrite template
agentit continuity checkpoint milestone-name --project .
```

## When to checkpoint

1. After interview confirmation
2. After expensive decisions
3. After meaningful milestones
4. Before provider/model/session handoff
5. Before token/context limits or pause
6. Before final completion

Also write `.agentit/checkpoints/*.json` for machine-readable snapshots when useful.

## Resume protocol

1. `agentit continuity status` / read STATE.md **before** re-asking the user
2. Inspect branch/PR/diff referenced
3. Verify assumptions still true
4. Repair stale state
5. Continue from Next actions

## Mid-task re-route

If independence, risk, or scope changed:

```bash
agentit trace "updated current goal" --project .
```

If `critic_required`, re-run independent critic before more implementation.

## Anti-patterns

- re-interviewing decisions already in STATE
- trusting chat memory over STATE
- finishing without updating Next actions / Verification
- storing secrets in STATE or checkpoints

## Verification

- [ ] STATE.md exists and has required sections
- [ ] Next actions are executable by a fresh agent
- [ ] Latest verification results recorded
- [ ] Checkpoint taken before handoff
