# Arquitectura adaptativa de agentes

## Decisión

La configuración deja de modelar el trabajo como una jerarquía fija de tres niveles. El sistema usa un agente principal fuerte y selecciona dinámicamente una topología según independencia, acoplamiento, aislamiento de contexto, paralelismo, permisos, riesgo y coste de coordinación.

Los nombres `architect`, `orchestrator`, `supervisor`, `worker` y `auditor` se mantienen por compatibilidad, pero representan capacidades temporales, no puestos por los que toda tarea deba circular.

La arquitectura combina tres capas complementarias:

1. **Harness/context engineering:** herramientas, permisos, worktrees y contexto disponible para cada ejecución.
2. **Loop engineering:** cómo cada nodo actúa, observa evidencia, verifica y converge o se detiene.
3. **Graph engineering:** cómo se conectan varios nodos, qué dependencias existen y quién gobierna routing, joins y recuperación.

Loop y graph engineering no sustituyen al router adaptativo. El router decide si hace falta un solo loop o un grafo de varios loops.

## Por qué cambia

Una jerarquía fija introduce tres problemas:

1. replica el contexto y las instrucciones en cada salto;
2. añade latencia y pérdida de intención aunque el trabajo esté acoplado;
3. confunde complejidad o número de archivos con divisibilidad real.

Los sistemas modernos obtienen ventaja de múltiples agentes principalmente cuando pueden explorar direcciones independientes, aislar contextos largos, trabajar con herramientas o permisos distintos, o aportar una verificación realmente independiente. En tareas acopladas, un agente fuerte con un plan suele ser más eficiente.

## Loop engineering

Cada unidad de trabajo usa un bucle local y acotado:

`objetivo verificable → actuar → observar evidencia real → verificar → corregir o terminar`

Un loop válido declara antes de empezar:

- condición observable de éxito;
- verificador real — test, lint, consulta, reproducción, diff o evaluator;
- estado persistente mínimo;
- estrategia de recuperación;
- límite de iteraciones;
- condición de escalado humano o al Architect.

Reglas:

- máximo normal de una corrección automática después de un fallo;
- una segunda vuelta exige nueva evidencia o una estrategia distinta;
- nunca usar objetivos abiertos como “seguir hasta que esté perfecto”;
- writer y reviewer deben estar separados cuando la independencia compense el coste;
- si el verificador no mide progreso, se corrige el verificador antes de continuar.

Esto ya estaba parcialmente presente mediante verificaciones, receipts y stop conditions. Ahora queda explícito como contrato de ejecución, no como comportamiento implícito del modelo.

## Graph engineering

Cuando una tarea contiene varios paquetes, el flujo se representa como un grafo pequeño. Cada nodo es un loop con:

- objetivo;
- entradas tipadas o artefactos concretos;
- salida esperada;
- owner y permisos;
- verificador;
- stop condition.

Cada arista representa una dependencia de artefacto o una condición verificable. Se prefiere un DAG determinista: fan-out para trabajo independiente, joins para integración y pipelines para dependencias ordenadas.

Los ciclos solo se permiten como bucles locales de reparación alrededor de un verificador y siempre tienen límite. El LLM puede proponer routing, pero el runtime o el Orchestrator conserva el control de dependencias, ownership, permisos y número máximo de iteraciones.

No se usa un grafo por moda. Para un trabajo acoplado, un plan secuencial de un solo agente sigue siendo superior. Graph engineering aporta valor cuando hace explícitos paralelismo, bloqueos, joins, revisiones independientes, checkpoints o recuperación.

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
- número de iteraciones por loop;
- retrabajo o conflictos de integración;
- verificaciones fallidas;
- valoración final del resultado.

Una topología o agente especializado solo se convierte en patrón permanente cuando mejora repetidamente calidad, coste o tiempo. Los casos exitosos y repetibles deben convertirse en skills con responsabilidad única, no en más texto global.

## Referencias de diseño

- Anthropic, *How we built our multi-agent research system*.
- Anthropic, *Effective context engineering for AI agents*.
- OpenAI, *How OpenAI uses Codex* y *Symphony*.
- Google, *Subagents have arrived in Gemini CLI*.
- Microsoft, *Multi-agent patterns* y *Orchestrator and subagent pattern*.
- Ruan et al., *AOrchestra: Automating Sub-Agent Creation for Agentic Orchestration*, 2026.
- Sarker et al., *GraphBit: A Graph-based Agentic Framework for Non-Linear Agent Orchestration*, 2026.
- Qi et al., *LLM-as-Code Agentic Programming for Agent Harness*, 2026.
- Xu et al., *Discovering Hierarchical Software Engineering Agents via Bandit Optimization*, ICLR 2026.
- Park et al., *Capable language models can outgrow the benefits of collaboration*, Nature Machine Intelligence, 2026.