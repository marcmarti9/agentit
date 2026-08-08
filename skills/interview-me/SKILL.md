---
name: interview-me
description: Clarify underspecified intent with focused questions. Use before planning when goals or users are unclear; not when requirements are concrete.
---

# Interview Me

## Overview

What people ask for and what they actually want are different things. They ask for "a dashboard" because that's what one asks for, not because a dashboard solves their problem. They say "make it faster" without a number to hit.

The cheapest moment to find this gap is before any plan, spec, or code exists. Once you've started building, switching costs are real, and the user will rationalize the wrong thing into a "good enough" thing. The misfit gets locked in.

This skill closes the gap before it costs anything. The other Define-phase skills assume you already know roughly what you want: `idea-refine` generates variations from an idea, `spec-driven-development` writes the requirements down, `doubt-driven-development` stress-tests a plan after you've drafted one. Interview-me is the part before all of those: map the design as a decision tree, work the frontier in rounds (with a recommended answer on each question), and stop only when shared understanding is real.

Default cadence is still one question at a time when confidence is climbing and questions chain. Use **frontier rounds** when confidence is below ~70% and two or more independent decisions are already unblocked (see Step 2).

## When to Use

Apply this skill when:

- The ask is missing at least one of: **who** the user is, **why** they want it, what **success** looks like, what the binding **constraint** is
- The request is conventional rather than specific ("build me X", "make it faster") and you can't unpack the convention without guessing
- You're tempted to start with assumptions you haven't surfaced
- The user hasn't said which value they're optimizing for when two reasonable ones are in tension (simplicity vs. flexibility, cost vs. speed)
- The user explicitly invokes: "interview me", "grill me", "before we start, are we sure?", "stress-test my thinking"

**When NOT to use:**

- The ask is unambiguous and self-contained ("rename this variable", "fix this typo")
- The user has explicitly asked for speed over verification
- Pure information requests ("how does X work?", "what does this code do?")
- Mechanical operations (renames, formats, file moves)
- You already have ≥95% confidence; re-read the stop condition below before assuming you don't

## Loading Constraints

This skill needs a live, responsive user. **Do not invoke in non-interactive contexts** like CI pipelines, scheduled runs, `/loop`, or autonomous-loop. If you're in one of those and the ask is underspecified, flag that as a blocker for the user instead of guessing.

## The Process

### Step 1: Hypothesize, with a confidence number

Before asking anything, write down your current best read of what the user wants in **one sentence**, plus an honest confidence number (0–100%):

```
HYPOTHESIS: You want a way to answer "how are we doing?" in standup, and "dashboard" was the convention that came to mind.
CONFIDENCE: ~30% — missing: who it's for, what "metrics" means in context, and what success looks like
```

The number forces honesty. If you wrote down a high number but can't actually predict the user's reactions to the next three questions you'd ask, the number is wrong. Start at the confidence level you can defend.

When confidence is below ~70%, append a brief reason on the same line — what's still unresolved or missing. This tells the user exactly what the interview needs to surface, and prevents the number from being a vague signal.

### Step 2: Work the design tree (single question or frontier round)

Treat the problem as a **design tree**: every settled decision unlocks the decisions that hang off it. The **frontier** is the set of decisions whose prerequisites are already settled — questions you can ask *now* without guessing answers you have not heard.

**Mode A — One question (default when questions chain):**

```
Q: <one focused question>
GUESS: <your hypothesis for the answer, with the reasoning that produced it>
```

Wait for the user to react before asking the next question.

Use Mode A when the next question depends on the previous answer, or when confidence is already ≥70% and you only need to close a small gap.

**Mode B — Frontier round (when confidence &lt; ~70% and ≥2 independent frontier questions exist):**

Ask the whole independent frontier in one round. Number each question and attach a recommended answer. Do not include questions that still depend on an unsettled answer in this same round.

```
FRONTIER ROUND (confidence ~40% — missing: user, success metric, constraint)

❓ **Q1** - **Who is this for?**: <body>
➡️ engineering team in standup (default guess)

❓ **Q2** - **What does done look like?**: <body>
➡️ a single list of experiments with status, not charts

❓ **Q3** - **What must we not build?**: <body>
➡️ no real-time dashboards, no multi-tenant admin
```

Wait for answers to the whole round, then recompute the frontier. A question whose answer depends on another still-open question belongs to a *later* round.

**Facts vs decisions:** Finding facts (repo layout, existing APIs, file names) is your job — look them up or dispatch a read-only probe. Do not ask the user for anything you can verify in the environment. Decisions stay with the user.

