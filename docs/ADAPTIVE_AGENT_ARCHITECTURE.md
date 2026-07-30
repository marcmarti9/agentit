# Arquitectura adaptativa de agentes

## Decisión

La configuración deja de modelar el trabajo como una jerarquía fija de tres niveles. El sistema usa un agente principal fuerte y selecciona dinámicamente una topología según independencia, acoplamiento, aislamiento de contexto, paralelismo, permisos, riesgo y coste de coordinación.

Los nombres `architect`, `orchestrator`, `supervisor`, `worker` y `auditor` se mantienen por compatibilidad, pero representan capacidades temporales, no puestos por los que toda tarea deba circular.

## Por qué cambia

Una jerarquía fija introduce tres problemas:

1. replica el contexto y las instrucciones en cada salto;
2. añade latencia y pérdida de intención aunque el trabajo esté acoplado;
3. confunde complejidad o número de archivos con divisibilidad real.

Los sistemas modernos obtienen ventaja de múltiples agentes principalmente cuando pueden explorar direcciones independientes, aislar contextos largos, trabajar con herramientas o permisos distintos, o aportar una verificación realmente independiente. En tareas acopladas, un agente fuerte con un plan suele ser más eficiente.

## Topologías admitidas

| Topología | Cuándo usarla | Regla de ownership |
|---|---|---|
| Directa | Cambio focalizado o muy acoplado | Architect escribe e integra |
| Plan + directa | Trabajo largo pero secuencial | Un único owner; estado persistido por hitos |
| Probe | Investigación, reproducción o localización | Solo lectura; devuelve evidencia |
| Fan-out/fan-in | Líneas independientes | Un owner por archivo/artefacto |
| Pipeline | Dependencias ordenadas | Cada etapa consume un artefacto estable |
| Writer + reviewers | Implementación con revisión independiente | Un único writer; reviewers en solo lectura |
| DAG orquestado | Varios paquetes con dependencias reales | Ownership explícito y worktrees aislados |
| Auditoría | Alto riesgo o arbitraje | Auditor de solo lectura y contexto fresco |

## Contrato de delegación

Cada subagente recibe solo:

- objetivo y criterio de terminado;
- entradas concretas;
- alcance de lectura/escritura;
- invariantes relevantes;
- artefacto o esquema de salida;
- verificación;
- stop condition y frontera de escalado.

No recibe la conversación completa ni documentación global no relacionada. Los resultados grandes se guardan en archivos, ramas, worktrees o logs y se devuelven mediante referencias.

## Presupuesto operativo

- Cero subagentes por defecto.
- Fan-out habitual de 2 o 3; máximo normal de 5.
- Una generación de profundidad por defecto.
- Un único writer por archivo, contrato o estado compartido.
- Una sola devolución automática por fallo corregible; después se escala.
- Modelo barato para ejecución mecánica; modelo fuerte para ambigüedad, integración o auditoría crítica.

## Riesgo y calidad

Las verificaciones se asignan por riesgo, no por ceremonia:

- bajo: checks focalizados del implementador;
- medio: tests relevantes y revisión del diff por el Architect;
- alto: tests obligatorios y Auditor independiente.

Alto riesgo incluye auth, secretos, RLS, migraciones destructivas, dinero, cálculos núcleo, contratos públicos y datos irreversibles.

## Recibo de cierre

Todo paquete delegado devuelve:

- resultado y artefactos;
- archivos modificados;
- pruebas ejecutadas u omitidas con motivo;
- riesgos y supuestos;
- decisiones pendientes;
- razón de parada.

## Señales para evolucionar el sistema

Registrar por tarea:

- topología elegida;
- agentes creados;
- tokens y tiempo aproximados;
- retrabajo o conflictos de integración;
- verificaciones fallidas;
- valoración final del resultado.

Una topología o agente especializado solo se convierte en patrón permanente cuando mejora repetidamente calidad, coste o tiempo. Los casos exitosos y repetibles deben convertirse en skills con responsabilidad única, no en más texto global.

## Referencias de diseño

- Anthropic, *How we built our multi-agent research system*.
- Anthropic, *Effective context engineering for AI agents*.
- OpenAI, *How OpenAI uses Codex*.
- Google, *Subagents have arrived in Gemini CLI*.
- Microsoft, *Multi-agent patterns* y *Orchestrator and subagent pattern*.
- Xu et al., *Discovering Hierarchical Software Engineering Agents via Bandit Optimization*, ICLR 2026.
- Park et al., *Capable language models can outgrow the benefits of collaboration*, Nature Machine Intelligence, 2026.
