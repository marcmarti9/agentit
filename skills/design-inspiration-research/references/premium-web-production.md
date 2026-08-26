# Premium web production — distilled reference playbook

This reference turns the useful workflow behind the bookmarked “$10k website” / cinematic-web articles into an Agentit procedure. It deliberately does **not** preserve the price headline as evidence: pricing screenshots and creator price anchors are marketing claims, while the production workflow can still be useful.

## Provenance

Primary bookmarked sources reviewed 2026-08-25:

- https://x.com/bateshkaaa/status/2079218516150862086 — primary source for the AI-compressed agency-quality website workflow: skills, section-level screenshot references, explicit constraints/ban list, first build, then separate polish passes.
- https://x.com/heynavtoor/status/2083221614595051602 — cinematic / Apple-like product-page workflow reference.
- https://x.com/xiathis/status/2077468692493791353 — cinematic high-craft web production reference.
- https://x.com/monokern/status/2074889830501155091 — 21st.dev component catalog with ready-made prompts to paste into a coding agent; useful for discovering interaction primitives, not a wholesale site-production method.

Authority: **process/design inspiration**, not independent evidence that a website is worth any quoted dollar amount or that cinematic motion improves conversion.

## The valuable idea

The repeatable advantage is not “ask Claude for a $10k website”. It is to give the model the same inputs a competent creative director would want:

1. real business/product truth;
2. concrete references rather than vague adjectives;
3. references mapped to specific page responsibilities;
4. explicit art direction before implementation;
5. one or a few signature interactions with a reason to exist;
6. repeated visual review against the rendered result;
7. a separate polish/QA pass after the first build.

AI compresses implementation and exploration time. It does not remove art direction, judgment, copy truth, performance constraints, accessibility, or market validation.

## Studio workflow

### 1. Establish project truth before aesthetics

Collect or inspect:

- actual product/service and audience;
- desired action / conversion goal;
- real proof and assets available;
- brand constraints;
- required pages/sections;
- technical stack and existing component system;
- performance/accessibility constraints;
- content that must be preserved.

Do not invent testimonials, logos, metrics, dashboards, awards, users, or product capabilities to make a reference-derived composition look convincing.

### 2. Build a section-level reference map

Do not choose one website and ask the agent to recreate it. Gather several references and map each to a narrow purpose.

Example:

```text
REFERENCE MAP
hero / first impression -> ref A: scale + asymmetric composition
navigation -> ref B: restrained floating navigation behavior
problem/story section -> ref C: editorial rhythm
product proof -> ref D: large artifact + annotation treatment
CTA -> ref E: quiet high-contrast close
motion grammar -> ref F: reveal pacing, not exact animation
```

When screenshots/assets are useful, store project-local working references in a clearly temporary/research location such as `reference/` or the project's existing design-research folder. Do not ship those assets accidentally and do not treat them as licensed production assets.

The value of a reference is the **decision it informs**, not the fact that it was downloaded.

### 3. Extract design DNA

For each reference, extract only the relevant dimensions:

- macrostructure / section rhythm;
- hierarchy and visual weight;
- grid / asymmetry / whitespace;
- typography roles and contrast;
- material/color language;
- image/product-artifact treatment;
- interaction archetype;
- motion timing/pacing;
- responsive behavior;
- what specifically should not be copied.

Then synthesize an original `DESIGN_DIRECTION` around the target project's own content and identity.

### 4. Ask only decision-frontier questions

After inspecting the project and references, ask questions only where the answer materially changes the design and cannot be recovered from existing context.

Typical decision frontiers:

- restrained vs expressive visual character;
- typography constraints/licensed fonts;
- which sections or claims are required;
- whether motion should be ambient, narrative, or nearly absent;
- whether the signature interaction is appropriate;
- content/assets that can or cannot be replaced.

Do not ask the user to re-specify details already discoverable from the repository, brief, brand files, or references.

### 5. Design a vertical slice first

Before filling the whole site with generated sections, implement:

- the hero / first viewport;
- one representative content section;
- core typography/tokens;
- the primary interaction/motion grammar;
- responsive behavior for those pieces.

