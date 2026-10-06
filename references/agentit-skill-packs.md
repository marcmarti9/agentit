# Agentit runtime skill packs

Packs are **flat semantic discovery maps**, not context bundles, tiers, curricula, priority lists, or routing code.

Their only job is to let a capable agent quickly answer:

1. what domain am I working in?
2. what Agentit skills exist around that domain?
3. what problem does each skill solve?

The primary AI then decides which skill bodies to load and **how many**. There is no minimum, maximum, default count, level, or required order.

A pack with twenty listed skills can still lead to `selected_skills: []` or one selected skill. Another task may justify many. That decision belongs to the model looking at the actual task.

A new execution session starts semantically cold: installed profiles and skill files remain discovery surfaces, but only the three global core skills are assumed active until the new task selects more.

## Overlapping approaches

For an actionable visual/copy second opinion choose `design-critique` or the Impeccable critique procedure as the primary method. Their overlapping generic judgment is an explicit alternative, not a reason to load both. Task-flow, accessibility and motion critics have distinct evidence scopes; choose only the lenses that change this review. Creation, system engineering, chart encoding and editorial composition have separate deliverables.

Choose one primary taste approach (`hallmark`, `design-taste-frontend`, or `impeccable`) for a design decision; their different taste constraints should not be concatenated indiscriminately. Data lookup (`ui-ux-pro-max`), research, 3D/motion implementation and performance may complement it. Use `humanizer` or `stop-slop` as alternative editorial passes, preserving evidence and uncertainty. Spec Kit is opt-in; executive roles are individual capabilities, not an always-on committee. Candidate wording is discovery guidance, never an automatic trigger.

## Worker projection contract

A spawned worker should receive something conceptually equivalent to:

```text
relevant_packs:
- design
- frontend

selected_skills:
- design-inspiration-research
- browser-testing-with-devtools

references:
- <only relevant curated/live material>
```

Schema-3 worker context includes the selected bodies and hashes; unread reference locators block spawn. The pack names are discovery/provenance labels. **Only the selected skill bodies consume worker skill context.**

Do not infer a skill count from pack size, task size, risk label, worker title, installed profile, or a previous session's selection.

---

## engineering

**Use for:** general implementation, bugs, refactors, repository changes, code quality, architecture, testing, debugging, security-sensitive code, performance work and engineering delivery.

**Skills in this pack:**

- `property-based-testing` — generated-domain invariants, independent properties, generators and shrinking; not ordinary example tests.
- `security-analysis` — scanner/SARIF triage, source-to-sink proof and variants of confirmed flaws; not routine hardening.


- `app-security-gate` — evidence-driven attack-path retesting for substantive application changes or release; not a global core skill.

- `anti-overengineering` — enforce BUILDER throughput and REVIEW depth without speculative architecture or repeated full-suite churn.
- `incremental-implementation` — build in small verifiable slices when incremental delivery reduces rework.
- `debugging-and-error-recovery` — reproduce, localize, fix and guard when something is actually broken.
- `planning-and-task-breakdown` — decompose non-trivial work when an explicit execution plan would help.
- `test-driven-development` — use behavioral tests to drive or prove implementation when TDD fits the change.
- `code-review-and-quality` — independent correctness/quality review before accepting meaningful code changes.
- `code-simplification` — reduce unnecessary complexity while preserving proven behavior.
- `constraint-driven-development` — write a project quality bar (`CONSTRAINTS.md`) and keep agents from quietly lowering it.
- `verification-before-completion` — fresh evidence before done/fixed/passing claims.
- `verification-gauntlet` — only for multiple material evidence surfaces; broader verification discipline when multiple evidence surfaces matter.
- `doubt-driven-development` — adversarially challenge unfamiliar, risky or consequential engineering decisions.
- `security-and-hardening` — threat modeling, trust boundaries, auth, secrets, input handling and hardening when security is materially involved.
- `performance-optimization` — measure and optimize real bottlenecks rather than guessing.
- `source-driven-development` — version-specific technical contracts; current official framework/library/protocol documentation materially affects correctness.
- `architect-orchestrator` — structural decomposition, architectural ownership or multi-stage coordination when one direct execution path is insufficient.
- `specialist-agent-routing` — spawn bounded specialists only when specialization, independence or context isolation is useful.
- `context-engineering` — control large or fragmented engineering context deliberately.
- `git-workflow-and-versioning` — branch/commit/history discipline when Git handoff matters.
- `documentation-and-adrs` — preserve durable architecture/decision knowledge when it would be expensive to rediscover.
- `diagram-design` — choose a truthful architecture/flow visualization route when spatial structure materially improves engineering understanding.
- `observability-and-instrumentation` — logs, metrics, traces and operational diagnostics when runtime behavior matters.
- `ci-cd-and-automation` — CI/CD and automated quality gates.
- `deprecation-and-migration` — safely retire or migrate interfaces/systems while preserving compatibility requirements.

---

## frontend

**Use for:** application UI implementation, browser behavior, accessibility, frontend architecture, runtime verification and frontend performance.

**Skills in this pack:**

- `property-based-testing` — parser/validator/state invariants when generated-domain testing is justified; not UI screenshot checks.
- `security-analysis` — investigate concrete UI/API attack paths or scanner findings; not styling-only changes.


- `app-security-gate` — test changed application trust boundaries before release.

- `frontend-ui-engineering` — production frontend implementation, component structure and accessibility baseline.
- `react-composition-patterns` — repair demonstrated reusable-component API pressure (boolean-prop proliferation, compound components, shared provider contracts) without abstracting ordinary one-off UI.
- `browser-testing-with-devtools` — verify rendered/runtime behavior in a real browser.
- `performance-optimization` — measure and improve frontend performance when evidence shows a bottleneck.
- `code-simplification` — keep component/state architecture lean.
- `hallmark` — substantial visual alternative/guard against generic visual clichés and fabricated content.
- `design-taste-frontend` — stronger visual judgment when implementation also needs art-direction sensitivity.
- `design-md-workflow` — read/maintain a durable project visual-identity contract when `DESIGN.md` or equivalent persistent design memory materially applies.
- `source-driven-development` — version-specific technical contracts; current framework/browser/API behavior matters.
- `security-and-hardening` — auth/session/input/trust-boundary work in frontend surfaces.
- `test-driven-development` — component/behavior tests when useful.
- `verification-before-completion` — fresh runtime/build/test evidence before completion claims.

If visual direction is material, inspect the `design` pack too. That does not require loading the whole design pack.

---

## design

**Use for:** public websites, landing pages, product/brand visual systems, visual direction, interaction design, motion, scrollytelling, Figma work, diagrams and spatial/3D experiences.

**Skills in this pack:**

- `motion-graphics-production` — authored rendered-video craft and production; not interactive web motion or a motion audit.
- `remotion-video-engineering` — selected Remotion project technical adapter; no automatic runtime setup.
- `advertising-video-production` — timed video-ad creative deliverables with source-backed proof and variants; not generic marketing strategy.
- `typography-and-layout` — choose and prove type roles, hierarchy, measure, spacing and fallback with real content; not a universal font ban or mandatory pairing.
- `brand-identity-design` — build a context-tested cross-media identity: marks, palette, type, imagery and application rules; not one-page CSS or brand strategy research.
- `design-system-engineering` — inventory and evolve actual tokens/components with consumers, drift, migration and ownership; not merely recording DESIGN.md.
- `data-visualization-design` — choose truthful chart encoding, scales, annotation, uncertainty and responsive alternatives; analytical claim validity remains a separate owner.
- `editorial-design` — compose sustained reading, decks and document layout, with optional printer-contract branch; file opening/editability belongs to artifact-production.
- `design-critique` — read-only brief-calibrated visual/copy second opinion with located evidence, concrete repairs and retests; primary alternative to Impeccable critique.
- `ux-heuristic-review` — walk actual tasks/states for understanding, control, prevention and recovery; expert findings are not participant research.
- `accessibility-design-review` — review names, keyboard/focus, forms, reflow and evidence limits; cognitive comprehension is an explicit JIT branch, not a conformance score.
- `motion-design-review` — critique animation purpose/frequency, interruption, reduced motion and measured vs suspected runtime cost; not an animation builder.

- `design-taste-frontend` — visual direction, hierarchy, composition and anti-generic frontend design judgment.
- `hallmark` — detect cliché AI aesthetics, fabricated proof and generic structural repetition.
- `design-inspiration-research` — research references, extract design DNA, synthesize rather than clone, and preserve provenance. Its references include the distilled premium/high-craft website production playbook.
- `design-md-workflow` — encode/read/verify durable project visual identity and tokens when persistent multi-session design memory is useful.
- `diagram-design` — route branded/general diagrams, code-grounded architecture maps, or simpler project-native diagrams without defaulting to AI-slop boxes.
- `impeccable` — structured visual critique and polish passes.
- `ui-ux-pro-max` — broader UI/UX pattern intelligence when the task benefits from it.
- `emil-design-eng` — interaction craft and design-engineering judgment.
- `design-trend-researcher` — investigate current visual/interaction patterns when freshness matters.
- `creative-web-experiences` — unconventional interactive web concepts when a standard page is not enough.
- `visual-storytelling-director` — narrative sequencing, visual story structure and presentation rhythm.
- `creative-tool-scout` — choose creative tools when unusual visual requirements make tooling selection material.
- `delight-and-whimsy` — deliberate moments of delight when they serve the experience rather than decorate everything.
- `figma-design-workflow` — Figma as a real source, collaboration or handoff surface.
- `scrollytelling-web` — narrative scroll experiences and section/state choreography.
- `scroll-world` — pre-rendered continuous camera worlds whose video timeline is scrubbed by scroll; use for fly-through/diorama journeys, not ordinary scrollytelling or realtime 3D.
- `gsap-scrolltrigger` — ScrollTrigger/timeline mechanics when GSAP is the right implementation tool.
- `gsap-performance` — keep advanced GSAP motion performant.
- `threejs-spatial-experiences` — interactive spatial/3D web experiences.
- `threejs-product-storytelling` — 3D specifically as a product/narrative device.
- `frontend-ui-engineering` — bridge visual direction into production-quality accessible UI.
- `browser-testing-with-devtools` — rendered desktop/mobile/browser evidence.
- `performance-optimization` — visual/motion work where runtime cost needs measurement.
- `reference-intelligence` — source-role/provenance judgment; use only when external/current references materially affect the design decision or provenance.
- `appllama-app-design-skill` — inspect only when the actual surface is native Expo/React Native product UI; it is not a default web-design dependency.

The design pack intentionally has many possibilities. **Do not subdivide them into basic/advanced tiers and do not infer that ambitious design work must load more of them.**

---

---

## design-review

**Use for:** read-only design criticism, comparing supplied alternatives and reviewing task flows, accessibility or motion. Reviews do not authorize remediation; expert observations are not participant tests or conformance proof.

**Skills in this pack:**

- `design-critique` — read-only brief-calibrated visual/copy second opinion with located evidence, concrete repairs and retests; primary alternative to Impeccable critique.
- `ux-heuristic-review` — walk actual tasks/states for understanding, control, prevention and recovery; expert findings are not participant research.
- `accessibility-design-review` — review names, keyboard/focus, forms, reflow and evidence limits; cognitive comprehension is an explicit JIT branch, not a conformance score.
- `motion-design-review` — critique animation purpose/frequency, interruption, reduced motion and measured vs suspected runtime cost; not an animation builder.
- `impeccable` — optional upstream critique/audit/polish workflow; choose a primary method rather than concatenating generic critics.
- `browser-testing-with-devtools` — obtain actual rendered/runtime evidence when available and permitted.
- `reference-intelligence` — establish applicable standards/reference authority when it matters.
- `verification-before-completion` — fresh evidence before declaring corrections verified.

## mobile

**Use for:** Expo/React Native, iOS/Android product UI, onboarding, paywalls, native navigation, sheets/modals, mobile state design and simulator-verified interaction work.

**Skills in this pack:**

- `mobile-runtime-engineering` — Expo/React Native hydration, navigation, offline mutation states and measured device performance; not visual inspiration or Flutter implementation.


- `appllama-usage` — research-tool mechanics only when the actual Appllama integration is selected and authorized.

- `appllama-app-design-skill` — study shipped mobile winners when useful, extract patterns rather than pixels, implement native-feeling Expo/React Native UI and verify whole flows in a simulator/emulator.
- `hallmark` — prevent generic AI styling and fabricated visual proof without importing the whole web-design pack.
- `source-driven-development` — version-specific technical contracts; use current Expo/React Native/platform documentation when API or platform behavior materially affects implementation.
- `mcp-tooling-fit` — inspect/enable the situational `mobile_design` MCP stack only when Appllama research would materially help and the user has/wants access.
- `verification-before-completion` — require fresh simulator/build/runtime evidence before claiming mobile UI behavior is complete.

Appllama is **optional, paid and credit-metered**. Its presence never makes `appllama-app-design-skill` global/core, and the pack itself never auto-enables the MCP or dictates a fixed skill count.

---

## backend

**Use for:** APIs, integrations, services, server-side architecture, runtime operations and backend trust boundaries.

**Skills in this pack:**

- `property-based-testing` — codecs, validators, numeric rules and state-transition invariants with generators.
- `security-analysis` — trace a suspected source-code vulnerability to its control and impact.
- `data-analysis-quality` — metric/query-output grain and reconciliation; not API implementation or database operation.


- `app-security-gate` — pre-release security evidence for APIs, sessions, data and integrations.

- `api-and-interface-design` — API/contracts/boundaries and compatibility decisions.
- `mcp-server-development` — design and implement MCP server/tool surfaces; not for merely selecting or calling an existing MCP.
- `observability-and-instrumentation` — logs, metrics, traces and diagnostics.
- `test-driven-development` — service/API behavior proof when useful.
- `code-simplification` — avoid accidental service/framework complexity.
- `verification-before-completion` — fresh runtime/test evidence.
- `security-and-hardening` — auth, secrets, PII, permissions and trust boundaries.
- `performance-optimization` — measured server/data-path optimization.
- `source-driven-development` — version-specific technical contracts; current protocols/framework/provider contracts.
- `architect-orchestrator` — structural or multi-service work.
- `debugging-and-error-recovery` — reproduce/localize backend failures.
- `deprecation-and-migration` — interface/service migration and compatibility work.
- `diagram-design` — communicate service topology/flows when a maintained visual is materially clearer than prose.

