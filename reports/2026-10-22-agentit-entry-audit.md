# Agentit entry, profiles and source audit — 2026-10-22

## Problem and observed causes

The requested outcome was actual skill use across ordinary chats and coding
agents, a source-neutral skill library, meaningful complete profile coverage,
current upstream reviews, bounded JIT context and consistent BUILDER/REVIEW.

The previous README quick start asked the agent to **install** Agentit. The core
described profiles mainly as installation availability; runtime discovery exposed
packs but lacked a profile discovery command and a complete purpose index in the
core. Merely listing IDs therefore looked like progress without a complete
read/application path. This is an observed documentation/navigation gap, not
proof of why every previous model failed to follow instructions.

ECC's importer also regenerated separate `ecc-*` profiles and appended another
source-labelled pack catalog. This made source-based separation recur after
refresh. Many skills lacked a useful non-ECC domain home or existed only in the
catch-all inventory. Some inherited profiles pulled in unrelated web frameworks.

## Implemented architecture

- `AGENTIT.md` is a generated single-file copy of all three exact owned core
  bodies, with byte counts and source hashes. It is readable by authorized file
  and repository tools without a terminal or installation. It does not contain
  domain skill bodies or private project state.
- `using-agentit` now requires complete core reads, profile discovery, complete
  selected skill reads and application to the actual task. It embeds purpose
  pointers for all 26 canonical profiles; compatibility names point to existing
  domains rather than creating another library.
- `references/agentit-profile-index.md` contains direct source links and domain
  metadata. The CLI exposes `skills profiles` and
  `skills candidates --profile ID [--direct]` with body sizes and approximate
  context costs. Metadata inspection never installs or activates bodies.
- Every one of the 403 canonical skills (103 root-library + 300 ECC) belongs to a
  meaningful domain profile; `all` and compatibility aliases cannot hide orphans.
  New domains: `engineering`, `languages`, `agent-systems`, `infrastructure`,
  `operations`, `healthcare`, `financial-protocols`.
- ECC sources remain under `vendor/ecc` for exact integrity, attribution and
  native-tool boundaries. The importer no longer rewrites unified profiles or
  appends a parallel catalog. Existing installation/pack IDs remain aliases.
- Profile inheritance was narrowed for design, mobile and artifacts. Skills
  remain selected by task relevance, not upstream brand or an automatic keyword
  classifier. A full profile is allowed when every member applies, context fits
  and overlapping procedures have a clear owner.
- BUILDER completes the requested scope with focused checks; REVIEW freezes
  feature scope and runs relevant broad gates. The policy applies from core even
  if the optional anti-overengineering specialist was not selected.
- A compact application record connects actual reads, adopted constraints/checks
  and outcome evidence. It explicitly does not certify comprehension/obedience.
- CI checks profile coverage and generated-entry drift. Existing complete-byte,
  integrity, permission, cache, worker and core-size constraints remain in force.

The core remains **15,907 UTF-8 bytes**, below the existing 16,000-byte invariant.
No specialist bodies were made globally active.

## Local stale-runtime finding and portable correction

Independent review found that this machine's prior private runtime exposed 406
skills while its canonical `all` profile resolved 403. Three historical unmanaged
skill bodies caused that discrepancy; six unmanaged references also violated
canonical package integrity. All nine were preserved with hashes outside the
runtime, while two private continuity/planning documents stayed untouched.

The portable bootstrap now recognizes only these nine reviewed public historical
path/hash pairs, requires original 0644 permissions and absence from the current
source, and uses its existing backup/rollback transaction to retire them. Name
matches alone never authorize removal. Customized bytes or permissions and all
other unmanaged/private files remain preserved and reported. Tests cover recovery,
idempotence, custom/private preservation, source exclusion and changes after plan.
This prevents the same known historical leftovers recurring on another machine
without introducing a broad cleanup policy.

After the local update, runtime discovery equals the source's 403 canonical IDs;
all 43 packages/698 files and ECC's 4,627 source files verify. The post-apply plan
contains only `keep` actions. Only the three managed core bodies are exposed by
Agentit in global discovery; unrelated user-owned host skills are not erased.

## Exactly what the core contains

Only these three complete bodies are global. All other expertise is JIT.

