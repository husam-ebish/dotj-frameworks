# Batch-017 report

### Batch summary

| Field | Result |
|---|---|
| Batch | Batch-017 |
| Status | COMPLETE (bounded E01 generated-import attribution; E01 remains IN PROGRESS) |
| Framework/repository | .NET runtime and base libraries / `dotj-core` |
| Plan task IDs | E01; E02, E03, N01 and WP-01/WP-02 remain NOT STARTED |
| Delivered outcome | Mapped the five Debug/Release `LibraryImports.g.cs` diff hunks to pinned source conditions and evaluated build properties. |

### What was implemented

No .j functionality or public API was implemented. The upstream source was not changed. The [attribution record](../../repos/dotj-core/evidence/corelib-conditional-imports-v10.0.12/manifest.json) retains six pinned source snapshots, their hashes, Debug/Release property evaluations and a member-by-member map of the generated diff. Six generated methods are absent from the Release output: `GCHandle.InternalGetBridgeWait` and four `JavaMarshal` imports follow `FEATURE_JAVAMARSHAL`/`FeatureJavaMarshal`; `Marshal.GetIsInCooperativeGCModeFunctionPointer` follows `DEBUG`. Two Windows imports, `FindNLSStringEx` and `FindStringOrdinal`, change generated code because `SetLastErrorForDebug` evaluates true under `DEBUG` and false otherwise. This accounts for all five observed diff hunks. It does not establish that any public API or runtime behavior is compatible with .j.

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

The written backlog has 1,356 named task IDs mixing preparation and implementation. No framework is formally marked BLOCKED.

### Validation results

| Check | Result | Evidence |
|---|---|---|
| Generated diff accounting | PASS | Five hunks, 4 added and 114 removed lines; all affected methods mapped. |
| Pinned source and evaluated properties | PASS | Six source snapshots and both property evaluations retained; hashes checked. |
| .j behavior and API compatibility | NOT RUN | E02/E03/N01 remain untouched. |
| Rights and notice clearance | NOT RUN | Applicability to generated output and transitive dependencies remains open. |
| Evidence and ledger | PASS | Manifest and 66-framework ledger parse. |

### Files changed

- `planning/stage-2/repos/dotj-core/evidence/corelib-conditional-imports-v10.0.12/`: pinned source snapshots, property evaluations and attribution manifest.
- `planning/stage-2/repos/dotj-core/evidence/baseline-lock.json`: scoped conditional-generation evidence.
- `planning/stage-2/IMPLEMENTATION-STATE.md` and `IMPLEMENTATION-PROGRESS.json`: Batch-017 handoff with zero implementation credit.
- `planning/stage-2/implementation/batches/Batch-017.md`: this report.

Work was performed on `feature/batch-017-core-conditional-imports` for merge into `master`. Token/usage measurements: unavailable.

### What remains

- Resolve generated-output and transitive license/notice applicability, independent build reproducibility, and official release-artifact provenance.
- Complete E02/E03/N01 and WP-01/WP-02 prerequisites before .j implementation credit.

### Next proposed batch

`Batch-018`, `dotj-core`, E01: map license and notice provenance for the eight captured generated output families and their direct generator sources. This requires a new CONTINUE signal.

**STOPPED. Waiting for your CONTINUE signal before starting the next batch.**