---

## data

**Use for:** databases, persistence, schemas, queries, migrations and data-heavy application work.

**Skills in this pack:**

- `data-analysis-quality` — determine whether metric/query/data claims can support the stated decision, with grain, cut-off, join cardinality and reconciliation.
- `property-based-testing` — generated-domain contracts for data transforms/codecs, not statistical modelling.
- `artifact-production` — deliver editable spreadsheet/report files with rendering and calculation checks.


- `supabase-postgres-best-practices` — PostgreSQL/Supabase-specific guidance **only when that stack is actually present**.
- `source-driven-development` — version-specific technical contracts; current database/platform docs and contracts.
- `test-driven-development` — prove query/migration/data behavior when appropriate.
- `observability-and-instrumentation` — data-path/runtime diagnostics.
- `security-and-hardening` — access controls, PII, row-level security and data trust boundaries.
- `performance-optimization` — measure query/storage/index performance before changing it.
- `doubt-driven-development` — adversarial review for destructive or structurally risky migrations.
- `architect-orchestrator` — multi-stage migrations and dependent systems.
- `deprecation-and-migration` — compatibility and rollout/rollback for schema/system migration.
- `verification-before-completion` — pre/post evidence for data changes.
- `diagram-design` — ER/schema/data-flow/lineage visuals when relationships are easier to verify spatially.

If no existing data skill fits the actual engine/domain, discover a better skill or use current canonical sources. Never force PostgreSQL guidance onto an unrelated database because it happens to be the nearest pack entry.

---

## product

**Use for:** product discovery, ambiguous feature decisions, requirements, specifications, prioritization and product/technical trade-offs.

**Skills in this pack:**

- `data-analysis-quality` — validate counts, rates and product evidence before a product decision.


- `adversarial-idea-review` — challenge business/product ideas before committing; not a substitute for code review.
- `spec-kit-workflow` — only when Spec Kit is present or explicitly requested; opt-in Spec Kit artifact/toolchain specialization; use one spec pipeline, not two.

- `interview-me` — unresolved material user/product decisions after discoverable facts have been inspected.
- `idea-refine` — explore and refine an early concept before committing to one shape.
- `spec-driven-development` — explicit requirements, scope and acceptance criteria.
- `planning-and-task-breakdown` — turn a decided outcome into executable units when useful.
- `documentation-and-adrs` — preserve durable product/architecture decisions.
- `doubt-driven-development` — challenge high-impact assumptions and alternatives.
- `reference-intelligence` — source-role/provenance judgment; market/product/comparable evidence materially affects the decision.
- `architect-orchestrator` — broad product + technical decomposition or multi-stage ownership.
- `marketing-and-growth` — product positioning/growth concerns are genuinely part of the decision.
- `diagram-design` — journey/flow/story-map visuals when they materially clarify a product decision.

---

## executive

**Use for:** company-level strategy, finance, people, legal, operations, marketing, product, board/governance and executive-priority decisions where specialist business judgment or cross-functional synthesis materially improves the result.

**Skills in this pack:**

- `data-analysis-quality` — audit business metric definitions and source reconciliation before consequential advice.
- `artifact-production` — usable board/report/deck files when a reusable artifact is requested.


- `executive-orchestration` — single accountable executive synthesis, model-owned specialist selection, bounded fan-out, conflict resolution, company context and authority boundaries.
- `executive-strategy` — positioning, market choice, moat, strategic options, partnerships, build/buy/partner and explicit non-goals.
- `executive-finance` — cash/runway, unit economics, scenarios, pricing economics, ROI and capital allocation.
- `executive-people` — role design, hiring, compensation, performance, retention and organization structure.
- `executive-legal` — contract/IP/employment/privacy/regulatory framing with jurisdiction-aware evidence and qualified-counsel escalation.
- `executive-operations` — bottlenecks, process, automation, vendor dependencies, capacity and operating metrics.
- `executive-marketing` — ICP, positioning, GTM, channel/funnel economics, brand/demand and retention-linked marketing decisions.
- `executive-product` — customer problem, PMF evidence, prioritization, sequencing, make/buy and product investment gates.
- `executive-board` — board/investor narrative, KPI/variance, governance, material risks and explicit asks.
- `executive-chief-of-staff` — triage, decision queue, ownership, blockers, follow-ups and operating cadence.
- `adversarial-idea-review` — kill/pivot/gate a company-level idea before commitment.
- `specialist-agent-routing` — bounded executive specialists only when independent expertise/context isolation/parallelism earns its coordination cost.
- `reference-intelligence` — source-role/provenance judgment; current markets, competitors, legal/regulatory/compensation evidence and provenance when the decision depends on them.
- `source-driven-development` — version-specific technical contracts; current authoritative sources for changing domain rules/contracts/platform behavior.
- `context-engineering` — large company/financial/customer/market evidence sets without dumping all context into every specialist.
- `doubt-driven-development` — adversarially challenge high-impact bets and fragile assumptions.
- `planning-and-task-breakdown` — turn a decided executive action into owned, sequenced work when useful.
- `documentation-and-adrs` — preserve durable decisions/assumptions/ownership when rediscovery would be costly.
- `verification-before-completion` — verify factual/action completion claims rather than accepting executive-sounding prose.
- `marketing-and-growth` — deeper campaign/CRO/content/SEO execution after an executive marketing decision when needed.

The `executive` profile is deliberately broad because profiles are installation/discovery surfaces. Installing or enabling it does **not** activate this pack or any executive skill body. A finance-only task may load only `executive-finance`; a cross-functional decision may load `executive-orchestration` plus whichever independent specialists can genuinely change the recommendation. Never preload the executive bench as a committee.

Executive skills decide at the business-function level. Pair them with engineering, product, marketing, release or other operational skills only when the decision proceeds into actual implementation.

---

## video

**Use for:** rendered motion graphics, logo/type/product films, video advertisements, footage assembly and selected rendering pipelines. Interactive UI motion remains in design; a strategy-only campaign remains in marketing.

**Skills in this pack:**

- `motion-graphics-production` — authored sequence from brief, key poses and scene craft through preview and final encode evidence.
- `advertising-video-production` — ad-specific hook, proof, storyboard, caption/audio, controlled variants and creative-test handoff; select as the ad production owner rather than stacking generic production by default.
- `remotion-video-engineering` — actual selected Remotion version, deterministic scene clocks, assets/props and render engineering; not a general video trigger.
- `creative-tool-scout` — unresolved route selection; its video branch compares HTML, native editors, offline 3D, interactive vectors and generated/hybrid media.
- `scroll-world` — specialized AI-rendered scene-chain pipeline for seamless camera journeys, frame-locked seams, encode and scroll delivery; paid providers remain separately authorized.
- `brand-identity-design` — identity development when required, not routine use of an approved logo.
- `typography-and-layout` — sustained type hierarchy/layout work when it needs its own design decision.
- `marketing-and-growth` — positioning, channel and learning decisions when genuinely in scope.
- `reference-intelligence` — current source/rights/provenance investigation when material.
- `verification-before-completion` — evidence for actual media/project delivery.

Profiles and packs deliver metadata only. References are conditional reads; selecting a route does not install tools, grant accounts, authorize billed generation or prove an encode.

---

## marketing

**Use for:** ICP/customer research, positioning, copy, campaigns, content strategy, email, CRO, launch planning and marketing operations.

**Skills in this pack:**

- `advertising-video-production` — actual timed video-ad production, proof and creative variants; no ads-account operations.

- `data-analysis-quality` — validate campaign/funnel/cohort claims before drawing conclusions.


- `marketing-and-growth` — main marketing operating skill. Its references contain the distilled large marketing-prompt corpus, SEO/growth loop and launch/content system.
- `shipping-and-launch` — launch/distribution readiness and operational launch checks.
- `humanizer` — preserve claims and brand voice while removing generic/robotic wording, structural AI tells and unsupported hype.
- `reference-intelligence` — source-role/provenance judgment; current competitor/market/launch evidence and source provenance.
- `source-driven-development` — version-specific technical contracts; current platform/API/policy behavior when it affects execution.
- `doubt-driven-development` — challenge high-impact strategy, claims or unsupported assumptions.
- `context-engineering` — large customer/competitor/content evidence sets.
- `documentation-and-adrs` — durable campaign/positioning decisions when worth preserving.

---

## seo

**Use for:** technical SEO, local SEO/GBP, search opportunity discovery, schema, search/content gaps, indexability, generative-AI search visibility and measurable organic-growth loops.

**Skills in this pack:**

- `marketing-and-growth` — the single SEO operating skill. Load `references/seo-growth-loop.md` for general/technical/search-loop work and `references/local-seo.md` for local/GBP work; load both only when the task spans both.
- `source-driven-development` — version-specific technical contracts; current search engine, structured-data, GBP and platform documentation.
- `context-engineering` — large GSC/site/query/competitor/GBP evidence sets.
- `reference-intelligence` — source-role/provenance judgment; current competitor/search evidence, authority classification and provenance.
- `performance-optimization` — Core Web Vitals/performance when measured evidence points there.
- `browser-testing-with-devtools` — rendered/indexability/runtime checks.
- `doubt-driven-development` — risky canonicals, migrations, programmatic SEO, location expansion or large-scale changes.
- `verification-before-completion` — evidence that technical/local changes actually landed and behave as expected.

AEO/GEO is not a parallel permanent skill by default. Treat it as a search surface inside the same SEO operating loop and use current platform-specific evidence when the behavior diverges.

---

## research

**Use for:** factual or technical research, reports, unfamiliar domains, source-heavy synthesis and current-domain investigations.

**Skills in this pack:**

- `data-analysis-quality` — trace structured-data claims to grain, formula, population and source.
- `artifact-production` — publishable local report/deck files when file structure/rendering matters.


- `source-driven-development` — version-specific technical contracts; establish authoritative/canonical source hierarchy and verify current contracts.
- `adversarial-idea-review` — attack a research/product direction before treating it as decided.
- `reference-intelligence` — source-role/provenance judgment; decide curated vs live sources, distinguish source roles and preserve provenance.
- `skillfinder-external-scout` — semantic external skill discovery when Agentit has no strong local owner or the user explicitly asks for the best skill across registries; never auto-installs candidates.
- `context-engineering` — manage large source/context sets without flooding the synthesis model.
- `verification-before-completion` — evidence-backed final claims.
- `doubt-driven-development` — adversarial source/assumption review.
- `architect-orchestrator` — parallel independent research branches and synthesis when that actually helps.
- `documentation-and-adrs` — preserve durable research decisions/knowledge when relevant to a project.
- `diagram-design` — visualize a researched system/process only when the visual is grounded in the collected evidence.

For current legal, tax, regulatory, medical, financial or other domain-specific work, Agentit does **not** need a permanent domain pack first. Use live authoritative domain sources whenever correctness depends on them.

---

## writing

**Use for:** documentation, technical prose, reports, explanations and externally visible written material.

**Skills in this pack:**

- `artifact-production` — reusable PDF/document/spreadsheet/deck production and verification; not ordinary chat prose.


- `stop-slop` — optional alternative editorial pass to humanizer; do not stack rigid style rules or remove factual qualifications.

- `humanizer` — primary editorial rewrite preserving meaning/voice; choose it or stop-slop, not both by default.
- `i-have-adhd` — reshape output for an ADHD reader: next action first, numbered steps, restated state, no tangents.
- `documentation-and-adrs` — durable technical/project documentation and decision records.
- `skill-authoring-and-evals` — create/edit agent-facing skills and instruction docs, tune triggers, progressive disclosure and selection/delivery evals.
- `source-driven-development` — version-specific technical contracts; factual/current source-grounded writing.
- `reference-intelligence` — source-role/provenance judgment; multi-source reports, source roles and provenance.
- `doubt-driven-development` — adversarial factual/argument review when stakes warrant it.
- `context-engineering` — large source sets or long documents.
- `verification-before-completion` — evidence before factual completion claims.

---

## release

**Use for:** CI/CD, deployments, migrations, launches, operational readiness and rollback planning.

**Skills in this pack:**

- `security-analysis` — triage confirmed/suspected source-code security findings; the app security gate still owns release disposition.


- `app-security-gate` — explicit PASS/BLOCKED security release gate backed by adversarial retests.

- `shipping-and-launch` — release readiness, launch checks and rollback thinking.
- `ci-cd-and-automation` — pipeline automation and quality gates.
- `verification-before-completion` — fresh release evidence.
- `verification-gauntlet` — only for multiple material evidence surfaces; multiple release verification surfaces when useful.
- `observability-and-instrumentation` — know whether a release is healthy after change.
- `deprecation-and-migration` — compatibility, retirement and migration plans.
- `security-and-hardening` — production/security boundaries.
- `doubt-driven-development` — high-risk rollout review.
- `architect-orchestrator` — multi-stage releases/migrations and dependency coordination.
- `git-workflow-and-versioning` — clean release/merge history and handoff.

---

## agency

**Use for:** client delivery where several domains, handoffs, documentation, review and shipping concerns interact.

`agency` is an **overlay/map**, not a mandatory parent pack. A client task can inspect `agency` plus `design`, `marketing`, `seo`, `engineering`, or any other domain that actually applies.

**Skills in this pack:**

- `artifact-production` — client-editable deliverables with honest visual/semantic verification.


- `git-workflow-and-versioning` — reviewable repository handoff.
- `anti-overengineering` — prevent client delivery from stalling in speculative architecture, test proliferation or repeated audit loops.
- `incremental-implementation` — bounded client delivery and staged implementation.
- `documentation-and-adrs` — durable client/project handoff context.
- `shipping-and-launch` — deployment/launch readiness.
- `architect-orchestrator` — multi-domain client programs when orchestration is useful.
- `specialist-agent-routing` — cleanly separated workers when specialization/parallelism pays off.
- `reference-intelligence` — source-role/provenance judgment; competitor, market, design or source-heavy client work.
- `marketing-and-growth` — marketing/growth delivery.
- `verification-before-completion` — prove client-facing changes before claiming completion.
- `design-md-workflow` — preserve a client's visual identity across repeated delivery when a durable design contract exists or is justified.
- `diagram-design` — client-facing system/process visuals when they materially improve handoff or decision quality.

