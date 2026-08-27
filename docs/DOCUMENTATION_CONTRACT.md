# Agentit documentation contract

Documentation is part of substantial implementation when it preserves knowledge that would otherwise be expensive to rediscover. It is not a requirement to publish temporary working state.

The minimum version of this contract is intentionally repeated in the global `using-agentit` core skill so a fresh session cannot miss it. The deeper `documentation-and-adrs` skill remains JIT.

## Separate durable docs from operational state

- `.agentit/STATE.md` is local/private operational continuity by default.
- Repository Markdown is for durable project knowledge: architecture, component responsibilities, interfaces, decisions, operations, troubleshooting, and verification procedures.

Never commit private task plans, launch plans, raw chats, credentials, or chain-of-thought merely because Agentit used them during execution.

## What durable documentation should cover

When materially affected, document:

1. system architecture and boundaries;
2. important component responsibilities and data/control flow;
3. interfaces, schemas, events, files, configuration assumptions, and invariants;
4. non-obvious durable decisions and trade-offs;
5. operational behavior, persistence, retries, fallbacks, and observability;
6. important failure modes and deterministic diagnostic/recovery steps;
7. reproducible verification;
8. documentation drift caused by the current change.

Do not create Markdown for trivial helpers or obvious syntax.

## Component-level rule

A fresh engineer or agent should be able to understand each **material responsibility** without reverse-engineering the whole repository.

For a component/subsystem that has meaningful behavior of its own, its canonical documentation should make clear, as applicable:

```text
purpose / ownership
inputs and outputs
public interfaces and important internal boundaries
data + control flow
state / persistence
configuration and invariants
external dependencies
failure modes / retries / fallbacks
observability / diagnostics
how to verify it
where its implementation lives
```

This does **not** mean “one Markdown file per class/function.” Split documentation by responsibility when that improves understanding; combine tightly coupled material only when one document remains clearer than several. The goal is navigable system knowledge, not file-count maximization or minimization.

When multiple components interact, keep a higher-level architecture/integration view that explains their relationships and links to the deeper component docs. A component page without its system context, or an architecture page with no usable component detail, is incomplete when both levels materially matter.

## Reuse the project's structure

Prefer the project's existing documentation layout. If none exists and the change creates enough durable knowledge to justify one, a reasonable default is:

```text
docs/
  ARCHITECTURE.md
  components/
  decisions/
  OPERATIONS.md
  TROUBLESHOOTING.md
```

The information matters more than exact filenames.

Avoid parallel sources of truth such as `ARCHITECTURE-new.md`, task-history dumps, or several documents repeating the same contract. Update the canonical source and link outward from it.

## Decision records

Use an ADR-style record for durable, non-obvious decisions whose rediscovery would be costly or risky. Record context, decision, realistic alternatives, consequences, and revisit conditions. Record evidence and conclusions, not private reasoning transcripts.

Not every implementation choice deserves an ADR. Prefer component/architecture docs for how the system currently works; use ADRs for why a consequential choice was made when that history remains useful.

## Troubleshooting

For meaningful runtime systems, documentation should support:

`symptom -> likely causes -> diagnostic evidence -> corrective action -> verification`

Prefer exact stable commands, logs, metrics, artifact paths, health endpoints, or receipts over vague “check the logs” advice.

## Workflow

Before implementation, identify existing docs that may become stale and map material components affected by the change. During implementation, update their canonical documentation when architecture/contracts/operations become stable. Before completion, check that materially changed docs are still true, links/paths exist, and cross-component diagrams or architecture summaries still match reality.

Operational `.agentit/STATE.md` should be current when continuity is needed, but it stays local/private unless the project already has an intentional tracked status mechanism.

Documentation and implementation should normally ship in the same reviewable change. “We will document it later” is not completion for substantial durable behavior unless the user explicitly scopes documentation out.

## Acceptance

A substantial task is sufficiently documented when a fresh competent agent or engineer can:

- find the canonical architecture entry point;
- understand each materially changed component/responsibility and how it interacts with the rest of the system;
- identify important interfaces, invariants, configuration and failure behavior;
- reproduce relevant verification;
- diagnose important known failure modes;
- understand durable non-obvious decisions that materially constrain future work;

without replaying the original chat or reverse-engineering the entire codebase.
