# Directrices globales para agentes

Estas reglas son comunes a cualquier repositorio. Las instrucciones locales del proyecto prevalecen cuando sean más específicas.

## Harness Agentit

### Activación

**Frases de disparo:** `usa agentit` · `use agentit` · `usando agentit` · `with agentit` · `modo agentit` · `agentit mode`.

Cuando el usuario diga cualquiera de ellas (o Agentit ya sea el harness por defecto de la sesión):

1. Carga `using-agentit` (`~/code/agentit/skills/using-agentit/SKILL.md` o copia del proveedor).
2. Sigue su playbook para el resto de la sesión.
3. No improvises otra metodología incompatible.

Agentit es provider-neutral: OpenAI, Anthropic, Google, xAI y clientes compatibles deben preservar las mismas semantics aunque cambie la primitiva de agentes/subagentes.

### Playbook compacto

| Paso | Acción |
|---|---|
| 0. Interview | Si afecta producto, inspecciona hechos y pregunta **todas las decisiones materiales identificables en una sola ronda**, incluyendo Standard/Polished/Studio. Solo bypass mecánico exacto. |
| 1. Persist | Tras confirmar entrevista, actualiza `docs/agentit/STATE.md` (o equivalente canónico) para poder reanudar sin el chat. |
| 2. Route | `python3 ~/code/agentit/router/route.py "tarea"` o `agentit trace "tarea" --project .` |
| 3. Profiles JIT | `agentit enable <profile> --project <ruta> --apply` si faltan skills. |
| 4. Skills | Carga solo skills relevantes; UI/UX Pro Max se consulta JIT, no se vuelca entero en contexto. |
| 5. Ejecuta | Single-agent-first. Especialistas solo si aportan valor y respetan el nivel de esfuerzo. |
| 6. Documenta | Mantén el estado actualizado tras decisiones/milestones y antes de cualquier corte/handoff. |
| 7. Verify | `agentit verify "tarea" --project . --apply`; no `done` sin evidencia fresca. |
| 8. Git | Branch + PR por defecto. No escribir/mergear directo a `main`/`master` salvo excepción explícita del usuario/proyecto. |

### Entrevista

Para trabajo de producto, no hagas goteo de preguntas. Tras inspeccionar repo/docs/tools, formula de golpe todas las preguntas materiales que ya puedas identificar. Cada pregunta incluye recomendación/default. Una segunda ronda solo se justifica si las respuestas revelan decisiones nuevas que no podían conocerse antes.

La entrevista debe recomendar y confirmar Standard / Polished / Studio con consecuencias y rango aproximado de tokens.

### Continuidad obligatoria

El chat es contexto desechable. Todo lo necesario para continuar una tarea significativa debe quedar en el repositorio.

Política canónica: `docs/PROJECT_CONTINUITY.md`.

Estado por defecto del proyecto: `docs/agentit/STATE.md` salvo equivalente existente.

Debe permitir a otro agente/máquina/proveedor saber: objetivo, intención confirmada, nivel de esfuerzo, estado actual, decisiones, archivos/artefactos, branch/PR, verificación, blockers y siguientes acciones.

Actualiza el estado:

- justo después de confirmar entrevista/esfuerzo;
- tras decisiones caras de redescubrir;
- tras milestones significativos;
- antes de cambiar de sesión/modelo/proveedor/máquina o quedarse sin contexto/tokens;
- antes de parar por error/límite/pausa;
- antes de cerrar la tarea.

Nunca persistir secretos, credenciales, chain-of-thought, transcripts completos o dumps enormes.

### Git / PR-first

Cambios de repositorio usan por defecto:

`branch de trabajo -> commits -> verificación -> PR -> decisión de merge`.

- No commitear directamente a la rama por defecto salvo instrucción explícita.
- No mergear automáticamente un PR salvo instrucción explícita.
- La documentación de continuidad viaja en el mismo branch/PR.
- Una excepción `directo a main` vale solo para la tarea concreta donde fue autorizada.

### Skills de diseño

- Inteligencia UI/UX estructurada → `ui-ux-pro-max-intelligence` (consulta JIT al upstream MIT; evidence/candidates, no dirección creativa automática).
- Art direction / landings / portfolios → `design-taste-frontend`.
- Critique/polish → `impeccable-design`.
- Interaction/motion → `emil-design-eng`.
- UI/a11y → `frontend-ui-engineering`.
- Research/trends → `design-inspiration-research`, `design-trend-researcher`.

El nivel de esfuerzo controla profundidad: Standard eficiente, Polished selectivo, Studio quality-first.

### Mantenimiento

- Tras cambios del harness: `bash ~/code/agentit/install.sh --provider all --with-guides --apply`.
- No reviertas guías/skills gestionados sin motivo.

## Reglas operativas

- Trabaja solo sobre el alcance solicitado.
- Inspecciona primero archivos directamente afectados; no leas todo el repo por ceremonia.
- Busca causa raíz; no ocultes errores ni añadas fallbacks falsos.
- Aplica preferencias del usuario salvo conflicto con seguridad/proyecto.
- Ejecuta verificaciones relevantes antes de cerrar.
- No deploys, migraciones remotas ni cambios externos sin autorización.
- Prioriza simplicidad, mantenibilidad y coherencia.
- Estilo conciso y directo.

## Política de delegación adaptativa

El agente principal conserva requisitos, arquitectura, integración, documentación y revisión final. Toda delegación debe proyectar instrucciones del proyecto, skills de la tarea, preferencias seguras, riesgo, I/O, verificación y stop condition mediante el Worker Context Contract.

Precedencia: `safety > user > project > preferences > defaults`.

No conviertas la arquitectura en una cadena fija. Si el proveedor no soporta subagentes, ejecuta el mismo rol/skill bundle en contexto aislado o en el parent. Multi-agent es optimización, no dependencia.
