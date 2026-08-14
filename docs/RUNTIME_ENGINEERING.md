# Runtime Engineering

Agentit enforces execution quality with three complementary layers:

- **Context Engineering**: what each agent receives (project instructions, scoped skills, capabilities, preferences).
- **Loop Engineering**: how each execution unit proves convergence.
- **Graph Engineering**: which units may run, in what dependency order, with what write ownership and handoff artifacts.

Runtime state lives under `.agentit/runtime/` and is intentionally ignored by git.

## Loop Engineering

Every executable unit with a verifiable outcome has a persisted loop contract:

```bash
python3 ~/code/agentit/router/runtime_cli.py loop-init \
  --state .agentit/runtime/loops/implementation.json \
  --goal "Homepage renders according to DESIGN_DIRECTION" \
  --verifier "browser QA + targeted tests" \
  --stop "desktop/mobile pass and no blocking critique findings"
```

After each attempt, record actual evidence:

```bash
python3 ~/code/agentit/router/runtime_cli.py loop-attempt \
  --state .agentit/runtime/loops/implementation.json \
  --result fail \
  --strategy "first implementation" \
  --evidence "mobile viewport overflows at 390px"
```

The default budget is two total attempts (one automatic retry). A retry must add fresh evidence or use a different strategy. A passing attempt requires non-empty verifier evidence and cannot report a non-zero verifier exit code.

A unit is accepted only when:

```bash
python3 ~/code/agentit/router/runtime_cli.py loop-check \
  --state .agentit/runtime/loops/implementation.json \
  --receipt .agentit/runtime/receipts/implementation.json
```

succeeds.

## Graph Engineering

Multi-node work is materialized as a DAG. Initialize each node loop first, then reference its state in the graph spec. `graph-init` resolves each loop's contract hash and binds the graph node to it.

Example Studio website graph spec:

```json
{
  "nodes": [
    {
      "id": "research-a",
      "objective": "Research editorial references",
      "loop_state": "loops/research-a.json"
    },
    {
      "id": "research-b",
      "objective": "Research cross-domain references",
      "loop_state": "loops/research-b.json"
    },
    {
      "id": "concept-1",
      "deps": ["research-a", "research-b"],
      "loop_state": "loops/concept-1.json"
    },
    {
      "id": "concept-2",
      "deps": ["research-a", "research-b"],
      "loop_state": "loops/concept-2.json"
    },
    {
      "id": "concept-3",
      "deps": ["research-a", "research-b"],
      "loop_state": "loops/concept-3.json"
    },
    {
      "id": "direction",
      "deps": ["concept-1", "concept-2", "concept-3"],
      "expected_artifacts": ["DESIGN_DIRECTION.md"],
      "loop_state": "loops/direction.json"
    },
    {
      "id": "implementation",
      "deps": ["direction"],
      "write_paths": ["src"],
      "loop_state": "loops/implementation.json"
    },
    {
      "id": "critic",
      "deps": ["implementation"],
      "loop_state": "loops/critic.json"
    },
    {
      "id": "qa",
      "deps": ["critic"],
      "loop_state": "loops/qa.json"
    }
  ]
}
```

If the graph spec is stored at `.agentit/runtime/graph-spec.json`, relative `loop_state` paths are resolved from that directory.

Initialize:

```bash
python3 ~/code/agentit/router/runtime_cli.py graph-init \
  --spec .agentit/runtime/graph-spec.json \
  --state .agentit/runtime/graph.json
```

Spawn only nodes returned by:

```bash
python3 ~/code/agentit/router/runtime_cli.py graph-ready \
  --state .agentit/runtime/graph.json
```

When a node returns a passed Loop Receipt:

```bash
python3 ~/code/agentit/router/runtime_cli.py graph-complete \
  --state .agentit/runtime/graph.json \
  --node research-a \
  --loop-receipt .agentit/runtime/receipts/research-a.json
```

For required handoff artifacts, pass each with `--artifact`. If a node cannot proceed, record the block with `graph-block` instead of silently bypassing it.

Final multi-node acceptance requires:

```bash
python3 ~/code/agentit/router/runtime_cli.py graph-check \
  --state .agentit/runtime/graph.json \
  --receipt .agentit/runtime/graph-receipt.json
```

## Enforced invariants

The runtime rejects:

- missing goals/verifiers/stop conditions;
- unbounded or exhausted retries;
- pass claims without evidence;
- repeated retry with neither new evidence nor a new strategy;
- malformed/tampered Loop Receipts;
- cycles, unknown/self dependencies and invalid DAG state;
- overlapping write ownership (`src` vs `src/page.tsx` also conflicts);
- unsafe write paths;
- advancing a node before dependencies complete;
- completing a node with another node's Loop Receipt;
- reusing one Loop Receipt for multiple nodes;
- missing expected handoff artifacts;
- final graph success while any node remains pending/blocked.

The runtime does not replace judgment. It makes the execution claims auditable and prevents the most common orchestration shortcuts from being silently accepted.
