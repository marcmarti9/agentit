# Plan de evaluación

## Objetivo

Medir calidad y coste total, no solo reducción de input. Cada caso debe conservar el original y el resultado completo en un fixture local. No se ejecutan operaciones destructivas reales.

El runtime se evalúa con la arquitectura adaptativa de `docs/ADAPTIVE_AGENT_ARCHITECTURE.md`: single-agent-first, cero subagentes por defecto, fan-out solo con independencia real y Auditor solo como gate de riesgo.

## Fases

### Fase A: smoke seguro (primera pasada)

- clasificación del router para explicación, CSS, bug, marketing, auth y producción;
- detección de diff/pipeline/SQL/secretos;
- validación de registry YAML;
- `bash -n` de instalador/actualizador;
- instalación en HOME temporal con archivo no relacionado para comprobar preservación;
- plan de actualización sin escritura.

### Fase B: fidelidad de contenido

Fixtures de logs, JSON, tablas, código, SQL, diffs, stack traces, hashes, IDs, rutas, números, negaciones, pipes, redirecciones y stdout redirigido. Comparar stdout, stderr, exit code, orden, líneas y recuperación exacta.

### Fase C: tareas representativas

1. cambio trivial de UI;
2. bug evidente;
3. bug desconocido;
4. feature pequeña;
5. feature mediana;
6. refactor;
7. revisión de seguridad;
8. operación de DB simulada;
9. migración simulada con rollback incompleto;
10. landing, copy comercial y CRO;
11. documentación y revisión de texto;
12. logs grandes, JSON grande, muchos tests exitosos con un fallo;
13. `git status`/`git diff` grande;
14. pipeline de shell.

### Fase D: comparativas

Para cada tarea, comparar solo cuando el adaptador esté instalado de forma aislada:

- baseline sin skill/compresión;
- configuración actual;
- router sin compresión;
- Caveman por perfil;
- RTK allowlisted;
- Headroom/CCR aislado;
- compresión semántica offline;
- skill A frente a skill B con solapamiento.

## Pruebas adversariales obligatorias

- fallo importante al final de miles de líneas;
- número crítico en tabla grande;
- negación que cambia el requisito;
- archivo peligroso omitido por truncado;
- stack trace cuya última línea no es la causa;
- comando con pipe y otro con redirección;
- JSON con claves repetidas pero valores distintos;
- migración con rollback incompleto;
- consulta aparentemente de lectura que modifica datos.

## Métricas

Registrar `input_no_cache`, creación/lecturas de cache, output, subagentes, repeticiones, recuperaciones, bytes/palabras originales y adaptados, duración, éxito, tests, regresiones, número de skills, archivos releídos y errores de compresión. Emitir ahorro bruto, neto, económico, de ventana y cambio de calidad por separado.

## Criterios de promoción

Ningún optimizador pasa a global por una sola tarea. Debe conservar exit codes y contenido crítico, tener rollback y fallback raw, no aumentar repeticiones, y demostrar mejora neta en un conjunto representativo. Un fallo adversarial en contenido crítico bloquea promoción.
