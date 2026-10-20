# Batch-029 report

### Batch summary

| Field | Result |
|---|---|
| Batch | Batch-029 |
| Status | COMPLETE (bounded N01 mapping; N01 remains IN PROGRESS) |
| Framework/repository | .NET runtime and base libraries / `dotj-core` |
| Plan task IDs | DJ-001-N01-T1/T2, WP-01 disposal slice |
| Delivered outcome | Recorded source/binary-backed exact-name Java candidates and the async return-type blocker. |

### What was implemented

| Item | Result |
|---|---|
| .j functionality | None; no public Java source created. |
| Preparation completed | The [N01 disposal ledger](../../repos/dotj-core/evidence/disposal-n01-v10.0.12.json) maps `System.IDisposable.Dispose(): void` to candidate package `System`, interface `IDisposable`, method `Dispose`, return `void`. `AutoCloseable.close` is an optional adapter, not the canonical name. |
| Explicit blocker | `System.IAsyncDisposable.DisposeAsync()` returns `System.Threading.Tasks.ValueTask`. Its public Java return and lifecycle remain blocked; `CompletionStage` is not substituted. |
| Contract limit | This two-interface mapping is not a compiled Java API, full N01 surface, or completed ownership behavior. |

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
| Batches completed | 29 (`Batch-001` through `Batch-029`) |
| **Batches still to do** | **At least 66**; exact total remains unbaselined and will be higher |
| Next proposed batch | `Batch-030` |

### Validation results

| Check | Result | Evidence |
|---|---|---|
| Source and binary names | PASS | Ledger entries checked against pinned source inventory and executed metadata oracle. |
| Exact-name policy | PASS for candidate spelling | Namespace, I prefixes and Dispose/DisposeAsync casing retained. |
| Compiled public Java API | NOT RUN | No public Java source created. |
| .j behavior tests | NOT RUN | No product behavior changed. |
| Full N01 gate | OPEN | Ownership fixtures, ValueTask and broader public surface remain. |
| Ledger | PASS | N01-T1/T2 IN PROGRESS; 66 frameworks and zero implementation credit retained. |

Token/usage measurements: unavailable.

### Files changed

| Path | Purpose |
|---|---|
| `planning/stage-2/repos/dotj-core/evidence/disposal-n01-v10.0.12.json` | Bounded exact-name mapping and blocker. |
| `planning/stage-2/repos/dotj-core/evidence/baseline-lock.json` | Links mapping. |
| `planning/stage-2/IMPLEMENTATION-STATE.md` and `IMPLEMENTATION-PROGRESS.json` | Marks bounded N01 work in progress. |
| `planning/stage-2/implementation/batches/Batch-029.md` | This report. |

Work was performed on `feature/batch-029-disposal-naming-ledger` for merge into `master`.

### What remains

| Item | Status |
|---|---|
| ValueTask contract, compiled public API and F01 ownership/context fixtures | OPEN. |
| Public WP-01 implementation and broad E01 qualification | NOT STARTED or OPEN. |

### Next proposed batch

| Field | Proposal |
|---|---|
| Batch | `Batch-030` |
| Framework / task | `dotj-core` / DJ-001-WP-01-T2 internal slice |
| Small outcome | Implement JDK-only owned/borrowed resource registration and deterministic close in a hidden helper, with direct executable tests. |
| Prerequisites | Ownership design exists; public facade remains gated. |
| Start condition | Authorized by current ten-point request. |

**STOPPED. Waiting for your CONTINUE signal before starting the next batch.**