| Body | Responsibilities in this revision |
| --- | --- |
| `skills/using-agentit/SKILL.md` | Entry/read-and-apply contract; optional installation and ordinary-reader path; every canonical profile purpose pointer; bare/material dispatch; semantic cold start versus retained context; actual reads/application record; delegation with real bodies; bounded Loop/Graph evidence; source provenance and tool permissions; task-owned MCP cleanup; opted-in tracking; durable architecture/docs drift; private continuity; truthful web content and anti-default visual baseline; constructive dissent; honest completion and external-action boundaries. |
| `skills/task-router/SKILL.md` | Model-owned task interpretation; compact scope/risk/ownership/verification decision; canonical BUILDER/REVIEW transitions and cadence; sufficient expertise rather than minimal reads; smallest justified implementation before abstractions; immediate checks for dangerous boundaries; security specialist/gate selection rules; profile/pack discovery and justified full-profile use; local-first skills and explicit external scouting; reference modes; current permissions; RISK_0–RISK_4; topology and one-writer ownership; independent review versus self-review; bounded stopping; user agency and authorized merge boundary. |
| `skills/using-agent-skills/SKILL.md` | Mechanical metadata discovery; exact explicitly selected body delivery; activation invariant and integrity checks; resource progressive disclosure; source precedence; unified vendored catalog; delivery receipts and schema-3 worker payloads; context retention limitations; authority envelope over upstream lifecycle language; adversarial review of serious ideas; ordinary-file-reader fallback and truncation handling; actual procedure application and outcome checks. |

`AGENTS.md` points repository hosts into the same contract. `CLAUDE.md` and
`CODEX.md` retain provider-specific adapters. The CLI, bootstrap, worker builder,
verification runtime, MCP manager and continuity store are mechanical services;
they are not additional always-loaded specialist skill bodies.

## JIT and context decision

Use purpose pointers first, then inspect matching metadata and read enough full
bodies to cover the stage's material requirements. Do not optimize for the
fewest reads; do not load a broad profile automatically. Full frontend metadata
describes hundreds of KB of bodies, and all 403 bodies exceed 3 MB. Token costs
in the CLI/index are the explicit bytes/4 heuristic, not measured tokenizer
counts. Domain-specific subsets and stage transitions preserve room for project
facts. Reading metadata or generating hashes alone does not prove application.

The [Agent Skills specification](https://agentskills.io/specification) separates
metadata discovery, full body activation and on-demand resources. ChatGPT's
[Projects and chats documentation](https://learn.chatgpt.com/docs/projects)
describes project instructions and shared source files; it does not prove that a
particular chat actually reads Agentit. Both primary sources were consulted in
this audit.

## Current-source review and limits

Canonical refresh and adaptations are documented with exact source pins and
review decisions in [upstream maintenance](../docs/UPSTREAM_MAINTENANCE.md),
`skills/UPSTREAM_LOCK.json`, `skills/UPSTREAM_SOURCES.md`,
`skills/ADAPTATION_SOURCES.json` and `THIRD_PARTY_NOTICES.md`.

ECC is retained at `90606c8315ee09cafc303515c5f33024db6b9882`, with 4,627
verified source files / 61,903,407 bytes. Its 300 canonical skills and 11 source
aliases remain intact. Import did not enable hooks or execute native tools.

The canonical non-ECC lock verifies 43 packages / 698 managed files / 16 source
repositories. Forty-two packages match reviewed latest HEADs. `image-to-code`
was removed upstream, so its last verified canonical pin is retained explicitly;
it is not labelled latest. Refresh detects its reappearance and requires a new
retention decision. Owned adaptations keep original provenance and separate
latest-source review records; they are not falsely represented as byte copies.
The review covered 25 adaptation records plus seven older/live-reference origins.
Three historical records lack original input paths; their unchanged upstream
HEAD/license is verified without invented history. ThreeJS review covers its
current README rather than an external specialist library that Agentit does not
copy. DESIGN.md guidance now includes section-level fenced YAML and unique
top-level token keys.

Tests can prove inventory coverage, complete bytes, safe refresh and mechanical
delivery. A fresh isolated worker can demonstrate the reader navigation path.
Neither certifies instruction adherence across models, actual ordinary ChatGPT
sessions, model versions, context lengths or future compaction behavior.
`evals/entry-host-cases.json` defines the further host-observed entry, cross-domain,
BUILDER and truncated-source cases. Do not mark those fixtures as executed merely
because the Python suite passes.

## Reproduce the source checks

```sh
python3 scripts/build_profile_index.py --check
python3 scripts/build_chat_entry.py --check
python3 scripts/sync_upstream_skills.py
python3 scripts/check_skill_curation.py
python3 scripts/ecc_integrate.py
python3 -m unittest discover -s router -p 'test_*.py'
python3 -m unittest discover -s tests -p 'test_*.py'
```

Final local evidence: **316 runtime tests + 74 script tests passed**, both generated
entry checks passed, canonical and ECC integrity passed, and the final verifier's
source fingerprints were identical before and after execution. Independent
read-only review found the stale-runtime issue above; after its portable fix the
reviewer reported no concrete findings and the 15 runtime inventory tests passed.
The ordinary-reader smoke read the complete core, matching backend/engineering/
security metadata, then full diagnosis/security bodies; it did not claim to
execute an application or certify ordinary ChatGPT hosts.

Machine-private command outputs, runtime receipts and installation backups stay
outside Git. A repository change and a local installation are separate evidence;
publication, CI status, merge and other computers' installations must likewise
be reported separately.
