---
name: reference-intelligence
description: Decide whether a task materially benefits from external references, then use the smallest domain-appropriate set as traceable evidence, inspiration, reusable artifacts, or architecture input without confusing those roles. Uses Agentit packs when they fit, discovers current canonical sources when they do not, re-verifies dynamic claims, records provenance, and prevents reference-driven cloning or unsupported claims.
---

# Reference Intelligence

External references are useful only when the agent knows **when they matter, what authority each source actually has, and how the source changed the work**.

The key rule is:

> **Always evaluate whether references are needed; do not always load references.**

A tiny local refactor, rename, formatting change, or self-contained bug may need no external references. A public website, fiscal/legal report, current framework integration, SEO plan, security-sensitive implementation, market comparison, launch strategy, or unfamiliar domain usually does.

The user must **not** need to paste the references again in the task prompt when Agentit already has a relevant pack/source or can discover the required current canonical sources.

Agentit ships a mechanical reference catalog at `references/catalog.yaml`. The active primary AI chooses sources/packs after understanding the task. `agentit refs` may list, filter, validate, or load an explicitly selected source/pack; it must never infer semantic relevance from free-text task input.

The catalog is a **curated accelerator, not a closed universe**. If no Agentit pack covers the domain, the primary AI must discover the appropriate live/canonical sources when references are materially required.

This skill complements `source-driven-development`:

- `source-driven-development` owns authoritative current framework/library/standard documentation for implementation correctness;
- `reference-intelligence` owns the broader decision of what external knowledge the task needs: design inspiration, official domain sources, regulations, process ideas, products/tools, architecture patterns, launch examples, research leads, creator claims, reusable artifacts, and comparable evidence.

When both apply, authoritative implementation/domain sources outrank inspiration.

## 1. Mandatory reference decision gate

For every **material** task, `TASK_DECISION` must explicitly resolve one of these states:

```text
reference_plan:
  mode: none | catalog | live | mixed
  reason: <why references are or are not useful>
```

Use `mode: none` only when external knowledge would not materially improve correctness, freshness, design quality, decision quality, or verification.

Examples:

### No references needed

```text
Task: rename a private helper and update its local tests
reference_plan:
  mode: none
  reason: repository-local behavior is sufficient; no external contract changed
```

### Web/design task

```text
Task: design and implement a high-quality public landing page
reference_plan:
  mode: mixed
  pack_or_sources: [web-design-studio]
  live_sources: current framework/component docs as needed
  purpose: design DNA + component discovery + UX QA + implementation correctness
```

### Fiscal/legal/current-domain task

```text
Task: prepare a Spanish corporate-tax report
reference_plan:
  mode: live
  domain: Spanish corporate taxation
  authority_needed: primary/canonical legal and tax sources
  likely_sources: current legislation + Agencia Tributaria + other official guidance where relevant
  reason: correctness depends on current jurisdiction-specific rules; no generic Agentit pack is enough
```

### Current framework/API task

```text
Task: implement auth using the project's current framework version
reference_plan:
  mode: live
  authority_needed: current official framework/provider docs
  reason: API and recommended patterns may have changed
```

An auditor must challenge `mode: none` when the task materially depends on current, jurisdiction-specific, external, unfamiliar, comparative, visual, regulatory, security, financial, or ecosystem knowledge.

## 2. Select the smallest domain-appropriate reference set

After `TASK_DECISION`:

### If a curated Agentit pack fits

1. inspect `agentit refs packs` or catalog metadata;
2. choose one explicit named pack or a small set of explicit source IDs;
3. load only those entries;
4. re-fetch/re-verify current underlying sources where freshness matters;
5. stop when the reference set is sufficient.

Typical packs include:

- `engineering-discipline`;
- `web-design-studio`;
- `growth-seo`;
- `launch-content`;
- `build-vs-buy`;
- `ai-systems-learning`;
- `agency-economics`.

### If no curated pack fits

Do **not** fall back to model memory merely because the catalog lacks that domain.

The primary AI should discover live sources using the authority hierarchy appropriate to the domain. Examples:

