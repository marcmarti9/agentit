# Auditoría de calidad de skills

**Fecha:** 2026-08-03
**Método:** lectura de los cuerpos locales relevantes y lectura de metadata/README de fuentes públicas solo cuando el repositorio no estaba instalado. “Hecho” significa observado en archivos; “recomendación” es decisión del harness.

## Criterios

Se valoraron trigger, especificidad, utilidad marginal, pasos verificables, salida, dependencia de versiones, coste de contexto, solapamiento, seguridad, reversibilidad y facilidad de evaluación. La calidad del nombre o de las estrellas no se consideró evidencia suficiente.

## Skills locales

| Elemento | Evidencia local | Calidad | Decisión |
|---|---|---|---|
| `architect-orchestrator` | `/home/Marc/agents-config/skills/architect-orchestrator/SKILL.md` y copias globales; activa jerarquía, niveles y auditoría | alta para tareas multidominio/críticas; demasiado ceremonial para trivial | `KEEP_CORE` como skill on-demand; Architect decide si delegar |
| `supabase-postgres-best-practices` | `SKILL.md`, `CHANGELOG.md` y referencias en el repo | específica y verificable para Postgres; coste alto si se carga fuera de DB | `KEEP_ON_DEMAND` |
| `context-engineering` | `/home/Marc/.agents/skills/context-engineering/SKILL.md` | buena guía de progressive disclosure, memoria y selección; no es un compresor ejecutable | `KEEP_CORE` como política de selección, no globalmente repetida |
| `security-and-hardening` | `/home/Marc/.agents/skills/security-and-hardening/SKILL.md` | fuerte para input no confiable, secretos, permisos y supply chain | `KEEP_ON_DEMAND`; se exige en RISK_3/RISK_4 |
| `debugging-and-error-recovery` | `/home/Marc/.agents/skills/debugging-and-error-recovery/SKILL.md` | pasos de causa raíz y verificación; útil solo ante fallos | `KEEP_ON_DEMAND` |
| `test-driven-development` | `/home/Marc/.agents/skills/test-driven-development/SKILL.md` | verificable, pero puede añadir ceremonia | `KEEP_ON_DEMAND`; no forzar en RISK_0/RISK_1 sin lógica |
| `incremental-implementation` | `/home/Marc/.agents/skills/incremental-implementation/SKILL.md` | útil para cambios de varios archivos; se solapa con metodología de desarrollo | `MERGE` conceptualmente con flujo del harness, no cargar siempre |
| `git-workflow-and-versioning` | `/home/Marc/.agents/skills/git-workflow-and-versioning/SKILL.md` | seguridad/reversibilidad de cambios; coste bajo si se invoca al modificar | `KEEP_ON_DEMAND` |
| `frontend-ui-engineering` | `/home/Marc/.agents/skills/frontend-ui-engineering/SKILL.md` | específica para UI funcional, responsive y accesibilidad | `KEEP_ON_DEMAND` |
| `code-review-and-quality` | `/home/Marc/.agents/skills/code-review-and-quality/SKILL.md` | revisión multidimensional; debe reservarse para cambios que lo justifiquen | `KEEP_ON_DEMAND` |
| `api-and-interface-design` | `/home/Marc/.agents/skills/api-and-interface-design/SKILL.md` | aporta límites y contratos públicos | `KEEP_ON_DEMAND` |
| `browser-testing-with-devtools` | skill local, requiere Chrome DevTools MCP | trigger claro, dependencia ausente porque no hay MCP configurado | `KEEP_ON_DEMAND`; marcar dependencia antes de seleccionar |

La salida del `gemini skills list` mostró aproximadamente 24 skills Addy habilitadas globalmente. No se debe convertir esa lista en contexto inicial completo: el registro debe exponer solo metadata y cargar el cuerpo seleccionado.

## Bundles solicitados

| Bundle | Estado real | Solapamiento | Decisión inicial |
|---|---|---|---|
| ECC | no clonado localmente; fuente remota observada | muy alto con ingeniería, memoria, seguridad, investigación, skills y orquestación | `KEEP_EXPERIMENTAL` por componentes; no instalar monolito |
| Superpowers | plugin Claude `6.2.0` instalado pero deshabilitado; cache `6.1.1` también presente | alto con spec/plan/TDD/subagentes/worktrees y Addy lifecycle | `KEEP_ON_DEMAND`; elegirlo como metodología principal solo cuando la tarea lo requiera |
| Agent Skills / Addy | marketplace local y copias globales | lifecycle, testing, review, shipping y frontend solapan con Superpowers | `KEEP_CORE` por skills individuales; consolidar fuente canónica |
| Marketing Skills | el repo de Corey no está instalado; existe `pm-skills` de Phuryn | marketing/product/growth; no son equivalentes por procedencia | `KEEP_ON_DEMAND`; no etiquetar `pm-skills` como Corey |
| Hallmark | no instalado localmente | diseño visual se cruza con frontend UI, pero no con backend | `KEEP_ON_DEMAND` solo en visual/audit/redesign |
| No AI Slop | no instalado localmente | revisión de prosa pública, no ingeniería | `KEEP_ON_DEMAND` como pasada final opcional |

## Reglas de calidad aplicadas

- Una skill no se conserva por duplicado solo porque venga de otro repositorio.
- Una variante profunda puede coexistir con una lite si cambia el nivel de riesgo o la calidad de verificación.
- Si una skill exige una herramienta ausente, el router la etiqueta como dependencia faltante y no inventa el resultado.
- Las skills no pueden cambiar la clasificación de riesgo ni activar hooks/MCP por sí solas.
- Todo upstream no instalado queda como hipótesis hasta revisar commit y archivos reales.
