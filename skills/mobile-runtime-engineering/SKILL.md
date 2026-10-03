---
name: mobile-runtime-engineering
description: >-
  Implement and verify Expo/React Native runtime behavior: cold-start hydration,
  deep links/back navigation, offline data and failed mutations, native lifecycle,
  large lists, or measured startup/frame/memory regressions. Not for visual
  inspiration, web-only React work, or Flutter/Swift/Kotlin implementation.
license: Apache-2.0
---

# Mobile runtime engineering

Own the working behavior of an Expo/React Native flow. Visual research belongs to
the design procedure; a screenshot cannot establish navigation, persistence or
device performance. This is an Agentit-owned, source-informed adaptation of Expo
and Callstack procedures, not a verbatim upstream package or their tool runtime.

## Establish the actual application

Read the affected route/component, package versions, lockfile, native/build
configuration and existing state/data owner. Record target platforms, Expo SDK,
React Native, navigation library and build kind. Determine whether the app uses
Expo Go, a development client, managed/prebuilt native projects or bare RN.
An example from the latest SDK is not evidence that an older project supports it.

Use the project's established native controls and data library when they fit.
Do not introduce a state manager, change navigation or add a native module merely
because a source recommends one. New native dependencies require compatible
build configuration and their own scoped verification.

Identify available simulator/device/profiler capabilities before relying on
them. An Appllama account, EAS service or agent-device CLI is optional and must
actually exist; a skill does not grant service access or permission to upload.

## Name the observable failure

Write a short flow contract: starting state, user action, persisted result,
visible outcome and failure/retry outcome. For example, a failed edit must retain
the draft, and retry must create one server record. Include the real data scale,
platform and version when those affect behavior.

Select the relevant branch only:

- Hydration, network, offline or mutation work: read
  [state-and-navigation.md](references/state-and-navigation.md).
- Startup, jank, memory or large-list work: read
  [performance-evidence.md](references/performance-evidence.md).
- Pure screen composition: use the existing UI/design owner rather than loading
  these runtime recipes.

## Implement one complete behavior

Keep state at its existing authoritative owner. Separate no response yet,
resolved empty data, usable content, paused offline work and failure. Cached
content may coexist with a failed refresh. Do not replace an error with an empty
state or a fabricated successful save.

For lifecycle-sensitive work, cancel or invalidate stale results, dispose
subscriptions/timers and avoid writing a previous account's response into the
current account's cache. Persist only what the product actually promises.
Treat device storage as exposed to the device owner; tokens need the supported
secure-storage path, and privileged service keys never belong in the client.

Check keyboard/safe-area handling, back/dismiss behavior, large text, screen
reader labels and reduced-motion settings on the affected flow. Preserve the
platform's familiar controls and meaningful focus order.

## Verify at the relevant boundary

Use focused logic/component checks for states and race conditions, then drive
the affected navigation/save/retry flow on the target simulator or device when
available. Check launch from a cold process and deep link where the change
depends on persisted hydration. Development build observations cannot establish
release performance or app-store readiness.

For performance claims, reproduce and measure the same interaction before and
after on equivalent build/device/data conditions. If the result is inconclusive,
say so; a profiler screenshot or a component-count reduction is not a speedup.

## Completion criteria

The requested flow works with realistic content and failure states; version and
platform assumptions are checked; drafts and account boundaries survive retries;
the verification names build/device and exercised cases. Report untested device,
release, offline-sync or store gates separately. No EAS upload, telemetry or
source-feedback submission is implied by this procedure.
