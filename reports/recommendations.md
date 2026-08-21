# Recomendaciones integradas

**Estado:** recomendaciones vigentes para el diseño del repositorio tras el refactor LLM-native. No constituyen por sí solas autorización de seguridad, despliegue ni publicación.

## Conservar como núcleo

- La IA principal interpreta la petición con todo el contexto disponible y es la propietaria de `TASK_DECISION`.
- No existe un router semántico programado: nada de regex, keywords, scoring o clasificadores Python para decidir intención, categoría, riesgo, topología, skills o delegación.
- Antes de trabajo material, un modelo barato independiente audita la decisión con `CLEAR / CHALLENGE / ESCALATE`; no sustituye al principal.
- `RISK_3/RISK_4`, trabajo destructivo o difícil de revertir, auth, pagos, secretos, PII, producción, migraciones significativas y planes estructurales grandes requieren además revisión fuerte independiente.
- La delegación se decide por beneficio real: especialidad, aislamiento, independencia, amplitud, latencia o juicio fresco. No hay single-agent-first ni multi-agent-forzado.
- `registry.yaml`, `profiles.yaml`, catálogos y manifests son inventarios/política mecánica, no clasificadores de lenguaje natural.
- Progressive disclosure, deduplicación exacta y preservación íntegra de comandos, SQL, errores, diffs, rutas, hashes y números siguen siendo garantías útiles.
- Instalador y actualizador permanecen plan-first, con manifiesto, ownership claro y rollback verificable.

## Selección y carga de skills

La IA principal elige el conjunto mínimo útil después de inspeccionar el contexto real. Una skill no se considera usada por aparecer en un ID, perfil o manifest: el modelo que ejecuta la etapa debe leer su `SKILL.md` o recibir una inyección provider-native equivalente.

Las skills específicas de dominio necesitan evidencia real del dominio. Por ejemplo, `supabase-postgres-best-practices` requiere contexto PostgreSQL/psql/Supabase; la palabra genérica “database” no basta.

## Runtime de ejecución

Eliminar el router semántico no elimina Loop/Graph Engineering.

- Toda unidad ejecutable con resultado verificable usa Loop Contract y solo se acepta con evidencia fresca + Loop Receipt válido.
- Todo trabajo multi-nodo materializa Graph Contract con dependencias, ownership y handoffs; la aceptación final necesita Graph Receipt respaldado por los Loop Receipts de sus nodos.
- Loop/Graph son infraestructura mecánica posterior a la decisión de la IA. No interpretan prompts.

## MCP

La IA principal selecciona explícitamente un `stack_id` a partir del contexto. `agentit mcp` y `agentit-manager` solo resuelven ese nombre y gestionan estado/configuración mecánicamente. No debe existir fallback de texto libre a heurísticas de stack.

## Inventario y plataforma

Generar la observación local con `python3 -m router.inventory`. `reports/local/inventory.yaml` permanece ignorado por Git y no debe contaminar el catálogo portable.

Los scripts shell requieren un entorno compatible con sus dependencias reales; antes de `--apply`, validar plataforma, paths, permisos y rollback.

## Componentes externos

Hooks, proxies, MCPs, wrappers y repositorios externos permanecen opt-in hasta revisar procedencia, permisos, red, fidelidad y rollback. Los estados del catálogo son decisiones de política, no afirmaciones sobre lo instalado en una máquina.

## Evidencia

No declarar `done`, `fixed` o `passing` sin evidencia fresca posterior al último cambio relevante y, con Agentit activo, sin el receipt Loop/Graph aplicable. El estado de GitHub Actions se registra solo después de una ejecución real sobre el HEAD correspondiente.
