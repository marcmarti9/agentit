---
name: artifact-retention-and-cleanup
description: Inventory and safely retire task artifacts, caches, generated output, worktrees and expired recovery copies using ownership, references, retention rules and measured reclaimed space. Use for scoped capacity or artifact-lifecycle work, not general machine cleaning.
license: Apache-2.0
---

# Artifact Retention and Cleanup

Use this skill when artifacts need a retention decision or a bounded cleanup. It is a JIT procedure, not a daemon, background purge, new storage service or permission to clean the host. Respect the task's roots and existing authorization; planning or inspecting candidates does not authorize destructive changes. Do not add a cleaner executable unless the task separately requires one.

## Establish scope and capacity

Identify the owner, allowed roots/resource IDs, purpose and capacity problem: full filesystem, growing task output, expired preview, completed worktree, or redundant recovery copy. Read existing retention/rollback/privacy requirements. Record filesystem or service capacity before work, using comparable units and the actual affected mount/quota; distinguish allocated disk, apparent file sizes and service-reported storage.

A near-full disk justifies prioritization, not broader deletion. Prefer verified task-owned regenerable material. Do not scan arbitrary private/home/server locations or prune whole providers merely because a scoped candidate lives there. If authorized scope cannot recover enough capacity, report the measured shortfall and safe remaining options.

## Classify by recoverability

| Class | Required evidence before retirement |
| --- | --- |
| Cache or dependency download | Exact owner/tool and root, no active writer/consumer, and a usable refill source. Offline needs, local patches and unavailable versions may make it valuable. Prefer the tool's bounded cleanup interface. |
| Regenerable build/test output | Retained source, manifests/lockfiles, generation command and required tool/input availability. Check that it contains no unique uploads, local configuration or unresolved failure evidence. |
| Task evidence, preview or worktree | Task/worker is finished and inactive; no open failure, reviewer, issue, handoff or active reference needs it. Preserve the minimal useful receipt/reproduction. A clean checkout or old timestamp alone proves none of this. |
| Backup, snapshot or rollback artifact | Explicit retention/expiry policy, retained recovery coverage and dependencies, rollback window closed, and relevant restore/integrity evidence. Keep the last verified recovery path; an untested replacement or a newer filename is insufficient. |
| Private/business data, credentials, databases or unknown content | Preserve by default. Follow the data owner's explicit retention/privacy/deletion authorization and domain procedures. Git sync or successful build does not make this data regenerable. |

Age and size can rank investigation; they cannot establish ownership, obsolescence or deletion authority. Preserve active runtime caches, shared state and artifacts of uncertain ownership. Do not classify Docker volumes/databases, ignored files, provider sessions, keys or uploaded media as disposable caches by their directory names.

## Produce a candidate inventory

Before mutation, create a small private manifest or review table in the existing task evidence area. For each candidate record:

- Exact path or immutable resource ID, owning task/person/tool and class; resolve symlinks and mount/storage boundaries without following them into unrelated roots.
- Measured apparent and, when available, allocated bytes or service quota impact; record measurement command/time. Avoid double-counting hardlinks, nested directories, snapshots or shared layers.
- Current identity/state suitable for revalidation: canonical root, device/inode where useful, metadata/content fingerprint or remote generation/version, directory inventory, active users/processes/locks and Git status/reachability for worktrees.
- References/consumers checked, including configuration, manifests, issue/review/handoff links, current release/rollback pointers and other active tasks. Record search scope and limits; no text match is not proof of no live consumer.
- Why it is eligible or protected, applicable expiry/retention rule and its source, authorization, recovery/regeneration method and estimated cost.
- Decision (`retain`, `candidate`, `blocked`), proposed exact operation and preservation destination/evidence. Unknown ownership, references or recovery means retain/blocked.

Keep private paths/content out of public reports when unnecessary. A compact example:

```text
candidate: <exact task-owned output root>
owner/class: <task-id> / regenerable output
bytes/baseline: <allocated measurement>, <mount free bytes and time>
identity: <root identity plus inventory/fingerprint>
references: <actual checks and limits>; active consumers: <observed state>
reason/policy: <completed task and policy source>; open failures/rollback: <state>
preserve/rebuild: <retained inputs, command, receipt location>
authority/operation: <session scope>, <exact bounded operation>
decision: candidate | retain | blocked
```

## Preview and preserve

Preview the exact selected candidates and operation, expected recovery, exclusions/protected items and capacity estimate. Use an existing tool's dry run when it accurately reflects the operation. Do not turn the preview into a wildcard, broad recursive scan, `prune all`, or an age-based delete rule.

Retain what matters before deletion: unresolved failure logs/traces, source and unpushed Git work, reproducibility inputs, required release/rollback generations and private configuration. Verify preservation actually includes untracked/ignored files where needed and that restore/regeneration is viable. A copy on the same full filesystem may add pressure; moving to quarantine there usually frees no capacity. Quarantine is an optional reversible step, not proof of reclaimed bytes or authorization to delete later.

If deletion is outside the current authorization, present this concrete preview for the necessary decision. Reuse existing explicit authorization when it covers these exact artifacts and actions. Do not repeatedly ask for already-authorized bounded steps.

## Revalidate immediately before mutation

Re-read each exact candidate's identity and relevant state against the preview: root containment, symlink/mount changes, content/generation drift, ownership, active processes/references, retention holds, open failures, rollback needs and preservation evidence. For a directory, a stable name/inode alone does not prove its contents stayed unchanged. Prevent concurrent writes with the platform's existing coordination where available; if a race cannot be safely bounded, retain the candidate.

Any mismatch invalidates that candidate's approval basis: stop its removal, update the inventory and reconsider. Never follow a replaced symlink, substitute a newly discovered path or expand to neighbors. Execute only the authorized exact subset with the native scoped operation. For Git/worktrees use the safe lifecycle in `git-workflow-and-versioning` when that skill is selected; never force-remove worktrees or discard dirty/unpushed state as cleanup.

## Verify and close

Check operation results and remaining identities, retained references/recovery artifacts and affected consumers. Remeasure the same filesystem/quota using the same method. Report candidates removed/retained/blocked, errors, before/after available bytes and observed delta separately from estimated candidate sizes.

Compression, shared extents/layers, snapshots, concurrent activity or deleted-but-open files can make the physical delta differ from the estimate. Explain the evidence limit; do not delete more or restart shared processes just to force the expected number. A removal receipt is not a restore test or secure-erasure guarantee.

Leave a concise receipt with inventory/preview, revalidation, exact actions, preservation locations, measured result and remaining holds. Keep recurring retention settings explicit and owned if requested; do not silently schedule a future purge. Stop when the scoped target is met, candidates are exhausted, or ownership/authority/recovery/concurrency is unresolved.
