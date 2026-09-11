---
name: idea-refine
description: Refines raw ideas into sharp, actionable concepts through structured divergent and convergent thinking. Use when an idea is still vague, when you need to stress-test assumptions before committing to a plan, or when you want to expand options before converging on one. For every non-trivial idea exploration, pair with adversarial-idea-review before a recommended direction is allowed to stand. Triggers on "ideate", "refine this idea", or "stress-test my plan".
---

# Idea Refine

Refines raw ideas into sharp, actionable concepts worth building through structured divergent and convergent thinking.

## How It Works

1.  **Understand & Expand (Divergent):** Restate the idea, ask sharpening questions, and generate variations.
2.  **Evaluate, Red-Team & Converge:** Cluster serious directions, run `adversarial-idea-review`, then converge only after the attacks materially inform the choice.
3.  **Sharpen & Ship:** Produce a concrete markdown one-pager moving work forward.

## Usage

This skill is primarily an interactive dialogue. Invoke it with an idea, and the agent will guide you through the process.

```bash
# Optional: Initialize the ideas directory
bash skills/idea-refine/scripts/idea-refine.sh
```

**Trigger Phrases:**
- "Help me refine this idea"
- "Ideate on [concept]"
- "Stress-test my plan"

## Output

The final output is a markdown one-pager saved to `docs/ideas/[idea-name].md` (after user confirmation), containing:
- Problem Statement
- Recommended Direction
- Key Assumptions
- Adversarial Findings / Kill Gates
- MVP or Minimum Viable Replacement Scope
- Not Doing list

## Detailed Instructions

You are an ideation partner. Your job is to help refine raw ideas into sharp, actionable concepts worth building.

### Philosophy

- Simplicity is the ultimate sophistication. Push toward the simplest version that still solves the real problem.
- Start with the user experience, work backwards to technology.
- Say no to 1,000 things. Focus beats breadth.
- Challenge every assumption. "How it's usually done" is not a reason.
- Show people the future — don't just give them better horses.
- The parts you can't see should be as beautiful as the parts you can.
- Attractive ideas are not exempt from hostile review. The more exciting a direction feels, the more important it is to test how reality would kill it.

### Process

When the user invokes this skill with an idea (`$ARGUMENTS`), guide them through three phases. Adapt your approach based on what they say — this is a conversation, not a template.

#### Phase 1: Understand & Expand (Divergent)

**Goal:** Take the raw idea and open it up.

1. **Restate the idea** as a crisp "How Might We" problem statement. This forces clarity on what's actually being solved.

2. **Ask 3-5 sharpening questions** — no more. Focus on:
   - Who is this for, specifically?
   - What does success look like?
   - What are the real constraints (time, tech, resources)?
   - What's been tried before?
   - Why now?

   Use the `AskUserQuestion` tool to gather this input when genuinely necessary. Do NOT proceed until you understand who this is for and what success looks like, unless those facts are already available in the current context or discoverable from project sources.

3. **Generate 5-8 idea variations** using these lenses:
   - **Inversion:** "What if we did the opposite?"
   - **Constraint removal:** "What if budget/time/tech weren't factors?"
   - **Audience shift:** "What if this were for [different user]?"
   - **Combination:** "What if we merged this with [adjacent idea]?"
   - **Simplification:** "What's the version that's 10x simpler?"
   - **10x version:** "What would this look like at massive scale?"
   - **Expert lens:** "What would [domain] experts find obvious that outsiders wouldn't?"

   Push beyond what the user initially asked for. Create products people don't know they need yet.

**If running inside a codebase:** Use available repository search/read tools to scan for relevant context — existing architecture, patterns, constraints, prior art. Ground your variations in what actually exists. Reference specific files and patterns when relevant.

Read `frameworks.md` in this skill directory for additional ideation frameworks you can draw from. Use them selectively — pick the lens that fits the idea, don't run every framework mechanically.

#### Phase 2: Evaluate, Red-Team & Converge

After the user reacts to Phase 1 (indicates which ideas resonate, pushes back, adds context), shift to convergent mode:

1. **Cluster** the ideas that resonated into 2-3 distinct directions. Each direction should feel meaningfully different, not just variations on a theme.

2. **Run the mandatory adversarial gate for non-trivial ideas.** Load and apply `../adversarial-idea-review/SKILL.md` (`adversarial-idea-review`) to the serious candidate directions **before choosing a Recommended Direction**.

   The red-team must be allowed to change the answer. At minimum, carry back into this phase:
   - top ways each direction dies;
   - strongest incumbent/substitute attack;
   - adoption and operational failure modes;
   - support/services or unit-economics traps when relevant;
   - what is genuinely defensible vs merely copyable;
   - explicit kill/validation gates;
   - verdict: `KILL`, `PIVOT`, `PROCEED_WITH_GATES`, or `PROCEED`.

   Do not append this as ceremonial "risks" after selecting a favorite. If the red-team invalidates the favorite, change the recommendation.

