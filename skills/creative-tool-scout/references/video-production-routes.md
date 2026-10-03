# Video and motion production routes

Read only when selecting a pipeline for a rendered motion/video deliverable
or a genuinely different alternative to the existing project stack. Separate
authoring, media generation, rendering and distribution: one tool need not do
all four. This is a comparison procedure, not runtime installation authority.

| Required capability | Candidate route | Tradeoff to test |
|---|---|---|
| Exact typography, UI, data and editable variants | Frame-driven Remotion composition in an appropriate React project | Installed APIs, asset/font readiness, frame determinism, renderer license and encode evidence |
| HTML/CSS/SVG composition with timeline choreography | Hyperframes or an existing deterministic HTML video renderer | Seekable paused timeline, installed API contract, capture/render parity and caption/media support |
| Existing designer-authored motion project / MOGRT | Authorized After Effects project and available native/MCP surface | Preserve editable project, inspect layers/assets, bounded undoable writes, project diff and actual previews |
| Product geometry, lighting and real camera shots | Existing licensed 3D asset and Blender/approved offline renderer | Asset fidelity, camera/lighting craft, render cost and compositing; a web Three.js scene is not automatically a film pipeline |
| Overlay, trim, mix, transcode or packaging | Existing NLE or FFmpeg tooling | Precision, subtitle/audio sync, color/codec/alpha compatibility and decoded final file |
| Interactive vector state | Existing Rive runtime | States/input/interruptions across target platforms; not a default film encoder |
| Portable vector animation | Lottie-compatible authoring/export | Supported feature subset and actual target renderer, fonts/assets and visual parity |
| Live-action atmosphere or synthetic performer | Approved generated/hybrid footage provider | Current quality/limits, identity/product stability, consent/upload authority and spend |

Choose against the actual brief: controllability, editable handoff, installed
capabilities, cost, reproducibility, export formats, team operation and rights.
Prefer the already suitable workflow when moving stacks adds little value.
Do not copy current provider prices, account status or feature promises into
permanent instructions; inspect current primary docs for the chosen branch.

For an existing AE project, inspect only relevant compositions/layers and use
stable identifiers. Establish the previous state, requested change and undo or
snapshot path, apply a bounded edit, then inspect the resulting project diff
and representative frames/playback. Tool success is not visual verification.
If the host lacks an authorized native app/bridge, report the unavailable
capability rather than claiming the file was opened or installing a bridge.

Compare previews and final rendering at the same representative times. A
browser animation that depends on wall-clock time, live input or random values
cannot simply be screen-captured as a reproducible frame-driven composition.
Test time seeking and media readiness before committing to a capture pipeline.

Primary technical sources: [Remotion skills](https://www.remotion.dev/docs/ai/skills),
[Remotion license](https://www.remotion.dev/docs/license),
[Hyperframes](https://github.com/heygen-com/hyperframes),
[Lottie specification](https://github.com/lottie/lottie-spec),
[Rive runtime](https://github.com/rive-app/rive-runtime).
AE operating procedure is informed by Engine-Room-Games/after-effects-mcp at
the immutable revision in the adaptation manifest; MIT notice is retained.
No upstream plugin, tool protocol, build script or auto-update flow is included.
