# Batch-007 report

### Batch summary

| Field | Result |
|---|---|
| Batch | Batch-007 |
| Status | COMPLETE (bounded E01 evaluation and nonstatic restore; E01 remains IN PROGRESS) |
| Framework/repository | .NET runtime and base libraries / `dotj-core` |
| Plan task IDs | E01; E02, E03, N01 and WP-01/WP-02 remain NOT STARTED |
| Delivered outcome | Evaluated the pinned CoreLib generator project under one `netstandard2.0` profile, confirmed effective Roslyn 4.14.0, and retained a 20-package restore graph with explicit static-graph and package-hash limitations. |

### What was implemented

No .j framework functionality was implemented. No public .j APIs, classes or methods were added or changed. No .j behavior was tested.

#### Preparation completed

- Reverified the v10.0.12 source ZIP SHA-256 `ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115` and extracted a temporary subset containing the original generator project, repository root and `eng` files, and relevant library props/targets. The upstream `global.json` requests SDK 10.0.110 with major roll-forward; installed SDK 10.0.401 was selected.
- Ran `dotnet msbuild` with `-getProperty:TargetFramework,MicrosoftCodeAnalysisVersion_LatestVS`, `-getItem:PackageReference`, and `-p:TargetFramework=netstandard2.0`. Evaluation exited 0 and returned property 4.14.0 and nine package references. `Microsoft.CodeAnalysis.CSharp` was 4.14.0. Imports also supplied toolset and analyzer references; the evaluated list is in [manifest.json](../../repos/dotj-core/evidence/restore-graph-v10.0.12-netstandard2.0/manifest.json).
- The repository's static-graph restore failed in this temporary subset with a `NuGet.Build.Tasks.Console.MSBuildStaticGraphRestore` null-reference error. Restore with `-p:RestoreUseStaticGraphEvaluation=false`, the pinned repository `NuGet.Config`, and a separate temporary package folder exited 0 and restored the project; a repeat exited 0 with an up-to-date result. Its `project.assets.json` targets `netstandard2.0`, lists nine direct references and 20 resolved package identities. The repeat command's stdout/stderr, assets, cache metadata and SHA-512 sidecar bytes were retained as `.raw` evidence.
- The restored `Microsoft.CodeAnalysis.CSharp/4.14.0` package file has SHA-256 `e4cce3dd791860b9300d6875eebd4d11749b5f0c166103e23a6912325828d496`, matching Batch-006's official NuGet artifact. Its actual SHA-512 is `kqS2NihVvNQHxzLePtyYiiJmFzoYO9Wm46O9DhfUgIIf5NwTbvSy66kV9EM+qAHmGpi7zQy4w8JU6DFnPlAyTA==`. The Azure-feed cache metadata and assets file instead record `568a6wcTivauIhbeWcCwfWwIn7UV7MeHEBvFB2uzGIpM2OhJ4eM/FZ8KS0yhPoNxnSpjGzz7x7CIjTxhslojQA==`. The cause is unresolved; the differing metadata is not treated as a hash of the saved package bytes.

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
| Product or upstream source build | NOT RUN | This batch evaluated and restored a temporary subset; no source compilation or .j product build occurred. |
| Relevant behavior tests | NOT RUN | 0 .j tests and 0 mapped upstream behavior fixtures executed. |
| API/name compatibility | NOT RUN | E02/N01 mapping and compiled-surface comparison have not started. |
| Pinned source archive | PASS | Recomputed ZIP SHA-256 matched Batch-002 evidence. |
| MSBuild package evaluation | PASS (one profile) | Exit 0; `netstandard2.0`, effective property 4.14.0, nine evaluated package references. |
| Static-graph restore | FAIL (temporary subset) | Exit 1; NuGet static-graph null-reference error. This is not classified as an upstream source failure. |
| Nonstatic restore | PASS (one profile) | Exit 0 with static graph disabled; assets target `netstandard2.0`, nine direct references, 20 resolved packages. |
| Roslyn package bytes | PASS | Restored package SHA-256 and ZIP contents match Batch-006's official NuGet artifact. |
| Assets/cache hash metadata | OPEN | Assets and Azure-feed metadata SHA-512 differ from the actual restored package bytes and official catalog hash. |
| Evidence/ledger consistency | PASS | Raw evidence hashes, manifest and ledger parse; 66 frameworks and 1,356 task statuses retain no implementation credit. |

### Files changed

- `planning/stage-2/repos/dotj-core/evidence/restore-graph-v10.0.12-netstandard2.0/`: manifest, byte-preserved evaluation/restore logs, assets, cache metadata and sidecar.
- `planning/stage-2/repos/dotj-core/evidence/rights-scope-v10.0.12.json` and `baseline-lock.json`: link the bounded evaluation and its unresolved hash/restore issues.
- `planning/stage-2/IMPLEMENTATION-STATE.md` and `IMPLEMENTATION-PROGRESS.json`: Batch-007 handoff and unchanged implementation credit.
- `planning/stage-2/implementation/batches/Batch-007.md`: this report.

Work was performed on `feature/batch-007-core-generator-evaluation` for merge into `master`. Token/usage measurements: unavailable.

### What remains

- Explain the static-graph restore failure under a complete pinned source checkout and the Azure-feed hash metadata discrepancy. The passing nonstatic restore does not prove every upstream build profile is reproducible.
- Resolve transitive license/notice applicability, generated outputs, and any needed wider runtime provenance. The 20-package graph is an inventory, not rights clearance.
- E02/E03/N01 and WP-01/WP-02 remain NOT STARTED. No .j implementation has begun, and the implementation-only denominator remains unbaselined.

### Next proposed batch

`Batch-008`, `dotj-core`, E01: investigate the Roslyn 4.14.0 Azure-feed metadata versus package-byte SHA-512 mismatch using a NuGet.org-only restore profile, recording whether the discrepancy is feed-specific. Prerequisites: the Batch-006 official package record and this Batch-007 restore graph. Start only after the owner's next **CONTINUE** signal.

**STOPPED. Waiting for your CONTINUE signal before starting the next batch.**
