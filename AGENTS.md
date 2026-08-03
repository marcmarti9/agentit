# Directrices globales para agentes

Estas reglas son comunes a cualquier repositorio. Las instrucciones locales del proyecto prevalecen cuando sean más específicas.

- Trabaja solo sobre el alcance solicitado.
- Inspecciona primero los archivos directamente afectados.
- No leas toda la documentación del repositorio al comenzar.
- Consulta documentación adicional únicamente cuando exista una duda concreta o una instrucción local la señale.
- Resuelve directamente las tareas pequeñas y medianas. Usa subagentes solo cuando haya trabajo realmente independiente y paralelizable.
- Evita repetir contexto completo al delegar: transmite objetivo, restricciones, rutas y criterio de aceptación.
- Busca la causa raíz; no ocultes errores ni añadas fallbacks falsos.
- Aplica las preferencias del usuario (`applied_preferences` emitidas por el router) como el idioma, framework de testing o estilos UI, salvo que entren en conflicto con requisitos del proyecto.
- Ejecuta las verificaciones relevantes antes de cerrar la tarea. Si no puedes ejecutarlas, indícalo.
- No hagas commits, push, despliegues, migraciones remotas ni cambios externos sin petición expresa.
- Prioriza simplicidad, mantenibilidad y coherencia con el código existente.
- Estilo de respuesta conciso (Terse Prose): Sé directo, conciso y libre de paja. Omite conversaciones triviales, saludos, explicaciones obvias y resúmenes de código no modificado. Emite solo respuestas directas, diffs exactos y el resultado de la verificación.

## Política de delegación adaptativa

Al inicio de cada tarea, decide si conviene trabajar directamente o delegar. Trabaja directamente en tareas pequeñas, acopladas o con un único conjunto de cambios. Usa `terra_worker` como worker predeterminado para trabajo independiente, acotado y verificable que aporte una ventaja real. Reserva `luna_worker` para cuando el backend de la sesión confirme que Luna está disponible.

El agente principal conserva los requisitos, las decisiones de arquitectura, la integración y la revisión final. Cuando delegues, envía solo el objetivo, el alcance, los archivos permitidos, el criterio de aceptación y la verificación esperada; mantén las escrituras separadas y no encadenes subagentes sin una razón concreta.

No conviertas esta política en una cadena fija ni delegues por costumbre. Si la superficie multiagente no permite seleccionar el modelo del hijo, dilo y no afirmes que se está usando Luna.

Las configuraciones específicas de Claude Code viven en `CLAUDE.md` y `agents/`. Codex debe usar este archivo como guía principal y no asumir una jerarquía multiagente obligatoria.
