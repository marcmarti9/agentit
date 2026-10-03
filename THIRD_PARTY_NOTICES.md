# Third-party notices

Agentit includes, vendors, adapts, or is materially informed by the projects below. Agentit's original code and material remain Apache-2.0 except explicitly marked share-alike adaptations. Canonical skill snapshots, upstream paths and per-file integrity are recorded in `skills/UPSTREAM_LOCK.json` and `skills/UPSTREAM_SOURCES.md`. Exact upstream LICENSE/NOTICE files are retained under `vendor/licenses`; they govern the corresponding third-party material. Source-informed additions from the October 3 audit are separately recorded in `skills/ADAPTATION_SOURCES.json` and `vendor/adaptation-licenses`.

## Canonical vendored skill sources

### Addy Osmani / Agent Skills

Source: https://github.com/addyosmani/agent-skills

License: MIT. Copyright (c) 2025 Addy Osmani.

Agentit vendors the canonical upstream packages for matching engineering skill IDs without compressing or rewriting their skill bodies. Addy's repo-level shared `references/` files are vendored at Agentit's root `references/` so upstream relative links from those `skills/<id>` packages continue to resolve.

The raw upstream `using-agent-skills` meta-workflow is retained separately under `vendor/agent-skills/using-agent-skills`. The globally discoverable `skills/using-agent-skills` is an Agentit-owned adapter informed by that source; it is not represented as a verbatim upstream package. Agentit owns selective loading and authority policy outside the canonical packages.

That relocated raw meta-workflow is a provenance archive, not a separately
activated or self-contained workflow package. Its unchanged `../../references/`
links describe the upstream layout; when inspecting the archive, consult the
matching shared files in Agentit's root `references/` or the pinned source.

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

Agentit vendors Impeccable's canonical `.agents/skills/impeccable` distribution as `skills/impeccable`, including its skill body, agents, references, launchers and other regular distributed files. The current upstream distribution uses a versioned binary launcher for optional execution; Agentit's bootstrap and source refresh do not execute it or download that binary. Agentit-specific routing and composition remain outside the vendored package.

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

### Anthropic / skills

Source: https://github.com/anthropics/skills

License: Apache License 2.0 for the inspected `skill-creator` and `mcp-builder` packages.

Agentit's `skill-authoring-and-evals` and `mcp-server-development` are Agentit-owned, provider-neutral adaptations informed by those public skills. Agentit does not vendor Anthropic's skill-creator eval viewer/scripts, MCP reference package, or Claude-specific workflow, and does not claim drop-in compatibility.

### Vercel Labs / agent-skills

Source: https://github.com/vercel-labs/agent-skills

The inspected `vercel-composition-patterns` skill declares MIT licensing in its skill metadata.

Agentit's `react-composition-patterns` is an Agentit-owned adaptation of the component-composition ideas, narrowed to demonstrated API pressure and Agentit's anti-overengineering contract. Agentit does not vendor Vercel's compiled AGENTS document or rule-file package.


### Dietrich Gebert / Ponytail

Source: https://github.com/DietrichGebert/ponytail

License: MIT. Copyright (c) 2026 DietrichGebert.

Agentit's `anti-overengineering` BUILDER minimum-solution ladder is materially informed by Ponytail's YAGNI/reuse/stdlib/native-platform/minimum-code ordering and its distinction between lazy implementation and careless understanding. Agentit does not vendor Ponytail's skill pack, intensity modes, commands or review workflow; Agentit's BUILDER/REVIEW and risk policy remain authoritative.

### Matt Pocock / skills

Source: https://github.com/mattpocock/skills

License: MIT. Copyright (c) 2026 Matt Pocock.

Agentit has adapted or incorporated engineering ideas from the project into its own workflows, especially agent-document writing discipline, progressive disclosure, completion criteria, feedback-loop-first debugging, requirements interviewing, and related engineering-process guidance. The Agentit-owned `skill-authoring-and-evals` skill is also materially informed by `writing-for-agents`. Agentit does not claim drop-in compatibility with Matt Pocock's command/plugin system and does not vendor a canonical Matt Pocock skill package in the current registry.

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

## October 3, 2026 source-informed adaptations

These are modified, provider-neutral Agentit procedures, not verbatim packages or claims of upstream runtime compatibility. The immutable revisions, target files and exact retained license/NOTICE hashes are recorded in [`skills/ADAPTATION_SOURCES.json`](skills/ADAPTATION_SOURCES.json). Canonical refresh records remain in their separate upstream lock.

### expo/skills

