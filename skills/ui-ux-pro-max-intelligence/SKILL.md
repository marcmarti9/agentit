---
name: ui-ux-pro-max-intelligence
description: Provider-neutral JIT UI/UX design intelligence adapter for the upstream UI UX Pro Max database. Use for product-specific style, palette, typography, UX, chart, icon, motion, landing, and stack guidance; do not treat it as the final creative director.
---

# UI UX Pro Max Intelligence

## Role

Use the upstream `nextlevelbuilder/ui-ux-pro-max-skill` project as a **searchable design-intelligence source**, not as a replacement for Agentit's art direction, research, critique, or implementation skills.

Upstream is MIT-licensed. Do not dump the full database into model context. Query only the dimensions needed for the current task and synthesize the results into a compact artifact.

Canonical upstream: `https://github.com/nextlevelbuilder/ui-ux-pro-max-skill`.

## Why Agentit uses it

UI UX Pro Max is strongest at structured, product-aware lookup:

- product patterns and landing structures;
- style families;
- color palettes;
- typography pairings;
- UX/accessibility rules;
- icons;
- charts/data visualization;
- motion/GSAP presets;
- stack-specific implementation guidance.

Agentit's other design skills remain responsible for judgment:

- `design-taste-frontend` -> art direction and visual thesis;
- `impeccable` -> craft critique and polish;
- `emil-design-eng` -> interaction/motion feel;
- `creative-web-experiences` -> concept generation;
- `design-inspiration-research` / `design-trend-researcher` -> current external references;
- `visual-storytelling-director` -> narrative pacing.

Treat database output as evidence/candidates, never as an automatic design.

## JIT discovery

Before using the database, look for an existing local checkout or installed skill. Candidate locations include provider-specific skill roots and a project/harness vendor cache. Do not assume one provider's path.

If the upstream search tool is available, use its `search.py` with the exact path discovered at runtime. Prefer `python3` when available. Do not hard-code `${CLAUDE_PLUGIN_ROOT}` into shared Agentit policy.

If no local copy exists:

1. use live GitHub/web access to inspect the upstream when the environment supports it; or
2. report that the external database is unavailable and fall back to Agentit's built-in design skills.

Do not silently clone/install external code during ordinary execution unless the current environment/user policy authorizes dependency installation.

## Workflow

### 1. Detect the product and stack

Infer factual information from the repo when possible: product type, existing stack, design system, tokens, component library, target surface, and current interaction patterns.

Ask the user only for decisions/preferences that cannot be discovered.

### 2. Query narrowly

For a new visual surface, prefer one design-system query first, then only the domains that materially affect the chosen direction.

Useful upstream domains include:

- `product`
- `style`
- `color`
- `typography`
- `google-fonts`
- `ux`
- `landing`
- `icons`
- `chart`
- `gsap`
- stack-specific guidance

Do not query every domain by ceremony.

### 3. Synthesize, don't copy

Write a compact intelligence artifact containing:

```text
PRODUCT / CONTEXT
...

RECOMMENDED BASELINES
- layout / information architecture
- typography
- palette / contrast
- interaction / accessibility
- stack-specific constraints

CANDIDATE VISUAL FAMILIES
A. ...
B. ...
C. ...

AVOID
- saturated / generic patterns
- conflicts with brand or content

SOURCE NOTES
- upstream queries used
- any missing/zero-result searches
```

If a search returns zero or irrelevant results, say so. Never fabricate a database match.

### 4. Hand off to judgment skills

The intelligence artifact is input to the creative/design process. A strong default flow is:

`UI UX Pro Max intelligence -> Taste / creative direction -> implementation -> Impeccable / Emil / critic`.

For high-ambition work, combine it with live inspiration research rather than using only database recommendations.

## Effort-level behavior

### Standard

Use only when it can prevent an obvious design mistake or answer a concrete lookup. One compact query or small set of targeted queries. Keep context tight.

### Polished

Use product + relevant style/typography/color/UX guidance when it materially improves the result. Persist a concise design baseline if the project will continue across sessions.

### Studio

Use as one evidence source among live research, concept competition, art direction, and critique. Broader querying is allowed, but the database must not collapse creative exploration into a preset template.

## Persistence

For continuing product work, save stable design decisions into the project's Agentit continuity documentation. If the upstream `--persist` design-system feature is used, record the generated path in the project's continuity state so another session/machine knows it exists.

Never rely on chat history as the only copy of a design-system decision.

## Anti-patterns

- loading the entire upstream database into the parent context;
- treating a recommended style/palette as mandatory art direction;
- defaulting every tech portfolio to dark + neon + glassmorphism;
- querying every domain regardless of task;
- hiding zero-result searches;
- assuming Claude-specific paths or APIs;
- replacing live trend/reference research with a static database;
- generating a persisted design system and failing to document where it lives.

## Verification

Before claiming the intelligence pass is complete:

- [ ] product/stack facts came from the repo or explicit user input;
- [ ] only relevant upstream domains were queried;
- [ ] query results were summarized rather than dumped wholesale;
- [ ] no zero-result query was represented as evidence;
- [ ] creative judgment remained with Agentit's design stack;
- [ ] any stable result needed for later sessions was persisted/documented.