**Why attach a guess / recommendation:**

- The user reacts faster to a wrong guess than they generate an answer from scratch
- It commits you to a hypothesis you can be visibly wrong about, which keeps you honest
- It surfaces *your* assumptions, which is what the interview is meant to expose

**Why not always batch:**

- Dependent questions asked together lock in the wrong framing
- Polite users skim long lists and agree by default
- Energy for careful thinking is finite

Mitigate sycophancy by being visibly willing to be wrong, and occasionally guess in a direction you expect the user to push back on.

Session is not done while the frontier still has open decision nodes.

### Step 3: Listen for "want vs. should want"

The most dangerous answers are the ones where the user says what a thoughtful answer *sounds like* rather than what they actually want. Watch for:

- Answers that pattern-match best-practice talk ("I want it to be scalable", "clean architecture") without specifics
- Answers that defer to convention ("the way most apps do it", "the standard approach")
- Phrases like "I should probably…", "I think I'm supposed to…", "good engineering practice says…"
- Buzzwords as goals — when "modern", "scalable", "robust" are the answer instead of a specific outcome

When you hear these, the question to ask is:

> *"If you didn't have to justify this to anyone, what would you actually want?"*

That single question often does more work than the previous five.

### Step 4: Restate intent in the user's own words

When your confidence is high, write back what you now think the user wants. Keep it tight (5–8 lines), use their language where possible, and structure it so the user can confirm or correct line by line:

```
Here's what I now think you want:

- Outcome:      <one line>
- User:         <one line — who benefits>
- Why now:      <one line — what changed>
- Success:      <one line — how we know it worked>
- Constraint:   <one line — the binding limit>
- Out of scope: <one line — what we're explicitly not doing>

Yes / no / refine?
```

Including "Out of scope" is non-negotiable. Half of misalignment is silent disagreement about what is *not* being built.

### Step 5: Confirm — explicit yes, not "whatever you think"

The gate is an explicit "yes." The following are **not** yes:

- "Whatever you think is best." → The user is delegating, which means they don't have 95% confidence either. Re-ask with two concrete options framed as a choice.
- "Sounds good." → Ambiguous. Ask: "Anything you'd refine?" Silence isn't confirmation.
- "Sure, let's go." → Often a polite exit, not an endorsement. Same follow-up.
- Silence followed by "okay let's start." → The user has given up on the interview, not converged. Stop and ask whether you've missed something.

If they correct you, fold the correction in and restate. Loop until you get an explicit yes.

### The 95% Confidence Stop

You're done when you can answer yes to this:

> *Can I predict the user's reaction to the next three questions I would ask?*

If yes, you have shared understanding. Stop interviewing and produce the restate. If no, you're not done; ask the next question.

This is a checkable test, not a vibe. It also has a floor: if you've gone several rounds and still can't predict, that's information about the ask, not a reason to keep grinding. Stop and tell the user: "I've asked X questions and I still can't predict your reactions. Something foundational is missing. Want to step back?"

## Output

The output of this skill is a **confirmed statement of intent**: the restate from Step 4, with an explicit yes from Step 5. That's the deliverable. Specs, plans, and task lists are downstream; they consume the intent this skill produces.

If the user wants the intent to persist (a multi-session project, a handoff to another collaborator), offer to save it to `docs/intent/[topic].md`. Only save if they confirm.

## Example

A short before-and-after.

**Without `interview-me`:**

```
User:  build me a dashboard for our metrics
Agent: <starts proposing chart libraries and layouts>
```

The agent has assumed: who it's for, what metrics, what "for our team" means, what success looks like. None of these are stated. Every assumption is a place the user can later say "that's not what I meant."

**With `interview-me`:**

```
User: build me a dashboard for our metrics

Agent:
HYPOTHESIS: You want a way to answer "how are we doing?" in standup, and "dashboard" came to mind because that's the conventional answer.
CONFIDENCE: ~30% — missing: who it's for, what "metrics" are, and what success looks like

Q:     When you say "how are we doing?", who's asking — you alone, the engineering team in standup, or up the chain (e.g., your manager, an exec, a board)?
GUESS: engineering team in standup, because "we" usually scopes that way and standups are where this question gets asked. If it's for execs the metrics and the framing change a lot.

User: It's actually for me. I keep losing track of which experiments are running and what their early signal looks like.

Agent:
Updated read: not a team dashboard at all. It's a personal experiment tracker. Confidence: ~60% — still missing: what "early signal" means and what done looks like.

Q:     Is the gap that you don't know which experiments exist, or that you can't see their results in one place?
GUESS: the second one. You have a list of experiments somewhere, but their results live in five different tools, and reconciling them by hand is what you're tired of.

User: First one actually. I literally don't have a list. They're spread across different docs.

Agent: <continues>
```

