# Semantic vs mechanical reference enforcement

Agentit's reference system deliberately splits responsibility:

- **AI semantic responsibility:** decide whether references matter and which domain/sources/packs are relevant.
- **Mechanical runtime responsibility:** once the AI chooses `catalog`, `live`, or `mixed`, require concrete source/evidence/provenance fields before a verification receipt can pass.

This avoids both failure modes:

1. brittle programmatic routing such as `if "website" in prompt -> web references`;
2. purely advisory instructions that an agent can mention and then ignore.

The verifier never decides that a fiscal task is fiscal or that a landing page needs design references. It only checks the explicit decision produced by the reviewed `TASK_DECISION`.
