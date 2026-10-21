# Batch-1317 report

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; framework remains IN PROGRESS) |
| Framework | `dotj-core` |
| Plan task | `DJ-001-WP-01-T1` |
| Outcome | Pinned and externally verified selected assembly attribute ordering and duplicate keys. |
| Validation | Six .NET observations, Java consumer, 29-type audit and distribution inventory passed. |
| Limitation | Complete attribute key policy and arbitrary assembly binding remain open. |
| Public API qualification | OPEN; no fully qualified public .j facade. |

## Progress

| Metric | Actual value |
|---|---:|
| Completed implementation tasks | **0 / 1,092 (0.00%)** |
| Remaining implementation tasks | **1,092 (100.00%)** |
| Frameworks fully implemented and qualified | **0 / 66 (0.00%)** |
| In-progress / not-started frameworks | **1 / 65** |
| Batches completed, total | **1,317** |
| Batches planned, total | **Unknown**; no project-wide batch baseline |
| Batches remaining, total | **Unknown**; acceptance items are not batches |
| Outstanding acceptance items | **1,686**: 330 gates + 264 naming tasks + 1,092 implementation tasks, less accepted items |
| Next proposed batch | `Batch-1318`: Probe selected assembly name punctuation and whitespace boundaries. |
| Progress measure | Equal-weight WP and SDK integration task completions; prerequisite gates excluded; partials receive zero credit. |

## Files changed

| Path | Purpose |
|---|---|
| `dotj-core/dotj-core-public/src/test/java/consumer/ProductTypeIdentityConsumer.java` | Oracle, consumer and contract evidence for selected attribute order. |
| `planning/stage-2/repos/dotj-core/WP01-T1-CONTRACT-v1.md` | Oracle, consumer and contract evidence for selected attribute order. |
| `planning/stage-2/repos/dotj-core/evidence/foundation-selected-metadata-v10.0.12.json` | Oracle, consumer and contract evidence for selected attribute order. |
| `planning/stage-2/repos/dotj-core/evidence/system-type-identity-candidate-v1.json` | Oracle, consumer and contract evidence for selected attribute order. |
| `tools/oracle/dotj-core/build-system-type-candidate.py` | Oracle, consumer and contract evidence for selected attribute order. |
| `tools/oracle/dotj-core/foundation-public-metadata/Program.cs` | Oracle, consumer and contract evidence for selected attribute order. |
| `planning/stage-2/IMPLEMENTATION-STATE.md` and `IMPLEMENTATION-PROGRESS.json` | Continuity and counts. |
| `planning/stage-2/implementation/batches/Batch-1317.md` | This report. |

**This batch is complete. The current request authorizes the next batch.**

## Verification

| Check | Result |
|---|---|
| Pinned .NET behavior | PASS: six selected ordering and duplicate cases. |
| External Java consumer | PASS: four accepted and two duplicate errors. |
| Candidate package | PASS: 29-type public audit, JAR and distribution inventory. |
| Qualification | OPEN: complete key policy and assembly binding. |
