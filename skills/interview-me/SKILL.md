---
name: interview-me
description: Confirm product intent before planning. Give independent recommendations, challenge materially weaker proposed methods, and keep final safe discretionary choices with the user. Greenfield and total visual redesigns require a deep recommendation-led interview.
---

# Interview Me

Product-affecting work is interviewed before planning/implementation. Purely mechanical execution may bypass. Inspect repo/docs/tools first so the user is never asked for facts Agentit can discover.

Users need no powerwords beyond natural Agentit activation. Do not require terms such as fan-out, Studio or pipeline.

## Recommendation is not agreement

The interview exists partly because the agent is expected to contribute judgment, not merely collect preferences.

When the user arrives with a proposed solution, separate:

- what outcome/constraint they actually own;
- what implementation/product/design method they currently suggest.

If the suggested method is materially weaker than a realistic alternative, say so in the interview. Recommend the alternative, explain the decisive trade-off, and ask the user to accept the recommendation or keep their original approach. Do **not** disguise disagreement as a neutral question when you actually have a strong evidence-backed recommendation.

Likewise, do not create arguments for show. If the user's proposal is sound and no alternative has a material advantage, recommend proceeding with it.

The user may answer “keep my approach” for any safe/feasible discretionary choice. Once that trade-off is explicit, persist and respect the resolved choice instead of re-litigating it during implementation.

## One comprehensive frontier round

Before asking anything, build a small **decision tree** for the task: what material choices exist, which are already resolved by evidence/context, which depend on another choice, and which unresolved choices can be answered independently now.

The currently answerable unresolved leaves are the **decision frontier**.

Ask **all material questions on the current decision frontier** in **one numbered batch**, not one question per message. Every question gets a recommendation/default. Use a follow-up batch only when the first answers expose **genuinely new material decisions** on a branch that could not reasonably have been known before.

This prevents two opposite failures:

- a linear interview that burns one message per independent question;
- a giant generic questionnaire containing branches that do not apply to this task.

The interview should make a weak prompt usable; it must not transfer the design/product job back to the user. The user may answer **“use your recommendation”** for any or all decisions.

For every product interview also recommend the primary domain pack. Ask craft depth only for genuinely visual/design work. Give a rough **project-aware token estimate** based on risk, complexity, domain, topology, likely specialists/critic and craft depth; state that it is provider-dependent and not a bill.

### Frontier construction rules

1. **Facts are not questions.** Discover repository, product, configuration, docs, analytics or source facts with available tools first.
2. **Outcome is not method.** Treat a user-suggested implementation as a candidate unless it is explicitly fixed as a requirement.
3. **Challenge material weaknesses.** Surface a better option when it materially improves the result; attach the recommendation and trade-off to the relevant frontier decision.
4. **Dependent choices wait.** If question B only makes sense after A is decided, do not ask B prematurely just to make the first batch look complete.
5. **Independent choices batch.** If audience, copy ownership and motion tolerance can all be answered independently, ask them together.
6. **Recommendations reduce cognitive load.** Give the default you would choose and why in one sentence. The recommendation should reflect your judgment, not what seems most agreeable.
7. **Materiality is the gate.** Do not ask about a preference that would not change implementation, risk, scope or acceptance.
8. **Persist the resolved tree.** Another agent should be able to see which branches were decided, which recommendation won, and which were intentionally left open.

## Mandatory deep visual interview

A new landing/homepage/public company or brand website/portfolio/storefront/campaign surface, or a request to completely redesign / do a “lavado total de cara” of an existing visual surface, gets a deep interview.

Cover the relevant decisions below in the first frontier batch when they are independently answerable:

1. **Outcome / conversion.** Recommend the primary action and ask what the surface must make people do or believe.
2. **Audience.** Recommend the likely primary audience; ask who matters most, what they know already, objections and trust concerns.
3. **Brand truth vs freedom.** List discoverable logo/colors/type/assets/product truth. Ask what must survive and, for total redesign, what may be replaced.
4. **Visual personality.** Offer 2–4 concrete, product-specific directions and recommend one. Examples: editorial/technical, warm/tactile, restrained/luxury, industrial/utilitarian. Do not ask only “what style?”.
5. **Imagery strategy.** Recommend imagery-heavy, imagery-light, artifact/product-led, or another fit. Distinguish photography, real screenshots, illustration, diagrams, video, 3D, generated art and no-imagery approaches. Ask what real assets exist.
6. **Critical copy ownership.** Ask whether Agentit may rewrite/restructure important copy. For hero/value proposition, key section headlines, CTA and proof/trust copy, propose a recommended message angle or 1–3 short candidate lines instead of asking the user to invent everything.
7. **Information architecture/story.** Suggest a likely page/section narrative; ask what must exist, what may disappear and whether reordering is allowed.
8. **Proof / credibility.** Ask what real evidence exists: clients, numbers, reviews, case studies, certifications, press, integrations, guarantees, team, physical presence or product screenshots. Never fabricate proof.
9. **Motion / interaction.** Recommend intensity. Distinguish quiet polish from cinematic/scrollytelling/spatial interaction.
10. **Distinctiveness tolerance.** Ask how far category conventions can be pushed and whether one memorable signature mechanic is desirable.
11. **References / dislikes.** Ask for any the user already has, but never depend on them; public visual work still gets Agentit's own inspiration research.
12. **Responsive/accessibility/performance constraints.** Ask only business/product constraints not already discoverable.
13. **Content volume/localization.** Ask when it materially changes navigation, composition or typography.
14. **Craft depth.** Recommend **Studio** for greenfield public surfaces and total visual redesigns; at least **Polished** for ordinary public-facing visual work unless the user wants leaner execution.

