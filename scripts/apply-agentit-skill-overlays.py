#!/usr/bin/env python3
"""Re-apply Agentit-owned policy overlays onto freshly vendored skill packages.

Canonical upstream copies are 1:1. Agentit still requires adversarial idea
review during non-trivial ideation, so `using-agent-skills` and `idea-refine`
receive a documented overlay after each refresh. Fail loudly if upstream
structure moved enough that the overlay cannot land.
"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


IDEATION_INVARIANT = """### Ideation invariant

For non-trivial idea exploration, **never converge from `idea-refine` straight into a recommendation**. Serious candidate directions must pass through `adversarial-idea-review` first.

The adversarial pass is not generic "list risks" work. It must try to change the answer by attacking, where relevant:

- buyer and user adoption;
- incumbents, substitutes, partners, and copycats;
- implementation and source-of-truth failures;
- support and service burden;
- pricing anchors and unit economics;
- operational failure after the demo;
- scale effects;
- fake/copyable moats;
- evidence quality and kill criteria.

If the attack finds a valid reason to kill, pivot, narrow, re-sequence, change pricing/support boundaries, or concede a segment to a competitor, the final recommendation must reflect it.

"""


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise SystemExit(f"{label}: expected overlay anchor not found")
    return text.replace(old, new, 1)


def overlay_using_agent_skills(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if "Any serious non-trivial candidate? → adversarial-idea-review BEFORE convergence" in text:
        return

    text = replace_once(
        text,
        "    ├── Have a rough concept, need variants? → idea-refine\n"
        "    ├── New project/feature/change? ──→ spec-driven-development\n",
        "    ├── Have a rough concept, need variants? → idea-refine\n"
        "    │   └── Any serious non-trivial candidate? → adversarial-idea-review BEFORE convergence\n"
        "    ├── Exploring an idea/strategy already shaped? → adversarial-idea-review\n"
        "    ├── New project/feature/change? ──→ spec-driven-development\n",
        "using-agent-skills discovery tree",
    )
    text = replace_once(
        text,
        "## Core Operating Behaviors\n",
        IDEATION_INVARIANT + "## Core Operating Behaviors\n",
        "using-agent-skills core behaviors heading",
    )
    text = replace_once(
        text,
        '10. Skipping verification because "it looks right"\n',
        '10. Skipping verification because "it looks right"\n'
        "11. Converging on an attractive non-trivial idea without first trying to kill it\n"
        "12. Running adversarial review as theatre after the recommendation is already fixed\n",
        "using-agent-skills failure modes",
    )
    text = replace_once(
        text,
        "3. **Multiple skills can apply.** A feature implementation might involve `idea-refine` → `spec-driven-development` → `planning-and-task-breakdown` → `incremental-implementation` → `test-driven-development` → `code-review-and-quality` → `code-simplification` → `shipping-and-launch` in sequence.\n",
        "3. **Multiple skills can apply.** A feature implementation might involve `idea-refine` → `adversarial-idea-review` → `spec-driven-development` → `planning-and-task-breakdown` → `incremental-implementation` → `test-driven-development` → `code-review-and-quality` → `code-simplification` → `shipping-and-launch` in sequence.\n",
        "using-agent-skills skill rule 3",
    )
    text = replace_once(
        text,
        "4. **When in doubt, start with a spec.** If the task is non-trivial and there's no spec, begin with `spec-driven-development`.\n",
        "4. **When in doubt, start with a spec.** If the task is non-trivial and there's no spec, begin with `spec-driven-development` — unless the product/strategy direction itself is still under exploration, in which case ideation and adversarial review come first.\n"
        "\n"
        "5. **Exploration is not complete until the serious candidate has survived attack.** For non-trivial ideas, `adversarial-idea-review` is a required gate before recommendation/specification.\n",
        "using-agent-skills skill rule 4",
    )
    text = replace_once(
        text,
        "1.  interview-me                → Extract what the user actually wants\n"
        "2.  idea-refine                 → Refine vague ideas\n"
        "3.  spec-driven-development     → Define what we're building\n"
        "4.  planning-and-task-breakdown → Break into verifiable chunks\n"
        "5.  context-engineering         → Load the right context\n"
        "6.  source-driven-development   → Verify against official docs\n"
        "7.  incremental-implementation  → Build slice by slice\n"
        "8.  observability-and-instrumentation → Instrument as you build (runs parallel with 7-9, not after)\n"
        "9.  doubt-driven-development    → Cross-examine non-trivial decisions in-flight\n"
        "10. test-driven-development     → Prove each slice works\n"
        "11. code-review-and-quality     → Review before merge\n"
        "12. code-simplification         → Reduce unnecessary complexity while preserving behavior\n"
        "13. git-workflow-and-versioning → Clean commit history\n"
        "14. documentation-and-adrs      → Document decisions\n"
        "15. deprecation-and-migration   → Retire old systems and move users safely when needed\n"
        "16. shipping-and-launch         → Deploy safely\n",
        "1.  interview-me                → Extract what the user actually wants\n"
        "2.  idea-refine                 → Expand and refine vague ideas\n"
        "3.  adversarial-idea-review     → Try to kill serious candidate directions before commitment\n"
        "4.  spec-driven-development     → Define what we're building\n"
        "5.  planning-and-task-breakdown → Break into verifiable chunks\n"
        "6.  context-engineering         → Load the right context\n"
        "7.  source-driven-development   → Verify against official docs\n"
        "8.  incremental-implementation  → Build slice by slice\n"
        "9.  observability-and-instrumentation → Instrument as you build (runs parallel with 8-10, not after)\n"
        "10. doubt-driven-development    → Cross-examine non-trivial implementation decisions in-flight\n"
        "11. test-driven-development     → Prove each slice works\n"
        "12. code-review-and-quality     → Review before merge\n"
        "13. code-simplification         → Reduce unnecessary complexity while preserving behavior\n"
        "14. git-workflow-and-versioning → Clean commit history\n"
        "15. documentation-and-adrs      → Document decisions\n"
        "16. deprecation-and-migration   → Retire old systems and move users safely when needed\n"
        "17. shipping-and-launch         → Deploy safely\n",
        "using-agent-skills lifecycle",
    )
    text = replace_once(
        text,
        "| Define | idea-refine | Refine ideas through structured divergent and convergent thinking |\n"
        "| Define | spec-driven-development | Requirements and acceptance criteria before code |\n",
        "| Define | idea-refine | Refine ideas through structured divergent and convergent thinking |\n"
        "| Define | adversarial-idea-review | Try to kill serious ideas via market, adoption, operations, economics, support, competition, scale, moat, and evidence before commitment |\n"
        "| Define | spec-driven-development | Requirements and acceptance criteria before code |\n",
        "using-agent-skills quick reference",
    )
    text = replace_once(
        text,
        "| Build | doubt-driven-development | Adversarial fresh-context review of every non-trivial decision |\n",
        "| Build | doubt-driven-development | Adversarial fresh-context review of every non-trivial implementation decision |\n",
        "using-agent-skills doubt-driven row",
    )
    marker = "Any serious non-trivial candidate? → adversarial-idea-review BEFORE convergence"
    if marker not in text:
        raise SystemExit("using-agent-skills overlay did not land")
    path.write_text(text, encoding="utf-8")


def overlay_idea_refine(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if "before choosing a Recommended Direction" in text and "adversarial-idea-review" in text:
        return

    text = replace_once(
        text,
        "description: Refines raw ideas into sharp, actionable concepts through structured divergent and convergent thinking. Use when an idea is still vague, when you need to stress-test assumptions before committing to a plan, or when you want to expand options before converging on one. Triggers on \"ideate\", \"refine this idea\", or \"stress-test my plan\".\n",
        "description: Refines raw ideas into sharp, actionable concepts through structured divergent and convergent thinking. Use when an idea is still vague, when you need to stress-test assumptions before committing to a plan, or when you want to expand options before converging on one. For every non-trivial idea exploration, pair with adversarial-idea-review before a recommended direction is allowed to stand. Triggers on \"ideate\", \"refine this idea\", or \"stress-test my plan\".\n",
        "idea-refine description",
    )
    text = replace_once(
        text,
        "2.  **Evaluate & Converge:** Cluster ideas, stress-test them, and surface hidden assumptions.\n",
        "2.  **Evaluate, Red-Team & Converge:** Cluster serious directions, run `adversarial-idea-review`, then converge only after the attacks materially inform the choice.\n",
        "idea-refine how it works",
    )
    text = replace_once(
        text,
        "- Recommended Direction\n"
        "- Key Assumptions\n"
        "- MVP Scope\n"
        "- Not Doing list\n",
        "- Recommended Direction\n"
        "- Key Assumptions\n"
        "- Adversarial Findings / Kill Gates\n"
        "- MVP or Minimum Viable Replacement Scope\n"
        "- Not Doing list\n",
        "idea-refine output list",
    )
    if "- Attractive ideas are not exempt from hostile review." not in text:
        text = replace_once(
            text,
            "- The parts you can't see should be as beautiful as the parts you can.\n",
            "- The parts you can't see should be as beautiful as the parts you can.\n"
            "- Attractive ideas are not exempt from hostile review. The more exciting a direction feels, the more important it is to test how reality would kill it.\n",
            "idea-refine philosophy",
        )

    text = replace_once(
        text,
        "#### Phase 2: Evaluate & Converge\n",
        "#### Phase 2: Evaluate, Red-Team & Converge\n",
        "idea-refine phase 2 heading",
    )
    text = replace_once(
        text,
        "1. **Cluster** the ideas that resonated into 2-3 distinct directions. Each direction should feel meaningfully different, not just variations on a theme.\n\n"
        "2. **Stress-test** each direction against three criteria:\n",
        "1. **Cluster** the ideas that resonated into 2-3 distinct directions. Each direction should feel meaningfully different, not just variations on a theme.\n\n"
        "2. **Run the mandatory adversarial gate for non-trivial ideas.** Load and apply `../adversarial-idea-review/SKILL.md` (`adversarial-idea-review`) to the serious candidate directions **before choosing a Recommended Direction**.\n\n"
        "   The red-team must be allowed to change the answer. At minimum, carry back into this phase:\n"
        "   - top ways each direction dies;\n"
        "   - strongest incumbent/substitute attack;\n"
        "   - adoption and operational failure modes;\n"
        "   - support/services or unit-economics traps when relevant;\n"
        "   - what is genuinely defensible vs merely copyable;\n"
        "   - explicit kill/validation gates;\n"
        "   - verdict: `KILL`, `PIVOT`, `PROCEED_WITH_GATES`, or `PROCEED`.\n\n"
        "   Do not append this as ceremonial \"risks\" after selecting a favorite. If the red-team invalidates the favorite, change the recommendation.\n\n"
        "3. **Stress-test surviving directions** against three baseline criteria:\n",
        "idea-refine phase 2 adversarial gate",
    )
    text = replace_once(
        text,
        "3. **Surface hidden assumptions.** For each direction, explicitly name:\n"
        "   - What you're betting is true (but haven't validated)\n"
        "   - What could kill this idea\n"
        "   - What you're choosing to ignore (and why that's okay for now)\n",
        "4. **Surface hidden assumptions.** For each surviving direction, explicitly name:\n"
        "   - What you're betting is true (but haven't validated)\n"
        "   - What could kill this idea\n"
        "   - What evidence would make you stop or pivot\n"
        "   - What you're choosing to ignore (and why that's okay for now)\n",
        "idea-refine assumptions",
    )
    text = replace_once(
        text,
        "**Be honest, not supportive.** If an idea is weak, say so with kindness. A good ideation partner is not a yes-machine. Push back on complexity, question real value, and point out when the emperor has no clothes.\n",
        "**Be honest, not supportive.** If an idea is weak, say so with specificity. A good ideation partner is not a yes-machine. Push back on complexity, question real value, concede when an incumbent is a better fit, and point out when the emperor has no clothes.\n",
        "idea-refine honesty line",
    )
    text = replace_once(
        text,
        "## Recommended Direction\n"
        "[The chosen direction and why — 2-3 paragraphs max]\n\n"
        "## Key Assumptions to Validate\n",
        "## Recommended Direction\n"
        "[The chosen direction and why — 2-3 paragraphs max. It must reflect the adversarial review.]\n\n"
        "## Adversarial Findings\n"
        "- Top way this dies: ...\n"
        "- Strongest substitute/competitor attack: ...\n"
        "- Operational/adoption trap: ...\n"
        "- Support/economics trap: ...\n"
        "- Moat status: real / emerging / hypothetical / none\n\n"
        "## Kill / Validation Gates\n"
        "- [ ] [Gate 1 — falsifiable evidence]\n"
        "- [ ] [Gate 2 — falsifiable evidence]\n"
        "- [ ] [Gate 3 — falsifiable evidence]\n\n"
        "## Key Assumptions to Validate\n",
        "idea-refine one-pager",
    )
    text = replace_once(
        text,
        "## MVP Scope\n"
        "[The minimum version that tests the core assumption. What's in, what's out.]\n",
        "## MVP / Minimum Viable Replacement Scope\n"
        "[The minimum version that tests or replaces the core workflow. What's in, what's out.]\n",
        "idea-refine mvp scope",
    )
    text = replace_once(
        text,
        '**The "Not Doing" list is arguably the most valuable part.** Focus is about saying no to good ideas. Make the trade-offs explicit.\n',
        '**The "Not Doing" and "Kill / Validation Gates" lists are load-bearing.** Focus is about saying no to good ideas, and rigor is about naming what evidence would prove the recommendation wrong.\n',
        "idea-refine not-doing note",
    )
    if "- **Don't choose a favorite before the adversarial gate.**" not in text:
        text = replace_once(
            text,
            "- **Don't ignore the codebase.** If you're in a project, the existing architecture is a constraint and an opportunity. Use it.\n",
            "- **Don't ignore the codebase/project context.** Existing architecture and business constraints are constraints and opportunities. Use them.\n"
            "- **Don't choose a favorite before the adversarial gate.** That turns red-team into rationalization.\n"
            "- **Don't run a weak red-team.** If nothing in scope, sequencing, pricing, GTM, validation, support, or recommendation could possibly change, the attack is probably theatre.\n"
            "- **Don't confuse an anecdote with a market fact.** Preserve the evidence labels from `adversarial-idea-review`.\n",
            "idea-refine anti-patterns",
        )
    if "- Recommending a non-trivial direction without applying `adversarial-idea-review`" not in text:
        text = replace_once(
            text,
            "- Jumping straight to Phase 3 output without running Phases 1 and 2\n",
            "- Jumping straight to Phase 3 output without running Phases 1 and 2\n"
            "- Recommending a non-trivial direction without applying `adversarial-idea-review`\n"
            "- Running the adversarial review after the recommendation is already fixed\n"
            "- Recording attacks but not changing the final direction when the attacks are valid\n",
            "idea-refine red flags",
        )
    if "Every serious non-trivial candidate passed through `adversarial-idea-review`" not in text:
        text = replace_once(
            text,
            "- [ ] Multiple directions were explored, not just the first idea\n"
            "- [ ] Hidden assumptions are explicitly listed with validation strategies\n"
            "- [ ] A \"Not Doing\" list makes trade-offs explicit\n"
            "- [ ] The output is a concrete artifact (markdown one-pager), not just conversation\n"
            "- [ ] The user confirmed the final direction before any implementation work\n",
            "- [ ] Multiple directions were explored, not just the first idea\n"
            "- [ ] Every serious non-trivial candidate passed through `adversarial-idea-review` before final convergence\n"
            "- [ ] The top failure modes, competitor/substitute attack, adoption/operations risk, and economics/support burden were considered where relevant\n"
            "- [ ] Hidden assumptions are explicitly listed with validation strategies\n"
            "- [ ] Falsifiable kill/validation gates exist for material uncertainty\n"
            "- [ ] The recommendation changed if the adversarial findings warranted a change\n"
            "- [ ] A \"Not Doing\" list makes trade-offs explicit\n"
            "- [ ] The output is a concrete artifact (markdown one-pager), not just conversation\n"
            "- [ ] The final direction is suitable to hand to specification work rather than merely sounding exciting\n",
            "idea-refine verification",
        )

    if "before choosing a Recommended Direction" not in text or "adversarial-idea-review" not in text:
        raise SystemExit("idea-refine overlay did not land")
    path.write_text(text, encoding="utf-8")


def main() -> int:
    overlay_using_agent_skills(ROOT / "skills" / "using-agent-skills" / "SKILL.md")
    overlay_idea_refine(ROOT / "skills" / "idea-refine" / "SKILL.md")
    print("Applied Agentit ideation overlays to using-agent-skills and idea-refine.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
