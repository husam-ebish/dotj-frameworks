# Batch-158 report

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; framework remains IN PROGRESS) |
| Framework | `dotj-core` |
| Plan task | `E01` |
| Outcome | Built a deterministic class-only IDisposable candidate JAR from the independent Java probe. |
| Validation | Two builds produced the same SHA-256; JAR has exactly manifest and System/IDisposable.class; javap matched the selected interface shape. |
| Limitation | This is compile-only evidence, not a licensed or behavior-qualified product package. |
| Public API qualification | OPEN; no fully qualified public .j facade. |

## Progress

| Metric | Actual value |
|---|---:|
| Completed implementation tasks | **0 / 1,092 (0.00%)** |
| Remaining implementation tasks | **1,092 (100.00%)** |
| Frameworks fully implemented and qualified | **0 / 66 (0.00%)** |
| In-progress / not-started frameworks | **1 / 65** |
| Batches completed | **158** (`Batch-001` through `Batch-158`) |
| Batches still to do | **At least 66**; exact total is not baselined |
| Next proposed batch | `Batch-159`: Compile and run an external Java consumer against the candidate JAR. |
| Progress measure | Equal-weight WP and SDK integration task completions; prerequisite gates excluded; partials receive zero credit. |

## Files changed

| Path | Purpose |
|---|---|
| `tools/oracle/dotj-core/build-idisposable-candidate.py` | Deterministic candidate builder, content manifest, and file map. |
| `planning/stage-2/repos/dotj-core/evidence/idisposable-candidate-jar-v1.json` | Deterministic candidate builder, content manifest, and file map. |
| `planning/stage-2/repos/dotj-core/evidence/idisposable-file-notice-map-v10.0.12.json` | Deterministic candidate builder, content manifest, and file map. |
| `planning/stage-2/IMPLEMENTATION-STATE.md` and `IMPLEMENTATION-PROGRESS.json` | Continuity and counts. |
| `planning/stage-2/implementation/batches/Batch-158.md` | This report. |

**STOPPED. Waiting for your CONTINUE signal before starting the next batch.**
