# Standards and coverage boundary

Read this reference when a review maps a finding to a normative requirement or
discusses conformance.

Use the current W3C sources, not an upstream skill, for normative claims:

- [WCAG 2.2](https://www.w3.org/TR/WCAG22/) for success criteria and the
  conformance model. Relevant review surfaces commonly include non-text
  content, meaningful sequence, reflow, keyboard, focus order/visibility/not
  obscured, error identification, labels/instructions, name/role/value, and
  status messages.
- [WAI-ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/) when
  a custom composite widget needs an interaction pattern. A named ARIA role
  without the required keyboard/state behavior is not a substitute for native
  controls.
- [Making Content Usable for People with Cognitive and Learning
  Disabilities](https://www.w3.org/TR/coga-usable/) for supplemental cognitive
  inclusion guidance. It does not convert the cognitive branch into a generic
  conformance verdict.

Record the criterion only when the evaluated state and evidence support that
mapping. If a target, process state, browser/device, or assistive-technology
condition is untested, list it as coverage missing. Automated findings and
heuristics help triage; neither replaces manual evaluation or a complete
conformance assessment.
