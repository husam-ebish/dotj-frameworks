# Batch-1936 report

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; framework remains IN PROGRESS) |
| Framework | `dotj-core` |
| Plan task | `DJ-001-WP-05-T1` |
| Outcome | Expose Decimal scale getter |
| Validation | Packaged Decimal get_Scale passed bit-pattern and signed-zero consumer checks; missing public getters fell from 33 to 32; 20/20 foundation gate pass |
| Limitation | Broader Decimal property parity remains open |
| Public API qualification | OPEN; no fully qualified public .j facade. |

## Progress

| Metric | Actual value |
|---|---:|
| Completed implementation tasks | **0 / 1,092 (0.00%)** |
| Remaining implementation tasks | **1,092 (100.00%)** |
| Frameworks fully implemented and qualified | **0 / 66 (0.00%)** |
| In-progress / not-started frameworks | **1 / 65** |
| Batches completed, total | **1,936** |
| Batches planned, total | **Unknown**; no project-wide batch baseline |
| Batches remaining, total | **Unknown**; acceptance items are not batches |
| Outstanding acceptance items | **1,686**: 330 gates + 264 naming tasks + 1,092 implementation tasks, less accepted items |
| Next proposed batch | `Batch-1937`: Implement another missing Decimal public member |
| Progress measure | Equal-weight WP and SDK integration task completions; prerequisite gates excluded; partials receive zero credit. |

## Files changed

| Path | Purpose |
|---|---|
| `dotj-core/dotj-core-public/src/main/java/System/Decimal.java` | Reference oracle, packaged consumer and distribution evidence |
| `dotj-core/dotj-core-public/src/test/java/consumer/ProductDecimalBitsConsumer.java` | Reference oracle, packaged consumer and distribution evidence |
| `planning/stage-2/repos/dotj-core/WP05-T1-BIT-HELPERS-v1.md` | Reference oracle, packaged consumer and distribution evidence |
| `planning/stage-2/repos/dotj-core/evidence/foundation-e01-review-packet-v1.json` | Reference oracle, packaged consumer and distribution evidence |
| `planning/stage-2/repos/dotj-core/evidence/foundation-file-notice-map-v1.json` | Reference oracle, packaged consumer and distribution evidence |
| `planning/stage-2/repos/dotj-core/evidence/foundation-notice-review-queue-v1.json` | Reference oracle, packaged consumer and distribution evidence |
| `planning/stage-2/repos/dotj-core/evidence/foundation-product-candidate-v1.json` | Reference oracle, packaged consumer and distribution evidence |
| `planning/stage-2/repos/dotj-core/evidence/foundation-public-candidate-gate-v1.json` | Reference oracle, packaged consumer and distribution evidence |
| `planning/stage-2/repos/dotj-core/evidence/foundation-public-candidate-ledger-v1.json` | Reference oracle, packaged consumer and distribution evidence |
| `planning/stage-2/repos/dotj-core/evidence/foundation-rights-inputs-v1.json` | Reference oracle, packaged consumer and distribution evidence |
| `planning/stage-2/repos/dotj-core/evidence/foundation-semantic-surface-v1.json` | Reference oracle, packaged consumer and distribution evidence |
| `planning/stage-2/repos/dotj-core/evidence/foundation-source-provenance-v1.json` | Reference oracle, packaged consumer and distribution evidence |
| `planning/stage-2/repos/dotj-core/evidence/foundation-upstream-text-comparison-v1.json` | Reference oracle, packaged consumer and distribution evidence |
| `planning/stage-2/repos/dotj-core/evidence/int32-declared-signature-audit-v1.json` | Reference oracle, packaged consumer and distribution evidence |
| `planning/stage-2/repos/dotj-core/evidence/int32-erasure-contract-v1.json` | Reference oracle, packaged consumer and distribution evidence |
| `planning/stage-2/repos/dotj-core/evidence/span-factory-types-v1.json` | Reference oracle, packaged consumer and distribution evidence |
| `planning/stage-2/repos/dotj-core/evidence/system-type-identity-candidate-v1.json` | Reference oracle, packaged consumer and distribution evidence |
| `planning/stage-2/repos/dotj-core/evidence/throw-selected-lowering-v1.json` | Reference oracle, packaged consumer and distribution evidence |
| `planning/stage-2/repos/dotj-core/evidence/throw-site-upstream-adjacency-v1.json` | Reference oracle, packaged consumer and distribution evidence |
| `tools/oracle/dotj-core/audit-foundation-public-candidate.py` | Reference oracle, packaged consumer and distribution evidence |
| `planning/stage-2/IMPLEMENTATION-STATE.md` and `IMPLEMENTATION-PROGRESS.json` | Continuity and counts. |
| `planning/stage-2/implementation/batches/Batch-1936.md` | This report. |

**This batch is complete. The current request authorizes the next batch.**
