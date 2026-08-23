# Agentit documentation contract

Agentit treats documentation as part of the implementation, not as optional cleanup.

Whenever Agentit performs substantial work in a repository, a fresh competent agent should be able to understand the system, the decisions behind it, how its parts interact, and how to diagnose failures **without having to reverse-engineer the entire codebase or replay the original chat**.

This contract complements `docs/PROJECT_CONTINUITY.md`:

- `docs/agentit/STATE.md` answers **where the work is now and how to resume it**.
- durable project documentation answers **how the system works and why it is built this way**.

Both are mandatory when applicable.

## Core rule

For substantial repository work, Agentit must leave Markdown documentation sufficient to recover all durable engineering and product knowledge introduced or materially changed by the task.

Documentation must cover, as applicable:

1. **System architecture** — major layers, components, boundaries, dependencies, data/control flow and external systems.
2. **Individual components** — what each important module/service/package/script does, its inputs, outputs, state, dependencies and failure modes.
3. **Interfaces and contracts** — APIs, schemas, events, files, environment assumptions, invariants, ownership boundaries and compatibility constraints.
4. **Decisions** — what was decided, why, alternatives considered, trade-offs, consequences and conditions that would justify revisiting the decision.
5. **Operational behavior** — startup, runtime lifecycle, background jobs, persistence, retries, fallbacks, configuration and observability.
6. **Troubleshooting** — likely failure modes, symptoms, diagnostic steps, relevant logs/metrics/files, recovery actions and known limitations.
7. **Verification** — how correctness is checked and which tests or commands prove the documented behavior.
8. **Change impact** — when a change modifies architecture, contracts or behavior, update every affected canonical Markdown document in the same branch/PR.

Do not create documentation for trivial syntax or implementation details that are obvious from a tiny local function. Document knowledge whose rediscovery would require meaningful code reading, experimentation, history reconstruction or architectural reasoning.

## Canonical documentation layout

Reuse an existing project documentation structure when one exists. Do not create duplicate competing docs.

When a project has no suitable structure, prefer:

```text
docs/
  ARCHITECTURE.md
  components/
    <component>.md
  decisions/
    ADR-0001-<decision>.md
  OPERATIONS.md
  TROUBLESHOOTING.md
  agentit/
    STATE.md
```

The exact filenames are not mandatory. The information is.

### `ARCHITECTURE.md`

Keep a navigable model of the whole system:

- purpose and scope;
- high-level diagram in Mermaid when useful;
- major components and ownership boundaries;
- dependency direction;
- request/data/event flow;
- persistence and external integrations;
- security/trust boundaries when relevant;
- links to component and decision docs;
- architectural invariants and known constraints.

A reader should be able to answer: **what are the pieces, why do they exist, and how does information move through them?**

### Component documentation

Create or update a component document when a component has enough behavior that understanding it from scratch would require non-trivial code reading.

Recommended structure:

```markdown
# <Component>

## Responsibility
What this component owns and explicitly does not own.

## Where it lives
Relevant paths/packages/services.

## Inputs and outputs
Requests, events, files, functions, schemas or other contracts.

## How it works
Important execution flow and state transitions.

## Dependencies
Internal and external dependencies and why they are needed.

## Configuration
Relevant settings and defaults. Never include secrets.

## Failure modes
What can fail, visible symptoms and likely causes.

## Verification
Tests, checks or observability used to prove it works.

## Related decisions
Links to ADRs/decision records.
```

### Decision records

Any durable, non-obvious decision that would be expensive or risky to rediscover must be recorded.

Examples:

- choosing one architecture over another;
- changing a public/internal contract;
- introducing a new dependency or infrastructure primitive;
- selecting a persistence strategy;
- defining retry/fallback semantics;
- choosing a security boundary;
- intentionally rejecting an apparently simpler alternative.

Prefer an ADR-style Markdown record:

```markdown
# ADR-XXXX: <decision>

## Status
Accepted | Superseded | Deprecated

## Context
Facts and constraints that forced a decision.

## Decision
The durable choice.

## Alternatives considered
Realistic alternatives and why they were not selected.

## Consequences
Benefits, costs, risks and follow-up implications.

## Revisit when
Concrete conditions that should trigger reconsideration.
```

Record the decision summary and evidence, **not private chain-of-thought**.

## Troubleshooting contract

Documentation is insufficient if it only explains the happy path.

For systems with meaningful runtime behavior, maintain troubleshooting knowledge that maps:

`symptom -> likely causes -> diagnostic evidence -> corrective action -> verification`

Include exact commands or paths when they are stable and safe to document. Prefer deterministic diagnosis over vague advice such as “check the logs”.

For each important failure mode, identify where evidence lives: logs, metrics, database rows, generated artifacts, runtime receipts, health endpoints, queues, configuration or external provider state.

## Documentation workflow

Documentation must evolve together with the implementation.

### Before implementation

During inspection, identify the canonical documentation affected by the planned change. If none exists and the change introduces important architecture or behavior, plan the minimal durable documentation structure before coding.

### During implementation

Update documentation whenever one of these becomes stable:

- a durable architectural decision;
- a new/changed component responsibility;
- an interface or data-contract change;
- a non-obvious invariant;
- an operational requirement;
- a discovered failure mode or diagnostic procedure.

Do not wait until the final response and rely on memory.

### Before completion

Agentit may not declare substantial repository work complete until it has checked documentation drift.

The final verification must answer:

- Are the architecture docs still true?
- Are every materially changed component and contract explained?
- Are durable decisions recorded with rationale and consequences?
- Are new failure modes and diagnosis paths documented?
- Does `docs/agentit/STATE.md` accurately describe current status and next actions?
- Do documentation links and referenced paths actually exist?

If any answer is no, documentation is part of the unfinished work.

## Documentation quality rules

Documentation must be useful to a fresh agent or engineer, not merely prove that a file was written.

Prefer:

- explanations of intent and invariants over line-by-line restatement of code;
- concrete flows and examples over vague prose;
- links between architecture, components and decisions;
- Mermaid diagrams where they substantially reduce cognitive load;
- explicit ownership boundaries and failure modes;
- stable commands and reproducible checks.

Avoid:

- giant generated dumps;
- copying source code into Markdown;
- documenting every trivial helper;
- stale TODO inventories with no ownership/status;
- duplicate architecture descriptions that can silently disagree;
- secrets, credentials, private chain-of-thought or raw transcripts.

## Definition of documented

A substantial Agentit task is **documented** only when a fresh agent can, from repository Markdown plus referenced artifacts:

1. explain the relevant architecture from the system level down to the changed component;
2. explain what each materially affected piece does and how it interacts with the rest;
3. identify the important decisions and why they were made;
4. identify the contracts/invariants that must not be accidentally broken;
5. reproduce the relevant verification;
6. diagnose the known important failure modes without first reading the whole implementation;
7. recover current work state from `docs/agentit/STATE.md`.

This is the documentation acceptance criterion for Agentit.
