# Plan de evaluación

## Objetivo

Evaluar exactitud, fidelidad y reversibilidad sin ejecutar operaciones destructivas reales. El router se prueba como heurística de planificación: nunca como ejecutor ni autorización. Las decisiones críticas requieren revisión humana.

## Fase A: contrato local

- riesgo por intención y entorno: explicación de backup, documentación de `chmod`, landing sobre backups y restore real en producción;
- separación de `skills_available`, `skills_recommended_missing` y el alias heredado `skills`;
- fallo cerrado ante catálogo ausente, YAML inválido, IDs duplicados, estados desconocidos, escape de rutas o dependencias esenciales ausentes;
- condición PostgreSQL/Supabase frente a SQLite;
- generación atómica del inventario local ignorado;
- sintaxis shell, YAML y JSON.

## Fase B: scripts en entorno desechable

- opciones incompatibles rechazadas antes de cualquier escritura;
- instalación y actualización por proveedor en HOME temporal;
- preservación de archivos no relacionados y rechazo de symlinks;
- backups privados (`0700`), copias privadas (`0600`), hashes y `original_mode` en el manifiesto;
- rollback simulado: restaurar reemplazos con hash y modo verificados; eliminar un destino nuevo solo si su hash actual coincide con `destination_sha256`;
- ejecución objetivo en Linux con Bash 4+ y utilidades GNU.

## Fase C: fidelidad y tareas representativas

Usar fixtures de logs, JSON, tablas, código, SQL, diffs, errores, hashes, IDs, rutas, números, negaciones, pipes y redirecciones. Comparar stdout, stderr, exit code, orden y recuperación exacta. Incluir UI trivial, bug, feature, auth, migración simulada, marketing, documentación, SQLite y PostgreSQL.

## Métricas

Registrar bytes/palabras originales y adaptados, skills recomendadas/cargadas, llamadas de herramienta, output, subagentes, recuperaciones, repeticiones, duración, tests y regresiones. No publicar cifras de reducción de contexto, tokens o coste sin un baseline comparable.

## Criterios de promoción

Un componente solo se promueve si conserva contenido crítico y exit codes, tiene rollback comprobable, no aumenta repeticiones y mejora un conjunto representativo. Un fallo adversarial en contenido crítico bloquea la promoción. Los resultados locales y GitHub Actions se registran por separado; nunca se infiere el estado de CI a partir de una ejecución local.
