# Observed source-only design critique fixture

## Scope and evidence

This is a source-only critique of the [supplied synthetic HTML fixture](fixtures/design-source-only.html). The binding
purple identity, system sans, and factual heading “Save time” are retained.
Evidence is limited to the supplied HTML/CSS/handler facts: a native
`<button>Learn more</button>`, `<input type=email placeholder=Email>`, no local
label or error association, an async submit handler with no local pending guard,
and CSS animations with no supplied reduced-motion branch. The callback's
implementation is unavailable.

No render, viewport, computed style, keyboard replay, accessibility tree,
screen-reader observation, network response, or performance trace was
available. This report makes no contrast, conformance, FPS, whole-product, or
actual task-completion claim.

| ID | Priority | Source-located finding | Smallest repair direction | Retest |
| --- | --- | --- | --- | --- |
| A11Y-1 | High | The supplied email field has no associated label or error relationship. Placeholder text alone is not the stated label/error contract and can disappear during entry. | Provide a persistent visible email label and associate validation/error text and outcome with the field; preserve the entered address on rejection. | With an empty and malformed email, use keyboard submission and inspect the field name, error announcement/association, focus recovery, and retained value in an actual browser and assistive technology. |
| UX-1 | High | The local async submit handler has no pending guard, disabled state, or local status/error state. The unavailable callback could supply some of these controls, so this is a source-located duplicate-invocation risk, not proof of duplicate orders. | Add or verify one in-flight guard, visible pending/error/success communication, and a recoverable form state without changing approved branding or copy. | Under a delayed success and a rejected request, activate the submit control repeatedly; confirm one intended callback invocation, visible status, preserved input, usable retry, and separately verify server idempotency if an order can result. |
| MOTION-1 | Material | The supplied stylesheet has animation but no reduced-motion branch. The actual motion and preference behavior were not run. | Add a preference-aware branch that removes or simplifies nonessential animation while preserving the state information and control availability. | Test the same checkout states with normal and reduced-motion settings; verify that status, focus, and next action remain clear when animation is simplified or skipped. |

## What to retain

- Keep the approved purple identity and system sans; no source fact justifies a
  brand or typography replacement.
- Keep the factual “Save time” heading. The source-only fixture provides no
  audience/context evidence for a copy rewrite.
- Retain the native button and email input type as useful semantic starting
  points. The missing field relationship and pending-state behavior remain
  separate repairs.

## Coverage limits and follow-up

The generic CTA label may be correct for its unseen destination; it is not
reported as a defect from this fixture. Hierarchy, responsive layout, exact
contrast, focus visibility/order, error announcement timing, animation purpose,
interruption behavior, and runtime cost require a rendered/replayed target.
The source-only findings above are repair directions, not remediation or a
certificate.

## Activation receipt

Activated through `python3 -m router.skills_cli activate` with task
`design-final-review`, stage `source-only-fixture`, and an isolated-worker
context label:

- `design-critique` — `b0b1913d4bbb0694f1cc25fd2e3aad699e11996b1b61d4653074c2a87f0883cb`
- `ux-heuristic-review` — `55a4089d8855aaa6df875a639cc67364626dad6124bb593da7d40a7ef8b59441`
- `accessibility-design-review` — `56f8761d5094a1148ff59ea880e5ec7239ee45f62a9a3df89f540e222fecb0d3`
- `motion-design-review` — `fdb02a4bc6b797451d946fc5d2256b2af2b36c359eb39374b7554ffb5f1f6fbd`

The receipt proves exact body delivery (23,898 bytes), not model compliance,
context erasure, or a rendered evaluation.
