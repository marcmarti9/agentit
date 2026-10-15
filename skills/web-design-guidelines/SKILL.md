---
name: web-design-guidelines
description: Audit web UI against the latest Vercel Web Interface Guidelines, with concrete file-and-line findings. Use for frontend accessibility, usability and interface review.
metadata:
  upstream: https://github.com/vercel-labs/agent-skills/tree/main/skills/web-design-guidelines
  upstream_skill_version: "1.0.0"
  authority: agentit-adapter
---

# Web Design Guidelines

Use the **live** Vercel Web Interface Guidelines; avoid stale copies. This Agentit-authored adapter references the official `web-design-guidelines` skill and does not vendor its text.

1. Confirm the interface or files to review. For site-wide audits, choose the affected UI files and critical user flows.
2. Read the latest rules at `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` before reviewing. If offline, disclose that freshness could not be verified.
3. Inspect actual code and, when relevant, rendered behavior: accessibility, keyboard/focus, states, responsive layout, forms, semantic structure, typography, copy and hierarchy. Verify material findings when a browser is available.
4. Report actionable results as `path:line — issue — minimal fix`, ordered by severity. Distinguish defects from suggestions and untested concerns; include passing observations when useful.
5. If remediation was requested, fix the specific issues and retest rather than rewriting the UI wholesale.

The project's brand, existing design system and explicit requirements outrank generic style preferences. Pair with `playwright-cli` for browser evidence or `design-md-workflow` only when a durable design contract is needed. This skill is selected just-in-time, never injected into every task.

Official skill: https://github.com/vercel-labs/agent-skills/blob/main/skills/web-design-guidelines/SKILL.md
Official guidelines: https://vercel.com/design/guidelines
