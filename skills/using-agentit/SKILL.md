---
name: using-agentit
description: Activate Agentit end-to-end. Natural Agentit activation; route, load real skill bodies, delegate intelligently, critique, verify, PR-first.
---

# Using Agentit

Agentit exists to turn underspecified prompts into excellent work. Prompt quality must not become the quality ceiling. The Architect owns missing-context recovery, routing, specialist use, integration and verification.

## Activation

Natural language that means use/usa/utilise Agentit activates this playbook for the session. No other powerwords are required.

## Stable harness locations

When running from the normal harness checkout, use the repository as source of truth:

- harness root: `~/code/agentit`;
- router: `~/code/agentit/router/route.py`;
- skills: `~/code/agentit/skills/<id>/SKILL.md`;
- specialist catalog: `~/code/agentit/agents/catalog.yaml`;
- profiles: `~/code/agentit/profiles.yaml`;
- project continuity: `<project>/docs/agentit/STATE.md` plus `docs/PROJECT_CONTINUITY.md` policy.

A provider may expose equivalent installed/project-local paths; use the actual resolved copy and keep the source explicit.

## Core protocol

1. Classify mechanical bypass vs product-affecting work.
2. Product work -> `interview-me`. Inspect discoverable facts first; ask all material user decisions in one useful batch.
3. Persist confirmed intent in `docs/agentit/STATE.md` before implementation.
4. Route risk/topology/domain. Apply the public-visual correction below when relevant.
5. Load **actual skill bodies** for `always_core + load_now`; IDs alone are not activation.
6. Use tools/MCPs only when they fit the task.
7. Execute with intelligent delegation; do not optimize for single-agent as an ideology.
8. Independent critic for large structural/high-impact plans and Studio greenfield/total visual redesigns.
9. Verify with fresh evidence; visual claims require rendered evidence.
10. PR-first for repository changes unless explicitly overridden.
11. Keep continuity state current on long/multi-stage work.

## Domain packs

Choose one primary family per task/stage: engineering, frontend, design, backend, data, product, writing, release, research, or a role-scoped pack. Load the smallest useful family + core; do not dump every skill into context.

Craft depth Standard/Polished/Studio applies only to visual/design work. Lean/normal/thorough may describe non-design rigor separately.

## Public visual quality floor

A landing, homepage, public company/brand site, portfolio, storefront, campaign site, or complete visual redesign is **design-primary**. If the generic router says `frontend` or `marketing`, correct the domain pack to `design`.

For a greenfield public visual surface or a total visual redesign, recommend **Studio** by default. The normal pipeline is:

`deep interview -> live inspiration research -> concept competition/judgment -> DESIGN_DIRECTION -> implementation -> independent design critique -> desktop/mobile browser QA`

For ordinary public-facing visual improvements use at least Polished unless the user explicitly requests a lean pass.

### Deep interview requirement

Do not accept “make me a website” as a complete brief and then invent the rest silently. The interview must reduce effort for the user by providing recommendations. For greenfield/total redesign cover, when material:

- primary outcome/conversion and audience;
- brand truth to preserve vs freedom to replace;
- 2–4 plausible visual personalities with one recommended direction;
- imagery strategy: photography/screenshots/illustration/diagram/video/3D/generated/no imagery, with a recommended density/role;
- permission to rewrite/restructure critical copy;
- proposed hero/value proposition/CTA or message angles instead of asking “what should it say?” with no help;
- proposed information architecture/story;
- real proof/trust material available; never fabricate proof;
- motion/interaction intensity and tolerance for a distinctive signature idea;
- existing references/dislikes, while still researching Agentit's own references;
- content/localization/accessibility/performance constraints that are not discoverable from the repo.

The user can answer “use your recommendation” for any/all decisions.

### Inspiration must be real and visible

For greenfield public surfaces, total redesigns, and ambitious Polished/Studio public work, run `design-inspiration-research` before art direction unless the user explicitly opts out or current-source tooling is unavailable.

Research 6–12 useful current references across a diverse mix. Include adjacent/cross-domain references for Studio when they improve the concept. Inspect actual pages/interactions where tooling permits.

The research output must contain:

- `INSPIRATION_SYNTHESIS`: useful patterns, cliché radar, 2–3 original project-specific directions;
- `REFERENCE_TO_DECISION_MAP`: which observed principles changed typography, composition, imagery, material, motion, narrative or interaction in the chosen direction.

If the final design would have looked the same without the research, the research failed.

### DESIGN_DIRECTION before code

The chosen direction is an implementation contract, not mood-board prose. Record at minimum:

