# Agentit state

**Updated:** 2026-08-12
**Status:** review fixes implemented; verification in progress
**Branch:** feat/intelligent-orchestration-v1
**PR:** https://github.com/marcmarti9/agentit/pull/12

## Goal

Deliver intelligent orchestration for Agentit: domain skill packs, design-only craft depth, project-aware tokens, smart spawn without hard caps, mandatory critic for large plans, MCP fit, long-horizon recovery, evidence-based verification, and first-class local model routing.

## Confirmed intent

- Audience: Agentit users and agents across providers
- Success: single vs multi decision is intelligent; no Studio tax on non-design; no powerwords except natural Agentit activation; recovery/verify/local models real
- Constraints: safety floors, one-writer, PR-first, no multi chaos
- Non-goals: multi-agent-by-default framework

## Domain pack

- Pack: engineering (harness/orchestration)
- Craft depth: n/a (not design/visual product UI)
- Spend: thorough
- Token estimate: project-aware via router `--project`
- Topology: fan_out / pipeline / writer_reviewer as signals dictate
- Critic required: yes for structural plans

## Current status

- Complete: router intelligence, domain packs, craft-depth design-only, MCP skill, continuity module, local model catalog, verification claim gate, worker orchestration fields, tests/evals; affirmative Agentit activation; vendor-neutral data profile routing
- In progress: final verification / PR update / merge
- Blocked: none
- Not started: optional follow-ups after merge (deeper MCP marketplace automation UI)

## Decisions

- Craft depth Standard/Polished/Studio is design-only
- No hard subagent min/max
- Natural language only; Agentit activation is the sole special phrase
- Project signals feed token estimates
- Local models are capability-tier first-class via preferences

## Important files and artifacts

- `router/route.py`, `router/continuity.py`, `router/project_signals.py`, `router/verify.py`, `router/worker_context.py`
- `effort/levels.yaml`, `models/capabilities.yaml`
- `skills/mcp-tooling-fit`, `long-horizon-recovery`, `local-model-routing`
- PR #12

## Verification

- router unit tests: 166 OK
- tests/: 17 OK
- evals: 14/14 after adversarial activation and MySQL profile cases
- Manual route smoke: fan_out + project signals + models + claims_without_evidence

## Next actions

1. Review/merge PR #12
2. After merge, reinstall core profile so `mcp-tooling-fit` + `long-horizon-recovery` are global
3. Optional: wire provider-native local endpoint probes

## Open questions / blockers

- None for this PR scope

## Recovery

- Last checkpoint: PR #12 branch
- Resume: read this file → `git checkout feat/intelligent-orchestration-v1` → continue Next actions
- Mid-task re-route: `agentit trace "<goal>" --project .`
