# Website ship surface

A public marketing or product website can look finished and still be unshipped. Visual polish is not the same as a site that is findable, shareable, usable on a phone, honest about legal/contact facts, and able to complete a form when something goes wrong.

Use this as a **ship-surface gate** after the page looks good. It does not replace `definition-of-done.md`, `shipping-and-launch`, accessibility, security, or performance checklists. It covers the gaps those lists often leave implicit on vibe-coded sites.

## Provenance

Reviewed 2026-09-13:

- https://x.com/Manixh02/status/2098985979067724192 — public checklist of launch items commonly missing from sites that already look complete.
- Reply https://x.com/TheXSami/status/2099026656836898895 — offline/failed-submit form persistence.

Authority: **process checklist / failure-mode list**, not legal advice and not evidence that ticking every box makes a site convert or comply in every jurisdiction.

## When to apply

Apply to public websites, landings, storefronts, and marketing pages that will be deployed to a real domain. Skip or mark N/A for internal tools, local prototypes the user explicitly does not intend to ship, and surfaces with no public URL.

If an item is N/A, write why. Silent omission is not N/A.

## Ship-surface checklist

### Discoverability and sharing

- [ ] Unique, accurate **meta title** on every indexable page
- [ ] Unique, accurate **meta description** on every indexable page
- [ ] **Favicon** set and loading in a real browser tab
- [ ] **Open Graph** title, description, and image resolve to a real preview (not a blank or default card)
- [ ] `robots.txt` exists and matches the intended indexation policy
- [ ] `sitemap.xml` exists for indexable URLs and is reachable
- [ ] Custom **404** page exists, explains the miss, and offers a way back (home/search/nav)

### First viewport and conversion path

- [ ] Primary **CTA is visible above the fold** on the pages that exist to convert
- [ ] Mobile layout is recomposed at real breakpoints, not only shrunk
- [ ] If the primary action matters on a phone, a **sticky mobile CTA** exists *or* the above-fold CTA remains reachable without hunting
- [ ] Contact details that the business claims are **real** (address/email/phone as required by the project and jurisdiction). Do not invent an address to look legitimate

### Interaction states

- [ ] **Loading states** for any async content or submit
- [ ] **Form error states** tied to fields, with recovery copy
- [ ] Successful submit lands on a **thank-you / confirmation** path, not a silent reset
- [ ] If a form can fail (network off, 4xx/5xx), the typed values are kept and the user is told it did not send
- [ ] Meaningful **alt text** on content images; decorative images are marked decorative
- [ ] Images used in production are **compressed** and sized for the layout (no raw multi-megabyte hero dumps)

### Trust, legal, and measurement

Treat these as product/compliance requirements of the actual site, not decoration.

- [ ] **Privacy policy** page exists if the site collects personal data or uses tracking. Content must match what the site actually does. Generated legalese is not a substitute for review when the site is real
- [ ] **Terms** exist when the site sells, signs users up, or otherwise creates a contractual surface
- [ ] **Cookie / tracking notice** exists when non-essential cookies or similar trackers are used. If there are no such trackers, do not add a fake banner
- [ ] **Analytics** is installed only if the project wants measurement, and only after the privacy/cookie decision is coherent
- [ ] No placeholder legal, contact, or analytics IDs left in production (`you@example.com`, lorem addresses, `G-XXXXXXXX`)

## How to verify

Do not mark an item done from file existence alone.

```text
item
-> rendered URL or response evidence
-> mobile and desktop where the item is visual
-> failure path where the item is a form/state
-> N/A reason if skipped
```

Minimum evidence for a public launch:

- unknown URL returns the custom 404, not a framework dump;
- page source or rendered head contains title, description, and OG tags;
- `/robots.txt` and `/sitemap.xml` return the intended documents;
- a form can be submitted, rejected, and recovered without losing input;
- a phone-width viewport can complete the primary action;
- legal/contact pages describe this project, not a template company.

## Overlap map

Keep responsibilities distinct:

| Concern | Home |
|---|---|
| Standing engineering bar | `references/definition-of-done.md` |
| Deploy, rollback, monitoring | `skills/shipping-and-launch` |
| UI states, responsive layout, alt text | `skills/frontend-ui-engineering` |
| Accessibility depth | `references/accessibility-checklist.md` |
| Image/perf budgets | `references/performance-checklist.md` |
| Indexation and SEO diagnosis | `skills/marketing-and-growth/references/seo-growth-loop.md` |
| Visual craft after the first build | `skills/design-inspiration-research/references/premium-web-production.md` |
| Public site still missing launch surface | this file |

## Anti-patterns

- Declaring a landing "done" because the hero looks expensive.
- Generating Privacy/Terms/Cookie pages with invented company facts.
- Adding a cookie banner on a site that sets no non-essential cookies.
- Shipping `localhost` OG images, missing favicons, or default framework 404s.
- Installing analytics before deciding what is being measured and disclosed.
- Treating this list as a new always-loaded skill. Load it when a public site is approaching launch.
