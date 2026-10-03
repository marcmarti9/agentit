# Mobile performance evidence

Read only for a measured or reproducible startup, frame, list, bundle or memory
problem. Original Agentit synthesis informed by Callstack's MIT procedures at
`61e6e7dfdf3a8ee862254c200d751fcb1fb863dc`. Do not read the whole optimization
catalog for an ordinary screen change.

## Define a comparable measurement

Record device model/OS, app commit, release or debug build, engine, data size,
network/cache state, exact interaction, measurement tool and repetitions. Choose
a user-relevant metric before optimizing: time to usable content, frame duration
distribution, long JS tasks, scroll blanks, retained memory after a repeated
flow, or delivered bundle bytes. There is no universal device-independent target.

Keep cold, warm, resumed, background and iOS prewarmed launches separate. Mark
the endpoint when the target action is usable, not when a root component mounts.
Use multiple equivalent runs and report distribution/variation; do not compare
one noisy debug run to a release build. Simulator results do not establish
low-end physical-device performance.

## Localize before changing structure

| Symptom | Evidence to inspect | Candidate fix after localization |
| --- | --- | --- |
| JS stalls while native animation stays smooth | JS task and React commit timeline | Reduce synchronous work/subscription breadth |
| Scroll blanks or list jank | Render window, row cost and realistic dataset | Existing virtualized list, stable identity, lighter rows |
| Slow usable startup | Native init, bundle evaluation, hydration/request markers | Defer actual noncritical work or remove measured startup cost |
| Memory rises after repeated close/reopen | Heap/native allocation snapshots and retained references | Dispose listener/resource and verify retention falls |
| Large delivered app | JS/native/assets breakdown from same build | Remove unused dependencies/assets or supported shrinking |

A fixed native settings list is not a recycled long feed. Check the installed
list library version before prescribing sizing props. Do not add FlashList,
React Compiler, Jotai, Zustand, memoization or a new bundler without evidence
that the present boundary is the cause and migration earns its cost.

Use existing React Native DevTools, native platform profiler or a verified
device tool. If a release profiler requires an extra integration, record that
limitation; do not silently install or send traces to a service. Avoid putting
user records, tokens or private payloads into traces.

## Close the loop

Rerun the same scenario after the smallest justified change. Keep equivalent
content, build mode, device and cache/network conditions. Verify interaction and
accessibility behavior as well as speed. Restore an experiment that fails its
target or breaks behavior. Store the useful baseline/result artifact in the
project's existing evidence location and report remaining unmeasured platforms.

Sources:
[Callstack main procedure](https://github.com/callstackincubator/agent-skills/blob/61e6e7dfdf3a8ee862254c200d751fcb1fb863dc/skills/react-native-best-practices/SKILL.md),
[profiling](https://github.com/callstackincubator/agent-skills/blob/61e6e7dfdf3a8ee862254c200d751fcb1fb863dc/skills/react-native-best-practices/references/js-profile-react.md),
[startup measurement](https://github.com/callstackincubator/agent-skills/blob/61e6e7dfdf3a8ee862254c200d751fcb1fb863dc/skills/react-native-best-practices/references/native-measure-tti.md).
Upstream scripts, remote chunks, telemetry, device integrations and library
installation commands are not included or implicitly authorized.