---

## agent-runtime

**Use for:** explicit skill discovery, model/provider capability selection, resumable work and user-requested interaction adaptation. These are optional support procedures, not a mandatory task lifecycle.

**Skills in this pack:**

- `find-skills` — discover an absent durable capability only after checking existing project/library fit.
- `skillfinder-external-scout` — heavyweight semantic fallback across the external skill ecosystem; use only when local/catalog discovery is insufficient or explicitly requested.
- `local-model-routing` — assess an actually available local model endpoint; no automatic routing implementation is implied.
- `long-horizon-recovery` — resumable multi-session work with fresh selection and bounded private checkpoints.
- `i-have-adhd` — only on explicit user request; do not infer a diagnosis, impose persistence across new tasks, or override user/host output constraints.
- `mcp-tooling-fit` — choose tools from observed capability and authorization, not their mere presence.
- `skill-authoring-and-evals` — author or evaluate Agentit/agent skills when the task itself is maintaining the instruction system.

---

## Cross-cutting rules

- A skill may appear in multiple packs. Packs are **views over capabilities**, not ownership boundaries.
- Pack order does not imply priority.
- Skill order inside a pack does not imply priority or execution sequence.
- There are no hidden pack levels or recommended counts.
- The primary AI may inspect multiple packs and choose any justified subset.
- Profiles classify installation/discovery availability; packs classify semantic possibilities; neither one is active runtime context by itself.
- Every new session re-selects non-core skill bodies, references and tools from the actual current task.
- General Agentit procedures are provider/model-neutral; provider-specific details belong only where the real integration/source requires them.
- `reference-intelligence` is JIT, not global. Load it when source/provenance judgment is material.
- `mcp-tooling-fit` is JIT when external tool/MCP selection itself needs judgment.
- `security-and-hardening` is JIT when a real security/trust boundary exists, not for every code edit.
- `architect-orchestrator` / `specialist-agent-routing` are JIT when orchestration/delegation actually helps.
- `long-horizon-recovery` is JIT for long/resumable work.
- `design-md-workflow` is JIT even when `DESIGN.md` persists as durable project knowledge.
- `diagram-design` is JIT; a diagram tool is never required merely because a task is technical.
- The base Agentit protocol still requires appropriate verification and documentation-drift checks even when no dedicated verification/documentation skill body is selected.

## Missing pack or skill

If no pack covers the domain well:

1. do not force the nearest unrelated pack;
2. use current authoritative sources for the domain when needed;
3. inspect project-local skills;
4. use `find-skills` / approved skill discovery if a reusable specialist procedure would materially help;
5. create/adapt a new skill only when the procedure is durable and likely to recur.

> **Packs are a map, not a prison. The model decides the route and how much knowledge it needs.**

<!-- ECC-GENERATED BEGIN -->

The full ECC source lives once in `vendor/ecc`. See `docs/ECC_INTEGRATION.md` for canonical owners, native tool setup and the explicit alias decisions.

## ecc-web

**Use for:** Frontend frameworks, web interaction, accessible implementation and browser testing.

**Skills in this pack:**

- `accessibility` — Design, implement, and audit accessible UI to WCAG 2.2 Level AA across Web, iOS, and Android — semantic ARIA roles and labels, accessibility traits and hints, focus management, contrast, target size, and screen-reader support. Use when building or auditing UI for accessibility compliance, keyboard navigation, or screen-reader support.
- `angular-developer` — Generates Angular code and provides architectural guidance. Trigger when creating projects, components, or services, or for best practices on reactivity (signals, linkedSignal, resource), forms, dependency injection, routing, SSR, accessibility (ARIA), animations, styling (component styles, Tailwind CSS), testing, or CLI tooling.
- `browser-qa` — Run automated post-deploy UI verification with a browser automation MCP (claude-in-chrome, Playwright, or Puppeteer): console-error and Core Web Vitals smoke checks, form and auth-flow interaction tests, screenshot visual regression across three breakpoints, and axe-core accessibility audits ending in a SHIP / DO-NOT-SHIP verdict. Use when testing a deployed feature on staging or preview, before shipping frontend changes, reviewing a frontend PR, or checking responsive layout and accessibility.
- `click-path-audit` — Trace every user-facing button/touchpoint through its full state change sequence to find bugs where functions individually work but cancel each other out, produce wrong final state, or leave the UI in an inconsistent state. Use when: systematic debugging found no bugs but users report broken buttons, or after any major refactor touching shared state stores.
- `design-system` — Generate a design system from an existing codebase or audit one for visual consistency: extract tokens (colors, typography, spacing, shadows) into design-tokens.json and CSS custom properties with DESIGN.md rationale and an interactive HTML preview, score the UI across 10 dimensions, and flag AI-slop patterns. Use when starting a design system, auditing visual consistency before a redesign, or reviewing a PR that touches styling.
- `e2e-testing` — Playwright E2E testing patterns, Page Object Model, configuration, CI/CD integration, artifact management, and flaky test strategies. Use when writing Playwright tests, structuring page objects, or fixing flaky E2E runs in CI.
- `frontend-a11y` — Accessibility patterns for React and Next.js — semantic HTML, ARIA attributes, form labeling, keyboard navigation, focus management, and screen reader support. Use when building or reviewing forms, modals, dropdowns, tooltips, or tabs, fixing a11y lint or code-review findings, or wiring up keyboard navigation and focus management.
- `frontend-design-direction` — Set an ECC-specific frontend design direction for production UI work. Use when building or improving websites, dashboards, applications, components, landing pages, visual tools, or any web UI that needs stronger product-specific design judgment.
- `frontend-patterns` — Frontend development patterns for React, Next.js, state management, performance optimization, and UI best practices. Use when building or reviewing React or Next.js components, state, or render performance.
- `inherit-legacy-style` — Prevent AI style drift on legacy projects by scanning the codebase for implicit conventions, resolving conflicts with the operator one at a time, and writing an enforceable .ai-style-rules.md (Golden Files, naming rules, DONTs) plus an optional CLAUDE.md hook. Use when onboarding an AI agent onto a hand-written legacy codebase or extracting a project's unwritten coding rules.
- `make-interfaces-feel-better` — Apply concrete design-engineering details that make interfaces feel polished. Use when reviewing or improving UI spacing, typography, borders, shadows, motion, hit areas, icons, text wrapping, and interaction states.
- `motion-advanced` — Advanced motion patterns for React / Next.js — drag & drop, gestures, text animations, SVG path drawing, custom hooks, imperative sequences (useAnimate), loaders, and the full API decision tree. Requires motion-foundations. Use when building drag and drop, gestures, text or SVG animation, or imperative animation sequences in React or Next.js.
- `motion-foundations` — Motion tokens, spring presets, performance rules, device adaptation, accessibility enforcement, and SSR safety for React / Next.js using motion/react. Foundation layer — all other motion skills depend on this. Use when setting up motion tokens, spring presets, reduced-motion handling, or SSR-safe animation in React or Next.js.
- `motion-patterns` — Production-ready animation patterns for React / Next.js — button, modal, toast, stagger, page transitions, exit animations, scroll, and layout — built on motion-foundations tokens and springs. Use when animating a specific UI element in React or Next.js — button, modal, toast, stagger, page transition, or scroll.
- `nextjs-turbopack` — Next.js 16+ and Turbopack guidance — incremental Rust bundling, file-system caching, faster dev startup and HMR, Turbopack vs webpack tradeoffs, and the middleware.ts to proxy.ts filename change. Use when developing or debugging Next.js 16+ apps, diagnosing slow dev startup or hot reload, choosing between bundlers, or reviewing middleware/proxy file naming.
- `nuxt4-patterns` — Nuxt 4 app patterns for hydration safety, performance, route rules, lazy loading, and SSR-safe data fetching with useFetch and useAsyncData. Use when building or reviewing a Nuxt 4 app, or debugging hydration mismatches and SSR-safe data fetching.
- `react-patterns` — React 18/19 patterns including hooks discipline, server/client component boundaries, Suspense + error boundaries, form actions, data fetching, state management decision trees, and accessibility-first composition. Use when writing or reviewing React components.
- `react-performance` — React and Next.js performance optimization patterns adapted from Vercel Engineering's React Best Practices (https://github.com/vercel-labs/agent-skills). Organizes 70+ rules across 8 priority categories — waterfalls, bundle size, server-side, client fetching, re-render, rendering, JS micro-perf, advanced. Use when writing, reviewing, or refactoring React/Next.js code for performance.
- `react-testing` — React component testing with React Testing Library, Vitest/Jest, MSW for network mocking, accessibility assertions with axe, and the decision boundary between component tests and Playwright/Cypress end-to-end runs. Use when writing or fixing tests for React components, hooks, or pages.
- `ui-to-vue` — Use when the user has UI screenshots or design exports that need batch conversion into Vue 3 components, especially with Vant, Element Plus, or Ant Design Vue.
- `vite-patterns` — Vite build tool patterns including config, plugins, HMR, env variables, proxy setup, SSR, library mode, dependency pre-bundling, and build optimization. Activate when working with vite.config.ts, Vite plugins, or Vite-based projects.
- `vue-patterns` — Vue.js 3 Composition API patterns, component architecture, reactivity best practices, Pinia state management, Vue Router navigation, and Nuxt SSR patterns. Activates for Vue, Nuxt, Vite, or Pinia projects. Use when building or reviewing Vue 3, Nuxt, or Pinia code — Composition API, reactivity, or router navigation.

---

## ecc-languages

**Use for:** Language/framework engineering, architecture and ecosystem-specific verification.

**Skills in this pack:**

