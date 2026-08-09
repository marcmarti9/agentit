---
name: design-taste-frontend
description: Full-fat art direction for landing pages, portfolios, marketing sites, visual redesigns, and expressive frontend work. Reads the brief, selects a coherent visual world, fights AI defaults, and drives typography, composition, imagery, motion, and production craft. Quality is prioritized over token minimization.
license: MIT
source: https://github.com/Leonxlnx/taste-skill
---

# Design Taste Frontend — Full Craft Mode

This is Agentit's quality-first adaptation of Leonxlnx's MIT-licensed Taste Skill. The previous Agentit version intentionally compressed the upstream methodology to save context. **That constraint is removed for design work.** Load and use the depth required to make the interface excellent.

Scope: marketing sites, landing pages, portfolios, showcases, editorial surfaces, creative frontend, and visual redesigns. Product UI can use this for art direction, but `impeccable-design` + `emil-design-eng` own repeated-use interaction craft.

Every rule is contextual. The brief and existing brand truth win.

## 0. Read the room before touching code

Infer:

1. **Surface kind** — SaaS landing, consumer product, agency, portfolio, editorial, event, product UI, redesign.
2. **Audience** — technical buyer, mainstream consumer, recruiter, creator, existing power user, regulated/public audience.
3. **Vibe words** — minimal, warm, technical, editorial, brutalist, cinematic, luxury, playful, utilitarian, Apple-like, industrial, etc.
4. **References** — URLs, screenshots, Figma files, competitors, named products/studios.
5. **Existing truth** — logo, type, palette, design tokens, product screenshots, photography, UI components, Figma systems.
6. **Constraints** — accessibility, brand rules, performance, platform, content volume, regulated/trust-first context.

State one compact design read before implementation:

> Reading this as: **<surface>** for **<audience>**, with a **<visual language>**, centered on **<one visual thesis>**.

Ask at most one design-direction question only when two materially different interpretations remain. Otherwise commit to a direction.

## 1. Anti-default discipline

Never autopilot into the recurrent AI bundle:

- purple/blue glow because “tech”;
- centered hero over a dark radial mesh;
- logo cloud → three equal cards → testimonials → CTA;
- generic glass cards on every section;
- Inter + slate palette regardless of brand;
- random gradient text;
- giant rounded rectangles wrapping everything;
- fake product screenshots built from decorative `div`s;
- endless floating blobs/marquees;
- every section using an eyebrow label;
- serif/italic accent word inserted only to look premium;
- motion attached to everything because the user asked for “animations.”

A familiar structure is allowed when it is actually right. The failure is unexamined defaulting.

## 2. Set design dials

Use three explicit dials to keep decisions coherent:

- `DESIGN_VARIANCE` 1–10 — strict/systematic → asymmetric/experimental.
- `MOTION_INTENSITY` 1–10 — static → cinematic/physics/scrollytelling.
- `VISUAL_DENSITY` 1–10 — gallery-airy → cockpit-dense.

Typical starting points:

| Read | Variance | Motion | Density |
| --- | ---: | ---: | ---: |
| Calm B2B / Linear-like | 5–6 | 3–4 | 3–5 |
| Premium consumer | 7–8 | 5–7 | 3–4 |
| Creative agency / Awwwards | 9–10 | 8–10 | 3–4 |
| Developer portfolio | 6–8 | 5–7 | 3–4 |
| Editorial | 6–8 | 3–6 | 2–4 |
| Public / regulated | 3–4 | 1–3 | 4–6 |

The user can override these conversationally. Do not make them edit a skill file.

## 3. Choose the foundation honestly

When the product clearly belongs to an existing design-system ecosystem, prefer the official system rather than reimplementing it cosmetically: Fluent, Material, Carbon, Polaris, Atlaskit, Primer, GOV.UK, USWDS, Radix, etc.

For owned SaaS/product surfaces, shadcn/Radix or an existing internal system can be a foundation, but never ship the library's default visual state as the final brand.

For expressive marketing/editorial work, native CSS/Tailwind plus carefully selected primitives is often better than forcing a product design system onto the page.

**One system per surface.** Do not mix component languages casually.

Verify dependencies before importing them.

## 4. One visual thesis

Exceptional pages usually have a dominant idea that everything else supports. Examples:

- the product physically decomposes as the story explains each subsystem;
- typography behaves like an editorial poster system;
- the product UI itself becomes the hero canvas;
- a photographic crop system creates a recognizable rhythm;
- a single material metaphor (paper, machined aluminum, translucent polymer, terminal, blueprint) drives the interface.

Write the thesis in one sentence. If a visual decision does not support it, the default answer is to remove it.

## 5. Composition

### Hero

The first viewport must establish identity and meaning immediately. A strong hero is not synonymous with centered copy.

Choose composition from the content:

- split product + statement;
- editorial oversized type;
- edge-to-edge artifact;
- asymmetric product stage;
- cinematic scene;
- dense proof/utility hero for technical products;
- quiet premium composition with strong negative space.

The primary action should be discoverable without hunting. Do not hide all useful information below a theatrical empty viewport.

### Section rhythm

Alternate structural modes deliberately. Avoid a page made from the same 3-column card component twelve times.

