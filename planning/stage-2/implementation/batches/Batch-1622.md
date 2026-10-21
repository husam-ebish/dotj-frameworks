# Batch-1622 report

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; framework remains IN PROGRESS) |
| Framework | `dotj-core` |
| Plan task | `DJ-001-WP-05-T1` |
| Outcome | Apply custom negative sign to selected Int32 decimal formats |
| Validation | Pinned .NET D, D5 and ToString(provider) outputs matched packaged Java string and Char/UTF-8 span consumers; 20/20 foundation gate pass |
| Limitation | G, currency, percent and other provider-sensitive formats remain open |
| Public API qualification | OPEN; no fully qualified public .j facade. |

## Progress

| Metric | Actual value |
|---|---:|
| Completed implementation tasks | **0 / 1,092 (0.00%)** |
| Remaining implementation tasks | **1,092 (100.00%)** |
| Frameworks fully implemented and qualified | **0 / 66 (0.00%)** |
| In-progress / not-started frameworks | **1 / 65** |
| Batches completed, total | **1,622** |
| Batches planned, total | **Unknown**; no project-wide batch baseline |
| Batches remaining, total | **Unknown**; acceptance items are not batches |
| Outstanding acceptance items | **1,686**: 330 gates + 264 naming tasks + 1,092 implementation tasks, less accepted items |
| Next proposed batch | `Batch-1623`: Extend custom provider behavior to selected general formatting |
| Progress measure | Equal-weight WP and SDK integration task completions; prerequisite gates excluded; partials receive zero credit. |

## Files changed

| Path | Purpose |
|---|---|
| `dotj-core/dotj-core-public/src/main/java/System/Int32.java` | Custom negative sign for selected decimal formatting |
| `dotj-core/dotj-core-public/src/test/java/consumer/ProductInt32SpanConsumer.java` | Custom negative sign for selected decimal formatting |
| `planning/stage-2/repos/dotj-core/WP05-T1-BIT-HELPERS-v1.md` | Custom negative sign for selected decimal formatting |
| `planning/stage-2/repos/dotj-core/evidence/foundation-e01-review-packet-v1.json` | Custom negative sign for selected decimal formatting |
| `planning/stage-2/repos/dotj-core/evidence/foundation-file-notice-map-v1.json` | Custom negative sign for selected decimal formatting |
| `planning/stage-2/repos/dotj-core/evidence/foundation-notice-review-queue-v1.json` | Custom negative sign for selected decimal formatting |
| `planning/stage-2/repos/dotj-core/evidence/foundation-product-candidate-v1.json` | Custom negative sign for selected decimal formatting |
| `planning/stage-2/repos/dotj-core/evidence/foundation-public-candidate-gate-v1.json` | Custom negative sign for selected decimal formatting |
| `planning/stage-2/repos/dotj-core/evidence/foundation-public-candidate-ledger-v1.json` | Custom negative sign for selected decimal formatting |
| `planning/stage-2/repos/dotj-core/evidence/foundation-rights-inputs-v1.json` | Custom negative sign for selected decimal formatting |
| `planning/stage-2/repos/dotj-core/evidence/foundation-selected-metadata-v10.0.12.json` | Custom negative sign for selected decimal formatting |
| `planning/stage-2/repos/dotj-core/evidence/foundation-semantic-surface-v1.json` | Custom negative sign for selected decimal formatting |
| `planning/stage-2/repos/dotj-core/evidence/foundation-source-provenance-v1.json` | Custom negative sign for selected decimal formatting |
| `planning/stage-2/repos/dotj-core/evidence/foundation-upstream-text-comparison-v1.json` | Custom negative sign for selected decimal formatting |
| `planning/stage-2/repos/dotj-core/evidence/int32-declared-signature-audit-v1.json` | Custom negative sign for selected decimal formatting |
| `planning/stage-2/repos/dotj-core/evidence/int32-erasure-contract-v1.json` | Custom negative sign for selected decimal formatting |
| `planning/stage-2/repos/dotj-core/evidence/span-factory-types-v1.json` | Custom negative sign for selected decimal formatting |
| `planning/stage-2/repos/dotj-core/evidence/system-type-identity-candidate-v1.json` | Custom negative sign for selected decimal formatting |
| `planning/stage-2/repos/dotj-core/evidence/throw-selected-lowering-v1.json` | Custom negative sign for selected decimal formatting |
| `planning/stage-2/repos/dotj-core/evidence/throw-site-upstream-adjacency-v1.json` | Custom negative sign for selected decimal formatting |
| `tools/oracle/dotj-core/build-foundation-product-candidate.py` | Custom negative sign for selected decimal formatting |
| `tools/oracle/dotj-core/foundation-public-metadata/Program.cs` | Custom negative sign for selected decimal formatting |
| `planning/stage-2/IMPLEMENTATION-STATE.md` and `IMPLEMENTATION-PROGRESS.json` | Continuity and counts. |
| `planning/stage-2/implementation/batches/Batch-1622.md` | This report. |

**This batch is complete. The current request authorizes the next batch.**
