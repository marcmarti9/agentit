# Marketing operating system — distilled from large prompt libraries

This reference converts the useful structure behind the bookmarked “500 prompts / replace a $10k marketing agency” article into reusable Agentit procedures.

It intentionally does **not** vendor hundreds of prompts verbatim. A prompt dump is hard to maintain, expensive in context, and encourages agents to choose wording templates instead of reasoning about the actual business. The durable asset is the **work graph** behind the prompts: inputs, intermediate artifacts, decisions, checks, and measurement loops.

## Provenance

Primary bookmarked source reviewed 2026-08-25:

- https://x.com/cyrilXBT/status/2083235395236495817 — large Claude/Fable marketing prompt collection covering strategy, copy, social, SEO, brand voice, customer research, email, repurposing, and related work.

Related bookmarked sources that reinforce the operating model:

- https://x.com/bloggersarvesh/status/2090789546925642183 — SEO prompt/workflow collection.
- https://x.com/SeijinJung/status/2087909540679540898 — marketing-agent architecture with live integrations and scheduled feedback loops.
- https://x.com/askOkara/status/2090804619626860811 — launch-reference research library.

Authority: **creator guidance / workflow inspiration**. Claims that these prompts replace a specific agency retainer or produce specific revenue are not independent evidence.

## Core principle

The useful transformation is:

```text
500 prompts
    ↓
~10 reusable marketing capabilities
    ↓
small context-specific procedures
    ↓
real business inputs
    ↓
measured outputs
```

Do not ask “which prompt number should I use?” Ask “what marketing decision or artifact is required, what evidence do I have, and what should happen next?”

## Context contract

Before substantial marketing work, inspect or request the smallest set of information that materially changes the result.

```text
OFFER
- what is being sold
- price / packaging when relevant
- actual differentiators
- real proof available

AUDIENCE
- target user/customer
- situation / trigger
- pain / desired outcome
- awareness level

MARKET
- competitors / alternatives
- category expectations
- objections
- search/social language where available

BRAND
- voice examples
- forbidden claims/phrasing
- desired personality

GOAL
- awareness | signup | lead | purchase | retention | launch | SEO | other
- primary CTA
- measurement window

EVIDENCE
- customer quotes/reviews
- analytics/search data
- winning/losing existing content
- product/customer-support data
```

If the repository or connected sources already contain these facts, inspect them before asking the user.

## Capability 1 — Customer / ICP research

### Goal
Create an actionable model of the customer, not a decorative persona.

### Inputs
- product/service truth;
- customer interviews/reviews/support logs when available;
- current audience data;
- category/competitor evidence.

### Output

```text
ICP / CUSTOMER MODEL
who:
trigger / job-to-be-done:
current alternative:
important pains:
desired outcomes:
decision criteria:
objections:
language / phrases observed:
proof they need:
channels / contexts:
unknowns:
```

### Objection map

For material purchase objections, distinguish:

```text
surface objection
underlying concern
emotional/risk root
proof or response actually available
claim we must not make
```

Do not invent psychological detail unsupported by evidence.

## Capability 2 — Competitive and category analysis

Analyze competitors to find **gaps and conventions**, not to clone their copy.

For each relevant competitor/alternative inspect:

- audience and positioning;
- primary promise;
- proof strategy;
- offer/pricing structure when public/current;
- content themes;
- CTA/funnel;
- obvious strengths;
- repeated category clichés;
- missing questions/needs;
- customer complaints/review themes where available.

Output:

```text
CATEGORY MAP
table stakes:
overused claims:
credible differentiation opportunities:
content/search gaps:
proof gaps:
risks of sounding interchangeable:
```

Current prices/features must be re-verified before they become strategic premises.

## Capability 3 — Positioning and message house

Translate product truth + customer evidence into a messaging system.

### Positioning draft

```text
For <audience in situation>,
<product> is <category / frame>
that helps <outcome>
through <credible mechanism/difference>,
unlike <alternative>,
because <proof / reason to believe>.
```

