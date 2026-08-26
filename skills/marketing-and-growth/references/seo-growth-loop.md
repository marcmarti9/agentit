# SEO / growth loop — distilled agent playbook

This reference distills the useful procedures behind the bookmarked Grok SEO prompt collection and Helena marketing-agent architecture. It is designed for real SEO/growth work with current data, not for preserving “magic prompts”.

## Provenance

Reviewed 2026-08-25:

- https://x.com/bloggersarvesh/status/2090789546925642183 — SEO workflow/prompt collection covering audits, competitive gaps, keywords/search intent, schema and content work.
- https://x.com/SeijinJung/status/2087909540679540898 — vendor architecture reference for a marketing agent connected to analytics/search/ads/CMS/email with scheduled reviews and persistent learnings.

Role: creator/vendor workflow inspiration. Any agency-price, revenue, ROAS or customer-performance claims remain vendor/creator claims unless independently corroborated.

## Core model

SEO/growth should be a feedback system:

```text
observe current evidence
-> diagnose
-> create/prioritize opportunity
-> propose or execute bounded change
-> verify deployment/indexability/tracking
-> wait an appropriate measurement window
-> evaluate outcome
-> write scoped learning
-> next action / stop / escalate
```

The agent is useful because it can repeatedly reason over evidence, not because it can run seven prompts in sequence.

## 1. Baseline before recommendations

Inspect the data sources relevant to the project. Possible sources include:

- Search Console;
- analytics/conversion tracking;
- current site/page HTML and rendered behavior;
- crawl/indexation evidence;
- current SERPs/search results when needed;
- product/catalog/feed data;
- business goals/margins where available;
- competitor/category pages;
- customer questions/reviews/support language;
- paid-search data only where it informs the question.

Record the period and data quality. If tracking is broken or ambiguous, say so before interpreting conversion changes.

## 2. Technical SEO audit

Inspect only applicable areas:

```text
crawlability / robots
indexability
canonicalization
redirects / status codes
sitemaps
internal linking
page titles / descriptions where useful
semantic headings/content structure
structured data appropriate to actual entities/content
rendering / JS discoverability
performance / Core Web Vitals where material
mobile usability
hreflang / locale when applicable
duplicate/thin/generated-content risks
orphan pages / pagination / faceting when applicable
```

For current search-engine rules and schema behavior, consult current canonical guidance instead of relying on this file as eternal truth.

Output findings as:

```text
finding
evidence / affected URLs
severity / business impact
confidence
proposed fix
blast radius
verification after fix
```

## 3. Search / competitor gap

Compare what users need with what the site and relevant competitors currently cover.

Look for:

- high-value queries/topics with no adequate page;
- existing pages ranking for mismatched intent;
- competitor topics/questions the project can answer credibly;
- weak proof or depth on important commercial pages;
- query clusters that should be consolidated rather than fragmented;
- internal-link opportunities;
- repeated category clichés that create weak differentiation.

Do not copy competitor content. Extract topic/intent gaps and create an original answer around the project's own expertise/product truth.

## 4. Keyword / intent research

Keywords are evidence of demand/language, not commands to stuff phrases into copy.

For each opportunity capture:

```text
query/topic cluster
intent
reader stage
current ranking/page if any
business relevance
content/product fit
competition / SERP pattern
proof/authority available
recommended action
```

When volume, difficulty, rankings or SERP features matter, obtain current data and record source/date.

## 5. Content brief

Before generating substantial SEO content, create a brief:

```text
primary topic / intent
reader + job-to-be-done
current page or gap
questions/subtopics to answer
unique evidence / project expertise
recommended structure
internal links
external/canonical source requirements
schema opportunity if genuinely applicable
CTA / next step
acceptance criteria
```

Content should satisfy the user problem first. Avoid producing pages solely because a keyword exists.

## 6. Schema / structured data

Use structured data only when it truthfully represents content/entities that are actually present.

Workflow:

```text
page/entity type
-> current official schema/search guidance
-> required/recommended properties
-> map real project data
-> implement
-> validate
-> inspect rendered output
```

Never fabricate reviews, ratings, prices, stock, organization facts, authorship or other properties to get richer snippets.

## 7. Opportunity backlog

Normalize findings into a backlog rather than implementing everything the agent notices.

Suggested fields:

```text
ID
area: technical | content | internal-link | schema | CRO | tracking | local | feed | other
observation
evidence
hypothesis
expected signal
impact
confidence
cost / complexity
risk / blast radius
action
owner / approval
review window
```

Prioritize with judgment. A simple `impact × confidence / effort` heuristic can help organize discussion, but the model should not pretend the numeric score is objective truth.

## 8. Bounded execution and permissions

High-autonomy work is usually appropriate for:

- read-only analysis;
- clustering and briefs;
- draft copy/content;
- technical diagnosis;
- post-deploy checks;
- periodic opportunity summaries.

Use stronger gates for:

- bulk URL/canonical/redirect changes;
- publishing many generated pages;
- changing templates across large catalogs;
- ad budgets/bids/campaign writes;
- production CMS mutations;
- tracking/conversion changes;
- claims with regulatory/commercial consequences.

A learning loop must never grant itself broader permissions.

## 9. Scheduled review loop

The Helena reference's durable idea is scheduled evidence review with compact persistent learnings.

A recurring job should declare:

```text
objective
input sources
frequency justified by data-change rate
allowed actions
metric / signal
review window
stop condition
escalation condition
output consumer
```

Do not create automations as a KPI. One useful weekly GSC review can be better than 100 jobs producing noise.

## 10. Learning record

Store only scoped evidence-based learning:

```text
observation:
evidence + period:
confidence: low | medium | high
scope:
what changes next:
recheck trigger/date:
```

Examples of bad learnings:

- “Google likes long articles.”
- “This title always works.”
- “CTR went up after our change, therefore our change caused it” without enough evidence/context.

## 11. SEO reviewer checklist

Before calling an SEO/growth task complete:

- [ ] current evidence was inspected where the task depends on current state;
- [ ] data quality/tracking uncertainty is explicit;
- [ ] findings link to affected pages/data rather than generic best practices;
- [ ] current official guidance was checked for changing technical rules;
- [ ] competitor/search research informed gaps, not copied content;
- [ ] schema represents real page/entity data;
- [ ] recommendations are prioritized rather than dumped;
- [ ] risky/bulk actions have an appropriate gate;
- [ ] measurement/review window is defined for changes expected to move metrics;
- [ ] learnings are scoped to evidence, not promoted into universal rules.

## The distilled takeaway

The useful parts of the bookmarked “agency-level SEO prompts” and autonomous marketing-agent systems are:

```text
specialized procedure
+ current connected evidence
+ bounded action
+ delayed measurement
+ persistent scoped learning
```

Not the price comparison, number of prompts, or number of automations.
