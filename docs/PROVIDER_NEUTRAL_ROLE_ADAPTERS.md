# Provider-neutral semantic roles

Agentit separates **semantic capabilities** from **host-native role adapters**.

The semantic capability is the contract. A provider-specific agent file, worker profile or subagent format is only an optional execution binding.

## Architect / orchestrator rule

`architect-orchestrator` is a JIT Agentit skill and must be available from the shared Agentit runtime regardless of whether the host is Claude Code, Codex, Antigravity/Gemini or another supported capable agent.

It is deliberately **not** part of global core. Every fresh session still begins with exactly:

```text
using-agentit
+ task-router
+ using-agent-skills
```

When a task genuinely needs structural decomposition, architecture ownership or multi-stage coordination, the primary AI may select `architect-orchestrator` from the shared runtime. The host can then execute that contract in the parent or project it into a bounded host-native worker if doing so is useful.

## No provider-only semantic bonus

A default installation must not make Claude Code semantically stronger by automatically installing `architect.md`, `orchestrator.md` or equivalent business/engineering roles only into `.claude/agents`.

Likewise, Agentit should not compensate by inventing fake cross-provider files whose formats are not actually supported by those hosts.

The portable contract is:

```text
shared Agentit runtime
  -> semantic pack discovery
  -> selected skill body
  -> optional host-native worker binding
```

not:

```text
Claude-specific semantic agent hierarchy
  -> other providers get less capability
```

## Host-native workers are still allowed

Provider-specific workers may exist when they express a real host capability, model choice or execution optimization. For example, Codex model-worker profiles can remain host-specific when their purpose is model/execution routing rather than defining a capability that other providers are denied.

A provider binding must degrade to an equivalent parent/worker execution using the same selected Agentit skill bodies when the preferred native mechanism is unavailable.

## Existing legacy Claude adapters

Older Agentit installations may already contain exact copies of legacy role adapters under `.claude/agents`.

New installs no longer project those semantic role adapters to Claude by default. Agentit does not silently delete existing host files during an upgrade because those files may have been modified by the user or another tool. Treat such existing files as legacy host configuration, not as canonical Agentit activation.

If cleanup is desired, only remove a legacy adapter after verifying that it is still an Agentit-managed/unmodified copy or after explicit user review.

## Regression contract

CI should enforce that:

- `architect-orchestrator` is packaged in the shared runtime for every supported provider install plan;
- provider-global skill projection remains the three-skill core;
- Claude receives no default semantic `agents/*.md` hierarchy;
- provider-specific execution helpers do not redefine Agentit's semantic capability model.
