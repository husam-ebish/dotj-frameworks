# Batch-401 report

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; framework remains IN PROGRESS) |
| Framework | `dotj-core` |
| Plan task | `DJ-001-N01-T2` |
| Outcome | Compile distinct internal JVM Task arity names and record unresolved .j source-level mapping. |
| Validation | JDK 21 javac and javap passed; two distinct backend class hashes recorded. |
| Limitation | Compile-only candidate; .j generic arity mapping, exact public API, behavior, and N01 acceptance remain open. |
| Public API qualification | OPEN; no fully qualified public .j facade. |

## Progress

| Metric | Actual value |
|---|---:|
| Completed implementation tasks | **0 / 1,092 (0.00%)** |
| Remaining implementation tasks | **1,092 (100.00%)** |
| Frameworks fully implemented and qualified | **0 / 66 (0.00%)** |
| In-progress / not-started frameworks | **1 / 65** |
| Batches completed / planned | **401 / 2,386 (16.81%)** (`stage-2-batches-v6`) |
| Requested 300-point series | **1 / 300 complete** (`Batch-401` through `Batch-700`) |
| Batches still to do | **1,985 planned**; revise the denominator in a new plan version when scope or batch granularity changes |
| Next proposed batch | `Batch-402`: Verify remaining pinned declared-public method metadata and owning source hashes. |
| Progress measure | Equal-weight WP and SDK integration task completions; prerequisite gates excluded; partials receive zero credit. |

## Files changed

| Path | Purpose |
|---|---|
| `tools/oracle/dotj-core/probe-task-arity-lowering.py` | Compile-only Task arity candidate, 300-point schedule, ledger tooling, and v6 plan. |
| `planning/stage-2/repos/dotj-core/evidence/task-arity-lowering-candidate-v10.0.12.json` | Compile-only Task arity candidate, 300-point schedule, ledger tooling, and v6 plan. |
| `planning/stage-2/implementation/N01-300-POINTS.json` | Compile-only Task arity candidate, 300-point schedule, ledger tooling, and v6 plan. |
| `planning/stage-2/repos/dotj-core/evidence/n01-remaining-methods-v10.0.12.json` | Compile-only Task arity candidate, 300-point schedule, ledger tooling, and v6 plan. |
| `planning/stage-2/implementation/BATCH-PLAN-v6.json` | Compile-only Task arity candidate, 300-point schedule, ledger tooling, and v6 plan. |
| `tools/progress/n01-remaining-method-ledger.py` | Compile-only Task arity candidate, 300-point schedule, ledger tooling, and v6 plan. |
| `tools/progress/verify-batch-plan.py` | Compile-only Task arity candidate, 300-point schedule, ledger tooling, and v6 plan. |
| `tools/progress/record-implementation-batch.py` | Compile-only Task arity candidate, 300-point schedule, ledger tooling, and v6 plan. |
| `planning/stage-2/IMPLEMENTATION-STATE.md` and `IMPLEMENTATION-PROGRESS.json` | Continuity and counts. |
| `planning/stage-2/implementation/batches/Batch-401.md` | This report. |

**STOPPED. Waiting for your CONTINUE signal before starting the next batch.**
