---
name: creative-tool-scout
description: Research and select the best current creative-development tools, libraries, primitives, and implementation techniques for a chosen experience instead of defaulting to familiar stacks.
---

# Creative Tool Scout

Use after a concept exists and before committing to a technical implementation when the experience depends on non-trivial motion, 3D, shaders, audio, generative visuals, unusual layout, or interaction.

## Goal

Answer: **what is the best current way to build this idea?** Do not choose a tool merely because the model already knows it.

## Research sources

Prefer live, current sources when available:

- official documentation and repositories;
- `designengineer.tools` as a discovery catalog, not an authority;
- creative-development showcases and implementation writeups;
- ecosystem examples from Three.js, GSAP, Rive, Motion, WebGL/WebGPU, canvas/SVG, audio, and relevant frameworks;
- Context7 or vendor docs for APIs after candidate tools are identified.

## Process

1. Translate the creative concept into technical capabilities: timeline, scroll coupling, vector state machine, real 3D, shader distortion, physics, audio sync, image sequence, camera path, etc.
2. Find 2-4 plausible approaches.
3. Compare them on visual ceiling, implementation complexity, bundle/runtime cost, mobile support, accessibility/reduced-motion, ecosystem maturity, framework fit, licensing, and maintenance risk.
4. Prefer the smallest stack that preserves the intended experience.
5. Verify critical API/version assumptions from primary docs before implementation.
6. Return one recommended stack plus alternatives and explicit reasons not to use them.

## Examples of capability mapping

- complex scroll choreography -> GSAP ScrollTrigger;
- authored vector/state animation -> Rive or Lottie when appropriate;
- simple component interaction -> CSS or Motion before GSAP;
- true spatial/product scenes -> Three.js / React Three Fiber;
- pre-rendered product rotation -> image sequence before unnecessary realtime 3D;
- cinematic shader transitions -> WebGL/WebGPU shader tooling only when the effect justifies the complexity;
- smooth-scroll library -> only if it materially improves choreography, never as decoration.

## Output contract

Return:

- required capabilities;
- recommended stack;
- why it wins;
- alternatives and rejection reasons;
- licensing/maturity caveats;
- performance and mobile implications;
- proof links/docs to consult during implementation.

Do not implement the whole feature unless explicitly delegated as an implementer. This specialist is primarily a research/probe role.
