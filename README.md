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

> 💡 **Core Philosophy**: Most multi-agent frameworks start by adding agents. **Agentit starts by asking if delegation is actually required.**

Agentit is an opinionated, safety-first meta-harness (v0.3.2) designed for developers and AI engineers who want predictable, reproducible, and vendor-neutral agent orchestration across **Claude Code**, **OpenAI Codex**, **Google Antigravity / Open Skills**, and **Grok Build**.

---

## 🌟 Highlights

- **🎯 Single-Agent-First Architecture**: Avoids unnecessary agent hierarchies. Simple tasks execute directly; multi-agent topologies (Probe, Fan-Out, Pipeline, Writer-Reviewer, Audit) spawn strictly when context isolation, parallel execution, or independent verification is required.
- **⚡ Native Context Engine Pipeline**:
  - **Tool Output Filtering (`router/tool_filter.py`)**: Format-aware adapters (`pytest`, `unittest`, `jest`, `cargo`, `generic`) prune noisy build/test output while preserving 100% of stack traces and failure evidence.
  - **Artifact References & CCR (`router/artifact_ref.py`)**: Archives text blocks (>150 lines or >10KB) into `.agentit/artifacts/` with sidecar SHA-256 metadata (`ref-<hash>.json`) and a secure `agentit://` URI resolver.
  - **Session Deduplication (`router/dedup.py`)**: Persists SHA-256 context hashes across CLI executions in `.agentit/sessions/<id>/dedup.json` with strict `0600` permissions and symlink protection.
- **🔬 Scout & Incubator Meta-Harness (`router/scout.py`)**: Ingests, evaluates, and classifies ecosystem ideas, repos, papers, and tweets (e.g. NanoNets Graft, Claude Company profiles) into a structured incubator (`incubator/candidates.yaml`) before promoting them to core architecture.
- **🔌 Provider-Isolated Deployment**: Cleanly separates configurations across runtimes:
  - **Claude Code**: Adaptive agents (`architect`, `orchestrator`, `supervisor`, `worker`, `auditor`), hooks, and skills. (Fully Supported)
  - **OpenAI Codex**: Global `AGENTS.md`, isolated worker profiles (`terra_worker`, `luna_worker`), and shared skills. (Fully Supported)
  - **Antigravity & Open Skills**: Native `~/.agents/skills` repository discovery. (Compatible via Open Skills)
  - **Grok Build & Others**: Standardized Open Skills discovery. (Compatible via Open Skills)
- **🧠 Heuristic Task Router**: Evaluates tasks by risk level, complexity, required context, database signals, and skill dependencies without loading heavy skill bodies or executing commands.
- **📦 31 Curated Shared Skills**: Out-of-the-box skills covering TDD, systematic debugging, security hardening, API design, frontend UI engineering, anti-AI-slop writing & design, and marketing & growth.
- **📉 Bounded Skill Discovery**: Only the 10-skill `core` profile is installed globally by default. Opt-in project profiles (`product`, `writing`, `design`, `supabase`, `frontend`, `backend`, `release`, `research`) remain on-demand to stay within Codex context budgets.
- **🛡️ Reversible & Safe Automation**: All scripts run in **dry-run plan mode by default** with strict `0700`/`0600` permissions, atomic `mkstemp` IO, symlink component rejection, and sidecar SHA-256 integrity validation.

---

## 🏗️ Adaptive Architecture

Rather than forcing a rigid top-down pyramid (Architect → Orchestrator → Worker), Agentit dynamically selects the minimal viable topology based on task independence, context budget, and risk:

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

## 🧰 Shared Skills Catalog (31 Skills)

`profiles.yaml` defines the installation visibility policy:

- `core`: 10 general skills installed globally by `install.sh`.
- `frontend`, `backend`, `supabase`, `product`, `writing`, `design`, `release`, and `research`: opt-in project profiles.
- `all`: explicit escape hatch for experiments.

```
skills/
├── anti-ai-slop-design           # Brand-authentic visual identity & UI anti-slop rules
├── anti-ai-slop-writing          # Purges 20+ AI writing buzzwords & empty filler
├── api-and-interface-design      # API contracts & module boundaries
├── architect-orchestrator        # Adaptive multi-agent routing
├── browser-testing-with-devtools # Browser & DOM verification
├── ci-cd-and-automation          # Pipeline automation & quality gates
├── code-review-and-quality       # Multi-axis code review
├── code-simplification           # Refactoring for readability
├── context-engineering           # Context optimization & memory
├── debugging-and-error-recovery  # Root-cause debugging workflow
├── deprecation-and-migration     # Legacy sunsetting & migrations
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
└── using-agent-skills            # Meta-skill for skill discovery
```

---

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/marcmarti9/agentit.git ~/agentit
cd ~/agentit

# 1. Preview installation plan (Dry-Run by default)
bash install.sh

# 2. Apply installation to all providers with global guides
bash install.sh --apply --with-guides
```

### CLI Commands

```bash
# Manage project skill profiles
./agentit enable supabase --project . --apply
./agentit status --project .
./agentit disable supabase --project . --apply

# Context engine commands
./agentit context filter build.log
./agentit context archive migration.sql --description "DB Schema"
./agentit context dedup "context block" --session session-123

# Artifact retrieval & verification
./agentit artifact get agentit://artifacts/ref-a1b2c3d4.txt
./agentit artifact read agentit://artifacts/ref-a1b2c3d4.txt --lines 1:50
./agentit artifact grep agentit://artifacts/ref-a1b2c3d4.txt "AssertionError"

# Scout & Incubator pipeline
./agentit scout status
./agentit scout add "https://github.com/NanoNets/Graft"
./agentit scout inspect nanonets-graft
./agentit scout reject caveman-lossy-prose --reason "Syntax truncation risk"
```

---

## 🧪 Testing & Verification

```bash
# Run router unit tests (76 tests)
python3 -m unittest discover -s router -p "test_*.py"

# Run full harness and installer tests (17 tests)
python3 -m unittest discover -s tests

# Run deterministic evaluation cases (10 cases)
python3 evals/run.py
```

---

## 📄 License

Licensed under the [Apache License, Version 2.0](LICENSE).
