---
name: anti-ai-slop-design
description: Prevent generic AI design slop (purple glows, generic cards, boring typography, lifeless layouts). Enforce brand-authentic visual identity, curated color systems, and responsive typography.
---

# Anti-AI-Slop Design System

## Core Directive

Reject cookie-cutter AI aesthetic tropes. Design UIs that reflect the specific brand identity, product context, and audience needs rather than applying repetitive AI visual clichés.

## Principles Over Dogma

1. **Context Over Trends**: Do not blindly apply glassmorphism, dark modes, or specific font pairs (e.g. Space Grotesk) to every product. A medical dashboard needs high contrast and legibility; a gaming app needs vibrant energy.
2. **Intentional Hierarchy**: Use visual scale, whitespace, and font weight to guide the user's eye naturally to the primary action.
3. **Responsive Micro-Interactions**: Use subtle motion to confirm user intent without causing distraction or layout shifts.

## Anti-Patterns to Avoid

| Slop Pattern | Why it Feels AI-Generated | Better Alternative |
|---|---|---|
| **Purple/Indigo Glow Overuse** | Linear `#6366f1` gradient buttons on dark backgrounds | Brand-curated HSL/OKLCH color themes matched to product identity |
| **Identical Rounded Cards** | Generic `border-radius: 12px` cards with standard heavy shadows | Layout structures tailored to the content type and visual hierarchy |
| **Default Inter Typography** | Using browser default Inter without font weight contrast | Intentional font pairing and scale tailored to readability and brand voice |
| **Lifeless Hero Sections** | Centered text + generic CTA button + floating laptop mock | Product-relevant interactive previews, live data, or functional widgets |
| **Static State Feedback** | Instant hover states without transition curves | Smooth micro-interactions (`transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1)`) |

## Design Checklist

- [ ] **Brand Authenticity**: Does the visual theme match the specific product domain?
- [ ] **Color Contrast**: Is WCAG AA contrast satisfied across light and dark modes?
- [ ] **Visual Hierarchy**: Is the primary call-to-action distinct from secondary controls?
- [ ] **Micro-Interactions**: Do interactive elements provide instant tactile feedback?
