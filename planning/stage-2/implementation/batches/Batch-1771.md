# Batch-1771 report

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; framework remains IN PROGRESS) |
| Framework | `dotj-core` |
| Plan task | `DJ-001-WP-05-T1` |
| Outcome | Implement selected Int32 round-trip explicit precision |
| Validation | Sixteen .NET 10 R/r precision vectors matched packaged Java; 20/20 foundation gate pass |
| Limitation | Broader round-trip format behavior remains open |
| Public API qualification | OPEN; no fully qualified public .j facade. |

## Progress

| Metric | Actual value |
|---|---:|
| Completed implementation tasks | **0 / 1,092 (0.00%)** |
| Remaining implementation tasks | **1,092 (100.00%)** |
| Frameworks fully implemented and qualified | **0 / 66 (0.00%)** |
| In-progress / not-started frameworks | **1 / 65** |
| Batches completed, total | **1,771** |
| Batches planned, total | **Unknown**; no project-wide batch baseline |
| Batches remaining, total | **Unknown**; acceptance items are not batches |
| Outstanding acceptance items | **1,686**: 330 gates + 264 naming tasks + 1,092 implementation tasks, less accepted items |
| Next proposed batch | `Batch-1772`: Pin Int32 G and R format alias behavior at extrema |
| Progress measure | Equal-weight WP and SDK integration task completions; prerequisite gates excluded; partials receive zero credit. |

## Files changed

| Path | Purpose |
|---|---|
| `dotj-core/dotj-core-public/src/main/java/System/Int32.java` | Product implementation, oracle, packaged consumer and distribution evidence |
| `dotj-core/dotj-core-public/src/test/java/consumer/ProductInt32RoundtripFormatConsumer.java` | Product implementation, oracle, packaged consumer and distribution evidence |
| `planning/stage-2/repos/dotj-core/WP05-T1-BIT-HELPERS-v1.md` | Product implementation, oracle, packaged consumer and distribution evidence |
| `planning/stage-2/repos/dotj-core/evidence/foundation-e01-review-packet-v1.json` | Product implementation, oracle, packaged consumer and distribution evidence |
| `planning/stage-2/repos/dotj-core/evidence/foundation-file-notice-map-v1.json` | Product implementation, oracle, packaged consumer and distribution evidence |
| `planning/stage-2/repos/dotj-core/evidence/foundation-notice-review-queue-v1.json` | Product implementation, oracle, packaged consumer and distribution evidence |
| `planning/stage-2/repos/dotj-core/evidence/foundation-product-candidate-v1.json` | Product implementation, oracle, packaged consumer and distribution evidence |
| `planning/stage-2/repos/dotj-core/evidence/foundation-public-candidate-gate-v1.json` | Product implementation, oracle, packaged consumer and distribution evidence |
| `planning/stage-2/repos/dotj-core/evidence/foundation-public-candidate-ledger-v1.json` | Product implementation, oracle, packaged consumer and distribution evidence |
| `planning/stage-2/repos/dotj-core/evidence/foundation-rights-inputs-v1.json` | Product implementation, oracle, packaged consumer and distribution evidence |
| `planning/stage-2/repos/dotj-core/evidence/foundation-selected-metadata-v10.0.12.json` | Product implementation, oracle, packaged consumer and distribution evidence |
| `planning/stage-2/repos/dotj-core/evidence/foundation-semantic-surface-v1.json` | Product implementation, oracle, packaged consumer and distribution evidence |
| `planning/stage-2/repos/dotj-core/evidence/foundation-source-provenance-v1.json` | Product implementation, oracle, packaged consumer and distribution evidence |
| `planning/stage-2/repos/dotj-core/evidence/foundation-upstream-text-comparison-v1.json` | Product implementation, oracle, packaged consumer and distribution evidence |
| `planning/stage-2/repos/dotj-core/evidence/int32-declared-signature-audit-v1.json` | Product implementation, oracle, packaged consumer and distribution evidence |
| `planning/stage-2/repos/dotj-core/evidence/int32-erasure-contract-v1.json` | Product implementation, oracle, packaged consumer and distribution evidence |
| `planning/stage-2/repos/dotj-core/evidence/span-factory-types-v1.json` | Product implementation, oracle, packaged consumer and distribution evidence |
| `planning/stage-2/repos/dotj-core/evidence/system-type-identity-candidate-v1.json` | Product implementation, oracle, packaged consumer and distribution evidence |
| `planning/stage-2/repos/dotj-core/evidence/throw-selected-lowering-v1.json` | Product implementation, oracle, packaged consumer and distribution evidence |
| `planning/stage-2/repos/dotj-core/evidence/throw-site-upstream-adjacency-v1.json` | Product implementation, oracle, packaged consumer and distribution evidence |
| `tools/oracle/dotj-core/build-foundation-product-candidate.py` | Product implementation, oracle, packaged consumer and distribution evidence |
| `tools/oracle/dotj-core/foundation-public-metadata/Program.cs` | Product implementation, oracle, packaged consumer and distribution evidence |
| `planning/stage-2/IMPLEMENTATION-STATE.md` and `IMPLEMENTATION-PROGRESS.json` | Continuity and counts. |
| `planning/stage-2/implementation/batches/Batch-1771.md` | This report. |

**This batch is complete. The current request authorizes the next batch.**
