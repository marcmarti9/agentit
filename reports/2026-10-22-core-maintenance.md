# Core quality, milestones and artifact lifetime — 2026-10-22

## Problem and resulting behavior

Agentit's core covered final documentation and handoff checkpoints, but did not
make intermediate durable milestones and storage ownership sufficiently visible.
Some inherited Git instructions prescribed unconditional verification, fixed
change sizes and destructive recovery. Local continuity could create private
state before checking whether project Git would expose it.

The core now requires readable idiomatic code, clear responsibilities/contracts
and the smallest sufficient design. Clean Code/KISS/DRY/SOLID guide judgment;
they do not mandate extra layers, interfaces or line counts. Meaningful milestones
record the problem, change, rationale, checks/limits and next action. Authorized
publication requires destination/version readback. Temporary state and failure
evidence remain private, and created artifacts have an owned storage lifetime.

## Core and JIT ownership

Exactly three global bodies remain: `using-agentit` for entry/shared obligations,
`task-router` for semantic selection/modes/risk, and `using-agent-skills` for
mechanical discovery/delivery. All 26 visible profile pointers remain present.
The core totals **15,833 bytes**, below the unchanged 16,000-byte bound.

The router owns cadence; one selected JIT procedure adds detail. Ordinary coding
can select `reliable-coding`; specialist procedures need distinct value. Adversarial
selection moved out of the mechanical adapter to the router for consequential or
materially uncertain proposals and explicit requests. Visual taste details stay
in the conditional web reference. Universal evidence honesty remains global;
constructive dissent is defined once in the router.

`documentation-and-adrs` captures decisions while their context is fresh without
creating a document per edit. The Git procedure saves coherent milestones,
preserves failed work and colleague changes, handles worktrees through a verified
lifecycle, and separates local saves, remote refs, CI and release observations.
Large imports need distinct provenance/review maps rather than arbitrary splitting.

## Retention and privacy

New `artifact-retention-and-cleanup` is discoverable in engineering, infrastructure,
release and agent-systems profiles/packs. It inventories exact owned candidates,
capacity, references, retention/rollback holds and recovery evidence; previews and
revalidates before authorized mutation and measures actual freed capacity.
It installs no daemon, blanket purge or new deletion executable. No user PC or
server cleanup was performed for this change.

Before private local writes, continuity verifies `.agentit` is untracked and
excluded, establishing an exact repository-local exclusion when needed. Nested
projects and linked worktrees are supported; tracked `.gitignore` and private
bytes are preserved. Unsafe/tracked/unverifiable state fails closed. Reads remain
read-only; non-Git projects remain supported. Explicit forced Git additions can
bypass ignore rules and still require staged-diff review.

Independent review reproduced a race: reverting a failed exclusion append could
erase a concurrent project's successful rule. Exclusions now append without
truncating concurrent content. A real-Git regression observed failure before the
fix and verifies both private state bytes and exclusion afterward. A failed init
may retain its own harmless local rule, without creating state.

A second reproduced defect came from clearing the caller's Git configuration:
the privacy check could see different global ignore rules from `git add`.
The guard now preserves caller configuration and removes only variables that
redirect repository/index/object context. Real-Git GLOBAL/COUNT and redirected
repository regressions observed the failure before repair; the independent
reviewer reran both original exposures and confirmed they are closed.

## Source preservation and image-to-code

Git and documentation are now explicitly Agentit-owned Apache-2.0 adaptations
with the original MIT attribution/license retained. Their exact pinned originals
remain separately hash-verified under `vendor/agent-skills`, following the existing
adapter pattern. A source-refresh regression proves that updating the archived
original does not overwrite the owned procedure.

`image-to-code` was moved by its author from Taste Skill to Imagegen Skills,
rather than demonstrated to have failed. Its body remains byte-identical; the
canonical active origin is now `Leonxlnx/imagegen-skills` at
`beb16b0d0f4dae9a6f5cb04ea41e97b93a54ab8e`, with the original MIT license retained.
The canonical registry contains **43 packages / 699 files / 17 sources**; the
unified skill catalog has **404 IDs** and 26 adaptation source records.

Primary explanation: [upstream relocation](https://github.com/Leonxlnx/taste-skill/pull/155),
[fixed source body](https://github.com/Leonxlnx/imagegen-skills/blob/beb16b0d0f4dae9a6f5cb04ea41e97b93a54ab8e/skills/image-to-code/SKILL.md).

## Verification and limits

Focused checks cover real Git privacy, nested/linked projects, accidental staging,
unsafe paths, concurrent exclusion writes, generated pointers/portable entry,
source/license integrity and refresh isolation. Final integrated command evidence,
independent review, installed-runtime checks and exact-head CI results accompany
the PR. A separate disposable coding fixture exercises actual policy application
with a regression and unrelated uncommitted collaborator work.

Observed local acceptance: **369 runtime tests and 75 script tests passed**,
along with generated profile/core freshness, canonical/ECC integrity, shell
syntax, compilation and whitespace checks. The final command verifier recorded
unchanged source fingerprints. **Three subprocess tests passed against the
installed CLI**, including initial private state in a Git project without an
ignore file. All-provider bootstrap backed up/applied 42 files, then reported
**5,572 keep operations, no changes and two preserved unmanaged private files**.
Remote CI results belong to the exact published PR head; the installed CLI
tests also run in its Ubuntu/macOS bootstrap jobs.

In that fixture, the existing regression failed before the fix and passed after
it without changing the tests. The collaborator's bytes and empty Git index were
preserved. A private checkpoint captured the patch and before/after evidence;
the worker respected its no-commit/no-network contract. Retention kept failure
evidence and blocked disposal of a purported rebuildable artifact after its
recipe produced different bytes. These are observed fixture outcomes, not a
claim about every host/model execution.

Static policy checks and delivery hashes do not establish universal model
compliance. An isolated fixture supports only its observed behavior. Local/CI
evidence does not certify production or a real remote/private-machine connection.
No merge, deployment, destructive host cleanup or account setup belongs to this
change. See the canonical documentation and continuity contracts for operations.
