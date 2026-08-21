# No programmatic router

Agentit intentionally does not implement natural-language routing in Python, shell, regexes, scoring tables, or another deterministic classifier.

The primary model reads the full task context and creates a `TASK_DECISION`. Before material execution, a second AI reviews that decision. Ordinary preflight review should use the cheapest capable model/endpoint available; high-consequence work additionally escalates to a stronger critic/judgment model.

Code may still perform mechanical operations after the decision (copy files, persist manifests/runtime state, run tests, enforce file ownership, invoke selected tools). Mechanical utilities must not reinterpret the prompt or choose semantic category, risk, topology, skills, or delegation from natural-language keywords.

Canonical protocol: `skills/task-router/SKILL.md`.

Canonical economy reviewer contract: `skills/task-router/references/economy-reviewer.md`.
