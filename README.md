# Agentit

[![CI Status](https://github.com/marcmarti9/agentit/actions/workflows/ci.yml/badge.svg)](https://github.com/marcmarti9/agentit/actions)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Release](https://img.shields.io/badge/version-v0.1.0--alpha-orange.svg)](https://github.com/marcmarti9/agentit/releases)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Bash 4.0+](https://img.shields.io/badge/bash-4.0+-green.svg)](https://www.gnu.org/software/bash/)

> **Agentit is a portable, provider-neutral harness for safe AI coding-agent orchestration, skill routing, and configuration management.**
>
> *Configure, route, and coordinate coding agents without locking yourself to one provider.*

---

> 💡 **Core Philosophy**: Most multi-agent frameworks start by adding agents. **Agentit starts by asking if delegation is actually required.**

Agentit is an **early-stage, opinionated, and safety-first agent harness (v0.1.0-alpha)** designed for developers and AI engineers who want predictable, reproducible, and vendor-neutral agent orchestration across **Claude Code**, **OpenAI Codex**, **Google Antigravity / Open Skills**, and **Grok Build**.

---

## 🌟 Highlights

- **🎯 Single-Agent-First Architecture**: Avoids unnecessary agent hierarchies. Simple tasks execute directly; multi-agent topologies (Probe, Fan-Out, Pipeline, Writer-Reviewer, Audit) spawn strictly when context isolation, parallel execution, or independent verification is required.
- **🔌 Provider-Isolated Deployment**: Cleanly separates configurations across runtimes:
  - **Claude Code**: Adaptive agents (`architect`, `orchestrator`, `supervisor`, `worker`, `auditor`), hooks, and skills.
  - **OpenAI Codex**: Global `AGENTS.md`, isolated worker profiles (`terra_worker`, `luna_worker`), and shared skills.
  - **Antigravity & Open Skills**: Native `~/.agents/skills` repository discovery.
  - **Grok Build & Others**: Standardized Open Skills discovery.
- **🧠 Heuristic Task Router**: Evaluates tasks by risk level, complexity, required context, database signals, and skill dependencies without loading heavy skill bodies or executing commands.
- **📦 28 Production-Grade Skills**: Out-of-the-box skills covering TDD, systematic debugging, security hardening, API design, frontend UI engineering, performance optimization, and product/marketing strategy.
- **🛡️ Reversible & Safe Automation**: All deployment scripts (`install.sh`, `update.sh`, `harden-local.sh`) run in **dry-run plan mode by default**, requiring explicit `--apply` flags. Automatic SHA-256 backup manifests ensure 100% loss-free rollback.

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

### Supported Topologies

| Topology | Use Case | Ownership & Control |
|---|---|---|
| **Direct** | Focused or tightly coupled tasks | Single agent owns plan & implementation |
| **Plan + Direct** | Sequential multi-step work | Single owner with milestone checkpoints |
| **Probe** | Read-only investigation & reproduction | Returns evidence without mutating code |
| **Fan-Out** | Genuinely independent tasks | One owner per file/artifact |
| **Pipeline (DAG)** | Sequential stage dependencies | Each stage consumes validated artifacts |
| **Writer + Reviewers** | Implementation + independent review | Single writer; reviewers read-only |
| **Audit** | High-risk (security, auth, migrations) | Read-only auditor with fresh context |

For full design specifications, see [`docs/ADAPTIVE_AGENT_ARCHITECTURE.md`](docs/ADAPTIVE_AGENT_ARCHITECTURE.md).

---

## 🧰 Shared Skills Catalog

The repository includes 28 modular, production-tested skills:

```
skills/
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

### System Requirements

- **Linux / macOS** with Bash 4+
- **GNU Coreutils & Findutils**
- **Python 3.10+** with `PyYAML`

### Installation

Clone the repository and run the safe installer:

```bash
git clone https://github.com/marcmarti9/agentit.git ~/agentit
cd ~/agentit

# 1. Preview installation plan (Dry-Run by default)
bash install.sh

# 2. Apply installation to all providers with global guides
bash install.sh --apply --with-guides
```

To target a specific provider:

```bash
# Target only Claude Code
bash install.sh --provider claude --apply

# Target only OpenAI Codex
bash install.sh --provider codex --apply

# Target only Antigravity / Open Skills
bash install.sh --provider antigravity --apply
```

### Rollback & Safety

`install.sh` never overwrites files without creating a private, timestamped backup manifest in `~/backups/agentit-pre-install-<timestamp>/`. To roll back any installation, refer to [`ROLLBACK.md`](ROLLBACK.md).

---

## 🚦 Task Router & Risk Classifier

The task router provides heuristic task classification, risk inference, and context budgeting without executing shell commands or modifying files.

### CLI Usage

```bash
# Classify a standard task
python3 router/route.py "Implement user authentication with JWT"

# Force an explicit risk override (cannot lower inferred risk)
python3 router/route.py --risk RISK_3 "Migrate database schema"
```

### JSON Output Contract

```json
{
  "risk_level": "RISK_2",
  "recommended_topology": "direct",
  "context_budget": "STANDARD",
  "skills_available": [
    "security-and-hardening",
    "api-and-interface-design"
  ],
  "skills_recommended_missing": [],
  "routing_advice": [
    "Ensure authentication tokens are stored securely",
    "Add integration tests for failure cases"
  ]
}
```

### Local Machine Inventory

Generate an isolated, machine-specific inventory report (gitignored by default):

```bash
python3 -m router.inventory
```

Outputs `reports/local/inventory.yaml` with strict `0600` file permissions.

---

## ⚙️ Runtimes & Provider Integration

| Provider | Global Instructions | Agent / Worker Profiles | Skills Path |
|---|---|---|---|
| **Claude Code** | `~/CLAUDE.md`, `~/AGENTS.md` | `~/.claude/agents/` (`architect`, `auditor`, etc.) | `~/.claude/skills/` |
| **OpenAI Codex** | `~/CODEX.md`, `~/.codex/AGENTS.md` | `~/.codex/agents/` (`terra_worker`, `luna_worker`) | `~/.codex/skills/` |
| **Antigravity (AGY)** | `~/AGENTS.md` | Built-in Subagent Engine | `~/.agents/skills/` |
| **Grok Build** | `~/.grok/AGENTS.md`, `~/AGENTS.md` | Built-in Subagent Engine | `~/.grok/skills/` |

---

## 🧪 Testing & Verification

Run the test suite locally:

```bash
# Run router unit tests
python3 -m unittest discover -s router -p "test_*.py"

# Run full harness and installer tests
python3 -m unittest discover -s tests
```

---

## 📁 Repository Structure

```
agentit/
├── AGENTS.md                  # Canonical global instruction guide
├── CLAUDE.md                  # Claude Code runtime guide
├── CODEX.md                   # OpenAI Codex runtime guide
├── README.md                  # System documentation
├── LICENSE                    # Apache-2.0 License
├── CONTRIBUTING.md            # Contribution guidelines
├── SECURITY.md                # Security policy
├── ROLLBACK.md                # Safety & rollback guide
├── MIGRATION_PLAN.md          # Architectural migration guide
├── registry.yaml              # Portable skills & rules registry
├── install.sh                 # Safe, idempotent installer script
├── update.sh                  # Repository sync script
├── agents/                    # Multi-agent definitions for Claude Code
├── .codex/agents/             # Portable worker profiles for Codex
├── docs/                      # Technical architecture docs
├── evals/                     # Evaluation plans & benchmark results
├── policies/                  # Risk, context, and token policies
├── reports/                   # Security, quality, and inventory reports
├── router/                    # Heuristic task router engine & tests
├── security/                  # Local security hardening scripts
├── skills/                    # 28 modular shared skills
└── tests/                     # Integration and script test suite
```

---

## 🤝 Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for details on submitting pull requests, writing skills, and running tests.

---

## 📄 License

Licensed under the [Apache License, Version 2.0](LICENSE).
