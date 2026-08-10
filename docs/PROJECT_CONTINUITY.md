# Agentit project continuity contract

Agentit must treat chat/session context as disposable. A task should be resumable after a lost session, provider switch, machine switch, token exhaustion, crash, or long pause using only the repository plus explicitly referenced external artifacts.

## Canonical project state

For every product-affecting task, maintain a compact repository-tracked continuity file at:

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

## Effort
Standard / Polished / Studio, rough token envelope, and user confirmation.

## Current status
What is complete, in progress, blocked, and not started.

## Decisions
Stable technical/product/design decisions and why they were chosen.

## Important files and artifacts
Paths, branches, PRs, design-system docs, research artifacts, migrations, external references.

## Verification
Commands/checks run, latest known results, and what still needs verification.

## Next actions
Ordered list a fresh agent can execute.

## Open questions / blockers
Anything that still requires the user or external access.
```

## Update cadence

Documentation is part of the work, not a final cleanup step.

Update state:

1. immediately after the interview/effort level is confirmed;
2. after any decision that would be expensive to rediscover;
3. after a meaningful milestone or package is completed;
4. before a provider/model/session handoff;
5. before stopping because of token/context limits, tool limits, time, errors, or user pause;
6. before final completion.

For Standard work, one compact file is enough. Polished/Studio may additionally create focused docs such as ADRs, design direction, research briefs, migration plans, or specs, but `STATE.md` remains the index pointing to them.

## What belongs in state

Persist facts needed to continue:

- branch and PR identifiers;
- confirmed effort level;
- exact current objective and scope;
- architecture/API/data-contract choices;
- chosen design direction and rejected alternatives when relevant;
- installed/required dependencies and their purpose;
- important commands and environment assumptions;
- files changed or owned by current work packages;
- test/verification status;
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
2. inspect the referenced branch/PR/diff and only the files needed for the next action;
3. verify whether recorded assumptions are still true;
4. summarize any stale/missing state and repair the document before continuing;
5. do not restart discovery or interview questions whose confirmed answers are already documented unless the task materially changed.

A new agent/provider should be able to answer: **what are we doing, why, what has been decided, where is the work, what has been verified, and what should I do next?**

## Git / PR persistence

Repository continuity only works if state survives locally and remotely. Agentit therefore uses branch + pull request workflow by default for repository changes. Documentation updates belong on the same work branch/PR as the implementation they describe.

Do not push directly to the default branch or merge the PR unless the user explicitly asks or project instructions explicitly require another workflow.

## Handoff checkpoint

When a session is likely to end before the task is done, leave a checkpoint that is executable rather than narrative. Example:

```markdown
## Current status
- Hero + nav implemented.
- Mobile menu still broken below 390px.
- Design critic pass not run.

## Verification
- `npm test`: pass at commit abc123.
- `npm run build`: pass.
- Playwright mobile check: FAIL, menu overlaps hero.

## Next actions
1. Fix mobile menu in `src/components/Nav.tsx`.
2. Re-run 390px/360px browser checks.
3. Run design critic.
4. Update this state file and PR description.
```

That is sufficient for a fresh session to resume without access to the previous chat.
