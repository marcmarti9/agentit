---
name: design-inspiration-research
description: Research current visual and interaction references before public greenfield or total-redesign art direction; extract design DNA, synthesize original directions, and keep provenance traceable.
---

# Design Inspiration Research

Research exists to change design decisions, not to produce a link dump.

This skill works with `reference-intelligence`. Hallmark's MIT-licensed `study` discipline materially informed the explicit **design-DNA** extraction below; Agentit keeps its own research/orchestration model and does not vendor Hallmark wholesale.

For premium/Studio public web work, also read `references/premium-web-production.md`. That file distills the useful production workflow from the bookmarked “$10k website” / cinematic-web articles; quoted price claims are deliberately not treated as evidence.

When a frontend task needs a missing component, interaction, or motion pattern, use `references/component-reference-scouting.md` as a JIT discovery map. It keeps the project system as the foundation while letting the agent inspect strong external component references before inventing commodity UI from scratch.

## Required by default

Run this pass before art direction/code for:

- greenfield public websites, landings, homepages, portfolios and storefronts;
- total visual redesigns;
- ambitious Polished/Studio public visual work;
- work where originality or current visual context matters.

Skip only when the user explicitly opts out, current-source tooling is unavailable, or the surface is routine repeated-use product UI where references add no material decision. If current research is unavailable, say so instead of presenting memory as live research.

## Research workload

When current web/browser tooling is available:

1. Search 4–8 distinct queries that describe the desired **experience**, not only the industry.
2. Inspect promising pages/interactions rather than relying on thumbnails.
3. Collect 6–12 useful references, then stop.
4. Mix real brands/products, strong studios/showcases and adjacent disciplines such as editorial, architecture, industrial design, fashion, photography, film titles, games, museums or retail when useful.
5. Studio work should normally include cross-domain references, not just competitors.
6. Cluster observations into 2–4 patterns and identify what has become cliché.
7. Synthesize 2–3 original project-specific directions from multiple principles.

When Agentit's curated references already contain a useful source or playbook, start there but re-verify live/current details when the decision depends on them. Curated references are accelerators, not an exhaustive knowledge base. Do not load every stored reference simply because it exists.

## Component/reference scouting

For a missing frontend pattern, do not jump directly from prompt to invented markup. Use this smaller loop:

```text
need
-> inspect existing project components/design tokens
-> identify the missing behavior
-> inspect a small set of relevant reference/component sources
-> shortlist candidates
-> verify code/license/dependencies/accessibility/responsiveness
-> choose one implementation family
-> adapt to project tokens and brand
-> integrate
-> verify in the browser
```

Load `references/component-reference-scouting.md` when this loop is material. Its curated sources include component foundations, expressive component catalogs, motion references, and design-system QA inputs. They are discovery candidates, never mandatory dependencies.

**Reference, do not collage.** Keep one primary component/design foundation per surface. External sources should supply a missing pattern or principle, not turn the product into several unrelated demos stitched together.

Prefer `ADOPT | ADAPT | COMPOSE | REFERENCE | BUILD | REJECT` as explicit outcomes for discovered components. Discovery is not adoption.

## Design-DNA extraction

For each useful reference, extract **dimensions**, not pixels. Keep only signals that may change the project:

- macrostructure and section rhythm;
- first-impression hook and hierarchy;
- composition/grid/scale/whitespace/depth;
- component or interaction archetypes;
- typography roles/pairing/measure;
- color anchor, tonal system and material language;
- imagery/crop/artifact strategy;
- interaction and motion grammar;
- narrative/reveal pacing;
- responsive behavior worth preserving conceptually;
- likely implementation family;
- why the principle fits this project;
- what should **not** be copied.

For an inspectable URL, exact CSS facts such as a font family or color value may be observable. That still does not make the source a template to clone. For a screenshot, infer the visual relationship rather than pretending to know invisible implementation details.

## Structural variety gate

A redesign is not original merely because the palette changed. Before selecting a direction, compare the **structure** of candidate references and the proposed page:

- hero archetype;
- section order/rhythm;
- repeated card/grid patterns;
- placement of proof and artifacts;
- CTA cadence;
- navigation/footer voice;
- motion/storytelling stages.

If the proposal is still `centered hero -> logo row -> three equal cards -> testimonials -> CTA` with cosmetic changes, the research has not done enough work.

## Truth and ownership boundaries

Reference research never grants permission to fabricate proof or reproduce protected expression.

- Do not invent metrics, testimonials, customer logos, traction, awards, or product screenshots to make a reference-derived layout work.
- Do not copy proprietary copy, brand assets, illustrations, photos, or a distinctive page wholesale.
- Preserve the target project's routes/component ownership/content truth during a redesign unless a rebuild or deletion plan is explicitly approved.
- Reusable code/components discovered through a reference still require dependency, license, accessibility, and project-fit review.

## Required deliverables

### INSPIRATION_SYNTHESIS

Include strongest reference signals, 2–4 pattern clusters, cliché radar, 2–3 original directions and implementation implications.

### REFERENCE_TO_DECISION_MAP

Map candidate/chosen decisions back to observed principles and state the project-specific adaptation:

- typography;
- composition and section rhythm;
- imagery/crop strategy;
- material/color;
- motion/interaction;
- narrative, proof and CTA presentation.

For every material source state its role (`inspiration`, `canonical`, `licensed artifact`, etc.) so a gallery reference never masquerades as factual/business evidence.

Do not claim a reference influenced the design when the effect cannot be explained. Do not copy distinctive brand assets/content/layouts.

### PROJECT PROVENANCE

When references materially shape the final direction, update the project's canonical reference ledger (normally `docs/agentit/REFERENCES.md`) with:

`source -> extracted principle -> project decision -> affected paths -> verification date`

Only durable influences belong there; do not dump the research browsing history.

## Implementation handoff

Feed `INSPIRATION_SYNTHESIS` and `REFERENCE_TO_DECISION_MAP` into `design-taste-frontend` and `impeccable-design` **before implementation**. The selected `DESIGN_DIRECTION` should cite the principles that shaped it.

Before inventing commodity UI primitives, inspect the project's own component system first. When a missing pattern justifies external scouting, use `references/component-reference-scouting.md`, inspect a small set of candidates, choose an explicit adoption outcome, and adapt the result to project tokens/accessibility instead of shipping catalog demo styling unchanged.

If the final design would plausibly look the same without this research, the research failed. Extract stronger principles or explicitly state that the references did not improve the direction.

## QA handoff

After implementation, use rendered/browser evidence plus the project's design/accessibility skills. Flow-specific external checklists such as Checklist Design may seed acceptance criteria for the relevant screen/flow, but they do not replace WCAG, project requirements, interaction judgment, or actual browser verification.

For interactive components, verify the states that materially exist in the product—normally default, hover where applicable, focus-visible, active/pressed, disabled, loading, error and success where semantics support them. Do not invent meaningless states merely to fill a checklist.

## Parallel research

Reference research is a strong delegation boundary because it is read-only and context-heavy. Independent workers may explore different lenses such as category peers, adjacent visual disciplines, motion/interaction and technical feasibility. The Architect synthesizes their bounded receipts and chooses the final direction.

## Failure modes

- link dump with no synthesis;
- copying one fashionable site;
- treating a creator's business claim as evidence because its design is attractive;
- forcing every trendy technique into one page;
- doing research only after the visual direction is already fixed;
- inventing commodity UI before checking compatible references when a reference pass would materially help;
- installing a component/tool before checking project primitives and license/dependency fit;
- mixing unrelated component languages into one surface;
- invisible research with no traceable impact on design;
- final design influenced by external work with no project provenance record.
