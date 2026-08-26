---
name: reference-intelligence
description: Decide whether a task materially benefits from external references, then use the smallest domain-appropriate curated/live set. Distinguish authority, actually read material sources, distill useful knowledge into existing skills, and record durable provenance without making the user re-paste references.
---

# Reference Intelligence

The purpose of this skill is simple:

> **Always decide whether references would materially improve the task; do not always load references.**

The primary AI owns that judgment. Agentit must not recreate it with keyword classifiers, scoring code, or a bespoke reference router.

## 1. Decide the reference mode

For every material `TASK_DECISION`, choose one:

```text
references:
  mode: none | curated | live | both
  why: <short reason>
  curated: <relevant Agentit index/playbook entries, if any>
  authority_needed: <canonical / licensed artifact / corroborated / inspiration / mixed>
  provenance: <whether a durable project reference record is useful>
```

### `none`

Correct when outside material knowledge would not change the result.

Examples:

- rename a local private function;
- formatting/cleanup;
- self-contained bug fully explained by repository evidence;
- small mechanical edit.

Do not research for ceremony.

### `curated`

Use when Agentit already contains a useful recurring playbook/reference. Start at `references/INDEX.md`, then read the linked domain skill/reference file that matters.

Examples:

- premium public website -> design reference index + `premium-web-production.md`;
- substantial marketing work -> `marketing-operating-system.md`.

### `live`

Use when the answer depends on current or domain-specific authority not pre-curated in Agentit.

Examples:

- Spanish fiscal report -> current legislation / tax authority / authoritative fiscal sources;
- current framework/API integration -> current official docs;
- current legal/security/platform requirements -> current authoritative sources.

Agentit does **not** need a prebuilt pack for every possible human domain. The model can research the correct sources when the task requires them.

### `both`

Use when a curated procedure improves how to work while live sources establish current facts.

Example:

```text
SEO task
curated -> how to structure the audit/feedback loop
live -> Search Console data, current SERP/platform guidance, current site evidence
```

## 2. Prefer underlying material over the social post

A bookmark often points to the real asset:

- article/thread;
- repository;
- course;
- prompt collection;
- launch library;
- component catalog;
- official product docs.

When the underlying material contains substantially more useful knowledge, **read it**. Do not stop at the tweet summary.

Then decide where the durable knowledge belongs:

```text
one-off fact -> use/cite in current task
recurring procedure -> existing skill or its references/*.md
reusable licensed artifact -> evaluate adopt/adapt/compose
reference library/tool -> index as a discovery source
current domain truth -> research live when needed
hype / unrelated curiosity -> do not promote into Agentit core
```

This is why the bookmarked premium-web articles and large marketing prompt corpus are distilled inside the relevant design/marketing skills rather than existing only as URLs in a catalog.

## 3. Distinguish source roles

A source's role determines what can be inferred from it.

- **canonical** — official docs/specification/source of truth for the thing being used;
- **licensed artifact** — reusable code/skill/assets whose license has been inspected;
- **corroborated evidence** — factual claim supported independently;
- **creator/vendor claim** — useful lead but not independent proof;
- **inspiration** — pattern/taste/process input, not factual authority;
- **internal evidence** — project/client data that establishes what happened in this system.

Examples:

- a beautiful site can influence composition but does not prove conversion;
- a vendor article can reveal a useful agent architecture but its ROAS claim remains a vendor claim;
- an MIT skill can be selectively adapted with attribution;
- current official tax guidance can establish a fiscal rule, while a design bookmark obviously cannot.

## 4. Distill, do not hoard

The valuable Agentit unit is normally **a capability/procedure**, not the original prompt wording.

When a source contains many prompts/examples:

1. identify recurring jobs;
2. group near-duplicates;
3. extract required inputs;
4. extract useful intermediate artifacts/decisions;
5. extract QA/evidence expectations;
6. turn genuinely reusable gaps into the existing domain skill/reference;
7. preserve source provenance;
8. discard redundant wording and hype.

Do not put 500 prompts into every marketing context. Teach the agent the marketing operating system behind them.

Likewise, a “$10k website” article should become a production playbook, not the instruction “make this look expensive”.

## 5. Curated index is intentionally small

`references/INDEX.md` is an agent-readable discovery map. It is not a database and has no custom Python runtime.

Keep something there only when it is broadly useful enough to accelerate future tasks.

Do **not** globally carry interesting-but-specialized bookmarks merely because they exist. If a future task specifically concerns an omitted topic, research it live then.

Default preference:

> enrich an existing skill with a deep `references/*.md` file instead of creating another top-level system.

## 6. References must actually affect the work

A reference is not “used” because its name appears in a plan.

For each material reference, the working agent should be able to state compactly:

```text
source:
role:
what I actually learned/observed:
what decision it changed:
what I deliberately did not infer/copy:
```

If it changed nothing, it normally does not belong in project provenance.

## 7. Durable project provenance

When external knowledge materially changes architecture, product behavior, visual direction, process, dependency selection, or another expensive-to-rediscover decision, update the project's existing canonical reference/decision documentation.

If there is no equivalent, `docs/agentit/REFERENCES.md` is the default lightweight ledger.

Record:

```text
source -> role -> extracted principle/evidence -> project decision -> affected area -> verified date
```

Do not turn the ledger into browsing history, a transcript, or chain-of-thought.

For reused code/skills/assets, preserve required license/attribution in the appropriate project notice as well.

## 8. Verification uses Agentit's existing runtime

Reference Intelligence does **not** need a second bespoke Python verifier.

When references are material to acceptance, bind the evidence into the existing Loop/Graph contract and verifier, for example:

```text
goal:
  implement the approved public landing-page direction

verifier includes:
  - required current docs were inspected where implementation depends on them
  - premium-web reference playbook/design research was actually used
  - rendered desktop/mobile result passes project checks
  - material external influences are recorded in project provenance
```

The existing runtime enforces the verifier/receipt. The model decides **what evidence matters**; software mechanically enforces the chosen acceptance contract.

## 9. Auditor responsibilities

The independent decision auditor should challenge:

- `none` when current/domain knowledge obviously matters;
- loading unrelated references;
- relying on model memory for dynamic/high-stakes facts;
- stopping at a tweet when its linked article/repo contains the real substance;
- creator/vendor claims promoted to facts;
- 500-prompt/context dumps instead of distilled procedures;
- design cloning;
- dependency/artifact reuse without license/fit review;
- claiming a reference was used when it produced no traceable decision/evidence.

The auditor challenges; it does not become the semantic router.

## Completion check

For substantial reference-driven work:

- [ ] reference mode was chosen contextually;
- [ ] only relevant sources were loaded;
- [ ] underlying material was inspected when it contained the useful substance;
- [ ] current authoritative sources were used when required;
- [ ] reusable knowledge was distilled into the appropriate domain skill/reference rather than duplicated blindly;
- [ ] source roles/claims were not confused;
- [ ] durable material influences were documented where useful;
- [ ] the actual result was verified independently of the references.
