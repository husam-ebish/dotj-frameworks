# Batch-1209 report

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; framework remains IN PROGRESS) |
| Framework | `dotj-core` |
| Plan task | `DJ-001-N01-T2` |
| Outcome | Verified the Java visibility boundary for a representative erased Task.FromException overload pair. |
| Validation | javac rejected unchanged exact-name overloads and external access to a package-private backend; a public backend compiled but appeared in javap public output. |
| Limitation | The 26 mapped backend names remain syntax candidates, not qualified exact public APIs; compiler and visibility design is required. |
| Public API qualification | OPEN; no fully qualified public .j facade. |

## Progress

| Metric | Actual value |
|---|---:|
| Completed implementation tasks | **0 / 1,092 (0.00%)** |
| Remaining implementation tasks | **1,092 (100.00%)** |
| Frameworks fully implemented and qualified | **0 / 66 (0.00%)** |
| In-progress / not-started frameworks | **1 / 65** |
| Batches completed, total | **1,209** |
| Batches planned, total | **Unknown**; no project-wide batch baseline |
| Batches remaining, total | **Unknown**; acceptance items are not batches |
| Outstanding acceptance items | **1,686**: 330 gates + 264 naming tasks + 1,092 implementation tasks, less accepted items |
| Next proposed batch | `Batch-1210`: Classify all 426 pinned methods by public mapping disposition, including the 26 collective erasure blockers. |
| Progress measure | Equal-weight WP and SDK integration task completions; prerequisite gates excluded; partials receive zero credit. |

## Files changed

| Path | Purpose |
|---|---|
| `tools/oracle/dotj-core/audit-erasure-public-visibility.py` | Erasure backend public-visibility feasibility record. |
| `planning/stage-2/repos/dotj-core/evidence/n01-erasure-public-visibility-v10.0.12.json` | Erasure backend public-visibility feasibility record. |
| `planning/stage-2/IMPLEMENTATION-STATE.md` and `IMPLEMENTATION-PROGRESS.json` | Continuity and counts. |
| `planning/stage-2/implementation/batches/Batch-1209.md` | This report. |

**This batch is complete. The current request authorizes the next batch.**

## Verification

| Check | Result |
|---|---|
| Exact-name pair | `javac --release 21` rejected the two `Task.FromException(Exception)` declarations together. |
| Hidden backend | An external package could not call the package-private mapped method. |
| Public backend | The external consumer compiled, and `javap -public` exposed the mapped method name. |
| Batch plan | PASS: 1,209 sequential batches; 1,686 acceptance items open. |

The mapping is an internal feasibility candidate. It does not yet satisfy the exact public API policy.
