# Dials and design-system map

Load after the design read. Do not invent dial aliases (`LAYOUT_VARIANCE`, etc.).

## Dial inference

| Signal | VARIANCE | MOTION | DENSITY |
|--------|----------|--------|---------|
| minimalist / clean / calm / Linear-style / editorial | 5–6 | 3–4 | 2–3 |
| premium consumer / Apple-y / luxury / brand | 7–8 | 5–7 | 3–4 |
| playful / Awwwards / experimental / agency | 9–10 | 8–10 | 3–4 |
| landing / portfolio / marketing (default) | 7–9 | 6–8 | 3–5 |
| trust-first / public-sector / regulated / a11y-critical | 3–4 | 2–3 | 4–5 |
| redesign — preserve | match existing | +1 max | match |
| redesign — overhaul | +2 max | +2 max | match |

## Use-case presets

| Use case | V | M | D |
|----------|---|---|---|
| Landing SaaS mainstream | 7 | 6 | 4 |
| Landing agency / creative | 9 | 8 | 3 |
| Landing premium consumer | 7 | 6 | 3 |
| Portfolio designer / studio | 8 | 7 | 3 |
| Portfolio developer | 6 | 5 | 4 |
| Editorial / blog | 6 | 4 | 3 |
| Public-sector service | 3 | 2 | 5 |

## How dials drive output

**DESIGN_VARIANCE**

- 1–3: equal grids, centered alignment, predictable padding
- 4–7: overlaps, mixed aspect ratios, left-aligned headers
- 8–10: masonry / asymmetric fr units, large empty zones  
- Mobile (`< 768px`): collapse asymmetric layouts to single column

**MOTION_INTENSITY**

- 1–3: hover/active only
- 4–7: CSS transitions, staggered load-ins (`transform` / `opacity`)
- 8–10: scroll choreography (Motion / GSAP ScrollTrigger) — never `window.addEventListener('scroll')` driving React state

**VISUAL_DENSITY**

- 1–3: large section gaps (`py-32`–`py-48` class of spacing)
- 4–7: standard app/marketing spacing
- 8–10: tight packing; prefer hairlines over card chrome; mono for dense numbers

## Official systems (install the package)

| Brief reads as… | Reach for |
|-----------------|-----------|
| Microsoft / enterprise SaaS | Fluent UI |
| Material / Google-flavored | Material 3 / `@material/web` |
| IBM analytics / dense B2B | Carbon |
| Shopify admin | Polaris |
| Atlassian | Atlaskit + tokens |
| GitHub-style devtool / community | Primer (Brand for marketing) |
| UK public sector | `govuk-frontend` |
| US public sector / trust-first | USWDS |
| Fast local-business MVP | Bootstrap 5.3 |
| Accessible React primitives + theme | Radix Themes |
| Ownable SaaS components | shadcn/ui (customize defaults; never ship stock look) |
| Indie Tailwind marketing | Tailwind v4 + deliberate tokens |

**Honesty:** one system per tree. Do not recreate official CSS by hand. Aesthetic trends (glass, brutalism, bento) are **not** official systems — implement with CSS/Tailwind and say so.

## Stack conventions (when no DS package)

- Prefer the project's existing framework and styling
- Greenfield default only when unconstrained: React/Next (RSC-safe), Tailwind, Motion (`motion/react`), fonts via `next/font` or self-host + `font-display: swap`
- Icons: one family (Phosphor, Hugeicons, Radix, Tabler preferred; Lucide only if project already uses it or user asks)
- No hand-rolled icon path SVGs for standard glyphs
- Full-height heroes: `min-h-[100dvh]` (or equivalent), not `h-screen` alone
- Prefer CSS Grid over flex percentage math for multi-column layouts
