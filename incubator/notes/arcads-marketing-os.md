# Arcads Marketing OS — incubator notes

- Scouted: 2026-08-18
- Source: https://x.com/rom1trs/status/2089692842708938829
- Vendor: Arcads (`@rom1trs` / `@arcads_ai`)
- Status: incubating — public skill files not yet inspectable

## Claim

One Claude skill that simulates a six-hire marketing department and hands work between roles:

- Head of Marketing — positioning, pricing, competitor teardowns
- Copywriter — graded copy, email sequences, social posts
- Creative Strategist — hooks, creative fatigue vs dead audience, ranked tests
- Launch Lead — 4 weeks before launch, Product Hunt hour-by-hour
- SEO Lead — GEO, app store rankings
- Analyst — scored site audits, test design, spotting AI slop

Stated loop: Analyst finds the leak → Copywriter rewrites → Creative Strategist tests → Analyst grades.

## Fit with Agentit

- Layer 4 scout: tweet/ecosystem skill, not a core coding primitive.
- Topology: Pipeline / Writer-Reviewer, not a new Architect hierarchy.
- Existing overlap: `skills/marketing-and-growth` already covers CRO, technical SEO, landing copy, analytics. This candidate is a *role operating system*, not a replacement.
- Profile target if promoted: on-demand `product` (or a thinner `growth` pack). Never `core`.

## Gate before promotion

1. Obtain the actual skill tree (currently gated behind a comment-"OS" drop).
2. Record license, attribution, and any Arcads API / MCP dependency.
3. Measure SKILL.md + references size; slim if it blows token budgets.
4. Split into atomic skills if the mega-skill cannot progressive-disclose.
5. Register only after a curated `SKILL.md` exists under `skills/` and `THIRD_PARTY_NOTICES.md` is updated.
6. Keep router recommendation optional (`skills_recommended_missing`) until the pack is local.

## Non-goals

- Do not auto-activate on every interview.
- Do not vendor the upstream as-is.
- Do not treat Arcads video-ad generation as a required capability for Agentit coding work.
