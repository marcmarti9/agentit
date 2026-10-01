---
name: react-composition-patterns
description: >-
  Applies scalable React component composition when an existing component API is becoming
  rigid: boolean-prop proliferation, reusable component libraries, compound components,
  shared provider contracts, explicit variants, or sibling consumers of shared state.
  Do not use for ordinary one-off React feature implementation where direct props/components
  are already simple.
---

# React Composition Patterns

## Purpose

Use composition to repair **demonstrated component API pressure**, not to create architecture preemptively.

This skill is intentionally narrow. General React implementation belongs to the normal frontend workflow; performance belongs to `performance-optimization`.

## Trigger gate

Use this skill when at least one is true:

- a component has accumulated several interacting boolean mode props;
- multiple consumers need different combinations of the same internals;
- a reusable library/component API needs a stable extension seam;
- siblings need coordinated state/actions from one owner;
- a compound-component API clearly improves the caller experience.

If the component has one or two straightforward use cases, keep the direct implementation.

## Patterns

### Prefer explicit variants over boolean mode soup

Instead of:

```tsx
<Dialog compact modal searchable inline />
```

prefer named/composed variants whose valid behavior is obvious to the caller.

A boolean is fine when it represents one genuinely independent binary fact. The smell is many booleans that encode mutually dependent modes.

### Compose capabilities

Expose pieces that callers can combine rather than a giant component that predicts every future layout.

Keep required invariants inside the owning component/provider; leave presentation choices to composition where safe.

### Compound components when parts share a contract

A compound API is useful when several child components participate in one coherent state machine or shared context.

Do not introduce context merely to avoid passing one prop through one level.

### Lift state to the nearest real owner

Move state upward when multiple siblings need the same state/actions.

Keep the provider interface focused on stable state/actions/meta. The provider may hide implementation details, but do not create an abstract state backend unless multiple implementations actually exist.

### Prefer children for structural composition

Use `children` and explicit subcomponents when callers are supplying UI structure.

Render props remain useful when the caller needs computed runtime data to render, not merely to insert markup.

### Version-aware React APIs

Do not assume a React 19 API is available. Inspect the project's actual React version and current official documentation before applying version-specific patterns.

## BUILDER

While implementing:

- solve the demonstrated API problem;
- migrate only the callers required by the task;
- use focused type/tests for the changed contract;
- stop once the caller API is clearer and the requested feature works.

Do not refactor the whole component library because one component changed.

## REVIEW

Check:

- invalid combinations are harder or impossible to express;
- naming communicates variants without reading internals;
- context/provider scope is no broader than necessary;
- state has one clear owner;
- callers are simpler, not merely different;
- no new abstraction exists without at least one current consumer;
- public component contracts have appropriate regression/type coverage.

## Completion criteria

The composition change is justified by a real current pressure, reduces caller complexity, preserves behavior, and introduces no speculative framework.
