---
name: epstein-md
description: Strict anti-AI-slop design rules for UI. Ban box-shadows, emojis, LIVE badges, blue/purple gradients and common AI words. Use when building or reviewing interfaces to avoid vibe-coded slop.
metadata:
  trigger: Frontend UI, component design, landing pages, dashboards, any visual interface
  source: Inspired by shipper.now epstein.md (https://x.com/shipper_now/status/2110637576935891122)
---

# Epstein MD Design

Hard rules against the most common AI-generated UI patterns.

These are not suggestions. Violate them only with an explicit, written reason that serves the content.

## Absolute bans

- **No box-shadows.** Not soft, not hard, not colored. Use borders, background contrast, or nothing.
- **No emojis.** Anywhere in UI chrome, buttons, empty states, or labels.
- **No "LIVE" / "Online" / status badges** with green dots or pills.
- **No blue or purple gradients.** No gradient text, no gradient backgrounds, no gradient borders. Solid colors only.
- **No glassmorphism.** No backdrop-blur panels, no frosted overlays.
- **No large border-radius on everything.** Prefer sharp or small radius (0–4px) unless the product already has a clear system.

## Banned AI words (do not use in UI copy or code comments)

delve, vibe, seamless, elevate, unlock, supercharge, harness, leverage, streamline, robust, cutting-edge, next-gen, game-changing, innovative, empower, transform, revolutionize, skyrocket, unleash, master, ultimate, comprehensive, holistic, synergy, paradigm, ecosystem, journey, experience (as filler), solution, platform (when empty), AI-powered (as badge), smart, intelligent, powerful, effortless, frictionless, intuitive (as claim), modern, sleek, beautiful (as claim), clean (as claim).

Prefer concrete verbs and nouns: "Send", "Create invoice", "3 open tasks", "Last synced 2m ago".

## Layout and structure

- Prefer left-aligned over centered heroes.
- One primary action per view. Secondary actions as text links.
- Cards only when the item is a true independent unit. Not as a default wrapper.
- Avoid the classic three-column feature grid unless the content actually has three equal things.
- No fake metrics or decorative numbers.
- No gradient orbs, blobs, or abstract background shapes.

## Checklist before shipping UI

- [ ] Zero box-shadows?
- [ ] Zero emojis?
- [ ] Zero LIVE/status pills?
- [ ] Zero blue/purple gradients?
- [ ] Zero banned AI words in visible text?
- [ ] Primary action is obvious and singular?
- [ ] Layout decisions serve the content, not a template?

## When to load

Load this skill for any frontend work, landing pages, dashboards, or design reviews. Combine with `design-taste-frontend` and `stop-slop` when writing both UI and copy.

## License

Apache-2.0 (Agentit)