This is a thinking scaffold, not mandatory public copy.

### Message house

```text
CORE PROMISE
- concise, truthful value proposition

PILLAR 1
- claim
- proof
- supporting examples

PILLAR 2
...

PILLAR 3
...

OBJECTIONS
- objection -> truthful answer/proof

CTA
- action + expected next step
```

Generate several positioning/headline variants when the decision is uncertain, then choose based on strategy/evidence rather than random preference.

## Capability 4 — Content strategy

Build strategy around audience problems and distribution mechanics, not a calendar full of filler.

Output:

```text
CONTENT STRATEGY
business objective:
audience:
content jobs:
content pillars:
proof / artifact sources:
channels:
format families:
posting/testing cadence:
conversion bridge:
metrics:
stop/review conditions:
```

Possible content jobs:

- teach a decision/framework;
- demonstrate product/mechanism;
- answer objections;
- provide proof/case study;
- compare alternatives;
- capture search intent;
- create awareness/hook;
- launch/update;
- repurpose a strong source asset.

A content pillar exists because it supports a business/audience need, not because “every brand needs five pillars.”

## Capability 5 — Copy / landing / sales assets

For substantial copy, reason through:

```text
reader state
-> desired next action
-> key promise
-> proof
-> objections
-> information sequence
-> copy
-> factual/brand review
```

### Sales/landing page skeleton

Use only sections that the offer actually needs:

- first-view proposition + CTA;
- problem/context;
- mechanism/product explanation;
- proof/demo/artifacts;
- benefits/outcomes;
- use cases;
- objections/FAQ;
- pricing/offer;
- final CTA.

Do not generate fake social proof to populate a conventional template.

### Headline exploration

Generate variants across **strategic angles**, not synonyms:

- outcome;
- pain/problem;
- mechanism;
- differentiation;
- identity/audience;
- speed/convenience only if truthful;
- proof-led only when proof exists.

Record what hypothesis each angle tests.

## Capability 6 — Repurposing / content atomization

One strong source asset can produce many native derivatives, but the output should adapt to the platform rather than mechanically truncate the same text.

```text
SOURCE ASSET
  -> extract thesis / proof / stories / examples / quotes
  -> choose platform-native angle
  -> generate derivatives
  -> remove duplication/filler
  -> factual/brand check
```

Possible derivatives:

- X post/thread;
- LinkedIn post;
- short-form video script;
- carousel;
- newsletter section;
- YouTube intro/outline;
- podcast outline;
- FAQ/help/article fragment.

Keep the source-of-truth facts synchronized. Repurposing must not create stronger claims than the original evidence.

## Capability 7 — SEO opportunity and content brief

Do not start with “write an SEO article”. Start from live search/business evidence when material.

### Opportunity discovery

Use current sources such as Search Console, keyword/search results, customer questions, competitors, and site inventory to classify:

- query/topic;
- intent;
- audience stage;
- current page or gap;
- business value;
- evidence/authority available;
- cannibalization risk;
- expected action.

### Content brief

```text
primary topic/query:
intent:
reader:
job/problem:
existing page / gap:
secondary concepts/questions:
recommended structure:
key points that must be answered:
internal links:
source/evidence requirements:
unique angle / differentiation:
CTA:
acceptance criteria:
```

Do not preserve stale keyword-volume/search-engine claims as permanent facts. Re-check current platform/search evidence.

## Capability 8 — Email lifecycle

Choose the sequence from the customer state, not from a fixed “5 email template”.

### Welcome/onboarding

Possible jobs:

1. confirm expectation / deliver promised asset;
2. establish problem/mechanism;
3. demonstrate value/use case;
4. answer main objection;
5. present appropriate CTA.

### Abandoned cart / incomplete action

Possible jobs:

- remind without manipulation;
- surface practical friction;
- reinforce product/offer truth;
- answer uncertainty;
- time-sensitive offer only if genuinely time-sensitive.

