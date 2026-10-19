# Batch-010 report

### Batch summary

| Field | Result |
|---|---|
| Batch | Batch-010 |
| Status | COMPLETE (bounded E01 full-source restore diagnosis; E01 remains IN PROGRESS) |
| Framework/repository | .NET runtime and base libraries / `dotj-core` |
| Plan task IDs | E01; E02, E03, N01 and WP-01/WP-02 remain NOT STARTED |
| Delivered outcome | Verified a complete pinned source extraction and a passing static-graph restore; isolated the prior failure to a redundant global target-framework property in this SDK environment. |

### What was implemented

No .j framework functionality or public API was implemented. This batch qualified one upstream build prerequisite.

The v10.0.12 archive SHA-256 matched the pinned record. Windows `tar` exited 1; an archive audit using extended Windows paths repaired three missing files and verified all 60,838 file entries present. The original generator project declares `netstandard2.0` itself. In the complete extraction with installed SDK 10.0.401, static-graph restore with `-p:TargetFramework=netstandard2.0` failed with the same NuGet null reference seen in Batch-007. A forced static-graph restore **without** that redundant global property passed. A forced restore **with** it failed again. The earlier temporary subset also passed forced static-graph restore when that property was omitted. The successful full-source assets file targets `netstandard2.0`, with nine direct and 20 resolved packages. Commands, logs, extraction audit and assets are in the [manifest](../../repos/dotj-core/evidence/full-source-static-restore-v10.0.12/manifest.json).

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
| Source archive | PASS | SHA-256 matched; extraction audit found zero missing archive file entries after three repairs. |
| Full-source static restore with global TFM | FAIL | NuGet `MSBuildStaticGraphRestore` null reference, including forced rerun. |
| Full-source nonstatic restore | PASS | Exit 0 with static graph disabled. |
| Full-source static restore without global TFM | PASS | Forced restore exit 0; assets target `netstandard2.0`, nine direct and 20 resolved packages. |
| Subset static restore without global TFM | PASS | Forced restore exit 0. |
| Generator compilation / full upstream build | NOT RUN | Package restore alone does not validate compilation or runtime build reproducibility. |
| .j behavior and API compatibility | NOT RUN | E02/E03/N01 remain untouched. |
| Evidence and ledger | PASS | Raw log hashes, manifest, assets and 66-framework ledger parse. |

### Files changed

- `planning/stage-2/repos/dotj-core/evidence/full-source-static-restore-v10.0.12/`: extraction audit script and result, restore logs, assets and manifest.
- `planning/stage-2/repos/dotj-core/evidence/baseline-lock.json`: records the passing static-graph profile and remaining build limits.
- `planning/stage-2/IMPLEMENTATION-STATE.md` and `IMPLEMENTATION-PROGRESS.json`: Batch-010 handoff with zero implementation credit.
- `planning/stage-2/implementation/batches/Batch-010.md`: this report.

Work was performed on `feature/batch-010-core-full-static-restore` for merge into `master`. Token/usage measurements: unavailable.

### What remains

- Compile the generator, identify outputs and resolve rights/notice applicability to source and generated artifacts. The selected SDK differs from upstream's requested version by major roll-forward.
- Complete E02/E03/N01 and WP-01/WP-02 prerequisites before public .j implementation.

### Next proposed batch

`Batch-011`, `dotj-core`, E01: compile the pinned generator project and record generated-output identities or a bounded build blocker. This is the third point authorized in the owner's current message.

**STOPPED. Batch-010 complete; proceeding only under the owner's explicit three-point authorization.**
