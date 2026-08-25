---
name: local-model-routing
description: Route work to local or remote models by capability tier. Use when local LLMs are available or the user wants local-first execution without silent quality drop.
---

# Local model routing

Local models are first-class. They are not a novelty switch.

Canonical catalog: `models/capabilities.yaml`.

## Tiers

| Tier | Roles |
|---|---|
| judgment | architect, hard tradeoffs |
| coding | primary implementation |
| fast | bounded workers, extraction, QA loops |
| critic | independent review / adversary |

## Preferences

`~/.agentit/preferences.yaml`:

```yaml
local_models:
  enabled: true
  endpoints:
    - id: local-coding
      base_url: http://127.0.0.1:11434/v1
      model: qwen2.5-coder
      tier: coding
      tools: true
      context_tokens: 32768
    - id: local-fast
      base_url: http://127.0.0.1:11434/v1
      model: llama3.2
      tier: fast
      tools: true
      context_tokens: 16000
```

Router output includes `models.parent|worker|critic` with local endpoint matches when enabled.

## Rules

1. Match **tier**, not brand names.
2. Role needs tools → endpoint must support tools/function calling.
3. Context must fit Worker Context Contract + files.
4. RISK_3/4 critic must not silently use a weak unproven local model — disclose or escalate.
5. Prefer a **different** model family for critic vs writer when possible.
6. If local fails capability check, fall back with explicit note; never fake parity.

## Capability check (per machine)

Before relying on a local endpoint for a role:

- can it call tools the task needs?
- does a small probe task succeed (list files / run a test command)?
- is context large enough for projected skills + files?

Record results in STATE or a checkpoint — do not assume yesterday’s model still works.

## Anti-patterns

- “local always” regardless of tier
- sending architecture arbitration to a 3B toy model silently
- assuming Ollama OpenAI compat equals full tool parity
- different machines without re-checking endpoints

## Verification

- [ ] `models` block present in route when local_models.enabled
- [ ] endpoint tiers cover needed roles or gaps disclosed
- [ ] critic independence preserved
