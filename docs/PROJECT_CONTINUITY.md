# Agentit project continuity contract

Chat/session context is disposable. Substantial work should be resumable after a lost session, provider switch, crash, context exhaustion, or long pause without publishing private working notes into the repository.

## Default state is local and private

Agentit's default operational state lives at:

`.agentit/STATE.md`

`.agentit/` is gitignored by the Agentit repository and should normally remain local/private in projects that adopt the same convention. Machine-readable checkpoints live under `.agentit/checkpoints/*.json`.

If a project already has an intentional, tracked canonical state/status document, Agentit may reuse it. Do not create or commit a public task-state file merely because Agentit is active.

Operational state and durable project documentation are different:

- `.agentit/STATE.md` — current objective, execution state, blockers, next actions, temporary handoff context.
- tracked project docs — durable architecture, interfaces, decisions, operations, and troubleshooting that belong in the product repository.

## Minimum state

```markdown
# Agentit state

## Goal
What is being built/changed and why.

## Confirmed intent
Audience, success criteria, constraints, non-goals.

## Execution decision
Relevant packs, complexity, risk, topology, selected skills/tools/references,
worker ownership, and review requirements.

## Current status
Complete, in progress, blocked, not started.

## Decisions
Compact durable decision summary and reviewer verdicts; never private chain-of-thought.

## Important files and artifacts
Paths, branch/PR, receipts, external artifacts, MCP set when relevant.

## Verification
Fresh commands/checks/receipts and what remains unverified.

## Next actions
Ordered executable steps.

## Open questions / blockers
Anything that still needs user input or external access.

## Recovery
Last checkpoint and exact resume path.
```

## Complexity and planning

Continuity records the semantic `TASK_DECISION`, including `complexity: trivial | bounded | substantial | structural`. It does not impose named quality/depth tiers. The primary AI decides how much work a task deserves and records the actual plan, topology, selected capabilities, and verification strategy.

For substantial or structural work, the agent should normally surface a short user-facing route summary before material execution: what it will inspect/change, major stages, delegation if any, and how completion will be verified. Keep this concise unless the user asks for a full plan.

## Update cadence

Update operational state when it would be expensive to reconstruct later, especially:

1. after the material `TASK_DECISION` and required review;
2. after a material user decision changes scope;
3. after a meaningful milestone;
4. before a provider/session/machine handoff;
5. before stopping because of context/tool/time limits or an error;
6. before final completion when recovery information would still matter.

Do not create continuity ceremony for trivial work.

## Persist

Useful state includes branch/PR identifiers, selected packs/skills/references/tools, complexity/risk/topology, worker ownership, stable decisions, changed files, verification receipts, failures/reproduction steps, blockers, and next actions.

Never persist secrets, credentials, private chain-of-thought, raw chat transcripts, giant tool dumps, or personal plans unrelated to the public project.

## Resume protocol

A fresh agent should:

1. inspect `.agentit/STATE.md` or the explicitly configured project equivalent;
2. inspect the referenced branch/PR/diff and only the files needed next;
3. verify recorded assumptions still hold;
4. repair stale operational state locally;
5. rebuild/review `TASK_DECISION` if scope, risk, or independence materially changed;
6. continue from `Next actions` instead of re-asking already resolved questions.

If cross-machine persistence is needed, use an intentionally chosen private/synced workspace or an existing tracked team status document. Agentit must not auto-publish private operational state to obtain portability.

## Git / PR workflow

Repository changes default to work branch -> verification -> PR -> review/user merge unless explicitly overridden. The implementation and durable project documentation travel in that PR. Local `.agentit/STATE.md` does not.
