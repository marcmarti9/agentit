---
name: architect-orchestrator
description: Intelligent orchestration after interview. Domain packs, skill budgets, specialist spawn without hard caps, mandatory critic for large plans. No powerwords.
---

# Adaptive Agent Architecture

## Core rule

Agentit is **interview-first for product work** and **intelligent about delegation**.

A capable main agent (Architect) owns the user relationship, decomposition, integration, and final answer. Multi-agent is used when it improves outcomes — not by ceremony, not forbidden by dogma.

No powerwords. Ordinary task language is enough. Only natural Agentit activation is special-cased.

Before topology:

1. mechanical vs product-affecting;
2. product work → `interview-me`;
3. domain pack from router/profiles (not universal Studio);
4. craft depth only if design/visual;
5. project-aware token estimate from router.

## Axes (not one effort dial)

| Axis | Meaning |
|---|---|
| Domain pack | Which skill family + MCP stack |
| Craft depth | standard/polished/studio — **design only** |
| Spend | lean/normal/thorough — soft main-agent rigor |
| Delegation | advisory recommended specialists; **no hard caps** |

## Skill loading

```
always_core (tiny) + skill_budget.load_now (≤3–4 bodies)
never full catalog into parent or worker
```

If the user assigns a role, load that domain only (+ core). Gaps → `find-skills` / marketplace.

## MCP

Run `mcp-tooling-fit` when tools matter: inventory, fit, disable noise, discover catalog/marketplace/web, plan install with user OK.

## Topologies

1. **Direct** — coupled single-thread work
2. **Plan + direct** — broad but sequential
3. **Probe** — read-only investigation
4. **Fan-out** — independent packages/files/domains
5. **Pipeline** — ordered stages (e.g. research → implement)
6. **Writer + reviewers** — one writer, independent review
7. **Design competition** — multiple concepts (usually studio craft)
8. **Orchestrated DAG** — multi-package dependencies
9. **Audit** — high-risk independent review

Router JSON fields: `topology`, `subagents`, `parallelism`, `critic_required`, `domain_pack`, `skill_budget`, `token_estimate`.

## Delegation test

Spawn when at least one is true:

- real independence / parallel speedup;
- context isolation for large research/logs;
- distinct expertise or tools;
- creative diversity;
- independent risk reduction or **critique**.

If none, stay single-agent. If the user demands multi-agent without benefit, explain and recommend not spawning.

## Critic gate (mandatory)

For large structural plans, architecture proposals, multi-module migrations, or high-impact sensitive implementation:

1. Architect drafts the plan/artifact;
2. **Independent critic subagent** (fresh context, read-only) challenges assumptions, coupling, missing risks, simpler alternatives;
3. Architect integrates critique before implementation commitment.

Do not self-grade as a substitute when isolation is available.

## Budgets

- **No hard min/max** subagent counts.
- `subagents.recommended` is guidance from the router.
- One writer per file/shared state; parallel writers need worktrees/branches.
- Default child depth: one generation.

## Provider-neutral execution

1. native subagent/worker
2. isolated delegated model call
3. fresh-context invocation
4. parent + same skill bundle

Multi-agent is never a correctness dependency.

## Worker Context Contract

Every spawn: objective, domain pack, effort/craft if any, projected project instructions, task skills only, risk, I/O ownership, output, verification, stop condition.

Precedence: `safety > user > project > preferences > defaults`.

## Verification

Correctness floor is independent of craft depth. RISK_3/4: fuller tests + independent review. Visual craft depth controls how deep UI QA goes.

## Anti-patterns

- Studio/Polished for non-design tasks
- fixed token bills
- powerwords
- loading full skill catalogs
- forced multi-agent or forced single-agent
- skipping critic on large structural plans
- multiple writers on shared state
- unbounded correction loops
