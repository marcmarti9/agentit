# Clasificación de riesgo

Usa el nivel más alto que aplique a la acción solicitada y al entorno de destino. La etiqueta proporcionada por el usuario puede subir el nivel, pero nunca rebajarlo cuando la tarea contiene señales de mayor impacto.

| Nivel | Alcance | Requisito mínimo |
|---|---|---|
| RISK_0 | conversación, explicación o brainstorming sin cambio real | concisión segura; sin skills salvo necesidad explícita |
| RISK_1 | cambio trivial y reversible, como CSS localizado, texto o formato | compresión estructural moderada; verificación dirigida |
| RISK_2 | feature, bug, refactor o integración normal | contexto arquitectónico suficiente; compresión selectiva y reversible |
| RISK_3 | cambio solicitado en auth, permisos, pagos, PII, APIs públicas, infraestructura, despliegue, migraciones, persistencia o concurrencia | contexto completo recuperable; pruebas amplias; revisión humana e independiente |
| RISK_4 | acción solicitada en producción, eliminación o transformación irreversible, restore, credenciales, permisos críticos o pérdida potencial de datos | fidelidad completa; backup verificado; dry run; revisión humana e independiente; comprobación posterior |

## Intención y entorno

La presencia de una palabra sensible no basta para elevar el riesgo: «explica un backup» es RISK_0 y «documenta `chmod`» es RISK_1 porque no piden ejecutar esas operaciones. En cambio, «restaura este backup en producción» solicita una acción sobre un entorno real y es RISK_4. Si la intención o el destino no están claros, pide confirmación o conserva el nivel superior; el router no autoriza la ejecución.

## Suelo de seguridad

Antes de clasificar, inspecciona destino, entorno, alcance, archivos afectados y reversibilidad. Si existe ambigüedad material, detente o eleva el riesgo. No trates una salida truncada, resumen o resultado comprimido como evidencia suficiente para RISK_3/RISK_4.

## Verificación

- RISK_0: verifica comprensión solo cuando el usuario pida un cambio.
- RISK_1: ejecuta una comprobación dirigida y conserva el diff.
- RISK_2: prueba el comportamiento afectado y revisa regresiones plausibles.
- RISK_3: ejecuta suite relevante, revisa seguridad y recupera originales antes de decidir.
- RISK_4: confirma backup y destino, usa dry run, obtiene segunda revisión y valida el estado después; si un dato crítico falta, no actúes.
