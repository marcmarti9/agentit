---
name: executive-operations
description: Diagnose operational constraints, process/vendor risk, execution capacity and automation opportunities, then turn them into measurable operating decisions.
---

# Executive Operations

Use this skill for process design, operational bottlenecks, vendor dependencies, service delivery, scaling, automation, cross-functional execution and operational metrics.

The default question is not “which tool should we buy?” It is **what is constraining reliable throughput, why, and what change removes that constraint with acceptable risk?**

## Diagnose before prescribing

Map the current operating flow at the level needed to expose:

- demand/input;
- owners and handoffs;
- bottleneck/queue;
- systems/tools involved;
- manual workarounds;
- failure/retry paths;
- vendor dependencies;
- decision/approval delays;
- output/service-level expectation;
- observable metrics.

Classify the primary problem as one or more of:

- process;
- people/capacity;
- tooling/automation;
- policy/decision rights;
- vendor/supply dependency;
- information/measurement.

Do not automate a process whose purpose/ownership is still unclear unless automation is itself the controlled experiment.

## Constraint-first operating rule

Throughput is often dominated by the tightest constraint. Prioritize removing the binding bottleneck before polishing low-impact steps elsewhere.

When a proposed improvement touches several areas, estimate the expected effect on:

- throughput / cycle time;
- error/rework rate;
- cost per unit/order/case;
- customer impact;
- human time reclaimed;
- reliability / failure blast radius;
- working capital or inventory;
- vendor lock-in/switching cost.

## Process before headcount

Before adding people to repeatable work, ask whether the work can be:

- removed;
- standardized;
- simplified;
- batched;
- automated;
- moved to a clearer owner.

Headcount can be the right answer. It should not be the substitute for understanding a broken process.

## Automation decisions

For automation, model:

- frequency and manual time;
- error rate/consequence;
- implementation/setup cost;
- maintenance/exception-handling cost;
- integration/security risk;
- expected utilization;
- payback and opportunity cost;
- observability and rollback/manual fallback.

Automate the stable path and explicitly design the exception path.

## Vendor and dependency risk

For critical vendors/services inspect:

- SLA and actual performance;
- switching/export/migration path;
- data ownership/portability;
- renewal/termination terms;
- concentration/single-source risk;
- support escalation;
- security/compliance boundaries;
- failure fallback and recovery time.

Critical single-source dependencies should have a known switching or degradation plan even when a full second supplier is uneconomic.

## Metrics

Pair lagging outcomes with leading indicators where useful.

Examples:

- revenue/output + qualified pipeline/order volume;
- missed SLA + queue age/capacity utilization;
- churn/refunds + defect/complaint rate;
- cost + process time/rework;
- deployment incidents + change-failure/rollback signal.

A metric that cannot trigger a decision is often dashboard decoration.

## Decision method

1. Define desired operating outcome.
2. Map current flow and binding constraint.
3. Identify root cause, not symptom.
4. Compare process/people/tool/vendor options.
5. Estimate impact, cost, risk and reversibility.
6. Choose the smallest change that meaningfully improves the constraint.
7. Assign owner and operating metric.
8. Define rollback/fallback and review point.

Pair with `executive-finance` for capital/payback, `executive-people` for org/capacity, `executive-legal` for vendor/contract/regulatory risk, and engineering/release packs when actual technical implementation begins.

## Failure modes

Avoid:

- buying software before diagnosing the process;
- optimizing non-bottlenecks;
- adding headcount to tribal/manual chaos;
- automation with no exception/fallback path;
- KPIs with no owner or action threshold;
- critical vendors with no exit knowledge;
- operational plans that ignore change management and real human workload.

## Provenance

Original Agentit guidance materially informed by the operations specialist design and constraint/process heuristics in Sente Labs' OpenExecutive (Apache-2.0). See `THIRD_PARTY_NOTICES.md`.