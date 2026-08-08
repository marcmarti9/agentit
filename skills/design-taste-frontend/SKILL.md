---
name: design-taste-frontend
description: Ship brand-authentic landing pages, portfolios, and redesigns without AI visual slop. Use for marketing sites, heroes, motion direction, and visual redesigns; not for dense dashboards, data tables, or backend-only work.
---

# Design Taste Frontend

Curated adaptation of [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) (`design-taste-frontend` v2 ideas) for Agentit: progressive disclosure, on-demand profile, no 80k monologue in every turn.

**Scope:** landing pages, portfolios, marketing sections, and visual redesigns.  
**Out of scope:** dense product dashboards, admin tables, multi-step app shells — use `frontend-ui-engineering` there. For a light anti-cliché pass without full design direction, use `anti-ai-slop-design`.

## When to Use

- Greenfield landing / marketing / portfolio UI
- Redesign of an existing public-facing page (audit first)
- User asks for premium / Linear / Awwwards / "not AI-looking" aesthetics
- Motion, typography, spacing, and layout hierarchy matter more than app chrome

## Process

### 1. Design read (before any code)

Infer from brief, vibe words, references, audience, existing brand assets, and hard constraints (a11y, public-sector, regulated).

Output one line:

> Reading this as: **\<page kind\>** for **\<audience\>**, with a **\<vibe\>** language, leaning toward **\<system or aesthetic family\>**.

If the read genuinely diverges, ask **one** clarifying question. Do not dump a questionnaire.

Anti-default: do not auto-pick purple gradients, centered hero + dark mesh, three equal feature cards, Inter + slate-900, or infinite micro-loops.

### 1b. Agent-usable references (no user screenshots)

When the brief is thin, asks for “premium / not AI-looking”, or you need concrete patterns:

1. Open `references/inspiration-sources.md`.
2. Fetch **1–3** sources that match the design read (prefer **Supahero / Minimal or mnmm / shadcn / Fonts In Use**; SaaSpo/Awwwards only if open).
3. Extract **text signals only** (site names, section types, component APIs, font names). Map them to dials and layout choices.
4. Record a short `REFERENCES USED` note (source → decision). Skip sources that 403 / timeout / return empty shells.

Do not wait for the user to paste captures. Do not bulk-fetch the whole list.

### 2. Set three dials

| Dial | Range | Meaning |
|------|-------|---------|
| `DESIGN_VARIANCE` | 1–10 | 1 = strict symmetry · 10 = asymmetric / experimental |
| `MOTION_INTENSITY` | 1–10 | 1 = static · 10 = cinematic / physics |
| `VISUAL_DENSITY` | 1–10 | 1 = gallery airy · 10 = cockpit dense |

**Baseline:** `8 / 6 / 4` for landings. Override from the design read (see `references/dials-and-systems.md`). State the chosen triple before building.

### 3. Foundation

- Prefer an **official design system** when the brief matches one (Fluent, Carbon, Primer, GOV.UK, USWDS, Polaris, shadcn with customization, etc.).
- One system per project. Do not hand-roll a full DS that already exists as a package.
- Stack defaults when no DS fits: project stack first; otherwise React/Next + Tailwind + Motion (`motion/react`) + self-hosted or `next/font` fonts.
- Verify dependencies in `package.json` before importing. Output install commands when missing.

Full map: `references/dials-and-systems.md`.

### 4. Build with hard layout discipline

Load when implementing sections:

- `references/inspiration-sources.md` — agent-fetchable galleries/docs (no screenshots required)
- `references/layout-hard-rules.md` — hero, nav, eyebrows, zigzag/bento, CTAs, theme lock
- `references/ai-tells.md` — production-tested forbidden patterns
- `references/motion-and-a11y.md` — motion motivation, reduced motion, CWV

Redesigns: `references/redesign-audit.md` before visual overhaul.

### 5. Pre-flight (must pass before claiming done)

- [ ] Design read + dial triple stated
- [ ] If references were needed: 1–3 agent-fetchable sources used (or noted as skipped) per `inspiration-sources.md`
- [ ] No banned AI tells from `references/ai-tells.md` without brief override
- [ ] Hero fits first viewport; primary CTA visible without scroll
- [ ] One accent family; one corner-radius system; page theme locked (light **or** dark, not random section flips)
- [ ] Eyebrow count ≤ ceil(sections / 3)
- [ ] Interactive states: hover / focus / active / loading / empty / error where relevant
- [ ] `prefers-reduced-motion` honored when `MOTION_INTENSITY > 3`
- [ ] WCAG AA contrast on text and CTAs
- [ ] Real or clearly labeled image slots — no div-fake product screenshots
- [ ] Copy self-audit: no filler verbs, no broken cute phrases, one CTA intent per label

Browser evidence when visual claims matter: `browser-testing-with-devtools`.

## Rationalizations

| Excuse | Reality |
|--------|---------|
| "Ship the template, polish later" | First visual impression is the product for landings. |
| "Purple is modern" | Unprompted AI-purple is a brand tell. Match the brief. |
| "Three cards are fine" | Equal triple feature cards are the #1 layout cliché. Vary structure. |
| "Motion can wait" | If the dial claims motion, ship working motion or lower the dial. |
| "Dashboard rules apply" | This skill is not for dense app chrome; switch to `frontend-ui-engineering`. |

## Red Flags

- Design read missing or identical for every project
- Inter + indigo glow with no brand rationale
- Fake screenshots built from nested `div`s
- Em-dash decoration, section-number eyebrows, multi-marquee pages
- Static page while claiming high `MOTION_INTENSITY`
- Mixing two design systems or icon families

## See Also

- `anti-ai-slop-design` — short checklist only
- `frontend-ui-engineering` — product UI, a11y, component architecture
- `browser-testing-with-devtools` — runtime visual verification
- Upstream research: https://github.com/Leonxlnx/taste-skill (MIT); Agentit keeps a slim, profile-gated fork for token budget
