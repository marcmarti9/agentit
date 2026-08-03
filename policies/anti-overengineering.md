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
- No apliques TDD ceremonialmente a un cambio trivial; sí prueba toda lógica, riesgo de regresión o comportamiento verificable.
- Distingue “podría ser útil” de “es necesario ahora”.
- Conserva una ruta clara de rollback y deja las decisiones experimentales aisladas.
