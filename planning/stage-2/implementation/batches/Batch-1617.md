# Batch-1617 report

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; framework remains IN PROGRESS) |
| Framework | `dotj-core` |
| Plan task | `DJ-001-WP-05-T1` |
| Outcome | Implement selected Int32 Span formatting carrier |
| Validation | Pinned CLR 42 success and short-buffer vectors, packaged Char and UTF-8 Byte subview consumer, and 19/19 foundation gate pass |
| Limitation | Heap-backed generic carrier has no CLR byref-like lifetime or exact overload ABI; wider formats and provider behavior remain open |
| Public API qualification | OPEN; no fully qualified public .j facade. |

## Progress

| Metric | Actual value |
|---|---:|
| Completed implementation tasks | **0 / 1,092 (0.00%)** |
| Remaining implementation tasks | **1,092 (100.00%)** |
| Frameworks fully implemented and qualified | **0 / 66 (0.00%)** |
| In-progress / not-started frameworks | **1 / 65** |
| Batches completed, total | **1,617** |
| Batches planned, total | **Unknown**; no project-wide batch baseline |
| Batches remaining, total | **Unknown**; acceptance items are not batches |
| Outstanding acceptance items | **1,686**: 330 gates + 264 naming tasks + 1,092 implementation tasks, less accepted items |
| Next proposed batch | `Batch-1618`: Expand Int32 span formatting vectors and provider behavior |
| Progress measure | Equal-weight WP and SDK integration task completions; prerequisite gates excluded; partials receive zero credit. |

## Files changed

| Path | Purpose |
|---|---|
| `dotj-core/dotj-core-public/src/main/java/System/Int32.java` | Selected mutable Span formatting carrier and erasure contract |
| `dotj-core/dotj-core-public/src/main/java/System/Span.java` | Selected mutable Span formatting carrier and erasure contract |
| `dotj-core/dotj-core-public/src/test/java/consumer/ProductInt32SpanConsumer.java` | Selected mutable Span formatting carrier and erasure contract |
| `planning/stage-2/repos/dotj-core/API-COMPATIBILITY.md` | Selected mutable Span formatting carrier and erasure contract |
| `planning/stage-2/repos/dotj-core/WP05-T1-BIT-HELPERS-v1.md` | Selected mutable Span formatting carrier and erasure contract |
| `planning/stage-2/repos/dotj-core/evidence/foundation-e01-review-packet-v1.json` | Selected mutable Span formatting carrier and erasure contract |
| `planning/stage-2/repos/dotj-core/evidence/foundation-file-notice-map-v1.json` | Selected mutable Span formatting carrier and erasure contract |
| `planning/stage-2/repos/dotj-core/evidence/foundation-notice-review-queue-v1.json` | Selected mutable Span formatting carrier and erasure contract |
| `planning/stage-2/repos/dotj-core/evidence/foundation-product-candidate-v1.json` | Selected mutable Span formatting carrier and erasure contract |
| `planning/stage-2/repos/dotj-core/evidence/foundation-public-candidate-gate-v1.json` | Selected mutable Span formatting carrier and erasure contract |
| `planning/stage-2/repos/dotj-core/evidence/foundation-public-candidate-ledger-v1.json` | Selected mutable Span formatting carrier and erasure contract |
| `planning/stage-2/repos/dotj-core/evidence/foundation-rights-inputs-v1.json` | Selected mutable Span formatting carrier and erasure contract |
| `planning/stage-2/repos/dotj-core/evidence/foundation-semantic-surface-v1.json` | Selected mutable Span formatting carrier and erasure contract |
| `planning/stage-2/repos/dotj-core/evidence/foundation-source-provenance-v1.json` | Selected mutable Span formatting carrier and erasure contract |
| `planning/stage-2/repos/dotj-core/evidence/foundation-upstream-text-comparison-v1.json` | Selected mutable Span formatting carrier and erasure contract |
| `planning/stage-2/repos/dotj-core/evidence/int32-declared-signature-audit-v1.json` | Selected mutable Span formatting carrier and erasure contract |
| `planning/stage-2/repos/dotj-core/evidence/int32-erasure-contract-v1.json` | Selected mutable Span formatting carrier and erasure contract |
| `planning/stage-2/repos/dotj-core/evidence/system-type-identity-candidate-v1.json` | Selected mutable Span formatting carrier and erasure contract |
| `planning/stage-2/repos/dotj-core/evidence/throw-selected-lowering-v1.json` | Selected mutable Span formatting carrier and erasure contract |
| `planning/stage-2/repos/dotj-core/evidence/throw-site-upstream-adjacency-v1.json` | Selected mutable Span formatting carrier and erasure contract |
| `tools/oracle/dotj-core/audit-foundation-source-provenance.py` | Selected mutable Span formatting carrier and erasure contract |
| `tools/oracle/dotj-core/audit-int32-declared-signatures.py` | Selected mutable Span formatting carrier and erasure contract |
| `tools/oracle/dotj-core/build-foundation-e01-review-packet.py` | Selected mutable Span formatting carrier and erasure contract |
| `tools/oracle/dotj-core/build-foundation-notice-review-queue.py` | Selected mutable Span formatting carrier and erasure contract |
| `tools/oracle/dotj-core/build-foundation-product-candidate.py` | Selected mutable Span formatting carrier and erasure contract |
| `tools/oracle/dotj-core/build-system-type-candidate.py` | Selected mutable Span formatting carrier and erasure contract |
| `tools/oracle/dotj-core/compare-foundation-upstream-text.py` | Selected mutable Span formatting carrier and erasure contract |
| `tools/oracle/dotj-core/lower-selected-typeof.py` | Selected mutable Span formatting carrier and erasure contract |
| `tools/oracle/dotj-core/run-foundation-public-candidate-gate.py` | Selected mutable Span formatting carrier and erasure contract |
| `tools/oracle/dotj-core/verify-int32-erasure-contract.py` | Selected mutable Span formatting carrier and erasure contract |
| `planning/stage-2/IMPLEMENTATION-STATE.md` and `IMPLEMENTATION-PROGRESS.json` | Continuity and counts. |
| `planning/stage-2/implementation/batches/Batch-1617.md` | This report. |

**This batch is complete. The current request authorizes the next batch.**
