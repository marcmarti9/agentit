# Definition of Done

A standing, project-wide bar that work must clear before it is actually declared done. Unlike acceptance criteria, which vary per task and answer "did we build the right thing?", the Definition of Done answers "is this finished to our standard?". Use it as the final completion gate in `planning-and-task-breakdown`, `incremental-implementation`, and `shipping-and-launch`.

Do **not** interpret this checklist as an instruction to rerun every repository-wide gate after every edit or thin implementation slice. During BUILD, use phase-appropriate targeted checks; apply the full Definition of Done when the feature/milestone is genuinely being closed, or earlier when the affected risk boundary requires it. See `anti-overengineering` for verification cadence.

## Definition of Done vs. Acceptance Criteria

| | Acceptance Criteria | Definition of Done |
|---|---|---|
| Scope | Specific to one task or spec | Applies at the real completion gate |
| Changes | Different for each item | Fixed and reused |
| Answers | "Did we build *this thing*?" | "Is it *ready*?" |
| Owner | Defined when planning the task | Defined once for the project |
| Example | "User can reset password via email link" | "Tests pass, no regressions, docs updated" |

The two are complementary. A task is done only when **its** acceptance criteria are met **and** the standing Definition of Done is satisfied. Skipping either leaves work that looks finished but is not.

## The Standing Checklist

Apply this to every change before declaring it done.

### Correctness
- [ ] All acceptance criteria for the task are met
- [ ] Code runs and behaves as intended, verified at runtime, not just compiled or typechecked
- [ ] New behavior is covered by tests that fail without the change and pass with it
- [ ] Existing tests still pass; no regressions introduced
- [ ] Edge cases and error paths are handled, not just the happy path

### Quality
- [ ] Code reveals intent through naming and structure; no comments needed to explain *what* it does
- [ ] No duplicated business logic
- [ ] No dead code, debug output, or commented-out blocks left behind
- [ ] Changes are scoped to the task; no unrelated refactors snuck in
- [ ] Linting and formatting pass

The depth behind these items lives in `code-review-and-quality` (the five-axis review) and `code-simplification` (reducing complexity without changing behavior).

### Integration
- [ ] Change works with the rest of the system, not just in isolation
- [ ] Database migrations, config changes, and feature flags are accounted for
- [ ] Backward compatibility considered for any public interface or API change

### Documentation
- [ ] Public interfaces, APIs, and user-facing behavior are documented
- [ ] Architectural decisions worth preserving are recorded (see `documentation-and-adrs`)
- [ ] Documentation describes the current state in timeless language, not the change history

### Ship-readiness
- [ ] Security implications reviewed for any untrusted input, auth, or data handling (see `security-and-hardening`)
- [ ] Observability in place for new critical paths (logs, metrics, traces) (see `observability-and-instrumentation`)
- [ ] Rollback path exists for anything risky (see `shipping-and-launch`)
- [ ] The human has reviewed and approved before merge or deploy

## How to Apply

- **During BUILD**: do not run this whole checklist after every edit. Use the cheapest targeted evidence that keeps the touched path sane.
- **Feature checkpoint**: verify the feature's acceptance criteria and directly related regressions, then continue.
- **Milestone / PR completion**: apply the full Correctness, Quality, Integration and Documentation bar once before claiming the work is done.
- **Per release**: the full checklist is the floor; `shipping-and-launch` adds the deploy-specific gates on top.

Tailor the list to the project once, then reuse it unchanged. A Definition of Done that is renegotiated every sprint is not a Definition of Done.

## Red Flags

- "It's done, I just haven't run it yet": unverified work is not done.
- "Tests pass" used as a synonym for done while docs, regressions, or runtime verification are skipped.
- A different bar applied depending on deadline pressure.
- Acceptance criteria treated as the whole bar, with no standing quality floor.
- "Done" declared before human review on changes that need it.
