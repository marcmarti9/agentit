# Deep dive comparativo: Superpowers, ECC, GSD Core, Matt Pocock vs Agentit

**Fecha:** 2026-08-05  
**Alcance:** análisis de capacidades (sin importar skills, sin commits, sin instalar dependencias).  
**Fuentes inspeccionadas:** clones shallow en `/tmp/agentit-deepdive/` + `gh` API/issues + árbol actual de Agentit (`skills/`, `router/`, `agents/`, `profiles.yaml`, `docs/`).

---

## 0. Cómo leer este informe

### 0.1 Tipos de evidencia

| Etiqueta | Significado |
|----------|-------------|
| **V** (verificado) | Leído en el repo clonado, archivo citado, o issue/API GitHub inspeccionada en esta sesión |
| **I** (inferencia) | Conclusión razonable a partir de V; no es claim del upstream |
| **C** (claim upstream) | Afirmación de README/marketing del repo; no revalidada empíricamente en runtime |

### 0.2 Decisiones de clasificación

Para cada capacidad:

- `already_covered` — Agentit ya la resuelve de forma comparable
- `enhance_existing` — existe superficie; falta rigor, contrato o señal
- `new_skill` — merecería un skill acotado (no megapack)
- `router_rule` — pertenece al router heurístico / perfiles / signals
- `new_topology` — topología de ejecución distinta a las actuales
- `integration` — CLI/hooks/MCP/runtime adapter, no skill de prosa
- `context_provider` — memoria, artefactos, inyección de contexto
- `scout_source` — fuente de descubrimiento, no core
- `reject` — no encaja con filosofía Agentit o es demasiado costosa/riesgosa

### 0.3 Criterio anti-estrellas

Las estrellas solo se usan como señal de adopción. Ninguna propuesta se justifica por popularidad sola. Se exige: **problema observable en Agentit**, **capacidad concreta**, **cómo evaluarla**.

### 0.4 GSD: repositorio activo

| Claim | Evidencia |
|-------|-----------|
| `gsd-build/get-shit-done` ya no es el home activo | **V** README empieza con redirect a Open GSD; `pushed_at` 2026-05-31 |
| Sucesor activo | **V** `open-gsd/gsd-core` (`@opengsd/gsd-core`), `pushed_at` 2026-08-05, ~7.7k★ |
| Org `gsd-build` también tiene `gsd-2` (~7.7k★, última push 2026-05) | **V** API org; **no** es el target de deep dive primario |

**Regla de este informe:** análisis GSD = **`open-gsd/gsd-core`**, con issue #671 del repo histórico solo como lección de fallos.

---

## 1. Estado actual de Agentit (baseline)

### 1.1 Qué es Agentit (V)

Meta-harness **provider-neutral** con:

- Router heurístico (`router/route.py`): risk, topology, skills, compression, verification
- Perfiles JIT (`profiles.yaml`): `core` (10 skills globales) + perfiles opt-in
- Skills curadas (~31) con progressive disclosure
- Roles adaptativos: architect / orchestrator / supervisor / worker / auditor
- Context engines: tool filter, artifact refs, session dedup
- Scout/incubator (`router/scout.py` → `incubator/candidates.yaml`)
- Preferencias usuario (`router/preferences.py`)
- Seguridad local (`security/harden-local.sh`) y dry-run por defecto en scripts

### 1.2 Filosofía operativa (V + I)

- Single-agent-first; multi-agente solo con justificación
- No instalar hooks/MCP automáticos sin revisión
- Discovery acotada (core pequeño) por presupuesto de contexto Codex
- Capacidades como skills + reglas de router, no pirámide fija

### 1.3 Superficie de skills relevante para el diff

| Área | Skills Agentit (V) |
|------|-------------------|
| Requisitos / discovery | `interview-me`, `idea-refine`, `spec-driven-development` |
| Adversarial | `doubt-driven-development` |
| Orquestación | `architect-orchestrator`, `task-router` |
| Plan / implementación | `planning-and-task-breakdown`, `incremental-implementation` |
| TDD / debug | `test-driven-development`, `debugging-and-error-recovery` |
| Review | `code-review-and-quality` |
| Research | `source-driven-development`, `context-engineering` |
| Writing agents | parcial vía `using-agent-skills`, docs internas |
| Memoria cross-session | artifact_ref + dedup (no vault semántico de preferencias) |
| Scout | `find-skills` + `router/scout.py` |

---

## 2. Superpowers (`obra/superpowers`)

### 2.1 Hechos verificados

