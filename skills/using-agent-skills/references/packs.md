# Agentit runtime skill packs

Packs are **flat semantic discovery maps**, not context bundles, tiers, curricula, priority lists, or routing code.

Their only job is to let a capable agent quickly answer:

1. what domain am I working in?
2. what Agentit skills exist around that domain?
3. what problem does each skill solve?

The primary AI then decides which skill bodies to load and **how many**. There is no minimum, maximum, default count, level, or required order.

A pack with twenty listed skills can still lead to `selected_skills: []` or one selected skill. Another task may justify many. That decision belongs to the model looking at the actual task.

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

The pack names are discovery/provenance labels. **Only the selected skill bodies consume worker skill context.**

Do not infer a skill count from pack size, task size, risk label, or worker title.

---

## engineering

**Use for:** general implementation, bugs, refactors, repository changes, code quality, architecture, testing, debugging, security-sensitive code, performance work and engineering delivery.

**Skills in this pack:**

- `incremental-implementation` — build in small verifiable slices when incremental delivery reduces rework.
- `debugging-and-error-recovery` — reproduce, localize, fix and guard when something is actually broken.
- `planning-and-task-breakdown` — decompose non-trivial work when an explicit execution plan would help.
- `test-driven-development` — use behavioral tests to drive or prove implementation when TDD fits the change.
- `code-review-and-quality` — independent correctness/quality review before accepting meaningful code changes.
- `code-simplification` — reduce unnecessary complexity while preserving proven behavior.
- `verification-before-completion` — fresh evidence before done/fixed/passing claims.
- `verification-gauntlet` — broader verification discipline when multiple evidence surfaces matter.
- `doubt-driven-development` — adversarially challenge unfamiliar, risky or consequential engineering decisions.
- `security-and-hardening` — threat modeling, trust boundaries, auth, secrets, input handling and hardening when security is materially involved.
- `performance-optimization` — measure and optimize real bottlenecks rather than guessing.
- `source-driven-development` — current official framework/library/protocol documentation materially affects correctness.
- `architect-orchestrator` — structural decomposition, architectural ownership or multi-stage coordination when one direct execution path is insufficient.
- `specialist-agent-routing` — spawn bounded specialists only when specialization, independence or context isolation is useful.
- `context-engineering` — control large or fragmented engineering context deliberately.
- `git-workflow-and-versioning` — branch/commit/history discipline when Git handoff matters.
- `documentation-and-adrs` — preserve durable architecture/decision knowledge when it would be expensive to rediscover.
- `observability-and-instrumentation` — logs, metrics, traces and operational diagnostics when runtime behavior matters.
- `ci-cd-and-automation` — CI/CD and automated quality gates.
- `deprecation-and-migration` — safely retire or migrate interfaces/systems while preserving compatibility requirements.

---

## frontend

**Use for:** application UI implementation, browser behavior, accessibility, frontend architecture, runtime verification and frontend performance.

**Skills in this pack:**

- `frontend-ui-engineering` — production frontend implementation, component structure and accessibility baseline.
- `browser-testing-with-devtools` — verify rendered/runtime behavior in a real browser.
- `performance-optimization` — measure and improve frontend performance when evidence shows a bottleneck.
- `code-simplification` — keep component/state architecture lean.
- `anti-ai-slop-design` — lightweight guard against generic visual clichés and fabricated content.
- `design-taste-frontend` — stronger visual judgment when implementation also needs art-direction sensitivity.
- `source-driven-development` — current framework/browser/API behavior matters.
- `security-and-hardening` — auth/session/input/trust-boundary work in frontend surfaces.
- `test-driven-development` — component/behavior tests when useful.
- `verification-before-completion` — fresh runtime/build/test evidence before completion claims.

If visual direction is material, inspect the `design` pack too. That does not require loading the whole design pack.

---

## design

**Use for:** public websites, landing pages, product/brand visual systems, visual direction, interaction design, motion, scrollytelling, Figma work and spatial/3D experiences.

**Skills in this pack:**

- `design-taste-frontend` — visual direction, hierarchy, composition and anti-generic frontend design judgment.
- `anti-ai-slop-design` — detect cliché AI aesthetics, fabricated proof and generic structural repetition.
- `design-inspiration-research` — research references, extract design DNA, synthesize rather than clone, and preserve provenance. Its references include the distilled premium/high-craft website production playbook.
- `impeccable-design` — structured visual critique and polish passes.
- `ui-ux-pro-max-intelligence` — broader UI/UX pattern intelligence when the task benefits from it.
- `emil-design-eng` — interaction craft and design-engineering judgment.
- `design-trend-researcher` — investigate current visual/interaction patterns when freshness matters.
- `creative-web-experiences` — unconventional interactive web concepts when a standard page is not enough.
- `visual-storytelling-director` — narrative sequencing, visual story structure and presentation rhythm.
- `creative-tool-scout` — choose creative tools when unusual visual requirements make tooling selection material.
- `delight-and-whimsy` — deliberate moments of delight when they serve the experience rather than decorate everything.
- `figma-design-workflow` — Figma as a real source, collaboration or handoff surface.
- `scrollytelling-web` — narrative scroll experiences and section/state choreography.
- `gsap-scrolltrigger` — ScrollTrigger/timeline mechanics when GSAP is the right implementation tool.
- `gsap-performance` — keep advanced GSAP motion performant.
- `threejs-spatial-experiences` — interactive spatial/3D web experiences.
- `threejs-product-storytelling` — 3D specifically as a product/narrative device.
- `frontend-ui-engineering` — bridge visual direction into production-quality accessible UI.
- `browser-testing-with-devtools` — rendered desktop/mobile/browser evidence.
- `performance-optimization` — visual/motion work where runtime cost needs measurement.
- `reference-intelligence` — use only when external/current references materially affect the design decision or provenance.
- `mobile-native-app-design` — inspect only when the actual surface is native Expo/React Native product UI; it is not a default web-design dependency.

