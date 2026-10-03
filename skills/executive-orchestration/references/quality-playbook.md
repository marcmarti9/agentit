# Executive decision quality playbook

Read this only when an executive decision crosses functions, has a material budget or irreversible consequence, or needs an evidence-backed recommendation rather than a single-domain answer. It supplements `executive-orchestration`; it does not activate specialists or authorize action.

## Produce a decision packet before convening specialists

Write the decision as a falsifiable packet. This prevents a cross-functional review from becoming a collection of generic opinions.

```text
decision and deadline:
company facts already verified:
customer / market context:
constraint (cash, capacity, contract, timing, risk):
options, including defer / do nothing where genuine:
decision owner and required approver:
what a good outcome looks like and by when:
critical uncertainty that could reverse the choice:
```

Mark every statement as a company fact, current external fact with source/date, estimate, heuristic, or specialist judgment. A decision packet without a decision owner or a reversal condition is not ready for executive synthesis.

## Select questions, not titles

Add a specialist only when its answer could change the recommendation. Give each selected specialist one bounded question, the relevant facts, the assumption it should challenge, and an expected handoff:

```text
question:
facts supplied:
assumption to test:
constraints / authority boundary:
return: recommendation, evidence, trade-off, dependency, reversal signal
```

Examples: Product tests whether the customer problem and adoption evidence earn the investment; Marketing tests ICP, alternative, message and channel economics; Finance tests cash exposure and downside; Operations tests delivery capacity. A role name alone is not a useful delegation contract.

## Reconcile a real disagreement

When specialist conclusions conflict, do not average them or present a committee transcript. Make a small reconciliation table:

| Claim | Evidence / assumption | What would settle it | Decision effect |
| --- | --- | --- | --- |
| Product says adoption is likely | interviews from one segment | prototype test with target buyers | proceed only if validated |
| Finance says payback is unsafe | conversion and margin estimate | downside cash model | cap exposure or defer |

The accountable executive chooses after identifying which assumption is decisive. If it cannot be tested before the deadline, choose the smallest reversible action that preserves the option, or explicitly escalate the unresolved risk.

## Decision output and follow-through

The final recommendation should state one direction, why it wins now, what is deliberately excluded, owner/approver, first action, exposure limit, success signal, review date and kill/reshape condition. Preserve the decision and the evidence needed to reassess it in the project’s canonical business record when that record is in scope.

Do not claim that a model, a specialist persona, or an elegant framework independently validated the decision. Quality comes from the evidence, the explicit trade-off and the observed follow-through.

## Source-informed adaptation

- **Source:** [SenteLabsAI/OpenExecutive](https://github.com/SenteLabsAI/OpenExecutive/tree/bba990f20dab7559967010e65b65630f1a35c684), especially its domain prompts and scenario-based executive evals.
- **Role:** licensed artifact and inspiration for bounded specialist questions, coherent synthesis and scenario expectations.
- **Observed:** its CMO/CPO prompts require customer/problem framing, prioritised recommendations, explicit sequencing and a named risky assumption; its `marketing_001` and `product_001` scenarios check whether an answer addresses the actual motion/trade-off rather than merely naming a framework.
- **Decision changed:** this reference adds the decision packet, claim-reconciliation table and reversal signal to the existing orchestration owner.
- **Not imported:** OpenExecutive’s runtime, personas, model configuration, benchmark thresholds, database/UI architecture or prompt wording.

OpenExecutive is Apache-2.0. This is an original adaptation, not a vendored copy. Its exact Apache-2.0 license and NOTICE are distributed with this adaptation.

Distribution attribution and exact source licenses are retained in `THIRD_PARTY_NOTICES.md`, `skills/ADAPTATION_SOURCES.json` and `vendor/adaptation-licenses/`. This reference is an Agentit-authored adaptation; it does not include upstream runtime/scripts.
