# Clasificación de riesgo

Usa el nivel más alto que aplique. La etiqueta proporcionada por el usuario puede subir el nivel, pero nunca rebajarlo cuando la tarea contiene señales de mayor impacto.

| Nivel | Alcance | Requisito mínimo |
|---|---|---|
| RISK_0 | conversación, explicación o brainstorming sin cambio real | concisión segura; sin skills salvo necesidad explícita |
| RISK_1 | cambio trivial y reversible, como CSS localizado, texto o formato | compresión estructural moderada; verificación dirigida |
| RISK_2 | feature, bug, refactor o integración normal | contexto arquitectónico suficiente; compresión selectiva y reversible |
| RISK_3 | auth, permisos, pagos, PII, APIs públicas, infraestructura, despliegue, migraciones, persistencia o concurrencia | contexto completo recuperable; pruebas amplias; revisión independiente |
| RISK_4 | producción, eliminación o transformación irreversible, backups/restores, credenciales, permisos críticos o pérdida potencial de datos | fidelidad completa; backup verificado; dry run; revisión independiente; comprobación posterior |

## Suelo de seguridad

Antes de clasificar, inspecciona destino, entorno, alcance, archivos afectados y reversibilidad. Si existe ambigüedad material, detente o eleva el riesgo. No trates una salida truncada, resumen o resultado comprimido como evidencia suficiente para RISK_3/RISK_4.

## Verificación

- RISK_0: verifica comprensión solo cuando el usuario pida un cambio.
- RISK_1: ejecuta una comprobación dirigida y conserva el diff.
- RISK_2: prueba el comportamiento afectado y revisa regresiones plausibles.
- RISK_3: ejecuta suite relevante, revisa seguridad y recupera originales antes de decidir.
- RISK_4: confirma backup y destino, usa dry run, obtiene segunda revisión y valida el estado después; si un dato crítico falta, no actúes.
