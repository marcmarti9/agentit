# Codex

Usa `~/AGENTS.md` como única guía global canónica.

- No cargues `~/.codex/agents/` ni una jerarquía Architect → Supervisor → Worker por defecto.
- Resuelve directamente tareas pequeñas y medianas.
- Para tareas grandes, crea un plan y usa subagentes solo si existen frentes independientes que puedan avanzar en paralelo.
- No leas documentación completa al iniciar una sesión; sigue el `AGENTS.md` del repositorio y abre únicamente los documentos que este enrute para la tarea actual.
- Mantén las delegaciones compactas: objetivo, restricciones, archivos relevantes y criterio de aceptación.

La configuración multiagente detallada de `agents/` está orientada a Claude Code y es opt-in para otros proveedores.