- `android-clean-architecture` — Clean Architecture patterns for Android and Kotlin Multiplatform projects — module structure, dependency rules, UseCases, Repositories, and data layer patterns. Use when structuring modules, layers, or data flow in an Android or KMP project.
- `backend-patterns` — Backend architecture patterns, API design, database optimization, and server-side best practices for Node.js, Express, and Next.js API routes. Use when building or reviewing Node.js, Express, or Next.js API routes and their data access.
- `bun-runtime` — Bun as runtime, package manager, bundler, and test runner. When to choose Bun vs Node, migration notes, and Vercel support.
- `compose-multiplatform-patterns` — Compose Multiplatform and Jetpack Compose patterns for KMP projects — state management, navigation, theming, performance, and platform-specific UI. Use when building Compose or Jetpack Compose UI, state, navigation, or theming in a KMP project.
- `cpp-coding-standards` — C++ coding standards based on the C++ Core Guidelines (isocpp.github.io). Use when writing, reviewing, or refactoring C++ code to enforce modern, safe, and idiomatic practices.
- `cpp-testing` — Use only when writing/updating/fixing C++ tests, configuring GoogleTest/CTest, diagnosing failing or flaky tests, or adding coverage/sanitizers.
- `csharp-testing` — C# and .NET testing patterns with xUnit, FluentAssertions, mocking, integration tests, and test organization best practices. Use when writing or reviewing xUnit tests, mocks, or integration tests in a C# / .NET project.
- `dart-flutter-patterns` — Production-ready Dart and Flutter patterns covering null safety, immutable state with Freezed, async composition, widget architecture, state management (BLoC, Riverpod, Provider), GoRouter navigation with auth guards, Dio networking, error handling, and testing. Use when writing or reviewing Dart and Flutter code — state, widgets, navigation, networking, or architecture.
- `django-celery` — Django + Celery async task patterns — configuration, task design, beat scheduling, retries, canvas workflows, monitoring, and testing. Use when adding background jobs, scheduled tasks, or async processing to a Django app.
- `django-patterns` — Django architecture patterns, REST API design with DRF, ORM best practices, caching, signals, middleware, and production-grade Django apps. Use when building or reviewing Django apps, DRF APIs, ORM queries, or caching.
- `django-security` — Django security best practices, authentication, authorization, CSRF protection, SQL injection prevention, XSS prevention, and secure deployment configurations. Use when reviewing Django authentication, authorization, input handling, or deployment settings.
- `django-tdd` — Django testing strategies with pytest-django, TDD methodology, factory_boy, mocking, coverage, and testing Django REST Framework APIs. Use when writing Django or DRF tests with pytest-django, or driving a Django feature test-first.
- `django-verification` — Run the full Django verification loop — environment check, mypy/ruff/black linting, migration safety, pytest with coverage targets, pip-audit and bandit security scans, settings and logging review, and diff review — producing a phased pass/fail report before release or PR. Use when preparing a Django pull request, validating migrations or coverage, or running pre-deploy readiness checks.
- `dotnet-patterns` — Idiomatic C# and .NET patterns, conventions, dependency injection, async/await, and best practices for building robust, maintainable .NET applications. Use when writing or reviewing C# / .NET code — DI, async, or general conventions.
- `fastapi-patterns` — FastAPI best practices covering project structure, Pydantic v2 schemas, dependency injection, async handlers, authentication, authorization, transactional service layers, and testing with httpx and pytest. Use when building or reviewing FastAPI apps — Pydantic schemas, dependencies, async handlers, auth, or tests.
- `flutter-dart-code-review` — Library-agnostic Flutter/Dart code review checklist covering widget best practices, state management patterns (BLoC, Riverpod, Provider, GetX, MobX, Signals), Dart idioms, performance, accessibility, security, and clean architecture. Use when reviewing Flutter or Dart code, whatever state management library the project uses.
- `foundation-models-on-device` — Apple FoundationModels framework for on-device LLM — text generation, guided generation with @Generable, tool calling, and snapshot streaming in iOS 26+. Use when adding on-device LLM features with Apple FoundationModels on iOS 26+.
- `fsharp-testing` — F# testing patterns with xUnit, FsUnit, Unquote, FsCheck property-based testing, integration tests, and test organization best practices. Use when writing F# tests with xUnit, FsUnit, Unquote, or FsCheck.
- `golang-patterns` — Idiomatic Go patterns, best practices, and conventions for building robust, efficient, and maintainable Go applications. Use when writing or reviewing Go code and idiomatic structure or conventions are in question.
- `golang-testing` — Go testing patterns including table-driven tests, subtests, benchmarks, fuzzing, and test coverage. Follows TDD methodology with idiomatic Go practices. Use when writing Go tests — table-driven cases, subtests, benchmarks, fuzzing, or coverage.
- `hexagonal-architecture` — Design, implement, and refactor Ports & Adapters systems with clear domain boundaries, dependency inversion, and testable use-case orchestration across TypeScript, Java, Kotlin, and Go services. Use when introducing or refactoring toward Ports and Adapters, or when domain logic has become entangled with I/O.
- `java-coding-standards` — Java coding standards for Spring Boot and Quarkus services: naming, immutability, Optional usage, streams, exceptions, generics, CDI, reactive patterns, and project layout. Automatically applies framework-specific conventions. Use when writing or reviewing Java in a Spring Boot or Quarkus service.
- `jpa-patterns` — JPA/Hibernate patterns for entity design, relationships, query optimization, transactions, auditing, indexing, pagination, and pooling in Spring Boot. Use when designing JPA entities or relationships, or when a Hibernate query, transaction, or N+1 problem needs fixing.
- `kotlin-coroutines-flows` — Kotlin Coroutines and Flow patterns for Android and KMP — structured concurrency, Flow operators, StateFlow, error handling, and testing. Use when writing coroutines or Flow code on Android or KMP, or debugging cancellation and concurrency.
- `kotlin-exposed-patterns` — JetBrains Exposed ORM patterns including DSL queries, DAO pattern, transactions, HikariCP connection pooling, Flyway migrations, and repository pattern. Use when working with the Exposed ORM — DSL or DAO queries, transactions, pooling, or migrations.
- `kotlin-ktor-patterns` — Ktor server patterns including routing DSL, plugins, authentication, Koin DI, kotlinx.serialization, WebSockets, and testApplication testing. Use when building a Ktor server — routing, plugins, auth, DI, serialization, or tests.
- `kotlin-patterns` — Idiomatic Kotlin patterns, best practices, and conventions for building robust, efficient, and maintainable Kotlin applications with coroutines, null safety, and DSL builders. Use when writing or reviewing Kotlin code and idiomatic structure or null safety is in question.
- `kotlin-testing` — Kotlin testing patterns with Kotest, MockK, coroutine testing, property-based testing, and Kover coverage. Follows TDD methodology with idiomatic Kotlin practices. Use when writing Kotlin tests with Kotest or MockK, or testing coroutines and checking coverage.
- `laravel-patterns` — Laravel architecture patterns, routing/controllers, Eloquent ORM, service layers, queues, events, caching, and API resources for production apps. Use when building or reviewing Laravel apps — controllers, Eloquent, service layers, queues, or API resources.
- `laravel-plugin-discovery` — Discover and evaluate Laravel packages via LaraPlugins.io MCP. Use when the user wants to find plugins, check package health, or assess Laravel/PHP compatibility.
- `laravel-security` — Laravel security best practices — authentication, authorization, Eloquent safety, CSRF, XSS prevention, API security, and secure deployment configurations. Use when reviewing Laravel auth, Eloquent safety, CSRF, XSS, API security, or deployment configuration.
- `laravel-tdd` — Laravel testing strategies with PHPUnit, Pest, model factories, HTTP tests, Sanctum authentication testing, mocking, and coverage. Use when writing Laravel tests with PHPUnit or Pest, or driving a Laravel feature test-first.
- `laravel-verification` — Verification loop for Laravel projects: env checks, linting, static analysis, tests with coverage, security scans, and deployment readiness. Use when verifying a Laravel project before merge or deploy — lint, static analysis, tests, coverage, security.
- `liquid-glass-design` — iOS 26 Liquid Glass design system — dynamic glass material with blur, reflection, and interactive morphing for SwiftUI, UIKit, and WidgetKit. Use when building iOS 26 Liquid Glass UI in SwiftUI, UIKit, or WidgetKit.
- `nestjs-patterns` — NestJS architecture patterns for modules, controllers, providers, DTO validation, guards, interceptors, config, and production-grade TypeScript backends. Use when building or reviewing a NestJS backend — modules, providers, DTO validation, guards, or interceptors.
- `perl-patterns` — Modern Perl 5.36+ idioms, best practices, and conventions for building robust, maintainable Perl applications. Use when writing or reviewing modern Perl 5.36+ code.
- `perl-security` — Comprehensive Perl security covering taint mode, input validation, safe process execution, DBI parameterized queries, web security (XSS/SQLi/CSRF), and perlcritic security policies. Use when reviewing Perl input handling, process execution, DBI queries, or web-facing code.
- `perl-testing` — Perl testing patterns using Test2::V0, Test::More, prove runner, mocking, coverage with Devel::Cover, and TDD methodology. Use when writing Perl tests with Test2::V0 or Test::More, or measuring coverage.
- `python-patterns` — Pythonic idioms, PEP 8 standards, type hints, and best practices for building robust, efficient, and maintainable Python applications. Use when writing or reviewing Python code and idiomatic structure, typing, or PEP 8 is in question.
- `python-testing` — Python testing strategies using pytest, TDD methodology, fixtures, mocking, parametrization, and coverage requirements. Use when writing pytest tests — fixtures, mocks, parametrization, or coverage.
- `quarkus-patterns` — Quarkus 3.x LTS architecture patterns with Camel for messaging, RESTful API design, CDI services, data access with Panache, and async processing. Use for Java Quarkus backend work with event-driven architectures. Use when building or reviewing a Quarkus service, especially with Camel messaging or Panache data access.
- `quarkus-security` — Quarkus security implementation patterns: JWT and OIDC authentication, @RolesAllowed RBAC and SecurityIdentity checks, Bean Validation and custom validators, parameterized Panache queries, BCrypt password hashing, CORS and security headers, rate limiting, audit logging, Vault or environment-variable secrets, and dependency CVE scanning. Use when adding authentication or authorization, validating input, managing secrets, or hardening a Quarkus application.
- `quarkus-tdd` — Test-driven development for Quarkus 3.x LTS using JUnit 5, Mockito, REST Assured, Camel testing, and JaCoCo. Use when adding features, fixing bugs, or refactoring event-driven services.
- `quarkus-verification` — Verification loop for Quarkus projects: build, static analysis (Checkstyle, PMD, SpotBugs), tests with JaCoCo coverage, OWASP dependency and container security scans, GraalVM native compilation, health checks, and config validation. Use when verifying a Quarkus service before a PR, after major refactoring or dependency upgrades, or pre-deploy.
- `rails-patterns` — Ruby on Rails framework patterns for Rails 7.1+ and 8.x apps. Covers the directory contract, skinny controllers with service objects, form objects, query objects, idiomatic ActiveRecord, background jobs, ViewComponent, Hotwire, and the Rails 8 Solid stack. Use when building or reviewing Rails apps, controllers, models, services, jobs, or views.
- `react-native-patterns` — React Native and Expo app patterns — Expo Router navigation, state separation (server/client/route/form), TanStack Query data fetching with Zod, performant lists, NativeWind/StyleSheet styling, native APIs, and secure storage. Use when building or editing React Native / Expo screens, components, navigation, or data layers.
- `rust-patterns` — Idiomatic Rust patterns, ownership, error handling, traits, concurrency, and best practices for building safe, performant applications. Use when writing or reviewing Rust code and ownership, error handling, traits, or concurrency is in question.
- `rust-testing` — Rust testing patterns including unit tests, integration tests, async testing, property-based testing, mocking, and coverage. Follows TDD methodology. Use when writing Rust tests — unit, integration, async, property-based, or coverage.
- `springboot-patterns` — Spring Boot architecture patterns, REST API design, layered services, data access, caching, async processing, and logging. Use for Java Spring Boot backend work. Use when building or reviewing a Spring Boot backend — REST layer, services, data access, caching, or async work.
- `springboot-security` — Spring Security best practices for authn/authz, validation, CSRF, secrets, headers, rate limiting, and dependency security in Java Spring Boot services. Use when reviewing Spring Security authn/authz, validation, CSRF, secrets, headers, or rate limiting.
- `springboot-tdd` — Test-driven development for Spring Boot using JUnit 5, Mockito, MockMvc, Testcontainers, and JaCoCo. Use when adding features, fixing bugs, or refactoring.
- `springboot-verification` — Run the full Spring Boot verification loop — Maven or Gradle build, SpotBugs, PMD, and Checkstyle static analysis, unit and Testcontainers integration tests with JaCoCo coverage, OWASP dependency and secret scans, and diff review — producing a pass/fail readiness report. Use when preparing a Spring Boot pull request, validating coverage thresholds, or running pre-deploy verification.
- `swift-actor-persistence` — Thread-safe data persistence in Swift using actors — in-memory cache with file-backed storage, eliminating data races by design. Use when persisting data in Swift and a data race or thread-safety problem needs designing out.
- `swift-concurrency-6-2` — Swift 6.2 Approachable Concurrency — single-threaded by default, @concurrent for explicit background offloading, isolated conformances for main actor types. Use when adopting Swift 6.2 concurrency — offloading with @concurrent or resolving main-actor isolation.
- `swift-protocol-di-testing` — Protocol-based dependency injection for testable Swift code — mock file system, network, and external APIs using focused protocols and Swift Testing. Use when Swift code needs testing and file system, network, or external APIs must be mocked.
- `swiftui-patterns` — SwiftUI architecture patterns, state management with @Observable, view composition, navigation, performance optimization, and modern iOS/macOS UI best practices. Use when building or reviewing SwiftUI views, @Observable state, navigation, or render performance.
- `tinystruct-patterns` — Expert guidance for developing with the tinystruct Java framework. Use when working on the tinystruct codebase or any project built on tinystruct — including creating Application classes, @Action-mapped routes, unit tests, ActionRegistry, HTTP/CLI dual-mode handling, the built-in HTTP server, the event system, JSON with Builder/Builders, database persistence with AbstractData, POJO generation, Server-Sent Events (SSE), file uploads, and outbound HTTP networking.
- `windows-desktop-e2e` — E2E testing for Windows native desktop apps (WPF, WinForms, Win32/MFC, Qt) using pywinauto and Windows UI Automation. Use when writing E2E tests for a Windows native desktop app with pywinauto or UI Automation.

---

## ecc-development

**Use for:** Repo execution, API contracts, measured optimization, tests and delivery.

**Skills in this pack:**

