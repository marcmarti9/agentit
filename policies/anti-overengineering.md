# Política anti-overengineering

Aplica la intervención correcta más pequeña que satisfaga la petición y pueda verificarse.

- Respeta la arquitectura, dependencias y estilo ya presentes.
- No introduzcas una abstracción usada una sola vez sin una razón concreta.
- No añadas dependencias, servicios, colas, cachés, bases de datos o microservicios sin necesidad actual.
- No conviertas constantes en configuración, ni diseñes extensibilidad hipotética.
- No hagas refactors globales para resolver un problema local.
- No escribas documentación ajena al cambio.
- No ejecutes una auditoría completa cuando una comprobación dirigida sea suficiente.
- No lances subagentes si coordinar y verificar cuesta más que hacerlo directamente.
- No apliques TDD ceremonialmente a un cambio trivial; sí prueba lógica material, regresiones, contratos y fronteras de riesgo.
- Distingue “podría ser útil” de “es necesario ahora”.
- Conserva una ruta clara de rollback y deja las decisiones experimentales aisladas.

## Cadencia de desarrollo

La validación se escala por fase y riesgo, no por ansiedad:

- **BUILD:** implementación + comprobación dirigida mínima + continuar. No ejecutar por defecto toda la suite, build, lint, typecheck y E2E después de cada cambio pequeño.
- **FEATURE CHECKPOINT:** comprobar el comportamiento end-to-end de la feature y el conjunto de regresión directamente relacionado.
- **MILESTONE / PRODUCT COMPLETE:** ejecutar una vez la verificación amplia requerida por el repositorio, revisar integración, seguridad/release cuando aplique y simplificar el diff.
- **Excepción:** auth, permisos, pagos, migraciones, pérdida de datos, concurrencia, secretos y otros límites de alto impacto requieren evidencias más fuertes antes de seguir.

Los tests compran confianza; no son un objetivo de volumen. No añadas tests triviales, duplicados o de detalles de implementación solo para aumentar cobertura.

La skill `anti-overengineering` operacionaliza esta política y, cuando se combina con `incremental-implementation`, gobierna la cadencia de verificación.
