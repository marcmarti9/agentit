# Agent-usable inspiration sources

Curated subset of public design-reference sites that return **extractable text/HTML** to coding agents (fetch / browse-page). No user screenshots required.

**How to use (agents):**

1. Pick **1–3** sources that match the design read (not the whole list).
2. Fetch the URL; pull concrete signals: site names, categories, section patterns, component APIs, font family names, copy patterns.
3. Turn signals into design decisions (dials, type, layout family, motion level). State them in the design read.
4. Prefer **linking out to a real example URL** found in a gallery over inventing a fake product UI from divs.
5. Do **not** clone brand assets, logos, or proprietary screenshots. Inspire patterns; ship original work for the user's brand.
6. If a fetch returns empty/403/captcha, skip that source and try another or proceed from dials + anti-slop rules alone.

**Not in this list:** Pinterest, login-walled SPAs, Cloudflare-blocked galleries, and pure visual shells that yield no text to agents (probed 2026-08-08).

---

## Priority for landings / marketing (start here)

Sources re-probed for unattended agent fetch. Prefer **stable** rows first.

| Priority | Source | URL | What the agent can extract | Stability notes |
|----------|--------|-----|----------------------------|-----------------|
| 1 | Supahero | https://supahero.io/ | Hero patterns, headlines, structure language | Stable, rich text |
| 1 | Minimal Gallery | https://minimal.gallery/ | Minimal site names, tools notes | Stable |
| 1 | Minimum | https://mnmm.xyz/ | Large minimal-site directory | Stable |
| 2 | Seesaw | https://www.seesaw.website/ | Experimental site names, tags | Stable, thinner |
| 2 | 60fps | https://60fps.design/ | Motion/UI taxonomy labels | Stable, moderate text |
| 2 | Mobbin | https://mobbin.com/ | Product taxonomy (screens often gated) | Text varies; still usable for naming |
| 3 | SaaSpo | https://saaspo.com/ | SaaS sections/categories when open | **Intermittent 403** — try once, skip if blocked |
| 3 | Awwwards | https://www.awwwards.com/ | Awards / trend labels when open | **Slow / timeouts** — try once, skip if blocked |

### Suggested fetch recipe (landings)

```
1) supahero.io                         → hero + conversion structure
2) minimal.gallery OR mnmm.xyz         → aesthetic extreme (calm/minimal)
3) Optional: 60fps.design if MOTION_INTENSITY ≥ 6
4) Only if needed: saaspo.com / awwwards.com (skip on 403/timeout)
```

Extract **named examples** (e.g. “split hero, not three equal cards”) and map them to layout hard rules.

---

## Components, systems, and implementable patterns

These are the strongest agent sources: docs, APIs, and copyable patterns without screenshots.

| Source | URL | What the agent can extract | Use when |
|--------|-----|----------------------------|----------|
| shadcn/ui | https://ui.shadcn.com/ | Component names, usage, tokens, composition | React design-system foundation (always customize) |
| 21st.dev | https://21st.dev/ | React UI catalog entries, component descriptions | Need non-default blocks beyond stock shadcn |
| Component Gallery | https://component.gallery/ | Component taxonomy + design-system examples | Naming patterns, DS comparison |
| NumberFlow | https://number-flow.barvian.me/ | Full component docs for animated numbers | Metrics, counters, pricing digits |
| Fancy Components | https://www.fancycomponents.dev/ | Component library pitch + links | Decorative micro-interactions (verify package first) |
| Cursify | https://cursify.vercel.app/ | Custom cursor component docs | Only if brief wants non-default cursors (use sparingly; a11y) |

### Suggested fetch recipe (implementation)

```
1) ui.shadcn.com  → primitives / forms / dialogs
2) 21st.dev or component.gallery  → richer marketing blocks if needed
3) number-flow only for animated stats
```

Always verify packages in `package.json` and prefer project stack over adding deps for flair.

---

## Typography (text-first; no screenshots)

| Source | URL | What the agent can extract | Use when |
|--------|-----|----------------------------|----------|
| Fonts In Use | https://fontsinuse.com/ | Real pairings, project contexts, type names | Serious brand/type direction |
| Free Faces | https://www.freefaces.gallery/ | Free face names by classification | Budget-friendly distinctive type |
| Best Free Fonts | https://bestfreefonts.com/ | Curated free families by style | Quick free font shortlist |

Prefer self-host / `next/font` and license-safe fonts. Avoid Inter-as-default when the brief allows better brand type (see dials + AI tells).

---

## Optional / adjacent (agent-readable, not core taste)

| Source | URL | Notes |
|--------|-----|--------|
| craftwork.design curated | https://craftwork.design/curated/websites | Extra website index |
| rebrand.gallery | https://www.rebrand.gallery/ | Rebrand before/after language (identity work) |
| loadmo.re | https://loadmo.re/ | Mobile web archive listings |
| skills.sh | https://www.skills.sh/ | Agent skills directory (meta; not visual design) |
| v0.app | https://v0.app/ | AI UI generator product page (process tool, not aesthetic source of truth) |

Game UI / FUI / generative tools (Game UI Database, HUDs+GUIs, cables.gl, NodeToy, etc.) are agent-readable but **out of scope** for default marketing landings unless the brief is game/FUI/gen-art.

---

## Explicitly avoided for unattended agent fetch

Do not depend on these without human help or a live browser session that actually renders content:

- pinterest.com, same.energy, searchsystem.co, shadertoy.com  
- reactbits.dev, motion-primitives.com (bot/rate walls in probe)  
- unicorn.studio, stitch.withgoogle.com (empty shells to fetch)  
- layers.to, fontshare.com, spiral.soot.com (too thin via HTTP alone)

---

## Output contract after consulting sources

When you used this list, report briefly:

```
REFERENCES USED:
- <source>: <what you took> → <design decision>
```

Example:

```
REFERENCES USED:
- saaspo.com: multi-section SaaS structure without triple equal cards → zigzag + bento only once
- fontsinuse.com: editorial sans pairings → Geist-like sans, not Inter default
- ui.shadcn.com: button/input primitives → own tokens, not stock shadcn chrome
```
