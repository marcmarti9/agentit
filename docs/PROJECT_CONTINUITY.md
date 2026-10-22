# Agentit project continuity contract

Chat/session context is disposable. Substantial work should be resumable after a lost session, provider switch, crash, context exhaustion, or long pause without publishing private working notes into the repository.

Continuity preserves **evidence and resumable state**, not active model context. A resumed session still starts semantically cold from Agentit's three-skill core and makes a fresh decision about non-core skills, references, tools and workers.

## Default state is local and private

Agentit's default operational state lives at:

`.agentit/STATE.md`

`.agentit/` stays local/private. Before private writes, the runtime checks that
its contents are untracked and excluded from project Git. If needed, init or a
checkpoint appends an exact project-relative rule to the repository's local
`info/exclude`, resolving the actual Git path for linked worktrees and nested
project directories. The tracked `.gitignore` and existing private content stay
unchanged. Machine-readable checkpoints live under `.agentit/checkpoints/*.json`.

Tracked private content, unsafe symlinks, broken/unverifiable Git state or an
overriding ignore rule block the write. Status/reading does not silently repair
exclusions; an empty unlinked status remains read-only. If existing private
state lacks exclusion, initialize its privacy deliberately before continuing.
If it is tracked, review exposure and untracking explicitly; Agentit does not
delete it or rewrite published history. Deliberate `git add -f` can bypass Git
ignore rules, so staged changes still need inspection. Non-Git projects retain
private filesystem state without requiring Git.

If a project already has an intentional, tracked canonical state/status document, Agentit may reuse it. Do not create or commit a public task-state file merely because Agentit is active.

Operational state and durable project documentation are different:

- `.agentit/STATE.md` — current objective, execution state, blockers, next actions, temporary handoff context.
- tracked project docs — durable architecture, component responsibilities, interfaces, decisions, operations, failure/recovery procedures and verification that belong in the product repository.

## Minimum state

```markdown
# Agentit state

## Goal
What is being built/changed and why.

## Confirmed intent
Audience, success criteria, constraints, non-goals.

## Execution decision
Relevant packs, complexity, risk, topology, previously selected skills/tools/references,
worker ownership, MCPs enabled by the task, cleanup ownership, and review requirements.

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

Continuity records the previous semantic `TASK_DECISION`, including `complexity: trivial | bounded | substantial | structural`. It does not impose named quality/depth tiers. The primary AI decides how much work a task deserves and records the actual plan, topology, selected capabilities, and verification strategy.

Recorded selections are **not automatic reactivation instructions**. On resume, they are evidence about the previous route. The fresh session re-checks current scope, repository state, freshness, availability and risk before selecting non-core skills/references/MCPs again.

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

Useful state includes branch/PR identifiers, previous packs/skills/references/tools, complexity/risk/topology, worker ownership, task-added MCPs and cleanup ownership, stable decisions, changed files, verification receipts, failures/reproduction steps, blockers, and next actions.

Never persist secrets, credentials, private chain-of-thought, raw chat transcripts, giant tool dumps, or personal plans unrelated to the public project.

## Resume protocol

A fresh agent should:

1. start from the three-skill Agentit core, not from the previous task's injected skill/tool context;
2. inspect `.agentit/STATE.md` or the explicitly configured project equivalent as resumable evidence;
3. inspect the referenced branch/PR/diff and only the files needed next;
4. verify recorded assumptions still hold;
5. repair stale operational state locally;
6. rebuild/review the current `TASK_DECISION` and explicitly re-select any non-core skills, references, workers or MCPs still justified;
7. continue from `Next actions` instead of re-asking already resolved user decisions.

A recorded MCP may still be configured/exposed by the provider. That is availability, not current authorization. Do not use it until the fresh decision selects it again. Clean up task-owned MCP enablement when safe and no longer needed.

If cross-machine persistence is needed, use an intentionally chosen private/synced workspace or an existing tracked team status document. Agentit must not auto-publish private operational state to obtain portability.

## Opt-in private cross-machine continuity

A project can sync **only** its compact `.agentit/STATE.md` to a **separate, access-controlled private Git repository**. This is **not** the project's regular Git remote. Checkpoints, transcripts, secrets and local MCP/provider configuration remain private/local. Do not put secrets or credentials into STATE.md: a private Git repository is access-controlled, not end-to-end encrypted.

Configure **once on each machine** (an SSH key or Git credential helper must already have access; do not embed tokens in URLs):

```bash
# This repository must already exist and be PRIVATE.
agentit continuity link git@github.com:YOUR-USER/private-agentit-state.git --project . --apply