- `ai-first-engineering` — Engineering operating model for teams where AI agents generate a large share of implementation output. Use when setting team process, review gates, or ownership rules for a codebase largely written by agents.
- `ai-regression-testing` — Regression testing strategies for AI-assisted development. Sandbox-mode API testing without database dependencies, automated bug-check workflows, and patterns to catch AI blind spots where the same model writes and reviews code. Use when adding regression coverage to AI-assisted code, or when the same model both wrote and reviewed a change.
- `api-connector-builder` — Build a new API connector or provider by matching the target repo's existing integration pattern exactly. Use when adding one more integration without inventing a second architecture.
- `api-design` — REST API design patterns including resource naming, status codes, pagination, filtering, error responses, versioning, and rate limiting for production APIs. Use when designing or reviewing REST endpoints, resource names, status codes, pagination, or versioning.
- `architecture-decision-records` — Capture architectural decisions as numbered ADR markdown files in docs/adr/ with context, alternatives considered, consequences, and an index README. Use when the user says 'record this decision' or 'ADR this', chooses between frameworks or databases, discusses trade-offs, or asks why the codebase is shaped this way.
- `benchmark` — Measure performance baselines and detect regressions across browser Core Web Vitals (LCP, INP, CLS, page weight), API endpoint latency percentiles, and build/test feedback times, with before/after comparison stored in git-tracked .ecc/benchmarks JSON. Use when checking page speed, responding to 'it feels slow' reports, verifying launch performance targets, or comparing stack alternatives.
- `benchmark-optimization-loop` — Convert 'make it faster' requests into a bounded measured optimization loop — baseline first, generate one-hypothesis variants, benchmark each against a correctness gate, and promote the fastest safe variant with reproducible commands. Use when asked to speed something up, try many variants, run recursive optimization, benchmark latency/throughput/cost, or pick the best implementation by repeated measured tests.
- `blueprint` — Turn a one-line objective into a step-by-step construction plan for multi-session, multi-agent engineering projects: one-PR-sized steps with self-contained context briefs, dependency graph with parallel-step detection, adversarial review gate, and plan mutation protocol. Use when planning a large feature, refactor, or roadmap that spans multiple PRs or sessions; not for single-PR tasks or when the user says "just do it".
- `code-tour` — Create CodeTour `.tour` files — persona-targeted, step-by-step walkthroughs with real file and line anchors. Use for onboarding tours, architecture walkthroughs, PR tours, RCA tours, and structured "explain how this works" requests. Use when the user asks for a code tour, onboarding walkthrough, PR tour, or an explanation of how a subsystem works.
- `codebase-onboarding` — Analyze an unfamiliar codebase and generate a structured onboarding guide with architecture map, key entry points, conventions, and a starter CLAUDE.md. Use when joining a new project or setting up Claude Code for the first time in a repo.
- `codehealth-mcp` — Real-time structural Code Health via CodeScene MCP — review before edits, verify score deltas after changes, gate commits and PRs. Use when reviewing code quality, refactoring, checking if AI changes degraded a file, or before commit/PR.
- `coding-standards` — Baseline cross-project coding conventions for naming, readability, immutability, and code-quality review. Use detailed frontend or backend skills for framework-specific patterns. Use when reviewing code quality or naming with no framework-specific skill that applies.
- `content-hash-cache-pattern` — Cache expensive file processing results using SHA-256 content hashes — path-independent, auto-invalidating, with service layer separation. Use when repeated file processing is slow and results should be cached and invalidated by content rather than path.
- `contract-first` — Coordinate frontend/backend or service-to-service work through one authoritative machine-checkable contract (OpenAPI, AsyncAPI, Protocol Buffers, or JSON Schema), with generated consumer types and contract-verified integration. Use when parallel consumer and provider work must evolve an API or event schema without field drift, mock/production shape mismatch, or one side silently redefining the interface.
- `cost-aware-llm-pipeline` — Cost optimization patterns for LLM API usage — model routing by task complexity, budget tracking, retry logic, and prompt caching. Use when LLM spend needs to come down, or when routing tasks across model tiers and budgets.
- `delivery-gate` — Stop hook that blocks Claude from finishing until quality checks pass. Detects rationalization patterns (surface text heuristics), stale learning logs (filesystem mtime), and low disk space. Complements self-audit by mechanically enforcing learning capture habits. Use when Claude should be mechanically blocked from declaring work finished before quality checks and learning capture actually pass.
- `deployment-patterns` — Deployment workflows, CI/CD pipeline patterns, Docker containerization, health checks, rollback strategies, and production readiness checklists for web applications. Use when setting up CI/CD, containerizing an app, or checking production readiness before a release.
- `documentation-lookup` — Use up-to-date library and framework docs via Context7 MCP instead of training data. Activates for setup questions, API references, code examples, or when the user names a framework (e.g. React, Next.js, Prisma).
- `error-handling` — Patterns for robust error handling across TypeScript, Python, and Go. Covers typed errors, error boundaries, retries, circuit breakers, and user-facing error messages. Use when designing error types, retries, circuit breakers, or user-facing failure messages in TypeScript, Python, or Go.
- `eval-harness` — Eval-driven development (EDD) framework for AI coding sessions — define capability and regression evals before coding, grade with code-based, model-based, rule, or human graders, and track pass@k and pass^k reliability. Use when defining pass/fail criteria for agent tasks, measuring agent reliability, building regression suites for prompt or agent changes, or benchmarking across model versions.
- `generating-python-installer` — Commercial-grade Python installer expert for Windows: Nuitka extreme compilation, dist slimming, DLL footprint analysis, and Inno Setup packaging to ship the smallest, fastest installers. Use when a Python app must ship as a minimal, fast-starting Windows installer; not for basic script-to-exe conversion. 中文触发：Nuitka 极限优化、Python 商业打包、极限编译 Python、dist 瘦身、DLL 分析、最小安装包、最快启动、商业级打包风格
- `github-ops` — GitHub repository operations, automation, and management. Issue triage, PR management, CI/CD operations, release management, and security monitoring using the gh CLI. Use when the user wants to manage GitHub issues, PRs, CI status, releases, contributors, stale items, or any GitHub operational task beyond simple git commands.
- `i18n-sync` — Translate and synchronize application JSON locale files using source-key usage, project terminology, and focused validation. Use when adding keys or languages, updating source copy, or reviewing missing and stale translations.
- `intent-driven-development` — Turn ambiguous or high-impact product and engineering changes into scoped, verifiable acceptance criteria before or alongside implementation. Use when a user asks to clarify a feature, define acceptance criteria, de-risk a security/data/migration/integration change, prepare implementation requirements for another agent, or make a complex request testable. Do not trigger for trivial edits, straightforward fixes, active debugging, code review, or implementation requests whose acceptance conditions are already clear unless the user explicitly invokes this skill.
- `living-docs-governance` — Keep a long-lived project's documentation from rotting by assigning existing project docs clear constitution, map, status, and history roles, then wiring the active agent harness to those canonical sources. Use in the maintain phase when docs drift from code, agents lose context between sessions, or intentional removals keep being recreated. Prefer adopting the repository's current docs structure over creating new root files. 中文触发：文档治理、活文档、项目状态追踪、防文档漂移、项目地图、健康仪表盘、删除区、长期项目治理
- `loop-design-check` — Design a goal-oriented agent loop or review one for failure modes: spinning, Goodhart-gaming the verifier, or running a wrong answer to completion. Covers machine-decidable goals, loop types, plan/build/judge skeletons, and runaway prevention; mechanism wiring lives in autonomous-loops. Use when designing, writing, or checking an agent loop. 中文触发：写 loop、设计 loop、做一个 loop、检查 loop 对不对、loop 体检、loop 会不会跑飞、可判定目标、五个崩法、plan build judge。
- `mcp-server-patterns` — Build MCP servers with Node/TypeScript SDK — tools, resources, prompts, Zod validation, stdio vs Streamable HTTP. Use Context7 or official MCP docs for latest API. Use when building or debugging an MCP server — tools, resources, prompts, validation, or transport choice.
- `opensource-pipeline` — Open-source pipeline: fork, sanitize, and package private projects for safe public release. Chains 3 agents (forker, sanitizer, packager). Triggers: '/opensource', 'open source this', 'make this public', 'prepare for open source'. Use when a private project must be forked, stripped of secrets, and packaged for public release.
- `plan-canvas` — Open plans and HTML artifacts in a local browser canvas where the human annotates elements, chats, and approves or requests changes without leaving the page. Use when presenting a plan for review, or when feedback like "move this, change that" is easier pointed at than typed.
- `plankton-code-quality` — Write-time code quality enforcement using Plankton — auto-formatting, linting, and Claude-powered fixes on every file edit via hooks. Use when setting up write-time formatting, linting, or auto-fix hooks on file edits.
- `product-capability` — Translate PRD intent, roadmap asks, or product discussions into an implementation-ready capability plan that exposes constraints, invariants, interfaces, and unresolved decisions before multi-service work starts. Use when the user needs an ECC-native PRD-to-SRS lane instead of vague planning prose.
- `product-lens` — Validate the why before building through four product diagnostics — a YC-style product diagnostic that produces PRODUCT-BRIEF.md with a go/no-go recommendation, a founder review scoring product-market-fit signals, a user journey audit measuring time-to-value, and ICE feature prioritization. Use when pressure-testing product direction, choosing between features, sanity-checking a launch, or converting a vague idea into a product brief.
- `production-audit` — Local-evidence production readiness audit for shipped apps, pre-launch reviews, post-merge checks, and "what breaks in prod?" questions without sending repo data to an external audit service. Use when auditing production readiness before launch, after a merge, or when asked what breaks in prod.
- `prompt-optimizer` — Analyze draft prompts, detect intent and missing context, match ECC commands, skills, and agents, and output a ready-to-paste optimized prompt with diagnosis and rationale — advisory only, never executes the task. Use when the user says 'optimize prompt', 'improve my prompt', 'rewrite this prompt', 'help me prompt', 优化prompt, 改进prompt, 怎么写prompt, or 帮我优化这个指令; not for requests to optimize code or performance.
- `regex-vs-llm-structured-text` — Decision framework for parsing structured text (quizzes, forms, invoices, receipts, tables) with a hybrid regex-first pipeline — regex extraction handles 95%+ cheaply, a confidence scorer flags low-confidence items, and an LLM validator fixes only the edge cases. Use when choosing between regex and LLM for text extraction, building a cheap document parser, or optimizing extraction cost and accuracy.
- `repo-scan` — Bootstrap pointer that installs the external repo-scan skill from a pinned, reviewable commit. Use when repo-scan must be installed before running its cross-stack source-code asset audit; this ECC pointer does not perform the audit itself.
- `search-first` — Research-before-coding workflow: search npm/PyPI, MCP servers, skills, and GitHub for existing tools before writing custom code, then adopt, extend, or build. Launches the researcher agent for non-trivial needs. Use when starting a feature, adding a dependency or integration, or about to write a utility that may already exist.
- `terminal-opener` — Open an executable and its argument array in a visible terminal window through a reusable, shell-free launch plan with dry-run, JSON, capability detection, detached fallback, and standalone recovery modes. Use when Codex needs to open an interactive CLI, SSH session, local development process, sandbox, or other argv-based command in a new host terminal; diagnose whether a supported terminal is available; or provide an actionable plan when the requested terminal is unsupported.
- `terminal-ops` — Evidence-first repo execution workflow for ECC. Use when the user wants a command run, a repo checked, a CI failure debugged, or a narrow fix pushed with exact proof of what was executed and verified.

---

## ecc-agent-systems

**Use for:** Agent tools, orchestration, memory, learning, context and host adapters; explicit selection only.

**Skills in this pack:**

