# Batch-1258 report

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; framework remains IN PROGRESS) |
| Framework | `dotj-core` |
| Plan task | `DJ-001-WP-01-T1` |
| Outcome | Added selected Decimal value candidate and typed IConvertible.ToDecimal return. |
| Validation | Pinned .NET eighteen-type metadata and decimal(42) observation, external Java consumer, public audit, JAR and distribution inventory passed. |
| Limitation | Nine CLR constructors and 78 methods, fractional behavior, arithmetic, formatting and qualification remain open. |
| Public API qualification | OPEN; no fully qualified public .j facade. |

## Progress

| Metric | Actual value |
|---|---:|
| Completed implementation tasks | **0 / 1,092 (0.00%)** |
| Remaining implementation tasks | **1,092 (100.00%)** |
| Frameworks fully implemented and qualified | **0 / 66 (0.00%)** |
| In-progress / not-started frameworks | **1 / 65** |
| Batches completed, total | **1,258** |
| Batches planned, total | **Unknown**; no project-wide batch baseline |
| Batches remaining, total | **Unknown**; acceptance items are not batches |
| Outstanding acceptance items | **1,686**: 330 gates + 264 naming tasks + 1,092 implementation tasks, less accepted items |
| Next proposed batch | `Batch-1259`: Implement selected DateTime public value candidate for IConvertible.ToDateTime. |
| Progress measure | Equal-weight WP and SDK integration task completions; prerequisite gates excluded; partials receive zero credit. |

## Files changed

| Path | Purpose |
|---|---|
| `dotj-core/dotj-core-public/src/main/java/System/Decimal.java` | Pinned Decimal integer construction and refreshed foundation evidence. |
| `dotj-core/dotj-core-public/src/main/java/System/IConvertible.java` | Pinned Decimal integer construction and refreshed foundation evidence. |
| `dotj-core/dotj-core-public/src/main/java/System/Type.java` | Pinned Decimal integer construction and refreshed foundation evidence. |
| `dotj-core/dotj-core-public/src/test/java/consumer/ProductTypeIdentityConsumer.java` | Pinned Decimal integer construction and refreshed foundation evidence. |
| `tools/oracle/dotj-core/foundation-public-metadata/Program.cs` | Pinned Decimal integer construction and refreshed foundation evidence. |
| `tools/oracle/dotj-core/capture-foundation-public-metadata.py` | Pinned Decimal integer construction and refreshed foundation evidence. |
| `tools/oracle/dotj-core/build-system-type-candidate.py` | Pinned Decimal integer construction and refreshed foundation evidence. |
| `tools/oracle/dotj-core/lower-selected-typeof.py` | Pinned Decimal integer construction and refreshed foundation evidence. |
| `tools/oracle/dotj-core/build-foundation-product-candidate.py` | Pinned Decimal integer construction and refreshed foundation evidence. |
| `tools/oracle/dotj-core/audit-foundation-public-candidate.py` | Pinned Decimal integer construction and refreshed foundation evidence. |
| `planning/stage-2/repos/dotj-core/WP01-T1-CONTRACT-v1.md` | Pinned Decimal integer construction and refreshed foundation evidence. |
| `planning/stage-2/repos/dotj-core/evidence/foundation-selected-metadata-v10.0.12.json` | Pinned Decimal integer construction and refreshed foundation evidence. |
| `planning/stage-2/repos/dotj-core/evidence/system-type-identity-candidate-v1.json` | Pinned Decimal integer construction and refreshed foundation evidence. |
| `planning/stage-2/repos/dotj-core/evidence/typeof-selected-lowering-v1.json` | Pinned Decimal integer construction and refreshed foundation evidence. |
| `planning/stage-2/repos/dotj-core/evidence/foundation-product-candidate-v1.json` | Pinned Decimal integer construction and refreshed foundation evidence. |
| `planning/stage-2/repos/dotj-core/evidence/foundation-public-candidate-ledger-v1.json` | Pinned Decimal integer construction and refreshed foundation evidence. |
| `planning/stage-2/repos/dotj-core/evidence/foundation-file-notice-map-v1.json` | Pinned Decimal integer construction and refreshed foundation evidence. |
| `planning/stage-2/IMPLEMENTATION-STATE.md` and `IMPLEMENTATION-PROGRESS.json` | Continuity and counts. |
| `planning/stage-2/implementation/batches/Batch-1258.md` | This report. |

**This batch is complete. The current request authorizes the next batch.**

## Verification

| Check | Result |
|---|---|
| Pinned .NET metadata | PASS: decimal(42) text/bits, ValueType relation, constructor and method counts. |
| External Java consumer | PASS: selected Decimal construction and typed ToDecimal call. |
| Candidate package | PASS: JAR, eighteen-type public audit and source/class inventory. |
| Qualification | OPEN: broad Decimal API and value behavior. |
