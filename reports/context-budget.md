# Presupuesto de contexto

Las cantidades siguientes son aproximaciones basadas en palabras/bytes locales, no consumo facturado de un modelo. La conversión exacta depende del tokenizer y del proveedor.

## Baseline observado

| Archivo | Bytes | Palabras | Riesgo de carga global |
|---|---:|---:|---|
| `/home/Marc/AGENTS.md` | 2,657 | 328 | core, razonable pero debe permanecer mínimo |
| `/home/Marc/CLAUDE.md` | 2,613 | 327 | provider, no cargar junto a duplicados innecesarios |
| `/home/Marc/CODEX.md` | 2,593 | 319 | provider, no cargar junto a duplicados innecesarios |
| `architect-orchestrator/SKILL.md` | 4,836 | 636 | alto si se carga en cada tarea |
| `supabase-postgres-best-practices/SKILL.md` | 2,576 | 337 | solo DB/Postgres |

Las copias globales de skills y el catálogo de Gemini no equivalen automáticamente a tokens inyectados en cada prompt, pero sí aumentan superficie de selección, riesgo de duplicado y tiempo de descubrimiento.

## Target propuesto

1. **Contexto inicial:** guía global mínima, metadata del registro y router; no cuerpos completos de skills.
2. **RISK_0/RISK_1:** 0–1 skill; solo perfil `TERSE_SAFE` cuando no se pierda claridad.
3. **RISK_2:** 1–3 skills seleccionadas, sin compresión semántica de código o errores.
4. **RISK_3/RISK_4:** contexto completo recuperable y revisión; el ahorro es secundario.

El nuevo `router/SKILL.md` tiene 383 palabras. Las cuatro políticas suman 902 palabras; no deben cargarse todas en cada conversación: `risk-classification` y la parte aplicable de `compression-denylist` bastan normalmente. `registry.yaml` contiene 1,246 palabras de metadata para 17 entradas y debe consumirse como índice, no como prompt completo repetido.

## Estimación antes/después

| Escenario | Antes observado | Después recomendado | Confianza |
|---|---|---|---|
| explicación simple | guía/provider + historial; sin skill necesaria | router/metadata, 0 skills, `TERSE_SAFE` | media; falta telemetría provider |
| CSS localizado | posible selección manual de bundles | router + 0–1 skill de frontend | media |
| bug estándar | riesgo de cargar metodología y skills duplicadas | router + debugging/TDD solo si aportan | media |
| feature mediana | Superpowers/Addy potencialmente simultáneos | una metodología + skills de dominio | media |
| auth/migración | salida completa y revisión | igual o más contexto, sin compresión destructiva | alta por política |

No se declara porcentaje de ahorro neto: no existe aún una medición de tokens totales, repeticiones ni coste del provider. El primer objetivo medible es reducir skills cargadas y archivos releídos, no perseguir un porcentaje externo.

## Contadores que faltan

El harness debe registrar por tarea: hash de prompt/contexto, skills seleccionadas, palabras/bytes leídos, llamadas de herramienta, output, subagentes, recuperaciones, repeticiones, duración, tests y resultado. Para proveedores sin telemetría fiable se reportan bytes/palabras como proxy y se marca la incertidumbre.
