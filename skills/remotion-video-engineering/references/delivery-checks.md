# Remotion delivery checks

Read this reference before final rendering, after changing scene durations or
aspect ratios, and whenever output disagrees with a Studio/preview result.

## Version and API gate

Record the exact package and lockfile version present in the project. Inspect
the local declarations/source exposed by that version and consult the matching
official Remotion documentation before introducing an API. The API surface
changes between releases; do not port component names or properties from a
different package/version by resemblance. This reference intentionally contains
no copied official skill prose or code.

## Timeline checks

For every scene, verify that its start, local zero, first visible frame, hold,
exit, and master offset agree. Check at least the frame immediately before and
after each cut. Inspect frame zero and the final frame separately. Where a
caption/audio cue uses seconds, calculate against the declared composition fps
and record the resulting frame range; then verify it in the actual render.

## Asset and layout checks

Confirm that every referenced asset resolves in the render environment and that
fonts load before the frame is evaluated. Check readable type, aspect-preserving
crops, caption placement, logo clear-space, and focal content at each requested
dimension. A responsive React layout is not evidence that a rendered video
variant has the right safe area.

## Final-output evidence

Keep the exact final-render command/output metadata where the project exposes
it. Decode the final media or extract frames from the final file at a beginning,
one or more scene boundaries, a caption/label-sensitive point, and its ending.
Log command success separately from visual inspection. If hardware/browser/codec
support prevents a final render, retain the static/preview evidence and name
the blocked final-encode check rather than claiming delivery.
