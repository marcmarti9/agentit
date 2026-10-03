# Profile and skill quality audit — October 3, 2026

## Delivered change and evidence boundary

The baseline at `edd0b15e317ffaad95d09e8158cb49f2ac2a2e80` contains **14 profiles / 79 installable skills**, not the older documented 75. The branch contains **17 profiles / 84 skills**. Every baseline body was inspected for declared responsibility, trigger, competing owner, context cost and retention evidence: [profile/body audit](2026-10-03-profile-skill-audit.md), [hash-bound inventory](2026-10-03-baseline-inventory.json). All 79 baseline body hashes and the profile hash were checked against baseline Git objects; that review is source evidence, not behavior measurement.

Five missing responsibilities now have bounded opt-in owners: generated-domain property tests, analytical claim/data quality, source-security finding investigation, Expo/React Native runtime state/performance, and reusable artifact production. Four existing owners gained conditional references rather than duplicate top-level skills. Six canonical source revisions were refreshed without editing upstream bytes. Core/default/global remain exactly `using-agentit`, `task-router`, `using-agent-skills`.

“Best” here means the strongest useful procedure among the inspected, scoped candidates, not a proven ranking of every public skill or a universal model-quality claim. No size quota drove selection. Large canonical bodies are retained; host/framework limits and tool availability still matter.

## Decisions across every profile/category

| Profile/category | Primary comparison and current owner | Decision / residual boundary |
|---|---|---|
| core / agent runtime | Agentit entry, semantic router, exact loader; Anthropic skill-creator evaluation concepts | Retain three core bodies and runtime selection; improve existing authoring reference, no external router/hooks/personas. |
| frontend | Addy engineering, existing taste/Impeccable/UIUX/React composition; Vercel React guidance | Retain visual owners; add PBT/security investigation discovery. Vercel performance overlaps existing performance/composition; no second React catch-all. |
| backend | Addy API/TDD/hardening and Trail of Bits | Add generated-domain contracts and finding triage; metric quality separate from operational observability. No automatic scanner installs or queue framework. |
| supabase | Supabase agent-skills, existing database package | Refresh canonical pin; inherit backend additions. Database query/RLS/performance stays with database owner; analytical grain/claims stays with data quality. |
| product | Existing ideation/adversarial/spec owners; marketingskills customer-research | Add source intelligence/data quality discovery. Generic specs do not introduce Spec Kit; customer evidence procedure fits marketing/reference owners. |
| executive | OpenExecutive bounded scenarios and existing executive roles | Add decision packet, scoped specialist questions, reconciliation, reversal criteria behind an explicit reference. Add metric/file owners; no persona committee or multi-agent runtime import. Sales/customer-success projects still require actual company/domain context. |
| writing | Existing documentation/humanizer/stop-slop; OpenAI PDF procedures | Add artifact production and source intelligence. Humanizer and stop-slop remain alternatives; ordinary chat prose does not invoke office tooling. Translation-specific procedures remain a candidate, not an unsupported import. |
| design | Existing taste, concept, narrative, GSAP/Three.js, UIUX and diagram packages; Vercel/W3C comparison | Retain distinct concept/narrative/engine owners; choose one primary taste system. No new generic design/accessibility duplicate. Defer diagram upstream update for missing verifier dependency (below). Formal accessibility certification is not claimed. |
| mobile | Existing Appllama UI vs Expo skills / Callstack RN best practices | Add runtime hydration/deep links/error states/idempotency and measured device performance; retain visual owner. Scope explicitly Expo/RN, not Flutter, Swift or Kotlin. Store submission remains platform/version-specific work. |
| release | Existing launch/CI/security gate vs Trail of Bits | Add investigation discovery; routine evidence vs multi-surface gauntlet vs final security gate remain distinct. No release/security clearance or incident-operation authority follows from package inclusion. |
| research | Existing source/reference/spec/adversarial owners; licensed research/eval concepts | Add source-role/immutable-license record, data and artifact owners. Framework version correctness stays with source-driven-development. |
| growth / SEO | Existing marketing SEO/content references vs marketingskills and broad packs | Strengthen marketing evidence-to-experiment contract; inherit product data owner. No duplicated forty-skill marketing router, SEO owner or external campaign execution. |
| agency | Existing planning/incremental/growth vs executive/artifact procedures | Add reusable artifact availability and preserve accountable operational boundaries. Do not create new account/contract control planes without a real change model. |
| all | Full explicit catalog | Add five IDs to inventory; never activate/deliver this profile wholesale. |
| new data / security / artifacts | Responsibilities above | Focused availability profiles; inheritance only, no new activation mechanism. |

