# Directrices globales para agentes

Estas reglas son comunes a cualquier repositorio. Las instrucciones locales del proyecto prevalecen cuando sean más específicas.

## Harness Agentit

### Activación

**Frases de disparo:** `usa agentit` · `use agentit` · `usando agentit` · `with agentit` · `modo agentit` · `agentit mode`.

Cuando el usuario diga cualquiera de ellas (o Agentit ya sea el harness por defecto de la sesión):

1. Carga el skill `using-agentit` (`~/code/agentit/skills/using-agentit/SKILL.md` o copia en `~/.agents/skills/using-agentit/`).
2. Sigue su playbook para el resto de la sesión.
3. No improvises otra orquestación multi-agente.

En esta máquina Agentit es el meta-harness canónico (Claude Code, Codex, Grok Build, Open Skills). Si el usuario no nombra Agentit pero la tarea es no trivial, aplica el mismo playbook.

### Playbook compacto

| Paso | Acción |
|------|--------|
| 1. Route | `python3 ~/code/agentit/router/route.py "tarea"` → lee `risk`, `topology`, `skills_available`, `skills_recommended_missing`, `applied_preferences`, `verification`, `jit_profile_recommendations` |
| 2. Profiles JIT | `agentit enable <profile> --project <ruta> --apply` si faltan skills de un perfil (`frontend`, `design`, `backend`, `supabase`, `product`, `writing`, `release`, `research`) |
| 3. Skills | Carga solo los `SKILL.md` recomendados (preferir `~/code/agentit/skills/<id>/`). References solo bajo demanda |
| 4. Ejecuta | Single-agent-first (`direct`). Subagentes solo si la topología lo justifica + Worker Context Contract |
| 5. Contexto | `agentit context filter|archive|dedup` y `agentit artifact …` si hay ruido o salidas grandes |
| 6. MCP | `agentit mcp status|enable|disable` (plan-first; `--apply` para escribir) |
| 7. Cierre | Sin done/fixed/passing sin **evidencia fresca de comando** en este turno |

CLI: `agentit` → `~/.local/bin/agentit`. Raíz: `~/code/agentit`.

### Skills de diseño (recordatorio)

- Landings / portfolios / rediseño visual → `design-taste-frontend` (perfil `design` o `frontend`, o cuerpo en el harness)
- UI de producto / a11y → `frontend-ui-engineering`
- Checklist anti-slop corta → `anti-ai-slop-design`

### Mantenimiento

- Tras cambios del harness: `bash ~/code/agentit/install.sh --provider all --with-guides --apply`
- No reviertas guías ni skills gestionados sin motivo

## Reglas operativas

- Trabaja solo sobre el alcance solicitado.
- Inspecciona primero los archivos directamente afectados.
- No leas toda la documentación del repositorio al comenzar.
- Consulta documentación adicional únicamente cuando exista una duda concreta o una instrucción local la señale.
- Resuelve directamente las tareas pequeñas y medianas. Usa subagentes solo cuando haya trabajo realmente independiente y paralelizable.
- Evita repetir contexto completo al delegar: transmite objetivo, restricciones, rutas y criterio de aceptación.
- Busca la causa raíz; no ocultes errores ni añadas fallbacks falsos.
- Aplica las preferencias del usuario (`applied_preferences` del router) salvo conflicto con requisitos del proyecto o seguridad.
- Ejecuta las verificaciones relevantes antes de cerrar la tarea. Si no puedes, indícalo. **No declares done/fixed/passing sin evidencia fresca de comando en este turno** (`verification-before-completion`).
- No hagas commits, push, despliegues, migraciones remotas ni cambios externos sin petición expresa.
- Prioriza simplicidad, mantenibilidad y coherencia con el código existente.
- Estilo conciso y directo: resultado, cambios, verificaciones, riesgos. Sin relleno.
- Sin emojis decorativos salvo contenido del usuario, UI, marca o petición explícita.

## Política de delegación adaptativa

Al inicio de cada tarea, decide si conviene trabajar directamente o delegar (preferir la topología del router). Trabaja directamente en tareas pequeñas, acopladas o con un único conjunto de cambios. Usa `terra_worker` como worker predeterminado para trabajo independiente, acotado y verificable. Reserva `luna_worker` solo cuando el backend confirme Luna.

El agente principal conserva requisitos, arquitectura, integración y revisión final. Toda creación de subagente debe pasar por el Worker Context Contract (`router/worker_context.py` / `agentit worker build`): proyectar instrucciones de proyecto, skills de la tarea (no el catálogo completo), preferencias seguras, riesgo, entradas/salidas y verificación. Precedencia: `safety > user > project > preferences > defaults`.

No conviertas esta política en una cadena fija. Si la superficie multiagente no permite seleccionar el modelo del hijo, dilo y no afirmes un modelo incorrecto.

Claude Code: ver también `CLAUDE.md` y `agents/`. Codex: este archivo como guía principal. Grok Build / Open Skills: este `AGENTS.md` + `~/.agents/skills` (core global; resto on-demand).
