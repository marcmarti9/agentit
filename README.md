# Agentit

[![CI Status](https://github.com/marcmarti9/agentit/actions/workflows/ci.yml/badge.svg)](https://github.com/marcmarti9/agentit/actions)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Release](https://img.shields.io/badge/version-v0.3.2--stable-green.svg)](https://github.com/marcmarti9/agentit/releases)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Bash 4.0+](https://img.shields.io/badge/bash-4.0+-green.svg)](https://www.gnu.org/software/bash/)

> **Agentit is a portable, provider-neutral meta-harness for safe AI coding-agent orchestration, skill routing, persistent context management, and ecosystem tool incubation.**
>
> *Configure, route, compress context, and coordinate coding agents without locking yourself to one provider.*

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
3. **Load only recommended skills** (progressive disclosure; references on demand)
4. **Execute** single-agent-first; subagents only with a real topology + Worker Context Contract
5. **Verify** — no done/fixed/passing without fresh command evidence

Global policy: [`AGENTS.md`](AGENTS.md). Bootstrap skill: [`skills/using-agentit/SKILL.md`](skills/using-agentit/SKILL.md).

---

## Highlights

| Area | What you get |
|------|----------------|
| **Single-agent-first** | Direct work by default; Probe / Fan-Out / Pipeline / Writer-Reviewer / Audit only when isolation or risk justifies it |
| **Router** | Risk, topology, skills, preferences, verification flags — plan only, never permission to destroy |
| **Core + profiles** | 11-skill global `core`; opt-in project profiles (`frontend`, `design`, `backend`, `supabase`, …) |
| **Design taste** | `design-taste-frontend` for landings/portfolios: dials, AI tells, pre-flight, **agent-fetchable inspiration sources** (no user screenshots required) |
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

## Shared skills (34)

`profiles.yaml` controls discovery cost:

| Profile | Role |
|---------|------|
| **`core`** (11, global install) | `using-agentit`, `task-router`, `architect-orchestrator`, debugging, review, TDD, security, source-driven, frontend UI, planning, `using-agent-skills` |
| **`frontend` / `design`** | Browser, performance, anti-slop design, **`design-taste-frontend`** |
| **`backend` / `supabase`** | API, observability, Postgres/Supabase practices |
| **`product` / `writing` / `release` / `research`** | Specs, marketing, launch, adversarial review |
| **`all`** | Escape hatch only |

```
skills/
├── anti-ai-slop-design           # Short brand-authentic anti-cliché checklist
├── anti-ai-slop-writing          # Purges AI writing buzzwords & filler
├── api-and-interface-design      # API contracts & module boundaries
├── architect-orchestrator        # Adaptive multi-agent routing
├── browser-testing-with-devtools # Browser & DOM verification
├── ci-cd-and-automation          # Pipeline automation & quality gates
├── code-review-and-quality       # Multi-axis code review
├── code-simplification           # Refactoring for readability
├── context-engineering           # Context optimization & memory
├── debugging-and-error-recovery  # Root-cause debugging workflow
├── deprecation-and-migration     # Legacy sunsetting & migrations
├── design-taste-frontend         # Landings/portfolios: dials, AI tells, agent refs
├── documentation-and-adrs        # ADRs & technical specs
├── doubt-driven-development      # Adversarial review before commit
├── find-skills                   # Skill discovery helper
├── frontend-ui-engineering       # Production-quality accessible UI
├── git-workflow-and-versioning   # Semantic versioning & git flows
├── idea-refine                   # Idea stress-testing & convergence
├── incremental-implementation    # Small step-by-step deliveries
├── interview-me                  # Requirement clarification
├── marketing-and-growth          # Technical SEO, CRO & copywriting
├── observability-and-instrumentation # Logging, metrics, tracing
├── performance-optimization      # Profiling & bottleneck fixing
├── planning-and-task-breakdown   # Work breakdown structures
├── security-and-hardening        # Vulnerability mitigation & audit
├── shipping-and-launch           # Pre-launch checklists & rollouts
├── source-driven-development     # Official documentation grounding
├── spec-driven-development       # Spec creation before coding
├── supabase-postgres-best-practices # Postgres query & schema rules
├── task-router                   # Heuristic task classifier
├── test-driven-development       # TDD & test-first implementation
├── using-agent-skills            # Lifecycle skill discovery map
├── using-agentit                 # Session bootstrap: "usa/use agentit"
└── verification-before-completion # Fresh evidence before done claims
```

### Design taste (landings without screenshots)

`design-taste-frontend` (profiles **`design`** / **`frontend`**) is a slim Agentit adaptation of [taste-skill](https://github.com/Leonxlnx/taste-skill) ideas:

- Design read + variance / motion / density dials  
- Layout hard rules and production AI-tells  
- **`references/inspiration-sources.md`**: galleries and docs that **agents can fetch as text** (Supahero, Minimal/mnmm, shadcn, 21st.dev, Fonts In Use, …) — no user screenshots required  
- Progressive disclosure: short `SKILL.md`, deep refs only when needed  

Enable on a project:

```bash
./agentit enable design --project . --apply
# or
./agentit enable frontend --project . --apply
```

---

## MCP catalog & runtime

Agents can list and toggle curated MCPs mid-session:

```bash
agentit mcp install-gateway --apply   # once: agentit-manager meta MCP
agentit mcp status
agentit mcp enable context7 --apply
agentit mcp enable-stack developer_core --apply
agentit mcp disable playwright --apply
```

Docs: [`docs/MCP_CATALOG.md`](docs/MCP_CATALOG.md). Starter stack: **agentit-manager + Context7 + GitHub + Playwright**.

---

## Quick start

### Install

```bash
git clone https://github.com/marcmarti9/agentit.git ~/code/agentit
cd ~/code/agentit

# Dry-run plan (default)
bash install.sh --provider all --with-guides

# Apply: core skills + AGENTS.md / CLAUDE.md / CODEX.md
bash install.sh --provider all --with-guides --apply

# Optional: CLI on PATH
ln -sf ~/code/agentit/agentit ~/.local/bin/agentit
```

Default skill install path for Open Skills / Grok: `~/.agents/skills/`.  
Claude: `~/.claude/skills/`. Codex: `~/.codex/skills/`.

### Route a task

```bash
python3 ~/code/agentit/router/route.py "Rediseña la landing de un SaaS B2B"
# → skills_available may include design-taste-frontend; topology usually direct
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
# Router + profiles + MCP + worker context (~122 tests)
python3 -m unittest discover -s router -p "test_*.py"

# Installer / harness scripts (~17 tests)
python3 -m unittest discover -s tests

# Deterministic eval cases
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
| [`AGENTS.md`](AGENTS.md) | Global agent playbook (trigger phrases + compact harness) |
| [`ABOUT.md`](ABOUT.md) | Product / philosophy deep dive |
| [`docs/MCP_CATALOG.md`](docs/MCP_CATALOG.md) | MCP catalog & runtime |
| [`docs/ADAPTIVE_AGENT_ARCHITECTURE.md`](docs/ADAPTIVE_AGENT_ARCHITECTURE.md) | Topologies & contracts |
| [`incubator/candidates.yaml`](incubator/candidates.yaml) | Scout pipeline decisions |
| [`skills/design-taste-frontend/references/inspiration-sources.md`](skills/design-taste-frontend/references/inspiration-sources.md) | Agent-fetchable design refs |

---

## License

Licensed under the [Apache License, Version 2.0](LICENSE).
