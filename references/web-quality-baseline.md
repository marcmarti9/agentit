# Web quality baseline

Original baseline from PR #43; the cold-start core carries its compact form.

## User-facing web quality invariant

Whenever Agentit creates or materially edits a user-facing website, landing page, product page, app UI, or web copy, the default result must feel intentionally designed for the actual product rather than assembled from generic AI/vibe-coded conventions.

Apply these baseline rules without loading a dedicated anti-slop skill:

- Never fabricate reviews, testimonials, counters, customer counts, metrics, logos, awards, usage numbers, results, or other social proof. Do not invent claims just because a conventional landing-page layout expects them.
- Avoid vague hero copy, generic AI marketing prose, empty hype, repetitive copy formulas, and habitual em-dash-heavy writing. Copy should communicate something concrete about the real product, user, or value proposition.
- Do not use emoji as interface icons when a proper icon or icon set is appropriate.
- Do not add decorative cursor effects or excessive scroll animation by default. Motion must have a functional or clearly intentional visual purpose.
- Do not default to stereotypical AI aesthetics such as purple/blue gradients, giant vague hero typography, excessive glass-card layouts, universal pill-shaped controls, or generic generated hero artwork.
- Do not add `Made with AI`, `Built with AI`, or equivalent badges unless the user explicitly wants them.

These are **anti-default rules, not absolute bans**. A gradient, pill control, generated image, animation, or similar pattern is valid when supported by the brand, product, reference design, platform convention, or an explicit creative decision. Never remove a legitimate design choice merely because it appears on an anti-slop list.

For production/public websites, verify basic legitimacy signals when they are within task scope: a real favicon, appropriate privacy/legal/terms pages, and the intended production domain. Do not require these for disposable prototypes or internal tools.

Prefer specific content, real product evidence, coherent visual hierarchy, restrained interaction, and deliberate structural variation over template conventions.

This invariant stays intentionally small. For substantial visual design, redesign, design-system work, or an explicit anti-slop/design audit, select a dedicated design skill such as `hallmark` JIT instead of expanding the global core.
