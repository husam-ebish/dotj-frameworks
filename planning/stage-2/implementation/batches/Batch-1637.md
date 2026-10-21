# Batch-1637 report

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; framework remains IN PROGRESS) |
| Framework | `dotj-core` |
| Plan task | `DJ-001-WP-05-T1` |
| Outcome | Implement selected NumberStyles.Any parsing |
| Validation | Seventeen pinned .NET 10 vectors matched packaged string, Char span, and UTF-8 span parsing; 20/20 foundation gate pass |
| Limitation | Arbitrary composed flags and broader culture behavior remain open |
| Public API qualification | OPEN; no fully qualified public .j facade. |

## Progress

| Metric | Actual value |
|---|---:|
| Completed implementation tasks | **0 / 1,092 (0.00%)** |
| Remaining implementation tasks | **1,092 (100.00%)** |
| Frameworks fully implemented and qualified | **0 / 66 (0.00%)** |
| In-progress / not-started frameworks | **1 / 65** |
| Batches completed, total | **1,637** |
| Batches planned, total | **Unknown**; no project-wide batch baseline |
| Batches remaining, total | **Unknown**; acceptance items are not batches |
| Outstanding acceptance items | **1,686**: 330 gates + 264 naming tasks + 1,092 implementation tasks, less accepted items |
| Next proposed batch | `Batch-1638`: Map selected NumberStyles flags combinations |
| Progress measure | Equal-weight WP and SDK integration task completions; prerequisite gates excluded; partials receive zero credit. |

## Files changed

| Path | Purpose |
|---|---|
| `dotj-core/dotj-core-public/src/main/java/System/Int32.java` | Selected Any parsing, oracle, packaged checks, and regenerated evidence |
| `dotj-core/dotj-core-public/src/test/java/consumer/ProductInt32SpanConsumer.java` | Selected Any parsing, oracle, packaged checks, and regenerated evidence |
| `planning/stage-2/repos/dotj-core/WP05-T1-BIT-HELPERS-v1.md` | Selected Any parsing, oracle, packaged checks, and regenerated evidence |
| `planning/stage-2/repos/dotj-core/evidence/foundation-e01-review-packet-v1.json` | Selected Any parsing, oracle, packaged checks, and regenerated evidence |
| `planning/stage-2/repos/dotj-core/evidence/foundation-file-notice-map-v1.json` | Selected Any parsing, oracle, packaged checks, and regenerated evidence |
| `planning/stage-2/repos/dotj-core/evidence/foundation-notice-review-queue-v1.json` | Selected Any parsing, oracle, packaged checks, and regenerated evidence |
| `planning/stage-2/repos/dotj-core/evidence/foundation-product-candidate-v1.json` | Selected Any parsing, oracle, packaged checks, and regenerated evidence |
| `planning/stage-2/repos/dotj-core/evidence/foundation-public-candidate-gate-v1.json` | Selected Any parsing, oracle, packaged checks, and regenerated evidence |
| `planning/stage-2/repos/dotj-core/evidence/foundation-public-candidate-ledger-v1.json` | Selected Any parsing, oracle, packaged checks, and regenerated evidence |
| `planning/stage-2/repos/dotj-core/evidence/foundation-rights-inputs-v1.json` | Selected Any parsing, oracle, packaged checks, and regenerated evidence |
| `planning/stage-2/repos/dotj-core/evidence/foundation-selected-metadata-v10.0.12.json` | Selected Any parsing, oracle, packaged checks, and regenerated evidence |
| `planning/stage-2/repos/dotj-core/evidence/foundation-semantic-surface-v1.json` | Selected Any parsing, oracle, packaged checks, and regenerated evidence |
| `planning/stage-2/repos/dotj-core/evidence/foundation-source-provenance-v1.json` | Selected Any parsing, oracle, packaged checks, and regenerated evidence |
| `planning/stage-2/repos/dotj-core/evidence/foundation-upstream-text-comparison-v1.json` | Selected Any parsing, oracle, packaged checks, and regenerated evidence |
| `planning/stage-2/repos/dotj-core/evidence/int32-declared-signature-audit-v1.json` | Selected Any parsing, oracle, packaged checks, and regenerated evidence |
| `planning/stage-2/repos/dotj-core/evidence/int32-erasure-contract-v1.json` | Selected Any parsing, oracle, packaged checks, and regenerated evidence |
| `planning/stage-2/repos/dotj-core/evidence/span-factory-types-v1.json` | Selected Any parsing, oracle, packaged checks, and regenerated evidence |
| `planning/stage-2/repos/dotj-core/evidence/system-type-identity-candidate-v1.json` | Selected Any parsing, oracle, packaged checks, and regenerated evidence |
| `planning/stage-2/repos/dotj-core/evidence/throw-selected-lowering-v1.json` | Selected Any parsing, oracle, packaged checks, and regenerated evidence |
| `planning/stage-2/repos/dotj-core/evidence/throw-site-upstream-adjacency-v1.json` | Selected Any parsing, oracle, packaged checks, and regenerated evidence |
| `tools/oracle/dotj-core/build-foundation-product-candidate.py` | Selected Any parsing, oracle, packaged checks, and regenerated evidence |
| `tools/oracle/dotj-core/foundation-public-metadata/Program.cs` | Selected Any parsing, oracle, packaged checks, and regenerated evidence |
| `planning/stage-2/IMPLEMENTATION-STATE.md` and `IMPLEMENTATION-PROGRESS.json` | Continuity and counts. |
| `planning/stage-2/implementation/batches/Batch-1637.md` | This report. |

**This batch is complete. The current request authorizes the next batch.**
