# Motion review coverage

Use this reference only when ordinary component-state review cannot establish
coverage.

## Scroll and continuous motion

Record the scroller, input modality, entry/exit points, and whether motion
blocks reading, target acquisition, or navigation. Test resize/content changes
and reduced motion where the implementation exposes those paths. A static
capture cannot prove scroll smoothness or lifecycle cleanup.

## Data and asynchronous state

Replay loading, success, empty, error, cancellation, stale response, and rapid
re-entry as applicable. Check that motion neither hides an error nor leaves
obsolete content or focus behind. If the state cannot be reproduced, mark the
coverage missing rather than auditing a substitute state.

## Native platforms

Use an emulator/device observation for platform transitions, system preference,
and interruption behavior. Source review can identify a candidate path but does
not prove device behavior.

## Performance claims

Use the platform profiler or a reproducible trace before calling a problem
measured. Record device/browser, route/state, interaction, and the observed
metric. Without that, describe only the source-located risk and proposed
retest; do not invent a frame-rate threshold.
