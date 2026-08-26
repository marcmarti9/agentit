# Agentit state

**Updated:** 2026-08-26
**Status:** public-launch PR in verification
**Branch:** `docs/readme-jit-architecture`
**PR:** https://github.com/marcmarti9/agentit/pull/32

## Goal

Prepare Agentit for broader public introduction with a product-first README and a reusable launch package grounded in implemented repository capabilities and evidence-gated claims.

## Confirmed intent

- Present Agentit as it currently exists, without narrating earlier README/architecture shortcomings.
- Make the README explain the product quickly: what Agentit is, what it gives an agent, how to install it, how the architecture works, how it is evaluated, and where to learn more.
- Keep the public message provider-neutral and architecture-focused.
- Prepare channel-native launch material for X, Reddit, LinkedIn, GitHub and Hacker News.
- Keep comparative quality/cost/token/latency claims behind paired agent-level evidence.
- Preserve PR-first workflow; user/reviewer decides merge.

## Task decision

- Relevant packs: marketing, writing, release, research.
- Selected skills/reference material: `marketing-and-growth`, `anti-ai-slop-writing`, `shipping-and-launch`, `reference-intelligence`, `marketing-and-growth/references/launch-content-system.md`.
- Risk: RISK_2 (public-facing repository/docs changes, reversible through Git).
- Reference mode: both — current repository truth plus live platform/community guidance where channel behavior is time-sensitive.
- Topology: direct writer with review/verification; no parallel writer needed.
- External publication: not performed from this PR. Launch copy is prepared; GitHub merge/public posting remains a separate explicit publication step.

## Current status

- Complete: README rewritten into a shorter product-first public entry point.
- Complete: README focuses on current capabilities and positive architecture rather than project-history criticism.
- Complete: quick start, capabilities, JIT packs, Reference Intelligence, independent audit, Loop/Graph, continuity, MCP/capabilities, safety, evaluation and documentation links are represented.
- Complete: `docs/PUBLIC_LAUNCH.md` added with positioning, launch waves, X/Reddit/LinkedIn drafts, GitHub release draft, HN-specific guidance, demo/evidence plan and launch/product metrics.
- Complete: launch copy avoids unsupported benchmark claims and points paired evidence to issue #29.
- Current external research: relevant Reddit communities continue to discuss agent frameworks, MCP, safe tool use and open-source agent infrastructure. Current HN moderation guidance asks users not to submit AI-generated/AI-edited text and Show HN is being moderated more selectively; HN copy therefore must be written by the human from factual prompts rather than copied from the launch document.
- In progress: CI/final PR verification after the latest documentation commits.

## Important files and artifacts

- `README.md`
- `docs/PUBLIC_LAUNCH.md`
- `docs/agentit/STATE.md`
- `skills/using-agentit/SKILL.md`
- `skills/using-agent-skills/references/packs.md`
- `skills/marketing-and-growth/SKILL.md`
- `skills/marketing-and-growth/references/launch-content-system.md`
- `evals/evaluation-plan.md`
- issue #29: https://github.com/marcmarti9/agentit/issues/29
- PR #32: https://github.com/marcmarti9/agentit/pull/32

## Verification

- README content was checked against current Agentit core, packs, runtime, capability/MCP, continuity and evaluation documentation before rewriting.
- Public benchmark wording is constrained by issue #29/evaluation-plan evidence policy.
- Channel guidance was refreshed on 2026-08-26 for HN and current agent-tooling discussion surfaces.
- Final acceptance still requires CI/check status for the final PR head and a review of the resulting PR diff.

## Next actions

1. Check CI on the final PR head.
2. Review the final PR diff for stale/history-focused README language and public-claim accuracy.
3. Update PR #32 title/body to reflect the full public-launch package.
4. Leave merge to the user/reviewer.
5. After merge, publish the chosen channel posts and start collecting launch/evaluation evidence.

## Open questions / blockers

- Paired agent-level benchmark results do not yet exist; issue #29 remains the evidence milestone for comparative claims.
- HN text must be written by the human rather than copied from AI-generated launch drafts.

## Recovery

Resume from PR #32 on `docs/readme-jit-architecture`. Inspect the latest head, CI and diff. If CI fails, fix only the reported issue. If CI passes, the PR is ready for human review/merge.