### Newsletter

Each issue should have a primary reader value and optional commercial bridge, rather than stuffing unrelated announcements together.

For every email sequence define suppression/unsubscribe/compliance requirements appropriate to the actual system/jurisdiction.

## Capability 9 — Campaign / launch architecture

For a material launch, chain the work instead of asking one model for “a campaign”.

```text
customer/category research
-> positioning
-> message house
-> launch brief
-> channel / campaign architecture
-> messaging matrix
-> core assets
-> platform-native derivatives
-> publish/distribute
-> collect questions/data
-> follow-ups
-> review outcome
```

### Launch brief

```text
what is launching:
audience:
trigger/problem:
one-sentence promise:
credible mechanism:
proof available:
main objection:
primary CTA:
channels:
creative/reference patterns:
claims/rights constraints:
success metrics:
review date/window:
```

Use launch libraries as pattern research, not copy sources.

## Capability 10 — Analytics, CRO, and learning loop

A marketing artifact is not “good” because the agent likes the copy.

Define outcome evidence appropriate to the task:

- CTR;
- watch/completion;
- qualified leads;
- signup completion;
- conversion rate;
- revenue / margin where available;
- search impressions/clicks/rankings;
- retention;
- replies/questions;
- qualitative objections.

Closed loop:

```text
baseline
-> hypothesis
-> change/content/campaign
-> measurement window
-> result
-> learning
-> keep / iterate / revert / stop
```

Persist learnings with scope and confidence; do not create universal rules from tiny samples.

## High-value workflow chains

### A. Go-to-market / launch

```text
customer evidence
-> competitor/category teardown
-> ICP synthesis
-> positioning
-> message house
-> launch brief
-> campaign/channel plan
-> assets
-> distribution
-> measurement
```

### B. Compounding content engine

```text
audience/search questions
-> topic clusters / content pillars
-> voice constraints
-> pillar asset
-> platform-native atomization
-> distribution
-> performance evidence
-> update future topics/angles
```

### C. SEO engine

```text
GSC/search/site evidence
-> opportunity map
-> content/technical brief
-> implementation
-> indexability QA
-> wait window
-> measurement
-> next opportunity
```

### D. Email funnel

```text
customer state / trigger
-> objective
-> objections
-> sequence jobs
-> copy
-> compliance + delivery QA
-> conversion/engagement evidence
-> iterate
```

### E. CRO campaign

```text
funnel evidence
-> friction hypothesis
-> message/design change
-> QA
-> test/measurement
-> learn
```

## How to use a giant prompt library correctly

A large prompt library is a **discovery dataset**, not a runtime dependency.

When one is encountered:

1. scan it for capabilities/procedures not already covered;
2. group near-duplicates;
3. extract input/output/evidence patterns;
4. incorporate only durable missing procedures into the relevant Agentit skill/reference;
5. preserve provenance;
6. discard hype and redundant wording;
7. do not load the original hundreds of prompts into normal task context.

This is the same reason codebases use functions/modules rather than copying 500 similar snippets into every file.

## Agent behavior over prompt wording

The article's strongest meta-principle is that good outputs depend on context and iteration more than on incantation-like wording.

Prefer:

- real customer/product context;
- examples of the brand's actual good content;
- explicit constraints;
- evidence and sources;
- iterative critique in the same task;
- artifacts that feed the next stage.

Avoid:

- “act as a world-class marketer” as a substitute for data;
- preserving 500 numbered prompts because they sound specific;
- claiming agency-equivalent results from prompt count;
- treating AI as a search engine for current facts without live sources;
- generating every channel before knowing which channels matter.

## Completion test

A marketing task using this reference should be able to answer:

- What business/audience problem was solved?
- Which evidence informed the work?
- Which intermediate artifact/decision led to this output?
- Which claims are supported?
- What will measure whether this worked?
- What happens after the measurement window?

If the answer is only “I used prompt 217”, the system failed.
