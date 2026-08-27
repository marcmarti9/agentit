---
name: anti-ai-slop-writing
description: Rewrite or review prose so it reads like a deliberate human writer rather than a generic chatbot. Preserve claims and citations, match the writer/brand voice, remove structural AI tells, and keep technical/factual text precise.
license: MIT
sources:
  - https://github.com/blader/humanizer
  - https://github.com/hardikpandya/stop-slop
---

# Anti-AI-Slop Writing

Humanize prose without changing what it means.

This Agentit skill is an original provider-neutral synthesis informed by the pattern catalogs in `blader/humanizer` and `hardikpandya/stop-slop`. Do not vendor either upstream wholesale. The useful idea is the review method: detect repeated AI-writing patterns, preserve factual content, then rewrite for the actual writer and destination.

## Priority order

When goals conflict, use this order:

1. **Factual fidelity** — preserve claims, numbers, names, dates, quotes, caveats and citations unless the source/user authorizes a change.
2. **Destination fit** — README, PR, technical docs, email, article, landing copy, social copy and academic prose have different acceptable voices.
3. **Writer/brand voice** — match supplied examples or established project voice before generic style advice.
4. **Clarity and density** — remove filler and unnecessary ceremony.
5. **Natural rhythm** — vary sentence/paragraph shape when it improves readability; do not manufacture quirks merely to look human.

Never invent facts, opinions, anecdotes, citations or personal experiences just to make prose feel less synthetic.

## Choose the editing mode

Infer the smallest useful intervention:

```text
POLISH      -> keep structure and voice; remove obvious tells/filler
HUMANIZE    -> restructure when needed while preserving all substantive content
VOICE_MATCH -> use supplied authentic samples as the primary style reference
TECHNICAL   -> prioritize precision, explicit actors/contracts and reproducibility
MARKETING   -> preserve approved claims and brand voice; remove generic hype
```

Do not turn a proofreading request into a wholesale rewrite unless the original structure itself is the problem.

## Voice fingerprint

When the user/project supplies authentic writing samples, inspect them before rewriting:

- typical sentence length and variance;
- paragraph size and how paragraphs open;
- formal vs conversational vocabulary;
- contractions, fragments and parentheticals;
- punctuation habits;
- humor, uncertainty, bluntness or restraint;
- preferred transitions;
- formatting habits;
- terms the writer repeatedly uses on purpose.

Match **patterns**, not typos. A real sample overrides generic bans unless it would break the destination's requirements.

If no voice sample exists, default to clear, direct prose appropriate to the destination rather than trying to simulate a quirky person.

## Audit pass: content problems

Look for these before sentence-level cosmetics.

### Inflated importance

Remove claims that make ordinary facts sound historically important, transformative or symbolic without evidence.

Weak:

> The migration marks a pivotal evolution in the company's technological landscape.

Better:

> The migration moves the service from the legacy host to the new cluster.

### Unsupported interpretation

Watch for vague authority or analysis that has no source:

- “experts say”;
- “industry observers believe”;
- “this reflects a broader shift”;
- “it is widely recognized”;
- plausible biography/backstory used to fill an evidence gap.

Name the real source when one exists. Otherwise remove or narrow the unsupported claim.

### Sales fog

Words such as `revolutionary`, `groundbreaking`, `world-class`, `cutting-edge`, `seamless`, `stunning`, `robust` or `powerful` are not banned, but they need evidence or a real brand reason. Prefer the concrete capability/result.

### Fake completeness

Do not add stock “Challenges”, “Future outlook”, “Key takeaways” or conclusion sections merely because an article-like structure feels incomplete. A section earns its existence by adding information.

## Audit pass: structural AI tells

Patterns matter more than individual words. Rewrite when several of these cluster or when the structure sounds templated.

### Repeated binary contrast

Avoid defaulting to:

```text
not X, but Y
not just X; Y
it's not about X, it's about Y
```

Use it when the contrast is genuinely the point, not as a universal emphasis device.

### Forced symmetry and groups of three

Do not force every idea into three benefits, three adjectives, three clauses or identical bullet shapes. Use the number the content actually has.

### Metronomic lists

Repeated `- **Label:** explanation` blocks often read like generated scaffolding. Keep that format when it improves scanning; otherwise combine related ideas into prose or vary the structure naturally.

### Dramatic fragments

Fragments can be voice. They become slop when every paragraph ends with theatrical beats such as:

```text
No fluff.
No guessing.
Just results.
```

Prefer complete, specific statements unless the established voice genuinely uses fragments.

### Rhetorical setup spam

Reduce repeated questions answered immediately by the writer, fake suspense, “here's the thing”, “the catch?”, and narrator-like stage directions.

### Synonym cycling

Do not rename the same entity every sentence to avoid repetition. Repeating the correct noun is often clearer than `the platform` -> `the solution` -> `the ecosystem` -> `the offering`.

### Abstract noun chains

