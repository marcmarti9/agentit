# Motion, performance, and accessibility

## Motion must be motivated

Before any animation, answer: hierarchy, storytelling, feedback, or state change.  
"Looks cool" is not enough. If you cannot justify it in one sentence, drop it.

When `MOTION_INTENSITY > 4`, the page must **actually move** (hero enter, section reveal, CTA hover at minimum) **or** you lower the dial. Half-broken ScrollTriggers are worse than static.

## Prefer correct tools

| Goal | Prefer | Avoid |
|------|--------|--------|
| Simple enter-on-scroll | Motion `whileInView` / CSS view timelines | Scroll listeners + `setState` |
| Pin / scrub / horizontal pan | GSAP ScrollTrigger or equivalent, with cleanup | `window.onscroll` math |
| Pointer physics / magnetic | Motion values (`useMotionValue` / `useTransform`) | Tracking pointer in React state every frame |
| Layout reflow animation | Motion `layout` / `layoutId` when state changes | Wrapping static trees "for safety" |

Animate **transform** and **opacity** only. No animating `top`/`left`/`width`/`height` for flair.

## Reduced motion (mandatory)

If `MOTION_INTENSITY > 3`:

- Honor `prefers-reduced-motion`
- Collapse infinite loops, parallax, scroll-hijack, and magnetic physics to static/instant
- In Motion: `useReducedMotion()`; in CSS: gate or override under `prefers-reduced-motion: reduce`

## Canonical patterns (sketch)

Sticky stack and horizontal pan need pin at viewport top (`start: "top top"` class of trigger), pin the wrapper, scrub the track, and **revert/cleanup** on unmount. Prefer project-local helpers over pasting large skeletons into every page.

Lighter alternative for lists/grids: stagger `whileInView` with `viewport={{ once: true }}` and a shared easing curve such as `[0.16, 1, 0.3, 1]`.

## Marquee

At most one marquee per page. Infinite logo strips are filler when repeated.

## Core Web Vitals targets

- LCP < 2.5s — prioritize hero media
- INP < 200ms — keep heavy work off the main thread
- CLS < 0.1 — reserve space for images, fonts, embeds

Grain/noise: fixed, non-interactive overlay only — never on scrolling content containers.

## Accessibility checklist (marketing pages)

- Keyboard reachability for all interactive controls
- Visible focus styles
- AA contrast for body and controls (AAA target for hero copy when feasible)
- Meaningful alt text; decorative images empty alt
- Do not rely on color alone for state
- Form errors associated with fields
- Skip link or equivalent landmark structure when the page is long

Product-component depth (ARIA patterns, focus traps): `frontend-ui-engineering` and project a11y checklists.
