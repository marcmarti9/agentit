# Research quality for source-led decisions

Read this when research will change a product, executive, marketing, writing or capability decision, especially when social posts point to underlying material. It refines source handling; it does not make web research mandatory for local tasks.

## Research record per material source

For each source that changes the output, record:

```text
claim or decision it informs:
source URL and accessed date:
source role: canonical | licensed artifact | corroborated evidence | creator claim | inspiration | internal evidence
revision / publication date and license when reuse is contemplated:
what was directly observed:
limits, incentives, population or freshness risks:
decision changed:
what was deliberately not inferred or copied:
```

This is enough to audit a material decision without storing a browsing transcript or private reasoning.

## Match evidence to the question

Use the primary artifact for implementation and license questions: the repository at a pinned commit, a product’s official documentation, the law/regulator, or original research data. Use independent sources when a factual claim needs corroboration. Treat creator posts, vendor case studies, Reddit and X as discovery or qualitative signal unless they link to stronger underlying evidence.

When a social item contains a useful customer quote, preserve its context and platform bias. Do not infer market size, conversion lift, policy compliance or product availability from it. If X cannot be accessed or the post is unavailable, record it as an unverified lead and continue from the linked primary material; never fill the gap from a repost or model memory.

## Pin reusable upstream material

Before adapting a skill, prompt or code-like artifact, obtain the repository owner/name, immutable commit SHA, exact file path, license and any NOTICE/copyright obligation. A branch name, star count, package registry listing or secondary mirror does not substitute for this record. Prefer an original procedure in the existing local owner over importing broad upstream runtime/tooling.

## Synthesis test

Every research conclusion must say whether it is a fact, estimate, inference or recommendation. A reader should be able to answer: “What would change this conclusion?” If no source changed a decision, remove it from durable provenance. If the conclusion is still unsettled, describe the cheapest further observation/test instead of converting uncertainty into a confident rule.

## Source-informed adaptation

- **Source:** [coreyhaines31/marketingskills customer-research](https://github.com/coreyhaines31/marketingskills/blob/dda3841f0b294e01e93b1541486beefbfab0915e/skills/customer-research/SKILL.md) (MIT) and [SenteLabsAI/OpenExecutive](https://github.com/SenteLabsAI/OpenExecutive/tree/bba990f20dab7559967010e65b65630f1a35c684) (Apache-2.0).
- **Role:** licensed artifacts/inspiration for preserving evidence context, separating source modes and making decision-critical assumptions explicit.
- **Decision changed:** the existing reference-intelligence procedure gets a compact per-source decision record and explicit inaccessible-social-source handling.
- **Not imported:** third-party prompts, social content, executable tooling, model-specific behavior or any source’s confidence thresholds.

Follow the applicable MIT and Apache-2.0 attribution/NOTICE duties if any derived source material is redistributed.

Distribution attribution and exact source licenses are retained in `THIRD_PARTY_NOTICES.md`, `skills/ADAPTATION_SOURCES.json` and `vendor/adaptation-licenses/`. This reference is an Agentit-authored adaptation; it does not include upstream runtime/scripts.