- `agent-architecture-audit` — Full-stack diagnostic for agent and LLM applications. Audits the 12-layer agent stack for wrapper regression, memory pollution, tool discipline failures, hidden repair loops, and rendering corruption. Produces severity-ranked findings with code-first fixes. Essential for developers building agent applications, autonomous loops, or any LLM-powered feature. Use when an agent or LLM feature misbehaves and the failing layer is unknown, or before shipping an agent stack.
- `agent-eval` — Head-to-head comparison of coding agents (Claude Code, Aider, Codex, etc.) on custom tasks with pass rate, cost, time, and consistency metrics. Use when choosing between coding agents, or when a change to an agent setup needs measured pass rate, cost, and time rather than an impression.
- `agent-harness-construction` — Design and optimize AI agent action spaces, tool definitions, and observation formatting for higher completion rates. Use when defining or revising an agent's tool set, action space, or observation format.
- `agent-introspection-debugging` — Structured self-debugging workflow for AI agent failures using capture, diagnosis, contained recovery, and introspection reports. Use when an agent run fails and you need a reproducible diagnosis instead of a retry.
- `agent-self-evaluation` — Use after completing any non-trivial task. The agent self-rates its output on 5 axes — accuracy, completeness, clarity, actionability, conciseness — with concrete evidence per criterion. Produces a structured 1-5 scorecard with specific improvement suggestions.
- `agentic-engineering` — Operate as an agentic engineer using eval-first execution, decomposition, and cost-aware model routing. Use when planning or executing engineering work that agents will carry out end to end.
- `agentic-os` — Build persistent multi-agent operating systems on Claude Code. Covers kernel architecture, specialist agents, slash commands, file-based memory, scheduled automation, and state management without external databases. Use when building a persistent multi-agent system on Claude Code with its own memory, commands, and scheduling.
- `autonomous-agent-harness` — Transform Claude Code into a fully autonomous agent system with persistent memory, scheduled operations, computer use, and task queuing. Replaces standalone agent frameworks (Hermes, AutoGPT) by leveraging Claude Code's native crons, dispatch, MCP tools, and memory. Use when the user wants continuous autonomous operation, scheduled tasks, or a self-directing agent loop.
- `claude-devfleet` — Orchestrate multi-agent coding tasks via Claude DevFleet — plan projects, dispatch parallel agents in isolated worktrees, monitor progress, and read structured reports. Use when dispatching parallel coding agents across isolated worktrees and tracking their reports.
- `config-gc` — Garbage collection for your Claude Code configuration. Periodically scans ~/.claude (skills, memory, hooks, permissions, MCP servers, caches) for redundant, stale, orphaned, or low-value items, then walks the user through a confirm-each-deletion cleanup. Use when the user says "clean up my config", "config GC", "too many skills", "audit my setup", "my .claude is bloated", or asks for a periodic config review.
- `configure-ecc` — Run the conversational ECC setup wizard inside the current harness: inventory the install, collect scope (user/project/local) and hook mode (off/minimal/standard/strict) in Claude Code, use Codex's native plugin lifecycle, or install the project surface under ./.kimi-code, then preview, apply, and verify. Use when installing, updating, reconfiguring, or repairing an ECC installation, changing hook profiles, or moving ECC between install scopes.
- `connections-optimizer` — Reorganize the user's X and LinkedIn network with review-first pruning, add/follow recommendations, and channel-specific warm outreach drafted in the user's real voice. Use when the user wants to clean up following lists, grow toward current priorities, or rebalance a social graph around higher-signal relationships.
- `context-budget` — Audits Claude Code context window consumption across agents, skills, MCP servers, and rules. Identifies bloat, redundant components, and produces prioritized token-savings recommendations. Use when the context window is filling up too fast and the agents, skills, MCP servers, or rules consuming it need to be identified.
- `continuous-agent-loop` — Patterns for continuous autonomous agent loops with quality gates, evals, and recovery controls. Use when running an agent loop that must self-check, gate on evals, and recover from failures.
- `continuous-learning-v2` — Instinct-based learning system that observes sessions via hooks, creates atomic instincts with confidence scoring, and evolves them into skills/commands/agents. v2.1 adds project-scoped instincts to prevent cross-project contamination. Use when capturing lessons from a session, managing instincts, or promoting them into skills, commands, or agents.
- `cost-tracking` — Track and report Claude Code token usage, spending, and budgets from the local ECC cost-tracker metrics log. Use when the user asks about costs, spending, usage, tokens, budgets, or cost breakdowns by model, session, or date.
- `council` — Convene a four-voice council for ambiguous decisions, tradeoffs, and go/no-go calls. Use when multiple valid paths exist and you need structured disagreement before choosing.
- `council-multi-model` — Add one optional external Codex critique after the existing council has produced a decision draft. Use when an ambiguous, high-consequence decision would benefit from a separate model invocation's attempt to break the synthesis. Requires explicit consent before sending the compact draft and disagreement to OpenAI, labels same-provider reviews honestly, and marks the review absent when the adapter is unavailable.
- `dev-team` — Simulate a collaborative dev team session where multiple role-based personas (PM, Architect, Developer, QA) respond to the same problem together in one session. Use when designing a feature, reviewing a proposal, or onboarding a new initiative and you want multi-role perspective without switching agents manually.
- `dmux-workflows` — Multi-agent orchestration using dmux (tmux pane manager for AI agents). Patterns for parallel agent workflows across Claude Code, Codex, OpenCode, and other harnesses. Use when running multiple agent sessions in parallel or coordinating multi-agent development workflows.
- `dynamic-workflow-mode` — Design task-local harnesses, eval gates, and reusable skill extraction for Claude dynamic workflow mode and other adaptive agent harnesses. Use when building a task-local harness, adding eval gates, or extracting a reusable skill from ad-hoc work.
- `ecc-guide` — Answer questions about ECC by reading the live repo surface — agents, skills, commands, hooks, rules, install profiles, and docs — instead of memory. Use when the user asks what ECC includes, how to install or reset it, which skill or command fits a task, or how project onboarding works.
- `ecc-recipes` — Map a described workflow to the right ECC command group with run-order and stop condition, or browse all command-group recipe families read live from the commands directory. Advisory only — never executes. Use when asked which commands run a workflow, the command sequence for a task, or to list ECC pipelines; not for executing the task (route to the command itself), single-command docs (use ecc-guide), or prompt rewrites (use prompt-optimizer).
- `ecc-tools-cost-audit` — Evidence-first ECC Tools burn and billing audit workflow. Use when investigating runaway PR creation, quota bypass, premium-model leakage, duplicate jobs, or GitHub App cost spikes in the ECC Tools repo.
- `enterprise-agent-ops` — Operational controls for long-lived or cloud-hosted agent systems — runtime lifecycle (start, pause, stop, restart), observability (logs, metrics, traces), least-privilege safety scopes and kill switches, and rollout/rollback change management with audit logs and success/cost metrics. Use when running production agent fleets on PM2, systemd, or containers that need monitoring, incident response, or deployment gates.
- `gan-style-harness` — GAN-inspired Generator-Evaluator agent harness for building high-quality applications autonomously. Based on Anthropic's March 2026 harness design paper. Use when a feature should be built autonomously through generator and evaluator iteration until it clears a quality bar.
- `growth-log` — Write growth log entries that extract reusable patterns from completed work — root cause, transferable rule, and a recognizable signal — instead of diary-style event narration, with a 4-8 sentence template and merge-duplicates discipline. Use when capturing what was learned after a complex task, debugging session, failure, or rollback, when reviewing progress over a period, or when a delivery gate asks what was learned.
- `hermes-imports` — Convert local Hermes operator workflows into sanitized ECC skills and release-pack artifacts. Use when preparing a Hermes workflow for public ECC reuse without leaking private workspace state, credentials, or local-only paths.
- `hookify-rules` — Create and configure hookify rules — markdown files with YAML frontmatter that match bash, file, prompt, or stop events by regex or conditions and show warn/block messages to the agent. Use when creating a hookify rule, writing hook rule syntax, configuring hookify, or adding pattern guardrails such as blocking dangerous commands, .env edits, or debug code.
- `iterative-retrieval` — Pattern for progressively refining context retrieval to solve the subagent context problem. Use when a subagent lacks the context it needs and retrieval must be refined across passes.
- `knowledge-ops` — Knowledge base management, ingestion, sync, and retrieval across multiple storage layers (local files, MCP memory, vector stores, Git repos). Use when the user wants to save, organize, sync, deduplicate, or search across their knowledge systems.
- `nanoclaw-repl` — Operate and extend NanoClaw, ECC's zero-dependency session-aware REPL, with persistent markdown-backed sessions and slash commands for model switching, skill loading, session branching, cross-session search, history compaction, and export. Use when running or extending scripts/claw.js, or when resuming, branching, compacting, searching, or exporting a NanoClaw session.
- `nasiko-control-plane` — Manage the experimental Nasiko CLI lifecycle through ECC — read-only status checks, consent-gated install of the pinned qualified version with dry-run preview, and ownership-checked uninstall, under explicit telemetry and secrets boundaries. Use when the user asks to install, inspect, or remove the Nasiko CLI or check whether it is present.
- `openclaw-persona-forge` — 为 OpenClaw AI Agent 锻造完整的龙虾灵魂方案。根据用户偏好或随机抽卡， 输出身份定位、灵魂描述(SOUL.md)、角色化底线规则、名字和头像生图提示词。 如当前环境提供已审核的生图 skill，可自动生成统一风格头像图片。 当用户需要创建、设计或定制 OpenClaw 龙虾灵魂时使用。 不适用于：微调已有 SOUL.md、非 OpenClaw 平台的角色设计、纯工具型无性格 Agent。 触发词：龙虾灵魂、虾魂、OpenClaw 灵魂、养虾灵魂、龙虾角色、龙虾定位、 龙虾剧本杀角色、龙虾游戏角色、龙虾 NPC、龙虾性格、龙虾背景故事、 lobster soul、lobster character、抽卡、随机龙虾、龙虾 SOUL、gacha。 Use when creating, designing, or customizing an OpenClaw lobster persona — identity, SOUL.md, name, or avatar prompt.
- `operator-approval-loop` — Operator approval contract with internal filing notices for agent-drafted outbound messages, hashed drafts, epoch-keyed decisions, durable delivery claims and receipts, and a pre-draft baseline gate. Use when an agent drafts messages to external counterparties and a human operator must approve, reject, or steer each send before it leaves.
- `orch-add-feature` — Orchestrate building a brand-new feature end to end — research, plan, TDD implementation, review, and gated commit — by delegating each phase to the matching ECC agent. Use when adding a capability that does not exist yet.
- `orch-build-mvp` — Orchestrate bootstrapping a working MVP from a design or spec document — ingest the SDD/PRD, plan thin vertical slices, scaffold the first end-to-end slice, then drive a generator-evaluator build loop with review and gated feat commits. Use when a design or spec document must become a running MVP through planned vertical slices.
- `orch-change-feature` — Orchestrate altering an existing, working feature to new desired behavior — update its tests to the new spec, change the implementation to match, review, and gated commit. Use when behavior is not broken but should be different.
- `orch-fix-defect` — Orchestrate fixing a bug — reproduce it as a failing regression test, fix to green, review, and gated commit — by delegating each phase to the matching ECC agent. Use when existing behavior is broken or wrong.
- `orch-pipeline` — Shared orchestration engine behind the orch-* skill family — the gated Research-Plan-TDD-Review-Commit pipeline, size classifier, agent and command map, and two human gates (plan approval, commit confirmation) that orch-* operation skills delegate to. Use indirectly via orch-add-feature, orch-fix-defect, orch-change-feature, orch-refine-code, or orch-build-mvp; read directly only when adding an orch operation or tuning shared phases.
- `orch-refine-code` — Orchestrate a behavior-preserving refactor — confirm tests are green, restructure without changing behavior, keep tests green, review, and gated commit. Use when the structure should improve but behavior must not change.
- `parallel-execution-optimizer` — Speed up a task by turning it into a dependency graph of parallel lanes with a lane matrix, batched reads and checks, write surfaces isolated by file, worktree, branch, or service, and a final verification table. Use when the user wants a task done much faster through parallel work, concurrent agents, batched tool calls, isolated worktrees, or many independent verification lanes without losing correctness.
- `plan-orchestrate` — Read a plan document, decompose it into steps, design a per-step agent chain from the ECC catalogue, and emit ready-to-paste /orchestrate custom prompts. Generative only — never invokes /orchestrate itself. Use when the user has a multi-step plan and wants to drive it through orchestrate without composing chains by hand.
- `ralphinho-rfc-pipeline` — Split an RFC into a multi-agent execution DAG — decompose into work units with dependencies and acceptance tests, run research, plan, implement, test, and review per unit, then merge through a queue with re-based branches and final system verification. Use when a feature is too large for a single agent pass, orchestrating RFC-driven multi-agent execution, or managing merge queues across agent-built units.
- `recursive-decision-ledger` — Run repeated rollouts ("Prime Gauss" style recursive prompting) while keeping an append-only decision ledger of trials, marks, coherence checks, and promotion gates, so recursive confidence never auto-approves live trading, deploy, or destructive actions. Use when the user asks for repeated rollouts, marked decision processes, high-dimensional search, stochastic optimization, local-optima exploration, ensemble comparison, or recursive reasoning with a visible evidence trail.
- `rules-distill` — Scan skills to extract cross-cutting principles and distill them into rules — append, revise, or create new rule files. Use when the same principle keeps recurring across skills and belongs in a rule file instead.
- `santa-method` — Multi-agent adversarial verification: two independent reviewers with the same rubric must both pass before output ships, with a fix-and-re-review convergence loop and human escalation cap. Use when gating publishing, production deploys, compliance or brand-sensitive content, or hallucination-prone claims before they ship.
- `skill-comply` — Visualize whether skills, rules, and agent definitions are actually followed — auto-generates scenarios at 3 prompt strictness levels, runs agents, classifies behavioral sequences, and reports compliance rates with full tool call timelines. Use when checking whether agents actually follow the skills, rules, and definitions they were given, rather than assuming they do.
- `skill-scout` — Search existing local, marketplace, GitHub, and web skill sources before creating a new skill. Use when the user wants to create, build, fork, or find a skill for a workflow.
- `skill-stocktake` — Use when auditing Claude skills and commands for quality. Supports Quick Scan (changed skills only) and Full Stocktake modes with sequential subagent batch evaluation.
- `strategic-compact` — Suggests manual context compaction at logical intervals to preserve context through task phases rather than arbitrary auto-compaction. Use when a session is approaching a context limit and a task phase is a natural place to compact.
- `team-agent-orchestration` — Run team-based orchestration for agent squads: work items with owners and scope, agent Kanban state, branch isolation, control pane visibility, and merge gates. Use when coordinating multiple agents in parallel across branches or worktrees — multi-agent fan-out, agent Kanban, squad coordination, or merging agent output into one product.
- `token-budget-advisor` — Offer a choice of response depth (25%/50%/75%/100%) with token estimates before answering, then answer at that level. Use when the user asks to control response length or token budget, such as 'token budget', 'short version', 'brief answer', 'respuesta corta vs larga', 'cuántos tokens', 'ahorrar tokens', 'responde al 50%', 'dame la versión corta', 'quiero controlar cuánto usas'. Skip if depth is already set this session or 'token' means an auth/payment token.
- `unified-memory` — Share durable, inspectable context and handoffs between Claude, Codex, Hermes, Cursor, OpenCode, and other agents through the local ECC Memory Vault. Use when an agent must save work state, transfer context, resume another agent's task, or search shared project knowledge.
- `workspace-surface-audit` — Audit the active repo, MCP servers, plugins, connectors, env surfaces, and harness setup, then recommend the highest-value ECC-native skills, hooks, agents, and operator workflows. Use when the user wants help setting up Claude Code or understanding what capabilities are actually available in their environment.

---

## ecc-data

**Use for:** Databases, data pipelines, machine learning, model operation and structured analysis.

**Skills in this pack:**

- `clickhouse-io` — ClickHouse database patterns, query optimization, analytics, and data engineering best practices for high-performance analytical workloads. Use when writing ClickHouse schemas or queries, or when an analytical query is too slow.
- `dashboard-builder` — Build monitoring dashboards that answer real operator questions for Grafana, SigNoz, and similar platforms. Use when turning metrics into a working dashboard instead of a vanity board.
- `data-scraper-agent` — Build a fully automated AI-powered data collection agent for any public source — job boards, prices, news, GitHub, sports, anything. Runs on a schedule, enriches data with a free LLM (Gemini Flash), stores results in Notion/Sheets/Supabase, and learns from user feedback. Runs 100% free on GitHub Actions. Use when the user wants to monitor, collect, or track any public data automatically.
- `data-throughput-accelerator` — Diagnose and accelerate large data movement — ingestion, backfill, export, ETL, warehouse loading, manifest catch-up, and table synchronization — by isolating the true bottleneck, benchmarking variants, and codifying the fastest path with a hard accounting block proving rows and timestamps cohere. Use when a pipeline or backfill is too slow and must get faster without losing data correctness.
- `database-migrations` — Safe, reversible database migration patterns: forward-only production changes, expand-contract zero-downtime renames, concurrent indexes, batched backfills, and per-tool workflows for PostgreSQL, Prisma, Drizzle, Kysely, Django, and golang-migrate. Use when writing a schema or data migration, adding a column or index to a large table, planning a rollback, or preparing a zero-downtime deploy.
- `ito-baskets` — Read-only Itô basket and prediction-market data skill. Index the live basket catalog, compare a basket against user-supplied research or a watchlist, build a source-grounded market brief, or draft a non-executable planning worksheet. Use when a user asks to browse or index Itô baskets, compare a basket against notes or a thesis, research prediction-market events/venues/liquidity, or plan a basket or market idea without trading. Never advises, orders, trades, reserves, or executes.
- `ito-compute` — Query live GPU inventory, submit an authenticated Itô fixed-rate RFQ, inspect RFQ or procurement status, revoke device credentials, and run explicitly gated node qualification through the separately installed canonical CLI. Use when a user asks to find H100/H200 capacity, request a fixed compute rate, check Itô compute status, validate GPU nodes, revoke Itô access, or rent or purchase GPU compute and needs the supported boundary explained.
- `ito-inference` — Inspect the availability of model serving on a completed Itô compute booking and, when the canonical backend becomes available, hand off an explicitly confirmed serving manifest. Use after ito-compute has booked GPU nodes and the user asks for an OpenAI-compatible endpoint, ito-serve, hosted Kimi, or self-hosted open-weights inference. ECC implements no serving stack of its own.
- `ito-training` — Inspect the availability of ML training on a completed Itô compute booking and, when the canonical backend becomes available, hand off an explicitly confirmed training manifest. Use after ito-compute has booked GPU nodes and the user wants pre-training, fine-tuning, or RL on that metal. ECC implements no training stack of its own.
- `latency-critical-systems` — Optimize and verify latency-sensitive systems — realtime dashboards, market data feeds, streaming agents, execution gateways, queues, and caches — by tracking p50/p95/p99 latency, freshness age, and queue depth, mapping hot paths, and running live readbacks. Use when p95 latency, throughput, or data freshness matters.
- `ml-adoption-playbook` — End-to-end methodology for AI agents and software engineers to add machine learning algorithms to existing non-ML codebases. Covers problem framing, data readiness, architectural decoupling, and baseline model integration. Use when adding a machine learning capability to a codebase that has none, from problem framing through a baseline model.
- `mle-workflow` — Production machine-learning engineering workflow for data contracts, reproducible training, model evaluation, deployment, monitoring, and rollback. Use when building, reviewing, or hardening ML systems beyond one-off notebooks.
- `mysql-patterns` — MySQL and MariaDB schema, query, indexing, transaction, replication, and connection-pool patterns for production backends. Use when designing MySQL or MariaDB schemas and indexes, or when a query, transaction, or replica lags.
- `postgres-patterns` — PostgreSQL database patterns for query optimization, schema design, indexing, and security. Based on Supabase best practices. Use when designing PostgreSQL schemas, indexes, or RLS policies, or when a query is too slow.
- `prisma-patterns` — Prisma ORM patterns for TypeScript backends — schema design, query optimization, transactions, pagination, and critical traps like updateMany returning count not records, $transaction timeouts, migrate dev resetting the DB, @updatedAt skipped on bulk writes, and serverless connection exhaustion. Use when writing a Prisma schema or query, or debugging transactions, migrations, or serverless connection limits.
- `pytorch-patterns` — PyTorch deep learning patterns and best practices for building robust, efficient, and reproducible training pipelines, model architectures, and data loading. Use when writing or reviewing PyTorch training loops, model architectures, or data loading, or when a run will not reproduce.
- `recsys-pipeline-architect` — Design composable recommendation, ranking, and feed pipelines using the six-stage Source→Hydrator→Filter→Scorer→Selector→SideEffect framework popularized by xAI's open-sourced For You algorithm. Use this skill whenever the user is building any system that picks "the top K items for a (user, context)" — social feeds, content CMSs, RAG rerankers, task prioritizers, notification triage, search reranking, ad ranking.
- `redis-patterns` — Redis data structure patterns, caching strategies, distributed locks, rate limiting, pub/sub, and connection management for production applications. Use when adding caching, a distributed lock, rate limiting, or pub/sub with Redis, or when key design needs review.
- `social-graph-ranker` — Weighted social-graph ranking for warm intro discovery, bridge scoring, and network gap analysis across X and LinkedIn. Use when the user wants the reusable graph-ranking engine itself, not the broader outreach or network-maintenance workflow layered on top of it.

