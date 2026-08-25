# Project reference ledger

This file records **durable external influences** on architecture, product behavior, design, process, or dependency selection. It is not browsing history.

Use the project's existing equivalent instead if one already exists. Do not duplicate sources of truth.

## How to record a reference

For each material influence, record the source's actual authority and the concrete project consequence.

| Source / Agentit reference ID | Role | Extracted principle | Project decision | Affected paths | Verified |
| --- | --- | --- | --- | --- | --- |
| _example: `monokern-21st-dev`_ | _canonical/tool candidate_ | _Search real component candidates before inventing commodity UI_ | _Evaluate project primitives, then 21st candidates; adapt selected code to our tokens/a11y_ | _`src/components/**`_ | _YYYY-MM-DD_ |

## Authority vocabulary

- `canonical` — official documentation/spec/canonical repository for the thing being used.
- `licensed artifact` — inspectable reusable code/skill with reviewed license.
- `corroborated` — factual claim independently supported.
- `creator claim` — creator/vendor says it; preserve it as a claim unless independently corroborated.
- `inspiration` — useful pattern/taste/idea, not factual authority.
- `unverified` — lead only; do not make it a project premise.

## Boundaries and attribution

Record, when applicable:

- what was intentionally **not** copied or inferred from a reference;
- license/attribution obligations for adapted artifacts;
- dependency/security/maintenance review performed before adoption;
- which dynamic assumption requires later re-verification;
- factual/business claims that remained unverified and therefore were not used as premises.

## Reference-driven decisions

Add compact subsections below when a decision needs more context than the table can carry.

### <decision / feature / design direction>

**Sources:** <ids/URLs>

**What was observable:** <facts/signals actually supported>

**Principle extracted:** <portable idea>

**Decision in this project:** <specific choice>

**Rejected inference / anti-copy boundary:** <what the project deliberately did not copy or assume>

**Revisit when:** <freshness, product, performance, licensing, or evidence trigger>
