# About Agentit

> **Agentit is a portable, provider-neutral harness for safe AI coding-agent orchestration, skill routing, and configuration management.**

---

## 🎯 The Core Philosophy

> *"Most multi-agent frameworks start by adding agents. **Agentit starts by asking if delegation is actually required.**"*

In the modern AI software engineering ecosystem, most agent frameworks default to complex, multi-tiered hierarchies (Architect → Orchestrator → Supervisor → Worker → Auditor) for even simple, 5-line bug fixes. This approach introduces three critical problems:

1. **Context Distortion**: Instructions are re-summarized across agent layers, eroding prompt fidelity and burning thousands of unnecessary context tokens.
2. **Latency Overhead**: Unnecessary agent handoffs create round-trip latency for tightly coupled tasks.
3. **Unsafe Execution**: Blindly running subagents without bounded contracts, file ownership, or verification gates leads to uncoordinated code edits.

**Agentit solves this by enforcing a Single-Agent-First architecture.** A single capable model handles tasks directly by default. Multi-agent topologies (Probe, Fan-Out, Pipeline, Writer-Reviewer, Audit) spawn **strictly when context isolation, parallel execution, or independent risk verification is required.**

---

## 🛠️ The Three Engineering Layers

Agentit structures agent orchestration across three distinct, complementary layers:

```
┌─────────────────────────────────────────────────────────────────┐
│                    Layer 1: Harness & Context                    │
│   (Permissions, Environment Isolation, Tools, Skills Registry)  │
└────────────────────────────────┬────────────────────────────────┘
                                 │
┌────────────────────────────────┴────────────────────────────────┐
│                    Layer 2: Local Bounded Loops                 │
│   (Observable Goal ──► Action ──► Evidence ──► Verification)    │
└────────────────────────────────┬────────────────────────────────┘
                                 │
┌────────────────────────────────┴────────────────────────────────┐
│                    Layer 3: Directed Graphs (DAG)               │
│   (Direct ── Probe ── Fan-Out ── Pipeline ── Writer/Reviewers)  │
└─────────────────────────────────────────────────────────────────┘
```

1. **Layer 1: Harness & Context Engineering**: Controls environment permissions, git worktree isolation, tool availability, and progressive disclosure of modular skills.
2. **Layer 2: Local Bounded Loops**: Defines how each agent acts, gathers empirical evidence, verifies changes against automated test suites, and halts upon completion or single-retry limits.
3. **Layer 3: Graph Engineering (DAG)**: Connects multiple bounded loops in deterministic acyclic graphs for parallel, non-overlapping work units.

---

## 🔌 Provider Neutrality

Agentit is designed from the ground up to be vendor-neutral. It decouples operational policies and shared skills from specific AI model runtimes:

- **Claude Code**: Native adaptive multi-agent profiles (`architect`, `auditor`, etc.) and hook management.
- **OpenAI Codex**: Scoped worker delegation profiles (`terra_worker`, `luna_worker`) without imposing rigid agent hierarchies.
- **Google Antigravity & Open Skills**: Automatic discovery via standardized `~/.agents/skills` conventions.
- **Grok Build & Others**: Compatible via standardized Open Skills discovery.

---

## 🛡️ Safety & Deterministic Controls

Agentit is built with a strict **safety-first engineering posture**:

- **Dry-Run by Default**: All management scripts (`install.sh`, `update.sh`, `harden-local.sh`) run in preview mode by default. File modifications occur strictly when passed an explicit `--apply` flag.
- **SHA-256 Backup Manifests**: Before overwriting or updating files, Agentit creates timestamped, private backup manifests with strict file permissions (`0700` directories, `0600` files).
- **Symlink Protection**: Scripts reject symlinked source or destination paths to prevent arbitrary file overwrite attacks.
- **Machine Isolation**: Environment secrets and local machine configurations remain isolated in gitignored files (`reports/local/inventory.yaml`, `settings.local.json`). Agentit never collects or stores secret credential values.

---

## 📄 Open Source & Community

Agentit is an early-stage, community-driven open-source project licensed under the [Apache License, Version 2.0](LICENSE).

- **GitHub Repository**: [https://github.com/marcmarti9/agentit](https://github.com/marcmarti9/agentit)
- **Contribution Guide**: [CONTRIBUTING.md](CONTRIBUTING.md)
- **Security Policy**: [SECURITY.md](SECURITY.md)
