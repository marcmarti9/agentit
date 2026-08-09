# Agentit

[![CI Status](https://github.com/marcmarti9/agentit/actions/workflows/ci.yml/badge.svg)](https://github.com/marcmarti9/agentit/actions)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Release](https://img.shields.io/badge/version-v0.3.2--stable-green.svg)](https://github.com/marcmarti9/agentit/releases)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Bash 4.0+](https://img.shields.io/badge/bash-4.0+-green.svg)](https://www.gnu.org/software/bash/)

> **Agentit is a portable, provider-neutral meta-harness for safe AI coding-agent orchestration, skill routing, specialist delegation, persistent context management, and ecosystem tool incubation.**
>
> *Configure, interview, route, coordinate, and verify coding agents without locking yourself to one provider.*

---

> **Core philosophy:** understand the real task first, use one capable agent by default, and add specialists only when they materially improve the result.

Agentit is an opinionated, safety-first meta-harness (v0.3.2) for predictable, vendor-neutral work across **OpenAI**, **Anthropic**, **Google**, **xAI**, and other compatible coding-agent environments. Provider adapters may expose different local primitives; Agentit's shared protocol stays semantic and portable.

---

## Session usage (one phrase)

After install, tell the agent:

```text
usa agentit
```

or:

```text
use agentit
```

Or pair it with the task:

```text
usa agentit y haz una landing premium para X
use agentit and implement the auth fix with tests
```

That loads the **`using-agentit`** playbook:

0. **Interview gate** — if missing user decisions could materially change the result, clarify them before planning
1. **Route** — `python3 ~/code/agentit/router/route.py "task"`
2. **JIT profiles** — `agentit enable <profile> --project . --apply` when skills are missing
3. **Load the skills the work actually needs**; deep design work is explicitly allowed to spend context on craft
4. **Choose direct vs specialist execution** — single-agent-first, but reusable expert roles are available when specialization, fresh context, independent review, or creative diversity helps
5. **Execute provider-neutrally** — native subagent if available; otherwise isolated delegation/fresh context; otherwise the parent uses the same specialist skill bundle directly
6. **Verify** — no done/fixed/passing without fresh command evidence

Global policy: [`AGENTS.md`](AGENTS.md). Bootstrap skill: [`skills/using-agentit/SKILL.md`](skills/using-agentit/SKILL.md). Interview/provider policy: [`docs/AGENTIT_INTERVIEW_AND_PROVIDER_POLICY.md`](docs/AGENTIT_INTERVIEW_AND_PROVIDER_POLICY.md).

---

## Highlights

| Area | What you get |
|------|----------------|
| **Interview-first when it matters** | `interview-me` resolves goals, users, success criteria, constraints, taste, and non-goals before expensive assumptions become code |
| **Single-agent-first** | Direct work by default; Probe / Specialist / Fan-Out / Pipeline / Writer-Reviewer / Design Competition / Audit only when there is a concrete benefit |
| **Provider-neutral specialists** | `agents/catalog.yaml` defines semantic expert roles + skill bundles; native multi-agent features are optional optimizations, never correctness dependencies |
| **Graceful degradation** | No subagents? The parent loads the exact specialist skill bundle and continues with the same objective/constraints/output contract |
| **Router** | Risk, topology, skills, preferences, verification flags — plan only, never permission to destroy |
| **Core + profiles** | 12-skill global `core`; opt-in project profiles (`frontend`, `design`, `backend`, `supabase`, …) |
| **Design studio** | Research + concepting + Taste + Impeccable + Emil + visual storytelling + creative tool scouting + Figma + scrollytelling + GSAP + spatial/3D experiences |
| **Verification gauntlet** | Signal-gated probes + anti-greenwash (`agentit verify`) so “200 tests passed” is not enough alone |
| **Worker contracts** | `agentit worker build` / `router/worker_context.py` projects project instructions + task skills into delegated contexts where supported |
| **Context engines** | Tool-output filter, artifact refs (`agentit://`), session dedup |
| **MCP runtime** | Mid-session enable/disable via `agentit mcp` and optional `agentit-manager` gateway |
| **Scout / incubator** | Evaluate ecosystem ideas before promoting them |
| **Safe install** | Plan-first scripts, backups, SHA-256 sidecars, symlink rejection |

---

## Interview before implementation

Agentit does not treat every prompt as a complete specification.

For non-trivial work, the parent first asks whether any unresolved **decision** could materially change architecture, scope, UX, visual direction, success criteria, audience, risk, cost, or the definition of “good”. If yes, it loads `interview-me` before planning.

The interview is deliberately not ceremonial:

- facts available in the repo, runtime, docs, connected tools, or live sources are looked up by the agent;
- only real user decisions are asked;
- dependent questions are normally asked one at a time;
- independent unresolved decisions may be asked as a frontier round;
- questions carry a recommended/default answer so the user can react quickly;
- the interview stops once further answers are unlikely to materially change the result;
- trivial/mechanical work proceeds immediately.

For a high-ambition redesign this can include audience, brand personality, business goal, emotional target, references to embrace/avoid, available assets, interaction appetite, device/performance constraints, accessibility, and acceptable visual risk.

The point is simple: **spend a few questions before spending thousands of tokens implementing the wrong thing.**

---

## Adaptive architecture

```text
                  ┌─────────────────────────────────────┐
                  │            Task Request             │
                  └──────────────────┬──────────────────┘
                                     │
                              Interview gate
                                     │
                          ┌──────────┴──────────┐
                          │   Heuristic Router  │
                          └──────────┬──────────┘
                                     │
     ┌─────────────┬────────────┬────┴─────┬───────────────┬──────────────┐
     ▼             ▼            ▼          ▼               ▼              ▼
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  ┌────────────┐ ┌──────────┐
│  Direct  │ │Specialist│ │ Fan-Out  │ │ Pipeline │  │  Design    │ │  Audit   │
│ (Single) │ │  Probe   │ │(Parallel│ │  (DAG)   │  │Competition │ │(High-Risk│
└──────────┘ └──────────┘ └──────────┘ └──────────┘  └────────────┘ └──────────┘
```

A specialist is a capability bundle, not a permanent fake employee. The Architect keeps user communication, integration, architecture ownership, and final verification.

---

## Provider-neutral specialist layer

`agents/catalog.yaml` maps reusable roles to small skill bundles, triggers, modes, and expected outputs. Examples include:

```text
agents/catalog.yaml
├── frontend-developer
├── backend-architect
├── ai-engineer
├── devops-automator
├── trend-researcher
├── feedback-synthesizer
├── sprint-prioritizer
├── ui-researcher
├── creative-tool-scout
├── visual-storytelling-director
├── spatial-experience-designer
├── delight-and-whimsy
├── design-critic
├── performance-benchmarker
├── api-tester
└── workflow-optimizer
```

The same logical specialist works regardless of model provider. Agentit chooses the best execution primitive available:

```text
native provider subagent/worker
        ↓ unavailable
isolated delegated model/tool call
        ↓ unavailable
separate fresh-context invocation
        ↓ unavailable
parent + exact specialist skill bundle
```

The **objective, skills, constraints, allowed I/O, output contract, verification, and stop condition stay the same**. Multi-agent execution improves isolation, parallelism, or diversity when available; it is never required for Agentit to remain correct.

This is intentionally compatible with OpenAI, Anthropic, Google, xAI, and future providers instead of baking Claude/Codex-specific agent names into shared policy.

---

## Shared skills (50)

`profiles.yaml` controls what is exposed per project. The engineering core remains bounded; the **design profile is intentionally craft-heavy**.

| Profile | Role |
|---------|------|
| **`core`** (12, global install) | `using-agentit`, `verification-gauntlet`, `task-router`, orchestration, debugging, review, TDD, security, source-driven, frontend UI, planning, `using-agent-skills` |
| **`frontend`** | Browser, performance, anti-slop design, Taste art direction |
| **`design`** | Frontend + research + trend mapping + concepting + full Taste + Impeccable + Emil + storytelling + tool scouting + delight + Figma + scrollytelling + GSAP + spatial/product Three.js |
| **`backend` / `supabase`** | API, observability, Postgres/Supabase practices |
| **`product` / `writing` / `release` / `research`** | Specs, marketing, launch, adversarial review |
| **`all`** | Escape hatch only |

Notable design skills:

```text
skills/
├── design-inspiration-research      # Live reference research; principles, not copying
├── design-trend-researcher          # Emerging / maturing / saturated creative patterns
├── creative-web-experiences        # Generate and compare interaction concepts
├── design-taste-frontend            # Full-fat art direction; quality over token minimization
├── impeccable-design                # Design-director craft floor, critique, polish, responsiveness
├── emil-design-eng                  # Emil Kowalski-inspired interaction and motion craft
├── visual-storytelling-director     # Narrative beats, reveals, pacing, rests, climax
├── creative-tool-scout              # Find current libraries/tools for the chosen concept
├── delight-and-whimsy               # Small memorable moments with restraint
├── figma-design-workflow            # Official Figma MCP / design-system / Code Connect workflow
├── scrollytelling-web               # Narrative scroll architecture and engine selection
├── gsap-scrolltrigger               # Pin/scrub/timeline mechanics
├── gsap-performance                 # High-motion runtime performance discipline
├── threejs-spatial-experiences      # Stores, museums, rooms, walkthroughs, spatial journeys
└── threejs-product-storytelling     # GLB/glTF, exploded products, camera/light/material direction
```

The remaining engineering/product skills continue to live under `skills/` and are included by `all`.

### Verification gauntlet

Agents write tests — and can greenwash them. Agentit adds an **external gauntlet**:

```bash
./agentit verify "Add Supabase RLS for profiles" --project .
./agentit verify "Add Supabase RLS for profiles" --project . --apply
# → receipt under .agentit/verify/
```

Catalog: [`probes/catalog.yaml`](probes/catalog.yaml). Skill: [`skills/verification-gauntlet/SKILL.md`](skills/verification-gauntlet/SKILL.md).

### Design studio: quality first

The `design` profile deliberately spends context where visual craft needs it. It separates research, creative direction, implementation, and critique instead of stuffing everything into one giant contradictory prompt.

Typical ownership:

- **Inspiration researcher** finds current references across real sites, studios, showcases, social/video sources when browser access permits, and adjacent disciplines.
- **Trend researcher** separates emerging ideas from saturated AI-slop patterns.
- **Creative Web Experiences** explores multiple concepts before committing to a technical effect.
- **Taste** chooses the art direction, visual thesis, composition, type, material, and motion intensity.
- **Impeccable** acts as craft director across Persuade / Operate / Read / Experience surfaces and owns critique/polish/hardening.
- **Emil design engineering** owns interaction feel, easing, perceived performance, micro-interactions, and repeated-use motion restraint.
- **Visual Storytelling Director** owns scene progression, reveals, pauses, rhythm, and narrative continuity.
- **Creative Tool Scout** checks whether a better current library/tool exists before defaulting to familiar technology; catalogs such as `designengineer.tools` are discovery surfaces, then primary docs are verified.
- **Figma workflow** uses the official MCP as structured design/design-system context rather than treating frames as screenshots.
- **Scrollytelling + GSAP** owns pinned, scrubbed, timeline-driven narrative work.
- **Three.js spatial experiences** handles guided/explorable stores, museums, showrooms, rooms, and spatial brand journeys.
- **Three.js product storytelling** handles real spatial product work: exploded assemblies, camera direction, materials, lighting, and depth.
- **Delight & Whimsy** adds a few memorable moments late in polish instead of turning the whole interface into a gimmick.
- **Design Critic + Performance Benchmarker** attack the finished implementation before it is accepted.

For genuinely ambitious work, Agentit may use a **design competition**: shared research brief → 2-3 independent concepts → explicit jury by brand fit/originality/clarity/usability/feasibility/performance/memorability → winner or justified hybrid → implementation → independent critique.

If the provider cannot spawn separate concept agents, the same competition can be executed sequentially in fresh/direct contexts. The method survives even when the provider primitive changes.

For a cinematic product landing, a typical project setup is:

```bash
./agentit enable design --project . --apply
agentit mcp enable-stack design_studio --apply
```

The `design_studio` MCP stack includes **Figma + Context7 + Playwright + Chrome DevTools**. Figma should use the official remote MCP/OAuth flow; no Figma token belongs in the repository.

### Scrollytelling / spatial / product decomposition

`scrollytelling-web` deliberately chooses the smallest engine that can express the idea well:

- native CSS / scroll-driven animation for simple work;
- Motion for local React interaction;
- **GSAP ScrollTrigger** for serious pin/scrub/timeline choreography;
- image sequences for photorealistic pre-rendered transformation;
- **Three.js / React Three Fiber** for genuine 3D products and spatial environments.

That does **not** mean every premium site becomes product decomposition. The creative layer may instead choose an editorial experience, virtual walkthrough, spatial store, interactive map, kinetic typography, image-led narrative, restrained static composition, or something else entirely.

Every cinematic/spatial sequence must have a reduced-motion path, a mobile strategy, reverse-navigation correctness where relevant, and end-to-end browser verification. A hero screenshot is not proof that an experience works.

Enable the full design profile:

```bash
./agentit enable design --project . --apply
```

---

## MCP catalog & runtime

Agents can list and toggle curated MCPs mid-session:

```bash
agentit mcp install-gateway --apply
agentit mcp status
agentit mcp enable context7 --apply
agentit mcp enable-stack developer_core --apply
agentit mcp enable-stack design_studio --apply   # Figma + docs + browser tooling
agentit mcp disable playwright --apply
```

Docs: [`docs/MCP_CATALOG.md`](docs/MCP_CATALOG.md). Starter engineering stack: **agentit-manager + Context7 + GitHub + Playwright**.

MCPs are capabilities, not portability requirements. If one provider/client cannot expose a particular integration, Agentit should use an equivalent available tool or report the missing capability explicitly rather than breaking the shared orchestration model.

---

## Quick start

### Install

```bash
git clone https://github.com/marcmarti9/agentit.git ~/code/agentit
cd ~/code/agentit

bash install.sh --provider all --with-guides
bash install.sh --provider all --with-guides --apply
ln -sf ~/code/agentit/agentit ~/.local/bin/agentit
```

Default skill install path for Open Skills / Grok: `~/.agents/skills/`.  
Claude: `~/.claude/skills/`. Codex: `~/.codex/skills/`.

### Route / trace a task

```bash
python3 ~/code/agentit/router/route.py "Rediseña la landing de un SaaS B2B"
./agentit trace "Implementa tests TDD para el servicio de backups" --project .
./agentit verify "Implementa tests TDD para el servicio de backups" --project . --apply
```

### Project profiles & context

```bash
./agentit enable design --project . --apply
./agentit status --project .
./agentit disable design --project . --apply

./agentit context filter build.log
./agentit context archive migration.sql --description "DB Schema"
./agentit context dedup "context block" --session session-123

./agentit artifact get agentit://artifacts/ref-a1b2c3d4.txt
./agentit artifact read agentit://artifacts/ref-a1b2c3d4.txt --lines 1:50
./agentit artifact grep agentit://artifacts/ref-a1b2c3d4.txt "AssertionError"
```

Profile enable copies **`SKILL.md` + `references/`** when present (safe managed files only).

### Scout & incubator

```bash
./agentit scout status
./agentit scout add "https://github.com/example/repo"
./agentit scout inspect <candidate-id>
```

---

## Providers

Agentit separates **shared semantics** from **provider adapters**.

| Provider family | Shared behavior |
|-----------------|-----------------|
| **OpenAI / Codex** | Interview → route → skills → direct/specialist execution → verify; native workers may be used when available |
| **Anthropic / Claude Code** | Same protocol; native subagents may be used when available |
| **Google / Antigravity / Open Skills** | Same protocol; provider-specific agent primitives are optional |
| **xAI / Grok** | Same protocol; Open Skills path and any available delegation primitive map to the same contracts |
| **Other compatible clients** | Read shared skills/catalogs and fall back to direct execution if no native multi-agent primitive exists |

The important guarantee is not that every provider has identical tooling. It is that **Agentit's result does not depend on one provider having a specific orchestration feature**.

See [`CODEX.md`](CODEX.md), [`CLAUDE.md`](CLAUDE.md), [`docs/ADAPTIVE_AGENT_ARCHITECTURE.md`](docs/ADAPTIVE_AGENT_ARCHITECTURE.md), and [`docs/AGENTIT_INTERVIEW_AND_PROVIDER_POLICY.md`](docs/AGENTIT_INTERVIEW_AND_PROVIDER_POLICY.md).

---

## Testing

```bash
python3 -m unittest discover -s router -p "test_*.py"
python3 -m unittest discover -s tests
python3 evals/run.py
```

---

## Safety defaults

- Scripts are **plan-first**; write only with `--apply`
- Install creates a backup under `~/backups/` (or `--backup-dir`)
- RISK_3 / RISK_4: full fidelity + human review; router never lowers inferred risk
- No commits, push, deploy, or remote mutations without an explicit user request (session policy in `AGENTS.md`)
- Multi-agent execution is an optimization; missing provider features must degrade to an equivalent direct workflow, not silently weaken safety or verification

---

## Docs map

| Doc | Purpose |
|-----|---------|
| [`AGENTS.md`](AGENTS.md) | Global agent playbook |
| [`ABOUT.md`](ABOUT.md) | Product / philosophy deep dive |
| [`docs/AGENTIT_INTERVIEW_AND_PROVIDER_POLICY.md`](docs/AGENTIT_INTERVIEW_AND_PROVIDER_POLICY.md) | Interview gate + cross-provider specialist semantics |
| [`docs/MCP_CATALOG.md`](docs/MCP_CATALOG.md) | MCP catalog & runtime |
| [`docs/ADAPTIVE_AGENT_ARCHITECTURE.md`](docs/ADAPTIVE_AGENT_ARCHITECTURE.md) | Topologies & contracts |
| [`agents/catalog.yaml`](agents/catalog.yaml) | Reusable specialist roles and skill bundles |
| [`incubator/candidates.yaml`](incubator/candidates.yaml) | Scout pipeline decisions |
| [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) | Design-skill upstream attribution and modification notices |

---

## License

Licensed under the [Apache License, Version 2.0](LICENSE). See [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) for third-party material and attributions.