---

## ecc-research-growth

**Use for:** Evidence-backed research, brand voice, publishing, growth and commercial analysis.

**Skills in this pack:**

- `article-writing` — Write articles, guides, blog posts, tutorials, newsletter issues, and other long-form content in a distinctive voice derived from supplied examples or brand guidance. Use when the user wants polished written content longer than a paragraph, especially when voice consistency, structure, and credibility matter.
- `benchmark-methodology` — Score a scoped competitor set into comparable profile cards: nine weighted dimensions (positioning, voice, visual craft, offer packaging, evidence, enterprise-readiness, thought leadership, pricing, client tension) with 1-5 evidence-anchored rubrics and a tension 2x2 plot. Use when benchmarking or scoring competitors, building a competitive comparison matrix, or grading rival positioning before assembling the report; runs after competitive-platform-analysis and before competitive-report-structure.
- `brand-discovery` — Run a structured, resumable multi-session brand identity interview across 8 modules (purpose, positioning, audience, personality, voice, narrative, founder tension) using laddering, 5 Whys, and projective techniques, persisting answers to disk and producing a master brandbook (90_SYNTHESIS.md). Use when creating or repositioning a brand, briefing designers or writers, or making implicit founder knowledge explicit.
- `brand-voice` — Build a source-derived writing style profile from real posts, essays, launch notes, docs, or site copy, then reuse that profile across content, outreach, and social workflows. Use when the user wants voice consistency without generic AI writing tropes.
- `competitive-platform-analysis` — Use when scoping a competitive landscape — identifying, categorising, and score-filtering a competitor set before any benchmarking begins. Decides who counts as a competitor, which tier they belong to, and which sources to mine. First step in the three-skill competitive pipeline; precedes benchmark-methodology.
- `competitive-report-structure` — Assemble scored competitor profile cards (from benchmark-methodology) into a decision-grade competitive report with landscape map, competitor tiers, benchmarking matrix, white-space analysis, strategic recommendations, and team alignment trigger questions. Use when presenting competitive findings to leadership or a board, writing a competitive landscape report, or as the final step of the competitive analysis pipeline.
- `content-engine` — Create platform-native content systems for X, LinkedIn, TikTok, YouTube, newsletters, and repurposed multi-platform campaigns. Use when the user wants social posts, threads, scripts, content calendars, or one source asset adapted cleanly across platforms.
- `crosspost` — Multi-platform content distribution across X, LinkedIn, Threads, and Bluesky. Adapts content per platform using content-engine patterns. Never posts identical content cross-platform. Use when the user wants to distribute content across social platforms.
- `deep-research` — Produce cited research reports from multiple web sources using firecrawl and exa MCP tools — plan sub-questions, search and deep-read sources, then synthesize findings with inline citations and confidence levels. Use when the user asks to research a topic in depth, run a deep dive or investigation, or do competitive analysis, technology evaluation, market sizing, or due diligence on a company.
- `exa-search` — Neural search via Exa MCP for web, code, and company research. Use when the user needs web search, code examples, company intel, people lookup, or AI-powered deep research with Exa's neural search engine.
- `investor-materials` — Create and update pitch decks, one-pagers, investor memos, accelerator applications, financial models, and fundraising materials. Use when the user needs investor-facing documents, projections, use-of-funds tables, milestone plans, or materials that must stay internally consistent across multiple fundraising assets.
- `investor-outreach` — Draft cold emails, warm intro blurbs, follow-ups, update emails, and investor communications for fundraising. Use when the user wants outreach to angels, VCs, strategic investors, or accelerators and needs concise, personalized, investor-facing messaging.
- `lead-intelligence` — AI-native lead intelligence and outreach pipeline. Replaces Apollo, Clay, and ZoomInfo with agent-powered signal scoring, mutual ranking, warm path discovery, source-derived voice modeling, and channel-specific outreach across email, LinkedIn, and X. Use when the user wants to find, qualify, and reach high-value contacts.
- `market-research` — Conduct market research, competitive analysis, investor due diligence, and industry intelligence with source attribution and decision-oriented summaries. Use when the user wants market sizing, competitor comparisons, fund research, technology scans, or research that informs business decisions.
- `marketing-campaign` — End-to-end marketing campaign planning and execution. Covers audience research, positioning, campaign angle definition, landing page copy, email sequences, social posts, ad copy, short-form video scripts, and content calendars. Use as the orchestration layer for multi-channel product launches. Use when planning or executing a multi-channel product launch, or producing landing page, email, social, or ad copy.
- `research-ops` — Evidence-first current-state research workflow for ECC. Use when the user wants fresh facts, comparisons, enrichment, or a recommendation built from current public evidence and any supplied local context.
- `scientific-db-pubmed-database` — Direct PubMed and NCBI E-utilities search workflows for biomedical literature, MeSH queries, PMID lookup, citation retrieval, and API-backed literature monitoring. Use when a task needs biomedical literature from PubMed rather than general web search.
- `scientific-db-uspto-database` — USPTO patent and trademark data workflow for official record lookup, PatentSearch queries, TSDR checks, assignment data, and reproducible IP research logs. Use when a task needs official United States patent or trademark records from USPTO systems.
- `scientific-pkg-gget` — gget CLI and Python workflow for quick genomic database queries, sequence lookup, BLAST-style searches, enrichment checks, and reproducible bioinformatics evidence logs. Use when a task needs quick bioinformatics lookup across genomic reference databases with the gget CLI or Python package.
- `scientific-thinking-literature-review` — Systematic literature-review workflow for academic, biomedical, technical, and scientific topics, including search planning, source screening, synthesis, citation checks, and evidence logging. Use when the task is to find, screen, synthesize, and cite a body of academic or technical literature.
- `scientific-thinking-scholar-evaluation` — Structured scholarly-work evaluation for papers, proposals, literature reviews, methods sections, evidence quality, citation support, and research-writing feedback. Use when evaluating academic or scientific work — papers, proposals, methods sections, or evidence quality — against a repeatable rubric.
- `seo` — Audit, plan, and implement SEO improvements across technical SEO, on-page optimization, structured data, Core Web Vitals, and content strategy. Use when the user wants better search visibility, SEO remediation, schema markup, sitemap/robots work, or keyword mapping.
- `social-publisher` — Agent-driven scheduling and publishing of social media posts across 13 platforms via SocialClaw. Use when the user wants to publish to X, LinkedIn, Instagram, Facebook Pages, TikTok, Discord, Telegram, YouTube, Reddit, WordPress, or Pinterest — or when managing campaigns, uploading media, or monitoring post delivery status.
- `taste` — Creative-direction layer for music videos and short-form edits in the angelcore / cloud-trance / hyperpop family — a named-genre aesthetic vocabulary, mood + color + light system, beat-synced editing grammar, and a pipeline chaining ECC's video skills from b-roll generation to distribution. Use when a video must feel intentional rather than merely functional — music videos, fancams, moodboard-driven reels, or giving AI-generated b-roll a coherent visual direction.
- `taste-application` — Generate new video against a distilled style pack and cut it into a finished piece - plan takes from the reference's cut rhythm, generate on fal, grade with the pack's measured LUT, cut at the measured cadence, weave in existing footage, composite overlay plates, mint 3D props, and verify the result numerically. Use when the user wants to make a video in a captured style, supplement existing footage, or assemble generated clips into a real edit.
- `taste-distillation` — Measure a set of reference videos into a reusable style pack - colour grade as a 3D LUT, cut rhythm as a shot-length distribution, hero stills, screen-blend overlay plates, and a text spec for a generative model. Use when the user wants to capture the look of reference footage, build a repeatable look, mint assets from references, or reproduce someone's grade and pacing.
- `x-api` — X/Twitter API integration for posting tweets, threads, reading timelines, search, and analytics. Covers OAuth auth patterns, rate limits, and platform-native content posting. Use when the user wants to interact with X programmatically.

---

## ecc-media

**Use for:** Video, motion, Blender, slides, media generation and document processing.

**Skills in this pack:**

- `blender-motion-state-inspection` — Use this skill when inspecting Blender characters, rigs, poses, animation retargeting, ground contact, facing direction, or model-vs-motion alignment where screenshots alone are not enough.
- `fal-ai-media` — Unified media generation via fal.ai MCP — image, video, and audio. Covers text-to-image (Nano Banana), text/image-to-video (Seedance, Kling, Veo 3), text-to-speech (CSM-1B), and video-to-audio (ThinkSound). Use when the user wants to generate images, videos, or audio with AI.
- `frontend-slides` — Create stunning, animation-rich HTML presentations from scratch or by converting PowerPoint files. Use when the user wants to build a presentation, convert a PPT/PPTX to web, or create slides for a talk/pitch. Helps non-designers discover their aesthetic through visual exploration rather than abstract choices.
- `ios-icon-gen` — Generate iOS app icons as PNG imagesets for Xcode asset catalogs from SF Symbols (5000+ Apple-native) or Iconify API (275k+ open source icons from 200+ collections). Use when generating icons, creating icon assets, adding icons to asset catalog, or searching for icons for iOS projects.
- `manim-video` — Build reusable Manim explainers for technical concepts, graphs, system diagrams, and product walkthroughs, then hand off to the wider ECC video stack if needed. Use when the user wants a clean animated explainer rather than a generic talking-head script.
- `nutrient-document-processing` — Process, convert, OCR, extract, redact, sign, and fill documents using the Nutrient DWS API. Works with PDFs, DOCX, XLSX, PPTX, HTML, and images. Use when converting, OCRing, extracting from, redacting, signing, or filling documents via the Nutrient DWS API.
- `tasteforge-video` — Use for file-driven multimodal image, video, and 3D-asset discovery; taste interviews; distill or apply workflows; style-pack validation; editable EDL/FCPXML export; provenance audits; and offline planning that must fail closed before provider generation.
- `ui-demo` — Record polished UI demo videos using Playwright. Use when the user asks to create a demo, walkthrough, screen recording, or tutorial video of a web application. Produces WebM videos with visible cursor, natural pacing, and professional feel.
- `video-editing` — AI-assisted video editing workflows for cutting, structuring, and augmenting real footage. Covers the full pipeline from raw capture through FFmpeg, Remotion, ElevenLabs, fal.ai, and final polish in Descript or CapCut. Use when the user wants to edit video, cut footage, create vlogs, or build video content.
- `videodb` — Ingest, index, search, edit, and monitor video and audio with the VideoDB Python SDK — upload from files, URLs, or RTSP feeds, build spoken and scene indexes with timestamped search and playable clips, transcode and reframe, do timeline edits (subtitles, overlays, dubbing), and run real-time alerts on live streams or desktop capture. Use when working with video search, transcription, clipping, transcoding, streaming, or live video alerts.
- `visa-doc-translate` — Translate visa document images (bank deposit, employment, income, and retirement certificates; HEIC, PNG, or JPG) into English via OCR and produce a bilingual PDF pairing the original image with a formatted certified-style translation. Use when a visa application needs a document translated to English, an official certificate OCR'd and translated, or a bilingual translation PDF for immigration paperwork.

---

## ecc-operations

**Use for:** Infrastructure, integrations, networking and evidence-first business operations.

**Skills in this pack:**

