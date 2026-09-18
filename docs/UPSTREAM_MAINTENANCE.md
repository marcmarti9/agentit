# Upstream packages, provenance and authority

Agentit owns its runtime, routing, core adapter and source-informed compositions.
Canonical third-party packages retain their upstream bytes and license. The
machine-readable boundary is `skills/UPSTREAM_LOCK.json`:

- `mappings` bind a source repository, full commit SHA, package path and optional
  distributed destination to every package file's SHA-256 and executable mode;
- repository-root packages declare their included package entries;
- `shared` tracks upstream references used by relative links;
- `licenses` binds original LICENSE/NOTICE files to the same pinned snapshots.

Canonical task packages remain under their stable `skills/<id>` paths. The raw
`using-agent-skills` meta-workflow is retained under
`vendor/agent-skills/using-agent-skills`. Its globally installed namesake is an
Agentit-owned navigation adapter. Source-informed composites and attribution
are documented in `THIRD_PARTY_NOTICES.md`.

The relocated raw meta-workflow is archived for provenance rather than loaded
as an executable workflow. Its unchanged relative reference paths describe the
original source layout; inspect the matching root `references/` files or the
pinned upstream repository when following them. Regular task packages retain
their original relationship to Agentit's shared reference directory.

## Actual loading boundary

`router/skill_authority.py` defines one shared authority envelope. It is emitted
with `agentit skills show` in both prompt and JSON formats, with the standalone
skill loader, and in worker context payloads and rendered contracts.

The envelope explains that source workflow imperatives do not override host or
user authority, activate further skills, expand task scope, or authorize tool
execution. Domain guidance and useful verification remain applicable within
the selected task. This is an explicit agent instruction, not a sandbox or proof
that a model will obey it. The three core skill bodies establish the same rule
for hosts that open package files directly.

Source references stay JIT. Source advice about trimming context cannot erase
text already consumed by the current model. Source model names, interview
formats and lifecycle preferences do not become Agentit-wide requirements.

## Inspect and refresh

The default check is offline and read-only:

```bash
python3 scripts/sync_upstream_skills.py
```

To inspect current upstream revisions:

```bash
python3 scripts/sync_upstream_skills.py --refresh
```

The tool resolves each repository HEAD to a full SHA before downloading that
snapshot over HTTPS. It reads archive members without extracting them into the
workspace, rejects traversal and selected non-regular entries, and applies size
limits. No upstream scripts, hooks, package installers or dependencies execute.
Private archive caches live under `.agentit/upstream/archives` by default.

Review the resulting source commits and relevant package changes. A subsequent
unqualified `--refresh` can observe newer HEADs. To apply exactly the inspected
commits, save the plan's `source_commits` object as a JSON file and use:

```bash
python3 scripts/sync_upstream_skills.py --refresh --heads-file /path/to/reviewed-commits.json --offline --apply
```

The heads file accepts repository-to-SHA strings or records containing `sha`.
Offline refresh requires every exact archive in the cache. Historical locks
without file hashes are first checked against their old pinned source archives;
the tool never labels arbitrary current local contents as canonical.

Before a refresh, existing canonical files and modes must match the lock. Extra
local package files, modified references and unowned destination collisions
cause a refusal. Move intentional customizations into an owned adapter or
review them separately. The refresh preserves the selected upstream package and
removes only obsolete files covered by its previous integrity records.

Caught write or final-integrity failures restore prior files only while their
current bytes and mode match the expected refresh result. Concurrent edits are
preserved and reported for manual recovery. The lock is written last so a
process kill or machine failure leaves a detectable integrity mismatch.
Refresh is a repository maintenance operation, not the bootstrap's durable
installation transaction: use a work branch and Git to inspect or recover a
refresh interrupted outside Python's exception handling.

## Executable package dependencies

Vendoring a package is not permission to run it. An optional upstream launcher
may download additional software or contact a service when run. For example,
Impeccable's current distribution replaces much of its former JavaScript
tooling with a versioned binary launcher that verifies a downloaded checksum.
Agentit preserves that canonical distribution, but its installer and refresh
never invoke the launcher or obtain the binary. Select and review that external
execution separately when it is useful to a real task.

## Maintenance and review

The legacy shell sync entrypoints delegate to the portable Python tool. The
one-off registry reconciliation and policy-alignment scripts have been retired:
their job was a past migration, and rerunning them could rewrite current owned
policy or delete current package destinations.

CI runs offline full-file integrity verification and fixture-based refresh tests.
Those tests exercise read-only plans, package preservation, idempotence, local
edit refusal, traversal/link handling and failure recovery. Source provenance,
authorization and agent behavior remain separate claims.

## September 18 PR reconciliation

The integrated registry contains 41 pinned canonical packages (including the raw
archived meta-workflow), 579 managed package/shared/license files and 15 source
repositories. The current installable catalog has 75 skills; the three global
navigation bodies remain Agentit-owned. `constraint-driven-development` and
`i-have-adhd` are covered by refresh; aliases retired by #47 never become deletion
targets for their canonical replacements.

The ideation gate stays in the owned adapter, not an overlay rewriting Addy's raw
`idea-refine`. The public website ship checklist stays in owned references, not a
local edit of canonical `shipping-and-launch`. The full offline refresh fixture
exercises all 15 repositories, root packages, executable scripts, shared references,
archived meta-workflow, original licenses and idempotence without running upstream
code. Integrity does not certify an upstream launcher binary: no Impeccable binary
was executed by this review. Windows-native bootstrap remains outside the supported
Linux/macOS verification matrix.
