# Agentit curated reference index

This is a **small discovery map**, not a database and not an always-loaded context bundle.

The normal path is:

```text
first-prompt dispatch
-> Agentit if material
-> relevant semantic pack map(s)
-> selected skill(s)
-> selected reference(s)
-> live sources only when needed
```

Runtime pack discovery lives in:

- `skills/using-agent-skills/references/packs.md`

Reference handling discipline lives in:

- `skills/reference-intelligence/SKILL.md` — JIT; load only when references matter.

Packs are maps, not quality/effort levels. The primary AI chooses the smallest useful skill/reference set for the current stage; there is no `essential/standard/deep` reference depth contract.

## Engineering / agent discipline

Durable ideas from the original bookmark audit are integrated into existing procedures rather than kept as social-post prompts:

- inspect discoverable repository context before asking avoidable questions;
- assumptions should be falsifiable and planning proportional to risk;
- skills are composable procedures, not mega-prompts;
- agent loops need explicit state/evidence/stop conditions;
- roles, skills, tools and verifiers are distinct responsibilities.

Treat social-post claims as leads unless independently supported; licensed adapted material keeps attribution in the relevant notices.

## Design / premium web

Primary production playbook:

- `skills/design-inspiration-research/references/premium-web-production.md`

Component/reference scouting playbook:

- `skills/design-inspiration-research/references/component-reference-scouting.md`

Use the component scouting reference only when a frontend task materially benefits from external component, interaction, motion or design-system references. It keeps the project's own component system as the foundation, uses external catalogs as JIT discovery inputs, and requires an explicit `ADOPT | ADAPT | COMPOSE | REFERENCE | BUILD | REJECT` decision rather than blindly copying demos.

The premium-web playbook distills useful workflow patterns such as section-level references, design DNA, decision-frontier questions, a vertical slice, intentional signature interaction when justified, rendered defect/polish passes, and real desktop/mobile/performance/accessibility QA.

Useful external sources are design/process inputs, not conversion or pricing evidence. Re-verify current tool/setup details live before depending on them.

## Marketing / growth / SEO

Load only the playbook that matches the current task/stage:

- `skills/marketing-and-growth/references/marketing-operating-system.md`
- `skills/marketing-and-growth/references/seo-growth-loop.md`
- `skills/marketing-and-growth/references/launch-content-system.md`

Creator/vendor performance figures remain claims unless independently verified.

## Launch / content references

Launch/content work may draw on current launch libraries, product-video workflows, and scene-aligned production systems when relevant. Automate mechanical production, not factual/editorial/rights judgment.

Revenue headlines attached to creator workflows are not evidence of actual earnings.

## Build-vs-buy / tool discovery

Discovery does not equal adoption.

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

Specialized, volatile or hype-heavy material that does not improve the general operating protocol should be researched live only when relevant. Temporary model-provider/free-tier hype and experimental infrastructure belong here, not in globally injected context.

## Adding future references

Do not just append URLs.

```text
source
-> inspect underlying article/repo/video/docs
-> durable recurring insight?
   no -> leave it out
   yes -> existing responsible skill/reference?
          yes -> enrich it
          no -> add the smallest missing reusable capability
```

The promotion test is not “interesting”. It is:

> **Will this reliably improve recurring future work without wasting context or smuggling stale claims into the core?**
