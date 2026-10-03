---
name: typography-and-layout
description: Establish or review typography, reading measure, hierarchy, and responsive text layout for a web surface or document specification. Use for type decisions that affect legibility and page rhythm; do not use for brand-wide identity, component-system architecture, or printer preflight.
license: Apache-2.0
---

# Typography and Layout

Make text serve reading, hierarchy, and the real medium. This skill owns the typographic
specification and its rendered proof, not a brand identity, a component library, copy editing,
or an editable-file production workflow.

## Use when

- A page, report, or interface needs a type hierarchy, text measure, or spacing rhythm.
- An existing design is hard to scan, tiring to read, or breaks at narrow widths.
- A supplied brand specifies faces but not their use, fallbacks, scale, or proof.

## Do not use when

- Defining a logo, imagery, colour, or cross-media brand system: use `brand-identity-design`.
- Creating component tokens, component APIs, or migration governance: use
  `design-system-engineering`.
- Preparing editable DOCX/PPTX/PDF files or claiming a print-ready deliverable: use the
  artifact-production owner; involve `editorial-design` for reading direction.
- Correcting prose meaning, citations, or locale rules: return that work to the content owner.

## Inputs and boundary

Record the content class, target widths or page sizes, audience, required scripts, brand rules,
delivery medium, and available font-rights evidence. Treat a binding brand guide as a constraint,
not as a reason to invent a replacement. If faces, rights, script coverage, or stable content are
unknown, write a provisional specification and name the gap; do not make a release claim.

## Procedure

1. Inspect the actual content and its reading task. Identify body text, headings, labels, data,
   captions, code, and any non-Latin or numeric needs. Select the fewest roles that communicate
   the structure.
2. Honour approved faces. Otherwise choose families for legibility, available real styles,
   coverage, and licensed use. State why each role exists and give a metric-compatible fallback.
   Do not ban fonts by reputation, require paid-font hunting, or prescribe a fixed number of faces.
3. Define a role scale from the content and available space. Establish body size, line-height,
   weights, and spacing as named decisions; use discernible hierarchy rather than a universal
   ratio. Use real italic/bold files only.
4. Set the reading column from representative content. Constrain continuous prose to a comfortable
   measure appropriate to language, font metrics, and medium; let tables, diagrams, and code use
   a separately justified width. Choose paragraph spacing or first-line indents, never both by
   reflex.
5. Establish vertical rhythm. Tie heading margins, caption spacing, lists, controls, and figures
   to a small set of spacing decisions. A heading should visibly belong to the content it opens.
6. Design responsive behaviour from the actual breakpoints or containers. Preserve a side gutter,
   avoid accidental tiny type, allow long labels to wrap deliberately, and recompose dense data
   rather than shrinking it mechanically.
7. Specify font loading or embedding only where rights and the target format permit it. Record
   family/version, files, fallback, and any subset scope. A local preview does not prove embedding.
8. Render representative dense, sparse, long-label, and narrow cases. Inspect overflow, hierarchy,
   contrast, focus visibility where interactive, line length, and whether the fallback changes
   layout materially.
9. Deliver a compact type-and-layout record: roles, fonts/rights status, scale, measure, spacing,
   responsive rules, rendered evidence, and unresolved constraints.

## Decision rules

| Condition | Choose | Evidence |
|---|---|---|
| Sustained prose | A constrained reading column and generous enough leading | Rendered lines and sample content |
| Dense UI labels | Role-specific sizes with wrapping/truncation rules | Narrow-width render |
| Table or code exceeds prose measure | A deliberate overflow, scroll, or breakout treatment | No clipped content or lost association |
| Rights or glyph coverage are unresolved | A conditional spec or permitted substitute | Recorded rights/coverage gap |
| Justified narrow text produces rivers | Ragged setting or a revised measure | Re-rendered paragraph shape |

## Craft checks

- Heading levels are distinguishable without relying only on colour.
- Body text, captions, controls, and tables remain legible at the stated targets.
- Numeric figures match their task: aligned figures for columns, text figures where appropriate.
- Hyphenation, quotes, dashes, dates, and language conventions come from the approved house style;
  never assume a locale default.
- No synthetic bold, fake italic, manual line breaks, decorative all-caps paragraphs, or
  unexplained tracking repairs substitute for sound styles.

## Handoff

Give the implementer a role table, stylesheet or token location, representative content samples,
font asset/rights status, and the exact widths or formats reviewed. Give the content owner every
copy change request separately, since typographic repair must not quietly alter approved meaning.

## Common failures

- Choosing a typeface because it is fashionable instead of proving it serves the actual script,
  density, and medium.
- Treating an unverified fallback as a finished visual decision.
- Applying desktop line lengths and gaps unchanged to a narrow viewport.
- Calling an unrendered style sheet accessible, embedded, or print-safe.

## Evidence and degradation

Claim a rendered result only after inspecting the target render. If a renderer, stable copy, font
files, or target device is unavailable, deliver CSS/token or document-style guidance plus a
pending verification matrix. Do not infer visual fidelity, licensing, print behaviour, or browser
support from source text alone.

## Acceptance

- The decision record names roles, constraints, fallback, measure, hierarchy, and responsive
  behaviour.
- Representative renders show readable text without unintended overflow or hierarchy collapse.
- Rights, script coverage, and any untested conditions are explicit.
