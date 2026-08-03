# Puesta en marcha de Codex

## Instalación

Desde el repositorio clonado:

```bash
bash install.sh
```

El instalador conserva copias de seguridad y coloca:

- la guía global en `~/.codex/AGENTS.md`;
- `terra_worker` y `luna_worker` en `~/.codex/agents/`;
- la skill `architect-orchestrator` en `~/.codex/skills/`.

No copia la jerarquía de agentes de Claude a Codex.

## Ajustes locales recomendados

Conserva el `~/.codex/config.toml` de cada máquina y aplica solo los valores
que falten o quieras cambiar. Para el esquema actual, el agente principal usa
Sol con razonamiento medio y el worker predeterminado usa Terra con esfuerzo
medio:

```toml
model = "gpt-5.6-sol"
model_reasoning_effort = "medium"

[features.multi_agent_v2]
hide_spawn_agent_metadata = false
tool_namespace = "agents"

[agents]
enabled = true
max_concurrent_threads_per_session = 1
default_subagent_model = "gpt-5.6-terra"
default_subagent_reasoning_effort = "medium"
```

`luna_worker` queda instalado como perfil opcional con `gpt-5.6-luna` y
razonamiento `max`. Úsalo únicamente cuando la sesión confirme que el backend
puede seleccionar Luna; si no, el padre puede acabar ejecutando otro modelo o
rechazar el worker.

El modelo principal conserva los requisitos, las decisiones de arquitectura y
la revisión final. La delegación debe ser adaptativa: trabajo directo cuando
sea suficiente y workers solo para tareas independientes, acotadas y
verificables.
