# Reference-first component scouting

Use this reference when a frontend task needs a UI pattern, component, interaction, or motion treatment that the project does not already solve well.

The goal is not to assemble a collage of fashionable libraries. The goal is to let the agent work like a strong frontend engineer with good references: inspect proven patterns, understand why they work, then adapt the smallest useful idea into the project's own system.

## Core rule

**Reference, do not collage.**

Prefer this order:

```text
need
-> inspect existing project components/design tokens
-> identify the missing pattern
-> inspect a small set of relevant references
-> shortlist candidates
-> verify code/license/dependencies/accessibility/responsiveness
-> choose one implementation family
-> adapt to project tokens and brand
-> integrate
-> verify in the browser
```

Do not mix several unrelated component languages just because each individual example looks polished. One surface should still feel like one product.

## Curated discovery sources

These are discovery/reference candidates, not mandatory dependencies and not evidence that a component is suitable for every project. Re-verify live details before depending on code, licenses, APIs, install commands, or package compatibility.

### Foundations and production primitives

- `https://ui.shadcn.com` — broad React component foundation and registry; useful when the project already fits the shadcn/Radix ecosystem.
- `https://coss.com/ui` — component references and primitives; inspect compatibility, ownership and dependency fit before adoption.
- `https://reui.io/components` — component/block references, especially useful for agent-driven implementation discovery.

### Distinctive component patterns

- `https://beautifului.dev` — polished interface patterns, especially useful for AI-native product surfaces and richer states.
- `https://beui.dev` — animated/component references when a stronger visual treatment is justified.
- `https://rareui.com` — more expressive component references; use selectively rather than importing a whole visual language.

### Motion and interaction

- `https://transitions.dev` — focused transition and interaction patterns. Extract the motion principle instead of copying animation everywhere.
- `https://emilkowal.ski/ui/you-dont-need-animations` — restraint reference: motion should earn its place and frequent product interactions should remain fast and legible.

### Design-system and quality checks

- `https://designsystemchecklist.com` — audit/reference input for design-system completeness; it does not replace WCAG, project requirements, or rendered QA.
- `https://ui-skills.com` — discovery surface for focused UI/frontend skills. Treat individual skills as candidates that still require source, license and project-fit review.

## Scouting workload

Keep the pass proportional to the missing decision.

For a normal component need:

1. Inspect the existing project's component system first.
2. Define the missing behavior in one sentence.
3. Inspect 2–5 relevant candidates, not every catalog.
4. Prefer candidates whose implementation family already matches the project.
5. Compare behavior, states, accessibility, responsive behavior and dependency cost—not screenshots alone.
6. Select one base/pattern or decide to build locally.
7. Record the principle that is being adapted and what will change to fit the project.

For a large redesign or greenfield public site, component scouting is subordinate to the broader design direction. Do not let a component library dictate the art direction backwards.

## Candidate evaluation

Before adopting or adapting external component code, check:

- **Project fit** — does it solve the actual interaction/content problem?
- **System fit** — does it align with the existing framework, primitives and component ownership?
- **License** — can the code legally be used and redistributed in this project?
- **Dependencies** — are new packages justified, maintained and compatible?
- **Accessibility** — keyboard, focus, semantics, contrast and reduced-motion behavior where relevant.
- **Responsive behavior** — does the pattern recompute well across breakpoints instead of merely shrinking?
- **Performance** — animation/runtime cost, bundle impact, layout stability and asset cost.
- **State completeness** — default, hover/focus/pressed where applicable, disabled, loading, error/success when semantically real.
- **Brand adaptation** — typography, spacing, radii, color, iconography, motion and content must become part of the project's system rather than preserving the catalog's demo identity.

## Decision outcomes

A discovered component should end in one of these outcomes:

- `ADOPT` — use substantially as provided because license/system/quality fit is already strong.
- `ADAPT` — use the implementation as a base but restyle/restructure it to project rules.
- `COMPOSE` — combine local primitives to reproduce the useful interaction pattern without importing the component.
- `REFERENCE` — take only the design/interaction principle.
- `BUILD` — implement locally because external candidates add more cost than value.
- `REJECT` — do not use because of license, accessibility, dependency, performance or design-system mismatch.

Discovery is not adoption.

## Anti-Frankenstein gate

Before integrating, answer:

1. What is the primary design/component foundation for this surface?
2. Which external source, if any, is supplying a missing pattern?
3. Can the result be made coherent using the project's existing tokens and primitives?
4. Would a user perceive one design system or several unrelated demos stitched together?

If the answer to #4 is "several", stop and simplify.

Bad pattern:

```text
shadcn button
+ unrelated animated navbar
+ different-library modal
+ flashy transition pack
+ third visual language for cards
= demo collage
```

Good pattern:

```text
existing project foundation
+ one reference-derived interaction
+ project tokens
+ project content
+ browser-verified states
= coherent product UI
```

## Implementation handoff

When scouting materially changes implementation, pass forward:

```text
COMPONENT_DECISION
need: <missing UI/interaction>
foundation: <existing project system>
source: <reference URL/source role>
outcome: ADOPT | ADAPT | COMPOSE | REFERENCE | BUILD | REJECT
principle: <what is useful>
adaptation: <how it becomes project-specific>
dependencies: <new/none>
license_status: <verified/needs verification>
a11y_notes: <relevant states/risks>
verification: <browser/build checks required>
```

If external code materially enters the project, preserve the source/license attribution required by that code and add durable provenance to the project's reference ledger when appropriate.

## Failure modes

- asking the model to invent commodity UI from scratch when a strong compatible reference is available;
- searching catalogs before inspecting the project's own components;
- choosing from screenshots without inspecting behavior/code;
- importing a library for one trivial effect;
- copying demo styling instead of adapting to the brand;
- mixing multiple component languages into one surface;
- assuming copy-paste code is automatically licensed, accessible, responsive or maintained;
- adding motion merely because a motion reference exists;
- turning this curated source list into an always-loaded context bundle.
