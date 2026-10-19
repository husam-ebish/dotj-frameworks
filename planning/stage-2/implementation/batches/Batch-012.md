# Batch-012 report

### Batch summary

| Field | Result |
|---|---|
| Batch | Batch-012 |
| Status | COMPLETE (bounded E01 ILLink build-path fix; E01 remains IN PROGRESS) |
| Framework/repository | .NET runtime and base libraries / `dotj-core` |
| Plan task IDs | E01; E02, E03, N01 and WP-01/WP-02 remain NOT STARTED |
| Delivered outcome | Identified the mismatched NuGet package root behind the `ILLink.Tasks` errors, built that task project cleanly, and exposed the next CoreLib build failure. |

### What was implemented

No .j functionality or public API was implemented. The upstream source was not changed. This batch established a working build invocation for one prerequisite task project.

`ILLink.Tasks.csproj` declares `PackageDownloadAndReference` items for `Microsoft.Build.Framework` and `Microsoft.Build.Utilities.Core` version `17.11.48`, and the imported target constructs reference paths under `NuGetPackageRoot`. MSBuild evaluated that property to the default user cache, where both reference DLLs were absent. The earlier restore had placed both DLLs in the isolated package folder. Passing that folder as `-p:NuGetPackageRoot=...` built `ILLink.Tasks` for `net10.0` with zero warnings and errors. The same property advanced the CoreLib build past `ILLink.Tasks` and its generator project, then stopped at a Runtime Task Host error reporting a **blank detected SDK version** below its required version 10. The [evidence](../../repos/dotj-core/evidence/illink-package-root-v10.0.12/manifest.json) preserves source target files, evaluated properties and raw build logs.

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
| ILLink property and reference paths | PASS | Evaluated `NuGetPackageRoot`, project items and imported target; checked both reference DLLs in the isolated folder and their absence from the default folder. |
| Corrected `ILLink.Tasks` build | PASS | Exit 0, zero warnings and errors, `ILLink.Tasks.dll` produced. |
| Corrected CoreLib build | PARTIAL | Earlier 60 `ILLink.Tasks` errors gone; exit 1 at Runtime Task Host SDK-version detection. |
| Actual generated source capture | NOT VERIFIED | No CoreLib generated source files established. |
| .j behavior and API compatibility | NOT RUN | E02/E03/N01 remain untouched. |
| Evidence and ledger | PASS | Raw evidence hashes, manifest and 66-framework ledger parse. |

### Files changed

- `planning/stage-2/repos/dotj-core/evidence/illink-package-root-v10.0.12/`: source snapshots, evaluation, build logs and manifest.
- `planning/stage-2/repos/dotj-core/evidence/baseline-lock.json`: records the corrected invocation and next blocker.
- `planning/stage-2/IMPLEMENTATION-STATE.md` and `IMPLEMENTATION-PROGRESS.json`: Batch-012 handoff with zero implementation credit.
- `planning/stage-2/implementation/batches/Batch-012.md`: this report.

Work was performed on `feature/batch-012-core-illink-build-path` for merge into `master`. Token/usage measurements: unavailable.

### What remains

- Diagnose the Runtime Task Host's blank SDK version and attempt actual generator output capture only after a supported CoreLib build path is established.
- Resolve rights and notice applicability, E02/E03/N01 and WP-01/WP-02 gates.

### Next proposed batch

`Batch-013`, `dotj-core`, E01: trace the Runtime Task Host SDK-version failure in the corrected CoreLib build and test a bounded invocation fix. This is the second point authorized in the owner's current message.

**STOPPED. Batch-012 complete; proceeding only under the owner's explicit three-point authorization.**