| Hecho | Evidencia |
|-------|-----------|
| ~267k★, push 2026-08-05 | **V** `gh api` |
| 14 skills de proceso (no domain pack) | **V** `skills/*/SKILL.md` |
| Bootstrap SessionStart inyecta `using-superpowers` completo | **V** `hooks/session-start` + `hooks/hooks.json` |
| Metodología: brainstorm → design → plan → SDD → verify → finish branch | **V** README + skills |
| Hard-gate: no implementar sin design aprobado (`brainstorming`) | **V** `<HARD-GATE>` en skill |
| SDD: implementer fresco por task + review + final branch review | **V** `subagent-driven-development/SKILL.md` (~503 líneas) + `implementer-prompt.md` |
| Iron laws: root-cause antes de fix; TDD red-first; verification evidence-first | **V** skills correspondientes |
| Zero-dependency plugin; rechazo alto de PRs agent-slop (~94% claim) | **C/V** CLAUDE.md/AGENTS.md del repo |
| Tests de integración multi-harness (claude-code, codex, opencode, antigravity…) | **V** `tests/` |
| Issues abiertos: SDD commits a main fuera de worktree (#2050); TDD arrange silencioso (#2092); brainstorming sin exclusión mecánica (#2076) | **V** `gh issue list` |

### 2.2 Arquitectura (I a partir de V)

Superpowers no es un “router de riesgo” como Agentit. Es un **sistema de proceso con auto-trigger obligatorio**:

1. SessionStart carga la ley de invocar skills antes de actuar.
2. Skills de proceso tienen descripciones de disparo muy agresivas (`You MUST use this before any creative work`).
3. El plan se escribe para un “junior con mal gusto” (ejecutable sin contexto).
4. La ejecución multi-agente es **opcional pero preferida** cuando hay subagentes: SDD con contrato de escalación `BLOCKED` / `NEEDS_CONTEXT`.
5. La calidad se defiende con **presión anti-racionalización** (tablas Red Flags) más que con código del router.

### 2.3 Capacidades extraídas

| ID | Capacidad | Decisión | Agentit existente | Gap |
|----|-----------|----------|-------------------|-----|
| SP-01 | Hard-gate pre-implementación (design sign-off) | `enhance_existing` | `interview-me`, `idea-refine`, `spec-driven-development` | Agentit recomienda; Superpowers **prohíbe** código hasta approval. Falta umbral enforceable en router. |
| SP-02 | Skill bootstrap SessionStart (invoke-before-act) | `reject` como default global | `task-router` + AGENTS.md | Hooks automáticos chocan con política Agentit. Opcional por provider sí. |
| SP-03 | Plan “junior-proof” con YAGNI/DRY/TDD | `enhance_existing` | `planning-and-task-breakdown` | Menos checklist de descomposición por archivo y acceptance por task. |
| SP-04 | Subagent-driven development (fresh implementer + dual review) | `enhance_existing` / no `new_topology` | `architect-orchestrator` writer+reviewer, pipeline | Plantillas de implementer/reviewer más rígidas; self-review checklist antes de reportar. |
| SP-05 | Verification-before-completion (iron law evidencia fresca) | `enhance_existing` | verification en router + skills | Falta skill/regla única “no claims without command output this turn”. |
| SP-06 | Systematic debugging root-cause gate | `already_covered` (alto overlap) | `debugging-and-error-recovery` | Comparar tablas de presión; posible cherry-pick de red flags. |
| SP-07 | TDD red-green con anti-racionalización | `enhance_existing` | `test-driven-development` | Issue #2092: arrange silencioso — patrón a evitar al endurecer TDD. |
| SP-08 | Worktree isolation skill | `enhance_existing` | worktrees en arch docs / Grok isolation | Skill operativo portable multi-harness. |
| SP-09 | Writing skills as TDD (pressure scenarios) | `enhance_existing` | `using-agent-skills` | Eval adversarial de skills Agentit casi ausente. |
| SP-10 | Parallel dispatch por dominios independientes | `already_covered` | fan_out topology | Criterio de independencia similar. |

### 2.4 Contradicciones / riesgos vs Agentit

- **Trigger agresivo vs single-agent-first:** Superpowers fuerza brainstorming incluso en tareas triviales (issue #2076 lo reconoce). Agentit debería **excluir** tareas mecánicas (V: interview-me ya tiene “When NOT”). **I:** el riesgo de copiar Superpowers ciego es latencia y fricción.
- **Hooks SessionStart:** Agentit prohíbe activarlos sin revisión. Importar el bootstrap es `integration` opt-in, no core.
- **SDD worktree bugs (#2050, #1040):** **I:** Agentit debe tratar aislamiento como **enforceable** (cwd, path policy), no solo “prefer worktree”.

### 2.5 Problemas observables que resolverían en Agentit

1. Agentes saltan a código sin design en features no triviales.
2. Claims de “tests pass” sin corrida fresca.
3. Workers sin contrato de escalación (adivinan en vez de `NEEDS_CONTEXT`).

### 2.6 Cómo evaluar

- Suite de escenarios: “build X feature”, “fix bug”, “rename var” — medir hard-gate hits / false positives.
- Checklist de verificación: % de claims de éxito con evidencia de comando en el mismo turno.
- SDD mock: 3 tasks; verificar review package y no commits fuera de scope.

---

## 3. GSD Core (`open-gsd/gsd-core`)

### 3.1 Hechos verificados

| Hecho | Evidencia |
|-------|-----------|
| Phase loop: Discuss → Plan → Execute → Verify → Ship | **V** README |
| Fresh-context subagents; orchestrator delgado; state en `.planning/` | **V** `docs/explanation/context-engineering.md`, `multi-agent-orchestration.md`, `ARCHITECTURE.md` |
| Artefactos: `STATE.md`, `CONTEXT.md`, `PLAN.md`, `RESEARCH.md`, `SUMMARY.md` | **V** docs + templates |
| 6 namespace routers (`gsd-workflow`, `gsd-project`, `gsd-quality`, `gsd-context`, `gsd-manage`, `gsd-ideate`) | **V** `commands/gsd/ns-*.md` |
| Claim token discovery: ~120 tokens (6 routers) vs ~2150 (flat ~86 skills) | **C** docs COMMANDS/ARCHITECTURE citando #2792; **no** re-medido aquí |
| Layout nested solo en runtimes non-recursive; flat en Claude/Cursor/Codex (Skill tool hard-error) | **V** ARCHITECTURE.md (#1614, #924) |
| Issue histórico #671: subagents sin `CLAUDE.md` del proyecto → security/quality gaps reales | **V** issue + fix commit claim en gsd-build; **V** executor actual exige leer `./CLAUDE.md` |
| Issue abierto #2483: reviewer Claude hereda CLAUDE.md+memory (~4k/spawn) — asimetría de contexto | **V** open-gsd issues |
| Issue #3021: worktree branches derrotan guards | **V** open issues |
| Executor documenta que MCP project-scoped no llega a subagents → fallback CLI Context7 | **V** `agents/gsd-executor.md` |
| Effort frontmatter `max`/`low`; no `context:fork` en orchestrators (rompe Agent tool, #921) | **V** docs |

### 3.2 Arquitectura vs Agentit profiles (el “2% problem”)

| Dimensión | Agentit (V) | GSD (V) |
|-----------|-------------|---------|
| Reducción discovery | Perfiles JIT (`core` 10 + enable) | 6 meta-skills router + nested en algunos runtimes |
| Quién decide el subconjunto | Humano/`agentit enable` + router heuristics | Modelo elige namespace → tabla de ruteo |
| Persistencia cross-session | artifacts + dedup + incubator | `.planning/` como memoria de proyecto |
| Multi-agente default | No (single-first) | Sí para work pesado (fase loop) |
| Unit of work | Task + topology | Phase + milestone + plan waves |

**I:** Ambos atacan **coste de listing + context rot**, pero:

- Agentit optimiza **presupuesto de skills instaladas/descubribles**.
- GSD optimiza **ciclo de vida del trabajo** y **ventana limpia por agente**.

No son el mismo diseño. Complementarios, no sustituibles 1:1.

### 3.3 Capacidades extraídas

| ID | Capacidad | Decisión | Agentit existente | Gap |
|----|-----------|----------|-------------------|-----|
| GSD-01 | Phase loop con artefactos obligatorios | `enhance_existing` / parcial `new_topology` | plan+direct, pipeline, `spec-driven-development` | Falta spine de proyecto (STATE/CONTEXT) estandarizado opcional. |
| GSD-02 | Namespace routers (two-stage skill discovery) | `router_rule` | profiles.yaml | Meta-skills “cluster” encima de perfiles; o router emite clusters keyword-dense. |
| GSD-03 | Fresh subagent + thin orchestrator | `already_covered` (filosofía) | adaptive architecture | Agentit ya lo predica; GSD lo industrializa en workflows. |
| GSD-04 | Propagación de project instructions a workers | `enhance_existing` | contracts en AGENTS/architect | **Contrato de worker debe exigir** leer AGENTS.md/CLAUDE.md + skills del proyecto; lección #671. |
| GSD-05 | Context headroom hooks (PreCompact/Stop) | `integration` opt-in | compression modes | Solo con allowlist; medir rot, no copiar hooks a ciegas. |
| GSD-06 | Smart-zone plan token estimates | `reject` o experiment bajo | — | Útil si hay phase system; overkill sin él. |
| GSD-07 | Research provider waterfall + RESEARCH.md path-only | `enhance_existing` | `source-driven-development` | Contrato “devolver path, no volcar raw fetch al main”. |
| GSD-08 | Capability trust model (ledger + consent) | `scout_source` / futuro | scout incubator | Modelo de trust para skills externas. |
| GSD-09 | CONTEXT.md predicate fact-store | `context_provider` | — | Hechos parseables `CLASS.key=value` en CONTEXT. |
| GSD-10 | Worktree/path guards fail-closed | `enhance_existing` | isolation worktree | Issues GSD muestran que guards fallan abiertos (#3021) — no copiar bugs. |

### 3.4 Lección #671 (crítico para Agentit)

**V:** Ejecutores sin `CLAUDE.md` del proyecto omitieron skills de seguridad/React durante 6 fases → vulnerabilidades reales en review final.

**I para Agentit:**

- Toda topología con `worker` debe incluir en el prompt mínimo:
  - rutas de instrucciones de proyecto (`AGENTS.md`, `CLAUDE.md`, `CODEX.md`)
  - skills/perfil activos o cómo descubrirlos
  - ownership de archivos + verifier
- “Fresh context” **sin** projection de policy = **fresh negligence**.
- Test de regresión: spawn worker con CLAUDE.md que prohíbe patrón X; assert el worker no introduce X.

### 3.5 Contradicciones

- GSD **default multi-agent phase loop** vs Agentit **default direct**.
- GSD denso en TypeScript CLI + hooks + capabilities; Agentit Python+bash, dry-run first.
- **I:** Portar GSD entero = abandonar portabilidad y superficie mínima.

### 3.6 Evaluación

- Experimento A: un proyecto piloto con `.planning/`-like spine **solo** (sin portar GSD).
- Experimento B: medir tokens de skill listing: `core` 10 vs `core`+namespace meta-descriptions.
- Experimento C: harness test de propagación de instrucciones a worker (fail si no lee AGENTS.md).

---

## 4. ECC (`affaan-m/ECC`)

### 4.1 Hechos verificados

| Hecho | Evidencia |
|-------|-----------|
| ~238k★, push 2026-08-05 | **V** API |
| README: 67 agents, 281 skills, 94 command shims, hooks, memory, AgentShield | **C/V** README; **V** `ls skills/` = 281 dirs |
| Loop marketing: plan→test→implement→review→verify→remember→improve | **C** README |
| Continuous Learning v2.1: instincts atómicos, confidence, project-scoped, evolve→skill | **V** `skills/continuous-learning-v2/SKILL.md` + `instinct-cli.py` |
| Memory Vault `ecc.memory.v1`: markdown source of truth, trust unreviewed, create-only, no auto-promotion | **V** `docs/design/ecc-memory-vault.md` |
| Hooks densos: bash dispatcher, config-protection, observe continuous-learning, governance-capture, compact suggest | **V** `hooks/hooks.json` |
| `search-first` research-before-code | **V** skill |
| `skill-scout` search local/marketplace/GitHub before creating skills | **V** skill |
| AgentShield security scan de configs/hooks/MCP | **V** `skills/security-scan` |
| Rules packs por lenguaje (no en plugin Claude; copy manual) | **V** README + `rules/` |
| Issues: Windows path bugs memory (#2626), observer path (#2673), hookify no enforced (#2561), instincts ranking (#2371) | **V** issues |

### 4.2 Arquitectura (I)

ECC es el **competidor de amplitud**: kit operativo completo + learning + security productizado. Duplica conceptualmente:

| ECC | Agentit |
|-----|---------|
| agents especializados | roles adaptativos + skills |
| hooks enforcement | política de no-hooks-auto + harden-local |
| memory vault | artifact_ref (otro problema: handoff durable vs archive ruidoso) |
| instincts/preferences learned | `preferences.yaml` estático + applied_preferences |
| skill-scout | scout + find-skills |
| megaskill catalog | core acotado |

**I:** El valor no está en las 281 skills; está en **(1) instincts**, **(2) memory trust model**, **(3) AgentShield-like scan**, **(4) search-first**.

### 4.3 Capacidades extraídas

| ID | Capacidad | Decisión | Agentit existente | Gap |
|----|-----------|----------|-------------------|-----|
| ECC-01 | Instincts (atomic learned behaviors + confidence + scope) | `context_provider` / experiment | `preferences.yaml` | Preferencias son estáticas; no hay observación de correcciones de sesión. |
| ECC-02 | Memory vault unreviewed + human promotion | `context_provider` | artifacts | Falta modelo de trust explícito: memory ≠ instruction. |
| ECC-03 | Continuous observation hooks → learning | `reject` como default | — | Hooks siempre-on + observer Haiku: coste, privacidad, fallos Windows. |
| ECC-04 | search-first before coding | `enhance_existing` | `source-driven-development`, `find-skills` | Gate “adopt/extend/build” antes de greenfield utils. |
| ECC-05 | skill-scout before create | `already_covered` / enhance | `find-skills`, scout | Ya alineado; reforzar en using-agent-skills. |
| ECC-06 | AgentShield config/hook/MCP scan | `integration` | harden-local.sh | Ampliar a scan de skills/hooks MCP de terceros. |
| ECC-07 | config-protection (no debilitar linters) | `router_rule` / skill security | `security-and-hardening` | Regla: no “fix” aflojando eslint. |
| ECC-08 | 67 specialized agents | `reject` | adaptive roles | Especialización masiva contradice single-first. |
| ECC-09 | 281 skills install | `scout_source` / `reject` install | profiles | Solo índice scout. |
| ECC-10 | Cross-harness sync (Codex path, etc.) | `already_covered` (parcial) | multi-provider install | ECC más maduro en packaging; Agentit gana en neutralidad/safety. |

### 4.4 Riesgos ECC → Agentit

- **Complejidad y superficie de ataque de hooks** (issues de payload echo, gates no documentados).
- **Instincts como instrucciones silenciosas:** ECC mitiga con confidence y project scope (**V**); Agentit debe exigir **review humano** antes de que un instinct se comporte como rule.
- **Megapack mental:** instalar ECC “para no reinventar” destruiría el core-10.

### 4.5 Evaluación

- Prototype memory vault mínimo (3 kinds: fact, handoff, preference) con `trust: unreviewed`.
- No implementar continuous-learning hooks hasta threat model + opt-in.
- Comparar harden-local vs AgentShield en un proyecto fixture (checklist de findings).

---

## 5. Matt Pocock skills (`mattpocock/skills`)

### 5.1 Hechos verificados

| Hecho | Evidencia |
|-------|-----------|
| ~204k★, push 2026-08-05 | **V** API |
| Catálogo pequeño y curado (engineering + productivity + misc) | **V** árbol `skills/skills/` |
| `grilling`: design tree, rounds, frontier de preguntas, facts vía subagent | **V** `productivity/grilling/SKILL.md` |
| `grill-me` → wrapper a grilling | **V** |
| `writing-for-agents`: context pointers, context vs cognitive load, completion criteria, progressive disclosure, leading words | **V** skill denso |
| `diagnosing-bugs`: feedback loop red-capable obligatorio antes de hipótesis | **V** |
| `prototype`: throwaway logic HTML o UI variants | **V** |
| `to-spec` / `to-tickets` / `tdd` / `code-review` / `research` / `implement` | **V** |
| `wait-what`: re-pitch en STE + ubiquitous language | **V** |
| Codex `agents/openai.yaml` support (changelog claim X/session prior) | **C** (no re-leído package completo aquí) |

### 5.2 Naturaleza del sistema (I)

No es un harness. Es una **biblioteca de prácticas de ingeniería de alta densidad lingüística** — especialmente elicitation y escritura para agentes. El valor es la **calidad del proceso**, no la orquestación.

### 5.3 Capacidades extraídas

| ID | Capacidad | Decisión | Agentit existente | Gap |
|----|-----------|----------|-------------------|-----|
| MP-01 | Grilling por rounds + design tree + frontier | `enhance_existing` | `interview-me` (1Q at a time + hypothesis/confidence) | Agentit ya es fuerte; falta **rounds multi-pregunta del frontier** y mapa de decisiones. |
| MP-02 | writing-for-agents (pointers, hierarchy, completion criteria) | `enhance_existing` | `using-agent-skills`, docs de skills | Skill o sección canónica para **autores** de AGENTS.md/skills Agentit. |
| MP-03 | Feedback-loop-first debugging | `enhance_existing` | `debugging-and-error-recovery` | Enfatizar “no hypothesis without red command already run”. |
| MP-04 | Prototype throwaway (logic/UI) | `new_skill` (perfil product/design) | — | Rápido validar modelos de estado; no core. |
| MP-05 | Research as background agent → markdown cited | `enhance_existing` | `source-driven-development` | Path artifact + primary sources. |
| MP-06 | to-spec synthesis without re-interview | `enhance_existing` | `spec-driven-development` | Modo “sintetiza conversación actual”. |
| MP-07 | wait-what re-pitch | `reject` / trivial | anti-slop writing | Opcional; bajo ROI. |
| MP-08 | Domain modeling / wayfinder / wizard | `scout_source` | — | Cherry-pick caso a caso. |

### 5.4 Overlap con interview-me (detalle)

**V interview-me:** hipótesis + confidence, una pregunta a la vez, recommended answer, stop ≥95%, non-interactive ban.

**V grilling:** design tree, **toda la frontier** en un round (multi-Q numeradas), facts vía subagent, fin cuando frontier vacía.

**I:** No son equivalentes. Agentit gana en stop conditions y non-interactive safety; Matt gana en **cobertura de árbol de decisiones** y paralelismo de preguntas no dependientes. Decisión: **enhance `interview-me`**, no clonar `/grilling` completo.

### 5.5 Evaluación

- A/B: misma feature ambigua; interview-me vs interview-me+frontier rounds; contar supuestos residuales en el design final.
- Audit de 5 SKILL.md de Agentit con checklist writing-for-agents (pointers, completion criteria).

---

## 6. Matriz cruzada de solapamientos

| Capacidad | Superpowers | GSD | ECC | Matt | Agentit hoy | Decisión neta |
|----------|-------------|-----|-----|------|-------------|----------------|
| Single-agent-first | No (process-first) | No (phase multi-agent) | Agent-first specialists | N/A | Sí | **preserve** |
| Pre-code design gate | Hard | Discuss phase | Plan | Grill | Soft | **enhance** |
| Skill discovery cost | Few skills + bootstrap | Namespace routers | 281 skills risk | Few skills | Profiles JIT | **enhance routers** |
| Fresh worker + review | SDD | Execute waves | Review agents | implement+review | Adaptive | **enhance contracts** |
| Project instr. to workers | Prompt templates | CLAUDE.md read (post-#671) | rules packs | N/A | Partial | **enhance** |
| Verification iron law | Explicit skill | Verify phase | verify loop | tdd/debug | Partial | **enhance** |
| Cross-session memory | Specs/plans files | `.planning/` | Memory vault | handoff skill | artifacts | **experiment vault** |
| Learned preferences | No | profile-user | Instincts | No | static prefs | **experiment** |
| Security of agent config | Low surface | capability trust | AgentShield | git guardrails | harden-local | **enhance scan** |
| Research-first | brainstorm context | RESEARCH.md | search-first | research skill | source-driven | **enhance** |
| Writing for agents | writing-skills TDD | skill frontmatter contracts | skill-scout | writing-for-agents | partial | **enhance** |

---

## 7. Contradicciones entre los cuatro (no resolver copiando todos)

1. **Auto-trigger máximo (Superpowers)** vs **opt-in profiles (Agentit)** vs **command-driven phases (GSD)**.
2. **Few process skills (Superpowers/Matt)** vs **hundreds (ECC)** — Agentit debe quedarse en el primer campo.
3. **Multi-agent default (GSD/ECC)** vs **multi-agent exceptional (Agentit)** — no ceder el default.
4. **Memory as unreviewed context (ECC)** vs **memory as planning truth (GSD STATE)** — no mezclar: facts ≠ state machine.
5. **Hooks always-on (ECC/Superpowers bootstrap)** vs **Agentit no hooks sin allowlist**.

---

## 8. Ranking: máximo 10 capacidades dignas de experimento

Orden por **ROI para Agentit** (problema real × factibilidad × alineación filosófica × riesgo bajo).

### 1. Worker instruction projection contract (GSD #671 lesson)

- **Decisión:** `enhance_existing` (architect-orchestrator + worker agents)
- **Problema:** workers “fresh” ignoran AGENTS.md/skills del proyecto → regresiones de seguridad/estilo.
- **Experimento:** checklist mandatoria en prompt de worker; test unitario del template; caso fixture con rule prohibida.
- **Eval:** 0 violaciones de rule en 5 spawns adversariales.

### 2. Verification-before-completion iron law (Superpowers)

- **Decisión:** `enhance_existing` (router verification + skill core o párrafo en AGENTS.md)
- **Problema:** claims de done sin evidencia de comando en el turno.
- **Experimento:** regla en core AGENTS + 10 escenarios de eval manual.
- **Eval:** tasa de claims sin evidencia → 0 en suite.

### 3. Namespace / cluster discovery over flat skill list (GSD routers × Agentit profiles)

- **Decisión:** `router_rule`
- **Problema:** “2% problem” — listing de skills come tokens; perfiles ayudan pero el router aún recomienda poco en tasks no reconocidas.
- **Experimento:** 6–8 cluster descriptors keyword-dense (como ns-*) que mapean a profiles/skills sin instalar 80 skills.
- **Eval:** tokens de discovery listing + precision@k en 20 tasks etiquetadas.

### 4. Interview-me frontier rounds (Matt grilling)

- **Decisión:** `enhance_existing` (`interview-me`)
- **Problema:** una pregunta a la vez deja ramas del design tree sin explorar o alarga innecesariamente.
- **Experimento:** modo “frontier round” cuando confidence &lt; 70% y ≥2 preguntas independientes.
- **Eval:** supuestos residuales en design doc; tiempo a shared understanding.

### 5. writing-for-agents checklist for Agentit authors (Matt)

- **Decisión:** `enhance_existing` (`using-agent-skills` + CONTRIBUTING/docs)
- **Problema:** skills Agentit varían en completion criteria y pointers → invocación irregular.
- **Experimento:** aplicar checklist a 5 skills core; medir trigger false negatives.
- **Eval:** revisión humana + 5 prompts de invocación.

### 6. Plan junior-proof + task self-review (Superpowers writing-plans / implementer)

- **Decisión:** `enhance_existing` (`planning-and-task-breakdown`)
- **Problema:** planes ambiguos fallan en workers.
- **Experimento:** template de task con acceptance + files + test command + escalate conditions.
- **Eval:** un worker externo ejecuta plan sin chat history.

### 7. Project spine STATE/CONTEXT optional (GSD, stripped)

- **Decisión:** `context_provider` (no copiar GSD)
- **Problema:** work multi-sesión sin spine pierde decisiones.
- **Experimento:** `.agentit/STATE.md` + `CONTEXT.md` opcionales para topology plan/pipeline; integración con artifact_ref.
- **Eval:** reanudar sesión tras /clear con solo spine → decisiones correctas.

### 8. Memory vault unreviewed (ECC trust model, mínimo)

- **Decisión:** `context_provider`
- **Problema:** artifact_ref archiva ruido; no hay handoffs/preferencias con trust.
- **Experimento:** schema mínimo handoff/fact/preference; create-only; no auto-inject as rules.
- **Eval:** threat model + 3 harnesses leen el mismo markdown.

### 9. search-first / adopt-extend-build gate (ECC + source-driven)

- **Decisión:** `enhance_existing` (`source-driven-development` + router signal)
- **Problema:** reimplementar lo que ya existe en deps/skills.
- **Experimento:** para “add utility X”, forzar tabla adopt|extend|build.
- **Eval:** 10 tareas; % de reinventos evitados.

### 10. Agent config/skill security scan (ECC AgentShield × harden-local)

- **Decisión:** `integration`
- **Problema:** skills/hooks/MCP de terceros = supply chain.
- **Experimento:** extender harden-local o script dry-run que escanee SKILL.md/hooks por secrets, curl|bash, over-broad tools.
- **Eval:** fixtures maliciosos detectados; 0 false block en core.

### Explicitly deferred (not in top 10)

| Capacidad | Por qué no ahora |
|-----------|------------------|
| Superpowers SessionStart bootstrap global | viola no-hooks-auto |
| ECC continuous-learning hooks always-on | privacidad, flakiness, Windows bugs |
| ECC 281 skills / 67 agents install | antítesis core-10 |
| GSD full phase product | reescribe Agentit |
| Instincts auto-promotion | requiere governance madura post-vault |
| Smart-zone token estimators | dependencia de phase system |

---

## 9. Propuestas etiquetadas (formato pedido)

### 9.1

```yaml
capability: requirements_grilling_frontier_rounds
source: mattpocock/skills (grilling)
agentit_existing:
  - interview-me
  - idea-refine
overlap: high
gap:
  - multi-question frontier rounds
  - explicit design-tree map
  - subagent fact-finding while user decides
decision: enhance_existing
problem: residual assumptions after linear Q&A
eval: residual-assumption count on 5 ambiguous features
```

### 9.2

```yaml
capability: pre_implementation_hard_gate
source: obra/superpowers (brainstorming HARD-GATE)
agentit_existing:
  - interview-me
  - spec-driven-development
  - planning-and-task-breakdown
overlap: medium
gap:
  - enforceable no-code-until-design-approved for non-trivial work
  - mechanical-task exclusion (avoid Superpowers issue #2076)
decision: router_rule  # + light enhance of planning skills
problem: agents jump to code on medium features
eval: false_positive rate on renames vs hit rate on features
```

### 9.3

```yaml
capability: worker_project_instruction_projection
source: open-gsd/gsd-core (post-#671 executor project_context) + gsd-build#671
agentit_existing:
  - architect-orchestrator
  - agents/worker.md
overlap: medium
gap:
  - mandatory read of project AGENTS/CLAUDE/CODEX
  - skill/profile discovery in worker prompt
  - regression tests for projection
decision: enhance_existing
problem: fresh workers ship policy-violating code
eval: adversarial fixture with forbidden pattern
```

### 9.4

```yaml
capability: two_stage_skill_namespace_discovery
source: open-gsd/gsd-core (ns-* routers, #2792)
agentit_existing:
  - profiles.yaml
  - task-router
  - using-agent-skills
overlap: high (same problem class)
gap:
  - keyword-dense cluster descriptors for router output
  - runtime-aware flat vs nested note (don't nest on Claude Skill tool)
decision: router_rule
problem: discovery token cost + low skill recommendation confidence
eval: listing tokens + precision@k
```

### 9.5

```yaml
capability: verification_before_completion_iron_law
source: obra/superpowers (verification-before-completion)
agentit_existing:
  - router verification block
  - test-driven-development
  - code-review-and-quality
overlap: medium
gap:
  - same-turn fresh command evidence required for success claims
decision: enhance_existing
problem: false "done" reports
eval: transcript audit 20 tasks
```

### 9.6

```yaml
capability: unreviewed_memory_vault
source: affaan-m/ECC (ecc.memory.v1 design)
agentit_existing:
  - router/artifact_ref.py
  - router/dedup.py
overlap: low-medium
gap:
  - trust model (memory ≠ instruction)
  - create-only handoffs/preferences
  - human promotion path
decision: context_provider
problem: no durable cross-session operator memory with safety boundary
eval: threat model + multi-harness read of same files
```

### 9.7

```yaml
capability: writing_for_agents_authoring_standard
source: mattpocock/skills (writing-for-agents)
agentit_existing:
  - using-agent-skills
  - skill frontmatter practice
overlap: medium
gap:
  - context pointer craft
  - completion criteria clarity
  - progressive disclosure rules for SKILL.md
decision: enhance_existing
problem: uneven skill trigger quality in catalog
eval: rewrite 5 core skills; invocation tests
```

### 9.8

```yaml
capability: search_first_adopt_extend_build
source: affaan-m/ECC (search-first)
agentit_existing:
  - source-driven-development
  - find-skills
overlap: medium
gap:
  - explicit decision matrix before greenfield helpers
decision: enhance_existing
problem: reinvented utilities and ignored packages/skills
eval: 10 "add X" tasks reinvent rate
```

### 9.9

```yaml
capability: optional_project_planning_spine
source: open-gsd/gsd-core (.planning STATE/CONTEXT)
agentit_existing:
  - plan+direct topology
  - artifact references
  - spec-driven-development
overlap: medium
gap:
  - lightweight STATE.md across sessions without full GSD
decision: context_provider
# NOT new_topology full phase product
problem: multi-session drift on long projects
eval: resume-after-clear accuracy
```

### 9.10

```yaml
capability: agent_supply_chain_scan
source: affaan-m/ECC (AgentShield) + agentit security/harden-local.sh
agentit_existing:
  - security/harden-local.sh
  - security-and-hardening skill
overlap: medium
gap:
  - scan third-party skills/hooks/MCP for injection and secrets
decision: integration
problem: scout/import path without safety gate
eval: malicious fixture suite
```

### 9.11 (reject samples)

```yaml
capability: sessionstart_mandatory_skill_bootstrap
source: obra/superpowers hooks/session-start
decision: reject  # as default; optional provider profile only
reason: conflicts with Agentit no-auto-hooks policy

capability: install_ecc_full_skill_catalog
source: affaan-m/ECC
decision: reject
reason: destroys core-10 context budget; use scout_source only

capability: default_multi_agent_phase_loop
source: open-gsd/gsd-core
decision: reject
reason: contradicts single-agent-first; optional spine only
```

---

## 10. Qué NO hacer (lista corta)

1. No hacer `npx` install de Superpowers/ECC/GSD en el core Agentit.
2. No copiar 281 skills ni 67 agents.
3. No activar continuous-learning observers por defecto.
4. No anidar skills en layout Claude-like si el Skill tool hard-errors (lección GSD #924).
5. No tratar estrellas como quality signal de seguridad multi-agente (ver #671 y #2050).

---

## 11. Orden de implementación sugerido (post-informe)

1. **Worker projection contract** + test (riesgo real, bajo coste).
2. **Verification iron law** en AGENTS/core.
3. **interview-me frontier rounds**.
4. **writing-for-agents** audit de core skills.
5. **Router cluster descriptors** (GSD-like, Agentit-native).
6. **Optional STATE/CONTEXT spine**.
7. **Memory vault MVP** (trust model).
8. **search-first gate**.
9. **Supply-chain scan** extension.
10. Recién entonces: instincts experiment (opt-in, no hooks globales).

---

## 12. Apéndice: inventario de skills Superpowers (V)

| Skill | Rol |
|-------|-----|
| using-superpowers | bootstrap / invoke-before-act |
| brainstorming | design hard-gate |
| writing-plans | plan junior-proof |
| executing-plans | plan execution session |
| subagent-driven-development | SDD loop |
| dispatching-parallel-agents | fan-out |
| test-driven-development | TDD iron law |
| systematic-debugging | root-cause gate |
| requesting-code-review | dispatch reviewer |
| receiving-code-review | anti-sycophancy review response |
| verification-before-completion | evidence gate |
| using-git-worktrees | isolation |
| finishing-a-development-branch | integrate options |
| writing-skills | TDD for skills |

## 13. Apéndice: GSD namespace routers (V)

| Router name | description keywords (frontmatter) |
|-------------|--------------------------------------|
| gsd-workflow | workflow \| discuss plan execute verify phase progress |
| gsd-project | project lifecycle \| milestones audits summary |
| gsd-quality | quality gates \| code review debug audit security eval ui |
| gsd-context | codebase intel \| map graphify docs learnings mempalace |
| gsd-manage | config workspace \| workstreams thread update ship inbox |
| gsd-ideate | exploration capture \| explore sketch spike spec capture |

## 14. Apéndice: Matt skills engineering+productivity (V)

engineering: ask-matt, codebase-design, code-review, diagnosing-bugs, domain-modeling, grill-with-docs, implement, improve-codebase-architecture, prototype, research, resolving-merge-conflicts, setup-matt-pocock-skills, tdd, to-spec, to-tickets, triage, wayfinder, wizard  

productivity: grill-me, grilling, handoff, teach, to-questionnaire, wait-what, writing-for-agents

## 15. Limitaciones de este deep dive

- Clones **depth 1**; no historia completa ni todos los ADRs GSD.
- No se ejecutaron los harnesses en vivo (Claude/Codex) con cada plugin.
- Conteos de estrellas son snapshot 2026-08-05 y varían.
- ECC `skills/` 281 vs README números de agents: no se auditó calidad skill-by-skill.
- Addy Osmani (`addyosmani/agent-skills`, ~82k★) quedó fuera del top-4 pedido; útil como follow-up de cherry-pick engineering.

---

## 16. Conclusión

Los cuatro sistemas **no** piden ser importados. Piden ser **diseccionados**:

| Sistema | Aporte principal a Agentit |
|---------|----------------------------|
| Superpowers | Disciplina de proceso con iron laws y contratos SDD |
| GSD Core | Context rot + discovery cost + lección de proyección a subagentes |
| ECC | Trust model de memoria, instincts (futuro), security scan, search-first |
| Matt Pocock | Elicitation de frontera y escritura de documentos para agentes |

Agentit ya tiene la **arquitectura correcta** (single-first, profiles, router, scout, context engines). El gap no es “más skills”; es **endurecer gates, contracts y discovery** con piezas concretas de los cuatro, medidas con experimentos pequeños y reversibles.

**Siguiente paso natural:** implementar el experimento #1 (worker instruction projection) como PR aislado, sin instalar ningún harness externo.
