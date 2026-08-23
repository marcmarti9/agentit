# Directrices globales para agentes

Estas reglas son comunes a cualquier repositorio. Las instrucciones locales del proyecto prevalecen cuando sean más específicas.

## Harness Agentit

### Activación

**Única frase especial:** cualquier forma natural de “usar Agentit” en el idioma del usuario (`usa agentit`, `use agentit`, `utilise agentit`, etc.) cuando quede claro que se activa el harness **Agentit**.

Cuando Agentit esté activo:

1. Carga `using-agentit`.
2. Sigue su playbook el resto de la sesión.
3. No improvises otra metodología incompatible.

Agentit es provider-neutral. Cambiar de proveedor o modelo puede cambiar la primitiva de workers, pero no el protocolo.

## Decisiones de tarea: solo IA

**No existe un router programado.** No ejecutes un script, regex, árbol de keywords, clasificador Python ni validador semántico para decidir qué significa una petición.

La **IA principal** interpreta la tarea usando el contexto completo disponible: conversación, repo, archivos, herramientas, estado anterior, instrucciones y restricciones. Es la propietaria de la decisión semántica. No delegues esa responsabilidad a un modelo barato por ahorro de coste.

Antes de ejecutar debe formar una decisión explícita `TASK_DECISION` con, como mínimo:

- intención real y resultado esperado;
- hechos conocidos y dudas materiales;
- categoría/domain pack;
- complejidad;
- riesgo `RISK_0..RISK_4` y por qué;
- reversibilidad y efectos externos;
- skills/herramientas necesarias;
- topología: `direct`, `probe`, `fan_out`, `pipeline`, `writer_reviewer` o `audit`;
- especialistas/worker roles si aportan valor;
- plan de ejecución;
- verificación;
- backup/rollback/post-check cuando aplique.

El marco es estable; la respuesta puede cambiar con el contexto. La IA debe razonar sobre significado, no sobre coincidencias de palabras.

## Auditoría barata obligatoria antes de ejecutar

Después de que el modelo principal proponga `TASK_DECISION`, pide una segunda opinión independiente antes de ejecutar cambios materiales.

Para trabajo ordinario usa el modelo/endpoint competente más barato disponible, preferiblemente tier semántico `fast` y, cuando sea barato, de una familia distinta al modelo principal.

Este modelo es **auditor, no router ni autoridad final**. No debe sustituir la `TASK_DECISION`, asignar una clasificación alternativa como si fuese definitiva ni ejecutar el trabajo. Recibe solo:

- petición exacta del usuario y restricciones materiales;
- hechos relevantes ya inspeccionados;
- `TASK_DECISION` propuesta;
- reglas relevantes de Agentit.

Devuelve:

```text
AUDIT: CLEAR | CHALLENGE | ESCALATE
FINDINGS:
- ...
SUGGESTED_CHECKS:
- ...
CONFIDENCE: low | medium | high
```

Debe buscar activamente riesgo infravalorado, restricciones olvidadas, mala selección de skills/herramientas, delegación innecesaria o insuficiente, dependencias mal modeladas y verificación débil.

`CLEAR` significa que no encontró una objeción material.

`CHALLENGE` obliga al principal a reconsiderar el hallazgo. El principal sigue siendo el dueño de la decisión: puede corregirla o mantenerla con una justificación basada en evidencia. Si persiste un desacuerdo material, se escala.

`ESCALATE` significa que hace falta un modelo fuerte independiente. El modelo barato no arbitra el conflicto.

Máximo dos ciclos ordinarios de auditoría/reconsideración antes de escalar o exponer la incertidumbre.

Si no se puede spawnear otro modelo, usa un contexto aislado/fresco con el mismo contrato cuando sea posible. Para trabajo de riesgo alto, una autocrítica en el mismo contexto no equivale a la revisión fuerte independiente requerida.

### Escalado de revisión fuerte

El auditor barato **no sustituye** una revisión fuerte cuando el coste del error o el desacuerdo es alto.

Usa un reviewer/critic de tier `critic` o `judgment` cuando:

- `RISK_3` o `RISK_4`;
- el auditor barato devuelve `ESCALATE`;
- persiste un `CHALLENGE` material tras reconsideración del principal;
- hay operación destructiva o difícilmente reversible;
- hay auth, pagos, secretos, PII, migraciones de datos o producción;
- hay un plan estructural grande antes del compromiso de implementación.

