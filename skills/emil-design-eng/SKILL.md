---
name: emil-design-eng
description: Design-engineering craft inspired by Emil Kowalski's public skills: UI polish, component behavior, animation decisions, perceived performance, and invisible interaction details. Use for product UI, interaction polish, micro-interactions, motion critique, and final craft passes.
license: MIT
source: https://github.com/emilkowalski/skills
---

# Emil Design Engineering

Agentit adaptation of Emil Kowalski's MIT-licensed design-engineering skill. Quality wins over token economy: read the relevant sections before editing and apply the rules as a coherent craft system, not a checklist pasted onto an interface.

## Core stance

Functional is the floor. The goal is an interface whose invisible details compound into something that feels obvious, fast, physical, and intentional.

Taste is trained. Inspect excellent interfaces, identify why they work, and reproduce principles rather than surface decoration. Beauty is leverage only when it improves the experience; decorative cleverness that makes repeated actions slower is a regression.

## Animation decision framework

Before animating anything, answer in order:

1. **Should it animate?** Frequent actions should be instant or nearly instant. Keyboard-driven and high-frequency actions should normally not animate. Rare, explanatory, spatial, onboarding, or celebratory moments can carry more motion.
2. **Why does it animate?** Valid reasons include spatial continuity, state explanation, feedback, hierarchy, and preventing a jarring change. “Because it looks cool” is insufficient for recurring product UI.
3. **What motion model fits?** Entrances/exits generally favor a decisive ease-out; on-screen repositioning favors ease-in-out or a well-tuned spring; continuous progress favors linear mapping; gestures favor interruptible springs.
4. **How long?** Product UI should feel immediate. Small feedback is typically ~100–180 ms, popovers ~125–220 ms, selects/dropdowns ~150–250 ms, and larger drawers/modals ~200–500 ms. Marketing explanations can be slower when narrative requires it.

Prefer strong custom curves or physical springs over weak browser defaults. Never add `ease-in` to an interaction merely because it is available; delayed initial response makes UI feel sluggish.

## Interaction craft

- Pressable controls need tactile active feedback when appropriate (`scale(.97)` is a useful starting point, not a law).
- Avoid `scale(0)` entrances. Start from a nearly-real scale plus opacity so the object appears to have continuity.
- Popovers should transform from the trigger/origin when the primitive exposes it. Centered modals remain centered.
- Once a tooltip cluster is active, neighboring tooltips should become effectively instant rather than repeatedly charging an entrance delay.
- Prefer interruptible transitions/springs for interactions users may reverse quickly.
- Use subtle blur only as a transition bridge when crossfades expose two competing states; never hide fundamentally bad choreography under expensive blur.
- Prefer transforms and opacity for hot animation paths. Do not animate `transition: all`.
- Continuous pointer/scroll values must not be pushed through React state every frame. Use motion values, refs, GSAP, CSS scroll timelines, or another animation primitive designed for continuous values.

## Perceived performance

A responsive-looking system is part of actual usability. Immediate visual acknowledgement, fast first movement, skeleton/progress behavior that matches reality, and no gratuitous waiting animation all affect perceived latency.

Never fake progress or introduce animation that delays completion. The visual layer may explain waiting; it must not create it.

## Component quality floor

For every component touched, inspect:

- default, hover, focus-visible, active, disabled, loading, success, empty, and error states as applicable;
- keyboard and pointer behavior;
- touch target size and coarse-pointer behavior;
- origin and direction of overlays;
- truncation/wrapping with real long content;
- responsiveness from narrow mobile through wide desktop;
- reduced-motion behavior;
- visual continuity when content changes size;
- alignment of icons, text baselines, radii, borders, and shadows.

Do not hand-wave missing states as “polish later.” These are part of the design.

## Motion review

When reviewing existing motion, produce a concrete diagnosis before changing code. For each issue state the current behavior, proposed behavior, and why it improves feel. Pay special attention to:

- unnecessary motion on frequent actions;
- weak easings;
- durations that make controls feel delayed;
- wrong transform origins;
- elements materializing from nowhere;
- animations that cannot be interrupted;
- layout-triggering properties on hot paths;
- choreography where multiple elements compete for attention;
- motion that breaks on mobile or ignores reduced-motion.

## Marketing vs product UI

Product UI optimizes for repeated use, speed, clarity, and interruption. Marketing UI can spend more motion budget on explanation and memorable transitions. Do not transplant cinematic landing-page animation into a command palette, settings panel, or table.

For scroll-linked cinematic work, pair this skill with `scrollytelling-web`, `gsap-scrolltrigger`, and `gsap-performance`. For visual art direction, pair with `design-taste-frontend` and `impeccable-design`.

## Verification

Do not declare interaction polish from code inspection alone when a browser is available. Verify the actual interface at desktop and mobile widths, exercise the interaction repeatedly, inspect console/runtime errors, and confirm reduced-motion behavior.

## Attribution

Derived and adapted from the public MIT-licensed `emilkowalski/skills` repository by Emil Kowalski. Preserve this attribution when redistributing substantial portions of this skill.
