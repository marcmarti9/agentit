---
name: specialist-agent-routing
description: Select and spawn bounded specialist subagents from Agentit's agent catalog when specialization, independent exploration, context isolation, or review materially improves the result.
---

# Specialist Agent Routing

Agentit may create temporary specialists for a task. Specialists are not a permanent team and are not spawned just because a matching job title exists.

## Source of truth

Read `agents/catalog.yaml` when a task contains a strong domain signal or when the parent agent is considering delegation. Match the task against specialist `triggers`, then project only the listed `skills` plus the exact task context required.

## Spawn decision

Create a specialist only when at least one is true:

- the task needs expertise that is meaningfully distinct from the parent agent's current context;
- an independent proposal/review has real value;
- a research branch can run without touching shared mutable state;
- the specialist can use different tools or a different model efficiently;
- context isolation prevents a large research/design/diagnostic branch from polluting implementation context;
- parallel alternatives are intentionally desired.

Do not spawn for a small, tightly coupled change that the parent can complete directly.

## Specialist contract

Every specialist receives:

1. a single role id from `agents/catalog.yaml`;
2. exact objective and scope;
3. only the specialist's relevant skills;
4. allowed inputs and write ownership;
5. expected output schema from the catalog;
6. risk and safety constraints;
7. verification or evidence requirements;
8. stop/escalation condition.

Use the Worker Context Contract (`agentit worker build|render`) for the actual delegated package. Map catalog `mode` to runtime role: `implementer`, `reviewer`, or `probe`.

## Parent responsibilities

The parent/Architect owns decomposition, chooses the specialist, decides whether to accept its result, resolves conflicts between specialists, integrates changes, and performs final verification. Worker claims are not evidence by themselves.

## Design competition

For explicitly ambitious creative work, a special fan-out is allowed:

- one shared research brief;
- 2-3 independent concept specialists, preferably with different models or deliberate creative constraints;
- each returns a concept, visual thesis, interaction model, technical feasibility notes, and risks;
- a design critic / creative director evaluates them against the same criteria;
- select one winner or a clearly justified hybrid before implementation.

Do not run design competition for routine UI maintenance. Diversity is useful only when concept choice is a major part of the value.

## Model selection

Model choice is capability-based, not status-based. Use stronger reasoning/judgment models for architecture, creative direction, arbitration, and difficult reviews. Use cheaper/faster models for bounded implementation, research extraction, variant generation, browser loops, and repetitive QA when quality remains acceptable.

## Anti-patterns

- one subagent per file or conventional job title;
- permanent fake-company org charts;
- more than 2-3 specialists without a real DAG;
- multiple writers touching the same files;
- asking five agents the same question and majority-voting without criteria;
- delegating integration or final responsibility away from the parent;
- loading the full skill catalog into every worker;
- spawning a specialist when a skill alone would suffice.
