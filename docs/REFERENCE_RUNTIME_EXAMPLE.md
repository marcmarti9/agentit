# Runtime reference gate example

A web task may produce:

```text
reference_plan.mode = mixed
sources = [web-design-studio, https://react.dev/...]
```

The agent must then pass those explicit values into verification and provide compact evidence of what it inspected. Without that evidence, the apply receipt fails.

A local refactor may produce:

```text
reference_plan.mode = none
```

and no reference evidence is required.

This behavior is intentional: contextual references, not mandatory browsing.
