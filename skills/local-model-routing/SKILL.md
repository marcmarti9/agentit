---
name: local-model-routing
description: Assess an explicitly available local or remote model endpoint for a bounded role. Guidance only; no automatic model-routing implementation or capability parity is implied.
---

# Local model capability assessment

Use when the user requests local-first execution or an actual local endpoint is available and relevant. Merely listing an endpoint in preferences does not activate it, test it, or grant permission to send code to another provider.

`models/capabilities.yaml` is a discovery reference in a repository checkout, not a live router result. Installed runtime packaging may not include it. `router/preferences.py` accepts local-model preferences; Agentit currently does **not** implement an automatic `models.parent|worker|critic` route response. Never claim it does.

The primary model chooses a role using current evidence: reasoning, coding, bounded extraction or independent critique. Verify needed tools, context capacity, transport, privacy boundary and a small representative task against the real endpoint before relying on it. Record provider/model, version, observed capabilities, failures and verification date. A model name or declared tier is not evidence of parity.

Use the host's actual model/worker integration. An OpenAI-compatible endpoint is an interface claim, not proof that every tool or context feature works. No connection means this step is unavailable; do not fabricate execution. Do not install or contact a new provider, spend money or export private code without corresponding authorization.

For consequential review, preserve actual context isolation and disclose shared-model or unavailable-review limitations. Prefer genuinely complementary expertise when useful, but do not silently downgrade a high-risk critic or create a fixed hierarchy of provider brands.

On failure, use an authorized capable alternative or surface the blocked capability. Persist scoped evidence as data, not executable memory; retest after endpoint/version changes. Selection remains model-owned and task-scoped.
