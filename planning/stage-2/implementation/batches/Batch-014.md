# Batch-014 report

### Batch summary

| Field | Result |
|---|---|
| Batch | Batch-014 |
| Status | COMPLETE (bounded E01 generated-source capture; E01 remains IN PROGRESS) |
| Framework/repository | .NET runtime and base libraries / `dotj-core` |
| Plan task IDs | E01; E02, E03, N01 and WP-01/WP-02 remain NOT STARTED |
| Delivered outcome | Captured eight generated CoreLib source files from the successful pinned Debug build and recorded their bytes, hashes and generator inputs. |

### What was implemented

No .j functionality or public API was implemented. The pinned upstream source was not changed. The successful `windows.x64.Debug` CoreLib build emitted eight generated files totaling 705,898 bytes: five EventSource files, one native runtime EventSource file, `ProductVersionInfo.g.cs` and `LibraryImports.g.cs`. The [evidence](../../repos/dotj-core/evidence/corelib-generated-v10.0.12/manifest.json) preserves each output byte stream and SHA-256 hash plus five generator source hashes and two generator assembly hashes. The captured product-version output says `10.0.12` and `.NET 10.0.12-dev`, which bounds it to this build context. It is not yet a release-context generated-source baseline.

### Framework implementation progress

| Framework | Completed tasks / total | Implemented before | Implemented now | Remaining | Change |
|---|---:|---:|---:|---:|---:|
| .NET runtime and base libraries (`dotj-core`) | 0 / Not yet baselined | Not yet measurable | Not yet measurable | Not yet measurable | Not yet measurable |

### Overall project progress

| Metric | Actual value |
|---|---:|
| Frameworks fully implemented and qualified | 0 / 66 |
| Frameworks with implementation in progress | 0 |
| Frameworks with no implementation started | 66 |
| Completed implementation tasks | 0 / Not yet baselined |
| Overall implemented / remaining | Not yet measurable / Not yet measurable |
| Progress gained in this batch | Not yet measurable; no implementation task completed |
| Baseline version | `stage-2-2026-10-19-v1` (implementation-only classification pending) |

The written backlog contains 1,356 unique task IDs, including preparation. No framework is formally marked BLOCKED.

### Validation results

| Check | Result | Evidence |
|---|---|---|
| CoreLib project build | PASS | Batch-013 exit 0, zero warnings/errors. |
| Generated output inventory | PASS | Eight files found under the CoreLib generated directory; bytes copied and all capture hashes verified. |
| Generator input provenance | PARTIAL | Five generator source and two assembly hashes recorded; conditional inputs and release build profile still need review. |
| Regeneration determinism | NOT RUN | One successful build capture; no clean second build comparison. |
| .j behavior and API compatibility | NOT RUN | E02/E03/N01 remain untouched. |
| Evidence and ledger | PASS | Manifest and 66-framework ledger parse; hashes verified. |

### Files changed

- `planning/stage-2/repos/dotj-core/evidence/corelib-generated-v10.0.12/`: eight raw generated files and manifest.
- `planning/stage-2/repos/dotj-core/evidence/baseline-lock.json`: records the bounded generated-source capture.
- `planning/stage-2/IMPLEMENTATION-STATE.md` and `IMPLEMENTATION-PROGRESS.json`: Batch-014 handoff with zero implementation credit.
- `planning/stage-2/implementation/batches/Batch-014.md`: this report.

Work was performed on `feature/batch-014-core-generated-sources` for merge into `master`. Token/usage measurements: unavailable.

### What remains

- Compare Debug outputs with release-context generation and establish conditional input provenance; resolve rights and notice applicability.
- Complete E02/E03/N01 and WP-01/WP-02 prerequisites before .j implementation credit.

### Next proposed batch

`Batch-015`, `dotj-core`, E01: compare captured Debug generated CoreLib source with release-context inputs and bound generated-output provenance for the selected contracts. This requires a new CONTINUE signal.

**STOPPED. Waiting for your CONTINUE signal before starting the next batch.**
