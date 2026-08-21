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

La IA principal interpreta la tarea usando el contexto completo disponible: conversación, repo, archivos, herramientas, estado anterior, instrucciones y restricciones. Antes de ejecutar debe formar una decisión explícita `TASK_DECISION` con, como mínimo:

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

## Revisión obligatoria antes de ejecutar

Después de que el modelo principal proponga `TASK_DECISION`, **siempre** pide una segunda opinión independiente antes de ejecutar cambios materiales.

Para trabajo ordinario usa el modelo/endpoint competente más barato disponible, preferiblemente tier semántico `fast` y, cuando sea barato, de una familia distinta al modelo principal. Este worker es read-only y recibe solo:

- petición exacta del usuario y restricciones materiales;
- hechos relevantes ya inspeccionados;
- `TASK_DECISION` propuesta;
- reglas relevantes de Agentit.

El reviewer devuelve `APPROVE`, `REVISE` o `BLOCK` y debe buscar activamente riesgo infravalorado, restricciones olvidadas, mala selección de skills/herramientas, delegación innecesaria o insuficiente, dependencias mal modeladas y verificación débil.

Si devuelve `REVISE`, el principal corrige la decisión y vuelve a revisarla cuando el cambio sea material. Máximo dos ciclos ordinarios antes de escoger una ruta conservadora o escalar la incertidumbre.

Si no se puede spawnear otro modelo, usa un contexto aislado/fresco con el mismo contrato. Si tampoco existe esa posibilidad, haz una autocrítica adversarial explícita y deja constancia de que no hubo independencia.

### Escalado de revisión

El reviewer barato **no sustituye** una revisión fuerte cuando el coste del error es alto.

- `RISK_3/RISK_4` → además, reviewer/critic de tier `critic` o `judgment`.
- Operación destructiva o difícilmente reversible → `RISK_4`, backup/rollback y post-check.
- Auth, pagos, secretos, PII, migraciones de datos o producción → revisión independiente fuerte.
- Plan estructural grande → critic independiente antes del compromiso de implementación.
- Superficie visual pública → `design` como dominio principal y verificación renderizada/browser.

## Playbook compacto

| Paso | Acción |
|---|---|
| 0. Inspect | Recupera hechos y contexto antes de decidir o preguntar. |
| 1. Decide | El modelo principal crea `TASK_DECISION` usando el protocolo `task-router`. |
| 2. Review | Worker barato independiente revisa la decisión; escala a critic/judgment cuando corresponda. |
| 3. Interview | Si afecta producto, una sola ronda útil con todas las decisiones materiales no deducibles. |
| 4. Persist | Mantén `docs/agentit/STATE.md` o equivalente en trabajo sustancial. |
| 5. Skills | Carga solo bodies realmente útiles + core mínimo. IDs no equivalen a skills cargadas. |
| 6. MCP/tools | Usa solo herramientas que aporten; inventario real y least privilege. |
| 7. Execute | Ejecuta la decisión revisada. Delegación inteligente, no decorativa. |
| 8. Verify | No declares `done/fixed/passing` sin evidencia fresca. |
| 9. Git | Branch + PR por defecto para cambios de repositorio. |

## Skills y packs

Los perfiles (`frontend`, `backend`, `design`, etc.) son familias de conocimiento. La IA decide cuáles necesita leyendo su metadata y cuerpos cuando corresponda; ningún script decide semánticamente por ella.

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