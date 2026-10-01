# Skill refresh and curation — 2026-10-01

## Scope

Audit every canonical vendored Agentit skill source against the current default-branch HEAD, refresh stale packages, inspect recent high-signal skill libraries, and preserve Agentit's JIT/full-body activation contract.

## Existing upstream refresh

Agentit currently has **41 canonical vendored skill mappings across 15 upstream repositories**.

| Upstream | Vendored skills | Pinned | Current HEAD | Status |\n|---|---:|---|---|---|\n| `Appllama/appllama-skills` | 2 | `dd5caaec3d5d` | `dd5caaec3d5d` | current |\n| `Leonxlnx/taste-skill` | 1 | `ce26fc25c0e5` | `ce26fc25c0e5` | current |\n| `Nutlope/hallmark` | 1 | `13ac0ec7e148` | `13ac0ec7e148` | current |\n| `addyosmani/agent-skills` | 25 | `2686b620fc1f` | `2686b620fc1f` | current |\n| `ayghri/i-have-adhd` | 1 | `839872f9d1cd` | `839872f9d1cd` | current |\n| `blader/humanizer` | 1 | `225a6f39ac85` | `225a6f39ac85` | current |\n| `cathrynlavery/diagram-design` | 1 | `57148ac6f7cf` | `57148ac6f7cf` | current |\n| `emilkowalski/skills` | 1 | `d16ebe60d09a` | `d16ebe60d09a` | current |\n| `greensock/gsap-skills` | 2 | `aed9cfd32777` | `aed9cfd32777` | current |\n| `hardikpandya/stop-slop` | 1 | `8da1f030185b` | `8da1f030185b` | current |\n| `nextlevelbuilder/ui-ux-pro-max-skill` | 1 | `09170eec67ee` | `09170eec67ee` | current |\n| `obra/superpowers` | 1 | `8ca22dba9a94` | `8ca22dba9a94` | current |\n| `pbakaus/impeccable` | 1 | `c74755d92098` | `c74755d92098` | current |\n| `supabase/agent-skills` | 1 | `544bfc56c89a` | `544bfc56c89a` | current |\n| `vercel-labs/skills` | 1 | `3694740352ee` | `3694740352ee` | current |\n

Result: every vendored source is now pinned to the current HEAD observed during this audit. Fourteen sources were already current. `pbakaus/impeccable` was 17 commits behind and was refreshed to `c74755d920985f7a92cef691ca970ba95f90126e`; only files changed upstream inside the canonical `.agents/skills/impeccable` package were replaced, and its lock hashes/source pin were updated.

## New source inspection

Inspected current public skill libraries included:

- Anthropic `anthropics/skills` at `8a1541c4a3ffa5a20a5a91de0dcf3f0bab1d1ef4`.
- Matt Pocock `mattpocock/skills` at `d81f3a183412e71a5b1e84ca21bc1a35eea03a60`.
- Vercel Labs `vercel-labs/agent-skills` at `063bee94c3f4df8453406c830b0a7df0f2860278`.
- Remotion `remotion-dev/skills` at `a9b199e165505267eda1ed3e0ef3dd3567c43411`.
- Additional broad catalogs were inspected for discovery value but not treated as automatic dependencies.

### Added as Agentit-owned adaptations

1. **`skill-authoring-and-evals`**
   - informed by Anthropic `skill-creator` and Matt Pocock `writing-for-agents`;
   - owns skill/agent-document authoring, trigger precision, progressive disclosure and selection/delivery evals;
   - scoped to writing/agent-runtime discovery, never core.

2. **`mcp-server-development`**
   - informed by Anthropic `mcp-builder`;
   - owns building MCP servers/tool surfaces;
   - distinct from `mcp-tooling-fit`, which chooses/uses an existing MCP;
   - scoped to backend/engineering discovery.

3. **`react-composition-patterns`**
   - informed by Vercel's composition-pattern skill;
   - only triggers on demonstrated reusable-component API pressure;
   - explicitly does not apply to ordinary one-off React implementation;
   - scoped to frontend discovery.

### Considered but not imported

- **Vercel React best practices:** strong source, but substantial overlap with existing `frontend-ui-engineering` + `performance-optimization`; adding a second broad React doctrine would increase selection ambiguity.
- **Vercel deploy-to-vercel:** useful, but overlaps tool/connector deployment capability and carries external side effects; keep deployment authority in explicit tools/workflows.
- **Remotion bundle:** useful niche capability, but the umbrella package is large and the standalone repository did not expose an explicit repo-level license in this audit. Do not vendor until provenance/licensing is unambiguous and a concrete Agentit gap justifies it.
- **large scientific/domain megapacks:** useful as discovery/scout sources, not global Agentit inventory. Import only a concrete specialist when a recurring job warrants it.

## Activation contract

`agentit skills activate <ids>` now means:

