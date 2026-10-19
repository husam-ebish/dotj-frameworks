# Batch-003 report

### Batch summary

| Field | Result |
|---|---|
| Batch | Batch-003 |
| Status | COMPLETE (bounded E01 runtime-provenance outcome; E01 remains IN PROGRESS) |
| Framework/repository | .NET runtime and base libraries / `dotj-core` |
| Plan task IDs | E01; WP-01 and WP-02 remain downstream, NOT STARTED |
| Delivered outcome | Matched the installed .NET 10.0.12 runtime to Microsoft's published win-x64 artifact and reconciled its embedded `dotnet/dotnet` commit with the v10.0.12 `dotnet/runtime` CoreLib source tree. |

### What was implemented

No framework functionality was implemented. No public APIs, classes or methods were added or changed. No .j behavior was tested.

#### Preparation completed

- Read the official [10.0.12 release notes](https://github.com/dotnet/core/blob/main/release-notes/10.0/10.0.12/10.0.12.md) and [release metadata](https://builds.dotnet.microsoft.com/dotnet/release-metadata/10.0/releases.json). Downloaded `dotnet-runtime-10.0.12-win-x64.zip` (36,960,258 bytes); its SHA-512 `844fa99e16fd6f44e0a7c29def7a82d7846902334d6a955248a9519a4dddb3f5acceb9c9223bef69f8c83b8ae2417537e5b76dddf79fb7117dc85b5039bc1297` matches the metadata.
- ZIP CRC passed. All 189 files in the archive's `shared/Microsoft.NETCore.App/10.0.12/` directory had the same SHA-256 hashes as the corresponding installed files. This includes `.version`, `System.Private.CoreLib.dll`, and `coreclr.dll`.
- The installed and archived `.version` file gives commit `95017c711e6afc1085133d440e42b4bd78155701` and runtime 10.0.12. The commit resolves in [dotnet/dotnet](https://github.com/dotnet/dotnet/commit/95017c711e6afc1085133d440e42b4bd78155701), while the v10.0.12 source tag resolves in [dotnet/runtime](https://github.com/dotnet/runtime/commit/4271d88e0aebf3d04f188f1334c2220d80555ef6).
- The two repositories' whole runtime trees differ, but `src/runtime/src/libraries/System.Private.CoreLib` at the embedded `dotnet/dotnet` commit and `src/libraries/System.Private.CoreLib` at the runtime tag share Git tree `90aee3e6a7dc7020a668e9718155cda6a1abfb4f`. Six selected foundation blob identities also matched. This qualifies the source identity for the bounded CoreLib slice, not the whole runtime.
- Recorded the commands, hashes, comparisons and limits in `runtime-artifact-v10.0.12-win-x64.json` and linked it from `baseline-lock.json`.

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
| Overall implemented | Not yet measurable |
| Overall remaining | Not yet measurable |
| Progress gained in this batch | Not yet measurable; no implementation task completed |
| Baseline version | `stage-2-2026-10-19-v1` (task inventory; implementation-only classification pending) |

The three framework categories total 66. No framework is formally marked BLOCKED; `dotj-core` E01 remains in progress and all frameworks retain preparation/qualification gates. Artifact provenance work earns no implementation credit.

### Validation results

| Check | Result | Evidence |
|---|---|---|
| Build | NOT RUN | No application source exists; this batch changed evidence and tracking records only. |
| Relevant tests | NOT RUN | 0 .j tests executed; no implementation exists. |
| API/name compatibility | NOT RUN | E02/N01 mapping and compiled-surface comparison have not started. |
| Official artifact hash and ZIP integrity | PASS | Downloaded ZIP SHA-512 equals the official metadata value; ZIP CRC passed for 193 entries. |
| Installed runtime comparison | PASS | 189/189 runtime payload files matched installed files; zero missing or different. |
| CoreLib source identity | PASS (bounded) | Full CoreLib subtree SHA is identical at the two pinned repository commits; six selected foundation blobs also matched. Whole runtime trees differ. |
| Evidence/ledger consistency | PASS | New manifest and baseline lock parse; 66 frameworks and 1,356 unique task statuses remain NOT STARTED. |
| Reproducible source build and behavior oracle | NOT RUN | No source build or behavior fixture ran. |

### Files changed

- `planning/stage-2/repos/dotj-core/evidence/runtime-artifact-v10.0.12-win-x64.json`: artifact checksum, installed-file comparison and source-tree identities.
- `planning/stage-2/repos/dotj-core/evidence/baseline-lock.json`: verified artifact linkage and remaining E01 work.
- `planning/stage-2/IMPLEMENTATION-STATE.md` and `IMPLEMENTATION-PROGRESS.json`: Batch-003 handoff and unchanged implementation credit.
- `planning/stage-2/implementation/batches/Batch-003.md`: this report.

Work was performed on `feature/batch-003-core-runtime-provenance` for merge into `master`. Token/usage measurements: unavailable.

### What remains

- E01: review third-party notice applicability and transitive dependency rights; identify generated outputs and conditional build inputs; run and retain a pinned .NET behavior oracle.
- The whole `dotnet/dotnet` runtime subtree differs from the `dotnet/runtime` tag tree. The verified CoreLib scope must not be extrapolated to other runtime components. No reproducible source build was performed.
- E02/E03/N01 and WP-01/WP-02 remain NOT STARTED. The implementation-only backlog denominator is not yet established.

### Next proposed batch

`Batch-004`, `dotj-core`, E01: create and run a pinned .NET oracle bootstrap probe for the portable foundation, saving raw output and exact invocation flags. Prerequisites: the Batch-001 toolchain lock and Batch-003 verified runtime artifact. Do not start E02 or public implementation in that batch.

**STOPPED. Waiting for your CONTINUE signal before starting the next batch.**
