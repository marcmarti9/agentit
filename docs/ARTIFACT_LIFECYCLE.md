# Task artifacts, capacity and GitHub publication

Task owners keep an inventory of the resources they create, including worktrees,
QA copies, archives, build output, temporary databases and remote test resources.
Review it before **each** push, PR create/update or release. The global core skill
and provider-neutral `AGENTS.md` carry this requirement; it is not an opt-in skill.

`router/cleanup.py` is a small read-only review/guard. It never deletes resources,
executes ledger commands, discovers remote hosts, installs hooks or publishes to
GitHub. Cleanup actions still require ownership evidence and the user's existing
authorization. Production and other projects remain outside that authority.

## Capacity before creating resources

Estimate the total additional peak allocation of concurrent jobs, including copy
expansion, extraction, database restore, build caches and temporary overlap. Run
the guard on **each destination filesystem**, before allocating:

```sh
agentit cleanup capacity --path /existing/destination \
  --planned-peak-bytes 21474836480 --reserve-bytes 1073741824
# For a filesystem shared with production:
agentit cleanup capacity --path /existing/destination \
  --planned-peak-bytes 21474836480 --shared-production
```

The calculation is `f_bavail * f_frsize >= planned_peak_bytes + reserve_bytes`.
Root-reserved free blocks (`f_bfree`) are not available capacity. Shared production
always reserves at least **max(100 GiB, 10% total filesystem size)**, even when a
smaller reserve is requested. Failure exits nonzero; use another authorized
destination, reduce the peak or qualify and clean obsolete owned artifacts.
Do not create another large replica merely to run a test under disk pressure.

## Private ledger

The Git worktree must ignore `.agentit/`; none of that directory may be tracked.
Initialize once, then update the ledger as resources are created:

```sh
agentit cleanup init --project . --task-id bounded-task-id
```

This writes `.agentit/cleanup/ledger.json` with `inventory_complete: false`.
Set it true only after inspecting the task's actual resource use. A source-only
task can use empty scope lists with explicit `no_local_resources_reason` and
`no_remote_resources_reason`; no remote access is needed in that case.

Example ledger (local paths and reasons are private):

```json
{
  "schema_version": 1,
  "task_id": "bounded-task-id",
  "inventory_complete": true,
  "retained_source_paths": [{
    "path": "peer-feature",
    "owner": "concurrent-worker",
    "reason": "Unfinished work belongs to another task and is outside this commit"
  }],
  "local_scopes": [{
    "path": ".agentit/qa",
    "resources": [{
      "name": "active-fixture",
      "ownership": "task",
      "disposition": "retained",
      "retention": "active",
      "reason": "Current QA still needs this fixture"
    }, {
      "name": "old-build",
      "ownership": "task",
      "disposition": "removed",
      "reason": "Reproducible obsolete output removed under existing authorization"
    }]
  }],
  "remote_scopes": [],
  "no_remote_resources_reason": "No remote artifacts used by this task",
  "capacity": [{
    "path": ".",
    "planned_peak_bytes": 0,
    "reserve_bytes": 1073741824,
    "shared_production": false
  }]
}
```

Each local scope is one existing directory, inspected **one level deep**, with
every immediate child classified. Retained subtrees are units; declare narrower
scopes when their children need review. Unlisted children, symlinks, missing
retained resources and allegedly removed resources still present block the gate.
The CLI never infers disposability from names, age or size. Resource ownership is
`task`, `other` or `unknown`. Disposition is `removed`, `retained`, `cleanup_required`
or `unresolved`, always with a reason. Only task-owned resources can be recorded
removed. Retention must be `active`, `private`, `unique`, `unsynced`, `required` or
`other_owner`; unknown retention and unresolved cleanup block publication while
preserving the resource. Reviewed retained resources produce
`REVIEWED_WITH_RETAINED`, never an assertion that no junk exists anywhere.

