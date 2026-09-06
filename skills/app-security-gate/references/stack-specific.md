# Stack-specific security gate rules

Load only the section(s) that match the detected stack. These rules supplement `../SKILL.md`; they do not replace the provider-neutral gate.

## Supabase

- The browser-safe anonymous/publishable key is intentionally public; do not misclassify it as a leaked secret.
- `service_role` / secret keys are privileged and must never ship to the browser or untrusted client.
- If the browser can query Supabase directly, RLS is part of the authorization boundary. Enable it on exposed tables and verify explicit `SELECT`, `INSERT`, `UPDATE`, and `DELETE` behavior for the intended roles.
- Test policies adversarially with two real test users/tenants. Reading only the policy text is insufficient evidence.
- Storage buckets need equivalent object-level policy discipline; public buckets must be deliberately public.
- Review RPC/database functions using elevated execution contexts (`SECURITY DEFINER` or equivalent). Their input validation, `search_path`, ownership, and authorization can bypass ordinary RLS assumptions.
- Never treat a hidden UI element as protection for an RPC, Edge Function, or table mutation.

## Firebase

- Firebase web configuration values such as the normal client `apiKey`, project ID, and app ID are not secret credentials by themselves.
- Firestore, Realtime Database, and Storage Rules are the actual client-facing authorization boundary. Test rules with multiple users and unauthenticated requests.
- Never ship Admin SDK credentials/service-account private keys to the client.
- Cloud Functions / backend handlers must independently authorize privileged actions; client Rules do not automatically secure arbitrary server endpoints.
- App Check can reduce abuse but is not authorization.

## Managed authentication: Clerk, Auth0, Supabase Auth, Firebase Auth, Cognito, similar

- Do not add custom password hashing/storage when the provider owns password credentials.
- Verify server-side session/token validation on privileged actions; client SDK state is not sufficient.
- Validate the correct issuer/audience/authorized-party claims required by the provider and deployment model.
- Do not trust user-editable metadata for roles or entitlements. Privileged claims/metadata need a trusted write path.
- Test revoked, expired, malformed, and cross-tenant sessions.
- Review password reset, email verification, invite, MFA recovery, and account-linking flows for replay and account enumeration.

## Next.js

- Anything under `NEXT_PUBLIC_*` is browser-visible by design. Only put publishable/non-secret values there.
- Route Handlers, API routes, Server Actions, loaders, and other server entry points must enforce authorization at the action/resource boundary.
- Middleware can provide coarse routing/auth checks but is not a substitute for object-level authorization inside mutations and data loaders.
- Treat Server Actions as remotely invocable mutation endpoints: validate input and authorize every action.
- Do not serialize secrets or privileged database fields through Server Component props, page data, hydration payloads, or error objects.
- Verify cache behavior does not share authenticated or tenant-specific responses across users.

## Vercel / Netlify / Cloudflare / common serverless and edge deployments

- Separate development, preview/staging, and production environment variables and data stores where practical.
- Confirm server-only variables are not copied into client bundles by framework-specific public prefixes or build-time substitution.
- Per-process/in-memory rate limiting is often ineffective in serverless/edge topologies; use platform/shared enforcement when consistent limits matter.
- Review preview deployments: they may expose unfinished admin/debug routes or production-like data to a broader audience than production.
- Scope deployment tokens, CI credentials, and environment access to the minimum required project/environment.
- Confirm logs and exception capture do not export secrets or sensitive request bodies to third-party observability systems.

## Stripe and payment providers

- Publishable/public client keys are expected in the browser; secret/API keys and webhook signing secrets are not.
- Never grant products, subscriptions, credits, paid-order state, or entitlements based solely on a client-provided success flag or redirect query parameter.
- Verify webhook signatures using the provider's official mechanism and the exact request representation it requires.
- Add replay/idempotency handling so duplicate valid events do not double-apply sensitive state transitions.
- Re-fetch or derive authoritative payment state server-side when the risk warrants it.
- Keep payment-provider secret scopes minimal and separate test/live credentials.

## PostgreSQL / Prisma / common ORMs

- ORM query builders generally parameterize values, but raw-query escape hatches may not. Search for raw SQL/unsafe variants and verify each data flow.
- A type-safe ORM does not prevent IDOR/BOLA or mass assignment. Ownership/tenant predicates and explicit writable-field allowlists remain mandatory.
- Database roles should have the minimum permissions required by that service.
- Review migrations for new public tables/views/functions and privilege grants, not only application code.
- If RLS is used, test the runtime role actually used in production and verify privileged backend roles do not accidentally bypass intended tenant checks.

## Object storage: S3, R2, Supabase Storage, GCS, similar

- Private/user content should be private by default unless public access is an explicit product requirement.
- Generate object keys server-side or constrain client-provided keys so users cannot overwrite or traverse into other users' namespaces.
- Signed URLs should be scoped to the intended object/action and expire reasonably.
- Authorization must be checked before minting a signed URL; possession of a user-supplied object key is not authorization.
- For public assets, confirm metadata and bucket listings do not reveal unintended private objects.

## OAuth / social login

- Validate `state`/PKCE and the provider-specific callback requirements.
- Restrict redirect/return URLs to an explicit safe set; do not reflect arbitrary `next` URLs after authentication.
- Prevent account-linking confusion where an attacker can bind an external identity to an existing account without proving control of both sides.
- Keep client secrets server-side; public client IDs are identifiers, not secrets.

## AI / LLM features

- Model output remains untrusted data. Do not pass it directly to SQL, shell commands, `eval`, HTML sinks, file paths, or privileged tool calls.
- Prompt instructions are not an authorization boundary. Enforce tool/resource permissions in code.
- Keep secrets and other tenants' data out of prompts/retrieval contexts unless access was explicitly authorized.
- Partition RAG/vector retrieval by tenant/user where data is private.
- Rate-limit and bound expensive agent/LLM loops so an attacker cannot create unbounded cost or execution.