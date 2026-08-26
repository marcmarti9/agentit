---
name: long-horizon-recovery
description: Keep substantial multi-session Agentit work resumable using private local state, compact checkpoints, and a refreshed TASK_DECISION when scope or risk changes.
---

# Long-horizon recovery

Chat/session context is disposable. Operational state should survive when the work is substantial enough to justify continuity, without publishing private working notes into the repository.

## Canonical state

Default local state:

- `.agentit/STATE.md`
- `.agentit/checkpoints/*.json`

See `docs/PROJECT_CONTINUITY.md`.

Do not create or commit `docs/agentit/STATE.md` merely because Agentit is active. If a project already has an intentional tracked team-status document, it may be reused explicitly; otherwise operational state stays local/private.

A useful state snapshot includes:

- goal and confirmed constraints;
- relevant packs;
- `complexity: trivial | bounded | substantial | structural` when material;
- risk and topology;
- selected skills, tools, references and workers;
- ownership boundaries;
- compact `TASK_DECISION` summary and reviewer verdicts;
- branch/PR and important artifacts;
- latest verification evidence;
- blockers and executable next actions.

Do not persist private chain-of-thought. Record decisions, evidence and consequences only.

## Commands

```bash
agentit continuity status --project .
agentit continuity init "goal text" --project .
agentit continuity init "goal text" --project . --apply
agentit continuity checkpoint milestone-name --project .
```

These commands are agent-facing mechanical helpers; users should not need to operate them manually.

## When to checkpoint

Use continuity when reconstruction would be meaningfully expensive. Typical moments:

1. after the material task decision and required review;
2. after a user decision materially changes scope;
3. after an expensive-to-rediscover milestone or architectural decision;
4. before a provider/model/session/machine handoff;
5. before stopping because of context/tool limits or an error;
6. before completion when recovery information still matters.

Do not create continuity ceremony for trivial work.

## Resume protocol

1. Read `.agentit/STATE.md` or the explicitly configured equivalent before re-asking resolved questions.
2. Inspect the referenced branch/PR/diff and only the files needed next.
3. Verify recorded assumptions are still true.
4. Repair stale local state.
5. Rebuild and review `TASK_DECISION` if scope, risk, independence or important constraints changed.
6. Continue from `Next actions`.

## Mid-task decision refresh

When a material change occurs:

1. the primary AI rebuilds the semantic `TASK_DECISION` from current context;
2. repeat the required independent audit/review;
3. update local state with the changed decision and next actions;
4. only then execute the materially changed route.

Do not call a prompt classifier to make that semantic decision. Software persists the explicit decision; the active AI owns its meaning.

## Anti-patterns

- publishing transient operational state in a public repository;
- re-interviewing decisions already recorded and still valid;
- trusting stale chat memory over current repository/evidence;
- continuing a materially changed plan without refreshing review;
- storing secrets, credentials, raw transcripts or private chain-of-thought;
- using named effort/craft tiers instead of recording the actual task decision.

## Verification

- [ ] Continuity was used only if the task warrants it.
- [ ] `.agentit/STATE.md` has enough information for a fresh agent to resume.
- [ ] State contains actual packs/complexity/risk/topology and selected capabilities, not legacy tier labels.
- [ ] Next actions and blockers are concrete.
- [ ] Latest verification evidence is recorded.
- [ ] State/checkpoints remain local/private unless the project explicitly chose another canonical team document.
