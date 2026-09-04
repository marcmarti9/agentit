# Third-party notices

Agentit includes, vendors, adapts, or is materially informed by the projects below. Agentit's original code and material remain Apache-2.0. Canonical skill snapshots and upstream paths are recorded in `skills/UPSTREAM_LOCK.json` and `skills/UPSTREAM_SOURCES.md`.

## Canonical vendored skill sources

### Addy Osmani / Agent Skills

Source: https://github.com/addyosmani/agent-skills

License: MIT. Copyright (c) 2025 Addy Osmani.

Agentit vendors the canonical upstream packages for matching engineering skill IDs without compressing or rewriting their skill bodies. Addy's repo-level shared `references/` files are vendored at Agentit's root `references/` so upstream relative links continue to resolve.

### Leonxlnx / taste-skill

Source: https://github.com/Leonxlnx/taste-skill

License: MIT. Copyright (c) 2026 Leonxlnx.

Agentit vendors the canonical upstream `skills/taste-skill` package as `skills/design-taste-frontend` without compressing or rewriting its skill body.

### Emil Kowalski / skills

Source: https://github.com/emilkowalski/skills

License: MIT. Copyright (c) 2026 Emil Kowalski.

Agentit vendors the canonical upstream `skills/emil-design-eng` package as `skills/emil-design-eng` without compressing or rewriting its skill body.

### GreenSock / gsap-skills

Source: https://github.com/greensock/gsap-skills

License: MIT. Copyright (c) 2026 GreenSock.

Agentit vendors the canonical upstream `gsap-scrolltrigger` and `gsap-performance` packages without compressing or rewriting their skill bodies.

### Paul Bakaus / Impeccable

Source: https://github.com/pbakaus/impeccable

License: Apache License 2.0. Copyright 2025 Paul Bakaus.

Agentit vendors Impeccable's canonical `.agents/skills/impeccable` distribution as `skills/impeccable`, including its complete skill package such as `SKILL.md`, agents, references, scripts, detector/live tooling, and other regular package files. Agentit-specific routing and composition remain outside the vendored package.

### Next Level Builder / UI UX Pro Max Skill

Source: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill

License: MIT. Copyright (c) 2024 Next Level Builder.

Agentit vendors the canonical `.claude/skills/ui-ux-pro-max` package in full, including its data, references, scripts, and package tests. The former compact `ui-ux-pro-max-intelligence` adapter is retired.

### Appllama / appllama-skills

Source: https://github.com/Appllama/appllama-skills

License: MIT. Copyright (c) 2026 Antmind Ventures Private Limited (appllama.io).

Agentit vendors the canonical `appllama-app-design-skill` and `appllama-usage` packages in full. The former compact `mobile-native-app-design` adapter is retired. Live Appllama MCP availability remains an external capability decision; Agentit does not bundle paid access, credentials, or the live service.

### Siqi Chen / Humanizer

Source: https://github.com/blader/humanizer

License: MIT. Copyright (c) 2025 Siqi Chen.

Agentit vendors the canonical Humanizer package, including its upstream skill body, agent metadata, and scripts, instead of maintaining the former compressed writing synthesis.

### Hardik Pandya / Stop Slop

Source: https://github.com/hardikpandya/stop-slop

License: MIT. Copyright (c) 2025 Hardik Pandya.

Agentit vendors the canonical Stop Slop package and references instead of folding its guidance into a compressed local wrapper.

### Cathryn Lavery / diagram-design

Source: https://github.com/cathrynlavery/diagram-design

License: MIT. Copyright (c) 2025 Cathryn Lavery.

Agentit vendors the canonical `diagram-design` package in full, including its references, renderer/example assets, and scripts. The former compact `diagram-and-architecture-visuals` adapter is retired.

### Supabase / Agent Skills

Source: https://github.com/supabase/agent-skills

License: MIT. Copyright (c) 2026 Supabase.

Agentit vendors the canonical `supabase-postgres-best-practices` package in full.

### Nutlope / Hallmark

Source: https://github.com/Nutlope/hallmark

License: MIT. Copyright (c) 2026 Hallmark contributors.

Agentit vendors the canonical `hallmark` package in full, including its reference library. The former local `anti-ai-slop-design` adapter is retired.

### Vercel Labs / Skills

Source: https://github.com/vercel-labs/skills

License: MIT. Copyright (c) 2026 Vercel, Inc.

Agentit vendors the canonical `find-skills` package in full. The exact upstream snapshot and path are recorded in `skills/UPSTREAM_LOCK.json`.

### Jesse Vincent / Superpowers

Source: https://github.com/obra/superpowers

License: MIT. Copyright (c) 2025 Jesse Vincent.

Agentit vendors the canonical `verification-before-completion` package in full. Agentit-specific Loop/Graph receipt enforcement remains in Agentit's runtime and core policy instead of being injected into the vendored skill body.

## Agentit-owned adaptations and source-informed skills

### Matt Pocock / skills

Source: https://github.com/mattpocock/skills

License: MIT. Copyright (c) 2026 Matt Pocock.

Agentit has adapted or incorporated engineering ideas from the project into its own workflows, especially agent-document writing discipline, progressive disclosure, completion criteria, feedback-loop-first debugging, requirements interviewing, and related engineering-process guidance. Agentit does not claim drop-in compatibility with Matt Pocock's command/plugin system and does not vendor a canonical Matt Pocock skill package in the current registry.

### Scott Sun / Three.js Awesome Graphics Agent Skills

Source: https://github.com/scottstts/Threejs-Awesome-Graphics-Agent-Skills

License: MIT. Copyright (c) 2026 Scott Sun.

Agentit's `threejs-product-storytelling` is original guidance informed by the project's graphics-quality and validation philosophy. Agentit does not vendor its specialist implementation/example library.

### Google Labs / DESIGN.md

Source: https://github.com/google-labs-code/design.md

License: Apache License 2.0.

Agentit's `design-md-workflow` is original integration guidance around the external alpha `DESIGN.md` format. Agentit does not vendor Google's parser, linter, or schema implementation and does not treat the alpha format as a permanent Agentit-owned standard.

### tt-a1i / Archify

Source: https://github.com/tt-a1i/archify

License: MIT. Copyright (c) 2026 tt-a1i (Archify), with upstream copyright notices retained by that project.

Agentit's diagram and architecture workflows may treat Archify as an optional JIT external implementation family for typed, validated, code-grounded architecture maps. Agentit does not vendor Archify's renderer, JSON schemas, validators, or artifacts.

### Sente Labs / OpenExecutive

Source: https://github.com/SenteLabsAI/OpenExecutive

License: Apache License 2.0. Copyright 2025 Open Executive Contributors.

Agentit's `executive` profile and `executive-*` skills are original provider-neutral adaptations materially informed by OpenExecutive's public architecture and operating guidance: a coherent executive synthesis layer, domain-specialist decomposition, model-owned specialist selection, parallel specialist consultation, company context, durable memory concepts, authority boundaries, domain decision heuristics, and evaluation discipline.

Agentit does not vendor OpenExecutive's Python/TypeScript runtime, prompts verbatim, UI, FastAPI/Next.js application, ChromaDB/SQLite persistence, scheduler/integration implementation, or provider/model configuration. It does not require Anthropic/Claude and does not claim drop-in compatibility with OpenExecutive.

## MIT license text

The following notice applies to the MIT-licensed upstream material identified above; the individual copyright notices remain those listed in each source section.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
