# Agentit curated reference index

This is a **small discovery map**, not a database and not an always-loaded context bundle.

The normal path is:

```text
first-prompt dispatch
-> Agentit if material
-> pack + depth
-> selected skill
-> selected deep reference(s)
-> live sources only when needed
```

Runtime pack/depth discovery lives in:

- `skills/using-agent-skills/references/packs.md`

Reference handling discipline lives in:

- `skills/reference-intelligence/SKILL.md` — JIT; load only when references matter.

## Engineering / agent discipline

Durable ideas from the original bookmark audit are integrated into existing procedures rather than kept as social-post prompts:

- inspect discoverable repository context before asking avoidable questions;
- assumptions should be falsifiable and planning proportional to risk;
- skills are composable procedures, not mega-prompts;
- agent loops need explicit state/evidence/stop conditions;
- roles, skills, tools and verifiers are distinct responsibilities.

Useful upstream sources include Matt Pocock's composable skills, Min Choi's inspect-first engineering contract, self-correcting-agent loop material and versioned-agent-role patterns. Treat social-post claims as leads unless independently supported; licensed adapted material keeps attribution in the relevant notices.

## Design / premium web

Primary deep playbook:

- `skills/design-inspiration-research/references/premium-web-production.md`

It distills the useful workflow behind the bookmarked “$10k/$50k website” material: section-level references, design DNA, decision-frontier questions, vertical slice, one intentional signature interaction when justified, rendered defect pass, polish pass and real desktop/mobile/performance/accessibility QA.

Useful external discovery/reference sources from the audit include:

- real-site inspiration collections;
- Hallmark-style design study/anti-slop discipline;
- Checklist Design;
- 21st.dev component discovery;
- selected microinteraction/motion references;
- cinematic/3D production examples.

These are **design/process inputs**, not conversion or pricing evidence. Re-verify current tool/setup details live before depending on them.

## Marketing / growth / SEO

Load only the playbook that matches the current pack/stage:

- `skills/marketing-and-growth/references/marketing-operating-system.md`
  - distilled from the large marketing-prompt corpus into reusable customer research, positioning, content, copy, email, campaign and analytics procedures instead of hundreds of literal prompts.

- `skills/marketing-and-growth/references/seo-growth-loop.md`
  - data-first technical/search audit, gap/intent/schema/content opportunity, bounded changes, measurement windows and compact learnings.

- `skills/marketing-and-growth/references/launch-content-system.md`
  - launch research, factual brief, scene plan, asset/assembly workflow, claims/rights/brand QA, platform variants and learning loop.

The Grok SEO and Helena material contributes workflow architecture; vendor/creator performance figures remain claims, not independent benchmarks.

## Launch / content references

The launch/content playbook can draw on:

- Okara Launch Library for comparable launch patterns;
- Motion/product-video workflows for production acceleration;
- faceless-video automation patterns for script/timestamps/scene-aligned asset assembly.

Automate mechanical production, not factual/editorial/rights judgment. Revenue headlines attached to creator workflows are not proof of actual earnings.

## Build-vs-buy / tool discovery

Useful references can reveal component catalogs, chat infrastructure, creative-video systems or developer resource lists. Discovery does not equal adoption.

Use:

```text
need
-> inspect existing project capability
-> verify canonical/current external option
-> license/security/maintenance/dependency fit
-> ADOPT | ADAPT | COMPOSE | REFERENCE | INCUBATE | REJECT | BUILD
```

Do not promote a tool into global Agentit context merely because a bookmark made it look interesting.

## What deliberately stays out of the core

Specialized or hype-heavy material that does not improve the general operating protocol should be researched live only when relevant.

Examples deliberately not carried in active packs include:

- experimental huge-model offloading / Colibrì;
- salary/hiring anecdotes used mainly as attention hooks;
- temporary model-provider/free-tier hype.

## Adding future bookmarks

Do not just append URLs.

```text
bookmark
-> inspect underlying article/repo/video/docs
-> durable insight?
   no -> leave it out
   yes -> existing responsible skill?
          yes -> enrich that skill or references/*.md
          no -> add the smallest missing reusable capability
```

The promotion test is not “interesting”. It is:

> **Will this reliably improve recurring future work without wasting context?**
