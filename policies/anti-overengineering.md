# Política anti-overengineering

Agentit usa exactamente dos modos de desarrollo:

```text
DEVELOPMENT_MODE: BUILDER | REVIEW
```

## BUILDER

Objetivo: terminar todas las features solicitadas.

- Implementa de forma directa y respeta arquitectura/estilo existentes.
- Tras cada cambio usa solo la comprobación dirigida mínima que aporte información útil.
- No ejecutes por defecto toda la suite, build, lint, typecheck y E2E después de cada feature.
- No añadas tests triviales, duplicados o de detalles de implementación.
- No hagas refactors globales, documentación ceremonial, abstracciones hipotéticas ni subagentes que cuesten más de coordinar que resolver.
- Continúa construyendo hasta que el conjunto funcional pedido esté implementado.

## REVIEW

Objetivo: revisar profundamente el producto ya construido, sin añadir nuevas features.

- Congela el scope funcional.
- Ejecuta los gates amplios exigidos por el repositorio.
- Revisa integración, E2E críticos, seguridad, migraciones/datos, dependencias, rendimiento, accesibilidad y documentación solo cuando apliquen.
- Inspecciona el diff completo y elimina complejidad accidental demostrada.
- Corrige findings en lotes con checks dirigidos; vuelve a ejecutar los checks globales al final del lote, no tras cada línea.

## Regla de justificación

Una abstracción, test, dependencia, documento, worker, review o comando adicional debe responder a un requisito actual, bug observado, contrato existente o riesgo real. "Podría servir", "future-proof" y "por si acaso" no bastan.

## Excepción de riesgo

Auth, permisos, pagos, secretos, migraciones destructivas, datos de producción, concurrencia y otros límites de alto impacto se verifican de forma dirigida tan pronto como sea necesario. Esto no convierte automáticamente todo BUILDER en REVIEW.

La skill `anti-overengineering` operacionaliza esta política y gobierna la cadencia cuando se combina con otras skills de implementación/testing/review.
