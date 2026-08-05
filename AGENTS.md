# Directrices globales para agentes

Estas reglas son comunes a cualquier repositorio. Las instrucciones locales del proyecto prevalecen cuando sean más específicas.

## Harness Agentit (obligatorio)

Agentit es el meta-harness por defecto en esta máquina (Claude Code, Codex, Grok Build y Open Skills). Úsalo siempre; no improvises otra orquestación.

- Raíz del harness: `~/code/agentit` (CLI: `agentit` en PATH → `~/.local/bin/agentit`).
- Al inicio de cada tarea no trivial (implementación, depuración, refactor, multi-archivo, riesgo operativo o duda de topología), ejecuta el router y sigue su propuesta salvo que las instrucciones del proyecto o el usuario digan lo contrario:
  - `python3 ~/code/agentit/router/route.py "descripción de la tarea"`
  - Lee `topology`, `risk`, `skills_available`, `applied_preferences`, `verification` y `jit_profile_recommendations`.
- El router es heurística de planificación, no permiso de ejecución. Single-agent-first: `direct` por defecto; subagentes solo si la topología y el contrato lo justifican.
- Carga solo los `SKILL.md` recomendados y disponibles (perfil `core` global + perfiles de proyecto). No cargues todo el catálogo.
- Perfiles de proyecto (JIT):
  - `agentit enable <profile> --project <ruta> --apply` cuando el router o la tarea lo requieran
  - `agentit status --project <ruta>`
- Motores de contexto (salidas grandes / ruido / dedup):
  - `agentit context filter <archivo>`
  - `agentit context archive <archivo> --description "..."`
  - `agentit context dedup "..." --session <id>`
  - `agentit artifact get|read|grep agentit://...`
- Scout/incubator solo cuando el usuario pida evaluar ideas, repos o herramientas del ecosistema: `agentit scout ...`
- Tras `install.sh`/`update.sh`, no reviertas guías ni skills gestionados sin motivo; el harness se mantiene con `bash ~/code/agentit/update.sh`.

## Reglas operativas

- Trabaja solo sobre el alcance solicitado.
- Inspecciona primero los archivos directamente afectados.
- No leas toda la documentación del repositorio al comenzar.
- Consulta documentación adicional únicamente cuando exista una duda concreta o una instrucción local la señale.
- Resuelve directamente las tareas pequeñas y medianas. Usa subagentes solo cuando haya trabajo realmente independiente y paralelizable.
- Evita repetir contexto completo al delegar: transmite objetivo, restricciones, rutas y criterio de aceptación.
- Busca la causa raíz; no ocultes errores ni añadas fallbacks falsos.
- Aplica las preferencias del usuario (`applied_preferences` emitidas por el router) como el idioma, framework de testing o estilos UI, salvo que entren en conflicto con requisitos del proyecto.
- Ejecuta las verificaciones relevantes antes de cerrar la tarea. Si no puedes ejecutarlas, indícalo. **No declares done/fixed/passing sin evidencia fresca de comando en este turno** (skill `verification-before-completion`; iron law también en `using-agent-skills`).
- No hagas commits, push, despliegues, migraciones remotas ni cambios externos sin petición expresa.
- Prioriza simplicidad, mantenibilidad y coherencia con el código existente.
- Estilo conciso y directo: Sé directo y elimina el relleno. Prioriza el resultado, los cambios realizados, las verificaciones y cualquier riesgo o acción necesaria. No omitas contexto necesario para entender, revisar o usar correctamente la solución.
- Sin emojis decorativos: No uses emojis decorativos por defecto en artefactos técnicos, código o respuestas. Consérvalos solo cuando formen parte del contenido del usuario, la interfaz, la marca o una petición explícita.

## Política de delegación adaptativa

Al inicio de cada tarea, decide si conviene trabajar directamente o delegar (preferir la topología del router Agentit). Trabaja directamente en tareas pequeñas, acopladas o con un único conjunto de cambios. Usa `terra_worker` como worker predeterminado para trabajo independiente, acotado y verificable que aporte una ventaja real. Reserva `luna_worker` para cuando el backend de la sesión confirme que Luna está disponible.

El agente principal conserva los requisitos, las decisiones de arquitectura, la integración y la revisión final. Cuando delegues, **toda** creación de subagente debe pasar por el Worker Context Contract (`router/worker_context.py` / `agentit worker build`): proyectar instrucciones de proyecto (`AGENTS.md`/`CLAUDE.md`/…), skills activas de la tarea (no el catálogo completo), preferencias seguras, riesgo y constraints, entradas/artefactos, salida y verificación. Contexto fresco sin proyectar instrucciones del proyecto es negligencia. Precedencia: `safety > user > project > preferences > defaults`. Mantén las escrituras separadas y no encadenes subagentes sin una razón concreta.

No conviertas esta política en una cadena fija ni delegues por costumbre. Si la superficie multiagente no permite seleccionar el modelo del hijo, dilo y no afirmes que se está usando Luna.

Las configuraciones específicas de Claude Code viven en `CLAUDE.md` y `agents/`. Codex debe usar este archivo como guía principal y no asumir una jerarquía multiagente obligatoria. Grok Build sigue este `AGENTS.md` y el catálogo Open Skills en `~/.agents/skills`.
