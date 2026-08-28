# OpenAI Codex Integration & Setup Guide

Agentit keeps Codex semantically aligned with every other supported provider: the host sees only the three Agentit core navigation skills at startup, while task-specific expertise is loaded JIT from Agentit's private runtime.

## Skill surface

Codex's Agentit-visible skill root is:

```text
~/.agents/skills/
  using-agentit/
  task-router/
  using-agent-skills/
```

Do not project the rest of Agentit's catalog into this directory. Provider-native skill discovery can advertise installed skill metadata to the model before the full body is activated, so a large global skill directory is startup context pollution.

The full Agentit skill library remains private under:

```text
~/.agentit/runtime/skills
```

The coordinator discovers and loads non-core skills mechanically:

```text
agentit skills packs
agentit skills candidates engineering backend
agentit skills show debugging-and-error-recovery security-and-hardening --project .
```

See `docs/JIT_SKILL_LOADING.md` for the cross-provider contract.

## Portable worker profiles

Codex also has two host-specific execution/model profiles under `.codex/agents/`:

### `terra_worker`

- model: GPT-5.6 Terra
- reasoning effort: Medium
- role: routine bounded implementation, refactoring and tests when delegation helps.

### `luna_worker`

- model: GPT-5.6 Luna
- reasoning effort: Max
- role: high-context reading, complex implementation and larger isolated workloads.

These profiles are execution bindings, not semantic capabilities denied to other providers. The same selected Agentit skill bodies must remain usable directly in the parent when a native worker primitive is unavailable.

## Installation

The portable Python bootstrap is canonical:

```bash
python3 bootstrap.py --provider codex
python3 bootstrap.py --provider codex --apply
```

It installs the private Agentit runtime, projects only the three core skills to `~/.agents/skills`, preserves the two allowlisted worker profiles under `~/.codex/agents`, backs up replacements, and safely removes only provably unmodified legacy Agentit non-core copies from old Codex skill roots.

`~/.codex/config.toml` remains machine-local and is not overwritten by the normal Agentit bootstrap.

## Delegation contract

The coordinator retains user intent, semantic task decisions, integration and final acceptance. A worker receives only bounded objective/context, selected skill bodies, relevant references, permissions, ownership and verification requirements.

Workers do not get the whole Agentit skill catalog. A skill ID without its exact selected body does not count as activation.
