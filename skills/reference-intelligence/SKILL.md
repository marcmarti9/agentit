---
name: reference-intelligence
description: Use external references as traceable evidence, inspiration, reusable artifacts, or architecture input without confusing those roles. Selects the smallest useful Agentit reference pack, re-verifies dynamic claims when material, extracts durable principles, records provenance in the project, and prevents reference-driven cloning or social-media claims from becoming facts.
---

# Reference Intelligence

External references are useful only when the agent knows **what kind of authority each source actually has** and can explain how it changed the work.

Agentit ships a mechanical reference catalog at `references/catalog.yaml`. The active primary AI chooses sources/packs after understanding the task. `agentit refs` may list, filter, validate, or load an explicitly selected source/pack; it must never infer semantic relevance from free-text task input.

This skill complements `source-driven-development`:

- `source-driven-development` owns authoritative current framework/library/standard documentation for implementation correctness;
- `reference-intelligence` owns broader design inspiration, process ideas, products/tools, architecture patterns, launch examples, research leads, creator claims, and reusable external artifacts.

When both apply, authoritative implementation docs outrank inspiration.

## 1. Classify the role before trusting the source

Every materially used reference has one primary role:

- **canonical** — official docs/spec/canonical repository for the thing being used;
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
- official framework docs can establish an API contract but do not establish that the API is the right product decision.

## 2. Select the smallest useful reference pack

After `TASK_DECISION`, decide whether external reference work materially helps. If yes:

1. inspect `agentit refs packs` or the catalog metadata;
2. choose one explicit named pack or a small set of explicit source IDs;
3. load only those entries;
4. fetch/re-verify the underlying live/canonical sources when the decision is time-sensitive, risky, dependency-forming, or the catalog marks evidence as a creator claim/partial verification;
5. stop when the reference set is sufficient to make the decision.

Do not dump every bookmark or gallery into context. Reference overload is another form of context pollution.

Typical packs include:

- `engineering-discipline`;
- `web-design-studio`;
- `growth-seo`;
- `launch-content`;
- `build-vs-buy`;
- `ai-systems-learning`;
- `agency-economics`.

Packs are starting points, not mandatory bundles.

## 3. Extract principles, not vibes

For each selected source, produce a compact internal extraction:

```text
REFERENCE EXTRACTION
source: <id + URL>
role: canonical | licensed artifact | corroborated | creator claim | inspiration | unverified
what is observable: <facts directly supported>
principle worth keeping: <portable idea>
project consequence: <specific decision/change, or none>
what NOT to infer: <unsupported claim / cloning boundary / stale assumption>
```

A reference that produces no project consequence should usually remain a catalog entry, not project documentation.

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

## 4. Build-vs-buy / adopt-vs-adapt gate

When a reference exposes a tool, package, skill, MCP, component library, or codebase that might become a dependency, apply the search-first decision used by `source-driven-development`:

- **ADOPT** — maintained exact fit, acceptable license/security/dependency cost;
- **ADAPT** — useful licensed base, but Agentit/project needs a deliberate local variant;
- **COMPOSE** — combine smaller existing pieces;
- **REFERENCE ONLY** — the idea is useful but the artifact should not enter the runtime;
- **INCUBATE** — promising but missing evidence/license/config/fit;
- **REJECT** — cost/risk/overlap exceeds value;
- **BUILD** — nothing suitable remains after search.

Never globally install a second process owner merely because it is popular. Agentit prefers strengthening an existing skill over creating overlapping instructions that can disagree silently.

## 5. Evidence/freshness gate

Re-verify before material reliance when any of these are true:

- the source describes a current API, product, MCP endpoint, price, free tier, model, regulation, browser support, or platform behavior;
- the catalog marks `creator_claim`, `unverified`, `partially_verified`, or equivalent;
- a dependency/security/license decision will be made;
- the source's factual claim is important to business/revenue/product strategy;
- the source is old enough that change is plausible.

Prefer canonical current sources for implementation/configuration. Preserve creator claims as claims even when they come from the vendor itself.

Do not turn a viral price/revenue/hiring anecdote into a benchmark without independent evidence.

## 6. Project provenance ledger

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

When a code/skill artifact is substantially adapted, also preserve the license/attribution in the project's appropriate third-party notice/license location.

## 7. Reference-aware planning

For substantial work, `TASK_DECISION` should include a compact `reference_plan` when references matter:

```text
reference_plan:
  needed: yes
  pack_or_sources: [web-design-studio]
  purpose: art direction + implementable component discovery + UX QA
  authority_needed: inspiration + canonical component/tool docs
  freshness_check: current MCP/package setup before adding dependency
  provenance_output: docs/agentit/REFERENCES.md
```

The cheap auditor should challenge:

- a creator claim being treated as fact;
- stale/unverified setup instructions;
- unnecessary reference overload;
- a dependency adopted without license/maintenance/security review;
- design cloning instead of synthesis;
- a material external influence missing from durable project provenance.

## 8. Reference-first design workflow

For serious public visual work, combine this skill with the design profile:

`brief/existing truth -> reference study -> design DNA -> original design thesis -> component/tool discovery -> implementation -> anti-slop/UX audit -> desktop/mobile browser verification`

Useful reference types are intentionally different:

- gallery/site examples for composition and visual language;
- real component catalogs for implementable primitives;
- UX checklists for flow-specific failure modes;
- official browser/framework docs for correctness;
- rendered project evidence for the final acceptance claim.

Do not confuse any one of these with the others.

## 9. Reference-first launch/content workflow

For material launches/content campaigns:

`comparable launch research -> positioning/hook patterns -> factual brief -> asset/scene plan -> production -> human claim/rights/brand review -> distribution -> analytics -> later evaluation -> learnings`

A product URL is context, not a complete creative brief. A viral launch is a reference, not proof that copying its wording will reproduce its results.

## 10. Closed-loop marketing/reference learning

When a marketing/SEO reference inspires automation, make the loop explicit:

`observe real data -> diagnose -> propose/execute within permissions -> define metric -> schedule review -> evaluate -> update compact learnings -> retry/stop/escalate`

Self-improvement means improving stored procedure/context/strategy from evidence. It never means silently loosening safety, approval, budget, factuality, or verification boundaries.

## Completion checks

Before claiming substantial reference-driven work complete:

- [ ] The selected sources/packs were explicit, not programmatically inferred from task text.
- [ ] Every material source has the correct authority/evidence role.
- [ ] Dynamic or high-impact claims were re-verified where needed.
- [ ] Reused code/skills/components received license/dependency/security review.
- [ ] Design work synthesizes patterns rather than cloning protected expression/assets.
- [ ] Unsupported creator claims did not become project facts.
- [ ] The project reference ledger records every durable external influence that matters.
- [ ] The implementation is still verified against its own acceptance criteria; references are not proof that the result works.
