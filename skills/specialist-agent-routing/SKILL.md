---
name: specialist-agent-routing
description: Select and spawn domain specialists with scoped skills. Intelligent spawn, no hard caps, critic for large plans, natural language only.
---

# Specialist Agent Routing

Specialists are temporary domain experts, not a permanent org chart. Spawn when they improve the result; never by ceremony and never because a job title exists.

## Source of truth

Read `agents/catalog.yaml`. Match triggers and domain. Project only listed skills + task context via Worker Context Contract.

## Spawn decision

Create a specialist when at least one is true:

- distinct expertise vs current parent context;
- independent proposal or review (including **critic**);
- research branch without shared mutable state;
- different tools/model efficiency;
- context isolation for large research/design/diagnostics;
- real parallel independent packages.

Do **not** require powerwords. Ordinary language (“frontend and backend”, two file paths, “at the same time”, “several agents”) is enough. If the user asks for agents without independence, push back.

## No hard caps

There is no mandatory min/max specialist count. Use router `subagents.recommended` as soft guidance. Stop when ownership or integration cost exceeds benefit.

## Critic specialists

For large structural plans / architecture / high-impact proposals, spawn a read-only critic (design-critic, code-review, or auditor-class role) **before** committing to implementation. Fresh context; no shared rationalization thread.

## Specialist contract

1. role id from catalog (or ad-hoc domain name if catalog lacks a fit);
2. objective and scope;
3. only that specialist’s skills;
4. allowed I/O and write ownership;
5. output contract;
6. risk/safety;
7. verification;
8. stop/escalation.

Use `agentit worker build|render`. Modes: implementer, reviewer, probe.

## Parent responsibilities

Architect owns decomposition, acceptance, conflict resolution, integration, final verification, and the user-facing answer. Worker claims are not evidence.

## Missing skills

If the domain is missing:

1. check local skills / profiles;
2. `find-skills` / skills.sh marketplace;
3. propose install;
4. only then load.

## Design competition

Usually for studio-level visual craft: 2–3 independent concepts → explicit jury → implement → critique. Not for routine UI maintenance.

## Anti-patterns

- one subagent per job title;
- hard quotas for show;
- multiple writers on the same files;
- dumping the full skill catalog into workers;
- spawning when a single skill in the parent would suffice;
- skipping critic on large structural plans.
