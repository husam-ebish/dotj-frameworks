# Batch-006 report

### Batch summary

| Field | Result |
|---|---|
| Batch | Batch-006 |
| Status | COMPLETE (bounded direct E01 package evidence; E01 remains IN PROGRESS) |
| Framework/repository | .NET runtime and base libraries / `dotj-core` |
| Plan task IDs | E01; E02, E03, N01 and WP-01/WP-02 remain NOT STARTED |
| Delivered outcome | Resolved the generator project's declared Roslyn package property to 4.14.0 at the pinned source commit, verified that NuGet artifact against the official catalog, and retained its direct license and notice metadata. |

### What was implemented

No .j framework functionality was implemented. No public .j APIs, classes or methods were added or changed. No .j behavior was tested.

#### Preparation completed

- The pinned [generator project](https://github.com/dotnet/runtime/blob/4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/gen/System.Private.CoreLib.Generators.csproj) requests `Microsoft.CodeAnalysis.CSharp` with version `$(MicrosoftCodeAnalysisVersion_LatestVS)` and `PrivateAssets="all"`. At the same source commit, [eng/Versions.props](https://github.com/dotnet/runtime/blob/4271d88e0aebf3d04f188f1334c2220d80555ef6/eng/Versions.props) line 72 sets that property to `4.14.0`; its SHA-256 is recorded. A separate `eng/Version.Details.xml` entry names a 5.0 prerelease Roslyn dependency, but it is not the generator project's direct version expression. Effective MSBuild evaluation has not been run.
- Downloaded the [Microsoft.CodeAnalysis.CSharp 4.14.0 NuGet package](https://www.nuget.org/packages/Microsoft.CodeAnalysis.CSharp/4.14.0) through NuGet's package endpoint. Its 17,342,224 bytes have SHA-256 `e4cce3dd791860b9300d6875eebd4d11749b5f0c166103e23a6912325828d496`; computed SHA-512 matches the [official NuGet catalog entry](https://api.nuget.org/v3/catalog0/data/2025.05.15.18.34.12/microsoft.codeanalysis.csharp.4.14.0.json). ZIP CRC passed for 55 members.
- Retained the package's unmodified `.nuspec` and `ThirdPartyNotices.rtf` with raw-byte preservation. The nuspec identifies version 4.14.0, declares license expression `MIT`, and points to Roslyn commit `8edf7bcd4f1594c3d68a6a567469f41dbd33dd1b`. It declares ten direct dependencies in the `.NETStandard2.0` group. The package contains the RTF notice; it does not embed a separate license file. Exact hashes and retrieval details are in [manifest.json](../../repos/dotj-core/evidence/roslyn-package-v4.14.0/manifest.json).
- Updated the [rights-scope record](../../repos/dotj-core/evidence/rights-scope-v10.0.12.json) and baseline lock to distinguish the declared package evidence from an evaluated upstream build and transitive rights closure. No upstream package was added to a .j product.

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

The three framework categories total 66. The written backlog contains 1,356 unique task IDs but mixes implementation and preparation, so it is not an implementation-only denominator. No framework is formally marked BLOCKED. E01 qualification gates remain open.

### Validation results

| Check | Result | Evidence |
|---|---|---|
| Build | NOT RUN | No .j or upstream generator build was attempted; this batch recorded source and package evidence. |
| Relevant tests | NOT RUN | 0 .j tests and 0 mapped upstream behavior fixtures executed. |
| API/name compatibility | NOT RUN | E02/N01 mapping and compiled-surface comparison have not started. |
| Source property and declaration | PASS (declared value) | Pinned generator project SHA-256 matched Batch-002; pinned `eng/Versions.props` line 72 states 4.14.0. Effective imported property value was not evaluated. |
| Package identity/integrity | PASS | Official NuGet catalog SHA-512 matched downloaded package; ZIP CRC passed for 55 members; nuspec ID/version matched 4.14.0. |
| Direct package license/notice | PASS (inventory) | Nuspec declares MIT and embeds `ThirdPartyNotices.rtf`; both retained with SHA-256 evidence. No legal or redistribution clearance is asserted. |
| Dependency closure | NOT RUN | Ten `.NETStandard2.0` direct dependency declarations were counted; restore, transitive packages and rights were not evaluated. |
| Evidence/ledger consistency | PASS | Manifest, lock and progress JSON parse; 66 frameworks and 1,356 unique task statuses retain no implementation credit. |

### Files changed

- `planning/stage-2/repos/dotj-core/evidence/roslyn-package-v4.14.0/.gitattributes`, `manifest.json`, `Microsoft.CodeAnalysis.CSharp.nuspec`, and `ThirdPartyNotices.rtf`: direct package integrity and preserved metadata/notice evidence.
- `planning/stage-2/repos/dotj-core/evidence/rights-scope-v10.0.12.json` and `baseline-lock.json`: link the package evidence while retaining open gates.
- `planning/stage-2/IMPLEMENTATION-STATE.md` and `IMPLEMENTATION-PROGRESS.json`: Batch-006 handoff and unchanged implementation credit.
- `planning/stage-2/implementation/batches/Batch-006.md`: this report.

Work was performed on `feature/batch-006-core-generator-package` for merge into `master`. Token/usage measurements: unavailable.

### What remains

- Evaluate the effective generator project imports, property overrides and restore graph under a controlled build profile. A source property value alone does not prove the package selected in every configuration.
- Resolve direct and transitive dependency rights, generated output identities, file-to-notice applicability and any broader runtime provenance. The direct MIT expression and notice do not establish release eligibility.
- E02/E03/N01 and WP-01/WP-02 remain NOT STARTED. No .j implementation has begun, and the implementation-only backlog denominator is not established.

### Next proposed batch

`Batch-007`, `dotj-core`, E01: evaluate the pinned CoreLib generator project's effective package version and direct restore graph under one controlled `netstandard2.0` build profile, recording any property override or restore limitation. Prerequisites: the Batch-002 source pin and this Batch-006 package record. Start only after the owner's next **CONTINUE** signal.

**STOPPED. Waiting for your CONTINUE signal before starting the next batch.**
