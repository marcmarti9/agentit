# Agentit documentation contract

Documentation is part of substantial implementation when it preserves knowledge that would otherwise be expensive to rediscover. It is not a requirement to publish temporary working state.

## Separate durable docs from operational state

- `.agentit/STATE.md` is local/private operational continuity by default.
- Repository Markdown is for durable project knowledge: architecture, interfaces, decisions, operations, troubleshooting, and verification procedures.

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

## Decision records

Use an ADR-style record for durable, non-obvious decisions whose rediscovery would be costly or risky. Record context, decision, realistic alternatives, consequences, and revisit conditions. Record evidence and conclusions, not private reasoning transcripts.

## Troubleshooting

For meaningful runtime systems, documentation should support:

`symptom -> likely causes -> diagnostic evidence -> corrective action -> verification`

Prefer exact stable commands, logs, metrics, artifact paths, health endpoints, or receipts over vague “check the logs” advice.

## Workflow

Before implementation, identify existing docs that may become stale. During implementation, update them when architecture/contracts/operations become stable. Before completion, check that materially changed docs are still true and links/paths exist.

Operational `.agentit/STATE.md` should be current when continuity is needed, but it stays local/private unless the project already has an intentional tracked status mechanism.

## Acceptance

A substantial task is sufficiently documented when a fresh competent agent or engineer can understand the materially changed architecture/contracts/decisions, reproduce relevant verification, and diagnose important known failure modes without replaying the original chat or reverse-engineering the entire codebase.