The baseline audit’s absent-specialist labels are hypotheses, not proof of incapacity: accessibility/SEO already have relevant guidance; domain-specific persistence, incident handling, localization and store policy need real task/platform evidence before adding permanent owners.

## Primary source comparison and licensing

All accepted source records pin immutable revisions and inspected scoped licenses, with exact LICENSE/NOTICE bytes distributed under `vendor/adaptation-licenses`. [Machine-readable manifest](../skills/ADAPTATION_SOURCES.json) and [notices](../THIRD_PARTY_NOTICES.md) identify modified scopes. These are provider-neutral adaptations without upstream runtime/scripts.

| Inspected source | Specific useful procedure | Integration decision |
|---|---|---|
| [Trail of Bits skills](https://github.com/trailofbits/skills/tree/82fe8226252622fa807643bdca1710901198553a) — CC-BY-SA-4.0 | Valid generators, independent properties, shrinking; source/sink/control/coverage and variant triage | New `property-based-testing` and `security-analysis`, including their refs, **CC-BY-SA-4.0**. Explicit exceptions to Apache-2.0. |
| [Trail of Bits Testing Handbook](https://github.com/trailofbits/testing-handbook/tree/190294f0ed563baddf4941cd2388be5bd4d5c5ba) — CC-BY-4.0 | Scanner configuration and evidence interpretation | Source attribution retained for security-analysis adaptation. |
| [ajrcre data-analysis-skills](https://github.com/ajrcre/data-analysis-skills/tree/cbc906e4912a980423aecd1e318061eb98f3e0b2) — MIT | Grain/population/cut-off, joins, formulas and independent controls | New data-quality owner; original synthesis plus retained MIT notice. No database or visualization duplicate. |
| [Expo skills](https://github.com/expo/skills/tree/13ad8e05874195633b5c185f6947bb6400e228fc) — MIT | Router/auth hydration, navigation intent, fetching and offline/cancellation state | Mobile runtime owner/state reference, with installed-version verification. No EAS/OTA/upload or native-module instruction import. |
| [Callstack agent-skills](https://github.com/callstackincubator/agent-skills/tree/61e6e7dfdf3a8ee862254c200d751fcb1fb863dc) — MIT | Localize RN performance with native/JS evidence before optimizing | Mobile performance reference; comparable build/device/data, not mandatory profiler/tool installation. |
| [OpenAI skills/PDF](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/pdf) — scoped Apache-2.0 | Render saved PDF pages and inspect; text extraction is separate evidence | New artifact owner, format-specific controls and editable source. Office formats also have Agentit-authored controls; no claim of copying those separately licensed packages. |
| [OpenExecutive](https://github.com/SenteLabsAI/OpenExecutive/tree/bba990f20dab7559967010e65b65630f1a35c684) — Apache-2.0 | Bounded executive scenarios, coherent trade-off synthesis | Strengthen existing executive/reference branches; preserve LICENSE and NOTICE, no runtime/persona import. |
| [marketingskills](https://github.com/coreyhaines31/marketingskills/tree/dda3841f0b294e01e93b1541486beefbfab0915e) — MIT | Source bias, customer evidence, observable output/experiment criteria | Existing marketing/reference branches; reject overlapping catalog/tool/context convention import. |
| [Anthropic skill-creator](https://github.com/anthropics/skills/tree/8a1541c4a3ffa5a20a5a91de0dcf3f0bab1d1ef4/skills/skill-creator) — scoped Apache-2.0 | Paired output/assertion comparison, variance and human review | Existing authoring evaluation branch. No Claude-specific CLI/browser workflow; no inference that every Anthropic package has the same license. |
| [Vercel React agent-skills](https://github.com/vercel-labs/agent-skills/tree/063bee94c3f4df8453406c830b0a7df0f2860278) | React performance/composition coverage | Compared and retained existing owners. Package-frontmatter licensing is scoped; no root-license or imported-runtime claim. |
| [Vercel agent-browser/dogfood](https://github.com/vercel-labs/agent-browser/tree/526157cfd4ec64f45939f9ba0f10d5936aa7ac33) — Apache-2.0 | Evidence-led exploratory browser QA | Retain `browser-testing-with-devtools`; no browser/release-testing duplicate. |
| [tebakkasus/skills](https://github.com/tebakkasus/skills/tree/a96cc20bb5e0d47ff7fdcee967eebd561c99deb2) — MIT | Broad product/marketing/research catalog | Compared and rejected overlapping top-level expansion. Breadth alone is not better behavior. |

Existing canonical design sources (taste, Impeccable, UIUX, Emil, Appllama, diagram) and engineering packages were compared through the baseline bodies and fresh upstream plans; their pins/licenses remain in [UPSTREAM_SOURCES](../skills/UPSTREAM_SOURCES.md), not duplicated into the adaptation manifest.

## GitHub, Reddit, X and web discovery

GitHub pinned source bodies and scoped licenses supplied implementation evidence. Social sources supplied leads/context only; popularity, claims and install snippets were not acceptance criteria. Searches included current skills/packs, category-specific procedures and comparison to existing owners.

- [Reddit: use in real codebases](https://www.reddit.com/r/ClaudeCode/comments/1qff04w/how_are_you_using_skills_in_real_codebases/) was opened and inspected: community approaches illustrate lazy discovery and differing workflow conventions; they do not prove quality or justify importing hooks.
- [Reddit: repositories](https://www.reddit.com/r/claudeskills/comments/1vypjfq/top_agent_skills_repositories/) and [Codex value discussion](https://www.reddit.com/r/codex/comments/1wsgdmv/best_codex_skills_that_add_the_most_value_beyond/) were discovery leads. Claims of superiority/testing require primary evidence.
- X searches surfaced [organization/deduplication discussion](https://x.com/_simonsmith/status/2029713209179988445) and [skill-design discussion](https://x.com/NickSpisak_/status/2033974734723887333). Direct opens failed in this environment; only search-index excerpts were available. No procedure, license or technical claim was adopted from X. This is explicitly partial X access, not a completed full-post review.
- [W3C Easy Checks](https://www.w3.org/WAI/test-evaluate/preliminary/) is a primary comparison source for accessibility basics; it did not justify a second generic UI owner or a certification claim.

## Canonical refresh: accepted and deferred

Read-only refresh planning examined all 15 sources. An independent worker reviewed the fresh diff and refresh lock/application behavior. Six changed pins were accepted:

- Addy `1401c8b8030e023baeebb31781a6653fe8e93026`: valid JS rethrow, stronger mutation/review/spec discipline, floor-guard checks, progressive performance references.
- Impeccable `e103efe779e2dd01274dabae83531fef00bf2563`: mode references, launcher version/exit propagation and browser-session changes. Canonical launchers were preserved, not run; binary safety and Windows execution are unverified.
- UIUX `477bcb28c9812b385cb51a4605ddf30d7b2266e2`: upstream relevance-fixture change.
- Emil `e8a175de22ae1e49370fc144c1f3bb9aeedf988d`, Supabase `c9be0e931b7930f7d02126d04774d904c381e7d7`, Vercel skills `18f96ea131dab3b0fcc9b27cf7c6f6cbb6174680`: changed source revisions with mapped package bytes unchanged.

Diagram candidate `f903933a534ba92cde1c85a28186267b3a317bb2` is deferred: its new architecture-delta path requires repo-root verifier scripts not included in the distributed package mapping. Retained pin is `57148ac6f7cf8f2d0080f23437ab2929bca15f3e`. Do not rewrite canonical instructions or manufacture a verifier pass. Offline application produced 41 canonical packages / 599 managed files / 15 sources.

## Observed selection and response evidence

Thirty [cases](../evals/skill-curation-cases.json) cover five new owners plus competing procedures and negative triggers. Two isolated workers produced observed selections, not scripted routing. [Raw packets, original rubric and outputs](../evals/observations/2026-10-03/) are retained.

Exploratory packet: 28/30 matched its authored original rubric. One required owner (design inspiration) was absent from its candidate set; TDD metadata had been overwritten with a narrower data-pack description. These are fixture defects. The corrected fresh-context packet uses complete description metadata and includes the absent owner; it again scored 28/30 against the unchanged original rubric, with two rubric disagreements: ordinary test-only work selected no TDD, and prose editing selected the documented stop-slop alternative.

The rubric was then corrected with source-based reasons, **not silently rescored as a quality win**: canonical TDD owns implementation/behavior changes, so two examples on an unchanged function need no mandatory body; humanizer and stop-slop are explicitly alternatives, so require one valid primary set. Original expected answers and all observed outputs remain available. All positive/negative checks for the five new owners were respected in the corrected observed sample. No universal selection-rate or baseline-improvement claim follows.

Eight [observed response plans](../evals/observations/2026-10-03/behavior-plans.md) were generated after explicit exact-body/reference delivery. Manual inspection found the requested distinguishing controls: independent sort properties, join grain/control counts, observation versus causal explanation, scan coverage versus exit success, ownership versus login/parameterization, retained draft/idempotency under uncertain write, actual PDF render versus extraction, and spreadsheet calculation versus cached values. These are model plans, not executed apps/scans/device/office tests. No paired baseline/treatment application benchmark was run; the paired-eval branch documents how to make such claims later.

## Agentit actually used

The main task recorded `DISPATCH_DECISION=agentit`, `TASK_DECISION`, `DEVELOPMENT_MODE=REVIEW`, RISK_2, scope, selected packs/bodies/reasons, references and verification in private `.agentit/audit/TASK_DECISION.json`. The repository CLI performed pack/candidate discovery and exact activation/resource reads with task/stage receipts. Selected bodies: reference-intelligence, skill-authoring-and-evals, source-driven-development, security-and-hardening; completion and review bodies were selected for final verification/review. Delegated workers received actual validated schema-3 payloads with complete selected bodies and applicable project instructions, rather than an ID-only list. The deterministic runtime also ran the curation checker through loop-init/run/check with `--require-command`; this is command-bound structural verification, not quality scoring. Private operational state/receipts were not committed. Neither receipts nor envelopes prove attention, context erasure or OS isolation.

## Verification and remaining boundaries

The new offline checker validates opt-in/core inventory, pack coverage, fixed source revisions, exact retained license/NOTICE hashes, safe target paths, reviewed license identifiers and adaptation frontmatter licenses. Regression tests check metadata-only discovery, exact single-body delivery, explicit references and rejection of bad provenance. CI runs both this checker and existing canonical integrity tests. These checks do not choose natural-language intent.

Fresh local validation: 276 router tests and 48 script tests passed; the six curation tests were rerun after the final frontmatter/rubric validation edit. Canonical integrity verified 41 packages / 599 files / 15 sources; curation structure verified 17 profiles / 84 skills / 9 adaptation sources. Shell/Python syntax and YAML/JSON/capability configuration checks passed. A temporary-home offline bootstrap across Claude, Codex, Grok, Gemini and Antigravity delivered only the three core skills globally, preserved exact adaptation license bytes in private runtime, and passed idempotent apply/rollback. Dependency installation was deliberately skipped in this local smoke; remote Linux/macOS CI tests real dependency installation. The independent final reviewer found arbitrary license identifiers were accepted. That finding was fixed by restricting identifiers to the four actually reviewed licenses and adding two mutation cases; new licenses require review before expanding the schema. Remote CI results are recorded in the PR. Documentation drift was checked across profiles/packs/registry/README/ABOUT/JIT/curation/upstream/notices and current inventory counts; historical snapshots remain explicitly dated. No global user installation, merge, deployment, scanner execution, external service activation, paid action or application/device/renderer benchmark was performed.
