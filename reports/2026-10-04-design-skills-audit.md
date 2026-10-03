# Design craft and critics expansion — October 3–4, 2026

This continues the [all-profile audit](2026-10-03-skill-quality-audit.md) with the
requested priority on design and design critics. The original baseline and
October 3 outcomes remain historical evidence, not current inventory counts.
The catalog now contains **93 skills / 18 profiles**; this expansion adds nine
skills to the previous 84 and an opt-in `design-review` profile. Against the
original baseline, the PR adds fourteen skills and four profiles in total.
Default/global/core remain exactly the three navigation bodies.

## Delivered responsibilities

| Skill | Concrete job | Nearby job kept separate |
| --- | --- | --- |
| `typography-and-layout` | Type roles, hierarchy, measure, spacing, script/font rights, fallback and real-content proofs | Cross-media identity, component systems, copy meaning and file preflight |
| `brand-identity-design` | Marks, color, typography, imagery and application stress tests with a usable asset handoff | Positioning research, one asset export and UI component implementation |
| `design-system-engineering` | Inventory actual tokens/components/consumers; reconcile design/code/runtime drift; incremental migration and ownership | Merely storing visual memory in DESIGN.md or abstracting one button |
| `data-visualization-design` | Message, encoding, scales, missingness/uncertainty, annotations and target-size chart proof | Validating query/statistical math and whole-dashboard architecture |
| `editorial-design` | Reading map, report/deck sequence, captions, page rhythm and medium-specific composition | Editable-file generation and printer preflight; concepts need printer specs before readiness claims |
| `design-critique` | Read-only visual/copy second opinion against the brief; located, prioritized, evidence-labelled repairs and retests | Building/polishing, participant testing and accessibility certification |
| `ux-heuristic-review` | Walk real user tasks and proposed/implemented states for understanding, control and recovery | Visual taste, participant research and technical access testing |
| `accessibility-design-review` | Names, keyboard/focus, forms, dynamic states, reflow and automated/manual evidence boundaries | Scanner execution alone, component implementation and conformance certification |
| `motion-design-review` | Diagnose purpose/frequency, interruption, continuity, motion preferences and measured vs suspected runtime cost | Motion creation, library migration and proven-bottleneck optimization |

Optional references remain explicit JIT reads: broad-critique report contract,
cross-surface design debt, motion coverage, normative accessibility boundaries
and cognitive comprehension. Cognitive review distinguishes necessary task
complexity from avoidable recall/decision burden; counts are not conformance
scores or participant results.

## Broad discovery and source comparison

Search covered current GitHub repositories, pack directories, Reddit discussions,
X-indexed search and primary web sources. Popularity and creator claims were
used as leads, never as proof of quality. This is a broad bounded search, not a
claim that the entire internet or every file in each pack was evaluated.

Pinned paths and exact retained MIT license hashes are in
[ADAPTATION_SOURCES.json](../skills/ADAPTATION_SOURCES.json). Source bodies were
read by the owning researcher/writer before adaptation; code and upstream
installers were not executed. The original procedures were rewritten for
Agentit's host-neutral authority, selected delivery and truthful evidence.

