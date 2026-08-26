# Agentit public launch package

This document is the working launch brief for introducing Agentit publicly without making claims ahead of evidence.

## Positioning

### One sentence

Agentit is an open-source, provider-neutral reliability and just-in-time expertise layer for capable AI coding agents.

### Short explanation

Agentit sits around an existing coding agent and gives it a compact operating protocol for material work: task-specific skills and references, independent decision review, bounded delegation, resumable project state, MCP/capability selection, Loop/Graph execution contracts, fresh verification and reviewable Git delivery.

### Core message

```text
Keep the agent capable.
Keep startup context tiny.
Load expertise only when the task earns it.
Make material execution inspectable and verifiable.
```

### Primary audience

- developers already using coding agents such as Claude Code, Codex or similar tools;
- people building serious workflows around agentic coding;
- developers interested in context engineering, MCP, multi-agent orchestration and agent reliability;
- open-source contributors working on agent tooling.

### Proof available at launch

Public claims can point to implemented repository facts:

- three-skill global bootstrap with JIT skill selection;
- model-owned `TASK_DECISION`;
- independent decision-audit contract;
- flat semantic skill packs;
- curated/live Reference Intelligence;
- Loop and Graph runtime contracts with receipts;
- project continuity and checkpoints;
- provider-neutral capability resolution and least-privilege envelopes;
- MCP catalog/runtime;
- reversible portable bootstrap;
- deterministic CI coverage;
- public paired-evaluation plan in issue #29.

Performance/quality claims should use measured paired-agent evidence once those runs exist.

## Launch sequence

### Wave 0 — repository ready

Before sending meaningful traffic:

- merge the public-launch README after review and green CI;
- verify the top of the README explains Agentit within one screen;
- verify installation instructions from a clean macOS/Linux environment through CI/current evidence;
- keep issue #29 visible as the public benchmark/evidence tracker;
- make sure repository description/topics remain aligned with the README;
- verify all public links in the launch copy.

### Wave 1 — technical founder launch

Publish the same factual thesis in channel-native forms:

1. X: short launch post or thread;
2. Reddit: discussion-first technical post in communities where agent frameworks/tooling are already discussed;
3. LinkedIn: concise engineering/founder explanation;
4. GitHub: release/changelog note once the launch README is merged;
5. Hacker News: founder-written Show HN text only when current HN submission conditions allow it.

### Wave 2 — evidence

When the first paired evaluations exist, publish the raw task pair and acceptance evidence rather than only a summary number.

Useful follow-ups:

- one paired bug-fix run;
- one security-sensitive run;
- one multi-session continuity run;
- what the independent audit changed;
- cases where Agentit added overhead without enough benefit and what was simplified because of it.

### Wave 3 — build in public

Turn real repository changes into technical posts:

- architecture decisions;
- benchmark results;
- protocol-tax removals;
- new provider/MCP support;
- contributor PRs;
- failures and the resulting design changes.

## X launch copy

### Single-post version

I built Agentit: an open-source reliability layer for AI coding agents.

It sits around capable agents and adds JIT skills/references, independent decision review, bounded workers, resumable state, MCP/capability selection, and verifiable Loop/Graph execution.

Provider-neutral. Apache-2.0.

https://github.com/marcmarti9/agentit

### Thread version

