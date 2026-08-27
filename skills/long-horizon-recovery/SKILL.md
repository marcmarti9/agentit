---
name: long-horizon-recovery
description: Keep substantial multi-session Agentit work resumable using private local state, compact checkpoints, and a fresh task decision when a new execution session resumes.
---

# Long-horizon recovery

Chat/session context is disposable. Operational state should survive when the work is substantial enough to justify continuity, without publishing private working notes into the repository.

Continuity is evidence, not context injection. A resumed execution session still starts from Agentit's three-skill core and explicitly re-selects any non-core skills, references, workers and MCPs it still needs.

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
- previously selected skills, tools, references and workers;
- MCPs enabled by this task and cleanup ownership when relevant;
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

1. Start with only the normal three-skill Agentit core as active Agentit context.
2. Read `.agentit/STATE.md` or the explicitly configured equivalent before re-asking resolved user questions.
3. Inspect the referenced branch/PR/diff and only the files needed next.
4. Verify recorded assumptions are still true and repair stale local state.
5. Build a fresh current `TASK_DECISION`; reuse valid facts/user decisions from continuity, but explicitly re-select every non-core skill/reference/worker/MCP that remains justified.
6. Repeat the required independent audit/review for the current decision when applicable.
7. Continue from `Next actions`.

A previously selected skill or MCP is historical evidence, not automatic current activation. A provider may still expose an MCP physically; ignore it unless the fresh current decision selects it again.

## Mid-task decision refresh

When a material change occurs within the same execution session:

1. the primary AI rebuilds the semantic `TASK_DECISION` from current context;
2. repeat the required independent audit/review;
3. update local state with the changed decision and next actions;
4. add/remove JIT skills/references/tools as the new decision requires;
5. only then execute the materially changed route.

Do not call a prompt classifier to make that semantic decision. Software persists the explicit decision; the active AI owns its meaning.

## Cleanup

Before finishing or handing off:

- record which MCPs the task itself enabled;
- disable those task-added MCPs when safe and when the user/project did not intentionally request persistent availability;
- do not disable unrelated user or concurrent-session MCP configuration;
- if the provider cannot unload until restart/reconnect, record that fact and still require fresh re-selection next session.

## Anti-patterns

- publishing transient operational state in a public repository;
- re-interviewing user decisions already recorded and still valid;
- treating previous selected skills/MCPs as automatically active after a new session starts;
- trusting stale chat memory over current repository/evidence;
- continuing a materially changed plan without refreshing review;
- storing secrets, credentials, raw transcripts or private chain-of-thought;
- using named effort/craft tiers instead of recording the actual task decision.

## Verification

- [ ] Continuity was used only if the task warrants it.
- [ ] `.agentit/STATE.md` has enough information for a fresh agent to resume without preserving old active context.
- [ ] State contains actual packs/complexity/risk/topology and prior selected capabilities, not legacy tier labels.
- [ ] A resumed execution session makes a fresh non-core selection from the current task.
- [ ] Next actions and blockers are concrete.
- [ ] Latest verification evidence is recorded.
- [ ] Task-added MCP cleanup ownership is clear when relevant.
- [ ] State/checkpoints remain local/private unless the project explicitly chose another canonical team document.
