---
name: design-system-engineering
description: Build, assess, or evolve the implemented tokens, components, patterns, migration path, and governance of a design system. Use for real design-system drift and reuse; do not use for a remembered design direction, a single component, or brand identity creation.
license: Apache-2.0
---

# Design System Engineering

Create an operating system for recurring interface decisions that exists in the actual design and
code surfaces. This skill owns foundations, component contracts, migration, and governance. A
`DESIGN.md`, moodboard, or remembered convention is evidence to inspect, not proof of a system.

## Use when

- Repeated UI patterns have diverged across product surfaces or repositories.
- Tokens, components, documentation, and implemented behaviour need reconciliation.
- A team needs an incremental path from ad-hoc UI to a maintained system.

## Do not use when

- The request is a one-off page, a single local component, or cosmetic polishing with no reuse
  decision; use the page or frontend owner.
- The request establishes marks, imagery, or brand positioning; use `brand-identity-design`.
- A design file alone is being reorganised without implementation or operating-model scope.
- Data quality, computation, or analytical definitions are at issue; those remain with the data
  owner even when the output uses system components.

## Inputs and boundary

Inspect the deployed or source implementation, design libraries, existing tokens, component usage,
accessibility requirements, consumers, release constraints, and maintenance owners. Do not replace
an established client control surface or install a new CMS/tool merely to make a system editable.
Distinguish documented intent, design-library state, code state, and observed production state.

## Procedure

1. Build an inventory from real surfaces. Group duplicate components by behaviour and usage, not
   by file names. Record source locations, consumers, variants, states, and observed drift.
2. Define the smallest foundation set that resolves current inconsistency: primitives where useful,
   semantic tokens for meaningful roles, and contextual aliases only when they prevent repetition.
   Give every token an owner, meaning, and implementation location; avoid speculative token growth.
3. Set component contracts from actual need: anatomy, variants, states, responsive behaviour,
   keyboard and assistive behaviour, content limits, and unsupported uses. Components consume
   semantic decisions rather than arbitrary raw values where that improves safe change.
4. Reconcile design and code. For every priority item, state whether design, code, documentation,
   and deployed surface agree. Do not claim parity based on a file name or visual memory.
5. Choose migration slices by user impact and dependency order. Supply compatibility or deprecation
   guidance, a rollback path, and concrete adoption checks. Avoid a destructive broad replacement.
6. Establish proportionate governance: responsible owner, proposal/review route, versioning policy
   for breaking changes, documentation update point, and a way to surface drift. Governance should
   enable ordinary client changes safely without exposing privileged infrastructure controls.
7. Verify priority components in their target context: states, content extremes, responsiveness,
   accessibility, visual regression risk, and consumer adoption. Record commands/renders used and
   gaps that remain.

## Decision rules

| Condition | Decision | Evidence |
|---|---|---|
| Same behaviour, several implementations | Consolidate after comparing consumers | Usage inventory and migration test |
| Different semantic purpose, similar appearance | Keep distinct semantic contracts | Documented purpose and states |
| A breaking API or token change | Plan version/deprecation and rollback | Consumer map and adoption gate |
| Design/code disagree | Treat as drift until reconciled | Direct inspection of both surfaces |
| No owner can maintain an abstraction | Do not promote it as a system dependency | Named ownership gap |

## Evidence and degradation

An audit may be read-only. Implementation, migrations, publication, and dependency changes need
their own authorization. When a design library, runtime, render environment, or consumer access is
unavailable, deliver an evidence-bound gap list and migration proposal; do not assert component
parity, accessibility, release readiness, or adoption.

## Handoff

Publish the system decision record where its actual consumers can find it, with source locations,
owners, compatibility window, migration sequence, and verification commands or renders. Keep
product content and business configuration in their existing client-approved control surfaces;
system governance documents must not become a shadow administration interface.

## Common failures

- Declaring a token system from a style sheet without checking component consumers.
- Naming every visual difference a variant rather than clarifying semantic purpose.
- Replacing a widespread component before mapping its states and dependencies.
- Treating Figma/design documentation as proof of code or deployed parity.

## Completion record

Record the source snapshot, priority component list, accepted token semantics, consumer migration
state, named owners, and the next review trigger. This creates an auditable maintenance boundary
without pretending that documentation alone has completed adoption.

Review the record again after a consumer migration or a meaningful platform change. Observed drift
is a maintenance signal, not a reason to silently fork the system in a local feature.

## Acceptance

- The inventory separates actual implementation from documentation and memory.
- Priority tokens and components have purpose, owner, state behaviour, and consumer evidence.
- Migration and governance make normal changes possible without undocumented manual intervention.
- Verification names tested contexts, residual drift, and rollout gates.
