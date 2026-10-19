# Batch-013 report

### Batch summary

| Field | Result |
|---|---|
| Batch | Batch-013 |
| Status | COMPLETE (bounded E01 CoreLib build-path fix; E01 remains IN PROGRESS) |
| Framework/repository | .NET runtime and base libraries / `dotj-core` |
| Plan task IDs | E01; E02, E03, N01 and WP-01/WP-02 remain NOT STARTED |
| Delivered outcome | Diagnosed the Runtime Task Host SDK-path failure and built pinned CoreLib with zero warnings and errors. |

### What was implemented

No .j functionality or public API was implemented. The pinned upstream source was not changed. `NetCoreSdkRoot` evaluated empty, and `RuntimeIdentifierGraphPath` pointed to the repository's platform RID graph. The [MSBuild task-factory source](https://source.dot.net/Microsoft.Build/Instance/TaskFactories/AssemblyTaskFactory.cs.html) shows the .NET task host uses `NetCoreSdkRoot`, falling back to the directory of `RuntimeIdentifierGraphPath`. Passing `NETCoreSdkVersion=10.0.401` alone retained the failure. Passing the installed SDK directory as `NetCoreSdkRoot`, alongside the isolated restore's `NuGetPackageRoot`, built CoreLib successfully. The [evidence](../../repos/dotj-core/evidence/corelib-taskhost-sdk-root-v10.0.12/manifest.json) contains property evaluation, attempts, output log and output DLL hash. This proves the bounded build invocation on this machine; generated source bytes are the next verification target.

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
| Evaluated task-host properties | PASS | Empty `NetCoreSdkRoot`, repo RID graph path, SDK version 10.0.401 and host path recorded. |
| Version-only retry | FAIL | Runtime Task Host SDK-version error persisted. |
| Explicit SDK-root CoreLib build | PASS | Exit 0, zero warnings and errors; `System.Private.CoreLib.dll` produced and hashed. |
| Actual generated source capture | NOT VERIFIED | Build was run with `EmitCompilerGeneratedFiles`; generated files are to be inventoried in Batch-014. |
| .j behavior and API compatibility | NOT RUN | E02/E03/N01 remain untouched. |
| Evidence and ledger | PASS | Raw hashes, manifest and 66-framework ledger parse. |

### Files changed

- `planning/stage-2/repos/dotj-core/evidence/corelib-taskhost-sdk-root-v10.0.12/`: property evaluation, build logs and manifest.
- `planning/stage-2/repos/dotj-core/evidence/baseline-lock.json`: records the successful bounded invocation.
- `planning/stage-2/IMPLEMENTATION-STATE.md` and `IMPLEMENTATION-PROGRESS.json`: Batch-013 handoff with zero implementation credit.
- `planning/stage-2/implementation/batches/Batch-013.md`: this report.

Work was performed on `feature/batch-013-core-taskhost-sdk` for merge into `master`. Token/usage measurements: unavailable.

### What remains

- Capture actual generated source and conditional inputs; establish a reproducible full upstream build only if needed for the chosen compatibility profile.
- Resolve rights and notice applicability, E02/E03/N01 and WP-01/WP-02 gates.

### Next proposed batch

`Batch-014`, `dotj-core`, E01: capture and verify actual generated CoreLib source outputs from the successful pinned build, including inputs and stable hashes. This is the third point authorized in the owner's current message.

**STOPPED. Batch-013 complete; proceeding only under the owner's explicit three-point authorization.**
