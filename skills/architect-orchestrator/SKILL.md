---
name: architect-orchestrator
description: Intelligent orchestration after interview. Delegate for expertise, independence, context isolation and critique; enforce Loop and Graph Engineering at runtime.
---

# Adaptive Agent Architecture

The Architect owns the user relationship, decomposition, judgment, integration and final answer. Multi-agent is neither mandatory nor a fallback: use it whenever it materially improves outcome, context hygiene or independent judgment.

## Before topology

1. mechanical vs product-affecting;
2. product work -> load and run `interview-me`;
3. choose domain pack;
4. craft depth only for visual/design work;
5. ensure selected skill **bodies** are actually loaded, not just their IDs;
6. choose topology based on dependencies + useful independence;
7. instantiate runtime contracts before execution: bounded loops for every executable unit, and a validated graph for multi-node work.

## No single-agent gravity

Do not ask only “can one agent do this?”. Ask “does isolation or independent work improve this?”. Valid reasons to delegate include independent packages/files/domains, large documentation/reference sets, several research hypotheses/lenses, different expertise/tools, creative concept diversity and independent critique/review.

A strong parent should spend scarce context on synthesis and hard decisions. Use capable workers for high-volume reading/research when available and require bounded receipts/evidence. The parent verifies and integrates; it does not blindly trust summaries.

Do not hardcode provider model names into portable policy. Provider adapters map semantic tiers: judgment-heavy parent, capable research/implementation worker, independent critic.

## Topologies

- `direct`: tightly coupled single-thread work with no material isolation benefit;
- `probe`: read-only investigation;
- `fan_out`: independent research/packages/concepts;
- `pipeline`: dependent stages;
- `writer_reviewer`: one owner + fresh review;
- `audit`: high-impact independent review;
- design competition: independent concepts followed by explicit jury;
- DAG: multi-package dependencies when needed.

`subagents.recommended` is soft guidance. No hard min/max quotas.

# Runtime Loop Engineering

Loop Engineering is mandatory for every executable unit, including work performed directly by the Architect when it has a verifiable outcome. A loop declares **observable goal, verifier, stop condition, attempt budget and escalation boundary** before action.

Use the runtime state machine rather than prose promises:

```bash
python3 ~/code/agentit/router/runtime_cli.py loop-init \
  --state .agentit/runtime/loops/<node-id>.json \
  --goal "<observable goal>" --verifier "<verifier>" --stop "<stop condition>"
```

Record every attempt with actual evidence. The default budget is 2 attempts total (one automatic retry). A retry must provide fresh evidence or a different strategy. Do not weaken/fix the verifier to manufacture progress.

A unit is complete only if:

```bash
python3 ~/code/agentit/router/runtime_cli.py loop-check --state .agentit/runtime/loops/<node-id>.json
```

returns success. The resulting `Loop Receipt` is the evidence accepted by Graph Engineering. Narrative “done” without a passed receipt is not completion.

If the budget is exhausted, evidence shows the approach is invalid, or a material decision leaves the authorized scope, escalate instead of looping indefinitely.

# Runtime Graph Engineering

When topology has more than one execution node, materialize it as a DAG before spawning work. Store runtime artifacts under ignored `.agentit/runtime/`.

A graph spec defines for each node:

- stable node id and objective;
- dependency ids;
- exclusive `write_paths` ownership (read-only nodes use none);
- expected handoff artifacts where relevant.

Initialize/validate:

```bash
python3 ~/code/agentit/router/runtime_cli.py graph-init \
  --spec .agentit/runtime/graph-spec.json \
  --state .agentit/runtime/graph.json
```

The runtime rejects cycles, unknown/self dependencies, unsafe paths and overlapping write ownership before execution.

Spawn **only** nodes returned by:

```bash
python3 ~/code/agentit/router/runtime_cli.py graph-ready --state .agentit/runtime/graph.json
```

A worker node can unlock dependents only after returning a passed Loop Receipt. Persist that receipt and record completion with `graph-complete`. Missing expected artifacts block completion. A blocked/escalated node must be represented with `graph-block`; do not silently route around it.

Final multi-node success requires:

```bash
python3 ~/code/agentit/router/runtime_cli.py graph-check --state .agentit/runtime/graph.json
```

A final answer claiming multi-node completion without a passed Graph Receipt is a protocol failure.

## Public visual pipeline

A public landing/homepage/company or brand website/portfolio/storefront, especially greenfield or total redesign, is design-primary.

Greenfield/total Studio default graph:

1. deep recommendation-led interview;
2. live reference research, often fan-out by independent lens;
3. **3 genuinely different concepts** in Studio (2 can be enough for Polished uncertainty);
4. Architect judges against brief + research + constraints;
5. write one `DESIGN_DIRECTION` artifact;
6. one final implementation owner consumes that direction;
7. fresh independent design critic;
8. desktop/mobile browser verification.

Research/concept nodes should be read-only. `DESIGN_DIRECTION` is an explicit handoff artifact. Final implementation has one writer owner. Critic is read-only. Each node has its own bounded loop and receipt.

Concepts differ in visual thesis, composition, typography/imagery and narrative/interaction—not palette swaps.

## Skill loading

Use `always_core + task/stage skills`, never the whole catalog. “Smallest useful” does not mean dropping art direction from a public website.

A route/profile/worker containing a skill name is not evidence the skill ran. The model must read/receive the `SKILL.md` body or provider-native loading must provide equivalent evidence. Keep the Skill Load Receipt.

## Worker contract

Every spawn receives objective, scope, role, project/user instructions, actual task-scoped skill bodies, ownership, expected output/evidence, verifier, stop condition and loop state/id. One writer per shared file/state.

Workers return findings/artifacts + Skill Load Receipt when applicable + mandatory Loop Receipt. The Architect validates/records the receipt before marking a graph node completed.

## Critic gate

Use a fresh independent critic for large structural/high-impact plans, architecture/migration decisions where isolation improves review, Studio greenfield public visual work and total visual redesigns.

For visual work the critic checks hierarchy, composition, type, imagery, motion, direction fidelity, generic AI-template signals, cardification/container abuse, repeated section silhouettes, responsive behavior and whether reference research visibly affected the design.

## Stop spawning when

- branches are no longer independent;
- coordination cost exceeds context/expertise benefit;
- multiple workers would need the same write ownership;
- remaining work is a tightly coupled integration decision owned by the Architect.

## Anti-patterns

- forced single-agent because “one model can do it”;
- workers for show;
- parent serially reading a massive corpus without considering isolation;
- skill IDs without bodies;
- execution without Loop Receipt;
- advancing a dependent node without `graph-ready`;
- cycles or overlapping writers hidden in prose orchestration;
- concept competition where every result is the same template;
- skipping fresh critique on flagship/total visual work;
- unbounded correction loops.
