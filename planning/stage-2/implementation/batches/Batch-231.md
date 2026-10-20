# Batch-231 report

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; framework remains IN PROGRESS) |
| Framework | `dotj-core` |
| Plan task | `E03` |
| Outcome | Record infinite-timeout behavior when the generic source faults. |
| Validation | 38 selected Task/ValueTask reference cases passed on pinned CoreLib, including waitAsyncInfiniteTimeoutFault. |
| Limitation | This is a bounded .NET reference observation; Java timeout behavior and public Task.WaitAsync parity remain open. |
| Public API qualification | OPEN; no fully qualified public .j facade. |

## Progress

| Metric | Actual value |
|---|---:|
| Completed implementation tasks | **0 / 1,092 (0.00%)** |
| Remaining implementation tasks | **1,092 (100.00%)** |
| Frameworks fully implemented and qualified | **0 / 66 (0.00%)** |
| In-progress / not-started frameworks | **1 / 65** |
| Batches completed / planned | **231 / 1,936 (11.93%)** (`stage-2-batches-v3`) |
| Requested 27-point series | **8 / 27 complete** (`Batch-224` through `Batch-250`) |
| Batches still to do | **1,705 planned**; revise the denominator in a new plan version when scope or batch granularity changes |
| Next proposed batch | `Batch-232`: Record infinite-timeout behavior when the generic source cancels. |
| Progress measure | Equal-weight WP and SDK integration task completions; prerequisite gates excluded; partials receive zero credit. |

## Files changed

| Path | Purpose |
|---|---|
| `tools/oracle/dotj-core/task-behavior/Program.cs` | One scheduled WaitAsync reference case and progress evidence. |
| `tools/oracle/dotj-core/run-foundation-gate.py` | One scheduled WaitAsync reference case and progress evidence. |
| `planning/stage-2/repos/dotj-core/evidence/task-behavior-v10.0.12/oracle-output.json` | One scheduled WaitAsync reference case and progress evidence. |
| `planning/stage-2/IMPLEMENTATION-STATE.md` and `IMPLEMENTATION-PROGRESS.json` | Continuity and counts. |
| `planning/stage-2/implementation/batches/Batch-231.md` | This report. |

**STOPPED. Waiting for your CONTINUE signal before starting the next batch.**
