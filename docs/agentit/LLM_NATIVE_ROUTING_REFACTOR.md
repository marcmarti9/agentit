# Agentit LLM-native routing refactor

## Goal

Remove prompt-keyword semantic routing from Agentit and make the active LLM the
mandatory classifier, while retaining deterministic safety validation.

## What changed

- `router/route.py` no longer infers risk/category/topology from natural language.
- `router/decision_contract.py` defines the structured host-model decision contract.
- `router/registry.py` verifies model-selected skill availability without selecting skills.
- `task-router` is now an LLM decision protocol rather than a regex router.
- `using-agentit` and `AGENTS.md` require the model to classify every task from full context.
- traces distinguish `decision_request` from `validated_decision`.
- evals now test hard decision invariants, not prompt-classifier heuristics.

## Non-goal

This does not remove routing as a concept. It moves semantic routing to the model
and leaves code responsible only for stable, testable invariants and inventory.