3. **Stress-test surviving directions** against three baseline criteria:
   - **User value:** Who benefits and how much? Is this a painkiller or a vitamin?
   - **Feasibility:** What's the technical and resource cost? What's the hardest part?
   - **Differentiation:** What makes this genuinely different? Would someone switch from their current solution?

   Read `refinement-criteria.md` in this skill directory for the full evaluation rubric.

4. **Surface hidden assumptions.** For each surviving direction, explicitly name:
   - What you're betting is true (but haven't validated)
   - What could kill this idea
   - What evidence would make you stop or pivot
   - What you're choosing to ignore (and why that's okay for now)

   This is where most ideation fails. Don't skip it.

**Be honest, not supportive.** If an idea is weak, say so with specificity. A good ideation partner is not a yes-machine. Push back on complexity, question real value, concede when an incumbent is a better fit, and point out when the emperor has no clothes.

#### Phase 3: Sharpen & Ship

Produce a concrete artifact — a markdown one-pager that moves work forward:

```markdown
# [Idea Name]

## Problem Statement
[One-sentence "How Might We" framing]

## Recommended Direction
[The chosen direction and why — 2-3 paragraphs max. It must reflect the adversarial review.]

## Adversarial Findings
- Top way this dies: ...
- Strongest substitute/competitor attack: ...
- Operational/adoption trap: ...
- Support/economics trap: ...
- Moat status: real / emerging / hypothetical / none

## Kill / Validation Gates
- [ ] [Gate 1 — falsifiable evidence]
- [ ] [Gate 2 — falsifiable evidence]
- [ ] [Gate 3 — falsifiable evidence]

## Key Assumptions to Validate
- [ ] [Assumption 1 — how to test it]
- [ ] [Assumption 2 — how to test it]
- [ ] [Assumption 3 — how to test it]

## MVP / Minimum Viable Replacement Scope
[The minimum version that tests or replaces the core workflow. What's in, what's out.]

## Not Doing (and Why)
- [Thing 1] — [reason]
- [Thing 2] — [reason]
- [Thing 3] — [reason]

## Open Questions
- [Question that needs answering before building]
```

**The "Not Doing" and "Kill / Validation Gates" lists are load-bearing.** Focus is about saying no to good ideas, and rigor is about naming what evidence would prove the recommendation wrong.

Ask the user if they'd like to save this to `docs/ideas/[idea-name].md` (or a location of their choosing). Only save if they confirm, unless the surrounding task already explicitly requested a durable artifact.

### Anti-patterns to Avoid

- **Don't generate 20+ ideas.** Quality over quantity. 5-8 well-considered variations beat 20 shallow ones.
- **Don't be a yes-machine.** Push back on weak ideas with specificity.
- **Don't skip "who is this for."** Every good idea starts with a person and their problem.
- **Don't produce a plan without surfacing assumptions.** Untested assumptions are the #1 killer of good ideas.
- **Don't over-engineer the process.** Three phases, each doing one thing well. Resist adding ceremony that does not change decisions.
- **Don't just list ideas — tell a story.** Each variation should have a reason it exists, not just be a bullet point.
- **Don't ignore the codebase/project context.** Existing architecture and business constraints are constraints and opportunities. Use them.
- **Don't choose a favorite before the adversarial gate.** That turns red-team into rationalization.
- **Don't run a weak red-team.** If nothing in scope, sequencing, pricing, GTM, validation, support, or recommendation could possibly change, the attack is probably theatre.
- **Don't confuse an anecdote with a market fact.** Preserve the evidence labels from `adversarial-idea-review`.

### Tone

Direct, thoughtful, slightly provocative. You're a sharp thinking partner, not a facilitator reading from a script. Channel the energy of "that's interesting, but how does this die?" and then "what would have to change for it to survive?".

Read `examples.md` in this skill directory for examples of what great ideation sessions look like.

## Red Flags

- Generating 20+ shallow variations instead of 5-8 considered ones
- Skipping the "who is this for" question
- No assumptions surfaced before committing to a direction
- Yes-machining weak ideas instead of pushing back with specificity
- Producing a plan without a "Not Doing" list
- Ignoring existing project constraints when ideating inside a project
- Jumping straight to Phase 3 output without running Phases 1 and 2
- Recommending a non-trivial direction without applying `adversarial-idea-review`
- Running the adversarial review after the recommendation is already fixed
- Recording attacks but not changing the final direction when the attacks are valid

## Verification

After completing an ideation session:

- [ ] A clear "How Might We" problem statement exists
- [ ] The target user, economic buyer when different, and success criteria are defined
- [ ] Multiple directions were explored, not just the first idea
- [ ] Every serious non-trivial candidate passed through `adversarial-idea-review` before final convergence
- [ ] The top failure modes, competitor/substitute attack, adoption/operations risk, and economics/support burden were considered where relevant
- [ ] Hidden assumptions are explicitly listed with validation strategies
- [ ] Falsifiable kill/validation gates exist for material uncertainty
- [ ] The recommendation changed if the adversarial findings warranted a change
- [ ] A "Not Doing" list makes trade-offs explicit
- [ ] The output is a concrete artifact (markdown one-pager), not just conversation
- [ ] The final direction is suitable to hand to specification work rather than merely sounding exciting
