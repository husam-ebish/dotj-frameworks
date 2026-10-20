# Batch-028 report

### Batch summary

| Field | Result |
|---|---|
| Batch | Batch-028 |
| Status | COMPLETE (bounded E03 independent oracle; E03 remains IN PROGRESS) |
| Framework/repository | .NET runtime and base libraries / `dotj-core` |
| Plan task IDs | E03, WP-01 synchronous disposal slice |
| Delivered outcome | Executed a small .NET 10.0.12 oracle for `IDisposable` dispatch and `using` cleanup/failure behavior. |

### What was implemented

| Item | Result |
|---|---|
| .j functionality | None. |
| Preparation completed | The [oracle output](../../repos/dotj-core/evidence/disposal-behavior-v10.0.12/oracle-output.json) records one `Dispose` call through the interface, one for normal `using`, and one when the body throws. When both body and `Dispose` throw in the sample, the observed exception is `dispose`. Two explicit `Dispose` calls invoke the sample twice; an untouched instance has zero calls. |
| Scope | This is an independent C# oracle on the installed, previously official-artifact-matched CoreLib. The upstream xUnit tests from Batch-027 were not run. Interface-wide idempotence, caller ownership, context isolation and async disposal are not established. |

### Framework implementation progress

| Framework | Completed tasks / total | Implemented before | Implemented now | Remaining | Change |
|---|---:|---:|---:|---:|---:|
| .NET runtime and base libraries (`dotj-core`) | 0 / Not yet baselined | Not yet measurable | Not yet measurable | Not yet measurable | Not yet measurable |

### Overall project progress

| Metric | Actual value |
|---|---:|
| Frameworks fully implemented and qualified | 0 / 66 (**0.00% framework qualification**) |
| Frameworks with implementation in progress | 0 |
| Frameworks with no implementation started | 66 |
| Completed implementation tasks | 0 / Not yet baselined |
| Overall implemented / remaining | **Not yet measurable / Not yet measurable** |
| Progress gained in this batch | Not yet measurable; no implementation task completed |
| Baseline version | `stage-2-2026-10-19-v1` |
| Batches completed | 28 (`Batch-001` through `Batch-028`) |
| **Batches still to do** | **At least 66**; exact total remains unbaselined and will be higher |
| Next proposed batch | `Batch-029` |

### Validation results

| Check | Result | Evidence |
|---|---|---|
| C# oracle build | PASS | `dotnet build -c Release`: 0 warnings and 0 errors. |
| C# oracle execution | PASS | `dotnet run --no-build -c Release`: eight recorded observations matched expected values. |
| Runtime identity | PASS | CoreLib SHA-256 `1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678`. |
| Upstream xUnit execution | NOT RUN | Source mapping retained; no upstream test runner invoked. |
| .j build/tests | NOT RUN | No .j source changed. |
| Designed WP-01 ownership/context fixtures | OPEN | Not exercised by this oracle. |
| Ledger | PASS | 66 frameworks and zero implementation credit retained. |

Executed `python planning/stage-2/repos/dotj-core/evidence/disposal-behavior-v10.0.12/capture.py --repo-root "C:\source\repos\dotj Frameworks"` (PASS). The [manifest](../../repos/dotj-core/evidence/disposal-behavior-v10.0.12/manifest.json) hashes source, build log and output. Token/usage measurements: unavailable.

### Files changed

| Path | Purpose |
|---|---|
| `tools/oracle/dotj-core/disposal-behavior/` | Single-purpose C# oracle and counted disposable fixture. |
| `planning/stage-2/repos/dotj-core/evidence/disposal-behavior-v10.0.12/` | Capture script, raw results and manifest. |
| `planning/stage-2/repos/dotj-core/evidence/baseline-lock.json` | Links oracle evidence. |
| `planning/stage-2/IMPLEMENTATION-STATE.md` and `IMPLEMENTATION-PROGRESS.json` | Batch-028 handoff. |
| `planning/stage-2/implementation/batches/Batch-028.md` | This report. |

Work was performed on `feature/batch-028-disposal-behavior-oracle` for merge into `master`.

### What remains

| Item | Status |
|---|---|
| Direct F01-03/F01-04 evidence and upstream test execution | OPEN. |
| N01 public Java mapping, ValueTask, WP-01 implementation and broad E01 qualification | OPEN or NOT STARTED. |

### Next proposed batch

| Field | Proposal |
|---|---|
| Batch | `Batch-029` |
| Framework / task | `dotj-core` / N01, bounded WP-01 disposal slice |
| Small outcome | Record exact-name Java representation for `System.IDisposable` and the explicit `IAsyncDisposable` blocker. |
| Prerequisites | Pinned source and binary signatures plus synchronous oracle observations. |
| Start condition | Authorized by current ten-point request. |

**STOPPED. Waiting for your CONTINUE signal before starting the next batch.**
