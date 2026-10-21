# Batch-1615 report

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; framework remains IN PROGRESS) |
| Framework | `dotj-core` |
| Plan task | `DJ-001-WP-05-T1` |
| Outcome | Implement selected ReadOnlySpan Int32 parsing carrier |
| Validation | Pinned char/UTF-8 byte Parse and TryParse vectors, packaged consumer and 18/18 foundation gate pass |
| Limitation | Ten CLR overloads collapse to five JVM methods; byref-like lifetime and full span semantics open |
| Public API qualification | OPEN; no fully qualified public .j facade. |

## Progress

| Metric | Actual value |
|---|---:|
| Completed implementation tasks | **0 / 1,092 (0.00%)** |
| Remaining implementation tasks | **1,092 (100.00%)** |
| Frameworks fully implemented and qualified | **0 / 66 (0.00%)** |
| In-progress / not-started frameworks | **1 / 65** |
| Batches completed, total | **1,615** |
| Batches planned, total | **Unknown**; no project-wide batch baseline |
| Batches remaining, total | **Unknown**; acceptance items are not batches |
| Outstanding acceptance items | **1,686**: 330 gates + 264 naming tasks + 1,092 implementation tasks, less accepted items |
| Next proposed batch | `Batch-1616`: Resolve span erasure and extra public method contract gaps |
| Progress measure | Equal-weight WP and SDK integration task completions; prerequisite gates excluded; partials receive zero credit. |

## Files changed

| Path | Purpose |
|---|---|
| `dotj-core/dotj-core-public/src/main/java/System/Int32.java` | Selected ReadOnlySpan parsing behavior and explicit erasure audit |
| `dotj-core/dotj-core-public/src/main/java/System/ReadOnlySpan.java` | Selected ReadOnlySpan parsing behavior and explicit erasure audit |
| `dotj-core/dotj-core-public/src/test/java/consumer/ProductInt32ArithmeticConsumer.java` | Selected ReadOnlySpan parsing behavior and explicit erasure audit |
| `dotj-core/dotj-core-public/src/test/java/consumer/ProductTypeIdentityConsumer.java` | Selected ReadOnlySpan parsing behavior and explicit erasure audit |
| `planning/stage-2/repos/dotj-core/WP05-T1-BIT-HELPERS-v1.md` | Selected ReadOnlySpan parsing behavior and explicit erasure audit |
| `planning/stage-2/repos/dotj-core/evidence/foundation-e01-review-packet-v1.json` | Selected ReadOnlySpan parsing behavior and explicit erasure audit |
| `planning/stage-2/repos/dotj-core/evidence/foundation-file-notice-map-v1.json` | Selected ReadOnlySpan parsing behavior and explicit erasure audit |
| `planning/stage-2/repos/dotj-core/evidence/foundation-notice-review-queue-v1.json` | Selected ReadOnlySpan parsing behavior and explicit erasure audit |
| `planning/stage-2/repos/dotj-core/evidence/foundation-product-candidate-v1.json` | Selected ReadOnlySpan parsing behavior and explicit erasure audit |
| `planning/stage-2/repos/dotj-core/evidence/foundation-public-candidate-gate-v1.json` | Selected ReadOnlySpan parsing behavior and explicit erasure audit |
| `planning/stage-2/repos/dotj-core/evidence/foundation-public-candidate-ledger-v1.json` | Selected ReadOnlySpan parsing behavior and explicit erasure audit |
| `planning/stage-2/repos/dotj-core/evidence/foundation-rights-inputs-v1.json` | Selected ReadOnlySpan parsing behavior and explicit erasure audit |
| `planning/stage-2/repos/dotj-core/evidence/foundation-selected-metadata-v10.0.12.json` | Selected ReadOnlySpan parsing behavior and explicit erasure audit |
| `planning/stage-2/repos/dotj-core/evidence/foundation-semantic-surface-v1.json` | Selected ReadOnlySpan parsing behavior and explicit erasure audit |
| `planning/stage-2/repos/dotj-core/evidence/foundation-source-provenance-v1.json` | Selected ReadOnlySpan parsing behavior and explicit erasure audit |
| `planning/stage-2/repos/dotj-core/evidence/foundation-upstream-text-comparison-v1.json` | Selected ReadOnlySpan parsing behavior and explicit erasure audit |
| `planning/stage-2/repos/dotj-core/evidence/int32-declared-signature-audit-v1.json` | Selected ReadOnlySpan parsing behavior and explicit erasure audit |
| `planning/stage-2/repos/dotj-core/evidence/system-type-identity-candidate-v1.json` | Selected ReadOnlySpan parsing behavior and explicit erasure audit |
| `planning/stage-2/repos/dotj-core/evidence/throw-selected-lowering-v1.json` | Selected ReadOnlySpan parsing behavior and explicit erasure audit |
| `planning/stage-2/repos/dotj-core/evidence/throw-site-upstream-adjacency-v1.json` | Selected ReadOnlySpan parsing behavior and explicit erasure audit |
| `tools/oracle/dotj-core/audit-foundation-source-provenance.py` | Selected ReadOnlySpan parsing behavior and explicit erasure audit |
| `tools/oracle/dotj-core/audit-int32-declared-signatures.py` | Selected ReadOnlySpan parsing behavior and explicit erasure audit |
| `tools/oracle/dotj-core/build-foundation-e01-review-packet.py` | Selected ReadOnlySpan parsing behavior and explicit erasure audit |
| `tools/oracle/dotj-core/build-foundation-notice-review-queue.py` | Selected ReadOnlySpan parsing behavior and explicit erasure audit |
| `tools/oracle/dotj-core/build-foundation-product-candidate.py` | Selected ReadOnlySpan parsing behavior and explicit erasure audit |
| `tools/oracle/dotj-core/build-system-type-candidate.py` | Selected ReadOnlySpan parsing behavior and explicit erasure audit |
| `tools/oracle/dotj-core/compare-foundation-upstream-text.py` | Selected ReadOnlySpan parsing behavior and explicit erasure audit |
| `tools/oracle/dotj-core/foundation-public-metadata/Program.cs` | Selected ReadOnlySpan parsing behavior and explicit erasure audit |
| `tools/oracle/dotj-core/lower-selected-typeof.py` | Selected ReadOnlySpan parsing behavior and explicit erasure audit |
| `tools/oracle/dotj-core/run-foundation-public-candidate-gate.py` | Selected ReadOnlySpan parsing behavior and explicit erasure audit |
| `dotj-core/dotj-core-public/src/test/java/consumer/ProductInt32SpanConsumer.java` | Selected ReadOnlySpan parsing behavior and explicit erasure audit |
| `planning/stage-2/IMPLEMENTATION-STATE.md` and `IMPLEMENTATION-PROGRESS.json` | Continuity and counts. |
| `planning/stage-2/implementation/batches/Batch-1615.md` | This report. |

**This batch is complete. The current request authorizes the next batch.**