| Primary source | What was inspected | Decision and material contribution |
| --- | --- | --- |
| [RampStackCo](https://github.com/rampstackco/claude-skills/tree/3d4510a94a76ead80122c691b5c480f92f3fbe40) | Creative/art direction, identity and design-system bodies, root MIT | Adapt identity application tests and actual-system layers/governance; direction is incorporated into existing jobs rather than another generic creative-director owner |
| [Peter Bamuhigire](https://github.com/peterbamuhigire/design-system-skills/tree/c9b334d770c449db7401730db29c9b70953e62f1) | Eight typography/font-rights, editorial, chart and deck/print bodies, root MIT | Adapt professional craft/proof procedures; reject font bans, paid-font discovery, fixed ratios, assumed locales and source-specific mandatory tools |
| [OneWave](https://github.com/OneWave-AI/claude-skills/tree/fc5b7851a6c7ba367e05797df46ad3679df355dd/claude-design-critic) | Design critic body, root MIT | Adapt exact locations, actionable repair report, copy pairs and grounded strengths; reject universal purple/emoji bans, automatic remediation and marketing labels as evidence |
| [Crit](https://github.com/vmarafetti/crit/tree/87a6c56a8b718be061723f44300eee4a859adcb9) | Researcher read skill/audit/template; integrator inspected report structure and MIT | Adapt stable finding IDs and action/coverage split; reject mandatory six-lens scope, legal assertions, arbitrary scores and made-up effort hours |
| [Owl designer skills](https://github.com/Owl-Listener/designer-skills/tree/9a6930cf84a822eb458624bd11c61aac5bbdf224) | Critique, heuristic-evaluation and debt bodies, root MIT | Adapt task-based expert walkthrough and optional debt inventory; remove fixed evaluator counts and multiplication of ordinal labels |
| [Motion principles](https://github.com/kylezantos/design-motion-principles/tree/4a9ca879f24a361f4dca4174fe2da0f67b5ddee3) | Main creation/audit body, root MIT | Adapt technology-neutral contextual audit; omit named-designer personas, prescribed output and scripts |
| [a11y-agent-skills](https://github.com/smukh/a11y-agent-skills/tree/8bc24f049734c607e23bd3955700fd4858649614) | Accessibility audit body, root MIT | Adapt reproducible state and automated/manual evidence boundary; no CLI/MCP/Action/scanner runtime adopted |
| [Owl inclusive skills](https://github.com/Owl-Listener/inclusive-design-skills/tree/6e0740f04b2130af60bc57abe3401b91e460e70d) | Cognitive-load assessment body, root MIT | Adapt selective cognitive/comprehension branch; no numeric accessibility verdicts |
| [ibelick UI skills](https://github.com/ibelick/ui-skills/tree/ebf5f26cd275b1412be8a2c8784c4f8da628e7c2) | Accessibility and motion-performance bodies, root MIT | Adapt native-first, located access review; existing performance owners cover technical optimization, no duplicate performance skill |
| [gstack](https://github.com/garrytan/gstack/tree/ac20ef1e1380248fcaeea337d39f5fd2b04b7a3b) | Design checklist, metadata, MIT and third-party NOTICE | Retain as comparison; no scripts, auto-fix rules, browser runtime or template text incorporated |
| [Genjutsu / former Creative Excellence](https://github.com/AThevon/genjutsu/tree/09c177b1868f14deb24a7bc0b258348130167c8d) | Cast body and scoped MIT notices | Inspiration only: useful interaction thesis already covered; reject host-specific mandatory multi-agent/tool pipeline |
| [Microsoft CAT](https://github.com/microsoft/cat-agent-skills/tree/54647c5d4cfa6908d17864cfa1c62196277ac6e5) | Brand-template-enforcer body, root MIT | No new owner: actual Office template reuse belongs to artifact-production, not another generic design skill |
| [Taste skills](https://github.com/Dragoon0x/taste-skills/tree/bb8bf6b8bb0b56160ca34846158286855c6f091d) | Visual/team critique bodies, MIT plus TERMS overlay | No material copy; overlap and extra terms do not earn an additional primary taste owner |
| [UI analyzer](https://github.com/tomwangowa/agent-skills/tree/48b25ae2767f7575698e16ad2a46d1a96b19b5f9) | Screenshot analyzer body and license search | Reject: no inspected root reuse license, overly broad prescriptions and unsupported screenshot precision |
| [Anthropic knowledge-work plugins](https://github.com/anthropics/knowledge-work-plugins/tree/8444efcd48f7012f09797778a36a33e73d0861f4) | Exact tree/path check | Cited design-critique body absent at this revision; no adoption from catalog claims |
| [OpenDesign](https://github.com/nexu-io/open-design/tree/53231d40b778d88eba23f35547bf99485d3ae9fc) | Public runtime/protocol discovery | No independently inspected critique procedure adopted; runtime expansion is outside this skill-method change |

The RampStack tree repeats the same source skills across distributions; its
309 SKILL paths were **not** counted as 309 unique capabilities. Source pack
size is not an activation quota or a justification to import all files.
`ramricky/interface-design` could not be resolved at the inspected endpoint;
`0xdesign/design-plugin` and design directories remained discovery leads, not
licensed material copied into Agentit.

Existing Hallmark, taste, Impeccable, Emil, GSAP, mobile, Figma and 3D coverage
was compared before adding owners. They retain their canonical bytes. Generic
visual critique is an explicit **alternative**: choose `design-critique` or the
Impeccable critique method, not both by default. The new method provides a
manual, provider-neutral repair report without requiring its upstream launcher.
Specialized UX/access/motion critics have different tasks/evidence. Figma's
Agentit-owned companion guidance now chooses by need rather than prescribing a
five-skill bundle.

## Social and normative sources

Reddit discussions surfaced existing Impeccable/UIUX/taste, motion and newer
pack leads. Examples inspected during discovery:

- [Codex design-skills discussion](https://www.reddit.com/r/codex/comments/1wownb5/not_a_codex_expert_need_help_for_design_skills/)
- [Comparison discussion](https://www.reddit.com/r/ClaudeCode/comments/1syachi/best_skill_for_uxui_impeccable_vs_uxui_pro_max_vs/)
- [Recent Codex tools/skills discussion](https://www.reddit.com/r/codex/comments/1ww472q/what_tools_or_skills_are_you_using_to_improve/)

X searches did not yield usable verified design-skill posts in this expansion;
indexed results were largely irrelevant. No claim of a complete X audit is made.
Relevant packages were inspected directly on GitHub instead. W3C
[WCAG guidance](https://www.w3.org/WAI/WCAG22/quickref/),
[WCAG 2.2](https://www.w3.org/TR/WCAG22/),
[ARIA APG](https://www.w3.org/WAI/ARIA/apg/) and
[COGA](https://www.w3.org/TR/coga-usable/) govern standards-related checks;
cognitive guidance remains supplemental, not a generic compliance verdict.

## JIT, profiles and actual Agentit use

`design` now makes the new craft/review owners available. `design-review` extends
core with only review/evidence capabilities; `product`, `data`, `artifacts` and
`all` expose the relevant new responsibilities. No profile loads bodies.
Metadata-only discovery and exact selected-body/resource loading are covered by
curation regressions across all fourteen skills added in this PR.

Actual main decision: `DISPATCH_DECISION: agentit`, bounded design expansion,
RISK_2, research/design/writing discovery, reference mode `both`, selected
`reference-intelligence` and `skill-authoring-and-evals`. Main moved from
BUILDER integration to REVIEW. Stage activation receipts and concrete validated
schema-3 worker prompts remain in private `.agentit/`; they are not proof of
attention or an OS sandbox. Research and writing scopes were disjoint; the
blind selector received candidate metadata without bodies or expected answers.

## Verification and observed behavior

- Router suite: **276 passed**. Tests suite: **49 passed**, including seven expanded
  curation regressions for all new bodies/references.
- Offline catalog/provenance: **93 skills / 18 profiles / 18 adaptation sources**.
- Canonical integrity: **41 packages / 599 files / 15 sources** verified unchanged
  by this extension. Core/global/default unchanged; no lock refresh needed here.
- Independent blind metadata selection: **22/22 authored boundaries met**,
  including every new owner's positive and near-miss case. The input contained
  the complete intended candidate metadata from five relevant packs (81 entries,
  including repeated IDs across packs). This is one observed selection sample,
  not a causal quality benchmark or proof of general reliability.
- [Selection outputs](../evals/design-observed-selection-20261004.json) and
  [source-only critic exercise](../evals/design-observed-behavior-20261004.md)
  preserve actual outputs rather than merely authored expectations.
- Documentation drift checked against the affected README/profile table,
  discovery packs, registry, curation policy, notices and exact source manifest.
  Original dated audit counts remain historical. No private cache/transcript,
  credentials or source installs are included.

Independent review found that declared inspected-source paths could be emptied or removed without rejection. New path-bearing records now declare that provenance field mandatory; missing/empty/non-list, absolute, traversal, non-canonical, backslash and duplicate paths are rejected by a focused mutation regression. Legacy records retain their earlier contract rather than receiving invented source paths. The reviewer’s source-only exercise is preserved above.

The [synthetic source fixture](../evals/fixtures/design-source-only.html) and source-only exercise deliberately lack captures, runtime measurements and
callback implementation. It tests evidence honesty, approved-brand preservation
and retestable repairs. It does **not** establish visual fidelity, keyboard/AT
behavior, actual duplicate orders, FPS, contrast, WCAG conformance, user-test
results or commercial improvement. Rendered comparative tasks and human design
review remain necessary before claiming that these skills produce better
outcomes than every alternative.

Rollback is a normal revert of this opt-in extension. No merge, global user
installation, deployment, paid-tool activation or upstream executable ran.
