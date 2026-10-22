---
name: git-workflow-and-versioning
description: Organize Git branches, coherent milestone commits, failure checkpoints, worktrees, authorized remote handoffs and releases. Use when history, recovery or publication needs explicit care.
license: Apache-2.0
---

# Git Workflow and Versioning

Agentit-owned operational adaptation. The verbatim upstream source is retained at `vendor/agent-skills/git-workflow-and-versioning/SKILL.md`; provenance and license records remain authoritative for that source.

Use the repository's branching, versioning and review conventions. Agentit's `task-router` owns development modes and verification cadence. This skill supplies Git safety and handoff practices; it does not authorize commits, pushes, merges, releases or deletion.

## Establish the working state

Before changing branches or history, inspect the repository root, current branch, `git status --short --branch`, staged/unstaged diff and `git worktree list --porcelain`. Inspect upstream/ahead-behind state when a handoff matters. Identify existing user/concurrent work and your ownership. A dirty tree is work to preserve, not a cleanup error.

Use a work branch from the intended base unless project/session instructions say otherwise. Keep it focused and integrate when verified and authorized; do not force a branch lifetime or merge deadline. Do not switch or rewrite a shared checkout while another worker owns it.

## Save coherent milestones

A milestone is a useful review, recovery or handoff point: a completed behavior with its relevant tests/docs, a resolved defect, or an explicitly labelled incomplete checkpoint before interruption. Commit at those points when authorized. Editing a file or passing a trivial check does not require a new commit.

- Group changes that must travel together to explain and verify one intent. Keep unrelated formatting, dependencies and refactors separate when practical.
- Size by conceptual cohesion and reviewability, without fixed line quotas. Do not split an implementation from its essential regression test merely to make smaller commits.
- Before each save, inspect the exact staged paths and diff. Stage owned files/hunks explicitly; avoid sweeping another person's files into a commit.
- Use the project's message convention, with a short purpose and a body explaining material rationale or trade-offs. For example: `fix: reject negative cart quantities` with the invariant it protects.
- Run the cheapest meaningful checks for the affected milestone. Reuse fresh applicable evidence when sources and relevant environment have not changed. Required final/CI/release gates remain required at their proper boundary; a full suite is not an unconditional pre-commit step.
- Inspect for secrets/private artifacts and unintended generated content using the project's existing checks. A keyword search is a hint, not proof that a diff is safe. Do not install hooks or dependencies just to implement this skill.

A verified milestone should record the revision, relevant check results and material limitations. If commits are prohibited, preserve a private checkpoint with the diff, owned untracked files and evidence instead. Neither a local commit nor a checkpoint proves remote backup.

## Failed verification: preserve, diagnose, repair

A failing test is evidence, not permission to discard work. Capture the command, exit status, relevant logs, source revision/diff and reproduction conditions in an appropriate private location. Preserve useful failed screenshots, traces and fixtures while the failure remains open; sanitize before any publication.

Localize the cause and repair the owned change, then rerun the affected verifier. Keep the original failure and subsequent result distinguishable. Do not weaken tests, reset the whole checkout, clean untracked files, or replace the tree with the last passing revision as routine recovery. If a rollback is actually necessary, first preserve current staged/unstaged/untracked state, identify the exact owned change and authorization, and choose a narrow reversible operation. Stop on ambiguous ownership or uncertain recovery.

A stash is local and may omit untracked/ignored files; a patch omits untracked content. Verify what any checkpoint actually contains. An incomplete checkpoint must state its failing/pending checks; never call it green.

## Worktrees have a lifecycle

A worktree helps when branch isolation or concurrent work is useful; it is optional for a small direct change. Inspect existing worktrees and reuse a suitable task-owned one before creating another. Record its root, branch/base, owner and purpose. Follow the host's managed-worktree API when applicable.

Before removal, inspect that exact worktree's status, staged/unstaged changes, untracked and needed ignored files, local commits, upstream and active users/processes. Preserve required failure evidence and private state separately. Confirm commits needed elsewhere are reachable from a retained branch or verified authorized remote; a clean worktree can still contain unpushed work.

Remove only an inactive task-owned worktree whose useful content is retained, using ordinary Git or the host's recoverable archive operation. Never force removal or recursively delete a checkout as routine cleanup. Preserve uncertain/shared worktrees and report the blocking item. Recheck worktree inventory and retained references afterward. Branch deletion and pruning are separate decisions with their own ownership/reachability checks. An unsuccessful experiment does not make its worktree disposable.

## Authorized remote handoff

A local commit is a save point; pushing is a separate external action. Reuse explicit session authorization for the named repository/branch, but do not infer it from a configured remote. Before publication:

1. Confirm remote identity, intended branch/ref, staged/committed scope and privacy. Exclude credentials, customer data, raw sessions and private checkpoints. Preserve needed private artifacts through an explicitly authorized private channel.
2. Check remote divergence using an authorized remote read. Push the intended ref without overwriting unrelated history. Stop on unexpected divergence or rejection; do not force-push a shared branch as recovery.
3. Read back the exact remote ref and compare its SHA with the local commit. Verify the PR URL/base/head and observed CI state if a PR is part of the task. A successful push does not mean CI passed or a release deployed.
4. Leave a concise handoff: branch and SHA, purpose/rationale, reproducible checks with results, pending failures/gates, artifact locations and the next safe step. State any private state that was intentionally kept outside Git.

PR creation, merge, tags and release publication follow their respective authorization. Do not claim a durable remote backup until readback succeeds.

## Generated files and history investigation

Follow repository policy for generated output, lockfiles, migrations and shared configuration. `.gitignore` prevents accidental additions; it does not make existing ignored data disposable. Preserve source inputs, manifests and reproducibility requirements.

Use `git log`, `git diff` and `git blame` for history evidence. Run checkout-changing investigations such as bisect in a suitable isolated checkout, or first preserve the full working state. Resolve conflicts against both intended behaviors; verify the combined result instead of accepting one side wholesale.

## Release and versioning

Use the project's versioning scheme. Under semantic versioning, a backward-compatible fix is patch, an additive compatible feature minor, and a breaking public contract major. Assess consumer behavior, not diff size; document material compatibility uncertainty and migration needs.

Keep version metadata, the intended release tag and a curated consumer-facing changelog consistent according to the repository's release mechanism. Group entries by impact (`Added`, `Changed`, `Fixed`, `Deprecated`, `Removed`, `Security`) where useful. Tags identify a reproducible revision; creating/pushing one or publishing a release requires the corresponding authorization and release checks.

## Handoff check

Confirm owned scope and rationale are reviewable, relevant evidence is fresh, failed work remains recoverable, and local/remote/CI/release facts are labelled separately. Save at the next meaningful milestone or before interruption; do not manufacture extra commits or repeat broad verification solely to create activity.
