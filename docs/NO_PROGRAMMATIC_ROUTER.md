# No programmatic router

Agentit intentionally does not implement natural-language routing in Python, shell, regexes, scoring tables, or another deterministic classifier.

The **primary model** reads the full task context and owns the semantic `TASK_DECISION`: intent, category/domain, complexity, risk, topology, skills, tools, delegation, execution plan and verification strategy.

A second cheap AI is used only as a bounded, read-only **auditor** of that proposal. It looks for omissions, contradictions, underestimated risk and reasons to escalate. It does not become the router and does not issue an authoritative replacement decision.

If the cheap audit finds material disagreement, or if the task is `RISK_3/RISK_4`, destructive, hard to reverse, security/auth/payment/PII/production sensitive, or structurally large, a stronger independent `critic`/`judgment` model reviews the primary decision and acts as the independent judgment gate before material execution.

Code may still perform mechanical operations after the decision (copy files, persist manifests/runtime state, run tests, enforce file ownership, invoke selected tools). Mechanical utilities must not reinterpret the prompt or choose semantic category, risk, topology, skills, or delegation from natural-language keywords.

The architecture boundary is:

> **Primary AI decides; cheap AI audits; strong AI arbitrates when needed; software performs mechanical operations afterward.**

Canonical protocol: `skills/task-router/SKILL.md`.

Canonical economy audit contract: `skills/task-router/references/economy-reviewer.md`.
