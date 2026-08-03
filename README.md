# agents-config

Configuración multi-proveedor sincronizada entre máquinas, con routing adaptativo, progressive disclosure y despliegue reversible.

## Principio principal

Cada proveedor recibe solo lo que necesita:

- **Claude Code:** agentes adaptativos (`architect`, `orchestrator`, `supervisor`, `worker`, `auditor`) y skills.
- **OpenAI Codex:** `AGENTS.md` global compacto y skills compartidas. La jerarquía de Claude no se instala en `~/.codex/agents` por defecto.
- **Antigravity / Open Skills:** skills compartidas en `~/.agents/skills`.

La arquitectura multiagente no es una pirámide fija. Un agente fuerte resuelve directamente por defecto y selecciona probes, fan-out, pipelines, writer+reviewers, DAG orquestado o auditoría solo cuando la topología aporta valor real.

## Arquitectura adaptativa

La decisión de delegar se basa en independencia, acoplamiento, aislamiento de contexto, paralelismo real, permisos, riesgo y coste de coordinación. Reglas principales:

- cero subagentes por defecto;
- 2-3 en un fan-out normal, máximo habitual de 5;
- una generación de profundidad por defecto;
- un único writer por archivo o contrato;
- worktrees/ramas aisladas para escritores paralelos;
- contratos mínimos y outputs grandes persistidos como artefactos;
- verificación y auditoría proporcionales al riesgo.

La decisión completa está en [`docs/ADAPTIVE_AGENT_ARCHITECTURE.md`](docs/ADAPTIVE_AGENT_ARCHITECTURE.md).

## Archivos

- `AGENTS.md`: reglas globales comunes y compactas; fuente canónica para Codex.
- `CLAUDE.md`: adaptación para Claude Code.
- `CODEX.md`: adaptación mínima para Codex.
- `agents/`: capacidades multiagente para Claude Code.
- `skills/`: habilidades reutilizables y documentación bajo demanda.
- `router/`, `registry.yaml` y `policies/`: selección de contexto, riesgo y compresión segura.
- `reports/` y `evals/`: inventario, auditoría y evaluaciones reproducibles.
- `settings*.json` y `hooks/`: configuración de Claude Code.
- `install.sh`: instala cada proveedor de forma aislada.
- `update.sh`: sincroniza cambios locales sin mezclar configuraciones.

## Instalar

```bash
git clone https://github.com/marcmarti9/agents-config.git ~/agents-config
cd ~/agents-config
bash install.sh
```

El instalador muestra un plan y no modifica nada por defecto. Para aplicar, revisa el plan y ejecuta `bash install.sh --apply`. Genera backup y hashes, rechaza symlinks y no elimina archivos existentes. Settings, guías globales y hooks requieren flags explícitos.

Para una instalación específica:

```bash
bash install.sh --provider claude --apply
bash install.sh --provider codex --apply
bash install.sh --provider antigravity --apply
```

## Actualizar el repositorio

```bash
cd ~/agents-config
bash update.sh
git diff
```

`update.sh` también muestra un plan por defecto; aplica una allowlist solo con `--apply`. No importa `settings.local.json` ni directorios arbitrarios.

## Uso recomendado

Las tareas focalizadas o fuertemente acopladas se resuelven directamente. Los subagentes se usan para aislamiento de contexto, exploración independiente, paralelismo seguro, especialización o revisión de riesgo. La documentación de cada proyecto actúa como índice y se carga bajo demanda.
