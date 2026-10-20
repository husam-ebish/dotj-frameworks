# Batch-221 report

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; framework remains IN PROGRESS) |
| Framework | `dotj-core` |
| Plan task | `E03` |
| Outcome | Added a 200-round internal race fixture for source completion versus canceling only its wait. |
| Validation | Both wait outcomes were observed; every round preserved successful source completion, one stable wait outcome, and zero retained signal listeners; the combined foundation gate passed with four internal async fixtures. |
| Limitation | This bounded Java race does not establish .NET Task.WaitAsync parity, exhaustive interleavings, or a qualified public Task/ValueTask representation. |
| Public API qualification | OPEN; no fully qualified public .j facade. |

## Progress

| Metric | Actual value |
|---|---:|
| Completed implementation tasks | **0 / 1,092 (0.00%)** |
| Remaining implementation tasks | **1,092 (100.00%)** |
| Frameworks fully implemented and qualified | **0 / 66 (0.00%)** |
| In-progress / not-started frameworks | **1 / 65** |
| Batches completed | **221** (`Batch-001` through `Batch-221`) |
| This requested batch | **1 / 1 complete** |
| Total planned batches | **Not baselined**; no defensible cumulative `x/y` denominator exists yet |
| Batches still to do | **Unknown**; lower bound: at least 66 to address 66 unqualified frameworks |
| Next proposed batch | `Batch-222`: Baseline a versioned total batch plan for a defensible cumulative x/y count. |
| Progress measure | Equal-weight WP and SDK integration task completions; prerequisite gates excluded; partials receive zero credit. |

## Public async names and batch denominator

| Question | Answer |
|---|---|
| How will public async methods be named? | The selected .NET source spells them `Task.WaitAsync(...)`, `IAsyncDisposable.DisposeAsync()`, and `CancellationTokenSource.CancelAsync()`. The intended public `.j` facade must preserve `WaitAsync`, `DisposeAsync`, and `CancelAsync` with that casing and concept. These are planned names, not implemented or qualified public Java signatures. Internal helpers such as `waitAsync` can use Java spelling because they are package-private. |
| Why has the “at least 66” count stayed the same? | It is a lower bound derived from **66 unqualified frameworks**, with at least one future batch needed per framework. None has qualified yet, so the bound has not fallen. Partial evidence batches increase the completed count without reducing it. |
| Why no cumulative `221/y`? | The 1,092 implementation-task denominator is fixed, but no complete batch schedule says how many batches each task and its gates require. Assigning `y` now would be invented. Batch 222 is reserved to baseline a versioned batch schedule so future reports can show a planned `x/y` and revise it transparently if scope changes. |

## Files changed

| Path | Purpose |
|---|---|
| `dotj-core/dotj-core-01/src/test/java/org/dotj/internal/async/AsyncWaitRaceTest.java` | Wait-race fixture, bounded evidence, and batch reporting clarity. |
| `tools/oracle/dotj-core/run-async-java-fixtures.ps1` | Wait-race fixture, bounded evidence, and batch reporting clarity. |
| `tools/oracle/dotj-core/run-foundation-gate.py` | Wait-race fixture, bounded evidence, and batch reporting clarity. |
| `planning/stage-2/repos/dotj-core/evidence/async-state-map-v10.0.12.md` | Wait-race fixture, bounded evidence, and batch reporting clarity. |
| `planning/stage-2/repos/dotj-core/evidence/foundation-gate-v10.0.12.json` | Wait-race fixture, bounded evidence, and batch reporting clarity. |
| `planning/stage-2/repos/dotj-core/evidence/internal-core-jar-v1.json` | Refreshed working-tree source hash after Git line-ending conversion; internal JAR hash remains unchanged. |
| `planning/stage-2/repos/dotj-core/WP01-WP02-READINESS-v10.0.12.md` | Wait-race fixture, bounded evidence, and batch reporting clarity. |
| `tools/progress/record-implementation-batch.py` | Wait-race fixture, bounded evidence, and batch reporting clarity. |
| `planning/stage-2/IMPLEMENTATION-STATE.md` and `IMPLEMENTATION-PROGRESS.json` | Continuity and counts. |
| `planning/stage-2/implementation/batches/Batch-221.md` | This report. |

**STOPPED. Waiting for your CONTINUE signal before starting the next batch.**
