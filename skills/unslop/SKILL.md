---
name: unslop
description: "Remediate an existing UI that looks AI-generated through a located anti-slop audit, product-specific direction, and visual redline passes. Select for explicit 'unslop'/de-vibecode requests or repetitive generic UI chrome; not for prose rewriting, greenfield UI design, or read-only critique."
license: CC-BY-4.0
metadata:
  upstream: heydamir/unslop
  author: Damir Sokolovsky
---

# Unslop: product-specific visual remediation

Source-informed adaptation of [Unslop](https://github.com/heydamir/unslop) by Damir Sokolovsky (@heydamir), inspected at `4652254daff586ff4739849395a127b56f7f8cc7`, CC BY 4.0. This Agentit adaptation is shorter, provider-neutral and does not include the upstream scripts, media examples or runtime. Preserve attribution when redistributing. See `THIRD_PARTY_NOTICES.md`.

## Ownership and boundaries

Use for an **existing** dashboard, app screen or landing page whose visual presentation has recognisable generated-template patterns and the user wants them removed **in the implementation**. It owns a bounded *visual redline plus repair* workflow, not a new product design process. For a read-only critique, select `design-critique`; for greenfield design or broad art direction choose a primary owner such as `impeccable`, `hallmark` or `design-taste-frontend`; for AI-sounding **prose**, choose `humanizer` or `stop-slop`. Do not stack competing taste owners by default.

Keep actual features, routes, information architecture, section order, accessibility semantics, content truth and brand commitments. User-specified aesthetics, legitimate gradients, expressive effects and existing identity outrank a universal no-gradient rule. Do not remove deliberate design merely because it resembles a trend. Apply Agentit's BUILDER/REVIEW, user permissions and verification contract; this skill never authorises browser installation, paid asset generation, video capture or rewriting live production sites.

## 1. Inspect and diagnose

- Read the binding brief/tokens/components and inspect the real screen at the target viewport and theme; use source-only analysis when rendering is unavailable, clearly labelled as such.
- Record **located** issues (component, region, selector or file), impact and evidence. Look for purposeless glows, saturated gradients across ordinary chrome, decorative emoji badges, repeated card layouts, indiscriminate shadows, uneven spacing, many competing accents, empty hype copy, misleading mock statistics and arbitrary display typography.
- Classify the result: **heavy** (systemic) → full passes; **light** (limited) → fix only found defects, preserve visual identity; **none** → no redesign, report concrete minor suggestions if useful. A pre-existing good design is a successful outcome.

## 2. Establish a direction grounded in the product

Before significant visual changes, write five short lines:
1. **Product:** what it actually does and for whom.
2. **Character:** 2–3 specific qualities based on the audience and task, not empty labels such as modern or premium.
3. **World:** concrete materials/setting/visual language that belong to the product.
4. **Moments:** one or two areas where rich color, imagery or interaction genuinely convey meaning.
5. **Signature:** one recurring detail tied to the product.

Show the audit/direction before editing **only when the user asked to review the direction first** or a consequential product/brand choice remains unresolved. Otherwise proceed within the granted scope; do not introduce a permission-gathering loop for routine reversible changes.

## 3. Repair in nine coherent passes

Do a single scoped pass for each relevant concern, or consolidate code edits while checking the same order:

1. **Spacing:** consistent rhythm, aligned baselines and grouping; replace arbitrary one-off gaps without mechanically forcing every dimension to one grid.
2. **Color:** intentional neutral surfaces, legible role hierarchy and restrained functional accents; preserve meaningful brand color and semantic status indicators.
3. **Icons:** coherent library, size, stroke and alignment; replace decorative emoji only when that improves clarity.
4. **Copy:** specific, verifiable product language; retain factual claims/terms rather than inventing social proof, metrics or benefits.
5. **Type:** clear hierarchy, readable scale, actual brand font/fallbacks and consistent numeric formatting.
6. **Layout:** restore focus and task flow across desktop/mobile, keeping required sections, states and behavior intact.
7. **Details:** coherent borders, radii, keycaps, chart encoding and precise empty/error/loading states; avoid ornamental noise.
8. **Visuals:** show real or truthfully labelled product content, not generic glowing blobs; respect asset licenses and tool permissions. Prefer existing assets before optional generation.
9. **Motion:** keep purposeful feedback; remove purposeless loops and respect reduced-motion settings. No animation is required for a successful cleanup.

Put visual richness where content warrants attention, while keeping ordinary controls calm. Contrast, labels, focus, input behavior, responsive reflow and semantics remain functional requirements, not optional taste.

## 4. Verify and report

- Compare before/after at the **same** viewport, theme and content state. If a runtime is available, inspect mobile and desktop, error states, layout regressions and functional interactions; report tested coverage exactly.
- Revisit every audit item; distinguish fixed, retained-by-brief and unverified. Keep iterations bounded to real defects.
- Summarize the visual direction, changed components/pass, preserved behavior and any remaining risks. Do not claim improved usability or conversion without user evidence.
- Optional progress/story video only when explicitly requested and supported by authorised tools. Inspect scripts before execution, do not auto-install upstream tooling, and do not infer permission for paid imagery.

## Selection checks

- **Positive:** “unslop this existing dashboard”; “remove the generic AI design from our current landing page, keep its content and functionality”.
- **Negative:** “write less AI-sounding marketing prose” → editorial owner; “design a new site from scratch” → greenfield design owner; “critique this screenshot without editing” → read-only critique owner.

**Done** means located baseline issues have documented dispositions, requested visual repairs exist in the authorised artifact, and observed verification is reported with its limits.
