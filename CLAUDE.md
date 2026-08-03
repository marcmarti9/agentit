# Directrices de Claude Code

Usa `~/AGENTS.md` como guía global y selecciona la topología mínima que justifique la tarea. `architect` es el owner y punto de contacto con el usuario, no una fase obligatoria de una pirámide.

- Resuelve directamente por defecto.
- Usa `plan + directa` para trabajo amplio pero acoplado.
- Usa `probe` para investigación aislada y de solo lectura.
- Usa `fan-out`, pipeline o DAG solo con independencia real, ownership separado y beneficio neto de coordinación.
- Usa `orchestrator`, `supervisor`, `worker` y `auditor` como capacidades adaptativas, no como cadena fija.
- Mantén un único writer por archivo o contrato; usa worktrees/ramas aisladas para escritores paralelos.
- Para RISK_3/RISK_4 conserva contexto completo, recupera originales y exige revisión/verificación proporcional.
- No actives hooks, MCP, proxies ni compresión destructiva sin revisión, allowlist y rollback.

Cada subagente debe recibir objetivo, alcance de lectura/escritura, entradas, salida, verificador y stop condition; los resultados grandes deben persistirse como artefactos referenciados.

OmniRoute en `http://localhost:20128` solo se usa después de comprobar que hay un listener y que el routing es el esperado.
