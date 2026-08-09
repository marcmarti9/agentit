---
name: threejs-spatial-experiences
description: Build premium navigable or guided 3D web environments such as stores, galleries, buildings, rooms, exhibitions, landscapes, and spatial brand journeys. Use when the experience is about moving through space rather than inspecting one product.
---

# Three.js Spatial Experiences

Create spatial web experiences that feel authored, legible, and intentional. Avoid the default "orbit-controls demo with a model in the middle" aesthetic.

## Start with the spatial narrative

Define:

- entry point and first reveal;
- destination or sequence of spaces;
- camera language: on-rails, free-look, constrained walk, orbit at stations, dolly, crane, spline, teleport, or hybrid;
- points of interest and what each one teaches/reveals;
- transitions between spatial scenes and DOM content;
- exit/CTA;
- mobile and reduced-motion alternative.

Draw a simple scene graph and camera path before polishing materials.

## Camera systems

Choose deliberately:

- on-rails spline for cinematic tours and predictable storytelling;
- scroll-to-camera mapping for guided spatial narratives;
- hotspot/waypoint transitions for stores, museums, and room-to-room exploration;
- constrained first-person only when free exploration creates real value;
- hybrid authored/free-look when users should inspect a scene without getting lost.

Camera movement should ease through position, target, FOV, and roll as a coherent shot. Avoid nausea-inducing rotation, arbitrary acceleration, and dead time.

## Environment craft

- Use GLB/glTF with intentional hierarchy, naming, pivots, and scale.
- Prefer baked lighting/lightmaps for static interiors when it materially improves mobile performance.
- Use a clear lighting hierarchy: environment/key/fill/accent rather than many arbitrary lights.
- Keep materials physically plausible unless the art direction calls for stylization.
- Use reflections selectively; expensive realism that tanks frame time is not premium.
- Treat fog, depth, portals, occlusion, and reveal timing as composition tools.

## Interaction patterns

Consider:

- room/station hotspots;
- product shelves that transition from 3D context to readable DOM detail;
- guided paths with optional detours;
- doors/elevators/portals as chapter transitions;
- contextual labels anchored in screen-space HTML;
- click/hover/raycast affordances with obvious focus states;
- minimap/progress/chapter navigation when orientation would otherwise suffer.

Do not force WASD controls into a normal marketing site.

## Performance architecture

Budget before building the final scene:

- texture dimensions and compression;
- polygon count and draw calls;
- instancing for repeated geometry;
- LOD for large scenes;
- frustum/occlusion-aware rendering where useful;
- lazy scene/asset loading by chapter;
- capped device pixel ratio;
- compressed GLB/textures where supported;
- dispose geometry/materials/textures on teardown;
- avoid per-frame React state churn.

Pair with `gsap-performance` and verify on a representative mobile device/profile, not only a desktop GPU.

## DOM + WebGL integration

Important copy, navigation, forms, pricing, and calls-to-action should normally remain semantic DOM. Let WebGL provide the spatial layer while HTML provides readability, accessibility, and robust interaction.

Transitions between DOM and 3D should feel continuous: shared visual anchors, matching camera/object motion, controlled fades/masks, and stable layout.

## Fallback contract

The experience must retain its story when WebGL is unavailable, reduced motion is requested, battery/GPU is weak, or the viewport is small. Use stills, video, image sequences, chapter cards, or simplified camera states rather than presenting a broken miniature version of desktop.

## QA

Test the full journey for:

- camera clipping and geometry intersections;
- accidental navigation traps;
- asset pop-in;
- text contrast against changing backgrounds;
- hotspot hit targets and keyboard access;
- resize/orientation changes;
- tab visibility pause/resume;
- loading/retry behavior;
- memory leaks after route changes;
- frame pacing, not just average FPS.

## Pairing

Use `creative-web-experiences` to decide whether a spatial concept is appropriate. Use `scrollytelling-web` + GSAP if scroll drives the route. Use `threejs-product-storytelling` when a specific object becomes the main subject rather than the environment itself.