- fiscal/tax -> current legislation, tax authority, official administrative guidance;
- legal/compliance -> statute/regulator/official guidance first;
- medicine/health -> authoritative clinical/public-health sources appropriate to the question;
- standards -> current specification/standards body;
- framework/library/API -> current official docs/changelog;
- security -> primary vendor/advisory/CVE/standard sources;
- finance/economics -> primary data issuer/regulator/official statistics where possible;
- product/market comparison -> vendor docs + independent evidence where claims matter;
- design -> current real references + canonical implementation docs;
- travel/local -> current official/local/business sources as appropriate.

The AI chooses the source family semantically. Programs may execute search/fetch after that decision, but may not infer the domain from prompt keywords.

Do not dump an entire field into context. **Progressive disclosure applies to references too.**

## 3. Classify the role before trusting the source

Every materially used reference has one primary role:

- **canonical** — official docs/spec/legislation/regulator/canonical repository for the thing being used;
- **licensed artifact** — inspectable reusable code/skill/design artifact with a reviewed license;
- **corroborated evidence** — a material factual claim supported independently;
- **creator claim** — the creator/vendor/post author says it; useful as a lead, not independent proof;
- **inspiration** — used for patterns/taste/ideas, not factual authority;
- **unverified lead** — insufficient evidence; never convert it into a factual premise.

A source can be excellent inspiration and terrible evidence at the same time.

Examples:

- a beautiful landing page can inspire composition without proving its conversion rate;
- a founder thread can expose a useful automation architecture without proving the revenue screenshot;
- an MIT-licensed skill can be adapted with attribution after inspecting the actual repository;
- official framework docs can establish an API contract but do not establish that the API is the right product decision;
- an official tax authority can be authoritative about administrative guidance while the underlying statute still matters for the legal rule itself.

## 4. Actually load/use the references before execution

A selected reference ID or pack name inside `TASK_DECISION` is **not evidence of use**.

When `reference_plan.mode != none`, before implementation or final analysis the responsible model must actually:

1. load/fetch the selected references;
2. inspect the material portions;
3. classify authority;
4. extract the relevant principles/facts;
5. use them in the decision or explicitly conclude that they did not change it.

If the source is unavailable, stale, inaccessible, or insufficient, either replace it with a suitable source or record the gap. Do not silently continue as though it had been read.

This is the same principle Agentit applies to skills: **an ID is discovery metadata, not activation**.

## 5. Extract principles, not vibes

For each selected source, produce a compact internal extraction:

```text
REFERENCE EXTRACTION
source: <id + URL>
role: canonical | licensed artifact | corroborated | creator claim | inspiration | unverified
what is observable: <facts directly supported>
principle/fact worth keeping: <portable idea or authoritative fact>
project consequence: <specific decision/change, or none>
what NOT to infer: <unsupported claim / cloning boundary / stale assumption>
```

A reference that produces no durable project consequence should usually remain out of permanent project documentation.

For design references, separate the DNA into dimensions such as:

- macrostructure / section rhythm;
- hierarchy / composition;
- typography roles;
- color/material system;
- component archetypes;
- imagery/artifact strategy;
- interaction/motion role;
- responsive behavior;
- accessibility/performance constraints.

Synthesize multiple signals into an original project thesis. Never copy pixels, proprietary assets, logos, copy, or a distinctive page wholesale merely because it was supplied as a reference.

## 6. Build-vs-buy / adopt-vs-adapt gate

When a reference exposes a tool, package, skill, MCP, component library, or codebase that might become a dependency, apply the search-first decision used by `source-driven-development`:

- **ADOPT** — maintained exact fit, acceptable license/security/dependency cost;
- **ADAPT** — useful licensed base, but Agentit/project needs a deliberate local variant;
- **COMPOSE** — combine smaller existing pieces;
- **REFERENCE ONLY** — the idea is useful but the artifact should not enter the runtime;
- **INCUBATE** — promising but missing evidence/license/config/fit;
- **REJECT** — cost/risk/overlap exceeds value;
- **BUILD** — nothing suitable remains after search.

Never globally install a second process owner merely because it is popular. Agentit prefers strengthening an existing skill over creating overlapping instructions that can disagree silently.

## 7. Evidence/freshness gate

Re-verify before material reliance when any of these are true:

- the source describes a current API, product, MCP endpoint, price, free tier, model, regulation, browser support, platform behavior, tax rule, policy, rate, deadline, or legal requirement;
- the catalog marks `creator_claim`, `unverified`, `partially_verified`, or equivalent;
- a dependency/security/license decision will be made;
- the source's factual claim is important to business/revenue/product strategy;
- the source is old enough that change is plausible.

