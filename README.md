# agents-config

Configuración multi-proveedor sincronizada entre máquinas.

## Principio principal

Cada proveedor recibe solo lo que necesita:

- **Claude Code:** jerarquía completa de agentes (`architect`, `orchestrator`, `supervisor`, `worker`, `auditor`), hooks y skills.
- **OpenAI Codex:** `AGENTS.md` global compacto y skills compartidas. La jerarquía multiagente no se instala en `~/.codex/agents` por defecto.
- **Antigravity / Open Skills:** skills compartidas en `~/.agents/skills`.

Esto evita que una sesión normal de Codex cargue instrucciones ceremoniales o replique contexto entre subagentes sin necesidad.

## Archivos

- `AGENTS.md`: reglas globales comunes y compactas; fuente canónica para Codex.
- `CLAUDE.md`: adaptación para Claude Code.
- `CODEX.md`: adaptación mínima para Codex.
- `agents/`: jerarquía multiagente orientada a Claude Code.
- `skills/`: habilidades reutilizables y documentación bajo demanda.
- `settings*.json` y `hooks/`: configuración de Claude Code.
- `install.sh`: instala cada proveedor de forma aislada.
- `update.sh`: sincroniza cambios locales sin mezclar configuraciones.

## Instalar

```bash
git clone https://github.com/marcmarti9/agents-config.git ~/agents-config
cd ~/agents-config
bash install.sh
```

El instalador realiza copias de seguridad antes de sustituir archivos existentes.

## Actualizar el repositorio

```bash
cd ~/agents-config
bash update.sh
git diff
git add -A && git commit -m "update agent configs" && git push
```

## Uso recomendado

Las tareas pequeñas y medianas se resuelven directamente. La delegación se reserva para trabajo grande con frentes independientes y paralelizables. La documentación de cada proyecto debe actuar como índice y cargarse bajo demanda, no como lectura inicial completa.