Source: [expo/skills at `13ad8e05874195633b5c185f6947bb6400e228fc`](https://github.com/expo/skills/tree/13ad8e05874195633b5c185f6947bb6400e228fc). Inspected October 3, 2026.

Upstream scope/license: `LICENSE` — MIT; [unaltered license text](vendor/adaptation-licenses/expo--skills/LICENSE). The modified Agentit target material is Apache-2.0; retain the upstream copyright/permission text distributed with it.

Changed scope: `skills/mobile-runtime-engineering/SKILL.md`, `skills/mobile-runtime-engineering/references/state-and-navigation.md`.

### callstackincubator/agent-skills

Source: [callstackincubator/agent-skills at `61e6e7dfdf3a8ee862254c200d751fcb1fb863dc`](https://github.com/callstackincubator/agent-skills/tree/61e6e7dfdf3a8ee862254c200d751fcb1fb863dc). Inspected October 3, 2026.

Upstream scope/license: `LICENSE` — MIT; [unaltered license text](vendor/adaptation-licenses/callstackincubator--agent-skills/LICENSE). The modified Agentit target material is Apache-2.0; retain the upstream copyright/permission text distributed with it.

Changed scope: `skills/mobile-runtime-engineering/SKILL.md`, `skills/mobile-runtime-engineering/references/performance-evidence.md`.

### openai/skills

Source: [openai/skills at `49f948faa9258a0c61caceaf225e179651397431`](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431). Inspected October 3, 2026.

Upstream scope/license: `skills/.curated/pdf/LICENSE.txt` — Apache-2.0; [unaltered license text](vendor/adaptation-licenses/openai--skills/LICENSE.txt). The modified Agentit target material is Apache-2.0; retain the upstream copyright/permission text distributed with it.

Changed scope: `skills/artifact-production/SKILL.md`, `skills/artifact-production/references/format-verification.md`.

### SenteLabsAI/OpenExecutive

Source: [SenteLabsAI/OpenExecutive at `bba990f20dab7559967010e65b65630f1a35c684`](https://github.com/SenteLabsAI/OpenExecutive/tree/bba990f20dab7559967010e65b65630f1a35c684). Inspected October 3, 2026.

Upstream scope/license: `LICENSE` — Apache-2.0; [unaltered license text](vendor/adaptation-licenses/SenteLabsAI--OpenExecutive/LICENSE). The modified Agentit target material is Apache-2.0; retain the upstream copyright/permission text distributed with it. [Unaltered upstream NOTICE](vendor/adaptation-licenses/SenteLabsAI--OpenExecutive/NOTICE) is distributed alongside the license.

Changed scope: `skills/executive-orchestration/references/quality-playbook.md`, `skills/reference-intelligence/references/research-quality.md`.

### coreyhaines31/marketingskills

Source: [coreyhaines31/marketingskills at `dda3841f0b294e01e93b1541486beefbfab0915e`](https://github.com/coreyhaines31/marketingskills/tree/dda3841f0b294e01e93b1541486beefbfab0915e). Inspected October 3, 2026.

Upstream scope/license: `LICENSE` — MIT; [unaltered license text](vendor/adaptation-licenses/coreyhaines31--marketingskills/LICENSE). The modified Agentit target material is Apache-2.0; retain the upstream copyright/permission text distributed with it.

Changed scope: `skills/marketing-and-growth/references/quality-playbook.md`, `skills/reference-intelligence/references/research-quality.md`.

### anthropics/skills

Source: [anthropics/skills at `8a1541c4a3ffa5a20a5a91de0dcf3f0bab1d1ef4`](https://github.com/anthropics/skills/tree/8a1541c4a3ffa5a20a5a91de0dcf3f0bab1d1ef4). Inspected October 3, 2026.

Upstream scope/license: `skills/skill-creator/LICENSE.txt` — Apache-2.0; [unaltered license text](vendor/adaptation-licenses/anthropics--skills/LICENSE.txt). The modified Agentit target material is Apache-2.0; retain the upstream copyright/permission text distributed with it.

Changed scope: `skills/skill-authoring-and-evals/references/paired-evaluations.md`.

### trailofbits/skills

Source: [trailofbits/skills at `82fe8226252622fa807643bdca1710901198553a`](https://github.com/trailofbits/skills/tree/82fe8226252622fa807643bdca1710901198553a). Inspected October 3, 2026.

Upstream scope/license: `LICENSE` — CC-BY-SA-4.0; [unaltered license text](vendor/adaptation-licenses/trailofbits--skills/LICENSE). Attribution: Trail of Bits. The property-testing and security-analysis bodies and their references are substantial modified adaptations licensed **CC-BY-SA-4.0**, including the share-alike terms; these files are exceptions to Agentit’s Apache-2.0 license.

Changed scope: `skills/property-based-testing/SKILL.md`, `skills/property-based-testing/references/design-and-review.md`, `skills/security-analysis/SKILL.md`, `skills/security-analysis/references/finding-triage.md`.

### trailofbits/testing-handbook

Source: [trailofbits/testing-handbook at `190294f0ed563baddf4941cd2388be5bd4d5c5ba`](https://github.com/trailofbits/testing-handbook/tree/190294f0ed563baddf4941cd2388be5bd4d5c5ba). Inspected October 3, 2026.

Upstream scope/license: `LICENSE` — CC-BY-4.0; [unaltered license text](vendor/adaptation-licenses/trailofbits--testing-handbook/LICENSE). Attribution: Trail of Bits. Security-analysis procedures adapt configuration/coverage and finding-interpretation guidance; the resulting files are CC-BY-SA-4.0.

Changed scope: `skills/security-analysis/SKILL.md`, `skills/security-analysis/references/finding-triage.md`.

### ajrcre/data-analysis-skills

Source: [ajrcre/data-analysis-skills at `cbc906e4912a980423aecd1e318061eb98f3e0b2`](https://github.com/ajrcre/data-analysis-skills/tree/cbc906e4912a980423aecd1e318061eb98f3e0b2). Inspected October 3, 2026.

Upstream scope/license: `LICENSE` — MIT; [unaltered license text](vendor/adaptation-licenses/ajrcre--data-analysis-skills/LICENSE). The modified Agentit target material is Apache-2.0; retain the upstream copyright/permission text distributed with it.

Changed scope: `skills/data-analysis-quality/SKILL.md`, `skills/data-analysis-quality/references/claim-checks.md`.