The design pack intentionally has many possibilities. **Do not subdivide them into basic/advanced tiers and do not infer that ambitious design work must load more of them.**

---

## mobile

**Use for:** Expo/React Native, iOS/Android product UI, onboarding, paywalls, native navigation, sheets/modals, mobile state design and simulator-verified interaction work.

**Skills in this pack:**

- `mobile-native-app-design` — study shipped mobile winners when useful, extract patterns rather than pixels, implement native-feeling Expo/React Native UI and verify whole flows in a simulator/emulator.
- `anti-ai-slop-design` — prevent generic AI styling and fabricated visual proof without importing the whole web-design pack.
- `source-driven-development` — use current Expo/React Native/platform documentation when API or platform behavior materially affects implementation.
- `mcp-tooling-fit` — inspect/enable the situational `mobile_design` MCP stack only when Appllama research would materially help and the user has/wants access.
- `verification-before-completion` — require fresh simulator/build/runtime evidence before claiming mobile UI behavior is complete.

Appllama is **optional, paid and credit-metered**. Its presence never makes `mobile-native-app-design` global/core, and the pack itself never auto-enables the MCP or dictates a fixed skill count.

---

## backend

**Use for:** APIs, integrations, services, server-side architecture, runtime operations and backend trust boundaries.

**Skills in this pack:**

- `api-and-interface-design` — API/contracts/boundaries and compatibility decisions.
- `observability-and-instrumentation` — logs, metrics, traces and diagnostics.
- `test-driven-development` — service/API behavior proof when useful.
- `code-simplification` — avoid accidental service/framework complexity.
- `verification-before-completion` — fresh runtime/test evidence.
- `security-and-hardening` — auth, secrets, PII, permissions and trust boundaries.
- `performance-optimization` — measured server/data-path optimization.
- `source-driven-development` — current protocols/framework/provider contracts.
- `architect-orchestrator` — structural or multi-service work.
- `debugging-and-error-recovery` — reproduce/localize backend failures.
- `deprecation-and-migration` — interface/service migration and compatibility work.

---

## data

**Use for:** databases, persistence, schemas, queries, migrations and data-heavy application work.

**Skills in this pack:**

- `supabase-postgres-best-practices` — PostgreSQL/Supabase-specific guidance **only when that stack is actually present**.
- `source-driven-development` — current database/platform docs and contracts.
- `test-driven-development` — prove query/migration/data behavior when appropriate.
- `observability-and-instrumentation` — data-path/runtime diagnostics.
- `security-and-hardening` — access controls, PII, row-level security and data trust boundaries.
- `performance-optimization` — measure query/storage/index performance before changing it.
- `doubt-driven-development` — adversarial review for destructive or structurally risky migrations.
- `architect-orchestrator` — multi-stage migrations and dependent systems.
- `deprecation-and-migration` — compatibility and rollout/rollback for schema/system migration.
- `verification-before-completion` — pre/post evidence for data changes.

If no existing data skill fits the actual engine/domain, discover a better skill or use current canonical sources. Never force PostgreSQL guidance onto an unrelated database because it happens to be the nearest pack entry.

---

## product

**Use for:** product discovery, ambiguous feature decisions, requirements, specifications, prioritization and product/technical trade-offs.

**Skills in this pack:**

- `interview-me` — unresolved material user/product decisions after discoverable facts have been inspected.
- `idea-refine` — explore and refine an early concept before committing to one shape.
- `spec-driven-development` — explicit requirements, scope and acceptance criteria.
- `planning-and-task-breakdown` — turn a decided outcome into executable units when useful.
- `documentation-and-adrs` — preserve durable product/architecture decisions.
- `doubt-driven-development` — challenge high-impact assumptions and alternatives.
- `reference-intelligence` — market/product/comparable evidence materially affects the decision.
- `architect-orchestrator` — broad product + technical decomposition or multi-stage ownership.
- `marketing-and-growth` — product positioning/growth concerns are genuinely part of the decision.

---

## marketing

**Use for:** ICP/customer research, positioning, copy, campaigns, content strategy, email, CRO, launch planning and marketing operations.

**Skills in this pack:**

