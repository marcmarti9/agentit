---
name: app-security-gate
description: Adversarial pre-deploy security gate for web apps and APIs, especially AI/vibe-coded builds. Use after substantial implementation, before production release, or when asked whether an app is safe to ship. Composes security-and-hardening with evidence-driven attack-path checks, safe remediation, and mandatory retesting. Not for pure security theory or a single isolated hardening question.
---

# App Security Gate

A working happy path is not evidence that an application is safe to ship. This skill turns security review into a release gate: inspect the actual implementation, identify which controls apply to the detected stack, attempt realistic misuse paths, fix what can be fixed safely, and retest the final tree.

This skill owns **gating and adversarial verification**. Use `security-and-hardening` as the underlying control library rather than duplicating its general secure-coding guidance.

## When to Use

Use this skill when any of the following is true:

- an app, API, dashboard, SaaS, ecommerce feature, or backend is about to be deployed;
- substantial functionality was generated or modified quickly by an AI coding agent;
- authentication, authorization, database access, uploads, webhooks, payments, admin features, or multi-tenant data are involved;
- the user asks whether an application is secure, production-ready, or likely to get hacked;
- a prototype is becoming a real product.

**Not for:** generic explanations of security concepts, one isolated vulnerability question, or work with no runnable/application surface. Use `security-and-hardening` directly for those.

## Required Companion Skills

- Load `security-and-hardening` for control-level guidance.
- Use `verification-before-completion` for evidence discipline.
- Use `verification-gauntlet` when the project supports Agentit's runnable verification probes.
- For Supabase/Postgres projects, also load `supabase-postgres-best-practices` when database policy or schema work is material.

## Gate Contract

The final result is exactly one of:

- **PASS** — no unresolved Critical or High finding; material attack paths were retested on the final tree; residual Medium/Low risks are documented.
- **BLOCKED** — one or more release-blocking findings remain, required evidence is unavailable, or a critical control could not be verified.

Never claim an application is "secure" in the absolute sense. A PASS means **production-ready from the scope of this security gate with the evidence collected**.

### Automatic release blockers

Block release when any of these is present or cannot be ruled out with reasonable evidence:

- a privileged secret is exposed in client code, build output, logs, or reachable Git history and has not been revoked/rotated;
- unauthenticated access to protected functionality;
- horizontal or vertical authorization bypass (IDOR/BOLA, cross-tenant access, admin-role bypass);
- realistic SQL/NoSQL/command/template injection, SSRF, or remote-code-execution path;
- plaintext/recoverable password storage when the application itself stores passwords;
- unsafe upload behavior that enables code execution, path traversal, or unintended private-object disclosure;
- missing verification on security-sensitive webhooks or callbacks where forgery can cause privileged state changes;
- production debug/admin surfaces that materially bypass normal controls.

## Process

### 1. Map the real attack surface

Inspect the repository and deployed architecture before applying a checklist. Record:

- frontend framework and what code executes in the browser;
- backend/API/serverless functions and public endpoints;
- authentication provider and session/token mechanism;
- database, ORM/query layer, row/tenant model, and direct client-to-database access;
- object/file storage and upload/download flows;
- privileged/admin functions;
- webhooks, payment callbacks, email flows, OAuth redirects, and third-party APIs;
- CI/CD, runtime environment, preview/staging/production boundaries;
- secrets, PII, payment data, health/financial data, or other sensitive assets.

Mark each control below as **applicable**, **not applicable with reason**, or **unverified**. Do not force stack-specific advice onto a stack where it does not apply.

For common stacks, load `references/stack-specific.md` only for the detected technologies.

### 2. Secrets and client exposure

Verify all of the following:

- no privileged API keys, database credentials, service-role keys, private keys, signing secrets, webhook secrets, or session secrets are shipped to the browser;
- values intentionally designed to be public are distinguished from privileged secrets rather than blindly hidden;
- `.env*`, CI variables, examples, fixtures, logs, error payloads, source maps/build artifacts, and generated config do not leak secrets;
- staged changes and repository history are checked for previously committed credentials;
- if a real secret reached a remote repository, **revoke/rotate first**; removing the line or rewriting Git history alone is insufficient;
- purge from history only after rotation and only with explicit authorization for the history rewrite.

### 3. Authentication and session integrity

Verify server-side enforcement, not UI behavior:

- every protected action validates the session/token server-side;
- session cookies use appropriate `HttpOnly`, `Secure`, `SameSite`, expiry, rotation, and revocation controls when cookies are used;
- token validation checks signature and relevant expiry/issuer/audience claims;
- password hashing is required only when the app itself stores passwords; managed auth providers own password storage otherwise;
- login, signup, MFA, password reset, email verification, and recovery flows cannot be trivially abused or replayed;
- reset/verification tokens expire and are single-use where appropriate;
- account existence is not unnecessarily enumerable through login/reset/signup responses or timing;
- login and recovery endpoints have abuse controls appropriate to the deployment topology.

### 4. Authorization, ownership, and tenant isolation

Authentication is not authorization. Attempt to cross every object and privilege boundary:

- request another user's record by changing IDs, slugs, query parameters, body fields, or GraphQL variables;
- update/delete another user's object directly through the API rather than through the UI;
- call admin/moderator/owner actions as a normal user;
- change `role`, `ownerId`, `tenantId`, `userId`, price, discount, status, approval flags, entitlement fields, or other privileged fields in request bodies;
- test list/search/export endpoints for cross-tenant leakage, not only single-record endpoints;
- verify database/RLS/storage policies where clients can reach those systems directly;
- verify server-side queries include the required ownership/tenant constraint even if the UI hides foreign records.

A client-side check, hidden button, route middleware, or guessed-unpredictable ID is never sufficient authorization.

### 5. Database and state mutation

Verify:

- parameterized queries or safe ORM bindings are used; untrusted data is not concatenated into SQL/NoSQL/query DSLs;
- server-side schemas validate input before state changes;
- writes use explicit allowlists/DTOs so extra client fields cannot cause mass assignment or field tampering;
- least-privilege database/service credentials are used;
- row-level security/policies are enabled and tested when they are part of the trust boundary;
- sensitive data is protected in transit, at rest, and with field-level encryption only where the sensitivity/threat model warrants it;
- backups, exports, analytics replicas, caches, and search indexes do not accidentally become weaker copies of protected data;
- API responses return only fields required by the caller; do not serialize entire database records by default.

### 6. Input, output, and dangerous sinks

Trace untrusted data from entry point to sink. Check for:

- server-side schema validation, length/range limits, and allowlists;
- contextual escaping/encoding and safe framework rendering for user-controlled content;
- XSS through HTML/Markdown/rich text, stored content, error messages, or model-generated output;
- SQL/NoSQL injection, shell/command injection, template injection, unsafe `eval`, unsafe deserialization, and path traversal;
- SSRF wherever a user can influence a server-side URL, including image proxies, imports, previews, webhooks, and crawlers;
- open/unsafe redirects in OAuth, login, checkout, or `next`/`returnUrl` flows;
- CORS that is restricted to intended origins and never combines wildcard trust with credentials.

Do not run destructive exploit payloads against production. Prefer controlled local/staging repros or static/data-flow evidence when active testing could harm real systems.

### 7. File uploads and object storage

When uploads exist, verify:

- size limits, file-count limits, and authenticated/authorized upload paths;
- type checks do not trust the extension or client-provided MIME value alone when content is security-sensitive;
- filenames/paths are generated safely and cannot traverse directories or overwrite arbitrary objects;
- uploaded content cannot execute as application code;
- private files are private by default and downloads re-check authorization or use appropriately scoped/expiring signed URLs;
- image/document processing libraries are patched and resource limits prevent decompression/processing abuse;
- malware scanning or quarantine is used when the product's threat model warrants it.

### 8. Webhooks, external integrations, and abuse controls

Verify:

- webhook signatures/authentication are checked before processing privileged events;
- timestamp/freshness or event-ID deduplication prevents replay where replay matters;
- payment/order/entitlement state is derived from trusted server-side events, not client-submitted success flags;
- external API credentials are scoped to least privilege;
- login, reset, signup, invitation, verification, expensive search/AI endpoints, and mutation-heavy APIs have rate limits appropriate to expected abuse;
- multi-instance/serverless deployments use a shared or platform-level limiter rather than per-process counters when consistency matters;
- bot protection/CAPTCHA is added only where abuse evidence or risk warrants it; do not use it as a substitute for authorization or rate limiting.

### 9. Browser, transport, API, and deployment hardening

Verify the deployed configuration, not just source intent:

- HTTPS is enforced end-to-end; HSTS is used where appropriate;
- CSP, `frame-ancestors`/anti-clickjacking, `X-Content-Type-Options`, Referrer Policy, and Permissions Policy are set appropriately;
- CSRF is addressed for cookie-authenticated state-changing requests unless the architecture provides an equivalent protection;
- production errors do not expose stack traces, queries, filesystem paths, secrets, or internal identifiers unnecessarily;
- debug endpoints, development bypasses, test accounts, default credentials, and unintended admin panels are absent from production;
- source maps/build metadata are intentionally exposed or withheld based on whether they reveal sensitive implementation details;
- public ports/services and cloud/storage permissions match the intended attack surface;
- preview/staging and production secrets/data are separated.

