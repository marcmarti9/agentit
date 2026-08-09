# Agentit

[![CI Status](https://github.com/marcmarti9/agentit/actions/workflows/ci.yml/badge.svg)](https://github.com/marcmarti9/agentit/actions)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Release](https://img.shields.io/badge/version-v0.3.2--stable-green.svg)](https://github.com/marcmarti9/agentit/releases)

> **Agentit is a portable, provider-neutral meta-harness for interviewing, routing, coordinating, and verifying AI coding agents.**
>
> Efficient by default. Quality-first when the user explicitly chooses to spend more effort.

Agentit keeps shared behavior semantic and portable across **OpenAI, Anthropic, Google, xAI, and other compatible coding-agent environments**. Provider-specific subagents/workers are optional execution primitives, not correctness dependencies.

---

## One-phrase usage

Tell the coding agent:

```text
usa agentit
```

or pair it with work:

```text
usa agentit y haz mi portfolio personal
```

For product-affecting work Agentit does **not** immediately start coding. The flow is:

```text
request
  ↓
mechanical chore? ── yes → execute directly
  │ no
  ↓
interview
  ↓
recommend + confirm effort level
(Standard / Polished / Studio)
  ↓
route + skills + optional specialists
  ↓
implement
  ↓
verify
```

The interview can be one short confirmation for a tiny clear change, or a deeper discovery process for an open-ended product/design/architecture task.

---

## Adaptive effort levels

Canonical policy: [`effort/levels.yaml`](effort/levels.yaml).

Every product-affecting task chooses an effort level during the interview. The agent must **recommend** a level, explain what the result will look like, give a rough token estimate, and let the user confirm or override it.

| Level | What it optimizes for | Rough total model tokens* | Typical behavior |
|---|---|---:|---|
| **Standard** | efficiency + production quality | **~15k-80k** | one agent by default, minimal research, focused implementation, proportional QA |
| **Polished** | visibly stronger quality | **~50k-250k** | targeted research, approach comparison when useful, 0-2 specialists, more edge-case/visual polish and iteration |
| **Studio** | best reasonable result | **~150k-800k+** | deep discovery, broad relevant research, concept exploration, specialists/model diversity, independent critique, extensive polish |

\* Rough total-session envelopes across parent + delegated model calls. They are not billing guarantees; provider, model, context, retries, tools, and task size can move them substantially.

### What the interview should say

A good effort question looks like this:

```text
EFFORT RECOMMENDATION: Polished

Why: this is public-facing and worth extra craft, but the concept is already clear enough that a full Studio exploration is probably wasteful.

Standard (~15k-80k): clean/correct, limited exploration and polish.
Polished (~50k-250k): targeted research, stronger responsive/edge-case QA, more iteration. <- recommended
Studio (~150k-800k+): multiple concepts/specialists and much deeper critique; probably overkill here.

Which level do you want?
```

The agent should not silently turn Standard into a 400k-token multi-agent research session. If new complexity materially changes the budget/value tradeoff, it asks before escalating.

**Correctness and safety are never downgraded by effort level.**

---

## Interview-first product work

[`skills/interview-me/SKILL.md`](skills/interview-me/SKILL.md) is now the normal gate for any task that creates or changes a meaningful product decision: features, pages, components, UX, visual design, architecture, APIs, data models, workflows, copy, positioning, automations, or refactors with materially different valid outcomes.

The interview is adaptive:

- clear tiny product change → one short confirmation may be enough;
- one unresolved decision → ask it + effort level;
- several independent decisions → one frontier round;
- open-ended product/design/architecture → interview until the meaningful decision frontier is closed.

Facts are the agent's job: inspect repo/docs/tools/live sources. The user should be asked for decisions, preferences, tradeoffs, and success criteria.

### Mechanical bypass

Interview may be skipped only for exact chores that save time **without choosing product behavior**, for example:

- create explicitly named directories/files;
- exact move/rename;
- run an explicitly requested test/command;
- deterministic formatting;
- copy exact content to a known destination.

`Add a settings page`, `change navbar behavior`, `add an endpoint`, or `rewrite the CTA` are product-affecting even if easy, so they still get a short interview + effort confirmation.

---

## Single-agent-first specialist layer

Agentit does not simulate a fake company for every task. Direct work is the default.

[`agents/catalog.yaml`](agents/catalog.yaml) defines temporary semantic specialists such as:

```text
frontend-developer
backend-architect
ai-engineer
devops-automator
trend-researcher
ui-researcher
creative-tool-scout
visual-storytelling-director
spatial-experience-designer
delight-and-whimsy
design-critic
performance-benchmarker
api-tester
workflow-optimizer
```

A specialist is a role + small skill bundle + output contract. The parent remains responsible for decomposition, integration, verification, and user communication.

Effort level changes how much delegation is reasonable:

- **Standard:** 0 specialists by default; usually at most 1 when clearly valuable.
- **Polished:** usually 0-2.
- **Studio:** 2-5 can make sense, but only when they add real value.

Even Studio may stay single-agent if delegation buys nothing.

---

## Provider-neutral execution

The same specialist works regardless of provider. Agentit chooses the best primitive available:

```text
native provider subagent/worker
        ↓ unavailable
isolated delegated model/tool call
        ↓ unavailable
separate fresh-context invocation
        ↓ unavailable
parent + exact specialist skill bundle
```

The **objective, skills, constraints, allowed I/O, output contract, verification, effort level, and stop condition stay equivalent**.

Multi-agent execution is an optimization for isolation, diversity, and parallelism. Agentit must remain usable with OpenAI, Anthropic, Google, xAI, and future providers even if they expose different orchestration features.

Canonical policy: [`docs/AGENTIT_INTERVIEW_AND_PROVIDER_POLICY.md`](docs/AGENTIT_INTERVIEW_AND_PROVIDER_POLICY.md).

---

## Design studio

The `design` profile contains a craft-first stack for serious visual work:

```text
design-inspiration-research
design-trend-researcher
creative-web-experiences
design-taste-frontend
impeccable-design
emil-design-eng
visual-storytelling-director
creative-tool-scout
delight-and-whimsy
figma-design-workflow
scrollytelling-web
gsap-scrolltrigger
gsap-performance
threejs-spatial-experiences
threejs-product-storytelling
```

But **design no longer means unlimited token spend by default**.

- Standard design → minimum relevant craft skills + rendered browser check.
- Polished design → targeted research/specialists + stronger responsive/state/interaction QA.
- Studio design → full relevant craft stack, broad reference/tool research, multiple concepts when valuable, independent critique, performance/browser loops.

A premium site also does not automatically mean product decomposition or scrollytelling. Agentit can choose editorial, spatial, kinetic, 2D/3D, image-led, restrained static, or other interaction models based on the actual brand/content.

### Design competition

Normally a **Studio** topology:

```text
shared research brief
  ↓
2-3 independent concepts
  ↓
explicit jury
(brand fit / originality / clarity / usability / feasibility / performance / memorability)
  ↓
winner or justified hybrid
  ↓
implementation
  ↓
independent design + performance critique
```

If native subagents are unavailable, the same method can run sequentially in fresh/direct contexts.

---

## Shared skills and profiles

`profiles.yaml` keeps the global engineering core bounded and activates heavier skills JIT.

| Profile | Role |
|---|---|
| `core` | routing, orchestration, debugging, review, TDD, security, source-driven work, frontend UI, planning, verification |
| `frontend` | browser/performance/UI design engineering |
| `design` | research + art direction + motion + Figma + creative tooling + scrollytelling + spatial/product 3D |
| `backend` / `supabase` | APIs, observability, Postgres/Supabase |
| `product` / `writing` / `release` / `research` | discovery, specs, marketing, launch, adversarial review |
| `all` | explicit escape hatch only |

---

## Verification gauntlet

No `done`, `fixed`, or `passing` claim should rely solely on the implementing agent's own assertion.

```bash
./agentit verify "Add Supabase RLS for profiles" --project .
./agentit verify "Add Supabase RLS for profiles" --project . --apply
```

Receipts live under `.agentit/verify/`. Catalog: [`probes/catalog.yaml`](probes/catalog.yaml).

Verification depth can increase with effort, but risk/correctness gates do not decrease at Standard.

---

## MCP and live tools

```bash
agentit mcp status
agentit mcp enable context7 --apply
agentit mcp enable-stack developer_core --apply
agentit mcp enable-stack design_studio --apply
```

The `design_studio` stack combines Figma, Context7, Playwright, and Chrome DevTools. Inspiration/tool research may use live browser sources such as showcases, studios, social/video platforms where access permits, and catalogs such as `designengineer.tools`, then verify technical choices against primary docs.

MCPs are capabilities, not portability requirements; unavailable integrations should degrade to equivalent tools or be reported explicitly.

---

## Quick start

```bash
git clone https://github.com/marcmarti9/agentit.git ~/code/agentit
cd ~/code/agentit

bash install.sh --provider all --with-guides
bash install.sh --provider all --with-guides --apply
ln -sf ~/code/agentit/agentit ~/.local/bin/agentit
```

Default Open Skills / Grok path: `~/.agents/skills/`. Claude: `~/.claude/skills/`. Codex: `~/.codex/skills/`.

Enable a project profile:

```bash
./agentit enable design --project . --apply
./agentit status --project .
```

Route / trace / verify:

```bash
python3 ~/code/agentit/router/route.py "confirmed task"
./agentit trace "confirmed task" --project .
./agentit verify "confirmed task" --project . --apply
```

---

## Safety defaults

- plan-first scripts; writes require `--apply` where designed;
- RISK_3 / RISK_4 retain full safety/human-review gates;
- no commits, push, deploy, or remote mutations without explicit authorization;
- one writer per shared file/state in parallel work;
- missing provider multi-agent features must degrade gracefully;
- safety/correctness outrank effort/token budget.

---

## Docs map

| Doc | Purpose |
|---|---|
| [`AGENTS.md`](AGENTS.md) | Global agent playbook |
| [`ABOUT.md`](ABOUT.md) | Product philosophy |
| [`effort/levels.yaml`](effort/levels.yaml) | Standard / Polished / Studio behavior and token envelopes |
| [`docs/AGENTIT_INTERVIEW_AND_PROVIDER_POLICY.md`](docs/AGENTIT_INTERVIEW_AND_PROVIDER_POLICY.md) | Interview + effort + provider-neutral policy |
| [`docs/ADAPTIVE_AGENT_ARCHITECTURE.md`](docs/ADAPTIVE_AGENT_ARCHITECTURE.md) | Topologies and contracts |
| [`docs/MCP_CATALOG.md`](docs/MCP_CATALOG.md) | MCP catalog/runtime |
| [`agents/catalog.yaml`](agents/catalog.yaml) | Specialist roles |
| [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) | Third-party attribution |

---

## Testing

```bash
python3 -m unittest discover -s router -p "test_*.py"
python3 -m unittest discover -s tests
python3 evals/run.py
```

---

## License

Licensed under the [Apache License, Version 2.0](LICENSE). See [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) for third-party material and attributions.