- `automation-audit-ops` — Evidence-first automation inventory and overlap audit workflow for ECC. Use when the user wants to know which jobs, hooks, connectors, MCP servers, or wrappers are live, broken, redundant, or missing before fixing anything.
- `canary-watch` — Use this skill to monitor and verify a deployed URL after releases — checks HTTP endpoints, SSE streams, static assets, console errors, and performance regressions after deploys, merges, or dependency upgrades. Smoke / canary / post-deploy verification.
- `carrier-relationship-management` — Manage truckload, LTL, and intermodal carrier portfolios: sourcing and FMCSA vetting, freight rate and fuel-surcharge negotiation, RFPs and routing guides, carrier scorecards, allocation, and renewals. Use when onboarding carriers, running freight RFPs, negotiating rates, evaluating carrier performance, reallocating freight, or building freight strategy.
- `cisco-ios-patterns` — Cisco IOS and IOS-XE review patterns for show commands, config hierarchy, wildcard masks, ACL placement, interface hygiene, and safe change-window verification. Use when reading, writing, or reviewing Cisco IOS / IOS-XE configuration or planning a change window.
- `ck` — Persistent per-project memory for Claude Code (Context Keeper) driven by deterministic Node.js /ck commands: init, save, resume, info, list, forget, and v1-to-v2 migrate, plus a SessionStart hook that injects a compact project brief. Use when context must survive across sessions, saving session state with next steps and decisions, resuming where a previous session left off, or picking up a project without re-explaining it.
- `counterparty-channel-discipline` — Per-channel strict prompts, mention gating, silent observation, and a communication autonomy policy for agents that sit in shared channels with external counterparties. Use when an agent joins group chats, shared channels, or DMs where outsiders can read every message and you need it to speak only when addressed, never leak internal context, and route risky content to draft-only approval.
- `customer-billing-ops` — Operate customer billing workflows such as subscriptions, refunds, churn triage, billing-portal recovery, and plan analysis using connected billing tools like Stripe. Use when the user needs to help a customer, inspect subscription state, or manage revenue-impacting billing operations.
- `customs-trade-compliance` — Codified customs and trade compliance expertise — HS/HTS tariff classification with GRI rules, commercial invoices and entry documentation, Incoterms 2020, FTA qualification and duty optimization (USMCA, RCEP, FTZs, drawback), denied-party screening, and penalty mitigation across US, EU, UK, and APAC jurisdictions. Use when classifying goods, preparing import/export documentation, screening restricted parties, responding to customs audits or CF-28/penalty notices, or optimizing duties.
- `docker-patterns` — Docker and Docker Compose patterns for local development, hardened CLI installer harnesses, container security, networking, volumes, and multi-service orchestration. Use when creating or reviewing Dockerfiles and Compose services, testing installers across Linux distributions, or planning accurate native macOS and Windows validation.
- `email-ops` — Evidence-first mailbox triage, drafting, send verification, and sent-mail-safe follow-up workflow for ECC. Use when the user wants to organize email, draft or send through the real mail surface, or prove what landed in Sent.
- `energy-procurement` — Procure electricity and natural gas for commercial and industrial facilities: tariff and rate-schedule optimization, demand-charge mitigation, supplier RFPs, fixed/index/block-and-index hedging, renewable PPA and REC evaluation, and sustainability reporting. Use when procuring energy, optimizing utility tariffs, managing demand charges, evaluating PPAs, or building energy budgets and hedge strategies.
- `esign-field-placement` — Deterministic method for placing signature, date, and text fields in a web e-signature composer through a browser automation session, using a fixed signature page, numeric Location panel coordinates instead of drag, and a save-as-draft default. Use when automating envelope preparation for generated agreements and you need repeatable field positions, correct per-recipient ownership, and a hard gate before anything is sent or signed.
- `finance-billing-ops` — Evidence-first revenue, pricing, refunds, team-billing, and billing-model truth workflow for ECC. Use when the user wants a sales snapshot, pricing comparison, duplicate-charge diagnosis, or code-backed billing reality instead of generic payments advice.
- `flox-environments` — Create reproducible, cross-platform (macOS/Linux) development environments with Flox, a declarative Nix-based environment manager. Use when setting up project toolchains, installing system-level dependencies (compilers, databases, native libs), pinning exact package versions for a team, onboarding developers, running local services (PostgreSQL, Redis, Kafka), or solving 'works on my machine' problems — including agent/vibe-coding setups that need project-scoped tools without sudo. Also use when the user mentions .flox/, manifest.toml, flox activate, or FloxHub.
- `google-workspace-ops` — Operate across Google Drive, Docs, Sheets, and Slides as one workflow surface for plans, trackers, decks, and shared documents. Use when the user needs to find, summarize, edit, migrate, or clean up Google Workspace assets without dropping to raw tool calls.
- `homelab-network-readiness` — Readiness checklist for homelab VLAN segmentation, local DNS filtering (Pi-hole, AdGuard Home), and WireGuard-style remote access. Use when planning or reviewing home network changes — splitting a flat network into trusted, IoT, guest, or management VLANs, moving DHCP to a local resolver, or adding VPN access — before changing router, firewall, DHCP, or VPN configuration.
- `homelab-network-setup` — Practical home and homelab network planning for gateways, switches, access points, IP ranges, DHCP reservations, DNS, cabling, and common beginner mistakes. Use when planning or fixing a home or homelab network — gateway, switch, AP, IP ranges, DHCP, DNS, or cabling.
- `homelab-pihole-dns` — Pi-hole installation, blocklist management, DNS-over-HTTPS setup, DHCP integration, local DNS records, and troubleshooting broken DNS resolution on a home network. Use when the task explicitly involves Pi-hole — installing it, managing blocklists, configuring DoH or DHCP, adding local DNS records, or diagnosing DNS resolution with Pi-hole in the path.
- `homelab-vlan-segmentation` — Segmenting home networks into VLANs for IoT, guest, trusted, and server traffic using UniFi, pfSense/OPNsense, and MikroTik — including switch trunk config, firewall rules, and wireless SSID mapping. Use when splitting a home network into IoT, guest, trusted, and server VLANs on UniFi, pfSense/OPNsense, or MikroTik.
- `homelab-wireguard-vpn` — WireGuard VPN server setup, peer configuration, key generation, split tunneling vs full tunnel routing, and remote access to a home network from mobile and laptop clients. Use when setting up WireGuard for remote access to a home network, or deciding between split and full tunnel routing.
- `inventory-demand-planning` — Codified demand planning expertise for multi-location retailers: demand forecasting method selection, ABC/XYZ segmentation, safety stock and reorder-point optimization, promotional lift and post-promo dip estimation, and seasonal transition and markdown timing. Use when forecasting demand, setting safety stock, planning replenishment, managing promotions, or optimizing inventory levels.
- `jira-integration` — Use this skill when retrieving Jira tickets, analyzing requirements, updating ticket status, adding comments, or transitioning issues. Provides Jira API patterns via MCP or direct REST calls.
- `kubernetes-patterns` — Kubernetes workload patterns, resource management, RBAC, probes, autoscaling, ConfigMap/Secret handling, and kubectl debugging for production-grade deployments. Use when writing or reviewing Kubernetes manifests, or debugging probes, RBAC, autoscaling, or resource limits.
- `logistics-exception-management` — Codified freight-exception handling expertise for shipment delays, damages, losses, shortages, and carrier disputes, with escalation protocols, carrier-specific behaviors by mode, claims procedures, and eat-the-cost vs fight-the-claim judgment frameworks. Use when handling shipping exceptions, freight claims, delivery issues, or carrier disputes.
- `mailtrap-email-integration` — Guides agents through integrating transactional email sending via Mailtrap's Email API, including sandbox testing, domain verification, and API authentication. Use when implementing email-sending features, debugging delivery issues, or setting up safe dev/staging email testing.
- `master-agreement-generator` — Generate review drafts of counterparty master agreements from one template plus a JSON spec, with role-selected clauses and a Schedule A workflow limited to the executed agreement's notice authority. Use when you need reproducible drafting and separately reviewed execution preparation.
- `messages-ops` — Evidence-first live messaging workflow for ECC. Use when the user wants to read texts or DMs, recover a recent one-time code, inspect a thread before replying, or prove which message source was actually checked.
- `netmiko-ssh-automation` — Safe Python Netmiko patterns for read-only collection, bounded batch SSH, TextFSM parsing, guarded config changes, timeouts, and network automation error handling. Use when automating network device access with Python Netmiko, whether collecting state or pushing guarded config changes.
- `network-bgp-diagnostics` — Diagnostics-only BGP troubleshooting patterns for neighbor state, route exchange, prefix policy, AS path inspection, and safe evidence collection. Use when a BGP neighbor is down, routes are missing, or prefix policy and AS path need inspection.
- `network-config-validation` — Pre-deployment checks for router and switch configuration, including dangerous commands, duplicate addresses, subnet overlaps, stale references, management-plane risk, and IOS-style security hygiene. Use when reviewing a router or switch configuration before deployment.
- `network-interface-health` — Diagnose interface errors, drops, CRCs, duplex mismatches, flapping, speed negotiation issues, and counter trends on routers, switches, and Linux hosts. Use when an interface shows errors, drops, CRCs, flapping, or a duplex or speed mismatch.
- `production-scheduling` — Codified expertise for production scheduling, job sequencing, line balancing, changeover optimization, and bottleneck resolution in discrete and batch manufacturing. Informed by production schedulers with 15+ years experience. Includes TOC/drum-buffer-rope, SMED, OEE analysis, disruption response frameworks, and ERP/MES interaction patterns. Use when scheduling production, resolving bottlenecks, optimizing changeovers, responding to disruptions, or balancing manufacturing lines.
- `project-flow-ops` — Operate execution flow across GitHub and Linear by triaging issues and pull requests, linking active work, and keeping GitHub public-facing while Linear remains the internal execution layer. Use when the user wants backlog control, PR triage, or GitHub-to-Linear coordination.
- `quality-nonconformance` — Quality control and non-conformance management for regulated manufacturing (FDA 21 CFR 820, IATF 16949, AS9100): NCR lifecycle and disposition, 5-Why/Ishikawa/fault-tree/8D root cause analysis, CAPA systems, SPC interpretation, AQL sampling, and supplier quality audits. Use when investigating non-conformances, performing root cause analysis, managing CAPAs, interpreting SPC data, or handling supplier quality issues.
- `returns-reverse-logistics` — Codified expertise for returns authorization, receipt and inspection, disposition decisions, refund processing, fraud detection, and warranty claims management. Informed by returns operations managers with 15+ years experience. Includes grading frameworks, disposition economics, fraud pattern recognition, and vendor recovery processes. Use when handling product returns, reverse logistics, refund decisions, return fraud detection, or warranty claims.
- `uncloud` — Use when managing an Uncloud cluster — deploying services, configuring Caddy ingress, adding static proxy routes for non-cluster devices, publishing ports, scaling, inspecting logs, or managing machines and volumes with the `uc` CLI.
- `unified-notifications-ops` — Operate notifications as one ECC-native workflow across GitHub, Linear, desktop alerts, hooks, and connected communication surfaces. Use when the real problem is alert routing, deduplication, escalation, or inbox collapse.

---

## ecc-security-domains

**Use for:** Specialist security, healthcare and financial protocols; not authorization for external actions.

**Skills in this pack:**

- `agent-payment-x402` — Add x402 payment execution to AI agents with per-task budgets, spending controls, and non-custodial wallets. Supports Base through agentwallet-sdk and X Layer through OKX Payments / OKX Agent Payments Protocol. Use when an agent must pay for something itself and needs per-task budgets, spending controls, and a non-custodial wallet.
- `defi-amm-security` — Security checklist for Solidity AMM contracts, liquidity pools, and swap flows. Covers reentrancy, CEI ordering, donation or inflation attacks, oracle manipulation, slippage, admin controls, and integer math. Use when auditing or writing Solidity AMM, liquidity pool, or swap code.
- `evm-token-decimals` — Prevent silent decimal mismatch bugs across EVM chains. Covers runtime decimal lookup, chain-aware caching, bridged-token precision drift, and safe normalization for bots, dashboards, and DeFi tools. Use when handling token amounts across EVM chains, or when a balance, price, or transfer amount is off by orders of magnitude.
- `gateguard` — PreToolUse fact-forcing gate that denies the first Edit/Write/Bash (including MultiEdit) attempt until the agent presents concrete facts (importers, data schemas, verbatim user instruction), then allows retry; A/B-tested at +2.25 quality points. Use when enabling or configuring the GateGuard hook, exempting paths via env vars, or handling first-touch denials.
- `healthcare-cdss-patterns` — Clinical Decision Support System (CDSS) development patterns. Drug interaction checking, dose validation, clinical scoring (NEWS2, qSOFA), alert severity classification, and integration into EMR workflows. Use when building clinical decision support — drug interaction checks, dose validation, clinical scoring, or alert severity.
- `healthcare-emr-patterns` — EMR/EHR development patterns for healthcare applications. Clinical safety, encounter workflows, prescription generation, clinical decision support integration, and accessibility-first UI for medical data entry. Use when building EMR or EHR features such as encounter workflows, prescription generation, or clinical data entry UI.
- `healthcare-eval-harness` — Patient safety evaluation harness for healthcare application deployments. Automated test suites for CDSS accuracy, PHI exposure, clinical workflow integrity, and integration compliance. Blocks deployments on safety failures. Use when a healthcare deployment must be gated on patient-safety tests for CDSS accuracy, PHI exposure, and workflow integrity.
- `healthcare-phi-compliance` — Protected Health Information (PHI) and PII compliance patterns for healthcare applications: data classification, row-level access control, tamper-proof audit trails, schema tagging, and common leak vectors such as logs, URLs, and browser storage. Use when code touches patient or clinician data, when implementing HIPAA or GDPR access controls, or when auditing a healthcare system for data exposure.
- `hipaa-compliance` — HIPAA-specific entrypoint for healthcare privacy and security work. Use when a task is explicitly framed around HIPAA, PHI handling, covered entities, BAAs, breach posture, or US healthcare compliance requirements.
- `llm-trading-agent-security` — Security patterns for autonomous trading agents with wallet or transaction authority. Covers prompt injection, spend limits, pre-send simulation, circuit breakers, MEV protection, and key handling. Use when an autonomous agent holds wallet or transaction authority and its limits, simulation, or key handling need review.
- `nodejs-keccak256` — Prevent Ethereum hashing bugs in JavaScript and TypeScript. Node's sha3-256 is NIST SHA3, not Ethereum Keccak-256, and silently breaks selectors, signatures, storage slots, and address derivation. Use when hashing for Ethereum in JavaScript or TypeScript, or when a selector, signature, storage slot, or derived address is wrong.
- `prediction-market-oracle-research` — Research prediction markets as data sources or oracle signals for products, agents, dashboards, and corporate decision intelligence. Use for source-grounded analysis of market-implied probabilities, caveats, and integration patterns without investment advice. Use when evaluating prediction markets as a data source or oracle signal for a product, agent, or dashboard.
- `prediction-market-risk-review` — Review prediction-market, basket, oracle, and trading-agent workflows for compliance, safety, data-quality, privacy, and execution risk. Use before any workflow handles venue auth, user portfolio data, API keys, or trade planning.
- `safety-guard` — Guard against destructive operations with three modes: Careful intercepts dangerous commands (rm -rf, git push --force, DROP TABLE) for confirmation, Freeze locks writes to one directory, and Guard combines both via PreToolUse hooks. Use when working on production systems, running agents autonomously, restricting edits to a directory, or during migrations, deploys, and data changes.
- `security-bounty-hunter` — Hunt for exploitable, bounty-worthy security issues in repositories. Focuses on remotely reachable vulnerabilities that qualify for real reports instead of noisy local-only findings. Use when hunting reportable, remotely reachable vulnerabilities in a repository.
- `security-scan` — Scan your Claude Code configuration (.claude/ directory) for security vulnerabilities, misconfigurations, and injection risks using AgentShield. Checks CLAUDE.md, settings.json, MCP servers, hooks, and agent definitions. Use when auditing a .claude/ directory — CLAUDE.md, settings.json, MCP servers, hooks, or agent definitions.

---

<!-- ECC-GENERATED END -->
