# Layout hard rules

Failing these is shipping broken marketing UI. Override only when the brief explicitly demands it.

## Hero

- Fits the **initial viewport**. Headline max 2 lines desktop; subtext max ~20 words and 3–4 lines; primary CTA visible without scroll.
- Font scale planned with the hero asset. Prefer `text-4xl md:text-5xl lg:text-6xl` for most heroes; go larger only for very short headlines.
- Top padding cap ~`pt-24` desktop — content must not float mid-viewport.
- **Max 4 text elements:** optional eyebrow, headline, subtext, CTAs (1 primary + optional secondary).  
  Ban inside hero: feature lists, pricing teasers, trust avatar rows, micro-taglines under CTAs, "used by" logos.
- "Trusted by" logo walls sit **under** the hero as their own section.
- Prefer a real image / generated asset / live component preview over gradient-only heroes.

## Navigation

- Single line on desktop. If items wrap at `lg`, shorten labels or collapse secondary items.
- Height cap ~64–80px desktop.

## Eyebrows

Eyebrow = small uppercase wide-tracking label above a section title.

- **Max 1 eyebrow per 3 sections** (hero counts).  
  Example: 9 sections → at most 3 eyebrows.
- Prefer dropping the eyebrow; the headline is usually enough.
- Ban section-number eyebrows (`01 · Capabilities`, `00 / INDEX`).

## Section structure

- **Section-layout repetition ban:** each layout family (3-col cards, full-width quote, split text/image, bento, marquee…) at most **once** per page when possible; a long landing needs several families.
- **Zigzag cap:** alternating image/text split max **2** consecutive sections. Break with full-width, stack, bento, or marquee.
- **Split-header ban as default:** giant left headline + small floating right paragraph as section header. Stack headline then body (`max-w` ~65ch) unless the right column is a real visual/control.
- **Bento:** cell count equals content count (no empty filler tiles). At least some cells need real visual variation (image, tint, pattern) — not cream-on-cream text cards only.
- **Marquee:** at most **one** per page.

## CTAs and forms

- Primary CTA labels short (ideally 1–2 words, max ~3). No multi-line button text on desktop.
- **One label per intent** site-wide ("Contact us" + "Let's talk" + "Get in touch" = fail).
- Button and form contrast: WCAG AA. No white-on-white or ghost CTAs lost on photography without scrim/stroke.
- Labels above inputs; errors below; never placeholder-as-label.

## Cards, shape, color

- Cards only when elevation encodes hierarchy; otherwise dividers or space.
- Shadows tinted to background hue; avoid pure black drop shadows on light UI.
- **One corner-radius system** for the page (document the rule if mixed: e.g. pills for buttons, 12px cards).
- **One accent color family** for the whole page. No warm-gray site that grows a random blue CTA in section 7.
- Prefer neutrals (zinc/slate/stone) + one intentional accent. Unprompted purple/indigo glow is banned.

## Theme lock

- Page is light **or** dark (or system-driven globally). Sections do not flip theme mid-scroll unless the brief calls for a single deliberate color-block story.
- Design both modes when shipping consumer marketing UI unless the brand forbids it.

## Content density

- Default section shape: short headline (≤8 words) + short body (≤25 words) + one visual **or** one CTA.
- Long lists (>5 items): cards, grouped clusters, tabs, scroll-snap, or carousel — not a 20-row hairline table of specs.
- Spec sheets: featured metrics as tiles; rest behind disclosure or grouped clusters.
