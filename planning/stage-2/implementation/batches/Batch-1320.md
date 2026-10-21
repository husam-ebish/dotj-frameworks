# Batch-1320 report

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; framework remains IN PROGRESS) |
| Framework | `dotj-core` |
| Plan task | `DJ-001-WP-01-T1` |
| Outcome | Pinned and implemented selected assembly throwOnError error precedence and parameter position. |
| Validation | Six .NET observations, Java consumer, 29-type audit and distribution inventory passed. |
| Limitation | Complete error precedence, exact messages and binder resolution remain open. |
| Public API qualification | OPEN; no fully qualified public .j facade. |

## Progress

| Metric | Actual value |
|---|---:|
| Completed implementation tasks | **0 / 1,092 (0.00%)** |
| Remaining implementation tasks | **1,092 (100.00%)** |
| Frameworks fully implemented and qualified | **0 / 66 (0.00%)** |
| In-progress / not-started frameworks | **1 / 65** |
| Batches completed, total | **1,320** |
| Batches planned, total | **Unknown**; no project-wide batch baseline |
| Batches remaining, total | **Unknown**; acceptance items are not batches |
| Outstanding acceptance items | **1,686**: 330 gates + 264 naming tasks + 1,092 implementation tasks, less accepted items |
| Next proposed batch | `Batch-1321`: Probe selected whitespace inside assembly attribute values. |
| Progress measure | Equal-weight WP and SDK integration task completions; prerequisite gates excluded; partials receive zero credit. |

## Files changed

| Path | Purpose |
|---|---|
| `dotj-core/dotj-core-public/src/main/java/System/Type.java` | Selected parser, oracle, consumer and package evidence. |
| `dotj-core/dotj-core-public/src/test/java/consumer/ProductTypeIdentityConsumer.java` | Selected parser, oracle, consumer and package evidence. |
| `planning/stage-2/repos/dotj-core/WP01-T1-CONTRACT-v1.md` | Selected parser, oracle, consumer and package evidence. |
| `planning/stage-2/repos/dotj-core/evidence/foundation-file-notice-map-v1.json` | Selected parser, oracle, consumer and package evidence. |
| `planning/stage-2/repos/dotj-core/evidence/foundation-product-candidate-v1.json` | Selected parser, oracle, consumer and package evidence. |
| `planning/stage-2/repos/dotj-core/evidence/foundation-public-candidate-ledger-v1.json` | Selected parser, oracle, consumer and package evidence. |
| `planning/stage-2/repos/dotj-core/evidence/foundation-selected-metadata-v10.0.12.json` | Selected parser, oracle, consumer and package evidence. |
| `planning/stage-2/repos/dotj-core/evidence/system-type-identity-candidate-v1.json` | Selected parser, oracle, consumer and package evidence. |
| `planning/stage-2/repos/dotj-core/evidence/typeof-selected-lowering-v1.json` | Selected parser, oracle, consumer and package evidence. |
| `tools/oracle/dotj-core/build-system-type-candidate.py` | Selected parser, oracle, consumer and package evidence. |
| `tools/oracle/dotj-core/foundation-public-metadata/Program.cs` | Selected parser, oracle, consumer and package evidence. |
| `planning/stage-2/IMPLEMENTATION-STATE.md` and `IMPLEMENTATION-PROGRESS.json` | Continuity and counts. |
| `planning/stage-2/implementation/batches/Batch-1320.md` | This report. |

**This batch is complete. The current request authorizes the next batch.**

## Verification

| Check | Result |
|---|---|
| Pinned .NET behavior | PASS: six selected throwOnError cases. |
| External Java consumer | PASS: error identity, parameters and accepted unknown attribute. |
| Candidate package | PASS: 29-type public audit, JAR and distribution inventory. |
| Qualification | OPEN: full error precedence and binding. |
