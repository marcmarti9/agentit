---
name: interview-me
description: Resolve only the material user-owned decisions that remain after inspecting available context. Batch independent questions, recommend defaults, challenge weaker methods, and preserve the user's final safe discretionary choice.
---

# Interview Me

Interviewing is a JIT tool for unresolved material intent, not a mandatory ceremony for all product work. Inspect the repository, docs, tools and known project facts first. Ask only questions whose answers can materially change scope, behavior, architecture, acceptance or user-visible direction.

No powerwords, Agentit jargon, effort tiers or token-budget ritual are required.

## Outcome is not method

Separate:

- the outcome, constraints and non-goals the user actually owns;
- the implementation/product/design method currently suggested.

If the suggested method is materially weaker than a realistic alternative, say so and recommend the better route with the decisive trade-off. If the user still chooses the original safe/feasible approach, persist and respect that informed choice.

Do not invent disagreement for show. If the proposed route is sound, recommend proceeding.

## Decision frontier

Before asking anything, identify the unresolved decisions that are both material and currently answerable. That set is the current decision frontier.

Ask **all material questions** on that frontier in **one numbered batch**. Every question should include a concise recommendation/default when the agent has enough evidence to provide one.

Use a **follow-up batch** only when the answers expose **genuinely new material decisions** that could not reasonably have been asked before.

This avoids both one-question-per-message interviews and giant generic questionnaires.

### Frontier rules

1. Discoverable facts are not user questions.
2. A suggested implementation is a candidate method unless explicitly fixed as a requirement.
3. Challenge a materially weaker method with a concrete alternative.
4. Defer dependent questions until their parent choice is resolved.
5. Batch independent material choices.
6. Recommendations should reduce cognitive load, not merely mirror the user.
7. Do not ask preferences that would not change the result.
8. Persist resolved decisions when continuity is actually warranted.

## Design and public-facing work

For greenfield or major redesign work, the unresolved frontier often includes:

- outcome/conversion goal;
- primary audience and trust concerns;
- brand/product truths that must survive;
- visual direction and distinctiveness tolerance;
- imagery/assets strategy;
- critical copy ownership and message direction;
- information architecture/story;
- available proof/credibility;
- motion/interaction tolerance;
- responsive/accessibility/performance business constraints;
- localization/content-volume constraints.

Offer concrete directions and a recommendation rather than asking empty questions such as “what vibe?” or “what should the hero say?”. Never fabricate proof or assets.

Desired ambition may be described naturally (for example restrained, premium, exploratory, cinematic, minimal). Do not convert that into named Agentit quality/effort tiers.

## Domain and execution implications

The interview may surface relevant semantic packs, references, tools or delegation opportunities, but the primary AI records those choices in `TASK_DECISION`. The user does not need to choose internal pack names, topology jargon or worker counts.

Do not estimate token spend as a product requirement unless the user explicitly asks about cost/budget. Agentit should optimize context internally rather than making token accounting part of ordinary interviews.

## Small changes

If only one or two genuine user decisions remain, ask only those. If none remain, do not interview.

## After answers

1. Resolve contradictions and update confirmed intent.
2. Record accepted/rejected recommendations and hard constraints.
3. Identify whether a genuinely new material frontier exists.
4. If none exists, stop interviewing and let the primary AI finalize `TASK_DECISION`.
5. When substantial continuity is warranted, persist only the compact outcome/constraints/decision state in private local `.agentit/STATE.md` or an explicitly configured equivalent.

Do not publish transient interview notes or private reasoning into repository documentation.

## Mid-task changes

If implementation evidence changes a material assumption or the authorized scope changes, surface the new decision boundary. Re-interview only the newly unresolved user-owned choice, then rebuild/review the affected `TASK_DECISION`.

## Non-interactive contexts

Do not simulate a fake interview in CI or autonomous execution. If an unresolved user-owned decision materially blocks a safe/correct result, stop at that explicit boundary rather than inventing intent.

## Stop condition

The material decision frontier is empty for the work currently authorized, and the primary AI can construct a concrete route without inventing user-owned intent.

## Anti-patterns

- mandatory interview ceremony for obvious work;
- asking facts already visible in the project;
- one known question per turn;
- giant questionnaires with irrelevant branches;
- empty “what vibe?” / “what copy?” prompts when a recommendation is possible;
- automatic agreement with a materially weaker method;
- silently overriding an informed safe user choice;
- named effort/craft tiers;
- token-budget estimates injected into normal product interviews;
- storing raw chats, secrets or private chain-of-thought.

## Verification checklist

- [ ] discoverable facts inspected first;
- [ ] outcome/hard constraints separated from proposed method;
- [ ] material weaknesses challenged when a realistic better route exists;
- [ ] all material questions on the current frontier asked in one numbered batch;
- [ ] follow-up batch used only for genuinely new material decisions;
- [ ] every useful question includes a recommendation/default when evidence allows;
- [ ] informed final safe discretionary choices are respected;
- [ ] no legacy tier/token ceremony was introduced;
- [ ] substantial continuity, if needed, is stored privately by default.
