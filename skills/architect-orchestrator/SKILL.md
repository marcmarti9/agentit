---
name: architect-orchestrator
description: JIT orchestration for material work. Help the primary AI choose useful topology, bounded workers, independent alternatives/review, and deterministic Loop/Graph execution without imposing a fixed hierarchy.
---

# Adaptive orchestration

The primary AI owns decomposition, judgment, integration and the user-facing answer. This skill is optional JIT guidance when delegation, independent alternatives, graph ownership or bounded execution materially improves the task.

Agent roles are capabilities, not a mandatory org chart. Do not require an Architect/Supervisor/Worker hierarchy for work that does not benefit from it.

## Before topology

The primary AI should already have or construct a reviewed `TASK_DECISION` covering the material outcome, unresolved unknowns, relevant packs, selected skills/references/tools, complexity, risk, topology, plan and verification.

Before delegating:

1. inspect project/user constraints;
2. separate the desired outcome from a merely suggested implementation method;
3. challenge a materially weaker method and preserve the user's final safe discretionary choice;
4. ensure selected skill bodies/references are actually available JIT;
5. compare genuinely different alternatives before expensive-to-reverse structural commitment when that comparison has value;
6. choose topology from dependencies, ownership and useful independence;
7. instantiate deterministic Loop/Graph contracts for executable work when their enforcement is useful.

Do not ask users to choose internal pack names, worker counts or topology jargon.

## Why delegate

Useful reasons include:

- large independent reading/research sets;
- distinct implementation packages or ownership boundaries;
- different expertise/tools;
- independent hypotheses or design directions;
- fresh-context critique/review;
- isolation that reduces context contamination.

Stop when coordination costs more than the expected benefit. A capable parent model is not a reason to avoid all delegation, and multi-agent theater is not a reason to spawn workers.

## Structural alternatives

For a material public interface, service/module seam, persistence model, protocol, migration strategy or other expensive-to-reverse decision, compare more than the first plausible design when realistic alternatives exist.

Make alternatives genuinely different in seam/ownership/failure model, then compare interface simplicity, hidden complexity, locality, testability, operational risk, reversibility, migration cost and fit with project conventions. Record the durable conclusion, not private chain-of-thought.

## Topology vocabulary

Possible model-owned topologies include:

- `direct` — tightly coupled single-owner work;
- `probe` — read-only investigation;
- `fan_out` — genuinely independent research/packages/concepts;
- `pipeline` — dependent stages;
- `writer_reviewer` — one writer plus fresh review;
- `audit` — independent high-impact review;
- custom DAG — explicit multi-node dependencies/ownership.

These are options, not required stages. There are no hard minimum/maximum worker quotas.

## Worker Context Contract

Every delegated worker receives a bounded projection rather than the parent/global context dump:

- objective, scope and role;
- project instructions and explicit user constraints;
- relevant pack labels;
- selected skill bodies and selected references/artifacts;
- risk and parent topology;
- least-privilege capability envelope;
- allowed read/write ownership;
- expected output, verifier and stop condition.

Use `router/worker_context.py` for mechanical projection/validation. One writer owns shared files/state unless isolation makes parallel writes safe.

Provider adapters may implement spawning differently. The semantic worker contract remains provider-neutral.

# Runtime Loop Engineering

A Loop Contract is useful when an executable unit has an observable outcome and retries need deterministic bounds. It declares goal, verifier, stop condition, attempt budget and escalation boundary before action.

Resolve the Agentit root from the active installation/checkout rather than hardcoding a human path.

Example agent-facing commands:

```bash
python3 <agentit-root>/router/runtime_cli.py loop-init \
  --state .agentit/runtime/loops/<node-id>.json \
  --goal "<observable goal>" --verifier "<verifier>" --stop "<stop condition>"

python3 <agentit-root>/router/runtime_cli.py loop-check \
  --state .agentit/runtime/loops/<node-id>.json
```

The default runtime budget is bounded. Retries require fresh evidence or a meaningfully different strategy. Never weaken a verifier to manufacture success. Exhausted or invalid routes escalate instead of looping indefinitely.

# Runtime Graph Engineering

When execution genuinely has multiple dependent nodes, materialize a DAG under ignored `.agentit/runtime/`.

Each node defines:

- stable id/objective;
- dependencies;
- exclusive write paths (or read-only);
- expected handoff artifacts where relevant.

The deterministic runtime rejects cycles, invalid dependencies, unsafe paths and overlapping write ownership before execution. Only ready nodes should run; dependent completion requires accepted receipts/artifacts. Final graph success requires the graph verifier/receipt, not narrative confidence.

## Independent review

Use fresh independent review when consequence, structural commitment or uncertainty makes independence valuable. High-risk/security-sensitive/production/destructive work follows the stronger gates in the risk policy.

Reviewers challenge assumptions and evidence; they do not own routing or silently rewrite user intent. Same-context self-review is not independent when real independence is required.

## Design/public-facing work

Design work can benefit from independent reference research, alternative directions and fresh visual critique, but there is no fixed concept count or named quality tier. The primary AI chooses the amount of exploration justified by the requested ambition, uncertainty and cost.

When multiple directions are useful, make them genuinely different in visual thesis/composition/type/imagery/narrative—not palette swaps. Final implementation should still have clear ownership and browser/device verification appropriate to the claim.

## Skill loading

Load only the task/stage skills the primary AI selected. A skill ID in a catalog/worker spec is not equivalent to loading its body. Do not dump entire packs or the repository skill catalog into workers.

## Stop spawning when

- work is no longer independent;
- workers need conflicting write ownership;
- the remaining work is a tightly coupled integration decision;
- coordination/context cost exceeds expected expertise/independence benefit.

## Anti-patterns

- mandatory hierarchy;
- forced single-agent execution for ideology;
- workers for show;
- fixed worker quotas or fixed design-concept counts;
- legacy effort/craft tiers;
- parent serially reading a huge independent corpus without considering isolation;
- skill IDs without selected bodies;
- hardcoded local runtime paths;
- unbounded correction loops;
- completion claims without the required fresh verifier/receipt.
