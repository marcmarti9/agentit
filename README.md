# Agentit

[![CI Status](https://github.com/marcmarti9/agentit/actions/workflows/ci.yml/badge.svg)](https://github.com/marcmarti9/agentit/actions)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Release](https://img.shields.io/badge/version-v0.3.2--stable-green.svg)](https://github.com/marcmarti9/agentit/releases)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Bash 4.0+](https://img.shields.io/badge/bash-4.0+-green.svg)](https://www.gnu.org/software/bash/)

> **Agentit is a portable, provider-neutral meta-harness for safe AI coding-agent orchestration, skill routing, persistent context management, and ecosystem tool incubation.**
>
> *Configure, route, coordinate, and verify coding agents without locking yourself to one provider.*

---

> **Core philosophy:** Most multi-agent frameworks start by adding agents. **Agentit starts by asking if delegation is actually required.**

Agentit is an opinionated, safety-first meta-harness (v0.3.2) for predictable, vendor-neutral work across **Claude Code**, **OpenAI Codex**, **Google Antigravity / Open Skills**, and **Grok Build**.

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

That loads the **`using-agentit`** skill and runs the playbook:

1. **Route** — `python3 ~/code/agentit/router/route.py "task"`
2. **JIT profiles** — `agentit enable <profile> --project . --apply` when skills are missing
3. **Load the skills the work actually needs**; deep design work is explicitly allowed to spend context on craft
4. **Execute** single-agent-first; subagents only with a real topology + Worker Context Contract
5. **Verify** — no done/fixed/passing without fresh command evidence

Global policy: [`AGENTS.md`](AGENTS.md). Bootstrap skill: [`skills/using-agentit/SKILL.md`](skills/using-agentit/SKILL.md).

---

## Highlights

| Area | What you get |
|------|----------------|
| **Single-agent-first** | Direct work by default; Probe / Fan-Out / Pipeline / Writer-Reviewer / Audit only when isolation or risk justifies it |
| **Router** | Risk, topology, skills, preferences, verification flags — plan only, never permission to destroy |
| **Core + profiles** | 12-skill global `core`; opt-in project profiles (`frontend`, `design`, `backend`, `supabase`, …) |
| **Design studio** | Full-fat Taste + Impeccable + Emil design engineering + Figma MCP workflow + cinematic scrollytelling + GSAP + Three.js product storytelling |
| **Verification gauntlet** | Signal-gated probes + anti-greenwash (`agentit verify`) so “200 tests passed” is not enough alone |
| **Worker contracts** | `agentit worker build` / `router/worker_context.py` projects project instructions + task skills into subagents |
| **Context engines** | Tool-output filter, artifact refs (`agentit://`), session dedup |
| **MCP runtime** | Mid-session enable/disable via `agentit mcp` and optional `agentit-manager` gateway |
| **Scout / incubator** | Evaluate ecosystem ideas before promoting them |
| **Safe install** | Plan-first scripts, backups, SHA-256 sidecars, symlink rejection |

---

## Adaptive architecture

```
                  ┌─────────────────────────────────────┐
                  │            Task Request             │
                  └──────────────────┬──────────────────┘
                                     │
                          ┌──────────┴──────────┐
                          │   Heuristic Router  │
                          └──────────┬──────────┘
                                     │
     ┌──────────────────┬────────────┼────────────┬──────────────────┐
     ▼                  ▼            ▼            ▼                  ▼
┌──────────┐      ┌──────────┐  ┌──────────┐  ┌──────────┐     ┌──────────┐
│  Direct  │      │  Probe   │  │ Fan-Out  │  │ Pipeline │     │  Audit   │
│ (Single) │      │(Read-Only│  │ (Parallel│  │  (DAG)   │     │ (High-   │
└──────────┘      └──────────┘  └──────────┘  └──────────┘     │ Risk)    │
                                                               └──────────┘
```

---

## Shared skills (42)

`profiles.yaml` controls what is exposed per project. The engineering core remains bounded; the **design profile is intentionally craft-heavy**.

| Profile | Role |
|---------|------|
| **`core`** (12, global install) | `using-agentit`, `verification-gauntlet`, `task-router`, orchestration, debugging, review, TDD, security, source-driven, frontend UI, planning, `using-agent-skills` |
| **`frontend`** | Browser, performance, anti-slop design, Taste art direction |
| **`design`** | Frontend + full Taste + Impeccable + Emil + Figma + scrollytelling + GSAP + premium Three.js product storytelling |
| **`backend` / `supabase`** | API, observability, Postgres/Supabase practices |
| **`product` / `writing` / `release` / `research`** | Specs, marketing, launch, adversarial review |
| **`all`** | Escape hatch only |

Notable design skills:

```text
skills/
├── design-taste-frontend          # Full-fat art direction; quality over token minimization
├── impeccable-design              # Design-director craft floor, critique, polish, responsiveness
├── emil-design-eng                # Emil Kowalski-inspired interaction and motion craft
├── figma-design-workflow          # Official Figma MCP / design-system / Code Connect workflow
├── scrollytelling-web             # Narrative scroll architecture and engine selection
├── gsap-scrolltrigger             # Pin/scrub/timeline mechanics
├── gsap-performance               # High-motion runtime performance discipline
└── threejs-product-storytelling   # GLB/glTF, exploded products, camera/light/material direction
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

The `design` profile no longer optimizes the design methodology around minimizing tokens. It keeps the engineering core bounded, then deliberately spends context where visual craft needs it.

The stack has clear ownership rather than one giant contradictory prompt:

- **Taste** chooses the art direction, visual thesis, composition, type, material, and motion intensity.
- **Impeccable** acts as craft director across Persuade / Operate / Read / Experience surfaces and owns critique/polish/hardening.
- **Emil design engineering** owns interaction feel, easing, perceived performance, micro-interactions, and repeated-use motion restraint.
- **Figma workflow** uses the official MCP as structured design/design-system context rather than treating frames as screenshots.
- **Scrollytelling + GSAP** owns pinned, scrubbed, timeline-driven narrative work.
- **Three.js product storytelling** enters only when real spatial product work is justified: exploded assemblies, camera direction, materials, lighting, and depth.

For a cinematic product landing, a typical project setup is:

```bash
./agentit enable design --project . --apply
agentit mcp enable-stack frontend --apply
```

The existing `frontend` MCP stack includes **Context7 + Figma + Playwright + Chrome DevTools**. Figma should use the official remote MCP/OAuth flow; no Figma token belongs in the repository.

### Scrollytelling / product decomposition

`scrollytelling-web` deliberately chooses the smallest engine that can express the idea well:

- native CSS / scroll-driven animation for simple work;
- Motion for local React interaction;
- **GSAP ScrollTrigger** for serious pin/scrub/timeline choreography;
- image sequences for photorealistic pre-rendered transformation;
- **Three.js / React Three Fiber** for genuine 3D product decomposition and camera work.

Every cinematic sequence must have a reduced-motion path, a mobile strategy, reverse-scroll correctness, and end-to-end browser verification. A hero screenshot is not proof that a scroll narrative works.

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
agentit mcp enable-stack frontend --apply   # includes Figma + browser tooling
agentit mcp disable playwright --apply
```

Docs: [`docs/MCP_CATALOG.md`](docs/MCP_CATALOG.md). Starter engineering stack: **agentit-manager + Context7 + GitHub + Playwright**.

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

| Provider | What install configures |
|----------|-------------------------|
| **Claude Code** | Adaptive agents + core skills + optional settings/hooks |
| **Codex** | Core skills + portable workers (`terra_worker`, `luna_worker`) + guides |
| **Antigravity / Open Skills / Grok** | Core skills under `~/.agents/skills` |

See [`CODEX.md`](CODEX.md), [`CLAUDE.md`](CLAUDE.md), [`docs/ADAPTIVE_AGENT_ARCHITECTURE.md`](docs/ADAPTIVE_AGENT_ARCHITECTURE.md).

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

---

## Docs map

| Doc | Purpose |
|-----|---------|
| [`AGENTS.md`](AGENTS.md) | Global agent playbook |
| [`ABOUT.md`](ABOUT.md) | Product / philosophy deep dive |
| [`docs/MCP_CATALOG.md`](docs/MCP_CATALOG.md) | MCP catalog & runtime |
| [`docs/ADAPTIVE_AGENT_ARCHITECTURE.md`](docs/ADAPTIVE_AGENT_ARCHITECTURE.md) | Topologies & contracts |
| [`incubator/candidates.yaml`](incubator/candidates.yaml) | Scout pipeline decisions |
| [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) | Design-skill upstream attribution and modification notices |

---

## License

Licensed under the [Apache License, Version 2.0](LICENSE). See [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) for third-party material and attributions.
