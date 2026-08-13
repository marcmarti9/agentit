# Implementation Plan: Provider-Neutral Capability Resolution

## Overview

Add a provider-neutral contract between semantic specialists and the concrete
tools available in a host. Specialists request stable capability IDs; a pure
resolver selects an explicitly available ChatGPT app, MCP server, CLI, or local
implementation and emits a least-privilege envelope with an explainable fallback
chain. Unknown availability never becomes an assumed grant.

## Architecture Decisions

- Keep provider names out of specialist declarations. `agents/catalog.yaml`
  declares only required and preferred capability IDs.
- Store provider bindings and ordered implementation choices in
  `capabilities/catalog.yaml`; runtime inventory is an explicit input.
- Keep resolution deterministic, offline, and plan-only. It does not authenticate,
  install, enable, or call a provider.
- Project only selected provider permissions into delegated worker contexts.
  Required capabilities fail the pre-spawn gate when inventory proves they are
  unresolved; an omitted inventory remains an honest planning state.
- Extend router output without changing existing risk, skill, or topology fields.

## Task List

### Phase 1: Contract

- [x] Add failing catalog/resolver tests for validation, ordered fallback,
  host compatibility, and unresolved requirements.
- [x] Add failing router and worker-context tests for specialist-derived
  requirements and least-privilege envelopes.

### Checkpoint: Red

- [x] New tests fail because the capability layer does not exist yet.

### Phase 2: Implementation

- [x] Add the capability/provider catalog and pure resolver.
- [x] Declare capabilities for every semantic specialist.
- [x] Integrate specialist requirements and resolution into router output.
- [x] Integrate the resolved envelope into worker context and its spawn gate.

### Checkpoint: Green

- [x] Targeted capability, router, specialist, and worker tests pass.
- [x] Existing router and script suites remain green.

### Phase 3: Public Contract

- [x] Document inventory shape, fallbacks, least privilege, and extension steps.
- [x] Add representative eval cases and CI catalog validation.
- [x] Run Agentit verification, inspect the diff, commit, push, and open a draft PR.

## Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Host availability cannot be observed portably | High | Require an explicit inventory; never assume a plugin is authenticated or callable. |
| Provider mappings leak into specialist policy | High | Catalog tests reject provider IDs in specialist capability declarations. |
| Delegated workers receive excessive permissions | High | Emit only the selected binding and capability-scoped permissions; test absence of unrelated grants. |
| New output breaks router consumers | Medium | Add fields without removing or renaming the existing contract. |
| Work conflicts with pending PR #12 | Medium | Base this branch on `main` and limit edits to stable specialist/router/worker seams. |

## Open Questions

- None blocking. Additional private or workspace-only apps can be added later as
  provider bindings without changing specialist contracts.
