# Batch-1272 report

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; framework remains IN PROGRESS) |
| Framework | `dotj-core` |
| Plan task | `DJ-001-WP-01-T1` |
| Outcome | Added selected invariant Int32 N-format grouping and decimal precision. |
| Validation | Pinned .NET five number-format observations, external Java consumer, public audit, JAR and distribution inventory passed. |
| Limitation | Provider-driven separators and digits, other number formats and complete formatting remain open. |
| Public API qualification | OPEN; no fully qualified public .j facade. |

## Progress

| Metric | Actual value |
|---|---:|
| Completed implementation tasks | **0 / 1,092 (0.00%)** |
| Remaining implementation tasks | **1,092 (100.00%)** |
| Frameworks fully implemented and qualified | **0 / 66 (0.00%)** |
| In-progress / not-started frameworks | **1 / 65** |
| Batches completed, total | **1,272** |
| Batches planned, total | **Unknown**; no project-wide batch baseline |
| Batches remaining, total | **Unknown**; acceptance items are not batches |
| Outstanding acceptance items | **1,686**: 330 gates + 264 naming tasks + 1,092 implementation tasks, less accepted items |
| Next proposed batch | `Batch-1273`: Probe and implement selected Int32 currency formatting behavior. |
| Progress measure | Equal-weight WP and SDK integration task completions; prerequisite gates excluded; partials receive zero credit. |

## Files changed

| Path | Purpose |
|---|---|
| `dotj-core/dotj-core-public/src/main/java/System/Int32.java` | Selected invariant number formats and refreshed foundation evidence. |
| `dotj-core/dotj-core-public/src/test/java/consumer/ProductTypeIdentityConsumer.java` | Selected invariant number formats and refreshed foundation evidence. |
| `tools/oracle/dotj-core/foundation-public-metadata/Program.cs` | Selected invariant number formats and refreshed foundation evidence. |
| `tools/oracle/dotj-core/build-system-type-candidate.py` | Selected invariant number formats and refreshed foundation evidence. |
| `planning/stage-2/repos/dotj-core/WP01-T1-CONTRACT-v1.md` | Selected invariant number formats and refreshed foundation evidence. |
| `planning/stage-2/repos/dotj-core/evidence/foundation-selected-metadata-v10.0.12.json` | Selected invariant number formats and refreshed foundation evidence. |
| `planning/stage-2/repos/dotj-core/evidence/system-type-identity-candidate-v1.json` | Selected invariant number formats and refreshed foundation evidence. |
| `planning/stage-2/repos/dotj-core/evidence/typeof-selected-lowering-v1.json` | Selected invariant number formats and refreshed foundation evidence. |
| `planning/stage-2/repos/dotj-core/evidence/foundation-product-candidate-v1.json` | Selected invariant number formats and refreshed foundation evidence. |
| `planning/stage-2/repos/dotj-core/evidence/foundation-public-candidate-ledger-v1.json` | Selected invariant number formats and refreshed foundation evidence. |
| `planning/stage-2/repos/dotj-core/evidence/foundation-file-notice-map-v1.json` | Selected invariant number formats and refreshed foundation evidence. |
| `planning/stage-2/IMPLEMENTATION-STATE.md` and `IMPLEMENTATION-PROGRESS.json` | Continuity and counts. |
| `planning/stage-2/implementation/batches/Batch-1272.md` | This report. |

**This batch is complete. The current request authorizes the next batch.**

## Verification

| Check | Result |
|---|---|
| Pinned .NET behavior | PASS: five selected invariant N-format results. |
| External Java consumer | PASS: grouping, decimals, negative and default precision. |
| Candidate package | PASS: JAR, twenty-six-type public audit and source/class inventory. |
| Qualification | OPEN: provider-driven and broader number formatting. |
