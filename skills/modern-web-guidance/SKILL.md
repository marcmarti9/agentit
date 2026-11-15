---
name: modern-web-guidance
description: Retrieve GoogleChrome Modern Web Guidance for concrete HTML, CSS and client-side JavaScript implementation, browser support and legacy-web modernization. Use for native web-platform choices; not for generic visual audits, backend-only work or routine tooling.
metadata:
  upstream: https://github.com/GoogleChrome/modern-web-guidance
  authority: agentit-adapter
---

# Modern Web Guidance

Use Google's current web-platform guidance as a just-in-time reference, not an always-loaded rule set. This is an Agentit-owned adapter: it does not vendor Google's skill, npm CLI, guide corpus or compatibility data. Agentit's core controls semantic selection, permissions, BUILDER/REVIEW mode and verification.

## When to select

Select for concrete HTML, CSS, browser JavaScript, DOM API, accessibility, performance or compatibility decisions where newer native web features might improve implementation; also for explicitly requested broad legacy-web modernization. Do **not** select merely because a task is frontend: `frontend-ui-engineering` owns general implementation, `web-design-guidelines` owns interface audits, and `playwright-cli` owns browser runtime checks. This skill never grants network, package-execution or deployment permissions.

## Search, retrieve and apply

1. Identify the web-platform primitive and the project's browser/version requirements; prefer any explicit support policy.
2. With authorized network and npm execution, search using a generic, focused 2–5 word query for **one** feature, not private project text:

   ```sh
   DISABLE_TELEMETRY=1 npx -y modern-web-guidance@latest search "light dismiss dialog"
   ```

   The first invocation can download and execute an external npm package. Review/authorize that trust boundary before running it; never auto-install project dependencies, enable tools or send private data. The upstream CLI documents `DISABLE_TELEMETRY=1` as its telemetry opt-out.
3. Read search result descriptions, select only relevant **returned** guide IDs, and retrieve their full contents:

   ```sh
   DISABLE_TELEMETRY=1 npx -y modern-web-guidance@latest retrieve "<returned-guide-id>"
   ```

   Do not invent guide IDs. If nothing relevant is found, rephrase once with a concrete UI primitive. If output is saved to a file to avoid truncation, read the full file.
4. Apply relevant native features and the guide's browser fallbacks while preserving framework constraints, accessibility, requested scope and existing behavior. Baseline Widely Available features generally need no fallback; for newer features honor the guide's actual compatibility advice unless the project has an explicit browser policy.
5. Verify with focused tests and runtime/browser/keyboard/accessibility evidence when relevant and available. Credit guide IDs actually used and distinguish tested behavior from advice.

If the CLI is offline, unavailable or unauthorized, use existing authoritative platform references if available and **state that current Modern Web Guidance was not retrieved**.

## Optional broad modernization

Only for an open-ended, user-requested codebase modernization consider `legacy-scan <path> --json`, with the same execution authorization. Review each match manually: intentional fallbacks and shims may be false positives. Do not perform an entire-codebase scan for a narrow fix.

Upstream: https://github.com/GoogleChrome/modern-web-guidance (Apache-2.0). This is original Agentit adapter text, not a copy of the upstream skill or CLI.
