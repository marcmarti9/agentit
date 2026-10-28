---
name: high-end-motion-video
description: |
  Design and build high-end motion videos entirely in code (GSAP + Three.js or equivalent) with independent critic loops, measurable quality bar, and honesty constraints.
  Use when the task is to produce a finished motion film, product video, showreel, explainer or launch story that must hold up next to professional references.
  Not for simple edits, static assets, or when a lower-fidelity renderer is sufficient.
license: Apache-2.0
---

# High-End Motion Video

Own the full production of a motion video that is judged against the best work in the references, not merely against "no bugs".

This skill sits above ordinary advertising or UI motion. It enforces a critic that has never seen the building process, a measurable quality bar, and strict separation between measured facts and claims that still need a human.

## When to use

- Product launch films, showreels, explainers or brand motion that must feel premium.
- Tasks that explicitly ask for GSAP / Three.js / code-driven animation with a high quality bar.
- When the user provides style references and wants the output to hold up next to them.

Do not use for:
- Quick social cuts or simple captioned footage.
- Pure UI micro-interactions (prefer existing GSAP or frontend skills).
- Tasks where the user has already approved a lower-fidelity pipeline.

## Core contract

```text
brief + facts file + style references
        ↓
storyboard (critic) → shared tokens & handoffs
        ↓
parallel scene components (each with own critic)
        ↓
full render → fresh critic (sound-off + fact check + director)
        ↓
quality bar pass or one more loop
        ↓
deliverables + ledger
```

## Brief and facts

Require (or derive and document) before any animation:

- mode: showreel | product | launch-story | explainer
- viewer and desired end state
- length, aspect ratios, frame rate
- brand tokens (colours, fonts, logo files)
- **facts file**: the only source for numbers, names or claims that appear on screen
- assets and style references

Write `facts.json` with every claim, its exact source sentence and URL. Nothing invented (testimonials, ratings, prices, results, real people). Generated material is labelled.

## Motion principles (non-negotiable)

1. The thing in front of the shot becomes the transition. A title, logo or object moves toward camera while the next scene waits underneath.
2. One object carries the story across shots and keeps its identity.
3. One main movement leads; secondary movements layer under it and overlap. The frame never stops and starts all at once.
4. Speed always changes. Things land slowly enough to read, leave fast. No linear easing.
5. Cuts only when size, direction and subject match on both sides, and only on a beat.
6. Every action produces a visible result.
7. Type is motion. Big words enter from opposite sides, reveal the next scene, never sit over busy picture without a plate.
8. Vary scale: close, wide, overhead, full-frame type. Never repeat the same layout.

Frame one is a finished picture. The video must make sense with the sound off.

## Build rules

- Every animated value is a pure function of timeline time. No timers, no unseeded randomness.
- Shared pieces first: colours, fonts, shared 3D models, exact pixel positions of every handoff.
- Each scene is its own component with its own test page. Render stills and a short clip; send to a critic before it joins the film.
- Carried objects land on exactly the same pixels on both sides of a cut.
- Prefer building shots in code. Generated images only as supporting references; label them.
- 3D only where it explains something spatial. Product-shoot lighting, camera 35–55°, real materials, HTML labels tracked from the scene.

## Critic loop

The builder never judges its own work.

After the storyboard, after each major component, and after every full render:

- Send the render, the brief and the references to a **fresh critic** that has seen none of the building.
- The critic pulls its own frames (every 0.2 s + dense around transitions), measures frozen time and loudness, and returns a ranked list of problems with timestamps.
- Ends with "ship" or "one more pass".
- Additional checks on full renders: sound-off retelling, beat sync within 1 frame, fact check against facts.json, director's review of what feels assembled or generic.

Keep a ledger of every round: what was found, what changed, numbers before and after.

## Quality bar (must all pass)

Measured:
- Exact duration, size and frame rate.
- Frame one finished.
- ≤1 s frozen per 30 s; no still stretch >0.5 s.
- Text contrast ≥4.5:1, no collisions, inside safe margins.
- Brand colours match in the render.
- Cuts and hits within 1 frame of the beat.
- Loudness ~−14 LUFS, no clipping, effects below music and voice.
- Understood with the sound off.
- Every claim in facts.json.

Judged: a critic would put it beside the references without it looking weaker.

## Audio

- Music matches energy and sits low. Prefer clean library tracks.
- One soft whoosh per real scene change; small clicks only on real on-screen actions.
- Cut every scene change on a beat.
- Always export a music-only version.

## Deliverables

- Final MP4 per requested size/aspect (1080p 60 fps default for UI/product).
- Music-only version.
- Contact sheet of the final video.
- brief.md, facts.json, style bible, timing.json, ledger.md.
- Quality-bar results and a short note on anything a human should still check by eye and ear.

## Relationship to other skills

- Prefer this skill over `advertising-video-production` when the quality bar and critic loop are required.
- Compose with existing GSAP / Three.js skills for implementation details.
- Use `humanizer` only on spoken or on-screen copy if the brief demands it; facts stay untouched.