Use contrast in scale: full-bleed moments, narrow reading columns, artifact-led sections, dense evidence, quiet whitespace, sticky/scrollytelling stages.

Do not zigzag purely for variety; build rhythm around the story.

### Grid

Use a real alignment system even when the result feels freeform. Experimental layouts still need anchors. Break the grid locally, not accidentally.

## 6. Typography

Typography carries more identity than most decoration.

- Pick typefaces appropriate to the brand and content.
- Defaulting to Inter is not neutral when every generated site does it.
- A display face needs a reason and must still survive real content.
- Establish display/body/meta roles and a disciplined scale.
- Tune line-height, tracking, line breaks, measure, and weight.
- Avoid overly narrow body measure and giant display text that wraps into accidental four-line slogans.
- Same-family italic/bold emphasis is usually stronger than injecting a second random font.
- Serif is a design choice, not a universal premium switch.
- Test descenders/italics and clipping at actual line heights.

Use self-hosted/`next/font`/project-approved font delivery rather than casually adding blocking external font requests.

## 7. Color and material

Start with roles and hierarchy, then effects.

- Neutral canvas + one decisive accent often beats five accent families.
- Build enough tonal steps for text/surfaces/states instead of using opacity hacks everywhere.
- Treat gradients, glass, blur, noise, grain, scanlines, chrome, bloom, and shadows as materials with a conceptual and performance cost.
- Lock the page into a coherent light/dark/material world unless a deliberate narrative transition justifies a change.
- Meet contrast requirements in real component states.

## 8. Imagery and artifacts

Real imagery wins over fake placeholders when imagery is central to the concept.

- Use actual product screenshots, photos, illustrations, diagrams, video, or 3D assets when available.
- Preserve crop/focal point intentionally across responsive breakpoints.
- Do not fabricate screenshots out of nested generic cards and call them product imagery.
- If the asset is missing, use an explicit asset slot and design around the truth of what exists.

If Figma is the source, use `figma-design-workflow` rather than manually approximating frame measurements.

## 9. Motion direction

Motion is part of the design read, not an afterthought.

At low motion intensity, use tiny state transitions and restrained entrances. At medium intensity, use purposeful section reveals, product transitions, and spatial continuity. At high intensity, consider cinematic storytelling, pinned scenes, kinetic type, image sequences, or real 3D — but only if they support the thesis.

For repeated product UI, defer to `emil-design-eng`: frequent actions should be fast and often static.

For high-intensity landing pages, route to:

- `scrollytelling-web` for narrative architecture;
- `gsap-scrolltrigger` for pinned/scrubbed mechanics;
- `gsap-performance` for runtime discipline;
- `threejs-product-storytelling` for genuine product 3D.

Honor `prefers-reduced-motion` with a meaningful alternate composition.

## 10. Scrollytelling design rules

When scroll is the timeline:

- every chapter must communicate something;
- movement should resolve into readable holds;
- pinned stages need designed start/end handoffs;
- visual hierarchy still applies during intermediate frames;
- reverse scroll must remain coherent;
- mobile may use a different storytelling strategy;
- never stretch 10 seconds of visual content into a minute of scroll merely to feel cinematic.

A product explosion should reflect conceptual assemblies, not random particles flying apart.

## 11. Redesign audit

Before redesigning an existing public-facing page, inventory:

- what is recognizable/valuable in the current identity;
- what is fact/content/function and must survive;
- design tokens/assets worth preserving;
- hierarchy problems;
- structural repetition;
- type/color/material problems;
- interaction/motion problems;
- credibility/trust signals;
- responsive failures;
- accessibility/performance constraints.

Then explicitly decide **preserve**, **evolve**, or **replace** the visual world. Do not produce a timid half-redesign by accident.

## 12. Anti-slop production checks

Before completion:

- [ ] Design read and one visual thesis are explicit.
- [ ] Dial values match the actual implementation.
- [ ] The page does not depend on unprompted AI clichés.
- [ ] Typography, spacing, color, radii, iconography, and imagery form one system.
- [ ] Responsive layout is recomposed, not simply shrunk.
- [ ] Interactive states are complete where relevant.
- [ ] Motion has purpose and reduced-motion behavior.
- [ ] High-motion pages have been tested through the complete sequence.
- [ ] No fake screenshots/assets are presented as real product visuals.
- [ ] Accessibility and performance are part of the final design, not TODOs.
- [ ] Browser evidence exists before visual-success claims when browser tooling is available.

## 13. Quality-first pairing

For serious design work Agentit should normally combine this skill with:

- `impeccable-design` — design-director craft floor and critique;
- `emil-design-eng` — interaction/motion precision;
- `frontend-ui-engineering` — production frontend/a11y;
- `browser-testing-with-devtools` — rendered evidence;
- `figma-design-workflow` — when Figma is relevant.

Then add specialist motion/3D skills when the brief signals them.

## Attribution / modification note

Based on and substantially reworked from Leonxlnx's MIT-licensed `taste-skill`. This Agentit version deliberately restores a deep, quality-first art-direction layer and adds Agentit-specific routing, Figma, scrollytelling, verification, and specialist-skill integration. Preserve attribution when redistributing substantial portions.
