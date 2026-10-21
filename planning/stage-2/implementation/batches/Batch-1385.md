# Batch-1385 report

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; framework remains IN PROGRESS) |
| Framework | `dotj-core` |
| Plan task | `DJ-001-WP-01-T1` |
| Outcome | Added selected bare .j rethrow lowering with pinned exception and stack identity behavior. |
| Validation | Pinned .NET capture, generated Java external consumer, 29-type audit, semantic inventory, distribution and rights-input inventory passed. |
| Limitation | General catch binding, exact CLR frames, E01 rights and WP-01 qualification remain open. |
| Public API qualification | OPEN; no fully qualified public .j facade. |

## Progress

| Metric | Actual value |
|---|---:|
| Completed implementation tasks | **0 / 1,092 (0.00%)** |
| Remaining implementation tasks | **1,092 (100.00%)** |
| Frameworks fully implemented and qualified | **0 / 66 (0.00%)** |
| In-progress / not-started frameworks | **1 / 65** |
| Batches completed, total | **1,385** |
| Batches planned, total | **Unknown**; no project-wide batch baseline |
| Batches remaining, total | **Unknown**; acceptance items are not batches |
| Outstanding acceptance items | **1,686**: 330 gates + 264 naming tasks + 1,092 implementation tasks, less accepted items |
| Next proposed batch | `Batch-1386`: Map selected Exception.TargetSite to a bounded throw-site method identity. |
| Progress measure | Equal-weight WP and SDK integration task completions; prerequisite gates excluded; partials receive zero credit. |

## Files changed

| Path | Purpose |
|---|---|
| `planning/stage-2/repos/dotj-core/WP01-T1-CONTRACT-v1.md` | Selected bare rethrow behavior and updated lowering evidence. |
| `planning/stage-2/repos/dotj-core/evidence/foundation-selected-metadata-v10.0.12.json` | Selected bare rethrow behavior and updated lowering evidence. |
| `planning/stage-2/repos/dotj-core/evidence/foundation-semantic-surface-v1.json` | Selected bare rethrow behavior and updated lowering evidence. |
| `planning/stage-2/repos/dotj-core/evidence/throw-selected-lowering-v1.json` | Selected bare rethrow behavior and updated lowering evidence. |
| `planning/stage-2/repos/dotj-core/evidence/wp01-t1-contract-audit-v10.0.12.json` | Selected bare rethrow behavior and updated lowering evidence. |
| `tools/oracle/dotj-core/build-foundation-product-candidate.py` | Selected bare rethrow behavior and updated lowering evidence. |
| `tools/oracle/dotj-core/foundation-public-metadata/Program.cs` | Selected bare rethrow behavior and updated lowering evidence. |
| `tools/oracle/dotj-core/lower-selected-throw.py` | Selected bare rethrow behavior and updated lowering evidence. |
| `planning/stage-2/IMPLEMENTATION-STATE.md` and `IMPLEMENTATION-PROGRESS.json` | Continuity and counts. |
| `planning/stage-2/implementation/batches/Batch-1385.md` | This report. |

**This batch is complete. The current request authorizes the next batch.**
