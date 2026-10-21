# Batch-1367 report

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; framework remains IN PROGRESS) |
| Framework | `dotj-core` |
| Plan task | `DJ-001-WP-01-T1` |
| Outcome | Added selected case-sensitive and case-insensitive lookup across 29 public CoreLib types. |
| Validation | 29 paired pinned .NET observations, Java consumer, 29-type audit and distribution inventory passed. |
| Limitation | General Unicode case folding and remaining type names remain open. |
| Public API qualification | OPEN; no fully qualified public .j facade. |

## Progress

| Metric | Actual value |
|---|---:|
| Completed implementation tasks | **0 / 1,092 (0.00%)** |
| Remaining implementation tasks | **1,092 (100.00%)** |
| Frameworks fully implemented and qualified | **0 / 66 (0.00%)** |
| In-progress / not-started frameworks | **1 / 65** |
| Batches completed, total | **1,367** |
| Batches planned, total | **Unknown**; no project-wide batch baseline |
| Batches remaining, total | **Unknown**; acceptance items are not batches |
| Outstanding acceptance items | **1,686**: 330 gates + 264 naming tasks + 1,092 implementation tasks, less accepted items |
| Next proposed batch | `Batch-1368`: Check selected assembly-qualified case lookup across the 29 public CoreLib types. |
| Progress measure | Equal-weight WP and SDK integration task completions; prerequisite gates excluded; partials receive zero credit. |

## Files changed

| Path | Purpose |
|---|---|
| `dotj-core/dotj-core-public/src/main/java/System/Type.java` | Oracle, resolver, consumer and contract evidence for selected case lookup; robust oracle capture. |
| `dotj-core/dotj-core-public/src/test/java/consumer/ProductTypeIdentityConsumer.java` | Oracle, resolver, consumer and contract evidence for selected case lookup; robust oracle capture. |
| `planning/stage-2/repos/dotj-core/WP01-T1-CONTRACT-v1.md` | Oracle, resolver, consumer and contract evidence for selected case lookup; robust oracle capture. |
| `planning/stage-2/repos/dotj-core/evidence/foundation-file-notice-map-v1.json` | Oracle, resolver, consumer and contract evidence for selected case lookup; robust oracle capture. |
| `planning/stage-2/repos/dotj-core/evidence/foundation-product-candidate-v1.json` | Oracle, resolver, consumer and contract evidence for selected case lookup; robust oracle capture. |
| `planning/stage-2/repos/dotj-core/evidence/foundation-public-candidate-ledger-v1.json` | Oracle, resolver, consumer and contract evidence for selected case lookup; robust oracle capture. |
| `planning/stage-2/repos/dotj-core/evidence/foundation-selected-metadata-v10.0.12.json` | Oracle, resolver, consumer and contract evidence for selected case lookup; robust oracle capture. |
| `planning/stage-2/repos/dotj-core/evidence/system-type-identity-candidate-v1.json` | Oracle, resolver, consumer and contract evidence for selected case lookup; robust oracle capture. |
| `planning/stage-2/repos/dotj-core/evidence/typeof-selected-lowering-v1.json` | Oracle, resolver, consumer and contract evidence for selected case lookup; robust oracle capture. |
| `tools/oracle/dotj-core/build-system-type-candidate.py` | Oracle, resolver, consumer and contract evidence for selected case lookup; robust oracle capture. |
| `tools/oracle/dotj-core/capture-foundation-public-metadata.py` | Oracle, resolver, consumer and contract evidence for selected case lookup; robust oracle capture. |
| `tools/oracle/dotj-core/foundation-public-metadata/Program.cs` | Oracle, resolver, consumer and contract evidence for selected case lookup; robust oracle capture. |
| `planning/stage-2/IMPLEMENTATION-STATE.md` and `IMPLEMENTATION-PROGRESS.json` | Continuity and counts. |
| `planning/stage-2/implementation/batches/Batch-1367.md` | This report. |

**This batch is complete. The current request authorizes the next batch.**

## Verification

| Check | Result |
|---|---|
| Pinned .NET behavior | PASS: 29 paired case lookup observations. |
| External Java consumer | PASS: sensitive null and insensitive identity for all 29. |
| Candidate package | PASS: 29-type public audit, JAR and distribution inventory. |
| Qualification | OPEN: general Unicode case folding and remaining names. |