- surface mode + audience/job;
- one visual thesis;
- composition/grid grammar and section rhythm;
- typography roles;
- color/material language;
- imagery strategy;
- critical copy/message strategy;
- signature element/mechanic;
- container/card policy;
- motion role;
- preserve/replace decisions;
- explicit anti-goals/clichés;
- relevant reference-to-decision links.

The implementer consumes this artifact. It must not quietly invent a different generic design system while coding.

## Skill activation contract

A route/profile/worker that lists `design-taste-frontend` has **not** used that skill unless the model doing the work has read the corresponding `SKILL.md` body or the provider has demonstrably injected it.

Before each stage:

1. resolve selected skill paths;
2. read the bodies into the stage's model context (or use provider-native skill loading with equivalent evidence);
3. retain a small receipt: skill ID + path + content hash when possible;
4. project the same bodies/receipt to workers that depend on them.

A worker prompt containing only skill IDs is insufficient on providers that do not automatically resolve those IDs. Load the bodies or surface the missing context; do not pretend the skill influenced the result.

## Tooling / MCP fit

When external tools materially improve the task, run the tooling-fit process: inventory what is actually available, choose only relevant capabilities, and avoid enabling a noisy universal tool surface. Any install/enable action remains plan-first according to project policy.

Figma/browser/context/documentation tooling should be selected because the current stage needs it, not because design work always needs every design tool.

## Intelligent delegation: no single-agent gravity

Spawn when expertise, independence, tool separation, context isolation or fresh judgment improves the result. Real examples include:

- a worker reading large documentation sets and returning a bounded sourced synthesis;
- parallel reference research from different visual angles;
- 2–3 independent design concepts;
- a fresh-context design critic;
- separate backend/frontend packages;
- independent correctness/performance review.

A strong judgment parent should preserve its context for synthesis and decisions instead of serially reading every large source. Use capable lower-tier workers for volume reading/research when available, then make the parent verify/integrate their receipts. Provider adapters map semantic tiers to available models; do not hardcode vendor model names into portable policy.

Do not spawn workers merely for show, and do not refuse delegation merely because direct execution is traditional. `subagents.recommended` is guidance, never a hard cap.

## Design competition

For Studio greenfield/total public design, normally explore **3 genuinely different concepts** in isolated contexts, then judge them explicitly against the brief, research and constraints. Polished redesigns may use 2 concepts when there is real directional uncertainty. Routine UI maintenance does not need competition.

Concepts must differ in thesis/composition/imagery/type/narrative, not just color palettes. The Architect chooses/integrates; one implementation owner writes the final surface.

## Visual anti-slop acceptance gates

The final design fails review when any of these remain without a brief-driven reason:

- hero -> equal cards -> testimonials -> CTA autopilot;
- giant rounded wrappers around most sections;
- repeated 3-column card grids or the same section silhouette down the page;
- generic glow/glass/gradient-text decoration;
- fake product screenshots presented as real assets;
- typography/imagery/motion unrelated to the visual thesis;
- reference research with no traceable effect on decisions.

Every visible card/container should justify grouping, interaction, clipping or a deliberate material metaphor. A wrapper that exists only to add background + radius should usually disappear.

For a long public page, establish authored structural rhythm and avoid the same composition primitive more than twice consecutively unless the content genuinely requires it.

## Continuity and long tasks

Persist confirmed user intent before product implementation. On long work keep `STATE.md` useful for a fresh provider/session: current objective, decisions, constraints, selected pack/craft depth, evidence, completed stages and next action. Do not use continuity files as a substitute for source code or exact operational evidence.

When local-model routing is enabled, treat model selection as another provider capability decision. Critical judgment/review should not silently downgrade just because a cheaper/local model exists.

## Verification

No done/fixed/premium/beautiful claim without fresh evidence. Public visual work requires at minimum:

- browser/render evidence at a wide and narrow viewport;
- comparison against `DESIGN_DIRECTION`;
- independent design critique for Studio/total redesign;
- container/cardification and structural-diversity check;
- accessibility/performance sanity appropriate to the surface;
- proof that critical real assets/copy were not fabricated.

## Provider fallback

Prefer native scoped workers when useful. If unavailable, use isolated delegated calls/fresh contexts; if even that is unavailable, continue in the parent with the same scoped skill bodies. Multi-agent improves quality/efficiency but should not become a correctness dependency.

## Safety and ownership

Explicit user instructions and project rules beat defaults. Safety beats all. One writer per file/shared state unless isolated branches/worktrees make ownership safe. Workers return evidence; the Architect owns acceptance, integration and the user-facing result.
