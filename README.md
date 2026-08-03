# agents-config

Configuración multi-proveedor con routing adaptativo, progressive disclosure, inventario local y despliegue reversible.

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
- `router/` y `policies/`: clasificación heurística y planificación; nunca ejecutan la tarea.
- `registry.yaml`: política operativa portable, con rutas `${HOME}`/`${REPO_ROOT}` y sin observaciones de una máquina.
- `reports/` y `evals/`: método de inventario, revisiones y evaluaciones reproducibles.
- `security/harden-local.sh`: hardening reversible de aliases bypass y permisos MCP.
- `settings*.json` y `hooks/`: configuración de Claude Code.
- `install.sh`: instala cada proveedor de forma aislada.
- `update.sh`: sincroniza cambios locales sin mezclar configuraciones.

## Instalar

Los scripts shell están dirigidos a Linux con Bash 4+ y utilidades GNU (`coreutils` y `findutils`). El router y el inventario requieren Python 3 y PyYAML.

```bash
git clone https://github.com/marcmarti9/agents-config.git ~/agents-config
cd ~/agents-config
bash install.sh
```

El instalador muestra un plan y no modifica nada por defecto. Para aplicar, revisa el plan y ejecuta `bash install.sh --apply`. Genera un backup privado, registra hashes y el modo original, rechaza symlinks y no elimina archivos existentes. Settings, guías globales y hooks requieren flags explícitos. Consulta [`ROLLBACK.md`](ROLLBACK.md) antes de aplicar.

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

El hardening local también es plan por defecto:

```bash
bash security/harden-local.sh
bash security/harden-local.sh --apply
```

No analiza ni muestra valores de credenciales y no cambia la configuración del proxy. En modo apply calcula SHA-256 para verificar backups, por lo que lee los bytes del archivo sin interpretarlos.

## Router e inventario local

```bash
python3 router/route.py "describe la tarea"
python3 -m router.inventory
```

El router devuelve una propuesta JSON: clasifica y planifica, pero no ejecuta comandos, carga skills ni concede permiso. Las operaciones críticas requieren revisión humana y las instrucciones activas siguen teniendo precedencia.

- `skills_available`: recomendaciones cuyo estado, ruta y dependencias esenciales son compatibles en la máquina consultada.
- `skills_recommended_missing`: recomendaciones pertinentes que no superaron esas comprobaciones.
- `skills`: alias heredado de `skills_available`; nunca incluye recomendaciones ausentes.

`python3 -m router.inventory` escribe por defecto `reports/local/inventory.yaml`, una ruta ignorada por Git. El resultado es específico de la máquina y puede dejar la versión de un ejecutable sin observar; no debe convertirse en evidencia portable ni publicarse sin revisión.

## Uso recomendado

Las tareas focalizadas o fuertemente acopladas se resuelven directamente. Los subagentes se usan para aislamiento de contexto, exploración independiente, paralelismo seguro, especialización o revisión de riesgo. La documentación de cada proyecto actúa como índice y se carga bajo demanda.