- `marketing-and-growth` — main marketing operating skill. Its references contain the distilled large marketing-prompt corpus, SEO/growth loop and launch/content system.
- `shipping-and-launch` — launch/distribution readiness and operational launch checks.
- `anti-ai-slop-writing` — remove generic/robotic marketing prose and preserve brand voice.
- `reference-intelligence` — current competitor/market/launch evidence and source provenance.
- `source-driven-development` — current platform/API/policy behavior when it affects execution.
- `doubt-driven-development` — challenge high-impact strategy, claims or unsupported assumptions.
- `context-engineering` — large customer/competitor/content evidence sets.
- `documentation-and-adrs` — durable campaign/positioning decisions when worth preserving.

---

## seo

**Use for:** technical SEO, search opportunity discovery, schema, search/content gaps, indexability and measurable organic-growth loops.

**Skills in this pack:**

- `marketing-and-growth` — load its `references/seo-growth-loop.md` when that procedure is useful.
- `source-driven-development` — current search engine, structured-data and platform documentation.
- `context-engineering` — large GSC/site/query/competitor evidence sets.
- `reference-intelligence` — current competitor/search evidence, authority classification and provenance.
- `performance-optimization` — Core Web Vitals/performance when measured evidence points there.
- `browser-testing-with-devtools` — rendered/indexability/runtime checks.
- `doubt-driven-development` — risky canonicals, migrations, programmatic SEO or large-scale changes.
- `verification-before-completion` — evidence that technical changes actually landed and behave as expected.

---

## research

**Use for:** factual or technical research, reports, unfamiliar domains, source-heavy synthesis and current-domain investigations.

**Skills in this pack:**

- `source-driven-development` — establish authoritative/canonical source hierarchy and verify current contracts.
- `reference-intelligence` — decide curated vs live sources, distinguish source roles and preserve provenance.
- `context-engineering` — manage large source/context sets without flooding the synthesis model.
- `verification-before-completion` — evidence-backed final claims.
- `doubt-driven-development` — adversarial source/assumption review.
- `architect-orchestrator` — parallel independent research branches and synthesis when that actually helps.
- `documentation-and-adrs` — preserve durable research decisions/knowledge when relevant to a project.

For current legal, tax, regulatory, medical, financial or other domain-specific work, Agentit does **not** need a permanent domain pack first. Use live authoritative domain sources whenever correctness depends on them.

---

## writing

**Use for:** documentation, technical prose, reports, explanations and externally visible written material.

**Skills in this pack:**

- `anti-ai-slop-writing` — remove generic, repetitive or robotic prose.
- `documentation-and-adrs` — durable technical/project documentation and decision records.
- `source-driven-development` — factual/current source-grounded writing.
- `reference-intelligence` — multi-source reports, source roles and provenance.
- `doubt-driven-development` — adversarial factual/argument review when stakes warrant it.
- `context-engineering` — large source sets or long documents.
- `verification-before-completion` — evidence before factual completion claims.

---

## release

**Use for:** CI/CD, deployments, migrations, launches, operational readiness and rollback planning.

**Skills in this pack:**

- `shipping-and-launch` — release readiness, launch checks and rollback thinking.
- `ci-cd-and-automation` — pipeline automation and quality gates.
- `verification-before-completion` — fresh release evidence.
- `verification-gauntlet` — multiple release verification surfaces when useful.
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

- `git-workflow-and-versioning` — reviewable repository handoff.
- `incremental-implementation` — bounded client delivery and staged implementation.
- `documentation-and-adrs` — durable client/project handoff context.
- `shipping-and-launch` — deployment/launch readiness.
- `architect-orchestrator` — multi-domain client programs when orchestration is useful.
- `specialist-agent-routing` — cleanly separated workers when specialization/parallelism pays off.
- `reference-intelligence` — competitor, market, design or source-heavy client work.
- `marketing-and-growth` — marketing/growth delivery.
- `verification-before-completion` — prove client-facing changes before claiming completion.

---

## Cross-cutting rules

- A skill may appear in multiple packs. Packs are **views over capabilities**, not ownership boundaries.
- Pack order does not imply priority.
- Skill order inside a pack does not imply priority or execution sequence.
- There are no hidden pack levels or recommended counts.
- The primary AI may inspect multiple packs and choose any justified subset.
- General Agentit procedures are provider/model-neutral; provider-specific details belong only where the real integration/source requires them.
- `reference-intelligence` is JIT, not global. Load it when source/provenance judgment is material.
- `mcp-tooling-fit` is JIT when external tool/MCP selection itself needs judgment.
- `security-and-hardening` is JIT when a real security/trust boundary exists, not for every code edit.
- `architect-orchestrator` / `specialist-agent-routing` are JIT when orchestration/delegation actually helps.
- `long-horizon-recovery` is JIT for long/resumable work.
- The base Agentit protocol still requires appropriate verification even when no dedicated verification skill body is selected.

## Missing pack or skill

If no pack covers the domain well:

1. do not force the nearest unrelated pack;
2. use current authoritative sources for the domain when needed;
3. inspect project-local skills;
4. use `find-skills` / approved skill discovery if a reusable specialist procedure would materially help;
5. create/adapt a new skill only when the procedure is durable and likely to recur.

> **Packs are a map, not a prison. The model decides the route and how much knowledge it needs.**
