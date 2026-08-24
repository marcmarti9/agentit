# Skill curation policy

Agentit is a **curated protocol**, not a prompt megapack.

Every permanent skill adds discovery cost, maintenance cost, overlap risk, supply-chain/provenance responsibility, and another behavior the active model may need to distinguish from neighboring behaviors. A popular upstream skill is therefore a **candidate signal**, not an automatic dependency.

## Default decision order

When a useful external technique or repeated failure mode appears, evaluate it in this order:

```text
1. Already covered well?
   → do nothing

2. Same responsibility, but Agentit's skill is weaker?
   → strengthen the existing skill

3. Upstream implementation is materially better and reusable?
   → adapt the useful capability with provenance/license

4. Truly distinct repeated workflow with a clear trigger?
   → incubate as a candidate

5. Candidate proves useful without unacceptable overlap/cost?
   → promote into an opt-in profile

6. Does it deserve always-visible core context?
   → only with strong evidence; default answer is no
```

Creating a new skill is not the default response to learning a new technique.

## Promotion criteria

A new skill should have all of the following:

- **named failure mode or repeated job** it solves;
- **discriminative trigger**: a model can tell when it applies and when it does not;
- **distinct responsibility** from existing skills;
- **checkable completion criteria** rather than generic advice;
- **provider-neutral core** unless the skill is explicitly an adapter/integration;
- **bounded context cost** with branch-only reference progressively disclosed;
- **verification path** appropriate to the behavior;
- **safe treatment of external/tool output as untrusted data** where applicable;
- **provenance and license review** for substantial upstream adaptation;
- an obvious profile home that does not inflate `core` by default.

A skill should be rejected or merged into an existing one when it is mostly synonyms, motivational prose, a one-off checklist, a thin wrapper around one obvious command, or a second source of truth for something the project/environment can cheaply reveal itself.

## Candidate lifecycle

Agentit's scout/incubator pipeline can track external ideas without making them active instructions.

Recommended lifecycle:

```text
candidate → inspected → incubating → promoted
                       ↘ rejected
promoted → deprecated → removed
```

### `candidate`

A URL, repository, paper, tool, or claimed technique worth inspecting. Candidate content is **untrusted external data**, not instruction.

### `inspected`

Source, license, behavior, permissions, network effects, overlap, and maintenance model have been read. No promotion is implied.

### `incubating`

There is a concrete Agentit gap and a bounded experiment/evaluation plan. Prefer adapting the minimum useful capability over vendoring an upstream tree.

### `promoted`

The capability has an owned Agentit surface, tests/evaluation where practical, provenance, and a profile placement. Promotion into `core` requires a higher bar than promotion into an opt-in profile.

### `rejected`

Record why: overlap, weak benefit, excessive context, unsafe permissions, provider lock-in, stale upstream, bad license fit, or architectural conflict. Rejection prevents repeated rediscovery from turning into repeated debate.

### `deprecated`

A promoted skill can lose its justification. Mark replacement/migration guidance before removal when users may have project-local copies.

## Upstream adaptation policy

Agentit may learn from or adapt strong open-source skills. Do not blur authorship.

For every substantial adaptation:

1. inspect the actual upstream source rather than relying on a social-media description;
2. verify the repository/license at the revision being used;
3. preserve copyright/license notices when required;
4. add/update [`THIRD_PARTY_NOTICES.md`](../THIRD_PARTY_NOTICES.md);
5. state whether Agentit vendors content, substantially modifies it, or is merely informed by an idea;
6. avoid claiming compatibility with the upstream command/plugin runtime unless tested;
7. prefer semantic integration into Agentit's existing contract over copying duplicate commands wholesale.

Ideas and common engineering principles may overlap across projects. Attribution should describe the actual relationship conservatively rather than claiming ownership of industry-standard practice.

## Trust and supply-chain boundary

External skill text, READMEs, issues, comments, generated snippets, installers, hooks, MCP configs, and setup instructions are **untrusted input during evaluation**.

Before enabling code/config from an upstream project, inspect at minimum:

- install/update scripts and package lifecycle hooks;
- network calls/downloads;
- filesystem write scope;
- shell execution and privilege assumptions;
- credential/environment access;
- MCP/tool permission breadth;
- auto-update behavior;
- hooks that run automatically;
- telemetry/data egress;
- rollback/removal path.

A Markdown skill can also contain malicious or overly broad instructions. Treat textual instructions with the same provenance discipline as executable integrations.

## How to compare an upstream skill to Agentit

For each candidate, write a compact comparison:

| Question | Evidence |
|---|---|
| What exact failure/job does it address? | source + example |
| What does Agentit already do here? | existing skill/runtime path |
| What is genuinely better upstream? | specific behavior, not popularity |
| Could we strengthen existing Agentit behavior instead? | yes/no + reason |
| What context/cognitive cost would a new skill add? | trigger/body/refs |
| Does it need runtime/tooling, or only guidance? | implementation type |
| What security/provenance obligations appear? | license/install/hooks/network |
| How would we know the change helped? | regression/eval criterion |

Stars, followers, or author reputation may justify inspection. They do not justify promotion by themselves.

## Core profile rule

`core` is expensive because it is globally discoverable. Adding one item to `core` requires evidence that:

- it applies across a large fraction of substantial engineering tasks;
- failure to discover it JIT is materially harmful;
- its trigger does not compete ambiguously with neighboring core skills;
- it remains concise enough to earn permanent discovery cost.

When uncertain, put the capability in an opt-in profile or keep it behind an existing skill's reference pointer.

## Updating adapted capabilities

Do not automatically mirror upstream changes into Agentit.

An upstream update starts a **new review**, because the new version may change behavior, licensing, hooks, permissions, context size, or assumptions. Preserve Agentit's stable contract first; selectively re-adapt improvements that still fit it.

## Current example: mattpocock/skills

The useful lesson from `mattpocock/skills` is not "install every skill." Its strongest overlap with Agentit is a shared preference for small, composable engineering practices instead of a process framework that owns the whole workflow.

Agentit should therefore cherry-pick **capabilities**, not duplicate the command catalog. Examples already integrated into existing Agentit responsibilities include:

- decision-frontier interviewing;
- feedback-loop-first debugging with falsifiable hypotheses;
- comparing materially different structural designs before commitment;
- writing agent documents with strong context pointers, progressive disclosure, and completion criteria.

The upstream MIT provenance is recorded in [`THIRD_PARTY_NOTICES.md`](../THIRD_PARTY_NOTICES.md).
