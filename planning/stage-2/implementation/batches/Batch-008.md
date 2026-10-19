# Batch-008 report

### Batch summary

| Field | Result |
|---|---|
| Batch | Batch-008 |
| Status | COMPLETE (bounded E01 NuGet hash investigation; E01 remains IN PROGRESS) |
| Framework/repository | .NET runtime and base libraries / `dotj-core` |
| Plan task IDs | E01; E02, E03, N01 and WP-01/WP-02 remain NOT STARTED |
| Delivered outcome | Tested a fresh NuGet.org-only restore and established that the Roslyn 4.14.0 content-hash versus full-file hash difference also occurs outside the Azure feed. |

### What was implemented

No .j framework functionality was implemented. No public .j APIs, classes or methods were added or changed. No .j behavior was tested.

#### Preparation completed

- Restored the pinned v10.0.12 `System.Private.CoreLib.Generators.csproj` temporary subset with a NuGet.org-only source config, a fresh package folder, `netstandard2.0`, and static graph disabled. The restore exited 1: two exact beta package versions were unavailable (`NU1603`), and `Microsoft.DotNet.CodeAnalysis` and `Microsoft.DotNet.Build.Tasks.TargetFramework` were absent (`NU1101`). Thus NuGet.org alone did not reproduce the complete generator graph.
- Restored an independent `net10.0` probe project with a single direct `Microsoft.CodeAnalysis.CSharp` 4.14.0 reference against the same NuGet.org-only config and fresh package folder. It exited 0 and resolved three packages. The Roslyn cache metadata identifies `https://api.nuget.org/v3/index.json` as its source.
- The probe's assets `sha512` and `.nupkg.metadata.contentHash` both equal `568a6wcTivauIhbeWcCwfWwIn7UV7MeHEBvFB2uzGIpM2OhJ4eM/FZ8KS0yhPoNxnSpjGzz7x7CIjTxhslojQA==`, exactly the Batch-007 Azure-feed content hash. The probe's `.nupkg.sha512` sidecar and recomputed full-file SHA-512 both equal `kqS2NihVvNQHxzLePtyYiiJmFzoYO9Wm46O9DhfUgIIf5NwTbvSy66kV9EM+qAHmGpi7zQy4w8JU6DFnPlAyTA==`. The package SHA-256 matches the Batch-006 official artifact, and its ZIP has a `.signature.p7s` entry.
- [NuGet's metadata design](https://github.com/NuGet/Home/wiki/Nupkg-Metadata-File) defines `contentHash` over package content excluding signature metadata and the sidecar over complete `.nupkg` bytes. A [NuGet maintainer explanation](https://github.com/NuGet/Home/issues/10787) confirms the hashes need not match for signed packages. This explains the observed distinction; we did not independently reimplement NuGet's content-hash algorithm. Raw commands, configs, outputs, assets and cache records are in the [probe manifest](../../repos/dotj-core/evidence/nuget-hash-probe-v4.14.0/manifest.json).

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

The three framework categories total 66. The written backlog contains 1,356 unique task IDs but mixes implementation and preparation. No framework is formally marked BLOCKED. E01 still has qualification gates.

### Validation results

| Check | Result | Evidence |
|---|---|---|
| Product or upstream source build | NOT RUN | This batch performed package restores only; no source compilation or .j product build occurred. |
| Relevant behavior tests | NOT RUN | 0 .j tests and 0 mapped upstream behavior fixtures executed. |
| API/name compatibility | NOT RUN | E02/N01 mapping and compiled-surface comparison have not started. |
| NuGet.org-only original project restore | FAIL (expected dependency availability limit) | Exit 1 with `NU1603` and `NU1101` for four unavailable dependencies. |
| NuGet.org-only isolated Roslyn restore | PASS | Exit 0, `net10.0`, three resolved packages, fresh cache metadata source `api.nuget.org`. |
| Package file integrity | PASS | Recomputed SHA-512 matches sidecar; SHA-256 matches Batch-006 official package. |
| Azure-feed-specific mismatch hypothesis | NOT SUPPORTED | NuGet.org-only cache and Batch-007 Azure cache have the same content hash and full-file hash for Roslyn 4.14.0. |
| Hash meaning | DOCUMENTED | Official NuGet design and maintainer explanation distinguish signature-excluding content hash from complete-file hash. |
| Evidence/ledger consistency | PASS | Raw evidence hashes, manifest and ledger parse; 66 frameworks and 1,356 task statuses retain no implementation credit. |

### Files changed

- `planning/stage-2/repos/dotj-core/evidence/nuget-hash-probe-v4.14.0/`: probe manifest, byte-preserved configs, project, restore logs, assets, cache metadata and sidecar.
- `planning/stage-2/repos/dotj-core/evidence/baseline-lock.json`: records the resolved interpretation and remaining E01 gates.
- `planning/stage-2/IMPLEMENTATION-STATE.md` and `IMPLEMENTATION-PROGRESS.json`: Batch-008 handoff and unchanged implementation credit.
- `planning/stage-2/implementation/batches/Batch-008.md`: this report.

Work was performed on `feature/batch-008-core-nuget-hash` for merge into `master`. Token/usage measurements: unavailable.

### What remains

- Resolve static-graph restore under a complete pinned source checkout. The temporary source subset and nonstatic restore do not establish an upstream reproducible build.
- Resolve transitive package license/notice applicability, generated outputs, and any needed wider runtime provenance. The NuGet.org-only probe does not qualify the full generator graph or transitive rights.
- E02/E03/N01 and WP-01/WP-02 remain NOT STARTED. No .j implementation has begun, and the implementation-only denominator remains unbaselined.

### Next proposed batch

`Batch-009`, `dotj-core`, E01: inventory declared license expressions and notice files for the 20 packages in the pinned generator restore graph, recording missing or ambiguous entries without claiming transitive rights clearance. Prerequisite: the Batch-007 graph and this Batch-008 hash explanation. Start only after the owner's next **CONTINUE** signal.

**STOPPED. Waiting for your CONTINUE signal before starting the next batch.**
