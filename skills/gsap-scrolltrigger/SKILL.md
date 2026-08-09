---
name: gsap-scrolltrigger
description: Official-GSAP-informed guidance for scroll-triggered and scroll-scrubbed animation: pinning, scrub timelines, parallax, horizontal sections, start/end markers, snapping, refresh behavior, React cleanup, and ScrollTrigger debugging.
license: MIT
source: https://github.com/greensock/gsap-skills
---

# GSAP ScrollTrigger

Agentit adaptation of GreenSock's MIT-licensed official GSAP agent skills. Use this when scroll controls animation timing, pinning, scrubbed timelines, parallax, section reveals, horizontal storytelling, image sequences, or other synchronized scroll choreography.

## Use GSAP deliberately

For simple scroll reveals, native CSS/IntersectionObserver may be enough. Use ScrollTrigger when the animation requires precise sequencing, scrubbed progress, pinning, markers, cross-section coordination, or complex responsive choreography.

Verify the project actually has `gsap` installed before importing it. Register ScrollTrigger once in the appropriate client/runtime boundary.

```js
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
gsap.registerPlugin(ScrollTrigger);
```

## Core model

A ScrollTrigger owns a relationship between document scroll position and either callbacks or a GSAP tween/timeline.

Define intentionally:

- `trigger` — the element establishing the scroll region;
- `start` — where the relationship begins;
- `end` — where it ends;
- `scrub` — whether animation progress follows scroll progress;
- `pin` — whether a stage remains fixed while the timeline advances;
- `markers` — use during debugging, remove before ship;
- `invalidateOnRefresh` / refresh strategy — when dimensions are dynamic.

Start/end values are part of the design. Do not cargo-cult `"top top"` / `"+=3000"` without checking the actual narrative length.

## Timelines over independent triggers

When several elements form one story beat, prefer a single timeline with one ScrollTrigger over many loosely coupled triggers. This creates deterministic choreography and makes reverse scrolling understandable.

Use timeline labels for semantic phases such as `intro`, `explode`, `explain`, `reassemble` rather than scattering magic offsets through the file.

## Pinning

- Prefer pinning a stable wrapper/stage and animating its contents.
- Avoid animating transforms on the exact element ScrollTrigger is pinning unless you fully understand the measurement implications.
- Ensure the end state hands back to document flow without a jump or giant blank spacer.
- Nested pins are a last resort.
- Font/image/layout changes can invalidate measurements; refresh after meaningful layout stabilization when needed.

## Scrub

`scrub: true` maps scroll progress directly. A numeric scrub adds catch-up smoothing. Choose based on feel, not because smoother is automatically better.

For product storytelling, scroll must remain reversible: if the user scrolls back, the product should coherently reassemble/reverse rather than encounter one-way side effects.

## Horizontal storytelling

When vertical scroll drives a horizontal track, animate one container timeline and use `containerAnimation`/the supported GSAP pattern for triggers that live inside that transformed track. Keep the driving animation linear; easing the container destroys the mapping between scroll position and nested trigger position.

Do not make normal navigation horizontally scroll-jacked merely to look different.

## Responsive behavior

Use GSAP's responsive/context patterns or explicit media-query branches so mobile can have different start/end/pin behavior. A pinned desktop scene often needs a simpler mobile composition.

Do not rely on a resize producing the same geometry by accident. Verify orientation changes and narrow widths.

## React / Next

- Keep GSAP DOM animation in a client boundary.
- Scope selectors to a component root.
- Create animations inside lifecycle/context helpers that clean up on unmount.
- Revert ScrollTriggers/timelines during cleanup so route changes and Strict Mode do not duplicate them.
- Do not put scroll progress into `useState` every frame.

Pair with the project's React-specific GSAP lifecycle pattern when available.

## Scroller integrations

If using Lenis or another smooth-scroll engine, use the integration recommended by the current library/GSAP docs. Synchronize timing rather than running two unrelated scroll loops.

Do not add smooth scrolling if native scrolling already gives the desired result.

## Debugging

During implementation:

- enable markers on the trigger you are debugging;
- label timelines;
- inspect start/end values;
- confirm the right scroller/root is being used;
- verify triggers are not duplicated after hot reload/navigation;
- check reverse scroll;
- resize mid-sequence;
- confirm refresh does not jump the scene.

Remove markers/logging before completion.

## Accessibility

ScrollTrigger is never an excuse to make content inaccessible. Build a reduced-motion path that exposes the meaningful states without requiring a long scrub or aggressive camera motion. Do not hide essential text exclusively inside transient frames.

## Pairing

Use `scrollytelling-web` for narrative architecture, `gsap-performance` for performance, `emil-design-eng` for motion feel, and `browser-testing-with-devtools` for runtime verification.

## Attribution

Adapted from GreenSock's official MIT-licensed `greensock/gsap-skills` project. Preserve attribution when redistributing substantial portions.
