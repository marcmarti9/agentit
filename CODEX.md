# Codex

Usa `~/.codex/AGENTS.md` como guía global canónica de Codex. El instalador también mantiene `~/AGENTS.md` para los proveedores que usan la guía común.

El instalador instala globalmente solo el perfil `core` de `profiles.yaml` para
mantener acotado el catálogo de descubrimiento. Activa perfiles adicionales por
proyecto con `./agentit enable <profile> --project .`; el comando muestra un plan
por defecto y requiere `--apply` para escribir. Para migrar una instalación antigua
que tenía todas las skills globales, usa `bash install.sh --provider codex
--apply --prune-on-demand`; solo poda copias exactas y no modificadas con backup.

- No cargues la jerarquía de Claude Architect → Supervisor → Worker por defecto.
- Resuelve directamente tareas pequeñas y medianas.
- Para tareas grandes, crea un plan y usa subagentes solo si existen frentes independientes que puedan avanzar en paralelo.
- No leas documentación completa al iniciar una sesión; sigue el `AGENTS.md` del repositorio y abre únicamente los documentos que este enrute para la tarea actual.
- Mantén las delegaciones compactas: objetivo, restricciones, archivos relevantes y criterio de aceptación.

Los perfiles portables de `.codex/agents/` son workers acotados para Codex:

- `terra_worker`: worker predeterminado cuando el backend permite seleccionarlo.
- `luna_worker`: perfil opcional; úsalo solo cuando la sesión confirme que Luna está disponible.

La selección del modelo principal, el esfuerzo de razonamiento y las opciones del backend multiagente viven en `~/.codex/config.toml`, porque son preferencias locales y pueden variar entre máquinas. No subas ese archivo completo: puede contener rutas, servidores MCP y otros ajustes específicos del equipo.

La configuración multiagente detallada de `agents/` sigue orientada a Claude Code. La política de Codex es adaptativa y no obliga a crear una cadena fija de agentes.
