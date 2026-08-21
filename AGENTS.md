# Directrices globales para agentes

Estas reglas son comunes a cualquier repositorio. Las instrucciones locales del proyecto prevalecen cuando sean más específicas.

## Harness Agentit

### Activación

**Única frase especial:** cualquier forma natural de “usar Agentit” en el idioma del usuario (p. ej. `usa agentit`, `use agentit`, `utilise agentit`, `usando agentit`, …) siempre que quede claro que se activa el harness **Agentit**.

No hace falta ninguna otra powerword. Cuando Agentit esté activo:

1. Carga `using-agentit`.
2. Sigue su playbook el resto de la sesión.
3. No improvises otra metodología incompatible.

Agentit es provider-neutral: OpenAI, Anthropic, Google, xAI y clientes compatibles preservan las mismas semantics aunque cambie la primitiva de agentes/subagentes.

### El agente es el router semántico

No uses regex, árboles de keywords ni un script Python para decidir qué significa la petición. La IA activa clasifica la tarea obligatoriamente usando el protocolo `task-router` y **todo el contexto disponible**: conversación, repositorio, archivos, herramientas, instrucciones del usuario/proyecto y estado previo.

Aplica siempre el mismo marco de decisión, pero no fuerces la misma respuesta cuando el contexto cambie.

Antes de ejecutar decide como mínimo: intención, categoría, complejidad, riesgo, reversibilidad, topología, domain pack, skills, especialistas, capabilities, delegación, verificación y critic si aplica.

`router/decision_contract.py` solo valida invariantes deterministas de una decisión estructurada. `router/route.py` queda como adapter de compatibilidad: con texto natural devuelve `decision_required`; no inventa risk/category/topology.

### Playbook compacto

| Paso | Acción |
|---|---|
| 0. Inspect | Recupera contexto útil del chat/proyecto/herramientas antes de preguntar o decidir. |
| 1. Decide | La propia IA clasifica la tarea con `task-router`; valida hard gates si materializa JSON. |
| 2. Interview | Si afecta producto: una ronda útil con todas las decisiones materiales. Craft depth (Standard/Polished/Studio) solo si es diseño/visual. |
| 3. Persist | Actualiza `docs/agentit/STATE.md` (o equivalente) en trabajo sustancial. |
| 4. Skills | Carga solo el conjunto útil + core mínimo. IDs no equivalen a bodies cargados. |
| 5. MCP | `mcp-tooling-fit` cuando importe: inventario real, fit, least privilege y sin ruido universal. |
| 6. Runtime | Loop Contract para cada unidad; Graph Contract para trabajo multi-nodo. |
| 7. Ejecuta | Delegación inteligente. Sin cupos min/max duros. Critic obligatorio en trabajo estructural. |
| 8. Verify | `agentit verify "tarea" --project . --apply`; no `done` sin evidencia/receipts. |
| 9. Git | Branch + PR por defecto. |

### Risk / safety floors

- RISK_3/RISK_4 → revisión independiente.
- RISK_4 → preview/dry-run cuando tenga sentido + rollback plan + post-check.
- Operación destructiva sobre datos → RISK_4 + backup verificado.
- Trabajo estructural → critic independiente.
- Superficie visual pública → design-primary + evidencia renderizada/browser.
- `fan_out` → mínimo dos ramas realmente independientes + razón concreta.

Una restricción explícita de riesgo del usuario/proyecto solo puede subir el suelo, nunca bajarlo.

### Skills y packs

Los perfiles (`frontend`, `backend`, `design`, …) existen para cargar **familias** por tipo de tarea. La IA decide qué skills son relevantes; el registry solo verifica que existen y son cargables.

Una skill no se considera usada por aparecer en una lista. El modelo que ejecuta la etapa debe leer su `SKILL.md` o recibir inyección provider-native equivalente.

Si el usuario asigna un rol (“actúa como experto en X”), carga solo skills de ese dominio + core mínimo; si faltan, haz visible la carencia y sigue la política de instalación/aprobación correspondiente.

### Delegación

- No dogmático single-agent-first ni multi forzado.
- Spawnea cuando independencia, aislamiento, especialidad, amplitud o crítica fresca aportan.
- Si el usuario pide muchos agentes sin beneficio, dilo y recomienda no spawnear.
- Planes estructurales grandes → critic independiente antes de implementar en serio.
- Un writer por archivo/shared state salvo aislamiento explícito por branch/worktree.

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