Rewrite phrases where nominalizations hide the action:

> implementation of optimization of configuration

into explicit actors and verbs.

## Audit pass: common language tells

These are **signals, not forbidden-word regexes**. Technical usage can be legitimate.

Watch clusters of:

- `delve`, `tapestry`, `testament`, `pivotal`, `intricate`, `vibrant`;
- abstract `landscape`, `realm`, `journey`, `ecosystem` when a concrete noun exists;
- `underscores`, `highlights`, `showcases`, `fosters`, `elevates`, `enhances` used as empty analysis;
- `serves as`, `stands as`, `boasts`, `offers` replacing simple `is`, `has`, `does`;
- throat clearing: `In today's fast-paced...`, `It is important to note...`, `When it comes to...`;
- mechanical transitions: `Furthermore`, `Moreover`, `Additionally` on every paragraph;
- fake enthusiasm: `Thrilled to announce`, `Excited to share`, `Great question!` when the destination does not call for it.

Do not mechanically delete a word if the rewrite becomes less accurate or less natural.

## Audit pass: sentence mechanics

Prefer explicit actors when they matter:

> The deployment preserves the old config.

is usually stronger than:

> The old config is preserved.

But passive voice is valid when the actor is unknown, irrelevant, intentionally de-emphasized, or standard in the destination.

Also check:

- repeated sentence openings;
- repeated sentence length;
- excessive subordinate clauses;
- fake “from X to Y” ranges where X/Y are merely unrelated examples;
- dangling `-ing` phrases that pretend to add analysis;
- vague pronouns with multiple possible referents;
- clipped negative endings that omit the actor/action.

## Formatting tells

Do not decorate prose by default.

Check for:

- bold on every important noun;
- emoji headings in technical/factual material;
- Title Case On Every Heading when the project uses sentence case;
- unnecessary blockquotes/callouts;
- huge stacks of micro-headings;
- canned opening and closing paragraphs from the assistant rather than the artifact.

Punctuation is voice-dependent. Do **not** globally ban em dashes, semicolons, parentheses, contractions or fragments. Match the writer/project and use each intentionally.

## Chatbot leakage

Remove assistant-facing residue from standalone artifacts unless explicitly desired:

- “Of course” / “Certainly”;
- “I hope this helps”;
- “Let me know if...”;
- “Would you like me to...”;
- references to training cutoff or inability to browse when they are not part of the artifact;
- meta-commentary such as “Here is the rewritten version.”

Do not turn uncertainty into certainty. If the source is incomplete, preserve the uncertainty cleanly.

## Technical/documentation mode

For READMEs, architecture docs, runbooks, PRs and technical explanations:

- name real components, files, interfaces and commands;
- state preconditions and side effects;
- prefer reproducible evidence over adjectives;
- keep established technical terms even if they resemble an AI-watch word;
- preserve warnings/caveats;
- do not add fake benchmark numbers or compatibility claims;
- avoid marketing voice unless the artifact is intentionally public positioning copy.

The reader should be able to act on the text, not merely agree that it sounds polished.

## Marketing mode

For landing pages, emails and campaigns:

- keep the approved positioning and factual claims;
- replace generic “transform your business” language with the concrete customer outcome;
- use proof that actually exists;
- let specificity create persuasion instead of superlative stacking;
- preserve deliberate brand swagger if it is authentic to supplied examples.

Humanized does not mean bland.

## Rewrite procedure

Use a compact multi-pass workflow:

```text
1. lock facts + required claims/citations
2. fingerprint destination + voice
3. mark structural/content AI tells
4. rewrite the largest structural problems first
5. clean sentence-level tells and filler
6. read for rhythm and voice
7. compare against the locked facts
8. return only the artifact format the task requires
```

For long text, do not optimize every sentence independently. Paragraph and document rhythm matter more than a bag of local substitutions.

## Final self-check

Before accepting the rewrite:

- [ ] No factual claim, number, caveat or citation was silently changed.
- [ ] No fact/source/personal experience was invented.
- [ ] The destination's voice is appropriate.
- [ ] Supplied authentic voice examples outrank generic rules.
- [ ] The prose is not built from repeated AI templates.
- [ ] Hype is backed by evidence or intentionally part of brand voice.
- [ ] Lists/headings/formatting exist because they help the reader.
- [ ] Sentence and paragraph rhythm is not mechanically uniform.
- [ ] Technical text remains exact and actionable.
- [ ] Standalone artifacts contain no leftover chatbot chatter.

## Failure modes

- replacing every “AI word” with a thesaurus synonym;
- enforcing arbitrary bans that erase the writer's real voice;
- making text casual when the destination requires formal precision;
- deleting caveats to sound more confident;
- adding anecdotes/opinions to fake humanity;
- preserving a generic article template while only swapping vocabulary;
- turning all prose into short punchy fragments;
- over-humanizing technical docs until contracts and evidence become vague.