**1/**

I built Agentit: an open-source reliability + JIT expertise layer for AI coding agents.

The goal is simple: let capable models keep semantic control, then give material work better context, review, state and verification.

https://github.com/marcmarti9/agentit

**2/**

The global Agentit core is deliberately tiny:

```text
using-agentit
task-router
using-agent-skills
```

Everything deeper is loaded only when the active model decides the task needs it.

**3/**

Skills are exposed through semantic domain packs — engineering, design, frontend, backend, research, marketing, etc.

The pack is only a map. The model chooses the actual skill bodies and how many are worth loading into context.

**4/**

Material tasks can also get:

- curated/live Reference Intelligence;
- an independent decision audit;
- bounded specialist context;
- least-privilege capabilities and MCPs;
- resumable state/checkpoints.

**5/**

Execution can be bound to Loop/Graph contracts:

```text
goal → action → fresh evidence → verifier → accept/retry/escalate
```

Multi-agent work gets explicit dependencies, ownership, handoffs and receipts.

**6/**

I am also keeping the evaluation claims evidence-gated.

The repo has deterministic runtime tests and a public plan for paired real-agent runs: same model/environment, baseline vs Agentit.

Issue #29 tracks that work.

Apache-2.0. Feedback and PRs welcome.

https://github.com/marcmarti9/agentit

## Reddit

Reddit posts should lead with the technical problem and invite criticism rather than read like an ad.

### r/LocalLLaMA angle

**Suggested title:**

`I built a provider-neutral reliability/JIT context layer for coding agents — looking for architecture feedback`

**Draft:**

I have been building Agentit, an Apache-2.0 project that sits around capable coding agents rather than owning model inference itself.

The main idea is to keep startup context extremely small and let the active model choose extra expertise only when the task warrants it.

Current pieces include:

- a three-skill global bootstrap;
- semantic domain packs used only for discovery;
- JIT skill/reference loading;
- independent review of material task decisions;
- bounded worker contexts;
- Loop/Graph execution contracts with receipts;
- continuity/checkpoints across sessions;
- provider-neutral capabilities and MCP runtime support.

The semantic boundary is intentional: the LLM interprets the task; deterministic code manages state, capabilities, DAG/loop invariants and verification receipts.

I am now starting paired real-agent evaluations against a bare-agent baseline instead of assuming the extra protocol is beneficial everywhere. The evaluation plan is public in the repo.

Repo: https://github.com/marcmarti9/agentit

I would especially like criticism on where this adds useful reliability versus where you think the protocol tax is unnecessary.

### Coding-agent community angle

**Suggested title:**

`Open-sourced the reliability layer I use around coding agents: JIT skills, independent review, resumable state and execution receipts`

**Draft:**

I have open-sourced Agentit, a provider-neutral operating layer for capable coding agents.

A material task is handled roughly as:

```text
task
→ semantic decision by the primary model
→ JIT skill/reference/tool selection
→ independent decision audit
→ bounded direct/multi-agent execution
→ fresh verification receipts
→ resumable state + reviewable Git handoff
```

The interesting design choice is that Python never tries to classify natural-language task intent. Semantic choices remain with the model; the runtime only enforces explicit mechanical contracts.

I am looking for people willing to break the assumptions, try it on real repositories, or contribute paired baseline-vs-Agentit evaluations.

https://github.com/marcmarti9/agentit

## LinkedIn

I have open-sourced Agentit, a provider-neutral reliability layer for AI coding agents.

The project is built around a simple design constraint: keep startup context tiny and load deeper expertise only when the task actually needs it.

For material work, Agentit can give the active coding agent task-specific skills and references, independent decision review, bounded specialist contexts, resumable state, MCP/capability selection, and Loop/Graph execution contracts backed by fresh verification receipts.

The LLM keeps semantic judgment; deterministic code handles state and execution invariants.

The repository is Apache-2.0, and the next phase is empirical: paired runs against the same agent without Agentit, with the raw evaluation plan public in the repo.

https://github.com/marcmarti9/agentit

## Hacker News

Current HN guidance should be checked again immediately before submission. HN moderators currently ask users not to post AI-generated or AI-edited submission/comment text, and Show HN submissions are being moderated more selectively.

Do **not** copy generated launch prose from this document into HN.

When writing the submission yourself, cover these factual points in your own words:

- what Agentit is;
- why you started building it;
- that it works around capable coding-agent hosts instead of owning model inference;
- tiny global bootstrap + JIT expertise;
- model-owned semantic decisions;
- Loop/Graph deterministic execution contracts;
- resumable state/capability/MCP support;
- what people can try immediately;
- what is currently measured;
- that paired agent-level evaluations are the next evidence step;
- exactly what kind of technical criticism you want.

Keep the tone technical and factual. The useful HN discussion is architecture and trade-offs, not launch copy.

## GitHub release note draft

### Agentit — public architecture launch

Agentit is now ready for broader public testing as an open-source provider-neutral reliability and JIT expertise layer for capable AI agents.

This release surface includes:

- tiny three-skill global bootstrap;
- agent-owned `bare | agentit` dispatch and `TASK_DECISION`;
- flat semantic JIT skill packs;
- curated/live Reference Intelligence;
- independent decision audit and risk escalation;
- bounded worker-context projection;
- Loop/Graph execution contracts and verification receipts;
- resumable project state/checkpoints;
- provider-neutral capabilities and MCP management;
- portable reversible bootstrap for macOS and GNU/Linux;
- deterministic CI and a public paired-agent evaluation plan.

The next public milestone is real paired evidence comparing the same agent/environment with and without Agentit.

## Demo/evidence assets

### Demo 1 — context selection

Show one real task where the global context starts with only the three-skill core, then capture:

1. selected semantic pack(s);
2. selected skill bodies;
3. reference mode;
4. final bounded worker context.

The useful visual is the difference between everything Agentit *has available* and the small subset actually projected into the task.

### Demo 2 — verifiable execution

Use a real bounded bug or feature and capture:

```text
TASK_DECISION
→ independent audit
→ Loop Contract
→ failed/passed evidence if applicable
→ receipt
→ PR
```

Keep the entire chain inspectable from repository artifacts.

### Demo 3 — paired evaluation

Run the exact same real task twice:

```text
A: provider defaults + project instructions
B: same model/provider/version/environment + Agentit
```

Publish raw acceptance evidence first, then the comparison. Do not change tools, prompt, starting revision or acceptance criteria between arms.

## Distribution rules

- One product truth, adapted to each channel.
- Lead with architecture or evidence, not superlatives.
- Link directly to the repository.
- Ask for a specific kind of feedback.
- Reply technically to criticism and turn recurring objections into docs/evals/issues.
- Do not treat stars/views as proof of reliability.
- Do not generalize from one successful benchmark.

## Metrics

Track launch distribution separately from product evidence.

### Distribution

- repository unique visitors/clones if available;
- stars/forks/watchers;
- issue/PR quality;
- external mentions;
- post impressions and profile/repo clicks;
- number of people who actually install/try it when observable.

### Product evidence

- paired task acceptance;
- regressions;
- retries/failed tool calls;
- model calls and exposed token use;
- elapsed time;
- user interventions;
- verifier evidence quality;
- documentation drift;
- whether independent review materially changed the outcome.

## Launch decision

The repository can be introduced publicly on architecture and implemented capabilities now. Strong comparative claims belong to the paired-evaluation phase.
