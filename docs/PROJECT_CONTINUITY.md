# Agentit project continuity contract

Agentit must treat chat/session context as disposable. A task should be resumable after a lost session, provider switch, machine switch, token exhaustion, crash, or long pause using only the repository plus explicitly referenced external artifacts.

## Canonical project state

For every substantial product-affecting task, maintain a compact repository-tracked continuity file at:

`docs/agentit/STATE.md`

If the project already has an equivalent canonical project-state document, reuse it instead of creating a duplicate and record that choice in the file itself.

The file is operational state, not a transcript. Keep it concise enough that a fresh agent can read it immediately.

Minimum sections:

```markdown
# Agentit state

## Goal
What is being built/changed and why.

## Confirmed intent
Audience, success criteria, constraints, non-goals.

## Domain pack
Pack (engineering/frontend/design/…), craft depth if design/visual only,
effort, topology, whether strong independent review is required.

## Current status
What is complete, in progress, blocked, and not started.

## Decisions
Compact TASK_DECISION summary, economy-reviewer verdict, strong-review verdict
when required, and stable technical/product/design decisions.

## Important files and artifacts
Paths, branches, PRs, design-system docs, research artifacts, migrations,
MCP set, external references.

## Verification
Commands/checks run, receipt paths under `.agentit/verify/`, latest results,
what still needs verification. Done claims require fresh evidence.

## Next actions
Ordered list a fresh agent can execute.

## Open questions / blockers
Anything that still requires the user or external access.

## Recovery
Last checkpoint and how to resume. If scope/risk materially changed, rebuild
TASK_DECISION from current context and review it again before executing.
```

CLI helpers:

```bash
agentit continuity status --project .
agentit continuity init "goal" --project .
agentit continuity checkpoint label --project .
```

Machine-readable checkpoints: `.agentit/checkpoints/*.json`.

## Update cadence

Documentation is part of the work, not a final cleanup step.

Update state:

1. after the primary AI has established the material task decision and required reviewer(s);
2. after any product interview materially changes that decision;
3. after any decision that would be expensive to rediscover;
4. after a meaningful milestone or package is completed;
5. before a provider/model/session handoff;
6. before stopping because of token/context limits, tool limits, time, errors, or user pause;
7. before final completion.

## What belongs in state

Persist facts needed to continue:

- branch and PR identifiers;
- compact `TASK_DECISION` summary rather than private chain-of-thought;
- economy reviewer verdict and material required changes;
- strong critic/judgment verdict when required;
- domain pack / craft depth / effort;
- exact current objective and scope;
- architecture/API/data-contract choices;
- specialist/worker plan and ownership boundaries;
- MCP enablement decisions;
- local model endpoints used (ids only, no secrets);
- files changed or owned by current work packages;
- test/verification status and receipt paths;
- known failures and reproduction steps;
- pending user decisions;
- next executable steps.

Do not persist:

- secrets, tokens, credentials, private keys;
- raw chain-of-thought;
- huge tool dumps or full chat transcripts;
- temporary speculation that no longer affects execution;
- duplicated docs that already have a stable canonical location.

## Resume protocol

At the start of continuing work in an existing project:

1. inspect `docs/agentit/STATE.md` (or the recorded equivalent) before asking the user to repeat prior decisions;
2. run `agentit continuity status --project .` when available;
3. inspect the referenced branch/PR/diff and only the files needed for the next action;
4. verify whether recorded assumptions are still true;
5. summarize any stale/missing state and repair the document before continuing;
6. if scope/risk/independence materially changed, the primary AI rebuilds `TASK_DECISION` from current context and sends the changed proposal through the independent AI review again before execution;
7. do not restart discovery or interview questions whose confirmed answers are already documented unless the task materially changed.

A new agent/provider should be able to answer: **what are we doing, why, what has been decided, how was that decision reviewed, where is the work, what has been verified, and what should I do next?**

## Git / PR persistence

Use a **branch + pull request workflow by default**. Continuity docs travel on the same work branch/PR as the implementation they describe. Do not leave STATE.md only on a disposable machine.

Do not commit directly to the default branch unless the user explicitly asks for that exception on the current task.
