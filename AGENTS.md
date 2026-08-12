# Directrices globales para agentes

Estas reglas son comunes a cualquier repositorio. Las instrucciones locales del proyecto prevalecen cuando sean más específicas.

## Harness Agentit

### Activación

**Única frase especial:** cualquier forma natural de “usar Agentit” en el idioma del usuario (p. ej. `usa agentit`, `use agentit`, `utilise agentit`, `usando agentit`, …) siempre que quede claro que se activa el harness **agentit**.

No hace falta ninguna otra powerword. El resto del routing se basa en lenguaje ordinario del prompt (archivos, dominios, “al mismo tiempo”, “frontend y backend”, “revisa y arregla”, “varios agentes”, etc.).

Cuando Agentit esté activo:

1. Carga `using-agentit`.
2. Sigue su playbook el resto de la sesión.
3. No improvises otra metodología incompatible.

Agentit es provider-neutral: OpenAI, Anthropic, Google, xAI y clientes compatibles preservan las mismas semantics aunque cambie la primitiva de agentes/subagentes.

### Playbook compacto

| Paso | Acción |
|---|---|
| 0. Interview | Si afecta producto: una sola ronda con todas las decisiones materiales. **Craft depth (Standard/Polished/Studio) solo si es diseño/visual.** Domain pack de skills. Estimación de tokens del proyecto, no tablas fijas. |
| 1. Persist | Actualiza `docs/agentit/STATE.md` (o equivalente). |
| 2. Route | `python3 ~/code/agentit/router/route.py "tarea"` o `agentit trace "tarea" --project .` |
| 3. Skills | Solo `skill_budget`: always_core + load_now. Nunca el catálogo entero. |
| 4. MCP | `mcp-tooling-fit` cuando importe: status, fit, desactivar ruido, descubrir catálogo/marketplace/web. |
| 5. Ejecuta | Delegación inteligente. Sin cupos min/max duros. Critic obligatorio en planes estructurales grandes. |
| 6. Documenta | Estado actualizado en milestones y antes de cortes. |
| 7. Verify | `agentit verify "tarea" --project . --apply`; no `done` sin evidencia. |
| 8. Git | Branch + PR por defecto. |

### Skills y packs

Los perfiles (`frontend`, `backend`, `design`, …) existen para cargar **familias** por tipo de tarea. El agente principal no es mini-experto en todo: organiza, proyecta skills del pack, y spawnea especialistas con sus skills.

Si el usuario asigna un rol (“actúa como experto en X”), carga solo skills de ese dominio + core mínimo; si faltan, busca e instala con aprobación.

### Delegación

- No dogmático single-agent-first ni multi forzado.
- Spawnea cuando independencia, aislamiento, especialidad o crítica aportan.
- Si el usuario pide muchos agentes sin beneficio, dilo y recomienda no spawnear.
- Planes estructurales grandes → **siempre critic** independiente antes de implementar en serio.

### Continuidad

Chat desechable. Estado canónico: `docs/agentit/STATE.md`. Política: `docs/PROJECT_CONTINUITY.md`.

### Git / PR-first

`branch → commits → verificación → PR → merge por el usuario` salvo excepción explícita.

## Reglas operativas

- Alcance solo lo pedido.
- Inspecciona primero archivos afectados.
- Causa raíz; sin fallbacks falsos.
- Verificaciones relevantes antes de cerrar.
- Sin deploys/migraciones remotas sin autorización.
- Simplicidad y coherencia.

## Precedencia

`safety > user > project > preferences > defaults`.

Multi-agent es optimización, no dependencia de corrección. Si el proveedor no soporta subagentes, el parent ejecuta el mismo bundle de skills en contexto aislado o directo.