El critic fuerte revisa la `TASK_DECISION` del principal y los hallazgos del auditor barato. No se convierte en implementador, pero actúa como **gate independiente de juicio**: no se ejecuta trabajo material hasta resolver las objeciones críticas, revisar el plan o conseguir la decisión del usuario que falte.

Para operaciones destructivas: `RISK_4`, backup verificado, rollback y post-check. Para `RISK_4`, preview/dry-run siempre que tenga sentido técnico.

## Playbook compacto

| Paso | Acción |
|---|---|
| 0. Inspect | Recupera hechos y contexto antes de decidir o preguntar. |
| 1. Decide | El modelo principal crea `TASK_DECISION` usando `task-router`. |
| 2. Audit | Worker barato independiente busca fallos; no decide por el principal. |
| 3. Escalate | Si hay riesgo alto o desacuerdo material, critic/judgment fuerte arbitra antes de ejecutar. |
| 4. Interview | Si afecta producto, una sola ronda útil con todas las decisiones materiales no deducibles. |
| 5. Persist | Mantén `docs/agentit/STATE.md` o equivalente en trabajo sustancial. |
| 6. Skills | Carga solo bodies realmente útiles + core mínimo. IDs no equivalen a skills cargadas. |
| 7. MCP/tools | Usa solo herramientas que aporten; inventario real y least privilege. |
| 8. Execute | Ejecuta la decisión revisada. Delegación inteligente, no decorativa. |
| 9. Document | Actualiza Markdown durable: arquitectura, componentes, contratos, decisiones y troubleshooting afectados. |
| 10. Verify | No declares `done/fixed/passing` sin evidencia fresca ni revisión de drift documental. |
| 11. Git | Branch + PR por defecto para cambios de repositorio. |

## Documentación obligatoria

El chat y el código por sí solos no son documentación suficiente. En trabajo sustancial de repositorio, Agentit debe aplicar `docs/DOCUMENTATION_CONTRACT.md` junto con el contrato de continuidad.

Objetivo: un agente o ingeniero nuevo debe poder entender el sistema relevante **desde la arquitectura completa hasta cada pieza materialmente afectada**, incluyendo por qué existe, cómo interactúa, qué contratos/invariantes mantiene, qué decisiones se tomaron y cómo diagnosticar fallos, sin tener que leer todo el código ni reconstruir el historial de conversación.

Reglas mínimas:

- `docs/agentit/STATE.md` mantiene estado operativo y recuperación; no sustituye la documentación permanente.
- Actualiza la documentación canónica existente; no crees duplicados que puedan divergir.
- Documenta decisiones durables no obvias con contexto, decisión, alternativas, consecuencias y condición de revisión; nunca chain-of-thought privado.
- Documenta componentes no triviales con responsabilidad, ubicación, inputs/outputs, flujo, dependencias, configuración, fallos y verificación.
- Mantén arquitectura, interfaces, datos/eventos, operaciones y troubleshooting alineados con el código.
- Si una decisión, contrato, componente o fallo descubierto sería costoso de redescubrir, debe quedar persistido en `.md` durante el trabajo, no solo al final.
- Antes de declarar completado un cambio sustancial, comprueba explícitamente drift documental. Si la documentación relevante ya no describe la realidad, el trabajo no está terminado.

## Skills y packs

Los perfiles (`frontend`, `backend`, `design`, etc.) son familias de conocimiento. La IA principal decide cuáles necesita leyendo su metadata y cuerpos cuando corresponda; ningún script ni auditor barato decide semánticamente por ella.

Una skill no se considera usada por aparecer en una lista. El modelo que ejecuta una etapa debe leer su `SKILL.md` o recibir una inyección provider-native equivalente.

## Delegación

- No fuerces single-agent ni multi-agent por ideología.
- Spawnea cuando independencia, aislamiento, especialidad, amplitud o crítica fresca aportan valor.
- Un writer por archivo/shared state salvo aislamiento explícito por branch/worktree.
- El principal integra y responde ante el usuario.

## Continuidad

El chat es desechable. Estado canónico: `docs/agentit/STATE.md` o equivalente del proyecto. No persistas secretos ni chain-of-thought.

## Git / PR-first

`branch → commits → verificación → PR → merge por el usuario`, salvo excepción explícita.

## Reglas operativas

- Alcance solo lo pedido.
- Inspecciona primero los hechos afectados.
- Busca causa raíz; evita fallbacks falsos.
- No hagas deploys o migraciones remotas sin autorización.
- Verifica antes de cerrar.
- Simplicidad y coherencia.

## Precedencia

`safety > user > project > preferences > defaults`.