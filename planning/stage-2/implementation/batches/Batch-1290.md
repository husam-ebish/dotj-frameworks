# Batch-1290 report

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; framework remains IN PROGRESS) |
| Framework | `dotj-core` |
| Plan task | `DJ-001-WP-01-T1` |
| Outcome | Pinned and regression checked selected scaled near-zero rounding. |
| Validation | Five .NET observations, external Java consumer, public audit and distribution inventory passed. |
| Limitation | Other rounding boundaries, custom patterns and provider localization remain open. |
| Public API qualification | OPEN; no fully qualified public .j facade. |

## Progress

| Metric | Actual value |
|---|---:|
| Completed implementation tasks | **0 / 1,092 (0.00%)** |
| Remaining implementation tasks | **1,092 (100.00%)** |
| Frameworks fully implemented and qualified | **0 / 66 (0.00%)** |
| In-progress / not-started frameworks | **1 / 65** |
| Batches completed, total | **1,290** |
| Batches planned, total | **Unknown**; no project-wide batch baseline |
| Batches remaining, total | **Unknown**; acceptance items are not batches |
| Outstanding acceptance items | **1,686**: 330 gates + 264 naming tasks + 1,092 implementation tasks, less accepted items |
| Next proposed batch | `Batch-1291`: Probe selected custom negative/zero section rounding after scaling. |
| Progress measure | Equal-weight WP and SDK integration task completions; prerequisite gates excluded; partials receive zero credit. |

## Files changed

| Path | Purpose |
|---|---|
| `dotj-core/dotj-core-public/src/test/java/consumer/ProductTypeIdentityConsumer.java` | Selected near-zero scaling evidence and consumer regression. |
| `tools/oracle/dotj-core/foundation-public-metadata/Program.cs` | Selected near-zero scaling evidence and consumer regression. |
| `tools/oracle/dotj-core/build-system-type-candidate.py` | Selected near-zero scaling evidence and consumer regression. |
| `planning/stage-2/repos/dotj-core/WP01-T1-CONTRACT-v1.md` | Selected near-zero scaling evidence and consumer regression. |
| `planning/stage-2/repos/dotj-core/evidence/foundation-selected-metadata-v10.0.12.json` | Selected near-zero scaling evidence and consumer regression. |
| `planning/stage-2/repos/dotj-core/evidence/system-type-identity-candidate-v1.json` | Selected near-zero scaling evidence and consumer regression. |
| `planning/stage-2/IMPLEMENTATION-STATE.md` and `IMPLEMENTATION-PROGRESS.json` | Continuity and counts. |
| `planning/stage-2/implementation/batches/Batch-1290.md` | This report. |

**This batch is complete. The current request authorizes the next batch.**

## Verification

| Check | Result |
|---|---|
| Pinned .NET behavior | PASS: five near-zero scaling outputs. |
| External Java consumer | PASS: negative zero suppression and signed half-step rounding. |
| Candidate package | PASS: 26 type public audit, JAR and distribution inventory. |
| Qualification | OPEN: broader custom rounding and provider behavior. |
