---
name: impeccable-design
description: Craft-first frontend design direction adapted from Impeccable. Use to design, redesign, critique, polish, harden, simplify, typeset, animate, adapt, or push a frontend beyond safe AI defaults across marketing sites and product UI.
license: Apache-2.0
source: https://github.com/pbakaus/impeccable
---

# Impeccable Design

Agentit adaptation of Paul Bakaus' Apache-2.0 Impeccable project. This is the **craft director** layer: production-grade code, a clear visual point of view, deep respect for user needs, and enough ambition that the result does not collapse into generic AI UI.

The brief wins. Never redirect a pinned aesthetic, material, era, font, palette, platform convention, or brand system toward your own favorite style.

## Four surface modes

Classify the surface before designing it:

- **Persuade** — landing pages, campaigns, pricing, marketing. Attention and action matter; visual expression may be high.
- **Operate** — apps, dashboards, settings, editors, admin. Repeated use, scanability, speed, consistency, and native expectations dominate.
- **Read** — docs, articles, guides, changelogs. Comprehension and reading rhythm dominate.
- **Experience** — portfolios, showcases, galleries, experimental storytelling. The work itself leads and the interface can recede.

A product's category does not decide the mode; the current surface does. A developer tool landing page is Persuade. Its editor is Operate. Its docs are Read.

## New work vs refinement

**Refinement preserves. Redesign replaces.**

A refinement keeps the incumbent identity, behavior, content truth, and information architecture unless the user asks otherwise. A redesign preserves product truth, function, constraints, and brand facts but is allowed to replace the visual world instead of splitting the difference with the old one.

Before changing an existing interface, inspect at least one source of visual truth: tokens, theme, CSS, component primitives, brand assets, or an existing Figma system.

## Design direction pass

Before code, establish a compact design direction containing:

1. surface mode;
2. audience and job-to-be-done;
3. one visual thesis — the memorable idea the whole interface serves;
4. type system and hierarchy;
5. color/material system;
6. spacing/grid rhythm;
7. motion role;
8. what existing truth must be preserved;
9. explicit anti-goals / clichés to avoid.

Do not generate five aesthetic options unless the task is explicitly exploratory. Pick a direction and make it coherent.

## Craft floor

### Composition

- Every screen needs hierarchy that is legible at a glance.
- Prefer a deliberate dominant element over a democracy of equally loud cards.
- Alignment, optical balance, whitespace, and rhythm matter more than adding decoration.
- Use asymmetry when it supports the visual thesis, not to prove the layout is “creative.”
- Break the grid with intent; preserve readable anchors so the user never loses orientation.
- Avoid repeating the same component silhouette down the entire page.

### Typography

Typography is architecture, not a final styling pass.

- Choose type for brand voice and reading conditions, not because it is fashionable.
- Use a small, disciplined scale with clear display/body/meta roles.
- Control measure, leading, tracking, weight, optical size, and line breaks deliberately.
- Avoid generic “big gradient headline + tiny gray paragraph” hierarchy.
- Do not inject a random serif/italic word into a sans headline merely to manufacture taste.
- Test long strings, localization expansion, and narrow widths.

### Color and material

- Start from semantic roles: canvas, surface, elevated surface, text, muted text, border, accent, destructive, success, focus.
- One strong accent system usually beats a collection of unrelated saturated colors.
- Glow, glass, blur, noise, gradients, chromatic aberration, and grain are materials with costs; use them because the concept asks for them.
- Maintain contrast and legibility in every actual state, not just the hero screenshot.

### Spatial system

- Establish spacing increments and use them consistently enough that exceptions feel authored.
- Match radius and border language to the product's character.
- Keep related controls spatially grouped and unrelated groups visibly separated.
- Avoid “cardification”: not every idea needs its own rounded rectangle.

### Interaction

- Visible affordances must behave as they look.
- Hover cannot be the only carrier of critical information.
- Focus-visible treatment is designed, not merely technically present.
- Loading, empty, failure, disabled, destructive confirmation, and success states are part of the surface.
- Avoid clever gestures with no discoverable fallback.

### Responsive design

Do not shrink the desktop composition. Recompose it.

- Preserve hierarchy and narrative while changing layout strategy.
- Simplify or replace expensive/fragile effects on touch devices.
- Design nav, type measure, media crops, sticky regions, and interaction targets independently for mobile.
- Verify at least one narrow and one wide viewport.

## Commands / intents

Treat the following words as useful intent labels, even if the user never types the exact command:

- **shape** — plan UX/UI and concept before coding;
- **critique** — identify hierarchy, UX, coherence, and craft failures;
- **audit** — a11y, responsiveness, performance, states, technical quality;
- **polish** — final bounded craft pass;
- **bolder** — increase distinctiveness and visual conviction without adding random decoration;
- **quieter** — reduce noise while preserving identity;
- **distill** — remove complexity and expose the essential structure;
- **harden** — make edge cases, errors, i18n, loading, and responsive behavior production-ready;
- **animate** — add purposeful motion;
- **typeset** — fix typography and reading hierarchy;
- **layout** — fix spatial rhythm and composition;
- **delight** — add memorable details at moments that can afford them;
- **overdrive** — pursue technically ambitious craft when the brief explicitly rewards spectacle;
- **adapt** — redesign for different viewports/input modes;
- **optimize** — remove visual/runtime performance bottlenecks.

## Bounded visual QA

Do not endlessly polish. Build the coherent direction first, then perform a bounded visual QA cycle:

1. inspect desktop and mobile together;
2. batch the defects by hierarchy/layout/type/color/motion/state/a11y/performance;
3. fix them in one pass;
4. confirm once more if browser tooling is available;
5. stop when the acceptance criteria and craft floor are satisfied.

The goal is not fewer tokens; it is avoiding aimless local tweaks after the concept should already be coherent.

## Integration with Agentit

- Pair with `design-taste-frontend` for art direction and anti-default discipline.
- Pair with `emil-design-eng` for interaction details and motion feel.
- Pair with `figma-design-workflow` when a Figma source or design system exists.
- Pair with `scrollytelling-web` for cinematic scroll narratives.
- Pair with `browser-testing-with-devtools` for rendered verification.
- On high-motion work, use `gsap-scrolltrigger` + `gsap-performance` rather than hand-rolling fragile scroll listeners.

## Attribution / modification notice

This file is an Agentit-specific adaptation inspired by and derived from Impeccable by Paul Bakaus (Apache License 2.0). It has been substantially reorganized and modified for Agentit's provider-neutral skill model; it does not reproduce Impeccable's CLI/scripts or claim compatibility with its command runtime.
