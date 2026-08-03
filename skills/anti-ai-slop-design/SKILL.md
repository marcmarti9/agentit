---
name: anti-ai-slop-design
description: Prevent generic AI design slop (purple glows, generic cards, boring typography, lifeless layouts). Enforce distinctive visual identity, curated color systems, and micro-interactions.
---

# Anti-AI-Slop Design System

## Core Directive

Reject cookie-cutter AI aesthetic tropes. Create UIs with distinct personality, intentional typography, harmonious color palettes, and polished micro-interactions.

## Anti-Patterns to Avoid

| Slop Pattern | Why it Feels AI-Generated | Better Alternative |
|---|---|---|
| **Purple/Indigo Glow Overuse** | Linear `#6366f1` gradient buttons on dark backgrounds | Curated HSL/OKLCH color themes tailored to the brand |
| **Identical Rounded Cards** | Generic `border-radius: 12px` cards with standard shadows | Purpose-built layouts with varied scale, depth, and glassmorphism |
| **Default Inter Typography** | Using browser default Inter without weight contrast | Paired typography (e.g. Outfit / Space Grotesk for headers + Inter for body) |
| **Lifeless Hero Sections** | Centered text + generic CTA button + floating laptop mock | Interactive previews, live code snippets, or dynamic micro-animations |
| **Static State Feedback** | Instant hover states without transition curves | Smooth micro-interactions (`transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1)`) |

## Design Checklist

- [ ] **Color Palette**: Is there a primary, secondary, surface, and accent color with proper WCAG contrast?
- [ ] **Visual Hierarchy**: Are font size ratios clear (e.g., H1: 2.5rem, H2: 1.75rem, Body: 1rem)?
- [ ] **Micro-Interactions**: Do buttons have active/press scaling states (`transform: scale(0.98)`)?
- [ ] **Dark & Light Themes**: Are CSS custom properties used for dynamic theme switching?
- [ ] **No Generic Assets**: Are placeholders replaced with tailored visual demonstrations?
