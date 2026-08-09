---
name: threejs-product-storytelling
description: Premium Three.js / React Three Fiber product visualization for web storytelling: GLB/glTF scene structure, exploded views, camera direction, lighting, materials, scroll coupling, labels, post-processing, responsive degradation, and GPU validation.
license: MIT-inspired-original
research: https://github.com/scottstts/Threejs-Awesome-Graphics-Agent-Skills
---

# Three.js Product Storytelling

Use when the web experience genuinely needs spatial product visualization: exploded assemblies, camera travel, depth, realistic materials, product rotation, part isolation, or scroll-driven 3D storytelling.

Do not use Three.js as a prestige dependency. A pre-rendered sequence or DOM/CSS composition is better when it communicates the same thing with less complexity.

## Asset-first thinking

A premium scene starts with a usable model.

Prefer GLB/glTF with:

- semantic node/group names;
- separate meshes for independently animated parts;
- pivots placed where rotations/separations should originate;
- sane scale and orientation;
- PBR material inputs where realism matters;
- compressed, web-appropriate texture sizes;
- no accidental millions-of-polygons CAD dump.

Inspect the model hierarchy before coding the animation. If the asset cannot support the requested decomposition, fix the asset/hierarchy rather than writing increasingly fragile coordinate hacks.

## Framework choice

- Existing React/Next project with a substantial 3D scene → React Three Fiber is usually the ergonomic choice.
- Framework-agnostic/small scene → vanilla Three.js can be simpler.
- Do not migrate an existing stable Three.js scene solely for preference.

Keep the 3D scene isolated from unrelated UI. HTML overlays, content semantics, and navigation should remain normal DOM unless they truly need to exist in 3D.

## Scene direction

Treat the camera like cinematography, not a debug orbit controller.

Define authored shots/states:

- establishing view;
- focus/inspection view;
- exploded/technical view;
- hero/final view.

Use focal length/FOV, camera distance, object scale, negative space, and lens changes deliberately. Avoid gratuitous orbiting that makes the product harder to read.

## Exploded assemblies

For each semantic part or assembly define:

- intact local transform;
- exploded local transform;
- explosion vector/axis;
- optional rotation/focus change;
- chapter timing window;
- label/annotation relationship.

Explosion vectors should reflect how the object is built or understood. Random outward vectors read as a technical demo, not product storytelling.

Keep related parts grouped. Move assemblies first, subparts second when that mirrors the product hierarchy.

## Scroll coupling

The scene should consume a semantic progress/timeline from `scrollytelling-web`, not own ad-hoc window scroll listeners.

Map named narrative phases to scene transforms. GSAP can animate object/camera numeric properties when the project uses ScrollTrigger; React Three Fiber can consume normalized progress without forcing React re-renders every frame.

Reverse scroll must produce a valid reverse narrative.

## Lighting

Lighting is the primary visual-quality multiplier.

- Start with a readable key/fill/rim or environment strategy appropriate to the product.
- Use environment reflections for materials that need them, but do not let an HDRI choose the composition for you.
- Preserve form edges and material separation.
- Contact shadows/grounding matter for hero products.
- Avoid uniformly lighting every surface; shape needs contrast.

## Materials

Match the actual product language: anodized metal, glass, plastic, rubber, fabric, paint, ceramic, etc. Tune roughness/metalness/transmission/IOR/normal detail with physical plausibility as a starting point.

Avoid default “shiny sci-fi black + neon emissive” unless the brand/product calls for it.

## Post-processing

Post-processing should finish the image, not rescue bad lighting.

Use bloom, depth of field, vignette, chromatic effects, grain, or color grading sparingly and with a reason. Preserve a strong no-post baseline first.

## Labels and technical callouts

Prefer DOM overlays for readable text/interactive callouts unless labels must be occluded in the scene. Anchor them to projected 3D positions and prevent obvious collisions/clipping.

Do not rotate long paragraphs in 3D space.

## Performance

- Cap DPR deliberately (`Math.min(devicePixelRatio, budget)` style policy).
- Compress geometry/textures when supported by the pipeline.
- Lazy-load the heavy scene and provide a stable poster/skeleton state.
- Render on demand when continuous animation is unnecessary.
- Pause/reduce work when offscreen.
- Dispose GPU resources during teardown.
- Keep transparent layers and post-processing under control.
- Use LOD / simpler assets when scene scale justifies it.

Pair with `gsap-performance` for animation-heavy pages.

## Mobile strategy

Do not merely shrink the desktop canvas. Decide which story survives:

- simpler camera path;
- fewer independently animated parts;
- lower DPR/texture quality;
- shorter sequence;
- pre-rendered video/image sequence;
- static exploded diagram.

The mobile user should still understand the product.

## Accessibility

The product facts communicated by the scene must also exist in semantic DOM content. Reduced-motion can freeze at meaningful chapter states or replace the scrub with static diagrams/cards.

Never require aggressive camera motion to access essential information.

## Validation

Validate fixed narrative checkpoints with screenshots/captures, not just free-orbit inspection. Check:

- intact silhouette and material readability;
- each exploded phase;
- labels at target viewports;
- camera clipping;
- reverse scroll;
- GPU/frame pacing;
- mobile fallback;
- reduced-motion path;
- teardown/navigation memory behavior.

## Research attribution

This is an original Agentit skill informed by the MIT-licensed `scottstts/Threejs-Awesome-Graphics-Agent-Skills` project's graphics-quality philosophy and validation emphasis. It does not vendor that repository's specialist implementation examples.
