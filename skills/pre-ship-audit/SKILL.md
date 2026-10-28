---
name: pre-ship-audit
description: |
  Run a multi-subagent pre-ship audit on a web app, API or vibe-coded site before production or first payment.
  Covers performance/SEO, adversarial security, design consistency and payment/data readiness.
  Use when the user asks if something is ready to ship, before accepting real money, or after a substantial implementation.
license: Apache-2.0
---

# Pre-Ship Audit

A working happy path is not enough. This skill forces parallel independent checks before shipping or taking payment.

It composes existing skills (`app-security-gate`, `performance-optimization`, `web-design-guidelines`, etc.) into a bounded multi-subagent workflow and produces a single pass/fail table.

## When to use

- Before the first real payment or public launch.
- When the user says "is this ready to ship?" or "check this before we go live".
- After a large vibe-coded implementation that has not been audited.

Do not use for:
- Tiny CSS or copy changes with no trust boundary.
- Pure research or design exploration.

## Workflow

1. Confirm the environment is **not** connected to production data. Prefer local or a dedicated preview.
2. Split work across 4–5 subagents (or sequential passes if the host cannot fan out):
   - **Performance & SEO**
   - **Security (adversarial)**
   - **Design consistency & states**
   - **Payments & data** (if money or user data is involved)
   - **After-launch readiness** (monitoring, backups, legal)
3. Each subagent only records findings. No edits until the table is reviewed.
4. Primary agent fixes from the lists, then re-runs the same checks.
5. Deliver a before/after table.

## Check groups

### Performance & SEO
- Server-side or static rendering where it matters.
- Images WebP/AVIF, correctly sized, lazy below the fold.
- Fonts loaded the framework way; third-party scripts deferred.
- Bundle size, dynamic imports for heavy components.
- Sitemap, robots.txt, noindex, canonicals, meta descriptions, H1, FAQ schema, breadcrumbs, alt text.
- Lighthouse mobile (median of 3 runs) on home + 2–3 slowest pages.
- No orphan pages, no redirect chains, no layout shifts.

### Security (adversarial)
- Unauthenticated direct table access with frontend keys.
- IDOR: swap IDs between test users A and B.
- Role escalation via request body or direct DB write.
- Password-reset link reuse.
- Bypass UI limits by calling APIs directly.
- XSS in user-generated content and Markdown.
- SSRF if the app fetches URLs.
- Cache leaks of authenticated content.
- Preview links accessible without auth.
- Prompt-injection in uploaded docs or fetched pages.

Every attack must be executed, not just read in code. After a fix, temporarily disable the control, prove the attack works, re-enable and prove it fails.

### Design consistency & states
- Single DESIGN.md (or equivalent) that colours, type, spacing and radii follow.
- Loading, empty and error states exist and look intentional.
- Every button has hover/pressed/disabled feedback.
- Mobile: no horizontal scroll, tappable targets, text enlargement does not break layout.
- One primary CTA per page. No placeholder text left.

### Payments & data (when relevant)
- Private keys only on the server; git history searched.
- Every endpoint checks auth and permissions server-side; RLS on.
- Spending caps / alerts on metered services.
- Webhooks verify signature; idempotent processing.
- Refunds, cancellations and failed charges tested in test mode.
- Money as integers (smallest currency unit).
- Double-submit creates only one order.
- Soft delete + real wipe on account deletion.
- Users can export their data.
- Daily backups + one successful restore test (on a copy).

## Output

Produce a table:

| Group | Item | Status (pass/fail/needs confirmation) | File / location | Evidence |
|---|---|---|---|---|

Then a short list of must-fix items and the re-test results after fixes.

## Relationship to other skills

- Use `app-security-gate` as the security implementation owner; this skill owns the multi-check orchestration and the table.
- Prefer `high-end-motion-video` or `advertising-video-production` for video deliverables; this skill is for the app/site itself.
- Load `performance-optimization` and `web-design-guidelines` as supporting bodies when the host supports it.
