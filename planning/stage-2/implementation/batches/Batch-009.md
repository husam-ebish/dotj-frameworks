# Batch-009 report

### Batch summary

| Field | Result |
|---|---|
| Batch | Batch-009 |
| Status | COMPLETE (bounded E01 package declaration inventory; E01 remains IN PROGRESS) |
| Framework/repository | .NET runtime and base libraries / `dotj-core` |
| Plan task IDs | E01; E02, E03, N01 and WP-01/WP-02 remain NOT STARTED |
| Delivered outcome | Inventoried license declarations and notice-like files for all 20 packages in the pinned generator restore graph. |

### What was implemented

No .j framework functionality or public API was implemented. This was preparation for source and dependency qualification.

The [inventory](../../repos/dotj-core/evidence/generator-package-rights-v10.0.12/manifest.json) records each exact package identity, nuspec SHA-256 and snapshot, license element or legacy URL, and the paths and SHA-256 values of extracted files with license/notice-like names. It snapshots 20 nuspecs and 32 such files. Fourteen nuspecs declare an MIT expression. Six have no license element and instead expose legacy license URLs; all six have license/notice-like files. `Microsoft.DotNet.CodeAnalysis/10.0.0-beta.26411.108` has an MIT expression but no extracted file with a matching notice-like name. These observations do not establish complete rights or notice applicability.

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
| Graph identity coverage | PASS | All 20 identities in the Batch-007 graph have one inventory entry and nuspec snapshot. |
| Snapshot integrity | PASS | Recomputed hashes matched 20 nuspec snapshots and 32 notice-like file snapshots. |
| Product/upstream build and behavior tests | NOT RUN | No source compilation, .j test or mapped behavior fixture in this inventory batch. |
| API/name compatibility | NOT RUN | E02/N01 not started. |
| Transitive rights clearance | OPEN | Declarations and filenames do not establish full-file applicability, redistribution scope, or legal clearance. |
| Ledger consistency | PASS | 66 frameworks and 1,356 named tasks retain zero implementation completions. |

### Files changed

- `planning/stage-2/repos/dotj-core/evidence/generator-package-rights-v10.0.12/`: reproducible inventory script, manifest, 20 nuspec snapshots and 32 notice-like snapshots.
- `planning/stage-2/repos/dotj-core/evidence/baseline-lock.json`: links the bounded inventory.
- `planning/stage-2/IMPLEMENTATION-STATE.md` and `IMPLEMENTATION-PROGRESS.json`: Batch-009 handoff and unchanged implementation credit.
- `planning/stage-2/implementation/batches/Batch-009.md`: this report.

Work was performed on `feature/batch-009-core-package-rights` for merge into `master`. Token/usage measurements: unavailable.

### What remains

- Determine rights and notice applicability to selected source, generated outputs and eventual distribution; examine files beyond filename matches and any external license references.
- Resolve static-graph restore, generated output identities, broader provenance, E02/E03/N01 and the WP-01/WP-02 implementation gates.

### Next proposed batch

`Batch-010`, `dotj-core`, E01: test static-graph restore from a complete pinned v10.0.12 source extraction and compare it with the temporary-subset failure. This is the second of the three points authorized in the owner's current message.

**STOPPED. Batch-009 complete; proceeding only under the owner's explicit three-point authorization.**
