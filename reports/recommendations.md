# Recomendaciones integradas

**Estado:** baseline seguro aplicado al HOME; el push permanece bloqueado hasta completar la auditoría de los fixes finales.
**Prioridad:** corrección, integridad, seguridad y rollback preceden a contexto y coste.

El remoto `origin/main` ya contiene la arquitectura adaptativa del portátil en `eab20ca` (`docs/ADAPTIVE_AGENT_ARCHITECTURE.md`). Se integra como diseño superior al esquema fijo: mantiene nombres por compatibilidad, pero usa single-agent-first, probes, fan-out, pipelines y auditoría solo cuando el beneficio compensa la coordinación.

## Configuración recomendada

### Conservar como core

- guía global mínima con Architect como owner y topologías adaptativas, sin jerarquía obligatoria;
- arquitectura adaptativa de `origin/main`, con cero subagentes por defecto, contratos mínimos, ownership y loops acotados;
- router puro `router/route.py` y su skill de progressive disclosure;
- políticas de riesgo, anti-overengineering y denylist;
- una sola copia canónica del repositorio `agents-config`, con despliegues por manifiesto y hash;
- Addy Agent Skills como biblioteca de skills individuales, no como prompt global completo;
- `supabase-postgres-best-practices` solo para tareas Postgres/Supabase.

### Dejar bajo demanda

- Superpowers para features/bugs complejos donde spec/plan/TDD/worktree aporten valor;
- debugging, TDD, frontend, API, performance, seguridad y browser testing solo por trigger;
- Marketing Skills correcto (`coreyhaines31/marketingskills`) cuando se instale y valide, separado del `pm-skills` actual;
- Hallmark para diseño visual y No AI Slop para la revisión final de prosa pública;
- ECC por componentes seleccionados tras comparar solapamientos.

### Desactivar o no activar globalmente

- RTK auto-rewrite global, hooks de compresión y cualquier pipeline que modifique stdout sin fallback;
- compresión semántica en código, SQL, errores, diffs, comandos, números, requisitos y seguridad;
- tokless y scripts de instalación remota no revisados;
- OmniRoute como gateway: no está escuchando y no es necesario para este harness;
- hook PreCompact y `autoUploadSessions` en un baseline seguro hasta revisar privacidad, atomicidad, límites y consentimiento;
- `skipDangerousModePermissionPrompt: true` en una configuración segura.

La configuración de repositorio y HOME ya aplican la alternativa segura: aviso peligroso conservado, auto-upload desactivado, retención de 90 días y hook PreCompact fuera del baseline.

## Clasificación final de optimizadores

| Elemento | Decisión | Condición de promoción |
|---|---|---|
| Caveman | `ENABLE_BY_PROFILE` | solo `TERSE_SAFE`, comparación de claridad y output |
| RTK | `MANUAL_ONLY` | allowlist, pipes/redirects denegados, stdout raw recuperable, exit/stderr verificados |
| Headroom | `EXPERIMENTAL` por tarea | CCR local, ID estable, recuperación por rango y pruebas adversariales |
| context-compress | `MANUAL_ONLY` | batch de prosa secundaria y diff semántico revisado |
| tokless | `REJECT` para instalación automática | revisión de supply chain y necesidad demostrada |
| LLMLingua-2 | `EXPERIMENTAL` offline | originales retenidos y holdout adversarial sin pérdidas críticas |
| Agent Skills context engineering | `KEEP_AS_REFERENCE` | usar prácticas; no instalar duplicados completos |
| OmniRoute | `MANUAL_ONLY` | proceso verificado y ownership del proxy documentado |

## Contexto y ahorro esperado

La mejora de mayor confianza es progressive disclosure + deduplicación exacta + selección mínima. La compresión semántica no tiene aún ahorro neto medido. Antes/después se estima en `reports/context-budget.md`; cualquier porcentaje futuro debe incluir repeticiones, recuperaciones y subagentes.

## Conflictos y decisiones pendientes

1. Elegir una fuente canónica entre marketplace Addy, copias globales y repo local.
2. Decidir si Superpowers será la metodología estándar de deep work o una opción junto con Addy.
3. Instalar o no el repo correcto de Marketing Skills; no confundirlo con `pm-skills`.
4. Confirmar la ruta real de Antigravity para cada máquina; en este host el discovery global es `.agents`.
5. Añadir pruebas A/B de wrappers solo en un entorno desechable.
6. Revisar `agy`, las raíces confiadas de Antigravity y el proxy antes de cualquier optimización.

## Qué se implementó

- router conservador y pruebas unitarias;
- registro compacto con estados y triggers;
- políticas de riesgo, compresión y anti-overengineering;
- instalador multi-proveedor en modo plan por defecto, con backups, hashes, rechazo de symlinks y sin eliminaciones;
- actualizador con allowlist y opt-in de settings/hook;
- integración de `task-router` para Claude, Codex y Antigravity en el plan de despliegue.
- integración del commit remoto `eab20ca`; no se debe volver a la pirámide fija ni duplicar la arquitectura del portátil.

Se modificó el HOME real solo mediante backups/acciones explícitas descritas en el inventario; no se instaló ningún compresor ni se activó ningún MCP/proxy nuevo.
