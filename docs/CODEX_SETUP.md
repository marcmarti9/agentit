# OpenAI Codex Integration & Setup Guide

This guide describes how to configure, route, and manage OpenAI Codex worker profiles within the `Agentit` harness.

---

## Overview

Unlike Claude Code (which utilizes full multi-agent roles), OpenAI Codex is configured for **scoped delegation** using standalone, portable worker profiles.

The main coordinator agent retains user intent, architectural control, interface design, decomposition, and final acceptance. Heavy execution tasks (reading large files, implementing feature code, writing tests, running verifications) are delegated to isolated worker profiles.

---

## Portable Worker Profiles

Two lightweight TOML worker profiles are provided in `.codex/agents/`:

### 1. `terra_worker` (`.codex/agents/terra-worker.toml`)
- **Model**: GPT-5.6 Terra
- **Reasoning Effort**: Medium
- **Primary Role**: Default worker profile for mechanical code implementation, refactoring, writing unit tests, and routine tasks.

### 2. `luna_worker` (`.codex/agents/luna-worker.toml`)
- **Model**: GPT-5.6 Luna
- **Reasoning Effort**: Max
- **Primary Role**: High-context reading, complex logic implementation, large codebase analysis, or extensive refactoring.

---

## Installation & Deployment

The worker profiles are installed exclusively to `~/.codex/agents/` by `install.sh`:

```bash
# Preview installation plan
bash install.sh --provider codex

# Apply installation
bash install.sh --provider codex --apply
```

`install.sh` copies only declared worker profiles via an explicit allowlist and leaves your local `~/.codex/config.toml` untouched.

---

## Delegation Guidelines for Codex

### Coordinator Responsibilities
1. **Intent & Architecture**: Owns user requirements, API design, and module boundaries.
2. **Task Decomposition**: Breaks work into bounded, single-file or single-module subtasks.
3. **Diff Verification**: Reviews the actual git diff produced by workers rather than relying solely on text summaries.
4. **Final Acceptance**: Runs test suites and confirms completion before closing tasks.

### Worker Execution Rules
1. **Single Auto-Retry**: If a worker implementation fails verification (build, test, lint), return the failure output to the **same worker** with improved specifications. Do not spawn a new worker profile to bypass an error.
2. **Prohibited External Actions**: Workers must **NEVER** execute pull requests, git pushes, deployments, database migrations, or external network calls without explicit human authorization.
3. **Bounded Context**: Pass only the target file paths, contracts, and verifier recipes. Do not dump entire conversation histories into subagents.

---

## Local Configuration Safety

Local machine settings such as API keys, MCP servers, reasoning defaults, and custom backend flags belong in `~/.codex/config.toml`. 

Because `config.toml` contains environment-specific paths and local credentials, it is **never versioned** in this repository. Use `update.sh` to safely pull remote updates without overwriting local machine state:

```bash
bash update.sh --apply
```
