# Denylist y allowlist de compresión

Esta política es una barrera de seguridad. El contexto concreto de la tarea tiene prioridad y puede prohibir más cosas.

## Denylist inicial: nunca comprimir destructivamente

- eliminación, `DROP`, `TRUNCATE`, `DELETE`, restore, backup o migración;
- SQL de escritura, esquemas, permisos, credenciales y configuración crítica;
- errores, stderr, stack traces, diffs, `git status` cuando se necesita la lista completa y comprobaciones posteriores;
- comandos con pipes, redirecciones, `&&`, `;`, sustitución, pipelines o stdout redirigido;
- código fuente, archivos afectados, rutas, hashes, IDs, cantidades, fechas y números críticos;
- contratos de API, requisitos con negaciones o excepciones e instrucciones de seguridad;
- cualquier contenido de RISK_3/RISK_4 que pueda afectar a la decisión;
- cualquier salida cuyo original no pueda recuperarse con un identificador estable.

## Allowlist inicial, siempre condicionada

- logs repetitivos no críticos;
- progreso decorativo de compilación o instalación;
- tests exitosos repetitivos cuando el fallo completo queda visible;
- tablas o JSON grandes que puedan recuperarse exactamente;
- resultados de búsqueda voluminosos no críticos;
- explicaciones internas redundantes y output rutinario de `TERSE_SAFE`.

## Reglas de recuperación

El adaptador debe conservar el original, indicar que hubo reducción, registrar el identificador y permitir recuperación explícita. No recuperes automáticamente un bloque completo si basta un rango. Antes de una acción de riesgo alto, recupera todo el bloque que pueda influir en ella y registra esa recuperación.
