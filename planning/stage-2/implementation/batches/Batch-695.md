# Batch-695 report

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; framework remains IN PROGRESS) |
| Framework | `dotj-core` |
| Plan task | `DJ-001-N01-T1` |
| Outcome | Verify pinned declared-public metadata and owning source hash for System.Threading.Tasks.Task::System.Collections.Generic.IAsyncEnumerable`1[System.Threading.Tasks.Task] WhenEach(System.Threading.Tasks.Task[]). |
| Validation | Pinned CoreLib metadata and owning source file hashes passed; 323/327 remaining signatures verified. |
| Limitation | Selected declared-public methods only; constructors, properties, member-level source attribution, Java representation, behavior, and N01 acceptance remain open. |
| Public API qualification | OPEN; no fully qualified public .j facade. |

## Progress

| Metric | Actual value |
|---|---:|
| Completed implementation tasks | **0 / 1,092 (0.00%)** |
| Remaining implementation tasks | **1,092 (100.00%)** |
| Frameworks fully implemented and qualified | **0 / 66 (0.00%)** |
| In-progress / not-started frameworks | **1 / 65** |
| Batches completed / planned | **695 / 2,386 (29.13%)** (`stage-2-batches-v6`) |
| Requested 300-point series | **295 / 300 complete** (`Batch-401` through `Batch-700`) |
| Batches still to do | **1,691 planned**; revise the denominator in a new plan version when scope or batch granularity changes |
| Next proposed batch | `Batch-696`: Verify pinned declared-public metadata and owning source hash for System.Threading.Tasks.Task::System.Collections.Generic.IAsyncEnumerable`1[System.Threading.Tasks.Task`1[TResult]] WhenEach[TResult](System.Collections.Generic.IEnumerable`1[System.Threading.Tasks.Task`1[TResult]]). |
| Progress measure | Equal-weight WP and SDK integration task completions; prerequisite gates excluded; partials receive zero credit. |

## Files changed

| Path | Purpose |
|---|---|
| `planning/stage-2/repos/dotj-core/evidence/n01-remaining-methods-v10.0.12.json` | Pinned declared-public method metadata and source-hash ledger. |
| `planning/stage-2/IMPLEMENTATION-STATE.md` and `IMPLEMENTATION-PROGRESS.json` | Continuity and counts. |
| `planning/stage-2/implementation/batches/Batch-695.md` | This report. |

**STOPPED. Waiting for your CONTINUE signal before starting the next batch.**
