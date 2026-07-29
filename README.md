# agents-config

Configuración multi-proveedor de agentes (Claude Code, Antigravity, OpenAI Codex), sincronizada en mis máquinas vía este repo privado.

## Qué incluye

- `agents/` — jerarquía de agentes personalizada (`architect`, `orchestrator`, `supervisor`, `worker`, `auditor`) compartida y adaptable a Claude, Antigravity y Codex.
- `skills/` — habilidades personalizadas como `architect-orchestrator` y `supabase-postgres-best-practices`.
- `AGENTS.md`, `CLAUDE.md`, `CODEX.md` — directrices globales del proyecto y definición del flujo operativo de 3 niveles para cada cliente CLI.
- `settings.json`, `settings.local.json` — configuración global de `~/.claude/` (modelos, hooks, persistencia de sesiones, etc.).
- `hooks/precompact-memory.sh` — hook `PreCompact` para preservar memoria clave de proyecto.
- `install.sh` y `update.sh` — scripts para desplegar y actualizar la configuración en cualquier máquina.

## Jerarquía Multi-Agente (3 Niveles)

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

## Instalar en una máquina nueva

```bash
git clone https://github.com/marcmarti9/agents-config.git ~/agents-config
cd ~/agents-config
bash install.sh
```

Esto copia las configuraciones correspondientes a `~/.claude/`, `~/.codex/`, `~/.agents/` y `~/`.

## Actualizar el repo tras cambiar algo localmente

```bash
cd ~/agents-config
bash update.sh
git diff
git add -A && git commit -m "update agent configs" && git push
```
