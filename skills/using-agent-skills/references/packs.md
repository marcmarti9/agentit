# Agentit runtime skill packs

Packs are **semantic discovery scopes**, not automatic context bundles.

The parent/primary AI chooses a pack and depth, then selects the smallest concrete skill subset that the stage or worker actually needs. Never inject an entire pack merely because it was selected.

## Depth model

### `essential`

Smallest useful domain vocabulary/process. Default for bounded work. Usually 1–2 concrete skills.

### `standard`

Normal production depth. Adds the common implementation/review skills that materially improve a real task. Usually 2–4 concrete skills total after selection.

### `deep`

Specialist, high-stakes, niche, high-craft or structurally difficult work. Expands the **candidate pool**, not the context payload. Select only the few advanced skills actually needed.

Depth is allowed to increase during execution when evidence shows the current skill set is insufficient. Do not start at `deep` to look impressive.

## Worker projection contract

A spawned worker should receive something conceptually equivalent to:

```text
pack: design
depth: deep
selected_skills:
  - design-inspiration-research
  - scrollytelling-web
  - browser-testing-with-devtools
references:
  - <only relevant curated/live material>
```

`pack` and `depth` explain the domain/context budget. `selected_skills` are the only skill bodies that should be projected unless the worker discovers a concrete missing need and asks/escalates.

## Pack index

### engineering

**Use for:** general implementation, bug fixes, refactors, repository changes and code quality.

**essential candidates**
- `incremental-implementation` — small verifiable slices.
- `debugging-and-error-recovery` — reproduce/localize/fix/guard when something is broken.

**standard candidates**
- `planning-and-task-breakdown` — non-trivial decomposition.
- `test-driven-development` — behavioral proof while implementing.
- `code-review-and-quality` — independent correctness/quality review.
- `code-simplification` — remove unnecessary complexity after correctness.
- `verification-before-completion` / `verification-gauntlet` — evidence before done claims.

**deep candidates**
- `doubt-driven-development` — adversarial review for unfamiliar/high-impact decisions.
- `security-and-hardening` — threat/security-sensitive work.
- `performance-optimization` — measurement-led performance work.
- `source-driven-development` — current external framework/library contract matters.
- `architect-orchestrator` / `specialist-agent-routing` — structural or multi-agent work.

### frontend

**Use for:** application UI implementation, browser behavior, accessibility, frontend performance and maintenance.

**essential candidates**
- `frontend-ui-engineering` — production UI implementation baseline.

**standard candidates**
- `browser-testing-with-devtools` — rendered/runtime verification.
- `performance-optimization` — measured frontend performance work.
- `anti-ai-slop-design` — lightweight visual/brand anti-cliche pass.
- `code-simplification` — keep component architecture lean.

**deep candidates**
- `source-driven-development` — current framework/browser contracts.
- `security-and-hardening` — auth/session/input-sensitive frontend surfaces.
- use the `design` pack as the primary or secondary pack when visual art direction is material.

### design

**Use for:** public websites, landing pages, brand/product visual systems, high-craft UI, motion, scrollytelling and spatial experiences.

**essential candidates**
- `design-taste-frontend` — visual direction and anti-generic design baseline.
- `anti-ai-slop-design` — truthfulness/cliche guard.

**standard candidates**
- `design-inspiration-research` — current references, design DNA and provenance.
- `impeccable-design` — structured critique/polish.
- `browser-testing-with-devtools` — rendered desktop/mobile evidence.
- `frontend-ui-engineering` — implementation/accessibility bridge.
- `figma-design-workflow` — when Figma is a real source/handoff surface.

**deep candidates**
- `ui-ux-pro-max-intelligence` — broader design intelligence when needed.
- `emil-design-eng` — interaction craft/design-engineering judgment.
- `design-trend-researcher` — current visual/interaction landscape.
- `creative-web-experiences` — unconventional interactive web concepts.
- `visual-storytelling-director` — narrative/visual sequencing.
- `creative-tool-scout` — tool choice for unusual creative requirements.
- `delight-and-whimsy` — deliberate delight, not decoration everywhere.
- `scrollytelling-web` — narrative scroll architecture.
- `gsap-scrolltrigger` / `gsap-performance` — advanced timeline/scroll motion.
- `threejs-spatial-experiences` / `threejs-product-storytelling` — real 3D/spatial work.

### backend

**Use for:** APIs, services, integrations, server-side architecture and operational behavior.

**essential candidates**
- `api-and-interface-design` — contracts and boundaries.

**standard candidates**
- `observability-and-instrumentation` — logs/metrics/traces/diagnostics.
- `test-driven-development` — service behavior proof.
- `code-simplification` — avoid accidental service/framework complexity.
- `verification-before-completion` — runtime evidence.

**deep candidates**
- `security-and-hardening` — auth/secrets/PII/trust boundaries.
- `performance-optimization` — measured service/data-path performance.
- `source-driven-development` — external protocols/framework contracts.
- `architect-orchestrator` — structural multi-service changes.

### data

**Use for:** databases, schemas, persistence, migrations and data-heavy application work.

**essential candidates**
- `supabase-postgres-best-practices` — only when PostgreSQL/Supabase context is real.
- `source-driven-development` — current DB/platform contract when applicable.

**standard candidates**
- `test-driven-development` — migration/query/data behavior proof.
- `observability-and-instrumentation` — runtime/data-path diagnostics.
- `security-and-hardening` — access/PII/row-level/security boundaries.

**deep candidates**
- `performance-optimization` — query/storage performance measured first.
- `doubt-driven-development` — destructive/structural migration review.
- `architect-orchestrator` — multi-stage migrations and dependent systems.

