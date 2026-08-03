# Directrices globales para agentes

Estas reglas son comunes a cualquier repositorio. Las instrucciones locales del proyecto prevalecen cuando sean más específicas.

- Trabaja solo sobre el alcance solicitado.
- Inspecciona primero los archivos directamente afectados.
- No leas toda la documentación del repositorio al comenzar.
- Consulta documentación adicional únicamente cuando exista una duda concreta o una instrucción local la señale.
- Resuelve directamente las tareas pequeñas y medianas. Usa subagentes solo cuando haya trabajo realmente independiente y paralelizable.
- Evita repetir contexto completo al delegar: transmite objetivo, restricciones, rutas y criterio de aceptación.
- Busca la causa raíz; no ocultes errores ni añadas fallbacks falsos.
- Ejecuta las verificaciones relevantes antes de cerrar la tarea. Si no puedes ejecutarlas, indícalo.
- No hagas commits, push, despliegues, migraciones remotas ni cambios externos sin petición expresa.
- Prioriza simplicidad, mantenibilidad y coherencia con el código existente.

Las configuraciones específicas de Claude Code viven en `CLAUDE.md` y `agents/`. Codex debe usar este archivo como guía principal y no asumir una jerarquía multiagente obligatoria.