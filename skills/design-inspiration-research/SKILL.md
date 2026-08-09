---
name: design-inspiration-research
description: Research current visual, motion, interaction, spatial, and brand references before committing to a design direction. Use for ambitious redesigns, premium landing pages, creative coding, motion direction, spatial experiences, or when the user asks for fresh inspiration from the web, TikTok, galleries, social media, studios, or award sites.
---

# Design Inspiration Research

Act as a design researcher, not a scraper or copy machine. Gather current references, decompose why they work, and synthesize original directions for the project.

## Goal

Return a compact inspiration board made of **patterns and principles**, then feed those findings into `creative-web-experiences`, `design-taste-frontend`, and the implementation specialists.

Do not start coding before the reference pass when the user explicitly asks for fresh/current inspiration or when originality is a primary success criterion.

## Source mix

Prefer a diverse mix rather than one aesthetic bubble:

- studio and agency sites;
- Awwwards-style galleries and curated web showcases;
- real product/brand sites;
- portfolios and experimental creative-development sites;
- Figma Community when relevant;
- GitHub demos / CodePen / shader and Three.js showcases for implementation ideas;
- TikTok, Instagram, Pinterest, YouTube, X, or other social feeds when browser access is available and the content is useful;
- editorial, architecture, fashion, industrial design, photography, film titles, games, museums, and physical retail when cross-domain inspiration would improve the concept.

Treat social platforms as discovery surfaces, not authoritative technical documentation.

## Browser research workflow

When live browser/search tools are available:

1. Search 4-8 distinct queries that describe the **experience**, not only the industry. Examples: `interactive retail webgl`, `spatial ecommerce website`, `kinetic typography landing`, `scroll camera journey`, `digital flagship store`, `immersive editorial web`.
2. Open promising references and inspect actual behavior, not only thumbnails.
3. Record the URL/title/source and the specific mechanism worth learning from.
4. When a page is interactive, inspect multiple states or scroll sections.
5. Collect 6-12 useful references, then stop. More references are not automatically better.
6. Cluster them into 2-4 patterns and identify what is becoming cliché.
7. Synthesize new directions that combine principles from multiple references.

Use Playwright or Chrome DevTools when interaction must be experienced directly. Prefer an isolated browser profile. Do not attach to a user's personal daily browser unless explicitly authorized.

## TikTok / social research

If TikTok or another social platform is requested:

- Prefer ordinary browser navigation/search through public pages or an explicitly authorized isolated logged-in session.
- Respect platform access controls, rate limits, robots/terms, and authentication boundaries. Do not bypass CAPTCHAs, anti-bot systems, private accounts, paywalls, or login protections.
- Do not assume an official API supports arbitrary discovery. If the available API only exposes authorized-user content or restricted research access, fall back to browser research or another source.
- Capture **design observations and links**, not bulk-downloaded media.
- Social trends age quickly; note the research date and avoid treating engagement metrics as proof of design quality.

## What to extract from every reference

For each useful reference, answer only what matters:

- **Hook:** what makes the first 3-5 seconds distinctive?
- **Composition:** grid, scale, whitespace, depth, framing, typography.
- **Interaction:** what does the user do and what responds?
- **Motion grammar:** easing, pacing, continuity, camera, masks, transforms, cuts.
- **Narrative:** how does the experience reveal information?
- **Technical hypothesis:** CSS / GSAP / canvas / WebGL / video / image sequence / Rive / mixed DOM+3D.
- **Why it works:** the principle worth keeping.
- **What not to copy:** distinctive brand assets/layouts/content or overused gimmicks.

Do not reverse-engineer proprietary code when observation is enough.

## Deliverable: inspiration brief

Produce:

### Reference signals
A concise list of the strongest references and the one useful idea from each.

### Pattern clusters
Group observations into coherent directions such as spatial navigation, editorial motion, object theatre, tactile interaction, or restrained luxury.

### Cliché radar
Call out recurring patterns that would make the result feel derivative or AI-generated.

### Original synthesis
Propose 2-3 project-specific concepts. Each concept must combine multiple principles rather than cloning a single reference.

### Implementation implications
State which Agentit specialists should be loaded: GSAP, scrollytelling, Three.js spatial/product, Figma, performance, etc.

## Quality bar

A reference board is successful when it expands the solution space and improves judgement. It fails when it merely produces a Pinterest wall, copies the coolest site found, or forces every fashionable technique into one page.