If no existing data skill fits the actual engine/domain, discover a better skill or use live canonical sources rather than forcing PostgreSQL guidance onto unrelated databases.

### product

**Use for:** product discovery, ambiguous feature decisions, requirements, specifications and prioritization.

**essential candidates**
- `interview-me` — unresolved user/product decisions.
- `idea-refine` — explore/refine an early concept.

**standard candidates**
- `spec-driven-development` — explicit requirements/acceptance criteria.
- `planning-and-task-breakdown` — executable decomposition.
- `documentation-and-adrs` — durable decisions.

**deep candidates**
- `doubt-driven-development` — challenge high-impact product/architecture assumptions.
- `reference-intelligence` — market/product/reference evidence materially affects the decision.
- `architect-orchestrator` — broad product+technical decomposition.

### marketing

**Use for:** positioning, ICP, copy, campaigns, content strategy, email, CRO and launch planning.

**essential candidates**
- `marketing-and-growth` — main marketing operating skill.

**standard candidates**
- `shipping-and-launch` — launch/distribution readiness.
- `anti-ai-slop-writing` — brand-authentic copy refinement.
- `reference-intelligence` — current market/competitor/launch evidence.

**deep candidates**
- `source-driven-development` — platform/API/policy behavior matters.
- `doubt-driven-development` — high-impact strategy/claim review.
- relevant deep references inside `marketing-and-growth/references/`, especially the marketing operating system and launch content system.

### seo

**Use for:** technical SEO, search opportunity discovery, schema, content/search gaps and measurable organic-growth loops.

**essential candidates**
- `marketing-and-growth` — load its SEO-specific reference `references/seo-growth-loop.md`.

**standard candidates**
- `source-driven-development` — current search/platform/structured-data docs.
- `context-engineering` — large GSC/site/query evidence sets.
- `reference-intelligence` — current competitor/search evidence and provenance.

**deep candidates**
- `performance-optimization` — Core Web Vitals/performance when evidence points there.
- `browser-testing-with-devtools` — rendered/indexability/runtime checks.
- `doubt-driven-development` — risky migrations/canonicals/programmatic SEO/large-scale changes.

### research

**Use for:** factual research, technical research, reports, unfamiliar domains and source-heavy synthesis.

**essential candidates**
- `source-driven-development` — authoritative/canonical source hierarchy.

**standard candidates**
- `reference-intelligence` — contextual source roles, curated vs live, provenance.
- `context-engineering` — large source/context sets.
- `verification-before-completion` — evidence-backed final claims.

**deep candidates**
- `doubt-driven-development` — adversarial source/assumption review.
- `architect-orchestrator` — parallel independent research branches and synthesis.

For current legal, tax, regulatory, medical, financial or other domain-specific work, curated Agentit material is optional; live authoritative domain sources are mandatory when correctness depends on them.

### writing

**Use for:** documentation, technical prose, reports and externally visible written material.

**essential candidates**
- `anti-ai-slop-writing` — remove generic/robotic prose.

**standard candidates**
- `documentation-and-adrs` — durable technical/project documentation.
- `source-driven-development` — factual/current source-grounded writing.

**deep candidates**
- `reference-intelligence` — complex multi-source reports/provenance.
- `doubt-driven-development` — adversarial factual/argument review.

### release

**Use for:** CI/CD, deployments, migrations, launches and operational readiness.

**essential candidates**
- `shipping-and-launch` — release readiness and rollback thinking.

**standard candidates**
- `ci-cd-and-automation` — pipeline automation/gates.
- `verification-before-completion` / `verification-gauntlet` — fresh release evidence.
- `observability-and-instrumentation` — know whether the release is healthy.

**deep candidates**
- `deprecation-and-migration` — compatibility/retirement/migration plans.
- `security-and-hardening` — production/security boundaries.
- `doubt-driven-development` — high-risk rollout review.
- `architect-orchestrator` — multi-stage releases/migrations.

### agency

**Use for:** client delivery workflows combining product/growth/engineering handoffs rather than one technical domain.

**essential candidates**
- choose the actual delivery pack first (`design`, `marketing`, `seo`, `engineering`, etc.).
- `git-workflow-and-versioning` when repository handoff is involved.

**standard candidates**
- `incremental-implementation` — bounded client delivery.
- `documentation-and-adrs` — durable handoff/context.
- `shipping-and-launch` — deployment/launch readiness.

**deep candidates**
- `architect-orchestrator` — multi-domain client program.
- `specialist-agent-routing` — cleanly separated domain workers.
- `reference-intelligence` — competitor/market/design/source-heavy work.

`agency` should rarely be the only semantic pack; it is usually an operating overlay on the actual domain pack.

## Cross-cutting rules

- `reference-intelligence` is **JIT**, not global. Load it when `reference_plan.mode != none` or source/provenance judgment is material.
- `mcp-tooling-fit` is JIT when external tools/MCP selection matters.
- `security-and-hardening` is JIT when there is an actual security/trust boundary, not for every code edit.
- `verification-*` can be loaded at the stage that needs deeper verification discipline; the base Agentit protocol still requires evidence/receipts.
- `architect-orchestrator` and `specialist-agent-routing` are for structural/multi-agent work, not default ceremony.
- `long-horizon-recovery` is for long/resumable work, not every task.

## Missing pack or skill

If no pack covers the domain well:

1. do not force the nearest unrelated pack;
2. use current authoritative sources for the domain when needed;
3. inspect project-local skills;
4. use `find-skills` / approved skill discovery if a reusable specialist procedure would materially help;
5. create/adapt a new skill only when the procedure is durable and likely to recur.

Packs are a map, not a prison.
