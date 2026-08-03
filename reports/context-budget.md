# Presupuesto de contexto

Este documento define qué cargar, no afirma consumo facturado ni una reducción cuantitativa. La conversión entre bytes, palabras y tokens depende del proveedor y del tokenizer.

## Política de carga

1. **Contexto inicial:** guía global mínima y metadata seleccionada del catálogo; no cargar cuerpos completos de skills.
2. **RISK_0/RISK_1:** 0–1 skill y `TERSE_SAFE` solo cuando preserve claridad.
3. **RISK_2:** el conjunto mínimo de skills compatibles, sin compresión semántica de código, errores ni datos operativos.
4. **RISK_3/RISK_4:** originales recuperables, fidelidad completa cuando corresponda y revisión humana; el coste de contexto es secundario.

`registry.yaml` debe consumirse como índice de política portable. El router expone `skills_available` para cuerpos que podrían cargarse y `skills_recommended_missing` para recomendaciones no utilizables; el alias `skills` contiene solo las primeras. El inventario local no se inyecta completo en cada tarea.

## Escenarios de referencia

| Escenario | Carga recomendada |
|---|---|
| explicación simple | metadata mínima, sin skill salvo trigger explícito |
| CSS localizado | 0–1 skill de frontend si aporta verificación |
| bug estándar | debugging y/o TDD solo si son compatibles y útiles |
| feature mediana | una metodología y las skills de dominio necesarias |
| auth o migración | contexto completo recuperable y revisión, sin compresión destructiva |
| SQLite | guía general de base de datos; no cargar la skill específica de Postgres |
| PostgreSQL/Supabase | considerar `supabase-postgres-best-practices` si supera las comprobaciones locales |

## Medición pendiente

Para evaluar una mejora hay que registrar por tarea: bytes/palabras leídos, skills cargadas, llamadas de herramienta, output, subagentes, recuperaciones, repeticiones, duración, tests y resultado. Hasta disponer de esa telemetría comparativa no se publica una cifra de reducción de contexto, coste o tokens.
