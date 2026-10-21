# Batch-1384 report

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; framework remains IN PROGRESS) |
| Framework | `dotj-core` |
| Plan task | `DJ-001-WP-01-T1` |
| Outcome | Added bounded .j throw lowering for variable and Exception-constructor forms through ThrowSite.capture. |
| Validation | Generated external Java consumer passes identity, message and stack checks; 29-type audit, package and 30-source rights inventory pass after source-hash refresh. |
| Limitation | General .j parser, complex operands, rethrow, exact CLR frames, E01 rights and WP-01 qualification remain open. |
| Public API qualification | OPEN; no fully qualified public .j facade. |

## Progress

| Metric | Actual value |
|---|---:|
| Completed implementation tasks | **0 / 1,092 (0.00%)** |
| Remaining implementation tasks | **1,092 (100.00%)** |
| Frameworks fully implemented and qualified | **0 / 66 (0.00%)** |
| In-progress / not-started frameworks | **1 / 65** |
| Batches completed, total | **1,384** |
| Batches planned, total | **Unknown**; no project-wide batch baseline |
| Batches remaining, total | **Unknown**; acceptance items are not batches |
| Outstanding acceptance items | **1,686**: 330 gates + 264 naming tasks + 1,092 implementation tasks, less accepted items |
| Next proposed batch | `Batch-1385`: Extend selected throw lowering to rethrow behavior and pin CLR stack preservation. |
| Progress measure | Equal-weight WP and SDK integration task completions; prerequisite gates excluded; partials receive zero credit. |

## Files changed

| Path | Purpose |
|---|---|
| `planning/stage-2/repos/dotj-core/WP01-T1-CONTRACT-v1.md` | Bounded throw lowering script and external consumer evidence. |
| `planning/stage-2/repos/dotj-core/evidence/foundation-product-candidate-v1.json` | Bounded throw lowering script and external consumer evidence. |
| `planning/stage-2/repos/dotj-core/evidence/foundation-rights-inputs-v1.json` | Bounded throw lowering script and external consumer evidence. |
| `planning/stage-2/repos/dotj-core/evidence/system-type-identity-candidate-v1.json` | Bounded throw lowering script and external consumer evidence. |
| `planning/stage-2/repos/dotj-core/evidence/wp01-t1-contract-audit-v10.0.12.json` | Bounded throw lowering script and external consumer evidence. |
| `planning/stage-2/repos/dotj-core/evidence/throw-selected-lowering-v1.json` | Bounded throw lowering script and external consumer evidence. |
| `tools/oracle/dotj-core/lower-selected-throw.py` | Bounded throw lowering script and external consumer evidence. |
| `planning/stage-2/IMPLEMENTATION-STATE.md` and `IMPLEMENTATION-PROGRESS.json` | Continuity and counts. |
| `planning/stage-2/implementation/batches/Batch-1384.md` | This report. |

**This batch is complete. The current request authorizes the next batch.**