### Copy suggestion rule

Never ask an empty “What should the hero say?” when product context is sufficient to recommend wording. Give a suggested message direction or candidate lines and ask the user to accept/edit/reject them.

### Imagery suggestion rule

Never ask only “Do you want images?”. Explain the intended visual role/density. Example: “I’d make this product-led with 2–3 large real screenshots and almost no stock photography; okay?”.

## Domain packs

Recommend one primary pack from engineering, frontend, design, backend, data, product, writing, release, research or a user role. Load always-core + that family/task only, not every skill.

**Public visual surfaces are design-primary** even if a generic implementation description sounds like frontend or marketing. Implementation technology does not decide art direction.

If the user assigns a specialist role, scope skills to that role + core and discover missing coverage rather than inventing it.

## Craft depth and spend

Craft depth applies only to visual/design work:

- **Standard**: ordinary UI maintenance/components;
- **Polished**: public-facing work with stronger states/responsive/craft QA;
- **Studio**: flagship concepts; default recommendation for greenfield public surfaces and total redesigns.

For non-design thoroughness, lean/normal/thorough may be used as a soft spend posture. Do not present fixed historical token ranges as universal truth.

## Specialist/delegation questions

Do not force multi-agent ceremony, but treat these as legitimate benefits rather than excuses to stay direct:

- large documentation/reference reading;
- independent visual research angles;
- concept competition;
- fresh-context critique;
- independent packages/domains.

Studio greenfield/total public design normally warrants independent research/concept work plus a critic. The user does not need to request “multiple agents”.

## Small product changes

If only one or two genuine user decisions exist, ask both in one short round. Do not manufacture a 14-question interview for a two-line UI fix.

## After answers

1. Resolve contradictions.
2. Update the decision tree/frontier and identify any newly exposed material branches.
3. If a new material frontier exists, ask one follow-up batch; otherwise stop interviewing.
4. Restate confirmed intent, recommendations accepted/rejected, and defaults the user accepted.
5. Persist state per `docs/PROJECT_CONTINUITY.md` before implementation.
6. Capture outcome, audience, success criteria, constraints/non-goals, resolved method choices, domain pack, applicable craft depth/spend, rough token estimate and critic/specialist expectations.
7. For public greenfield/total redesign additionally persist brand preserve/replace decisions, visual directions, copy ownership/messages, imagery/assets strategy, IA/story, proof material, motion tolerance and references/dislikes.
8. Hand that state to research/art-direction stages; do not silently re-decide an informed user choice during coding.

## Mid-task escalation

If scope grows enough to materially change spend, topology or user-owned tradeoffs, surface the change before expanding work. Correctness requirements may force extra work; disclose why.

If implementation evidence later shows the accepted approach was based on a materially false assumption, challenge the decision again with the new evidence instead of blindly following stale intent.

## Non-interactive contexts

Do not simulate a fake interview in CI/autonomous execution. When unresolved product decisions materially affect the result, stop at a clear decision boundary rather than silently guessing them.

## Stop condition

The material decision frontier is empty **for the work currently authorized**, and a fresh agent can continue from persisted state without inventing material intent or re-deciding an already resolved trade-off. For greenfield/total visual work, copy strategy, imagery strategy and preservation/replacement scope are explicit enough to create a concrete `DESIGN_DIRECTION`.

## Anti-patterns

- automatic agreement because “the user asked for it that way”;
- performative disagreement with no material basis;
- silently overriding a safe informed user choice;
- one known question per turn;
- generic questionnaire containing irrelevant branches;
- asking dependent questions before their parent decision exists;
- asking only “what vibe?”;
- asking the user to write all critical copy from scratch;
- yes/no imagery questions with no recommendation;
- asking stack/version facts the repo can answer;
- craft depth questions for non-visual work;
- fixed token tables presented as billing truth;
- implementation before persisting intent;
- silent large spend escalation;
- treating multi-agent jargon as a powerword.

## Verification checklist

- [ ] Mechanical vs product-affecting classified.
- [ ] Discoverable facts inspected first.
- [ ] Outcome/hard constraints separated from proposed method.
- [ ] Materially better alternative surfaced when one exists.
- [ ] User's informed final safe discretionary choice persisted.
- [ ] Material decision tree/frontier identified.
- [ ] All material questions on the current frontier asked in one batch.
- [ ] Dependent branches deferred until meaningful.
- [ ] Recommendation/default attached to each question.
- [ ] Domain pack recommended; craft depth only when visual.
- [ ] Greenfield/total visual work received copy + imagery + preserve/replace questions.
- [ ] Rough project-aware token estimate supplied.
- [ ] Resolved decision tree persisted before implementation.
