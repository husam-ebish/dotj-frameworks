# Batch-1263 report

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; framework remains IN PROGRESS) |
| Framework | `dotj-core` |
| Plan task | `DJ-001-WP-01-T1` |
| Outcome | Added selected ISpanFormattable contract and Int32 two-character buffer behavior. |
| Validation | Pinned .NET twenty-one-type metadata and span-format observations, external Java consumer, public audit, JAR and distribution inventory passed. |
| Limitation | CLR Span/out parameter ABI, broad formatting and full interface enumeration remain open. |
| Public API qualification | OPEN; no fully qualified public .j facade. |

## Progress

| Metric | Actual value |
|---|---:|
| Completed implementation tasks | **0 / 1,092 (0.00%)** |
| Remaining implementation tasks | **1,092 (100.00%)** |
| Frameworks fully implemented and qualified | **0 / 66 (0.00%)** |
| In-progress / not-started frameworks | **1 / 65** |
| Batches completed, total | **1,263** |
| Batches planned, total | **Unknown**; no project-wide batch baseline |
| Batches remaining, total | **Unknown**; acceptance items are not batches |
| Outstanding acceptance items | **1,686**: 330 gates + 264 naming tasks + 1,092 implementation tasks, less accepted items |
| Next proposed batch | `Batch-1264`: Probe and implement selected IUtf8SpanFormattable behavior. |
| Progress measure | Equal-weight WP and SDK integration task completions; prerequisite gates excluded; partials receive zero credit. |

## Files changed

| Path | Purpose |
|---|---|
| `dotj-core/dotj-core-public/src/main/java/System/ISpanFormattable.java` | Selected span formatting contract and refreshed foundation evidence. |
| `dotj-core/dotj-core-public/src/main/java/System/Int32.java` | Selected span formatting contract and refreshed foundation evidence. |
| `dotj-core/dotj-core-public/src/main/java/System/Type.java` | Selected span formatting contract and refreshed foundation evidence. |
| `dotj-core/dotj-core-public/src/test/java/consumer/ProductTypeIdentityConsumer.java` | Selected span formatting contract and refreshed foundation evidence. |
| `tools/oracle/dotj-core/foundation-public-metadata/Program.cs` | Selected span formatting contract and refreshed foundation evidence. |
| `tools/oracle/dotj-core/capture-foundation-public-metadata.py` | Selected span formatting contract and refreshed foundation evidence. |
| `tools/oracle/dotj-core/build-system-type-candidate.py` | Selected span formatting contract and refreshed foundation evidence. |
| `tools/oracle/dotj-core/lower-selected-typeof.py` | Selected span formatting contract and refreshed foundation evidence. |
| `tools/oracle/dotj-core/build-foundation-product-candidate.py` | Selected span formatting contract and refreshed foundation evidence. |
| `tools/oracle/dotj-core/audit-foundation-public-candidate.py` | Selected span formatting contract and refreshed foundation evidence. |
| `planning/stage-2/repos/dotj-core/WP01-T1-CONTRACT-v1.md` | Selected span formatting contract and refreshed foundation evidence. |
| `planning/stage-2/repos/dotj-core/evidence/foundation-selected-metadata-v10.0.12.json` | Selected span formatting contract and refreshed foundation evidence. |
| `planning/stage-2/repos/dotj-core/evidence/system-type-identity-candidate-v1.json` | Selected span formatting contract and refreshed foundation evidence. |
| `planning/stage-2/repos/dotj-core/evidence/typeof-selected-lowering-v1.json` | Selected span formatting contract and refreshed foundation evidence. |
| `planning/stage-2/repos/dotj-core/evidence/foundation-product-candidate-v1.json` | Selected span formatting contract and refreshed foundation evidence. |
| `planning/stage-2/repos/dotj-core/evidence/foundation-public-candidate-ledger-v1.json` | Selected span formatting contract and refreshed foundation evidence. |
| `planning/stage-2/repos/dotj-core/evidence/foundation-file-notice-map-v1.json` | Selected span formatting contract and refreshed foundation evidence. |
| `planning/stage-2/IMPLEMENTATION-STATE.md` and `IMPLEMENTATION-PROGRESS.json` | Continuity and counts. |
| `planning/stage-2/implementation/batches/Batch-1263.md` | This report. |

**This batch is complete. The current request authorizes the next batch.**

## Verification

| Check | Result |
|---|---|
| Pinned .NET behavior | PASS: ISpanFormattable signature/inheritance, Int32 lookup and two buffer results. |
| External Java consumer | PASS: public interface dispatch, successful and short-buffer calls. |
| Candidate package | PASS: JAR, twenty-one-type public audit and source/class inventory. |
| Qualification | OPEN: CLR Span/out ABI and complete formatting behavior. |
