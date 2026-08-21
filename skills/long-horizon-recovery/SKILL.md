---
name: long-horizon-recovery
description: Keep multi-session work resumable. Checkpoint STATE, resume without re-interviewing, and rebuild/review the AI task decision when scope changes.
---

# Long-horizon recovery

Chat is disposable. Repository state is not.

## Canonical state

Maintain `docs/agentit/STATE.md` (see `docs/PROJECT_CONTINUITY.md`).

Minimum sections: Goal, Confirmed intent, Domain pack, Current status, Decisions, Important files, Verification, Next actions, Open questions, Recovery.

Useful state fields include:

- domain pack and design craft depth when relevant;
- effort/topology;
- compact `TASK_DECISION` summary;
- economy reviewer verdict;
- strong reviewer verdict when required;
- worker ownership/dependency decisions;
- latest verification evidence.

## Commands

```bash
agentit continuity status --project .
agentit continuity init "goal text" --project .
agentit continuity init "goal text" --project . --apply   # overwrite template
agentit continuity checkpoint milestone-name --project .
```

## When to checkpoint

1. After the material task decision/review is established
2. After product interview decisions materially change the plan
3. After expensive decisions
4. After meaningful milestones
5. Before provider/model/session handoff
6. Before token/context limits or pause
7. Before final completion

Also write `.agentit/checkpoints/*.json` for machine-readable snapshots when useful.

## Resume protocol

1. `agentit continuity status` / read STATE.md **before** re-asking the user
2. Inspect branch/PR/diff referenced
3. Verify assumptions still true
4. Repair stale state
5. Continue from Next actions

## Mid-task decision refresh

If independence, risk, scope, constraints, or important project facts changed materially:

1. the primary AI rebuilds `TASK_DECISION` from the current full context;
2. send the changed proposal through the mandatory economy reviewer again;
3. if the new decision is high-consequence, also run the required strong `critic`/`judgment` review;
4. update STATE before executing the materially changed plan.

Do not call a prompt router or trace classifier; the active AI owns the semantic decision.

## Anti-patterns

- re-interviewing decisions already in STATE
- trusting chat memory over STATE
- continuing a materially changed plan without refreshing/reviewing `TASK_DECISION`
- finishing without updating Next actions / Verification
- storing secrets or private chain-of-thought in STATE/checkpoints

## Verification

- [ ] STATE.md exists and has required sections
- [ ] Decision/reviewer status is clear enough for a fresh agent to continue
- [ ] Next actions are executable by a fresh agent
- [ ] Latest verification results recorded
- [ ] Checkpoint taken before handoff
