# Contextual reference-use examples

These examples exist to make the intended Agentit behavior concrete. They are not a keyword routing table.

## 1. Tiny repository-local refactor

```text
Task: rename a private helper and update local tests.
Decision: reference_plan.mode = none.
Why: repository-local truth is sufficient; no external/current contract changes.
```

Expected behavior: no web/reference lookup merely for ceremony.

## 2. Public website / landing

```text
Task: redesign a public landing page.
Decision: reference_plan.mode = mixed.
Catalog: web-design-studio.
Live: current framework/component docs where implementation depends on them.
```

Expected behavior: load actual references, extract design DNA/principles, synthesize an original direction, verify implementation in browser, and record durable external influences when material.

## 3. Fiscal report

```text
Task: prepare a current fiscal report for a specific jurisdiction/topic.
Decision: reference_plan.mode = live.
Authority: current legislation + official tax authority/administrative guidance + other primary sources needed for the issue.
```

Expected behavior: do not reuse web/design packs and do not rely on model memory because no `fiscal` Agentit pack exists. Discover current domain-appropriate sources and cite them in the report.

## 4. Current API integration

```text
Task: integrate an authentication provider with the project's current framework.
Decision: reference_plan.mode = live or mixed.
Authority: current official framework/provider docs; Agentit engineering packs only where they add process guidance.
```

Expected behavior: official current API docs establish implementation contracts; Agentit references may influence workflow but do not override official docs.

## 5. Product strategy using a viral creator post

```text
Task: evaluate a business strategy inspired by an X thread.
Decision: reference_plan.mode = mixed.
Role of post: creator claim / inspiration.
Other sources: independent/current market evidence when the claim affects the decision.
```

Expected behavior: extract the idea without promoting creator revenue/pricing/performance claims into facts.

## Invariant

The user should not need to repeat: "remember to use the references." If Agentit is activated, the primary AI must resolve `reference_plan`; the cheap auditor challenges an unjustified `none`; and a non-`none` plan cannot receive a passing verification receipt without inspected-source evidence.