Render it. Critique it. Fix the direction before scaling it across the page.

This avoids producing an entire polished-looking wrong direction.

### 6. Use one memorable interaction deliberately

The bookmarked workflow's useful principle is not “add flashy effects”. It is to identify a **signature mechanic** that reinforces the experience.

Possible families:

- cursor spotlight / reveal where discovery is part of the story;
- scroll-linked product transformation where sequence explains the product;
- restrained depth/parallax where layering communicates hierarchy;
- meaningful before/after interaction;
- tactile state transition on a key product control.

Gate it with:

```text
Does it communicate something?
Does it fit the brand?
Does it remain usable by keyboard/touch?
Does reduced-motion have a sane path?
Does it stay smooth on representative mobile hardware?
Is the implementation/maintenance cost justified?
```

If not, use simpler motion. “Premium” does not mean maximum animation density.

### 7. First defect pass: inspect the rendered page like a user

After the first complete implementation, perform a **defect pass** before aesthetic micro-polish.

Scroll and interact through the page at representative desktop and mobile widths. Capture concrete defects such as:

- awkward section transitions;
- empty/dead visual zones;
- overflow/clipping;
- animation jank or delayed input;
- type wrapping/measure problems;
- weak hierarchy;
- inconsistent spacing/tokens;
- motion that competes with reading;
- poor touch behavior;
- missing states;
- fake/placeholder-looking content.

Batch-fix the structural defects first.

### 8. Separate polish pass

Then run a deliberate polish review:

#### Typography
- hierarchy is obvious without relying on color alone;
- display/body roles are coherent;
- line length and wrapping are intentional;
- type choices fit the visual thesis rather than following a generic AI trend.

#### Color/material
- palette is restrained enough to create emphasis;
- token relationships are coherent;
- gradients/glows/glass exist only when they belong to the concept;
- contrast remains accessible.

#### Composition
- sections do not repeat the same centered heading + three equal cards pattern;
- artifacts/proof appear where the narrative needs them;
- scale and whitespace change rhythm intentionally.

#### Motion
- every major animation has a purpose;
- transitions do not block input or reading;
- reduced-motion is respected;
- no constant ornamental movement competes for attention.

#### Mobile
- mobile is recomposed, not merely shrunk;
- text hierarchy, art crops, controls and motion are independently checked;
- expensive effects degrade gracefully.

#### Copy/content
- no AI filler or fake specificity;
- claims are backed by project truth;
- CTA matches the actual next step;
- repeated marketing language is removed.

### 9. Human/independent critique is selective, not ceremonial

A critique pass should produce specific findings, not automatically force all suggestions into the product.

For each meaningful critique:

```text
finding
why it matters
proposed change
trade-off
accept / reject / test
```

The primary agent remains responsible for the integrated direction.

### 10. Completion evidence

A high-craft website is not complete because the code builds.

Require evidence appropriate to the claim:

- desktop + mobile rendered/browser inspection;
- console/network/runtime sanity;
- responsive behavior;
- keyboard/focus and reduced-motion behavior where applicable;
- performance check for expensive motion/assets;
- factual/content review;
- reference-to-decision map for material external influences.

## Anti-patterns extracted from the source set

- “Make it look like a $10k/$50k website.”
- Copy one reference wholesale.
- Start coding before knowing which reference informs which section.
- Generate every section in one pass and only review at the end.
- Add five signature effects instead of one coherent interaction language.
- Confuse cinematic complexity with conversion value.
- Preserve creator price/revenue claims as project facts.
- Use screenshots/reference assets in production without rights.
- Let the first generated version become the final version because it looks superficially polished.

## What Agentit should carry forward

The durable procedure is:

```text
truth
-> section-level references
-> design DNA
-> clarify real decision frontiers
-> original DESIGN_DIRECTION
-> vertical slice
-> signature mechanic if justified
-> full build
-> rendered defect pass
-> polish pass
-> browser/accessibility/performance verification
-> provenance
```

That is the useful part of the “$10k website” article. The dollar figure is not.
