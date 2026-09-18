# Agentit adversarial audit — pass 1, 2026-09-18

## Scope and evidence boundary

Baseline: `main` at `bf880fd7e04cb541eff48527ad9b54bf4bf0270c`. The pending SEO consolidation in PR #53 is not in this baseline. All **75 SKILL.md packages** were inventoried for metadata, size, discoverability, source ownership, overlaps and local links. Runtime tracing and adversarial reproduction concentrate on discovery, loading, worker projection, installation, evidence receipts and update paths. This is not an exhaustive factual revalidation of every statement in every upstream reference, nor an independent second-model audit.

Reproducible clean-run evidence: GitHub Actions run `35371883907`, artifact `10558103335`. Baseline: **201 router tests, one failure** (uncatalogued `local-seo-playbook`); **27 script tests, all passing**. The source snapshot and both complete logs are retained in the artifact. `jit-baseline-probes.json` records separate behavioral probes, not an LLM quality benchmark. `jit-skills-baseline.json` records each original package and digest.

## Intended operation versus implementation

The intended pipeline is: minimal core → model-owned task decision → pack metadata → selected skill bodies/resources → bounded worker/tool context → observed verification → scoped learning. Private profile installation already keeps most skill metadata out of host discovery. The semantic decision remains the primary model's job; no string-matching classifier should select a task's skills.

**Verdict at baseline: JIT is partially implemented, not an end-to-end guarantee.** The standalone loader reads real bodies, but the worker builder passes only IDs and calls them active. Installation availability is being confused with activation in a compatibility path. Tests prove useful installation/state invariants, but do not demonstrate that a real host/model loaded, understood or obeyed the right instructions.

## Findings, reproduction and repair acceptance

| ID | Priority | Finding / evidence | Required acceptance |
|---|---|---|---|
| J01 | P0 | `worker_context.render_worker_prompt` lists selected names, never calls the body loader. A marker present only in a selected body is absent from a spawn-valid prompt. | Selected exact bodies and digests survive projection; missing/tampered material blocks validation. |
| J02 | P1 | `resolve_skills_projected([], manifest, True)` activates the manifest without a fresh selection. | Installed availability never becomes a task selection. |
| J03 | P1 | Instruction discovery reads root and leaf, omitting intermediate `packages/AGENTS.md`. | All ancestor instructions in the bounded work path survive, in increasing specificity. |
| J04 | P1 | Loader resolves away a root symlink before testing it; dangling skill-path symlinks evade the initial existence check. | Reject unsafe roots/resources before reading; test direct/dangling/nested symlinks and traversal. |
| J05 | P1 | Any untracked `.agentit/profile-skills` body can silently override the harness. Cache ownership/digests are checked on writes, not on reads. | Validate managed cache manifests and file hashes; reject stale/tampered cache; preserve intentional project-native overrides. |
| J06 | P1 | `record_attempt(passed=True, evidence='I think tests pass')` yields a valid passed receipt with no executed verifier. A hash authenticates nothing by itself. | Distinguish self-report from process observation; a contract requiring command evidence cannot pass on self-report. Keep legitimate human/visual evidence explicitly labelled. |
| J07 | P1 | `sync-upstream-skills.sh` copies then deletes Hallmark, Humanizer, UI UX Pro Max, Appllama app design and diagram-design. | Exercise the entire update with offline upstream fixtures; every mapped package survives. |
| J08 | P1 | Three core bodies total **41,481 UTF-8 bytes**, plus 12,786 bytes of AGENTS; overlapping FAST / mandatory lifecycle / interview / audit policies contradict each other. | Small core, one mode contract, explicit precedence for upstream procedures; no implicit all-skill lifecycle or mandatory repeated interview. |
| J09 | P1 | Two owned SKILL files have invalid YAML (`scrollytelling-web`, `threejs-product-storytelling`); ten non-core skills are absent from pack discovery; local SEO also absent from all-profile. | Validate every package, mapping and frontmatter; all owned capabilities are discoverable without globally loading bodies. |
| J10 | P1 | Logical cold start / disable is sometimes described like context erasure. Most hosts append skill bodies to conversation context. | Explicitly separate selection, delivery, host retention and fresh-context isolation. No fabricated unload/reset claim. |
| J11 | P2 | Worker builder defaults to max 12 skills despite no quota contract; reference IDs are called projected without bodies. | No hidden quota; surface measured bytes and unresolved locators; require material references before spawn. |
| J12 | P2 | Relative shared-resource paths are ambiguous in private profile installs; host core does not clearly teach the private discovery CLI. | Document and test explicit roots and an exact-resource loader, with no automatic whole-library load. |
| J13 | P2 | Skill delivery has no task/stage receipt. A printed list of selected skills cannot establish actual content delivery. | Optional task/stage-bound receipts record delivered hashes/bytes, not asserted comprehension. No implicit selection reuse. |
| J14 | P1 | Optional precompact hook feeds transcript into an unrestricted headless Claude command, with no timeout or separate opt-in. | Remove model execution from the hook; preserve only a bounded, explicit user-approved continuity workflow. Existing installations must be refreshed. |
| J15 | P2 | Large overlapping design/editorial skills can cause conflicting taste directives; entire upstream sync can replace local policy. | Clarify alternative vs complementary use. Preserve canonical upstreams; keep Agentit integration policy outside vendored bodies and protect its core adapter from sync. |
| J16 | P2 | Capability envelope is a requested grant, not an OS/provider sandbox. Reviewer payload does not prove independent process/model execution. | Label enforcement layer and unobserved capabilities; never certify isolation or least privilege from JSON alone. |

