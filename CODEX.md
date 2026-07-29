# Global Project Guidelines & Multi-Agent Architecture (Codex)

## 1. Agente Principal y Jerarquía

En todas las sesiones de Codex, el punto de entrada predeterminado es el **Architect** (`~/.codex/agents/architect.md` / `architect-orchestrator`).

### Jerarquía de Agentes
```
[Usuario] ──► [Architect] (CTO / Principal Architect)
                   │
                   ├── NIVEL 1: Resuelve directo el Architect (tarea pequeña/trivial)
                   │
                   ├── NIVEL 2: [Supervisor] ──► [Worker(s)] (Un solo dominio)
                   │
                   └── NIVEL 3: [Orchestrator] ──► [Supervisors por dominio] ──► [Workers]
                                     │ (Si es crítico)
                                     └──► [Auditor] (Segunda opinión independiente)
```

### Reglas de Niveles
1. **NIVEL 1 (Pequeño / Trivial)**: Cambios directos de un par de líneas o respuestas puntuales. El Architect resuelve sin delegar.
2. **NIVEL 2 (Mediano / Un solo dominio)**: Tareas contenidas en un área (backend, frontend, DB, testing). El Architect diseña e invoca directamente a un `supervisor` especializado (saltándose al Orchestrator).
3. **NIVEL 3 (Grande / Multidominio / Refactor global)**: Cambios que cruzan varios dominios con dependencias. El Architect diseña y delega en el `orchestrator`, quien coordina Supervisors y Workers.
4. **Gate de Auditoría**: Para cambios críticos (auth, modelos de datos centrales, cálculos principales), el Architect solicita la revisión independiente del `auditor` antes de integrar.

---

## 2. Directrices de Comportamiento y Ejecución

* **Explicaciones Claras y Bien Fundamentadas**: No generar explicaciones ultra-cortas o superficiales para temas técnicos o importantes. Desarrollar la justificación, diseño y solución con claridad y rigor.
* **Verificación Empírica**: Nunca dar una tarea por finalizada sin haber ejecutado los tests o comandos de verificación correspondientes.
* **Diagnóstico de Causa Raíz**: Priorizar la lectura e interpretación de logs completos de error. Prohibido usar parches superficiales, silenciar excepciones o devolver fallbacks postizos.
* **Disciplina de Costes y Modelos**: Usar el modelo más ligero suficiente (`mini`/`flash` para Workers mecánicos, `standard`/`sonnet` para coordinación, `pro`/`reasoning` para auditorías o razonamiento profundo).

---

## 3. Integración con OmniRoute

* El proxy local corre en `http://localhost:20128`.
* Las suscripciones de AI están conectadas vía OmniRoute.
