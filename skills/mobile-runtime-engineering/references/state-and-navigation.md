# State, navigation and offline behavior

Read for cold-start hydration, deep links, API/cache state or a mutation that must
survive failure. This is original Agentit guidance informed by Expo's MIT skills
at `13ad8e05874195633b5c185f6947bb6400e228fc`; source details are in the adaptation
ledger. API names must still be checked against the actual installed SDK.

## Resolve hydration before choosing a destination

Write down which persisted values govern the initial route: authentication,
onboarding, selected workspace, pending action. Until these are loaded, preserve
the app's loading/splash state. A default false value is not a loaded onboarding
decision. Retain a pending deep link until prerequisites resolve, then validate
the destination and the user's access. A navigation guard does not replace
server authorization.

Check a cold launch with and without credentials, a deep link before hydration,
an expired session, switching accounts and process recreation. Verify Android
back and iOS interactive dismiss where the flow uses them. Do not assume browser
history or route-loader APIs have equivalent native behavior.

## Model data states explicitly

| Evidence | UI contract |
| --- | --- |
| Prerequisite missing | Explain the prerequisite; do not fetch a wrong account |
| No data and first request pending | Initial loading or skeleton with stable layout |
| No data and network paused | Offline/pending state with meaningful recovery |
| Successful response with zero rows | Empty state with create/filter recovery |
| Valid cached data and refresh pending | Content plus unobtrusive activity |
| Valid cached data and refresh failed | Content plus stale/retry indication |
| No data and request failed | Error with retry; preserve form/search state |

Connectivity is evidence about a connection, not proof that the server is
reachable. Feed the request's abort signal into the fetch where supported;
unmount or cache invalidation alone does not guarantee network cancellation.
Ignore results from obsolete identity/query generations. Remove listeners on
disposal and clear account-scoped caches on account changes.

## Make writes safe to retry

Disable repeat submit while the request is in flight and keep the draft on
failure. For optimistic edits, capture the prior value and define rollback or a
visible unsynced state. Request cancellation is not server rollback: if a write
may have succeeded before a timeout, resolve its status using the product's
idempotency/reconciliation contract before sending another one.

Retry only recoverable operations, within a bounded backoff policy. Do not retry
authentication/validation failures as if they were transient. Persist an offline
queue only when required: define identity scope, ordering, deduplication, expiry,
conflict resolution and an inspectable failed state. A persisted GET cache is
not an offline write-sync engine.

Verify failed save followed by retry, double tap, response after navigation,
background/resume, account switch and a timeout after server success. For a
queue, also verify replay after process death and conflict handling.

## Protect configuration and client data

Client bundles and public build variables are readable. Keep privileged keys
and credentials at the server. Use the supported secure token store and check
its platform-specific persistence/deletion behavior; clear it deliberately on
logout. Do not add upstream feedback/analytics commands to the product.

## Source choices and exclusions

- [Expo data-fetching source](https://github.com/expo/skills/blob/13ad8e05874195633b5c185f6947bb6400e228fc/plugins/expo/skills/expo-data-fetching/SKILL.md)
  motivated the independent hydration, content, offline and mutation states.
- [Expo Router source](https://github.com/expo/skills/blob/13ad8e05874195633b5c185f6947bb6400e228fc/plugins/expo/skills/expo-router/SKILL.md)
  motivated version/platform-aware native navigation.
- The cancellation, retry and idempotency cautions are Agentit corrections to
  overly broad examples, not a claim that all upstream networking recipes are
  safe. No upstream API snippets, scripts or submission workflows are copied.