P0 means the central worker JIT contract demonstrably fails. Priority is audit judgment, not a vulnerability severity score. These are local tooling defects, not evidence of exploitation or production compromise.

## What already works and should be preserved

Private profile storage, bounded `skills candidates`, exact explicit skill loading, project-native override precedence, hash-checked installation/rollback, graph dependency ordering, bounded retry mechanics and least-privilege capability resolution are useful. Do not replace them with a second orchestrator, hard-coded semantic router, mandatory agent committee or indiscriminate mega-skill. Fix the interfaces between them.

## Skill overlap decisions

Design taste alternatives (`hallmark`, `design-taste-frontend`, `impeccable`) are not interchangeable files to concatenate. Pick a primary design approach; add a specialist only for an unmet requirement. `ui-ux-pro-max` is a lookup/data resource; `emil-design-eng` is component/motion polish. Concept, inspiration, trend research, storytelling, implementation, GSAP performance and 3D scene construction are complementary stages, not a mandatory pipeline.

`humanizer` and `stop-slop` are alternative editorial passes. `spec-kit-workflow` is an opt-in project/toolchain specialization, not a second mandatory spec pipeline. `app-security-gate` is release evidence, while `security-and-hardening` is implementation guidance. `adversarial-idea-review` attacks a business/product candidate; `doubt-driven-development` attacks an artifact; ordinary code review and evidence validation are distinct. Executive skills retain bounded functions; do not auto-load the whole bench. Local/AI SEO duplication is handled by the pending PR #53 and must not be independently reimplemented with conflicting paths.

## External evidence, separate from repository evidence

- Agent Skills specification: https://agentskills.io/specification — metadata-first discovery, selected bodies, bounded supporting resources; recommendations for shorter entrypoints.
- OpenAI skills documentation: https://developers.openai.com/codex/skills/ — names/descriptions first; selected body loading; host metadata budget can omit candidates.
- Claude Code skills documentation: https://code.claude.com/docs/en/skills — loaded content persists in conversation; forked workers are a different context boundary; tool declarations are not a universal sandbox.

Accessed 2026-09-18. These establish host semantics, not that Agentit has passed an actual Claude/Codex behavioral evaluation.

## Pass 2 contract

Start implementation from this frozen finding list, not the previous assumption that JIT already works. Add regression tests that fail on the baseline, then change the smallest shared loading/projection/evidence paths. Re-run catalog-wide checks, isolated CLI/worker fixtures, upstream refresh simulation and both existing test suites. Bind final evidence to the implementation revision. Keep main unchanged and publish reviewable changes.

A new test process is a genuine isolated process, **not** an independent LLM review. Native host selection accuracy, attention, instruction compliance, latency and end-to-end task quality require separate observed host runs. Missing host evidence must remain an explicit limitation, not be replaced by a green unit-test claim.
