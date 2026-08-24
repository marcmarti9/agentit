# Evaluation results

## Current evidence status

This file records only evidence that still describes the **current LLM-native architecture**. Historical prompt-router numbers from the pre-refactor implementation are intentionally not carried forward as current results.

### What is mechanically covered by the repository

The current automated test surface includes deterministic contracts for:

- bounded skill profiles and safe project activation;
- capabilities and worker-context projection;
- MCP catalogs/runtime state;
- continuity and checkpoint state;
- context/artifact helpers;
- Loop/Graph runtime behavior and receipts;
- verification planning/execution and anti-greenwash receipts;
- architecture-policy invariants, including the prohibition on programmatic natural-language routing;
- install/update safety behavior in temporary fixtures;
- YAML/JSON/catalog validity and shell syntax through CI.

The public verification CLI additionally has regression coverage for explicit semantic signals: `--signal auth` can activate an auth-specific probe while natural-language task text alone is not parsed as a semantic router.

## Evidence that is intentionally not claimed

The repository currently does **not** provide a controlled agent-level benchmark proving that Agentit:

- produces better code than the same frontier model without Agentit;
- reduces tokens or cost;
- reduces wall-clock latency;
- improves every task type or provider equally;
- makes multi-agent execution worthwhile in all cases.

Those questions require paired real-agent experiments against a baseline as described in [`evaluation-plan.md`](evaluation-plan.md).

## Historical results

Older dated reports under `reports/` describe the architecture that existed when those reports were written. Some refer to the retired deterministic/heuristic semantic router and old skill counts. They are retained as project history and research evidence, **not** as documentation of current runtime behavior.

## CI rule

A local run, an old badge, or a historical result must never be represented as proof that current `HEAD` passes. For any public launch/release claim, cite the GitHub Actions result for the exact commit/tag being released.
