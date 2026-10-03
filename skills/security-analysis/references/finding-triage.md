# Finding triage and scanner evidence

Use this reference when a static-analysis report or a suspected vulnerability needs a
defensible classification.

## Static-analysis quality

Before accepting either findings or a clean result, inspect the revision, languages,
build/extraction log where applicable, ruleset, configuration, excluded paths, and result
format. A successful command may have analysed only generated code, a subset of languages,
or no meaningful files. Record coverage limits in the conclusion.

## Controls are contextual

Parameterization can prevent a query injection but does not enforce tenant ownership.
HTML encoding can prevent a rendering sink issue but does not protect a command sink.
Authentication identifies a principal but does not establish that principal may act on the
specific object. Verify the control immediately relevant to the sink and authorization
decision, including error and alternate paths.

## Safe reproduction

Prefer a unit or integration fixture under local control. Use a benign marker value and
assert the forbidden behavior is blocked, rather than attempting an intrusive payload.
If reproduction depends on a production-only identity, secret, or endpoint, document the
precondition and preserve the finding's confidence as conditional until authorized evidence
is available.

## Provenance

This Agentit adaptation and this reference are licensed CC-BY-SA-4.0. They are a
substantial procedure adaptation informed by Trail of Bits' CodeQL analysis skill at
commit `82fe8226252622fa807643bdca1710901198553a`, inspected 2026-10-03:
<https://github.com/trailofbits/skills/blob/82fe8226252622fa807643bdca1710901198553a/plugins/static-analysis/skills/codeql/SKILL.md>,
and the Trail of Bits Testing Handbook at commit
`190294f0ed563baddf4941cd2388be5bd4d5c5ba`:
<https://github.com/trailofbits/testing-handbook/tree/190294f0ed563baddf4941cd2388be5bd4d5c5ba>.
The skills source root `LICENSE` is CC BY-SA 4.0 (SHA256
`7abe19ec9bb73b36141b999b861d24ad855e808bafe0f81e84cce28556f6c297`), retained at
`vendor/adaptation-licenses/trailofbits--skills/LICENSE`; the handbook `LICENSE` is CC BY 4.0
(SHA256 `97d24386ff776d7160b87031b259a942bd03c9939796cab6724ad5d17d2cf785`), retained
at `vendor/adaptation-licenses/trailofbits--testing-handbook/LICENSE`. Distributed copies must
credit Trail of Bits and the pinned sources, link the applicable licenses, indicate this
adaptation, and keep this adaptation available under CC-BY-SA-4.0. No upstream scripts,
assets, installers, or runtime contract are included.
