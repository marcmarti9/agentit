# Optimización de contexto y tokens

El objetivo es el coste total de una tarea correcta, no el menor número bruto de tokens. Cuenta lecturas, caché, output, subagentes, repeticiones, recuperaciones y tiempo de ejecución.

## Perfiles de respuesta

- `VERBOSE_ALLOWED`: arquitectura, seguridad, incidentes, decisiones de alto impacto, documentación importante y enseñanza.
- `STANDARD`: trabajo normal, con decisiones y verificación suficientes.
- `TERSE_SAFE`: confirmaciones inequívocas, progreso rutinario, explicaciones simples y cambios triviales.

La concisión elimina relleno; nunca elimina rutas, números, errores, decisiones, restricciones, incertidumbre o pasos de verificación importantes.

## Progressive disclosure

El contexto inicial contiene solo el nombre, descripción, trigger, coste, riesgo y ruta de una skill. Carga su cuerpo completo después de seleccionarla. Deduplica exactamente por hash cuando dos bloques son idénticos; no deduzcas que dos bloques parecidos son intercambiables.

## Compresión

Por defecto solo se permite deduplicación exacta. Una recuperación reversible puede usarse únicamente en contenido no crítico cuando el original completo permanece local, tiene un identificador estable, se indica lo omitido y se puede recuperar por rango. Si el contenido puede influir en una acción RISK_3/RISK_4, recupera el original antes de decidir.

La compresión semántica es experimental y solo apta para prosa repetitiva o conocimiento secundario recuperable. Está prohibida para código que se vaya a modificar, SQL, migraciones, esquemas, contratos, comandos, secretos, errores exactos, diffs, límites, números, negaciones y controles de seguridad.

## Métricas

Registra ahorro bruto, ahorro neto, tokens de ventana, coste económico, duración, éxito, tests, regresiones, repeticiones, archivos releídos, llamadas adicionales y recuperaciones. No declares una mejora si el ahorro de una salida provoca repeticiones o una pérdida de calidad.
