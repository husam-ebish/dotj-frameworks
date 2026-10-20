# Batch-1207 report

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; framework remains IN PROGRESS) |
| Framework | `dotj-core` |
| Plan task | `DJ-001-N01-T2` |
| Outcome | Verified four Task/ValueTask constant-argument overload pairs with eight combined Java consumer calls. |
| Validation | Pinned Task.cs and ValueTask.cs hashes and method snapshots matched; all eight lowered calls compiled; four mistyped forms were rejected. |
| Limitation | Call forms are bounded after generic arity is known; no production .j compiler, general overload resolution, behavior, or public API qualification. |
| Public API qualification | OPEN; no fully qualified public .j facade. |

## Progress

| Metric | Actual value |
|---|---:|
| Completed implementation tasks | **0 / 1,092 (0.00%)** |
| Remaining implementation tasks | **1,092 (100.00%)** |
| Frameworks fully implemented and qualified | **0 / 66 (0.00%)** |
| In-progress / not-started frameworks | **1 / 65** |
| Batches completed, total | **1,207** |
| Batches planned, total | **Unknown**; no project-wide batch baseline |
| Batches remaining, total | **Unknown**; acceptance items are not batches |
| Outstanding acceptance items | **1,686**: 330 gates + 264 naming tasks + 1,092 implementation tasks, less accepted items |
| Next proposed batch | `Batch-1208`: Characterize and lower the two Task.Run erased overload triples using functional result shapes. |
| Progress measure | Equal-weight WP and SDK integration task completions; prerequisite gates excluded; partials receive zero credit. |

## Files changed

| Path | Purpose |
|---|---|
| `tools/oracle/dotj-core/audit-constant-argument-erasure-calls.py` | Combined constant-argument overload call proof and current handoff date. |
| `tools/progress/record-implementation-batch.py` | Combined constant-argument overload call proof and current handoff date. |
| `planning/stage-2/repos/dotj-core/evidence/n01-constant-argument-erasure-calls-v10.0.12.json` | Combined constant-argument overload call proof and current handoff date. |
| `planning/stage-2/IMPLEMENTATION-STATE.md` and `IMPLEMENTATION-PROGRESS.json` | Continuity and counts. |
| `planning/stage-2/implementation/batches/Batch-1207.md` | This report. |

**This batch is complete. The current request authorizes the next batch.**

## Verification

| Check | Result |
|---|---|
| Pinned sources | `Task.cs` and `ValueTask.cs` at commit `4271d88e0aebf3d04f188f1334c2220d80555ef6` matched recorded SHA-256 values. |
| Method identity | Eight signatures and metadata snapshot hashes matched the pinned inventory and backend name map. |
| Java consumer | Eight lowered calls compiled together with `javac --release 21`; four mistyped or unsupported forms were rejected. |
| Handoff date | State updated using the Europe/Zurich date, 2026-10-21. |
| Batch plan | PASS: 1,207 sequential batches; 1,686 acceptance items open. |

This covers only call syntax with known generic arity. No public Task/ValueTask behavior is qualified.
