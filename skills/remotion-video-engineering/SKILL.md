---
name: remotion-video-engineering
description: Engineer and verify a selected Remotion project when the task already requires Remotion/React frame rendering. Use for composition structure, deterministic frame timing, assets, fonts, editable props, preview probes, and final encoding. Do not use to choose a video concept, write ad strategy, review UI motion, or install Remotion.
license: Apache-2.0
---

# Remotion Video Engineering

This is a technical adapter for an existing or explicitly selected Remotion
project. It makes the render deterministic and editable; `motion-graphics-
production` owns the authored sequence and delivery intent.

## Trigger and boundary

Use when the requested implementation or repair is inside a Remotion project,
or a selected project has confirmed Remotion as its renderer. Do not invoke it
because a task merely mentions a video, animation, captions, React, or a brand
promo. Loading this adapter does not initiate package installation, project
scaffolding or browser acquisition. Setup is a separate planned action within
the user's authorized task scope; preserve any authority already established.

Before changing source, identify the project entry point, registered
compositions, package-manager lockfile, actual installed Remotion version, and
the package declarations/types available to that version. Read the matching
official [Remotion documentation](https://www.remotion.dev/docs/) for APIs used.
Do not infer API names, props, component
availability, or command flags from an older skill, online snippet, or a newer
release. If the package is absent or its local contract cannot be inspected,
record the limitation and stop short of API-specific edits until authorized
setup establishes a verifiable project contract.

## Model the composition

Give every composition an explicit width, height, fps, duration, default input
props, and stable identifier. Derive the duration from the planned scenes and
the selected fps, not from unexplained literals. A composition must have a
meaningful first and last frame; a trailing empty interval is a defect unless it
is intentional and documented.

Represent the sequence as named scene data or a small timeline module. Each
scene has a duration in frames and is rendered at its offset in the master.
Identify which clock a component receives: a frame hook inside a timed sequence
may already return its local frame. Subtract the scene offset only from an
explicit master clock; never subtract it twice. Verify local zero at each cut.
Keep scene timing, copy, asset paths, palette/font choices, and supported
variants in editable props/data rather than duplicating components for routine
content changes. Validate external props at the composition boundary and retain
safe, visible error handling for missing assets or invalid values.

Use the renderer's frame clock and interpolation/spring primitives for all
rendered movement. Derive time from the composition fps and current frame;
avoid browser-driven CSS animation, wall-clock timers, uncontrolled randomness,
network fetches during render, or side effects that make a frame depend on its
render order. Clamp ranges and give entering/exiting elements defined states
outside their active windows.

## Assets, text, and layouts

Resolve image, video, audio, font, and caption assets through the project's
approved asset path and the installed Remotion APIs. Inspect an asset's actual
duration/dimensions before using it to determine a scene or crop. Preload or
premount only where profiling or observed loading behavior justifies it; do not
make it a ritual. Use a real bundled/loaded font and wait for its supported load
mechanism before judging text layout. Async asset readiness must be awaited
through the installed renderer's supported mechanism; waiting for readiness
is distinct from optional performance preloading.

Keep layout proportional to video dimensions or named safe/content rectangles.
Avoid assuming a fixed 1080-by-1920 coordinate system. When supporting a second
ratio, share the semantic scene data while allowing distinct layout rules and
breakpoints; test both rather than scaling or letterboxing by default.

Treat supplied captions as timed editorial data, not decoration. Convert seconds
to frames against the composition fps, preserve approved wording, verify line
breaks and safe area at actual output size, and keep the visual sequence
understandable if audio is muted. Align audio cues to named beats, apply only
authorised source media, and verify the final encode rather than assuming a
timeline offset is audible.

Read [delivery-checks.md](references/delivery-checks.md) before a final render,
when adding scenes/variants, or when a render differs from the preview.

## Preview, render, and evidence

Use the project's existing scripts and package manager. First run the smallest
static/type check that covers changed code. Render a bounded preview or stills
at scene starts, settles, cuts, caption boundaries, and the final frame. Inspect
the frames for missing assets/fonts, overflow, incorrect offsets, premature or
late elements, invalid crops, and discontinuities.

After targeted fixes, run the requested final render. Then decode the resulting
file or extract representative frames from that exact output. Record the
composition id, input props, renderer version, output settings, reviewed frame
numbers/timestamps, and any check that could not run. A successful build or
Studio preview alone is not proof that the encoded file is usable.

## Failure handling

Classify a failure before retrying: version/API mismatch, missing dependency or
browser, source asset issue, font/layout issue, render resource exhaustion, or
encode/output error. Preserve the failing command and concise diagnostic. Do not
silently substitute a different renderer, package version, browser binary,
asset, codec, or cloud/paid service. Any such change is a separate decision.

## Completion criteria

The result has a deterministic frame model, scene offsets that match the
declared plan, editable composition inputs, verified assets/fonts and layouts
for every requested ratio, representative preview evidence, and final-output
decode/frame evidence. State unverified platform, audio, caption, or delivery
conditions explicitly.
