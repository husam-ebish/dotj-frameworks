# Batch-1206 report

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; framework remains IN PROGRESS) |
| Framework | `dotj-core` |
| Plan task | `DJ-001-N01-T2` |
| Outcome | Compiled two exact-name Task.FromException source-call forms after deterministic backend lowering. |
| Validation | Pinned Task.cs and metadata hashes matched; plain and explicit-generic calls compiled against mapped Java methods; three unsupported forms were rejected. |
| Limitation | This is a bounded syntax proof after method generic arity is known; no .j compiler, general overload resolution, behavior, or public API qualification. |
| Public API qualification | OPEN; no fully qualified public .j facade. |

## Progress

| Metric | Actual value |
|---|---:|
| Completed implementation tasks | **0 / 1,092 (0.00%)** |
| Remaining implementation tasks | **1,092 (100.00%)** |
| Frameworks fully implemented and qualified | **0 / 66 (0.00%)** |
| In-progress / not-started frameworks | **1 / 65** |
| Batches completed, total | **1,206** |
| Batches planned, total | **Unknown**; no project-wide batch baseline |
| Batches remaining, total | **Unknown**; acceptance items are not batches |
| Outstanding acceptance items | **1,686**: 330 gates + 264 naming tasks + 1,092 implementation tasks, less accepted items |
| Next proposed batch | `Batch-1207`: Check the ValueTask.FromException pair with the same source-call lowering rule. |
| Progress measure | Equal-weight WP and SDK integration task completions; prerequisite gates excluded; partials receive zero credit. |

## Files changed

| Path | Purpose |
|---|---|
| `tools/oracle/dotj-core/audit-task-fromexception-call-lowering.py` | Task.FromException call-lowering syntax proof. |
| `planning/stage-2/repos/dotj-core/evidence/n01-task-fromexception-call-lowering-v10.0.12.json` | Task.FromException call-lowering syntax proof. |
| `planning/stage-2/IMPLEMENTATION-STATE.md` and `IMPLEMENTATION-PROGRESS.json` | Continuity and counts. |
| `planning/stage-2/implementation/batches/Batch-1206.md` | This report. |

**This batch is complete. The current request authorizes the next batch.**

## Verification

| Check | Result |
|---|---|
| Pinned source and metadata | Task.cs at commit `4271d88e0aebf3d04f188f1334c2220d80555ef6` and the Task API snapshot matched recorded SHA-256 values. |
| Call lowering | Plain and explicit-generic `Task.FromException` calls selected distinct deterministic backend names. |
| Java consumer | Both lowered calls compiled with `javac --release 21`; three unsupported call forms were rejected by the bounded parser. |
| Batch plan | PASS: 1,206 sequential batches; 1,686 acceptance items open. |

This proves only the two declared call shapes. A complete `.j` parser, overload resolver, and Task semantics remain open.
