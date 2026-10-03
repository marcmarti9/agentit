# Remotion capability map

Use this as a routing and verification checklist, not as a substitute for the
current official Remotion documentation. The official capability surface can
change; inspect https://www.remotion.dev/docs/ai/skills and the exact installed
package version before using API-specific instructions.

## Current official capability families

As of 2026-10-04, Remotion's published Agent Skills surface includes a
best-practices hub plus focused guidance for project creation, React markup,
Studio preview, rendering, map animations, captions, Remotion-backed SaaS,
Studio interactivity/editability, documentation lookup, upgrades, and
browser-side multimedia handling.

Agentit deliberately does not vendor those official skill bodies unless their
reuse license is explicit and compatible. This adapter instead maps those
capabilities to Agentit's own procedure and consults current official docs at
execution time.

## Agentit ownership

- **Create / scaffold**: use this skill only when Remotion is explicitly chosen.
  Inspect the current creation path, package manager and target runtime first.
- **Markup / composition engineering**: this skill owns deterministic React
  composition structure, timing, assets, fonts, props and renderer-safe state.
- **Studio / preview**: use the project's installed Studio workflow for bounded
  visual probes. Preview success is not final-output evidence.
- **Render / stills**: use installed project scripts/CLI and verify the exact
  produced file by decoding or extracting representative frames.
- **Maps / geospatial video**: confirm map provider, data source, attribution,
  API-key handling and network/render constraints. Prefer the project's existing
  mapping stack; do not invent provider APIs or embed secrets.
- **Captions**: preserve approved wording, timing source and fps conversion;
  verify line breaks, safe area and audio/caption sync in final output.
- **SaaS / product integration**: treat Remotion as one subsystem. Separate
  composition code from job orchestration, storage, auth, billing, queues,
  observability and deployment. Load the relevant backend/security/product
  owners JIT instead of expanding this skill into an application architecture.
- **Studio interactivity / editability**: inspect current supported APIs before
  exposing editable controls. Keep values validated and composition defaults
  renderable without hidden editor state.
- **Docs lookup**: current official docs and installed type declarations are
  authoritative for API details. Do not preserve stale snippets as canon.
- **Upgrade**: inventory all Remotion-family packages and compatible media
  packages, follow the current migration path, then type-check, preview and
  render a bounded representative output.
- **Multimedia / metadata**: use the media stack actually present in the project
  and verify its versioned contract before reading duration, dimensions, codecs
  or frame metadata. Do not assume a particular helper package exists.
- **Licensing**: Remotion has its own current runtime/commercial licensing terms.
  Before a commercial deployment where licensing could matter, consult
  https://www.remotion.dev/docs/license rather than inferring terms from old
  source or from Agentit's Apache-2.0 adapter license.

## Companion Agentit skills

Use `motion-graphics-production` for authored motion language, timing and scene
craft; `advertising-video-production` for ad hooks, evidence-backed claims and
creative variants; `creative-tool-scout` when the renderer has not yet been
chosen. These are conditional owners, not a bundle to load for every Remotion
task.
