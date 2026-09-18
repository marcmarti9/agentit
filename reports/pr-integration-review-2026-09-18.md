# Adversarial review of the pending Agentit PRs — 2026-09-18

## Decision and scope

Review all seven open PR heads (#43, #44, #45, #47, #51, #52, #54), not just their
summaries or individual green checks. The user explicitly authorized fixes and
merge after this review. No global installation, provider reconfiguration or
production action is included. The integrated history retains every original
head as an ancestor; #53 was already included in #54 and closed as superseded.

The branches were **not safe to merge unchanged in arbitrary order**. #45 and #52
had conflicts with the latest JIT work, #52 could replace the owned adapter with an
upstream lifecycle, and #54 still had reproducible delivery/evidence defects.
The revised integration is a merge candidate only after fresh complete CI on its
published head. Individual old CI checks are not substituted for that gate.

## Findings, reproduction and correction

| ID | Severity | Failure observed or integration conflict | Correction and verifier |
| --- | --- | --- | --- |
| R1 | High | #52's upstream meta-skill and overlays conflict with #54's owned navigation adapter and #45's canonical-source boundary. | Preserve the owned adapter, archive raw upstream under `vendor/agent-skills`, carry one authority envelope through CLI/prompt/worker. Pinned byte/mode verification plus authority tests. |
| R2 | High | A managed private cache is accepted after the canonical skill or reference has been deleted. This could revive retired instructions. | Require the selected canonical resource still to exist and match. Two adversarial regressions. Native overrides remain intentional. |
| R3 | Medium | Text-mode newline translation changes CRLF bytes; valid caches appear corrupted. Prompt rendering also removes trailing whitespace from the supposedly exact body. | Decode raw UTF-8 bytes and preserve the entire selected body in prompt rendering. Three byte-transport regressions. |
| R4 | Medium | Worker creation reads an unrelated availability manifest; invalid JSON blocks an explicitly selected native skill. | Do not consult unselected cache availability. The selected-cache path still validates its manifest and fails closed. Two complementary regressions. |
| R5 | High | Schema-3 spawn validation accepts altered or omitted project instruction bodies, despite retaining paths/hashes; the authority envelope can also be absent. | Validate the ordered inventory, declared projection, content digest and shared authority field. Three mutation regressions. Unsigned metadata is not authentication. |
| R6 | High | A passed command's source evidence remains current after chmod or empty-directory changes; FIFOs are silently omitted. | Version-2 fingerprints include file kind/mode/digest and directory kind/mode; special files fail closed. Three filesystem regressions. |
| R7 | Medium | Merging the latest compact core and older invariants can silently lose #43/#44, while restoring the full old core defeats JIT size limits. | Keep #43's compact standing rule and verbatim expanded baseline in an owned reference; preserve #44's client-operability text without a second copy. Existing invariant tests retained. The 16,000-byte core bound was not raised. |
| R8 | Medium | Older maintenance tests assume a mutating shell updater, local canonical overlays, and source-directory permissions inherited from a particular checkout. | Replace those obsolete assumptions with a real offline refresh across all 15 sources and an exact metadata-preserving bootstrap fixture. Keep native policy assertions outside upstream prose. |

`router/test_pr_integration_regressions.py` was first run on the unmodified #54
implementation (`ac4f74e5...`, same implementation as its later evidence-only head).
**13 probes: 10 failures, 2 errors, 1 pass.** The already-protected malformed
selected-cache case is the negative control, not a new bug. After correction,
these 13 plus 3 authority-delivery tests pass. Full logs and immutable input heads
are in `reports/pr-review-evidence-2026-09-18/`.

## Disposition of every PR

| PR | Preserved work and reconciliation |
| --- | --- |
| #43 | Preserve the web quality invariant in the cold-start core. The original expanded text is retained in `references/web-quality-baseline.md`; `task-router` links the compact rule to JIT design selection. No duplicated upstream design doctrine. |
| #44 | Preserve the original client-operability block in `AGENTS.md`: mutable data, suitable existing admin surfaces, roles, safety and maintainability. Its scope is material client-system work, not a demand to build a panel for every small edit. |
| #45 | Preserve write-ahead backups/receipts, interrupted rollback recovery, runtime ownership inventory, metadata-aware obsolete-file retirement, protected user drift, portable source refresh and original licenses. Reconcile authority delivery with schema 3. |
| #47 | Preserve the canonical-package deletion fix as the portable updater's ownership contract. The complete refresh fixture verifies all former victims survive, with scripts/assets/shared resources. Do not restore the obsolete unconditional deletion script. |
| #51 | Preserve the full website ship-surface checklist, reference index and premium-web JIT entry. Do not edit raw canonical `shipping-and-launch` merely to add another link; owned discovery references provide the integration. |
| #52 | Preserve the newest pinned upstream versions, `constraint-driven-development`, ADHD package support, registry/pack/profile updates and documentation improvements. Replace canonical-body overlays with the owned adapter gate. |
| #54 | Preserve SEO consolidation, all historical audit reports/evidence, schema-3 body delivery, explicit selection, command-bound Loop evidence, compact core, discovery improvements and hook hardening. Add R2–R6 regressions and fixes. |

## Source integrity and deletion review

A read-only Actions job reconstructed the canonical files from the exact commit
pins in #52, using the reviewed safe archive parser from #45, without executing
upstream code. Run `35388808271` verified **41 canonical packages, 579 managed
files and 15 repositories**. This includes package files, shared references and
original license/NOTICE files. Metadata, selected source paths and hashes are
recorded in `skills/UPSTREAM_LOCK.json`; the archived raw meta-workflow is not the
globally installed adapter.

The full tracked code-checkpoint difference from `main` is recorded in
`tree-changes.json`, including old/new blob IDs and modes for every addition,
modification and deletion. The large deletion volume is primarily the Impeccable
upstream transition from JavaScript tooling to its versioned launcher; it is not
a deletion of Agentit's native JIT machinery. Reconstructing pinned source bytes
does **not** certify the launcher binary. The launcher can download and execute an
engine with host permissions; it is neither executed nor enabled by this review.
Use the existing explicit capability/authorization boundary before such execution.

All 75 installable skill bodies have valid discoverable metadata. The three core
bodies total **15,982 UTF-8 bytes**, below the unchanged 16,000-byte test bound.
This measures startup instruction size, not model speed, attention or quality.
The SEO reference remains owned and consolidated rather than replaced by a second
local SEO skill.

## Verification and publication gate

Run from a fresh checkout:

```sh
python3 -m unittest discover -s router -p 'test_*.py' -v
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/sync_upstream_skills.py
python3 -m py_compile agentit bootstrap.py router/entrypoint.py router/bootstrap.py
bash -n install.sh update.sh security/harden-local.sh scripts/sync-upstream-design-skills.sh scripts/sync-upstream-skills.sh hooks/precompact-memory.sh
git diff --check
```

Also require the existing Ubuntu and macOS portable-bootstrap CI jobs: fresh
install, installed CLI, real body/resource loading, schema-3 worker, executed
verifier, source binding and repeatable rollback. The first complete local pass
exposed an exact-copy fixture that lost checkout directory modes and policy tests
that still required obsolete upstream overlays/interview wording; those were
corrected at their contract owner and rechecked, not hidden by deleting tests.
The final PR verification receipt must identify the head and remote runs observed
before merge. Intermediate red runs remain diagnostic evidence, not release proof.

Documentation drift review covers the adapter/canonical boundary, default
read-only maintenance command, ideation mandate, CRLF/trailing-byte handling,
retired caches, authority transport, instruction validation, fingerprint-version
migration, bootstrap recovery and the supported platform boundary. Historical
September 18 audit measurements remain historical; this report supersedes them
only for the integrated revision.

## Limits and rollout

This is a fresh adversarial review with concrete reproductions, not an additional
independent LLM review of these fixes. Existing Copilot comments report quota
exhaustion; no such review is claimed. Native model/host selection, attention and
obedience were not evaluated, and deselection does not erase conversation tokens.
Hashes and JSON receipts remain unsigned. Capability envelopes are not OS sandboxes.
Windows-native bootstrap and upstream engine execution are not certified.

After merge, an existing installed Agentit remains on its installed revision until
a reviewed bootstrap/profile refresh is applied. Do not silently perform that
installation as part of a PR merge. Rebuild older schema-3 payloads lacking the
new authority field and rerun older source-bound verifiers before relying on their
freshness under fingerprint version 2.