Prefer current primary/canonical sources for correctness-sensitive claims. Preserve creator claims as claims even when they come from the vendor itself.

Do not turn a viral price/revenue/hiring anecdote into a benchmark without independent evidence.

## 8. Project provenance ledger

If external references **materially influence** architecture, product behavior, visual direction, process, dependency selection, or a durable business/technical decision, ensure the project has a canonical reference ledger.

Reuse an existing equivalent if present. Otherwise use:

`docs/agentit/REFERENCES.md`

Recommended structure:

```markdown
# Project reference ledger

## <decision / feature / design direction>

| Source | Role | Extracted principle | Project decision | Affected paths | Verified |
| --- | --- | --- | --- | --- | --- |
| <URL or Agentit source id> | inspiration | ... | ... | ... | YYYY-MM-DD |

### Boundaries
- What was intentionally not copied/inferred.
- License/attribution requirements when an artifact was adapted.
- Re-verification trigger for dynamic assumptions.
```

The ledger is not a browser-history dump. Record only references that affected a durable decision.

For one-off analytical answers/reports that do not mutate a repository, normal inline citations/source notes may be the correct provenance output instead of creating project files.

When a code/skill artifact is substantially adapted, also preserve the license/attribution in the project's appropriate third-party notice/license location.

## 9. Reference-aware planning

For material work, `TASK_DECISION` carries the explicit decision even when the answer is `none`:

```text
reference_plan:
  mode: none | catalog | live | mixed
  reason: ...
  pack_or_sources: [...]        # when catalog/mixed
  domain: ...                   # when live/mixed and useful
  purpose: ...
  authority_needed: ...
  freshness_check: ...
  provenance_output: ...
```

The cheap auditor should challenge:

- `mode: none` despite material dependence on external/current/domain-specific knowledge;
- a creator claim being treated as fact;
- stale/unverified setup instructions;
- unnecessary reference overload;
- failure to actually load a selected pack/source;
- a dependency adopted without license/maintenance/security review;
- design cloning instead of synthesis;
- a material external influence missing from durable project provenance.

## 10. Reference-first design workflow

For serious public visual work, combine this skill with the design profile:

`brief/existing truth -> reference study -> design DNA -> original design thesis -> component/tool discovery -> implementation -> anti-slop/UX audit -> desktop/mobile browser verification`

Useful reference types are intentionally different:

- gallery/site examples for composition and visual language;
- real component catalogs for implementable primitives;
- UX checklists for flow-specific failure modes;
- official browser/framework docs for correctness;
- rendered project evidence for the final acceptance claim.

Do not confuse any one of these with the others.

## 11. Reference-first launch/content workflow

For material launches/content campaigns:

`comparable launch research -> positioning/hook patterns -> factual brief -> asset/scene plan -> production -> human claim/rights/brand review -> distribution -> analytics -> later evaluation -> learnings`

A product URL is context, not a complete creative brief. A viral launch is a reference, not proof that copying its wording will reproduce its results.

## 12. Closed-loop marketing/reference learning

When a marketing/SEO reference inspires automation, make the loop explicit:

`observe real data -> diagnose -> propose/execute within permissions -> define metric -> schedule review -> evaluate -> update compact learnings -> retry/stop/escalate`

Self-improvement means improving stored procedure/context/strategy from evidence. It never means silently loosening safety, approval, budget, factuality, or verification boundaries.

## Completion checks

Before claiming material work complete:

- [ ] `reference_plan` was explicitly resolved to `none`, `catalog`, `live`, or `mixed`.
- [ ] `none` has a defensible reason; it was not chosen merely to save effort.
- [ ] When references were required, the selected sources were actually loaded/inspected before the relevant decision/output.
- [ ] When no Agentit pack fit, current domain-appropriate sources were discovered instead of relying on memory.
- [ ] Every material source has the correct authority/evidence role.
- [ ] Dynamic or high-impact claims were re-verified where needed.
- [ ] Reused code/skills/components received license/dependency/security review.
- [ ] Design work synthesizes patterns rather than cloning protected expression/assets.
- [ ] Unsupported creator claims did not become project facts.
- [ ] The project reference ledger or answer citations record every durable/material external influence that matters.
- [ ] The implementation/output is still verified against its own acceptance criteria; references are not proof that the result works.
