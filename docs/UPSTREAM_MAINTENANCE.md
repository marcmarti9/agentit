# Upstream packages, provenance and authority

## Current maintenance snapshot — October 22, 2026

Live `git ls-remote ... HEAD` resolved all 16 canonical and 25 adaptation source
repositories. The canonical lock now contains **43 packages / 698 managed files**.
Forty-two packages match their reviewed current source HEAD; `image-to-code`
retains its last canonical snapshot because TasteSkill removed that upstream
package. The active `design-taste-frontend` package advances to the current
TasteSkill source independently. No public skill IDs were removed or added by
this refresh. The older counts below are historical reports, not live inventory.

Eight canonical source revisions advanced. TasteSkill adds app-screen guidance,
scene assets and browser-profile cleanup; diagram-design updates imports and
SVG/PNG export; Impeccable advances to skill 4.7.0 and engine-launcher 0.1.16;
Playwright corrects raw-output and trace/test guidance. Find-skills, Humanizer,
UI UX Pro Max and verification-before-completion have unchanged selected package
bytes at their newer repository revisions. Existing licenses remain unchanged;
the distribution now also retains Playwright's root Apache-2.0/Puppeteer NOTICE.
No upstream scripts, launchers, native installers, browsers or binaries were run.

All 25 adaptation records carry a dated current-HEAD review in
[`ADAPTATION_SOURCES.json`](../skills/ADAPTATION_SOURCES.json); original
`revision` fields remain provenance. Twenty-two preserve unchanged scoped input
files or an unchanged original repository HEAD. Expo's new automatic feedback
submission and OpenExecutive's provider-specific mail/tool procedures were
reviewed and excluded. The marketing quality playbook adopts current-context and
prior-learning checks, ordered paid-account diagnosis, bounded action decisions,
and explicit facts/hypotheses/missing-data reporting. This is reviewed adaptation,
not a claim that owned compositions are canonical copies of upstream HEAD.
Three older records lack historical source-input paths; their unchanged HEAD
and retained license were verified without inventing retroactive provenance.

### Removed upstream packages

A mapping may declare `retired_upstream` only after a human/model source review,
with the observed full `reviewed_head`, review date and reason. It keeps the
mapping's original `snapshot` and complete integrity records. Refresh checks
that the package remains absent at current HEAD, reports the retained old pin,
and updates active sibling packages normally. If its source body reappears,
refresh refuses until the retention policy is reviewed again. Removing a source
path without this explicit record still fails; it never silently deletes a
public capability or labels old content latest. The source registry marks the
retirement beside its canonical pin.

`review.disposition` supports `source-unchanged`, `adaptation-updated`,
`adaptation-preserved` and `blocked`. A preserved adaptation explains why changed
upstream advice was not adopted; a blocked record must remain a disclosed gap.
Each review retains exact inspected paths and Git blob OIDs. Integrity and source
review do not prove model adherence or upstream executable correctness.

### Legacy and live-reference origins reviewed October 22, 2026

These seven older origins were previously listed only in third-party notices,
outside the 25-record adaptation manifest. The exact current HEADs and scoped
review decisions below complete that source inventory. The owned adaptations
are original synthesis; a current source review does not relicense them or claim
that their bodies are current byte-for-byte upstream copies. Historical source
pins absent from old notices were not invented. No external native package,
agent rule, dependency or installer was activated.

