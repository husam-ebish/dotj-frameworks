# Batch-1267 report

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; framework remains IN PROGRESS) |
| Framework | `dotj-core` |
| Plan task | `DJ-001-WP-01-T1` |
| Outcome | Added selected Int32.TryParse behavior with success values and zero on failure. |
| Validation | Pinned .NET six TryParse observations, external Java consumer, public audit, JAR and distribution inventory passed. |
| Limitation | Java array output differs from CLR out int; full parsing grammar and overloads remain open. |
| Public API qualification | OPEN; no fully qualified public .j facade. |

## Progress

| Metric | Actual value |
|---|---:|
| Completed implementation tasks | **0 / 1,092 (0.00%)** |
| Remaining implementation tasks | **1,092 (100.00%)** |
| Frameworks fully implemented and qualified | **0 / 66 (0.00%)** |
| In-progress / not-started frameworks | **1 / 65** |
| Batches completed, total | **1,267** |
| Batches planned, total | **Unknown**; no project-wide batch baseline |
| Batches remaining, total | **Unknown**; acceptance items are not batches |
| Outstanding acceptance items | **1,686**: 330 gates + 264 naming tasks + 1,092 implementation tasks, less accepted items |
| Next proposed batch | `Batch-1268`: Probe and implement selected Int32 hexadecimal Parse with NumberStyles. |
| Progress measure | Equal-weight WP and SDK integration task completions; prerequisite gates excluded; partials receive zero credit. |

## Files changed

| Path | Purpose |
|---|---|
| `dotj-core/dotj-core-public/src/main/java/System/Int32.java` | Selected TryParse outcomes and refreshed foundation evidence. |
| `dotj-core/dotj-core-public/src/test/java/consumer/ProductTypeIdentityConsumer.java` | Selected TryParse outcomes and refreshed foundation evidence. |
| `tools/oracle/dotj-core/foundation-public-metadata/Program.cs` | Selected TryParse outcomes and refreshed foundation evidence. |
| `tools/oracle/dotj-core/build-system-type-candidate.py` | Selected TryParse outcomes and refreshed foundation evidence. |
| `tools/oracle/dotj-core/audit-foundation-public-candidate.py` | Selected TryParse outcomes and refreshed foundation evidence. |
| `planning/stage-2/repos/dotj-core/WP01-T1-CONTRACT-v1.md` | Selected TryParse outcomes and refreshed foundation evidence. |
| `planning/stage-2/repos/dotj-core/evidence/foundation-selected-metadata-v10.0.12.json` | Selected TryParse outcomes and refreshed foundation evidence. |
| `planning/stage-2/repos/dotj-core/evidence/system-type-identity-candidate-v1.json` | Selected TryParse outcomes and refreshed foundation evidence. |
| `planning/stage-2/repos/dotj-core/evidence/typeof-selected-lowering-v1.json` | Selected TryParse outcomes and refreshed foundation evidence. |
| `planning/stage-2/repos/dotj-core/evidence/foundation-product-candidate-v1.json` | Selected TryParse outcomes and refreshed foundation evidence. |
| `planning/stage-2/repos/dotj-core/evidence/foundation-public-candidate-ledger-v1.json` | Selected TryParse outcomes and refreshed foundation evidence. |
| `planning/stage-2/repos/dotj-core/evidence/foundation-file-notice-map-v1.json` | Selected TryParse outcomes and refreshed foundation evidence. |
| `planning/stage-2/IMPLEMENTATION-STATE.md` and `IMPLEMENTATION-PROGRESS.json` | Continuity and counts. |
| `planning/stage-2/implementation/batches/Batch-1267.md` | This report. |

**This batch is complete. The current request authorizes the next batch.**

## Verification

| Check | Result |
|---|---|
| Pinned .NET behavior | PASS: six TryParse success and zero-on-failure observations. |
| External Java consumer | PASS: selected values and one-element result array. |
| Candidate package | PASS: JAR, twenty-five-type public audit and source/class inventory. |
| Qualification | OPEN: CLR out parameter ABI and full parsing grammar. |
