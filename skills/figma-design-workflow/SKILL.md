---
name: figma-design-workflow
description: Use the official Figma MCP as design context and design-system authority for design-to-code, code-to-Figma, component mapping, variables, assets, and collaborative visual iteration.
---

# Figma Design Workflow

Figma is not a screenshot oracle. When a Figma file, selection, component library, design system, or design handoff exists, use the official Figma MCP to retrieve structured design context and preserve the intent encoded in variables, components, layout, assets, and Code Connect mappings.

## Connection policy

Prefer Figma's official **remote MCP** (`https://mcp.figma.com/mcp`) and its OAuth flow. Do not store Figma credentials in the repository.

Before a Figma-dependent task, inspect Agentit MCP state. If Figma is not configured, use Agentit's MCP catalog/setup path rather than silently approximating a referenced design.

Useful current client setup patterns:

- Claude Code: `claude mcp add --transport http figma https://mcp.figma.com/mcp`
- Codex CLI: `codex mcp add figma --url https://mcp.figma.com/mcp`
- Cursor/other MCP clients: configure the remote HTTP URL using the client's supported remote-MCP flow.

Authentication/available tools are controlled by Figma and the user's seat/permissions. Treat missing write capabilities as a real constraint, not an error to work around with unofficial write automation.

## Design-to-code workflow

When implementing from Figma:

1. Resolve the exact frame/selection whenever possible instead of reading an entire large file.
2. Retrieve structured design context: hierarchy, layout, sizes, spacing, typography, colors/variables, components, and relevant assets.
3. Check Code Connect/component mappings when available. Prefer the project's actual implementation component over regenerating a lookalike.
4. Inspect existing repository tokens/components before creating new ones.
5. Build the smallest reusable component structure that preserves Figma semantics without overfitting to one frame.
6. Compare the rendered implementation against the intended frame at the relevant viewport(s).
7. Fix systemic mismatches (tokens/layout/type) before pixel-level local patches.

Do not convert every Figma group into a React component. Component boundaries should follow reusable behavior/semantics, not raw layer nesting.

## Design-system authority

When Figma and code disagree, determine which side is authoritative for this project before normalizing differences. Common cases:

- Figma is current source of truth → update implementation to match.
- Code/design tokens are authoritative and Figma is stale → preserve code and report drift.
- Both are evolving → use Code Connect/mapped components and identify the discrepancy instead of inventing a third version.

Never silently introduce near-duplicate colors, spacing values, radii, or components because a frame is one pixel off an existing token.

## Assets

Use Figma-provided assets/export paths when the MCP exposes them. Preserve SVG/vector assets where appropriate, image crop intent, aspect ratio, and accessibility semantics.

Do not rebuild a real illustration/product image from nested CSS `div`s just to imitate a screenshot. If the asset is absent, keep a clearly named asset slot or use the project's approved asset-generation workflow.

## Figma write / code-to-Figma

When the official MCP exposes write-to-canvas or live-UI capture capabilities and the user wants a Figma artifact:

- write native editable Figma structures, not a flattened screenshot;
- reuse the file's existing components, styles, and variables when possible;
- make bounded, reviewable changes to shared design files;
- avoid destructive rewrites of team-owned libraries;
- if capturing an implemented page back into Figma is supported, use it to close the design/code loop and then review the resulting structure.

Do not claim write support when the current seat/tool surface is read-only.

## Figma + Agentit design stack

For serious frontend design work, Figma context should normally be paired with:

- `design-taste-frontend` for art direction;
- `impeccable` for craft and critique;
- `emil-design-eng` for interaction polish;
- `browser-testing-with-devtools` / Playwright for implementation verification;
- `scrollytelling-web` when the target includes scroll choreography.

Figma describes intended structure. The browser proves the implementation actually works.

## Verification

Before completion, check:

- intended frame/selection was the one implemented;
- existing variables/tokens/components were reused where appropriate;
- Code Connect mappings were not ignored;
- desktop/mobile variants or constraints are represented;
- typography and assets are real, not approximated without disclosure;
- implementation has been visually inspected in the browser;
- any Figma/code drift that remains is explicitly reported.
