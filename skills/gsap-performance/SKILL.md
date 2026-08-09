---
name: gsap-performance
description: Performance rules for GSAP and high-motion web experiences: compositor-friendly properties, batching, quick setters, timeline ownership, ScrollTrigger cost, mobile constraints, cleanup, and runtime profiling.
license: MIT
source: https://github.com/greensock/gsap-skills
---

# GSAP Performance

Agentit adaptation of GreenSock's official MIT-licensed GSAP skills. Use alongside any animation-heavy page and especially with `gsap-scrolltrigger` or `scrollytelling-web`.

## Performance is part of motion design

A beautiful sequence that drops frames, blocks scrolling, overheats a phone, or leaks after navigation is not finished design.

## Hot-path rules

Prefer animating properties that can stay on the compositor: transforms and opacity. Be cautious with properties that repeatedly trigger layout/paint, including width/height/top/left, large filters, shadows, masks, and complex clip paths.

This is not an absolute ban: some premium effects require paint-heavy properties. Budget them intentionally, isolate them, and profile the actual result.

## Avoid render-loop React state

Never call React state setters on every scroll/pointer/animation frame just to mirror a continuous animation value. Keep continuous state in GSAP/motion values/refs and update React only for semantic discrete state changes.

## Reuse animation objects

- Prefer one timeline that owns related choreography rather than recreating tweens every frame.
- For very high-frequency pointer/scroll setter cases, use GSAP's optimized setter/to patterns instead of allocating new tweens continuously.
- Do not create new ScrollTriggers inside scroll callbacks.
- Kill/revert timelines, contexts, listeners, and triggers on unmount/navigation.

## DOM and layout

- Batch DOM reads before writes when manual measurement is necessary.
- Avoid alternating `getBoundingClientRect()` and style writes in loops.
- Keep enormous blurred layers and full-screen backdrop filters out of hot animated paths when possible.
- Promote layers deliberately; do not spray `will-change` across the whole page.
- Remove `will-change` or leave promotion decisions to the animation engine when permanent layers would waste memory.

## ScrollTrigger-specific

- Use the smallest number of triggers that accurately models the narrative.
- One timeline + one trigger is generally cheaper and more coherent than dozens of independent scrubbed triggers for one scene.
- Avoid refresh loops caused by continuously mutating layout around measured trigger boundaries.
- Lazy-initialize heavy below-the-fold scenes where practical.
- Pause expensive scene work when the relevant chapter is inactive.

## WebGL / Three.js pairing

On product storytelling pages:

- cap DPR instead of blindly rendering at device pixel ratio 3/4;
- use compressed textures/geometry when the asset pipeline supports them;
- avoid an always-running render loop when the scene can render on demand;
- pause or reduce work when offscreen;
- dispose geometries, materials, textures, render targets, and listeners during teardown;
- keep post-processing passes few and justified;
- test thermals/frame pacing on a real mobile-class device if the experience is important.

## Mobile degradation is design, not failure

A desktop cinematic scene may become a shorter scrub, pre-rendered sequence, static milestones, or simpler product rotation on constrained devices. Preserve the story and hierarchy; reduce implementation cost, not meaning.

## Measure

Use browser performance tooling on the actual interaction. Look for:

- long main-thread tasks;
- repeated layout/recalculate-style cycles;
- paint/composite hotspots;
- event-listener churn;
- memory growth across route transitions;
- duplicated timelines/triggers in development and production;
- slow asset decode/upload to GPU;
- frame drops at section handoffs.

Do not infer smoothness from source code or a single screenshot.

## Reduced motion

The reduced-motion path should often eliminate expensive cinematic work entirely. It is both an accessibility path and a useful robustness fallback.

## Attribution

Adapted from GreenSock's official MIT-licensed `greensock/gsap-skills` project. Preserve attribution when redistributing substantial portions.
