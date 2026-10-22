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
agentit skills activate debugging-and-error-recovery security-and-hardening --project .
```

See `docs/JIT_SKILL_LOADING.md` for the cross-provider contract.

## Portable worker profiles

Codex also has two host-specific execution/model profiles under `.codex/agents/`:

### `terra_worker`

- model: GPT-5.6 Terra
- reasoning effort: Medium
- role: routine bounded implementation, refactoring and tests when delegation helps.

### `luna_worker` — execution only, supervised by Sol

- model: GPT-6 Luna (`gpt-6-luna`)
- reasoning effort: Max
- supervisor: GPT-6.1 Sol or GPT-6 Sol, declared in the delegation contract.
- role: execute concrete, already-decided steps inside bounded paths; report results and escalate ambiguity.

Use it for applying a specified patch, repeating an approved transformation, extracting named facts from specified files or running listed checks. Do not select Luna because a task has a large context or produces much text. Do not assign open-ended implementation/research, diagnosis, architecture, product/security decisions, independent review, approval or supervision. These choices remain with Sol. Explicit `model` overrides and generic roles must respect the same limit.

Before spawning, Sol supplies its model, decided steps, allowed read/write paths, expected output, exact acceptance commands and stop/escalation conditions together with the actual schema-3 context. Missing contract parts stop execution. Unexpected findings return to Sol; selected skills do not expand Luna's authority. Sol inspects the actual diff/output and evidence before acceptance. Luna does not commit, push, deploy, migrate, delete data/backups or mutate external systems.

This is an instruction/selection contract, not an OS sandbox or cryptographic supervisor-model check. Host restrictions still need separate enforcement. Message counts alone do not establish which decisions a model took.

These profiles are execution bindings, not semantic capabilities denied to other providers. The same selected Agentit skill bodies must remain usable directly in the parent when a native worker primitive is unavailable.

## Installation

The portable Python bootstrap is canonical:

```bash
python3 bootstrap.py --provider codex
python3 bootstrap.py --provider codex --apply
```

It installs the private Agentit runtime, projects only the three core skills to `~/.agents/skills`, preserves the two allowlisted worker profiles under `~/.codex/agents`, backs up replacements, and safely removes only provably unmodified legacy Agentit non-core copies from old Codex skill roots.

`~/.codex/config.toml` remains machine-local and is not overwritten by the normal Agentit bootstrap.

Updating the repository does not update another machine: run the bootstrap there too. Already-running chats can retain old role descriptions/model bindings; start a fresh session and verify its exposed role/model before using the updated worker. The normal bootstrap does not rewrite previous chats, unrelated custom roles or provider-internal models.

The exact model ID and custom-agent `model` binding are documented by [OpenAI's Luna model page](https://developers.openai.com/api/docs/models/gpt-6-luna) and [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), checked 2026-10-22.

## Delegation contract

The coordinator retains user intent, semantic task decisions, integration and final acceptance. A worker receives only bounded objective/context, selected skill bodies, relevant references, permissions, ownership and verification requirements.

Workers do not get the whole Agentit skill catalog. A skill ID without its exact selected body does not count as activation.
