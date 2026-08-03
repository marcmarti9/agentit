---
name: anti-ai-slop-writing
description: Purge 20+ patterns of AI slop, robotic transitions, fake enthusiasm, and filler content from technical documentation, READMEs, PRs, and articles. Use when writing or editing human-grade text.
---

# Anti-AI-Slop Writing

## Core Directive

Eliminate AI writing clichés, robotic structure, and empty filler. Write clear, concise, direct human prose.

## The 20 Anti-Patterns to Purge

| Category | AI Slop Pattern | Preferred Human Alternative |
|---|---|---|
| **Forbidden Words** | "delve", "tapestry", "testament", "beacon", "game-changer", "seamless", "spearhead", "realm" | Delete or use plain language ("explore", "shows", "smooth", "lead") |
| **Fake Enthusiasm** | "Thrilled to announce", "Excited to share", "Revolutionary" | State the feature/change directly without self-congratulation |
| **Robotic Openings** | "In today's fast-paced digital landscape...", "In the ever-evolving world of..." | Start directly with the topic or problem |
| **Robotic Closings** | "In conclusion...", "Ultimately, only time will tell...", "Summary: In short..." | End after the last real point. No generic summaries. |
| **Empty Fillers** | "It is important to note that...", "Furthermore, it should be mentioned..." | Delete filler phrases; state the fact directly |
| **Decorative Emoji Spam** | Sprinkling decorative emojis across technical docs, PRs, commit messages, and code comments | No decorative emojis by default. Preserve emojis when part of UI states, user content, brand identity, or explicit request. |
| **Superlative Inflation**| Calling every minor update "robust", "cutting-edge", or "groundbreaking" | Describe exact specifications and empirical performance data |

## Checklist for Technical Documentation & READMEs

- [ ] Does the first sentence state what the software does without fluff?
- [ ] Are all forbidden AI buzzwords and decorative emojis removed?
- [ ] Is active voice used throughout?
- [ ] Are code examples copy-paste runnable without missing imports?
- [ ] Is the conclusion concise and free of generic wrap-up summaries?