Declare one combined capacity plan per filesystem covering the project and all
local scopes. A zero peak is appropriate after work is finished and no further
artifact allocation is planned. If jobs will continue, include their remaining
peak. A shared production destination must be marked `shared_production: true`.

Concurrent dirty/untracked sources can be kept through `retained_source_paths`,
with a bounded project-relative file/directory, owner and reason. This prevents
another worker's legitimate WIP from blocking a publication of the current commit.
The repository root and parent traversal cannot be exempted. Undeclared dirty
paths block publication; retained WIP may continue changing because the published
commit/tree remains fixed. The receipt does not claim to verify those WIP bytes.

## Explicit remote scopes

Declare each task-used remote artifact scope as
`{"id":"qa-host-scope","evidence":".agentit/cleanup/remote.json"}`. Using an already
authorized read-only connection, capture an inventory and destination capacity
from that exact scope. Agentit does not open a connection or run a supplied
command. The private evidence JSON shape is:

```json
{
  "scope_id": "qa-host-scope",
  "observed_at": "2026-10-20T09:00:00+00:00",
  "inventory_complete": true,
  "resources": [],
  "capacity": {
    "available_bytes": 536870912000,
    "total_bytes": 1073741824000,
    "planned_peak_bytes": 0,
    "reserve_bytes": 107374182400,
    "shared_production": true
  }
}
```

Resources use the same classification fields as local resources. Report available
bytes from remote `os.statvfs(path).f_bavail * f_frsize`, total from `f_blocks *
f_frsize`, and UTC observation time. Evidence must be no older than one hour.
Missing/incomplete/expired evidence or inadequate remote capacity blocks the gate.
The receipt labels it `operator_supplied`: a file hash binds bytes, not the truth
of a remote observation. Re-observe after remote resource changes.

## Publication sequence and receipts

After the final source commit, run:

```sh
agentit cleanup review --project .
agentit cleanup check --project .
# Or, as part of the normal verification surface:
agentit verify --project . --signal publication --apply
# Then perform the already-authorized GitHub publication immediately.
```

Review writes a private mode-0600 `.agentit/cleanup/review.json`, including the
ledger, source commit/tree, inventory observations, capacities and blockers. A
replacement review invalidates an old pass before reading the new ledger. Check
requires the same commit/tree, accounted-for uncommitted source, unchanged ledger, unchanged shallow local
inventory, unchanged fresh remote evidence and a review younger than 24 hours.
The cleanup receipt is not an inventoried resource: its own bytes and the
parent-directory mtime they update are omitted, while every other child of
`.agentit` or `.agentit/cleanup` still has to stay unchanged.
It rechecks local available capacity each time. Commit/source changes require a
new review; resource or ledger changes require a new review. It does not repeatedly
walk entire disks or recalculate recursive directory sizes.

Commands print only a sanitized status, commit, resource counts and fixed blocker
codes. Publish that summary if useful; never copy the private ledger, paths,
remote evidence, reasons, credentials, customer data or full receipts into a PR.
`verify --signal publication --apply` includes a blocking cleanup probe and exits
nonzero for failed blocking probes. Cleanup runs after the other probes and is
checked again after the verification receipt is written. If that write changes a
reviewed inventory or exhausts capacity, the same receipt is saved as BLOCKED and
a final check runs without further filesystem writes. That failure remains
blocked; the CLI only prints the final result afterward. Tests/builds that create
artifacts require a new cleanup review followed by `cleanup check` before
publication. Ordinary verification does not demand remote access or cleanup state.

These guards enforce explicit declared evidence, not completeness against a
dishonest producer, shell-level interception of Git, filesystem locking or deep
retained-subtree integrity. The responsible agent must declare all task scopes,
keep review/check adjacent to publication, re-observe mutations and use existing
permissions. No hook or global Git configuration is changed automatically.

Verification: `python3 -m unittest router.test_cleanup router.test_verify -v`.
The focused fixtures cover stale/missing/source-changed review, retention,
inventory drift, symlinks, remote freshness, publication failure exit and capacity.
