---
name: local-model-routing
description: Route work to local or remote models by capability tier. Use when local LLMs are available or the user wants local-first execution without silent quality drop.
---

# Local model routing

Local models are first-class. They are not a novelty switch.

Canonical catalog: `models/capabilities.yaml`.

## Core architecture: harness != model

The agent harness owns workflow semantics: task contract, tools, skills, state, approval boundaries, verification and receipts.

The model endpoint is an interchangeable **executor/judgment capability** only after it proves compatibility.

```text
Agentit protocol / harness
        ↓
semantic capability tier
        ↓
provider adapter / endpoint
        ↓
concrete model
```

This separation is intentionally compatible with patterns demonstrated by Claude-Code routers and other provider bridges, without assuming that any text-compatible endpoint has equivalent tool/session behavior.

Never hardcode the operating protocol around one current model name when the requirement can be expressed as a semantic tier/capability.

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
2. Role needs tools → endpoint must support tools/function calling in the **actual harness path**, not merely in a provider demo.
3. Context must fit Worker Context Contract + files.
4. RISK_3/4 critic must not silently use a weak unproven local model — disclose or escalate.
5. Prefer a **different** model family for critic vs writer when possible.
6. If local fails capability check, fall back with explicit note; never fake parity.
7. “OpenAI-compatible” HTTP syntax does **not** imply equivalent tool calls, streaming, structured outputs, reasoning controls, session semantics or stop behavior.
8. Free tiers/provider credits are routing opportunities, not architectural dependencies. Re-check limits before relying on them.

## Compatibility eval before substitution

When adding a new provider/model adapter, benchmark the **workflow**, not only generation quality.

Minimum evaluation matrix:

```text
text correctness
structured output adherence
tool call schema + arguments
multi-tool reliability
long context behavior
state/session continuity
streaming/stop semantics
latency to first useful action
end-to-end task success
critic/review usefulness
cost / quota / rate limits
failure recovery
```

A provider can score well on prose/code benchmarks and still be unusable as an Agentit worker because tool execution or session handling is brittle.

Record the evaluated model/version/provider/date. Do not turn one successful probe into permanent parity.

## Capability check (per machine)

Before relying on a local endpoint for a role:

- can it call tools the task needs?
- does a small probe task succeed (list files / run a test command)?
- is context large enough for projected skills + files?
- does the endpoint preserve the response/tool protocol Agentit expects?
- is latency acceptable for the role?

Record results in STATE or a checkpoint — do not assume yesterday’s model still works.

## Memory capacity != operational throughput

Offload systems can make models runnable by treating disk/RAM/VRAM as a hierarchy and loading only needed weights/experts. This is useful R&D and can unlock capacity, especially for sparse/MoE models.

But **runnable is not the same as operationally useful**.

Evaluate separately:

- model quality;
- memory footprint;
- storage/RAM/VRAM traffic;
- prompt-processing latency;
- tokens/second;
- time-to-first-useful-tool-call;
- end-to-end agent task time;
- power/thermal stability;
- concurrency.

A giant model at 0.x tokens/s may be excellent for an offline experiment and terrible for an interactive coding worker. Route based on measured service-level fitness, not parameter count.

## Model-routing decision record

For a material new endpoint/provider, preserve:

```text
endpoint/provider:
model/version:
role/tier:
why considered:
compatibility evidence:
latency/throughput:
tool support:
known failure modes:
fallback:
recheck trigger:
```

If the choice came from an external reference/tool discovery, `reference-intelligence` should record the source and what was actually adopted vs merely investigated.

## Anti-patterns

- “local always” regardless of tier;
- sending architecture arbitration to a 3B toy model silently;
- assuming OpenAI-compatible transport equals full Agentit/tool parity;
- routing production work because a provider is currently free;
- comparing only tokens/second while ignoring tool/task success;
- using a huge offloaded model simply because it fits in aggregate memory;
- different machines without re-checking endpoints;
- hardcoding one vendor's model names into durable workflow semantics.

## Verification

- [ ] `models` block present in route when local_models.enabled
- [ ] endpoint tiers cover needed roles or gaps disclosed
- [ ] critic independence preserved
- [ ] new adapters passed workflow-level compatibility checks
- [ ] local/offloaded endpoints meet latency/throughput needs for assigned roles
- [ ] provider quota/pricing assumptions are current when they affect routing