| Origin / exact reviewed HEAD | Disposition |
| --- | --- |
| [vercel-labs/agent-skills@063bee94c3f4df8453406c830b0a7df0f2860278](https://github.com/vercel-labs/agent-skills/tree/063bee94c3f4df8453406c830b0a7df0f2860278) | Preserved owned composition and live-guideline adapters: original source HEAD unchanged; composition stays bounded to demonstrated API pressure and project React version. |
| [DietrichGebert/ponytail@09c434ab73ca43761c5d8b0c5d341926c2fba710](https://github.com/DietrichGebert/ponytail/tree/09c434ab73ca43761c5d8b0c5d341926c2fba710) | Preserved owned minimum-solution ladder and BUILDER/REVIEW. Current source still requires complete affected callers/validation; its session-global modes, native commands and blanket invocation are not imported. |
| [mattpocock/skills@5beb35b040e3de97e54fa9e386d7e42d15c295c2](https://github.com/mattpocock/skills/tree/5beb35b040e3de97e54fa9e386d7e42d15c295c2) | Preserved original writing/debugging/completion synthesis. Reviewed current context-pointer wording, progressive disclosure and red-capable feedback loops; upstream mandatory TDD, auto-review and commits do not supersede Agentit. |
| [google-labs-code/design.md@6e5da5382f41edbba9d73b2c62f33f32e9971f15](https://github.com/google-labs-code/design.md/tree/6e5da5382f41edbba9d73b2c62f33f32e9971f15) | Updated owned format sentence: YAML tokens may be front matter or section-level fenced YAML; each top-level key occurs once across combined blocks. Exact alpha schema/CLI remains live-verified per task. |
| [tt-a1i/archify@25cf37080fc8b1dbe758a4efc3935b55f3327083](https://github.com/tt-a1i/archify/tree/25cf37080fc8b1dbe758a4efc3935b55f3327083) | Preserved optional external family. Current native diagram/explainer workflows, renderer/install commands and global-rule update offers are not Agentit dependencies or authority. |
| [VoltAgent/awesome-design-md@3b605329240ce735b510037cca322f1831fdd7f8](https://github.com/VoltAgent/awesome-design-md/tree/3b605329240ce735b510037cca322f1831fdd7f8) | Preserved live one/two-reference scouting. Current source HEAD unchanged; original brand/system authority remains above curated analyses. |
| [scottstts/Threejs-Awesome-Graphics-Agent-Skills@897aaa0a49f9346f342993e1eb74a30479f82614](https://github.com/scottstts/Threejs-Awesome-Graphics-Agent-Skills/tree/897aaa0a49f9346f342993e1eb74a30479f82614) | Preserved owned product-storytelling scope. Current README emphasizes deterministic inputs, diagnostics, temporal stability and no-post baselines. Specialist implementation/example library remains external and was not imported or executed. |

Inspected paths: Vercel `skills/composition-patterns/SKILL.md` and
`skills/web-design-guidelines/SKILL.md`; Ponytail `skills/ponytail/SKILL.md`;
Matt Pocock `skills/productivity/writing-for-agents/SKILL.md`,
`skills/engineering/diagnosing-bugs/SKILL.md` and `skills/engineering/implement/SKILL.md`;
Google `README.md` and `docs/spec.md`; Archify `archify/SKILL.md`; and the
Three.js and VoltAgent READMEs. Three.js archive retrieval was bounded and
replaced with an exact-commit README read; its specialist library was not audited.

## Historical maintenance snapshot — October 15, 2026

The canonical refresh retains 41 packages, 674 managed files and 15 upstream
repositories. TasteSkill v2 is pinned at `Leonxlnx/taste-skill@f624f37`.
The separate ECC source is pinned at `affaan-m/ECC@b92f181`, with 4,615 original
files, 311 original skills and 11 explicit aliases. The unified catalog has
398 canonical skills (98 Agentit and 300 ECC); core remains exactly three.

Eight newer adaptation sources were reviewed individually. The relevant Expo,
Callstack, Anthropic, Trail of Bits, Rampstack and ibelick source files are
byte-identical to their original pins, so their adaptations are preserved.
OpenExecutive informs direct factual answers and bounded consequential
decisions. Marketingskills informs falsifiable ad hypotheses, exact product
names, untrusted research handling and margin/cohort-based acquisition payback.
Promotional integrations and universal spending rules were not adopted.

`skills/ADAPTATION_SOURCES.json` keeps each adaptation's original `revision`;
an optional `review` records the newly inspected full commit, date, disposition,
exact source paths and Git blob OIDs, and the resulting decision. This avoids
relabeling old prose as a byte-for-byte current upstream copy. The offline
curation check validates the record's shape and pins; it does not fetch sources
or establish model quality. Current source licenses/NOTICE were reread and
match the retained originals. The design-system source was renamed to
`peterbamuhigire/chwezi-design-engine` without changing its pinned commit.

ECC's additional documentation router and commit-message procedure resolve to
the existing Agentit owners; the other 16 new skills remain opt-in JIT
capabilities. The unchanged upstream tree includes per-file licenses such as
the OSINT skill's CC-BY-SA-4.0 notice. Importing it does not install native
dependencies, enable hooks, collect logs or authorize external actions.

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
with `agentit skills activate` in both prompt and JSON formats (`show` remains a compatibility alias), with the standalone
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

The September 18 reconciliation recorded 41 pinned canonical packages (including the raw
archived meta-workflow), 579 managed package/shared/license files and 15 source
repositories. That historical catalog was documented as 75 skills; the three global
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

## October 3, 2026 review

The observed baseline catalog contained 79 skills and 14 profiles, despite the older count above. This audit produces 84 skills and 17 profiles, with the three global bodies unchanged. Six canonical source revisions were accepted; diagram-design remains pinned because its new verification instructions depend on repo-level scripts absent from the distributed package. The offline lock contains 41 packages, 599 managed files and 15 sources. See the [dated comparison and evidence](../reports/2026-10-03-skill-quality-audit.md). New owned adaptations use a separate [source manifest](../skills/ADAPTATION_SOURCES.json), not the canonical lock.

## October 4, 2026 extensions

The [design expansion](../reports/2026-10-04-design-skills-audit.md) reaches
93 skills/18 profiles; the [motion/video extension](../reports/2026-10-04-motion-video-skills-audit.md)
reaches 96 skills/19 profiles and 23 adaptation source records. These additions
do not change the 41-package canonical lock or three-body global core. Official
Remotion skills were inspected but not copied: no reusable scoped license was
established, and a sibling plugin license must not be applied to that package.
The owned adapter instead uses original guidance and matching current/local
API contracts. Referenced renderers are not installed by curation or discovery.
