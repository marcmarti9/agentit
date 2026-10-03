# Production planning and verification

Read this reference when the task needs a beat sheet, timed captions or audio,
an aspect-ratio variant, or a delivery verification plan.

## Beat-sheet record

Use a table with one row per scene. Include scene id, local start/end or
duration, viewer takeaway, visible source asset, spoken/on-screen text,
entry/settle/exit, and an inspection frame or timestamp. Mark source material
as supplied, licensed, approved, or pending rather than assuming a reference is
reusable.

For a sequence placed in a master timeline, keep the scene's own animation at
local zero. The master owns ordering and offsets; the scene owns its internal
poses. This makes a new duration or scene reorder a focused change.

## Time conversion and media plan

Choose one frame rate for a composition. Convert deliberately:

```text
frames = seconds × fps
seconds = frames ÷ fps
```

Use rounded, named frame values only where the selected renderer requires
integer frames. Keep the transcript, cue time, visual beat, and caption range
as distinct data: a caption may start before a visual lands, and an audio cue
may require a fade rather than an abrupt trim. Verify timing against the real
media and renderer; a planned calculation is not sync evidence.

If captions are required, preserve the original approved text, speaker changes
where relevant, and enough contrast/background treatment to read them over the
actual frame. If narration or music rights are pending, prepare the sequence
with an explicit silent/placeholder state rather than implying clear rights.

## Variant review

For every requested ratio, test the intended focal point and reading order.
Reflow type and supporting visual groups from semantic anchors such as the
content-safe rectangle, logo clear-space, product bounds, or a caption band.
Check crop, wrapping, edge clearance, overlap, and the final frame independently
per ratio. A second exported size is not a verified variant merely because it
uses the same timeline.

## Evidence record

Keep a short record containing:

- renderer/project version and composition identifier where applicable;
- preview/contact-sheet coverage of all scenes;
- stills/timestamps at transitions and legibility-sensitive moments;
- final output path, codec/container details if available, and a successful
  decode or representative frame extraction from that final file;
- unresolved conditions such as unlicensed audio, absent device/platform test,
  unverified captions, or unavailable colour-managed display.

Do not turn a contact sheet into a claim that every frame is flawless. It is a
coverage aid; investigate suspicious intervals with targeted stills or playback.