### 10. Dependency and supply-chain review

Use the repository's actual package manager and committed lockfile. Verify:

- the dependency graph installs reproducibly;
- native advisory scans are run and Critical/High results are triaged for reachability and fix risk;
- unreviewed package lifecycle/install scripts are not blindly executed;
- new dependencies and suspicious lockfile changes are reviewed for provenance, ownership, typosquatting, unexpected scripts, and transitive risk;
- forced/breaking audit remediation is not applied blindly;
- CI/CD credentials have minimum required scope and untrusted PR/build contexts cannot read privileged secrets.

## Adversarial Retest Matrix

After fixes, retest the **final tree**. At minimum, cover every applicable row:

| Attack path | Required evidence |
|---|---|
| Unauthenticated protected request | Direct API/server call is rejected |
| Horizontal IDOR/BOLA | User A cannot read/update/delete User B's object |
| Vertical privilege escalation | Normal user cannot invoke admin/owner action |
| Cross-tenant list/search/export | Tenant A receives no Tenant B records |
| Field tampering / mass assignment | Privileged fields are ignored/rejected server-side |
| Expired/tampered/replayed session | Invalid session is rejected and sensitive action does not occur |
| Password reset / verification abuse | Tokens expire/single-use as applicable; responses avoid needless enumeration |
| Injection / dangerous sink | Controlled malicious inputs remain data, not executable/query structure |
| XSS / rich user content | Output renders safely in the relevant browser surface |
| SSRF / outbound URL control | Disallowed/private destinations cannot be reached through user-influenced fetches |
| File upload abuse | Disallowed type/size/path/access attempts fail safely |
| Webhook forgery/replay | Bad signature or disallowed replay cannot mutate privileged state |
| Rate-limit abuse | Repeated auth/high-cost attempts are throttled in the real deployment topology |
| API overfetching | Sensitive/internal fields are absent from responses |

If a test would be unsafe against production, use staging/local execution, an isolated test tenant, or static evidence and record the limitation.

## Safe Auto-Fix Policy

When the repository is writable, fix issues instead of merely listing them **when the change is bounded, reversible, and testable**. Typical safe fixes include:

- server-side validation schemas and explicit writable-field allowlists;
- missing ownership/tenant guards;
- response DTO/serializer allowlists;
- secure cookie flags and token checks;
- security headers, strict CORS configuration, and safe redirect validation;
- upload size/type/path restrictions;
- rate-limit integration/configuration;
- tests that reproduce IDOR, privilege, tampering, replay, and leakage regressions;
- database/RLS migrations as code when they can be reviewed before deployment.

Do **not** silently perform irreversible or production-wide actions. Require explicit authorization and a rollback plan before revoking live credentials, rewriting published Git history, deleting production data, changing live tenant/admin roles, or applying policy changes that could lock users out.

## Stack-Specific Rules

Do not memorize folklore such as "all API keys must be hidden." Some stacks intentionally expose identifiers or publishable keys while relying on server-side policy as the security boundary.

Load `references/stack-specific.md` for the detected stack. Its rules currently cover Supabase, Firebase, managed auth providers, Next.js, common serverless deployments, payments/webhooks, and object storage.

## Required Close-Out

Return a compact report with this shape:

```text
SECURITY GATE: PASS | BLOCKED
Scope:
- architecture / surfaces reviewed

Findings:
- [Critical|High|Medium|Low] finding — evidence — affected path/surface

Fixes applied:
- change — verification

Adversarial retest:
- attack path — PASS/FAIL — evidence

Residual risk / unverified:
- item — reason — owner/follow-up
```

Do not inflate severity. A finding's severity depends on exploitability, privileges required, blast radius, data sensitivity, and deployment context.

## Completion Criteria

The skill is complete only when:

- [ ] attack surface and trust boundaries are documented;
- [ ] every relevant control is classified as applicable, not applicable with reason, or unverified;
- [ ] secrets/client exposure and Git-history risk were checked;
- [ ] authentication, authorization, ownership, admin, and tenant boundaries were tested where applicable;
- [ ] input/output, database, file, webhook, session, deployment, and supply-chain surfaces were reviewed where applicable;
- [ ] safe fixes were applied and verified instead of only recommended;
- [ ] adversarial tests were rerun on the final tree after fixes;
- [ ] no unresolved Critical/High finding remains for PASS;
- [ ] every evidence gap or accepted residual risk is explicit;
- [ ] final status is PASS or BLOCKED, never a vague "looks secure".