# When starting or resuming meaningful work, recover current remote state:
agentit continuity status --project .

# After updating .agentit/STATE.md, or before handing off to another PC:
agentit continuity checkpoint milestone-name --project .
agentit continuity sync --project .
```

A stable project key is derived from the project's Git `origin` URL (SSH and HTTPS GitHub URLs normalize to the same key). Without a portable origin, pass an explicit shared key as the second positional argument to `link` (for example `link REMOTE natursun --apply`) and reuse it on each machine. The local gitignored `.agentit/continuity-sync.json` stores the linkage and a last-synced fingerprint. Run `agentit continuity unlink --project . --apply` to disable sync without deleting local or remote state.

When linked, `continuity status` and `continuity init` reconcile **before** reading/creating state; `continuity checkpoint` reconciles after the local checkpoint. `continuity sync` also performs the same pull/push explicitly. An ordinary Git fast-forward push and the last-synced fingerprint prevent silent overwrites of divergent work. Concurrent changes and unavailable remotes **fail closed**: no force push or implicit merge occurs.

For deliberate conflict resolution, compare both versions, then choose one:

```bash
agentit continuity sync --resolve local --apply --project .
agentit continuity sync --resolve remote --apply --project .
```

The displaced version is preserved under private `.agentit/conflicts/` before replacement. `--resolve local` still uses a fast-forward Git push; a concurrent remote update causes the push to fail. For offline work, `agentit continuity status --offline --project .` and `checkpoint --offline` avoid contacting the remote. Offline work is **not synced** until a later successful call; conflicts must be reconciled on reconnect.

This sync is command-triggered, not an always-on daemon or automatic capture of chat transcripts. Agents must write useful STATE.md content and call continuity at cold start, meaningful milestones and handoff. Context not saved before a crash cannot be recovered.

### Transport boundaries

The continuity remote must differ from the project's normal origin. SSH/HTTPS
spellings of the same GitHub repository, local/file URLs and local symlink
aliases cannot bypass this check. The check also applies to previously saved
links; it does not establish that a different repository is private. The caller
must still verify access controls before linking. Agentit never creates or links
a new cloud repository implicitly.

Link, unlink and sync share a project lock. Failed initial synchronization leaves
no newly enabled link. Divergent versions preserve the local state and save a
private, hash-named remote snapshot for comparison. Explicit resolution still
preserves the displaced version and never force-pushes.

The Git transport disables hooks and filesystem-monitor callbacks, avoids
checking out remote files, and writes the one selected state blob without clean
or smudge filters. Existing unrelated remote files remain in their Git tree.
Normal authentication helpers remain available; credentials are neither embedded
in transport URLs nor copied to another machine.

## Verified machine handoff

State synchronization moves the compact working notes. It does not move the
project's code, verify an installed skill library, or transfer evidence files.
`continuity status` therefore labels its `resumable` result as
`local-state-structure` and explicitly does not claim cross-machine verification.

A private handoff directory adds the missing receiving-side checks. It contains
the complete state, an inert `RESUME.md`, a versioned manifest, and only the
explicitly selected evidence files. The manifest records:

- normalized project identity and exact Git commit/branch;
- hashes and sizes of the three core bodies and explicitly selected skill bodies;
- profile IDs and their resolved membership as historical metadata;
- state and artifact paths, byte counts and SHA-256 hashes.

No skill bodies, credentials, provider settings, host grants, browser sessions,
databases or automatic execution instructions travel in this package. Project
code travels through normal Git. The receiving agent starts from a fresh core
decision; past selections do not reactivate themselves.

### Prepare on machine A

Update `.agentit/STATE.md` with real decisions, evidence, blockers and an
executable next step. Commit the intended code changes to the reviewed branch
and publish them using the project's authorized Git workflow. A handoff refuses
dirty tracked or untracked code; it never silently exports a working tree.

These are agent-facing commands; the user can simply ask to continue on another
machine:

```sh
# Preview first: no package or configuration is written.
agentit continuity handoff --project . --output .agentit/next-pc \
  --skill long-horizon-recovery --artifact docs/verification-summary.md

