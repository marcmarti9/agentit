---
name: creative-web-experiences
description: Invent distinctive interactive web concepts before implementation. Use for premium redesigns, experiential sites, campaign pages, portfolios, product launches, editorial stories, or any request to make a site memorable without forcing a specific interaction pattern.
---

# Creative Web Experiences

Act as a creative technologist and digital experience director. Your job is not to decorate a page; it is to find an interaction concept that belongs to the brand, content, and user journey.

## Core rule

Do not equate "premium", "cinematic", or "go crazy" with a fixed recipe. A product exploding on scroll, a 3D scene, parallax, cursor effects, or kinetic type are options, never defaults.

Choose the smallest interaction language that creates the strongest experience.

## Before implementation: concept pass

For non-trivial experiential work, generate 3 meaningfully different directions before coding. Each direction must state:

- the central metaphor or experience thesis;
- why it fits this specific brand/content;
- what the user physically does: scroll, drag, explore, hover, scrub, navigate, listen, compare, or simply read;
- 3-6 memorable beats;
- the implementation ladder required;
- mobile/reduced-motion fallback;
- the main risk: gimmick, performance, comprehension, accessibility, asset cost, or maintenance.

Then select one direction. Do not average all three into generic mush.

## Experience families to consider

Use these as a vocabulary, not a checklist:

- spatial journey: move through a store, building, exhibition, city, landscape, machine, or abstract world;
- scroll film: authored scenes and camera states driven by reading progress;
- object theatre: a hero object changes state, scale, material, assembly, or context;
- editorial choreography: typography, imagery, grids, and transitions carry the narrative without heavy 3D;
- infinite canvas / map: users pan or zoom through a connected information space;
- guided exploration: hotspots, rooms, chapters, or stations invite controlled discovery;
- kinetic typography: type becomes the main visual/motion system;
- data/story transformation: maps, diagrams, comparisons, timelines, or metrics evolve as the story advances;
- layered depth: DOM, canvas, video, and WebGL move at different spatial planes;
- generative or reactive visual system: particles, shaders, procedural forms, audio-reactive or pointer-reactive visuals;
- tactile product interface: drag, rotate, reveal, compare, configure, peel, slice, inspect;
- restrained luxury: mostly static composition with a few exceptionally crafted transitions.

## Technology ladder

Pick technology after the concept:

1. semantic HTML/CSS and native browser features;
2. CSS transitions / View Transitions / scroll-driven animations when sufficient;
3. component motion for local state and gestures;
4. GSAP for authored timelines, ScrollTrigger, complex sequencing, pinning, scrub, or cross-element choreography;
5. canvas/WebGL/Three.js for genuinely spatial or shader-driven experiences;
6. Rive/Lottie/video/image sequences when authored assets are a better fit than runtime graphics.

Never add WebGL because it sounds premium.

## Creative constraints

- One dominant idea beats ten unrelated effects.
- The first screen should communicate character before interaction begins.
- Every major transition must either reveal information, change context, reinforce hierarchy, or create a deliberate emotional beat.
- Preserve orientation. Users should understand where they are and how to continue.
- Interactive spectacle must not hide core content from SEO, accessibility, or reduced-motion users.
- Avoid Awwwards-template clichés unless the brand genuinely benefits from them.

## Inspiration without imitation

When external research is available, pair with `design-inspiration-research` before locking the concept. Extract principles, not layouts. Never reproduce one reference wholesale; synthesize across multiple sources and document what was borrowed at the level of pattern, not pixels.

## Pairing

- Always pair non-trivial visual work with `design-taste-frontend`, `impeccable`, and `emil-design-eng`.
- For scroll narratives, add `scrollytelling-web`, `gsap-scrolltrigger`, and `gsap-performance`.
- For spaces and navigable environments, add `threejs-spatial-experiences`.
- For product/object assemblies, add `threejs-product-storytelling`.
- For Figma-driven work, add `figma-design-workflow`.
