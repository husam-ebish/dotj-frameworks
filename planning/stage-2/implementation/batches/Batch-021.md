# Batch-021 report

### Batch summary

| Field | Result |
|---|---|
| Batch | Batch-021 |
| Status | COMPLETE (bounded E01 static emission trace; E01 remains IN PROGRESS) |
| Framework/repository | .NET runtime and base libraries / `dotj-core` |
| Plan task IDs | E01; E02, E03, N01 and WP-01/WP-02 remain NOT STARTED |
| Delivered outcome | Traced two selected `LibraryImports.g.cs` stubs to pinned CoreLib declarations and generator source paths, with hashed excerpts and explicit limits. |

### What was implemented

| Item | Result |
|---|---|
| .j public APIs or behavior | None; no .j implementation source changed. |
| Preparation completed | The [emission trace manifest](../../repos/dotj-core/evidence/libraryimport-emission-trace-v10.0.12/manifest.json) retains 14 exact source line windows from nine pinned files and two windows from the 645,008-byte generated output. All nine source files have .NET Foundation MIT headers; the [pinned root MIT license](https://github.com/dotnet/runtime/blob/v10.0.12/LICENSE.TXT) remains a rights-review input. |
| Forwarder sample | `Internal.VersionResilientHashCode.TypeHashCode`: the pinned `[LibraryImport]` declaration and its QCall entry point correspond to the emitted extern `DllImport` stub. The emitted form matches `PrintForwarderStub`; the static trace cannot establish which forwarder branch ran. |
| Marshalling sample | `System.Array.InternalCreate`: `[MarshalAs(UnmanagedType.Bool)] bool fromArrayType` corresponds to the emitted `int` temporary, `(fromArrayType ? 1 : 0)` assignment and local `DllImport`. The pinned resolver, `WinBoolMarshaller`, statement composer and generator body construction account for this form. |
| Content classification | The selected output uses names, types and entry points from source declarations and C# syntax constructed by the generator. Neither excerpt has an inline notice marker. This is a static two-stub observation, not a determination of copyrighted expression, package notice applicability or the remaining generated file. |

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
| Baseline version | `stage-2-2026-10-19-v1` (implementation-only task classification pending) |
| Batches completed | 21 (`Batch-001` through `Batch-021`) |
| **Batches still to do** | **At least 66** to address the 66 unqualified frameworks; exact total remains unbaselined and will be higher |
| Next proposed batch | `Batch-022` |

The written backlog has 1,356 named IDs mixing preparation and implementation. The 0.00% qualified-framework measure is separate from the overall implementation percentage. No framework is formally marked BLOCKED.

### Validation results

| Check | Result | Evidence |
|---|---|---|
| .j build and tests | NOT RUN | No .j source exists or changed in this batch. |
| Upstream generator build | NOT RUN | Existing bounded build evidence retained; this batch performed static source/output tracing. |
| API/name compatibility | NOT RUN | E02/E03/N01 remain open. |
| Pinned output identity | PASS | Generated file SHA-256 matches the prior CoreLib evidence; two excerpts preserve exact line bytes. |
| Source identity and excerpts | PASS | Nine full source hashes and 14 excerpt hashes recorded; all nine files carry the observed MIT header. |
| Trace anchors | PASS | Eight source/output checks cover two declarations, output forms, forwarder construction, Boolean marshalling, concatenation and absent inline notice markers in the selected excerpts. |
| Rights or file-to-notice clearance | OPEN | Static sample is narrow and does not establish legal notice applicability or future .j artifact contents. |
| Ledger and evidence integrity | PASS | Manifest and 66-framework ledger parse; no implementation credit added. |

Executed capture: `python planning/stage-2/repos/dotj-core/evidence/libraryimport-emission-trace-v10.0.12/capture.py --repo-root "C:\source\repos\dotj Frameworks" --source-root "C:\Users\husam\AppData\Local\Temp\dotj-batch-010-full-source\runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6"` (PASS). The check captured 14 source and two output windows and passed eight anchors. `git diff --cached --check` and independent snapshot/ledger checks passed.

### Files changed

| Path | Purpose |
|---|---|
| `planning/stage-2/repos/dotj-core/evidence/libraryimport-emission-trace-v10.0.12/` | Capture script, exact source/output excerpts and trace manifest. |
| `planning/stage-2/repos/dotj-core/evidence/baseline-lock.json` | Adds bounded trace evidence to the E01 record. |
| `planning/stage-2/IMPLEMENTATION-STATE.md` and `IMPLEMENTATION-PROGRESS.json` | Batch-021 handoff with zero implementation credit and explicit remaining-batch lower bound. |
| `planning/stage-2/implementation/batches/Batch-021.md` | This report. |

Work was performed on `feature/batch-021-libraryimport-emission-trace` for merge into `master`. Token/usage measurements: unavailable.

### What remains

| Item | Status |
|---|---|
| Other generated stubs, non-C# resources and possible template sources | OPEN; only two stubs were traced. |
| File-level notices, package rights and future .j artifact composition | OPEN; no redistribution clearance claimed. |
| Independent/official release build provenance and E02/E03/N01, WP-01/WP-02 | OPEN or NOT STARTED as recorded in the state. |

### Next proposed batch

| Field | Proposal |
|---|---|
| Batch | `Batch-022` |
| Framework / task | `dotj-core` / E01 |
| Small outcome | Inventory non-C# resources and emitted template sources in the two-project LibraryImport generator build for possible copied-content provenance. |
| Prerequisites | Pinned v10.0.12 source, two-project restore graph and generated output already captured. |
| Start condition | New CONTINUE signal required. |

**STOPPED. Waiting for your CONTINUE signal before starting the next batch.**
