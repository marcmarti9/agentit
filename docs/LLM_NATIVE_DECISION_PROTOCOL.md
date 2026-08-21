# LLM-native decision protocol

Agentit no longer tries to understand natural-language tasks with a deterministic
keyword/regex router.

The host model owns semantic classification because it has the information that
a standalone prompt classifier does not: conversation history, repository state,
project instructions, available tools, previous decisions and the actual user
intent behind follow-ups.

## Architecture

```text
user task + full context
        ↓
host LLM decision (mandatory rubric)
        ↓
structured decision when useful
        ↓
deterministic contract validation
        ↓
skill/capability availability checks
        ↓
Loop / Graph runtime
        ↓
execution
        ↓
verification + receipts
```

The old architecture inverted those responsibilities by asking Python to infer
risk/category/topology from prompt strings before the model reasoned about the
task.

## Ownership boundary

The host LLM decides:

- intent and category;
- risk and reversibility;
- topology and delegation benefit;
- domain pack and skill relevance;
- specialists and capability needs;
- public-visual/design classification;
- verification strategy;
- whether a critic is required.

Python validates facts that do not require language understanding:

- schema/enums/types;
- explicit risk floors;
- RISK_3/4 review gates;
- RISK_4 operational gates;
- destructive-data backup rule;
- structural critic rule;
- fan-out consistency;
- public-visual design/browser invariants once the model has identified the surface;
- registry skill availability;
- capability-provider availability.

## Files

- `skills/task-router/SKILL.md` — mandatory model decision rubric.
- `skills/using-agentit/SKILL.md` — end-to-end Agentit playbook.
- `router/decision_contract.py` — structured decision schema + hard invariants.
- `router/registry.py` — deterministic registry validation/skill availability.
- `router/route.py` — compatibility adapter; **not a semantic router**.
- `evals/run.py` — deterministic contract regressions, not language-classifier benchmarks.

## Compatibility behavior

Historical callers may still invoke:

```bash
python3 router/route.py "Implement auth"
```

The command now returns a `decision_required` envelope containing the task,
protocol, preferences and deterministic project facts. It deliberately omits
inferred `risk`, `category` and `topology`.

A provider adapter can validate a model-produced decision with:

```bash
python3 router/route.py --decision decision.json
```

The active agent normally does not need to call the compatibility CLI just to
reason; it should apply the `task-router` skill directly.

## Why this is safer

A deterministic prompt router tends to grow exception trees for phrases such as
“delete button”, “backup service landing”, “explain payments”, or context-free
follow-ups like “fix it”. That is a brittle attempt to reproduce language
understanding manually.

The LLM-native design keeps semantic judgment where context exists while keeping
hard safety invariants deterministic and testable.

## Testing philosophy

CI no longer asserts that a regex tree classifies English/Spanish prompts into a
specific route. It asserts that:

- natural-language adapters do not invent a classification;
- valid structured decisions pass;
- unsafe/inconsistent decisions fail closed;
- registry and capability checks remain deterministic;
- existing runtime/verification/profile infrastructure still works.
