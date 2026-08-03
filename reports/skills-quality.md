# Criterios de calidad de skills

Esta revisión describe decisiones del catálogo portable. No afirma qué está instalado, habilitado o operativo en una máquina; esa observación pertenece al inventario local ignorado.

## Criterios

Se valoran trigger, especificidad, utilidad marginal, pasos verificables, dependencia de herramientas, coste de contexto, solapamiento, seguridad y reversibilidad. Un estado del catálogo o una ruta existente no bastan para validar la calidad ni la compatibilidad de una skill.

## Decisiones de selección

| Elemento | Uso recomendado | Condición |
|---|---|---|
| `architect-orchestrator` | core bajo demanda | tarea multidominio, delegación explícita o revisión crítica; no para trabajo trivial |
| `security-hardening` | core para alto riesgo | auth, secretos, permisos, input externo o integración |
| `debugging-and-error-recovery` | bajo demanda | existe un fallo o diagnóstico concreto |
| `test-driven-development` | bajo demanda | hay lógica o comportamiento comprobable |
| `frontend-ui-engineering` | bajo demanda | UI, CSS, accesibilidad o responsive |
| `supabase-postgres-best-practices` | especializada | solo con señal Postgres/PostgreSQL/`psql`/Supabase; nunca por SQLite solamente |
| bundles y optimizadores externos | experimentales o referencia | revisar upstream, dependencias, solapamiento y rollback antes de promover |

## Semántica operativa

- `registry.yaml` expresa política portable mediante estado, prioridad, trigger, rutas plantilla y dependencias.
- El router solo pone una recomendación en `skills_available` si el estado es compatible, existe al menos una ruta y se cumplen dependencias esenciales.
- Una recomendación pertinente que no cumple esas condiciones aparece en `skills_recommended_missing`; no se sustituye por un resultado inventado.
- `skills` es un alias heredado de `skills_available`, no la lista total de recomendaciones.
- Las skills no pueden reducir el riesgo ni activar hooks, MCP o ejecución por sí solas.

La disponibilidad, versión y hash por máquina deben observarse con `python3 -m router.inventory`; una versión puede quedar sin observar.
