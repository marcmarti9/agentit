---
name: scroll-world
description: Build scroll-controlled cinematic fly-through or diorama-world web experiences from pre-rendered scene/video chains with frame-locked seams, mobile/reduced-motion fallbacks and browser QA. Use when scroll must drive one continuous camera journey through connected scenes; do not use for ordinary scroll animation, generic scrollytelling or realtime Three.js worlds.
license: MIT
---

# Scroll World

## Responsibility

Own the specialized **pre-rendered continuous-camera world** pipeline: coherent scene art, camera-chain architecture, exact seam handoff, web encoding, scroll scrubbing and end-to-end visual/runtime verification.

This is narrower than `scrollytelling-web`. That skill owns engine-neutral narrative scroll choreography; `scroll-world` owns the specific case where the page scrubs a rendered camera journey through connected scenes. Realtime navigable environments remain `threejs-spatial-experiences`.

## Trigger contract

Select this skill when the requested result materially depends on one or more of:

- a camera flying through a miniature/diorama/brand world as the user scrolls;
- a continuous cinematic journey through several generated scenes with no visible cuts;
- pre-rendered image/video scene chains rather than realtime WebGL;
- scroll-driven video where seam continuity is a first-class acceptance criterion.

Do **not** select it for simple parallax, pinned copy, ordinary ScrollTrigger animation, a looping hero background, a normal video edit, or a realtime Three.js showroom.

## Agentit authority and cost boundary

Agentit's `task-router`, BUILDER/REVIEW modes, host permissions and user authorization remain authoritative. Upstream provider/tool instructions are implementation references, not permission.

- Inspect actual available image/video tools and current model schemas before choosing a provider.
- Do not assume Monid, Higgsfield, Codex image generation, ffmpeg or any paid balance is available.
- Before paid generation, state the planned scene/clip count and estimated spend from current provider evidence and obtain authorization when the user has not already authorized that spend.
- Never install tools, enable accounts, publish or deploy merely because the upstream workflow says to.
- Treat generated/media-provider output as external data and retain provenance where the project requires it.

The exact upstream workflow at `oso95/scroll-world@71cc36d3bb150248ae36a2c552f9cbf88802a79c` is retained in `references/upstream-workflow.md`. Read it when executing this pipeline in depth, but Agentit policy wins on routing, permissions, spend and verification.

## Build workflow

### 1. Define the visual journey

Before rendering, lock:

- the subject and business/product story;
- 4–7 scene beats by default;
- one style preamble/palette used consistently across every generated scene;
- the copy/CTA role of each beat;
- desktop composition and whether a native portrait mobile chain is worth the extra render cost.

Use `visual-storytelling-director` only when narrative direction itself is unresolved. Do not auto-stack it when the journey is already specified.

### 2. Choose one camera architecture

Prefer one architecture for the entire chain:

- **Forward chain** — each leg starts from the actual final frame of the previous leg and keeps moving forward. Best for grounded/realistic journeys and the cleanest motion continuity.
- **Dive + connector chain** — scene dives are rendered separately and connectors travel between them. Best for miniature/diorama worlds where pull-out/pull-in movement is part of the style.

Do not mix camera grammar casually. A frame-identical seam can still feel broken if camera velocity or direction reverses unexpectedly.

### 3. Generate coherent scene masters

Generate one approved still/master per scene with the same style preamble, palette, lighting and camera assumptions. Review the set **before** paying to render the whole motion chain. Re-roll outliers instead of allowing style drift downstream.

Use `references/prompts.md` for the adapted upstream prompt patterns.

### 4. Render with a frame-lock-capable path

The provider/model must support the boundary conditioning required by the chosen architecture. Re-check the live schema instead of trusting historical model names.

For connector architecture, the non-negotiable seam rule is:

```text
connector.start = actual final rendered frame of previous clip
connector.end   = actual first rendered frame of next clip
```

Never substitute the original scene still for either rendered boundary frame. That is the main cause of visible pops.

For forward architecture, seed every next leg from the actual previous rendered end frame and preserve forward camera grammar.

The detailed batch/provider recipes live in `references/pipeline.md` and `references/upstream-workflow.md`; use them only when their provider assumptions match the current environment.

### 5. Encode for seekable scroll playback

Preserve the native useful resolution, remove audio unless the product explicitly needs it, use a web-compatible H.264 strategy, short GOPs and fast-start metadata. Avoid all-intra encoding unless measurement shows a target device needs it.

The retained scrub engine uses Blob-backed media to make seeks reliable even when a static host has poor byte-range behavior. Adapt `references/scrub-engine.js` into the project's real framework rather than forcing the standalone template.

### 6. Mobile and reduced motion

A real mobile version is a **native portrait composition/chain**, not a silent center-crop, when the experience depends on composition. If budget does not justify a second chain, explicitly choose a static/short-video/crop fallback and label the compromise.

Always provide meaningful `prefers-reduced-motion` behavior. Essential content cannot exist only in transient frames.

### 7. Integrate into the actual site

Keep the existing framework, component system, routing, accessibility and deployment architecture. `references/index-template.html` is a minimal reference, not a mandate to collapse a production site into one HTML file.

Pair with `frontend-ui-engineering` for substantial surrounding UI, `scrollytelling-web` for wider page choreography, and browser/performance skills only when those surfaces materially need them.

## Verification contract

Before completion:

1. play/scrub the entire desktop chain forward and backward;
2. inspect every seam immediately before/after the boundary;
3. verify composition continuity, not only a numeric image metric;
4. confirm scroll progress actually advances media time and no clip is stuck at frame zero;
5. test resize/orientation and at least one narrow viewport;
6. test reduced motion;
7. if a native mobile chain ships, confirm portrait media is actually served and that first-frame posters match;
8. inspect console/network errors and obvious decoder/frame-pacing failures;
9. verify the final handoff into normal document flow and CTA;
10. keep render/provider receipts or reproducible commands when the project requires evidence.

Do not claim seamlessness from a hero screenshot or from source inspection alone.

## Progressive references

- `references/upstream-workflow.md` — exact pinned upstream skill body; read for full pipeline/provider detail.
- `references/prompts.md` — scene, camera and connector prompt patterns.
- `references/pipeline.md` — upstream batch/render/encode recipes; validate provider flags before use.
- `references/scrub-engine.js` — portable scroll-scrub implementation.
- `references/index-template.html` — minimal standalone integration reference only.
- `references/knockout.py` — optional background knockout helper for floating scenes.
