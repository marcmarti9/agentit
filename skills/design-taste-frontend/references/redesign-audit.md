# Redesign audit protocol

Use when the task is improve/restyle an **existing** site or app shell surface — not greenfield.

## 1. Inventory before paint

Record:

- Brand assets already in use (logo, colors, type, photography)
- Layout patterns that work (keep) vs patterns that fail (fix)
- Technical constraints (framework, CSS system, CMS, no-break routes)
- Preserve vs overhaul intent from the user

## 2. Severity-ordered issues

List concrete problems with evidence (screenshot, DOM, CSS token):

1. Hierarchy / readability failures
2. Spacing inconsistency / density wrong for audience
3. AI-tell clutter (see `ai-tells.md`)
4. Contrast / focus / keyboard gaps
5. Motion that hurts or is broken
6. Component duplication / one-off styles

## 3. Choose dials from existing DNA

- **Preserve:** match variance/density; motion +1 max for polish
- **Overhaul:** variance/motion may rise; keep density closer to current product unless the brief changes audience

State design read + dials before code.

## 4. Change in vertical slices

Prefer section-by-section or route-by-route:

1. Tokens / type / color first when global
2. Hero + nav (first impression)
3. Highest-traffic sections
4. Secondary pages

Avoid big-bang CSS rewrites without visual regression checks.

## 5. Verify

- Side-by-side before/after for each changed section
- Responsive spots: 320 / 768 / 1024 / 1440
- Reduced motion + contrast
- No regressions in forms, auth, or critical CTAs

Stop when acceptance criteria for the redesign scope are met — do not "finish the whole product" unprompted.