# Create the reviewed package in a new private directory.
agentit continuity handoff --project . --output .agentit/next-pc \
  --skill long-horizon-recovery --artifact docs/verification-summary.md --apply
```

Select the skills and evidence relevant to the actual task, not the example
unconditionally. `--profile ID` records profile metadata without loading or
selecting every member. The output parent must already exist; the output itself
must be new. Outputs inside the project must be ignored by project Git. Directory
mode is 0700 and files are 0600.

Transfer the directory through an explicitly authorized private channel. This
feature provides no cloud account, background daemon or encryption service.
Publishing the code and transferring the private handoff are separate actions.
Preparation records the code SHA but does not certify its availability on a
remote server; machine B must actually obtain that exact commit.

### Resume on machine B

Obtain the same project/commit through normal Git and provision the required
Agentit core/skills locally using the reviewed installer. Locations and provider
names may differ. Then inspect before applying:

```sh
agentit continuity inspect /private-transfer/next-pc --project .
agentit continuity resume /private-transfer/next-pc --project . --apply
```

`ready: false` or exit 2 means a check blocked the operation. The report explains
the mismatch without running commands from the incoming files. Wrong project,
wrong commit, dirty destination, stale/missing selected skills, profile drift,
corrupt/missing files, unsafe paths and unsupported schemas block restoration.
Equal selected body bytes remain compatible even when one machine loads a
managed cache and another loads the harness directly.

A differing existing state requires a deliberate choice. After comparing both
versions, `resume ... --replace-state --apply` retains the displaced state in a
private backup. Artifacts are restored under `.agentit/received/`, never over
project source. Repeated imports validate the actual bytes and are idempotent;
altered received files or concurrent state edits are preserved and reported.
The exact incoming manifest is retained beside the received artifacts as
`handoff-manifest.json`, so its commit and skill fingerprints remain available
after the transfer directory is removed.

### Evidence and limitations

Every transferred file must be regular, bounded and free of symlink/traversal
paths. Artifacts are explicit files, not recursive folders. Current limits are
32 artifacts, 1 MiB per file and 8 MiB total content. Credential/configuration,
database and transcript paths are refused. A marker filter refuses obvious
secret-like content without printing it; it cannot certify the absence of all
personal or sensitive data. Review the selected material before transfer.

Hashes detect accidental corruption and stale context, not a malicious producer
that rewrites both content and hashes. State and `RESUME.md` remain untrusted
source data: they cannot grant tools, waive project constraints, authorize a
deployment, or substitute for current verification. This protocol does not
transfer unsaved chat context, running processes or in-memory database state.

`router/test_handoff.py` exercises separate actual Git clones and changed roots;
`router/test_continuity_sync.py` exercises two local projects and a bare private
remote. These are local integration tests, not evidence that two physical
computers or a user's real remote have been connected.

## Git / PR workflow

Repository changes default to work branch -> verification -> PR -> review/user merge unless explicitly overridden. For substantial repository work, the documentation-drift check is part of verification and must pass before the PR handoff. The implementation and durable project documentation travel in that PR. Local `.agentit/STATE.md` does not.
