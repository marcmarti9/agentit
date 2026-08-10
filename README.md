# Agentit

[![CI Status](https://github.com/marcmarti9/agentit/actions/workflows/ci.yml/badge.svg)](https://github.com/marcmarti9/agentit/actions)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Release](https://img.shields.io/badge/version-v0.3.2--stable-green.svg)](https://github.com/marcmarti9/agentit/releases)

> **Agentit is a portable, provider-neutral meta-harness for AI coding agents: interview first, choose an explicit effort level, route skills/specialists, keep work resumable, verify, and deliver through PRs by default.**

Agentit is designed to work across **OpenAI, Anthropic, Google, xAI**, and compatible future coding-agent environments. Provider-specific subagents/workers are optional execution primitives; the shared Agentit protocol is semantic and portable.

## Use it

Tell the agent:

```text
usa agentit
```

or combine it with a task:

```text
usa agentit y crea mi portfolio personal
```

For product-affecting work Agentit follows roughly:

```text
inspect facts
   ↓
one comprehensive interview batch
   ↓
confirm Standard / Polished / Studio
   ↓
persist resumable project state
   ↓
route skills + optional specialists
   ↓
implement on work branch
   ↓
continuous documentation + verification
   ↓
PR by default
```

Purely mechanical chores such as exact `mkdir`, file moves/renames, formatting, copying known content, or running a specified command can bypass the interview.

---

## Interview-first, but not one-question-at-a-time

Agentit interviews **every product-affecting task**, not only ambiguous ones.

Before asking, the agent inspects repo/docs/tools so it does not ask discoverable facts. Then it asks **all currently identifiable material user decisions in one numbered batch**, with a recommended/default answer on every question.

The preferred flow is one interview message, one user reply, then work. A second batch is allowed only when the first answers reveal genuinely new decisions that could not reasonably have been known before.

Every product interview also recommends and confirms an effort level.

| Level | Typical total model tokens* | Intent |
|---|---:|---|
| **Standard** | ~15k-80k | efficient production-quality execution |
| **Polished** | ~50k-250k | targeted research, stronger polish/QA, selective specialists |
| **Studio** | ~150k-800k+ | quality-first flagship work, deeper research/concepting/review |

\* Rough total-session envelopes across parent + delegated calls, not billing guarantees.

Standard is not lower correctness. Studio is not automatically “design mode”. The agent recommends by marginal value, explains what changes between levels, and asks before materially escalating later.

Canonical files: [`skills/interview-me/SKILL.md`](skills/interview-me/SKILL.md), [`effort/levels.yaml`](effort/levels.yaml), [`docs/AGENTIT_INTERVIEW_AND_PROVIDER_POLICY.md`](docs/AGENTIT_INTERVIEW_AND_PROVIDER_POLICY.md).

---

## Continuity: sessions are disposable

Agentit assumes any chat can disappear because of context/token exhaustion, provider/model switch, app crash, machine switch, or a long pause.

For every product-affecting task, maintain a compact project state document at:

```text
docs/agentit/STATE.md
```

If the project already has an equivalent canonical state file, reuse it instead.

The state must let a completely fresh agent recover:

- what is being built and why;
- confirmed intent, audience, success criteria, constraints, and non-goals;
- selected Standard/Polished/Studio level;
- what is done / in progress / blocked / not started;
- durable product, architecture, API, data, and design decisions;
- important files/artifacts;
- branch + PR;
- verification commands/results;
- next executable actions;
- open user questions/blockers.

Update it after interview confirmation, expensive-to-rediscover decisions, meaningful milestones, before handoff/context exhaustion/pause, and before completion.

Do not persist secrets, credentials, raw chain-of-thought, full chat transcripts, or giant tool dumps.

Canonical policy: [`docs/PROJECT_CONTINUITY.md`](docs/PROJECT_CONTINUITY.md).

---

## Git: branch + PR by default

For repository changes Agentit defaults to:

```text
work branch → commits → verification → pull request → review/user merge decision
```

It should **not** commit/fast-forward directly onto `main`/`master` and should **not** auto-merge PRs unless the user explicitly authorizes that exception for the task or project instructions require another workflow.

Continuity/docs updates travel in the same branch/PR as implementation.

---

## Provider-neutral specialist layer

`agents/catalog.yaml` defines semantic roles with small skill bundles and output contracts. Examples include:

```text
frontend-developer
backend-architect
ai-engineer
devops-automator
design-system-researcher
ui-researcher
trend-researcher
creative-tool-scout
visual-storytelling-director
spatial-experience-designer
delight-and-whimsy
design-critic
performance-benchmarker
api-tester
workflow-optimizer
```

Agentit remains single-agent-first. A specialist is spawned only when fresh context, true parallelism, domain expertise, different tooling/model capability, creative diversity, or independent review outweighs coordination overhead.

Execution fallback:

```text
native provider subagent/worker
        ↓ unavailable
isolated delegated model/tool call
        ↓ unavailable
separate fresh-context invocation
        ↓ unavailable
parent + exact specialist skill bundle
```

Multi-agent execution is an optimization, never a correctness dependency.

---

## UI/UX Pro Max intelligence

Agentit's design profile includes `ui-ux-pro-max-intelligence`, a provider-neutral JIT adapter for the MIT-licensed upstream [`nextlevelbuilder/ui-ux-pro-max-skill`](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill).

The upstream project provides searchable product-aware intelligence for style families, palettes, typography, UX/accessibility rules, icons, charts, GSAP/motion patterns, landing structures, and many implementation stacks.

Agentit deliberately treats it as an **intelligence source, not the creative director**:

```text
UI UX Pro Max lookup
       ↓
compact product/design baseline
       ↓
Taste / creative direction / research
       ↓
implementation
       ↓
Impeccable / Emil / critic
```

The database should be queried JIT. Do not dump it wholesale into model context and do not let a preset style automatically become the art direction.

Effort behavior:

- **Standard:** narrow lookup only when it prevents a mistake or answers a concrete design question.
- **Polished:** targeted product/style/color/type/UX intelligence when useful.
- **Studio:** one evidence source among live inspiration research, concept exploration, creative direction, and independent critique.

See [`skills/ui-ux-pro-max-intelligence/SKILL.md`](skills/ui-ux-pro-max-intelligence/SKILL.md) and [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

---

## Design studio

The `design` profile contains a broad but JIT-routed craft stack:

```text
ui-ux-pro-max-intelligence       structured UI/UX design intelligence
design-inspiration-research      live project-specific references
design-trend-researcher          emerging / maturing / saturated patterns
creative-web-experiences         concept generation
design-taste-frontend            art direction / visual thesis
impeccable-design                critique / polish / responsive craft
emil-design-eng                  interaction and motion feel
visual-storytelling-director     narrative beats and pacing
creative-tool-scout              current implementation tooling
figma-design-workflow            official Figma MCP workflow
scrollytelling-web               narrative scroll architecture
gsap-scrolltrigger               pin/scrub/timeline mechanics
gsap-performance                 motion runtime performance
threejs-spatial-experiences      rooms/stores/museums/worlds
threejs-product-storytelling     GLB/glTF product storytelling
delight-and-whimsy               restrained memorable details
```

Do not load the whole stack just because design is active. Effort level and task signals control depth.

For genuinely high-ambition Studio work, Agentit may use a **design competition**: shared evidence brief → 2-3 independent concepts → explicit jury by brand fit/originality/clarity/usability/feasibility/performance/memorability → winner or justified hybrid → implementation → independent critique.

---

## Profiles

`profiles.yaml` keeps the global install bounded and activates deeper capabilities JIT.

| Profile | Purpose |
|---|---|
| `core` | bounded everyday engineering harness |
| `frontend` | browser/performance/UI maintenance |
| `design` | full craft studio + UI/UX intelligence |
| `backend` | API/service/observability |
| `supabase` | Postgres/Supabase guidance |
| `product` | discovery/spec/marketing |
| `writing` | documentation/writing |
| `release` | CI/migration/launch |
| `research` | context/spec/adversarial review |
| `all` | escape hatch only |

```bash
agentit enable design --project . --apply
agentit status --project .
agentit disable design --project . --apply
```

---

## Verification

Agentit separates model claims from verification evidence.

```bash
agentit verify "task summary" --project .
agentit verify "task summary" --project . --apply
```

No `done`, `fixed`, or `passing` claim without fresh evidence after the last relevant edit. Design work needs rendered evidence when browser tooling is available; high-ambition work should normally get independent critique/performance review.

---

## MCP runtime

```bash
agentit mcp status
agentit mcp enable context7 --apply
agentit mcp enable-stack developer_core --apply
agentit mcp enable-stack design_studio --apply
```

The design studio stack can combine Figma, Context7, Playwright, and Chrome DevTools. MCPs are optional capabilities, not portability requirements.

---

## Install

```bash
git clone https://github.com/marcmarti9/agentit.git ~/code/agentit
cd ~/code/agentit
bash install.sh --provider all --with-guides --apply
ln -sf ~/code/agentit/agentit ~/.local/bin/agentit
```

Open Skills / compatible clients typically use `~/.agents/skills/`; Claude can use `~/.claude/skills/`; Codex can use `~/.codex/skills/`. Shared Agentit semantics remain provider-neutral.

---

## Testing

```bash
python3 -m unittest discover -s router -p "test_*.py"
python3 -m unittest discover -s tests
python3 evals/run.py
```

---

## Docs map

| Doc | Purpose |
|---|---|
| [`AGENTS.md`](AGENTS.md) | global agent playbook |
| [`docs/AGENTIT_INTERVIEW_AND_PROVIDER_POLICY.md`](docs/AGENTIT_INTERVIEW_AND_PROVIDER_POLICY.md) | batched interview + effort + provider semantics |
| [`docs/PROJECT_CONTINUITY.md`](docs/PROJECT_CONTINUITY.md) | resumable project-state contract + PR-first workflow |
| [`agents/catalog.yaml`](agents/catalog.yaml) | reusable specialist roles |
| [`effort/levels.yaml`](effort/levels.yaml) | Standard / Polished / Studio budgets |
| [`docs/MCP_CATALOG.md`](docs/MCP_CATALOG.md) | MCP catalog/runtime |
| [`docs/ADAPTIVE_AGENT_ARCHITECTURE.md`](docs/ADAPTIVE_AGENT_ARCHITECTURE.md) | orchestration topologies/contracts |
| [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) | upstream design-skill attribution |

## License

Licensed under the [Apache License, Version 2.0](LICENSE). Third-party adaptations/integrations retain their applicable notices in [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).