1. semantic task selection happens first;
2. exactly those IDs are loaded;
3. the **complete exact `SKILL.md` bytes** for each selected skill are delivered;
4. SHA-256 and byte count are validated;
5. missing/stale/tampered bodies fail closed;
6. pack peers, mentioned skills and dependencies are **not** implicitly activated;
7. references/assets/scripts remain progressive disclosure and are loaded only when the active body reaches a branch that needs them.

`show` remains a compatibility alias.

Profiles and packs are discovery/installation metadata only. They never activate their entire contents.

## Development-mode interaction

Repository implementation uses `DEVELOPMENT_MODE: BUILDER | REVIEW`.

- **BUILDER:** complete requested functionality with targeted minimum checks.
- **REVIEW:** freeze feature scope and deeply validate the completed implementation.

Selected specialist skills cannot override that cadence or turn themselves into mandatory project lifecycles.

## Canonical vendored inventory

| Skill | Upstream | Snapshot |\n|---|---|---|\n| `api-and-interface-design` | `addyosmani/agent-skills` | `2686b620fc1f` |\n| `appllama-app-design-skill` | `Appllama/appllama-skills` | `dd5caaec3d5d` |\n| `appllama-usage` | `Appllama/appllama-skills` | `dd5caaec3d5d` |\n| `browser-testing-with-devtools` | `addyosmani/agent-skills` | `2686b620fc1f` |\n| `ci-cd-and-automation` | `addyosmani/agent-skills` | `2686b620fc1f` |\n| `code-review-and-quality` | `addyosmani/agent-skills` | `2686b620fc1f` |\n| `code-simplification` | `addyosmani/agent-skills` | `2686b620fc1f` |\n| `constraint-driven-development` | `addyosmani/agent-skills` | `2686b620fc1f` |\n| `context-engineering` | `addyosmani/agent-skills` | `2686b620fc1f` |\n| `debugging-and-error-recovery` | `addyosmani/agent-skills` | `2686b620fc1f` |\n| `deprecation-and-migration` | `addyosmani/agent-skills` | `2686b620fc1f` |\n| `design-taste-frontend` | `Leonxlnx/taste-skill` | `ce26fc25c0e5` |\n| `diagram-design` | `cathrynlavery/diagram-design` | `57148ac6f7cf` |\n| `documentation-and-adrs` | `addyosmani/agent-skills` | `2686b620fc1f` |\n| `doubt-driven-development` | `addyosmani/agent-skills` | `2686b620fc1f` |\n| `emil-design-eng` | `emilkowalski/skills` | `d16ebe60d09a` |\n| `find-skills` | `vercel-labs/skills` | `3694740352ee` |\n| `frontend-ui-engineering` | `addyosmani/agent-skills` | `2686b620fc1f` |\n| `git-workflow-and-versioning` | `addyosmani/agent-skills` | `2686b620fc1f` |\n| `gsap-performance` | `greensock/gsap-skills` | `aed9cfd32777` |\n| `gsap-scrolltrigger` | `greensock/gsap-skills` | `aed9cfd32777` |\n| `hallmark` | `Nutlope/hallmark` | `13ac0ec7e148` |\n| `humanizer` | `blader/humanizer` | `225a6f39ac85` |\n| `i-have-adhd` | `ayghri/i-have-adhd` | `839872f9d1cd` |\n| `idea-refine` | `addyosmani/agent-skills` | `2686b620fc1f` |\n| `impeccable` | `pbakaus/impeccable` | `c74755d92098` |\n| `incremental-implementation` | `addyosmani/agent-skills` | `2686b620fc1f` |\n| `interview-me` | `addyosmani/agent-skills` | `2686b620fc1f` |\n| `observability-and-instrumentation` | `addyosmani/agent-skills` | `2686b620fc1f` |\n| `performance-optimization` | `addyosmani/agent-skills` | `2686b620fc1f` |\n| `planning-and-task-breakdown` | `addyosmani/agent-skills` | `2686b620fc1f` |\n| `security-and-hardening` | `addyosmani/agent-skills` | `2686b620fc1f` |\n| `shipping-and-launch` | `addyosmani/agent-skills` | `2686b620fc1f` |\n| `source-driven-development` | `addyosmani/agent-skills` | `2686b620fc1f` |\n| `spec-driven-development` | `addyosmani/agent-skills` | `2686b620fc1f` |\n| `stop-slop` | `hardikpandya/stop-slop` | `8da1f030185b` |\n| `supabase-postgres-best-practices` | `supabase/agent-skills` | `544bfc56c89a` |\n| `test-driven-development` | `addyosmani/agent-skills` | `2686b620fc1f` |\n| `ui-ux-pro-max` | `nextlevelbuilder/ui-ux-pro-max-skill` | `09170eec67ee` |\n| `using-agent-skills` | `addyosmani/agent-skills` | `2686b620fc1f` |\n| `verification-before-completion` | `obra/superpowers` | `8ca22dba9a94` |\n
