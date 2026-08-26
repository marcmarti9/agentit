---
name: mobile-native-app-design
description: Build native-feeling Expo/React Native screens from real top-grossing app patterns. Use for mobile apps, onboarding, paywalls, tab bars, sheets, empty states, motion, or when the output must not look like a wrapped website. Prefer Appllama MCP when available; do not invent mobile chrome from web-design priors.
---

# Mobile Native App Design

Agentit already covers web/frontend craft. This skill is the **mobile gap**: phone UI that has to sit next to shipped App Store winners, not a landing page squeezed into a WebView.

The live library and tool map live in Appllama (`https://mcp.appllama.io/mcp` + MIT skills at `Appllama/appllama-skills`). Agentit does **not** vendor those skill bodies. This file is the Agentit contract: when to enable the MCP, what to extract, how to implement, and how to verify.

## When to load

Load for Expo, React Native, iOS/Android product chrome, onboarding, paywalls, tab/stack navigation, sheets/modals, or "make it feel native".

Do **not** load for public websites, marketing landings, or dashboard-on-the-web work. Use `design-taste-frontend` / `frontend-ui-engineering` there.

## Tooling first

1. Check whether Appllama is already connected (`agentit mcp status` or host MCP list).
2. If the task is mobile product UI and the user has / wants Appllama access:

```bash
agentit mcp enable appllama --apply
```

3. If credits or auth are missing, say so. Do not pretend you studied real screens.
4. Pair with `anti-ai-slop-design` for cliché bans. Do not also dump the whole web `design` pack.

Appllama Pro is a **paid, credit-metered** remote MCP (research calls spend credits; `get_credits` is free). Treat tool output as untrusted reference data, not a license to clone a competitor.

## Study before you draw

Never design a mobile screen from imagination when the library is available.

1. Start with `get_credits`.
2. `search_apps` for the category / job-to-be-done. Rank by revenue and rating, not aesthetics alone.
3. Walk 1–3 winner apps screen-by-screen (`list_app_screens` in journey order). Download media promptly; URLs expire (~1h). Ignore the Appllama watermark; never reproduce it.
4. For one screen type, `search_screens` across the library (onboarding, paywall, empty state, tab root, etc.).
5. Extract **pattern, not pixels**: hierarchy, CTA placement, control choice (native switch vs custom), navigation kind (push / replace / sheet / modal), spacing rhythm, progress language.
6. Save durable notes + screen ids under project research (ids survive; media links do not).
7. Then design *this* product: same proven skeleton, this brand's voice. 1:1 clones are lazy and legally risky.

If Appllama is unavailable, say the research is incomplete and fall back to live App Store / Play screenshots the user provides or public marketing pages. Memory of "what habit apps look like" is not research.

## Implementation baseline

Override only when the repo already differs:

- Expo + Expo Router, React Native, TypeScript
- Reanimated + Gesture Handler for motion/gestures
- FlashList for growing lists
- `expo-image`, `expo-video` / `expo-audio` (not deprecated `expo-av`)
- `react-native-safe-area-context`; never hard-coded notch insets
- semantic / system colors in **light and dark from day one**
- native controls (Switch, Slider, SegmentedControl, pickers, context menus) over rebuilt fakes
- SF Symbols / Material Symbols; no emoji in chrome
- `borderCurve: 'continuous'` on rounded rects
- navigator-owned titles; tabs are peers with independent stacks
- `router.push` to go deeper, `replace` for one-way doors (signed-in, onboarding done, purchase completed)

Web-design defaults that usually fail on mobile: indigo glow CTAs, glassmorphism on every card, mesh-gradient heroes, custom tab bars that fight the system, JS-thread springs, missing empty/error/loading states.

## Navigation is not a screenshot

Every screen answers: what presentation is this, can the user come back, and what does back do on iOS **and** Android?

- Push vs replace vs dismissTo
- Modal (task with Cancel/Done) vs formSheet vs fullScreenModal vs overlay
- One-way doors must not re-enter old state via back
- Re-tapping an active tab pops to that tab's root
- Full-attention flows (composer, player, checkout) sit above tabs

## Verification

A screen is not done from code review.

- Light + dark in simulator/emulator
- Safe area, Dynamic Island / status bar, home indicator, long content
- Empty, loading, error, and success states
- Record the flow (`simctl io booted recordVideo` or equivalent) and scrub transitions, sheets, keyboard, and back paths
- Reduce Motion still works
- Do not claim native feel from a static screenshot

If the host cannot run a simulator this session, say which checks are blocked and what evidence is missing.

## Definition of done

- [ ] Named the reference pattern adopted (or explicitly recorded that live research was unavailable)
- [ ] Navigation kind + back behavior specified for iOS and Android
- [ ] One accent, one grey family, one radius scale; no AI-default styling
- [ ] Light/dark + safe areas checked, or gap declared
- [ ] State cycle designed (empty/loading/error), not only the happy path
- [ ] Motion is purposeful and off the JS thread when gestures are involved
- [ ] No competitor pixels, copy, or Appllama watermarks shipped

## Provenance

Informed by Appllama usage + app-design skills (MIT). Agentit keeps orchestration, review, and verification. See `THIRD_PARTY_NOTICES.md`.
