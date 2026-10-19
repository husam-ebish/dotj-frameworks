# Batch-005 report

### Batch summary

| Field | Result |
|---|---|
| Batch | Batch-005 |
| Status | COMPLETE (bounded E01 header and direct-input review; E01 remains IN PROGRESS) |
| Framework/repository | .NET runtime and base libraries / `dotj-core` |
| Plan task IDs | E01; E02, E03, N01 and WP-01/WP-02 remain NOT STARTED |
| Delivered outcome | Verified license headers and hashes for five selected CoreLib contracts and nine direct generator source inputs, recorded root license/notices and the unresolved Roslyn package and notice mapping. |

### What was implemented

No .j framework functionality was implemented. No public .j APIs, classes or methods were added or changed. No .j behavior was tested.

#### Preparation completed

- Reviewed the [pinned .NET runtime license](https://github.com/dotnet/runtime/blob/4271d88e0aebf3d04f188f1334c2220d80555ef6/LICENSE.TXT) and [third-party notices](https://github.com/dotnet/runtime/blob/4271d88e0aebf3d04f188f1334c2220d80555ef6/THIRD-PARTY-NOTICES.TXT). The root license is MIT and states a copyright and permission notice retention condition. The notices contain 46 named sections, but the repository-wide file does not establish which section applies to a selected source file or future .j artifact.
- Retrieved the five selected foundation `.cs` files and six generator `.cs` files at immutable commit `4271d88e0aebf3d04f188f1334c2220d80555ef6`; all eleven matched their earlier pinned SHA-256 values. The generator project also directly links three shared CoreLib `.cs` files outside `gen`; their hashes were recorded. All fourteen reviewed `.cs` files begin with the .NET Foundation MIT header. The project XML has no per-file license header.
- The [generator project](https://github.com/dotnet/runtime/blob/4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/gen/System.Private.CoreLib.Generators.csproj) declares six local and three linked compile inputs plus `Microsoft.CodeAnalysis.CSharp` with `PrivateAssets="all"` and a version expression. The [CoreLib project](https://github.com/dotnet/runtime/blob/4271d88e0aebf3d04f188f1334c2220d80555ef6/src/coreclr/System.Private.CoreLib/System.Private.CoreLib.csproj) references that generator as an analyzer. The package version, artifact hash, direct license and transitive inputs were not resolved in this batch. `PrivateAssets` does not itself settle reuse or redistribution obligations.
- Saved exact paths, hashes, observations and open decisions in [rights-scope-v10.0.12.json](../../repos/dotj-core/evidence/rights-scope-v10.0.12.json). No upstream implementation source was copied into the .j product. The record makes no legal clearance or release-eligibility claim.

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

The three framework categories total 66. The written backlog contains 1,356 unique task IDs but mixes implementation and preparation, so it is not an implementation-only denominator. No framework is formally marked BLOCKED. The outstanding E01 rights and qualification gates remain visible.

### Validation results

| Check | Result | Evidence |
|---|---|---|
| Build | NOT RUN | This batch changed evidence and tracking records only; no product or upstream source build was attempted. |
| Relevant tests | NOT RUN | 0 .j tests and 0 upstream behavior fixtures executed. |
| API/name compatibility | NOT RUN | E02/N01 mapping and compiled-surface comparison have not started. |
| Source identity and headers | PASS (bounded) | 11 previously inventoried C# source hashes matched the pinned manifest; three newly identified linked C# files were hashed; all 14 displayed the two-line .NET Foundation MIT header. Generator project hash matched the pinned manifest. |
| Root license and notices | PASS (file integrity only) | Retained root license and notice SHA-256 values matched `source-archive-v10.0.12.json`; 46 notice headings counted. File-to-notice applicability remains OPEN. |
| Generator dependency rights | OPEN | `Microsoft.CodeAnalysis.CSharp` version expression and `PrivateAssets="all"` recorded; package artifact, license, transitives and generated outputs unresolved. |
| Evidence/ledger consistency | PASS | Evidence, lock and progress JSON parse; 66 frameworks and 1,356 unique task statuses have no implementation credit. |

### Files changed

- `planning/stage-2/repos/dotj-core/evidence/rights-scope-v10.0.12.json`: selected file/header, license/notice and direct generator-input record.
- `planning/stage-2/repos/dotj-core/evidence/source-archive-v10.0.12.json` and `baseline-lock.json`: link the bounded rights record and retain open E01 gates.
- `planning/stage-2/IMPLEMENTATION-STATE.md` and `IMPLEMENTATION-PROGRESS.json`: Batch-005 handoff with unchanged implementation credit.
- `planning/stage-2/implementation/batches/Batch-005.md`: this report.

Work was performed on `feature/batch-005-core-rights-scope` for merge into `master`. Token/usage measurements: unavailable.

### What remains

- Map applicable third-party notices to selected source and generated outputs; resolve the generator package version, artifact hash, direct license, transitive dependencies and conditional build inputs. A licensing reviewer remains the decision owner where required. No release or source-reuse eligibility is asserted.
- E01 also retains generated-output identities and any needed broader runtime provenance. E02/E03/N01 and WP-01/WP-02 remain NOT STARTED; the mapped behavior oracle has not run.
- No .j implementation has begun, and the implementation-only backlog denominator is not established.

### Next proposed batch

`Batch-006`, `dotj-core`, E01: resolve the pinned generator project's `Microsoft.CodeAnalysis.CSharp` package version and artifact identity, then record its direct license and notice evidence without claiming transitive closure. Prerequisites: the Batch-002 source archive and this Batch-005 direct-input record. Start only after the owner's next **CONTINUE** signal.

**STOPPED. Waiting for your CONTINUE signal before starting the next batch.**