Two questions in, the agent has discovered the actual ask isn't "a dashboard." It's "a list." Different artifact, different scope, different work. The dashboard would have been wrong.

## Interaction with Other Skills

- **`idea-refine`**: downstream. If the confirmed intent is "I want X but I don't know how to scope it," hand off to `idea-refine` to generate variations against the now-explicit intent.
- **`spec-driven-development`**: downstream. If the confirmed intent is concrete ("I want X for Y users with Z success criteria"), hand off to `spec-driven-development` to write it down.
- **`planning-and-task-breakdown`**: two hops downstream of this skill (after the spec).
- **`doubt-driven-development`**: opposite end of the timeline. Interview-me is pre-decision intent extraction; doubt-driven is post-decision artifact review. Both catch divergence, but at different moments.
- **`source-driven-development`**: orthogonal. Interview-me clarifies what the user wants; SDD verifies framework facts. They don't compete.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The ask is clear enough" | If you can't write the user's desired outcome in one sentence right now, the ask isn't clear. Run Step 1 before deciding. |
| "Asking too many questions wastes their time" | Time wasted by 4–6 targeted questions is small. Time wasted by building the wrong thing is enormous, and the user is the one bearing that cost. |
| "I'll figure it out as I build" | Switching costs after code exists are 10x what they are now. Discovery during implementation is rework. |
| "They said 'whatever you think,' so I should just decide" | "Whatever you think" is delegation, not decision. Re-ask with two concrete options as a choice. |
| "I should give them several options to pick from" | Options work when the user knows what they want and is choosing between trade-offs. They don't know what they want yet. Listing options widens the search; asking narrows it. |
| "If I attach my guess, I'm leading them" | Leading is the point. Reacting is faster than generating from scratch. The risk is sycophancy, not leading; mitigate by being visibly willing to be wrong. |
| "We've talked enough, I get it" | Test it: can you predict their reaction to the next three questions? If not, you don't get it yet. |
| "The user said yes, we're done" | If the yes followed a vague restate or an open-ended "sounds good," the yes is hollow. Restate concretely and re-confirm. |

## Red Flags

- Dumping dependent questions in one batch (not a true independent frontier)
- A question without your hypothesis / recommended answer: that's surveying, not committing
- Asking the user for facts you could look up in the repo or tools
- Accepting "whatever you think is best" as a terminal answer
- Producing a spec, plan, or task list before the user has explicitly confirmed your restate
- Questions framed as "what would be best practice?" instead of "what do you actually want?"
- The user gives a sophistication-signaling answer ("scalable", "clean", "modern") and you accept it without probing whether it's what they actually want
- Three or more rounds without your confidence visibly rising: you're asking the wrong questions, step back and reframe
- A confidence number below ~70% with no reason attached: the user can't help close the gap if they don't know what's missing
- Saving the intent doc before the user has confirmed (the doc itself implies a yes the user didn't give)
- Skipping the "Out of scope" line in the restate (silent disagreement about non-goals is half of misalignment)
- Declaring done while independent frontier nodes remain unasked

## Verification

After applying interview-me:

- [ ] An explicit hypothesis with a confidence number was stated in the first turn
- [ ] Every confidence number below ~70% was accompanied by a one-line reason (what's still unresolved or missing)
- [ ] Questions used Mode A (one-at-a-time) or Mode B (independent frontier round) correctly — never dependent multi-asks
- [ ] Every question carried a GUESS / recommended answer
- [ ] Facts were looked up or probed; only decisions went to the user
- [ ] At least one "what would you actually want if you didn't have to justify it?" probe ran when the user gave a sophistication-signaling or convention-signaling answer
- [ ] A concrete restate (Outcome / User / Why now / Success / Constraint / Out of scope) was written back to the user
- [ ] The user confirmed the restate with an explicit yes (not "whatever you think," not "sounds good," not silence)
- [ ] At the stop point, the agent could predict reactions to the next three questions it would ask and the frontier was empty
- [ ] Any handoff to a downstream skill (`idea-refine`, `spec-driven-development`) was framed in terms of the confirmed intent, not the original underspecified ask
