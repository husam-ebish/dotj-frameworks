# Batch-1201 report

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; framework remains IN PROGRESS) |
| Framework | `dotj-core` |
| Plan task | `DJ-001-N01-T2` |
| Outcome | Corrected four N01 Java syntax probes that incorrectly used primitive Boolean or Int32 as generic arguments. |
| Validation | Four boxed exact-name declarations now compile; the full 327-method ledger replay passed and the combined audit records 422 compiled, three static-generic blockers, and one optional-parameter probe limitation. |
| Limitation | Boxing is a syntax feasibility adaptation only; generic value semantics, combined overloads, and public behavior remain unqualified. |
| Public API qualification | OPEN; no fully qualified public .j facade. |

## Progress

| Metric | Actual value |
|---|---:|
| Completed implementation tasks | **0 / 1,092 (0.00%)** |
| Remaining implementation tasks | **1,092 (100.00%)** |
| Frameworks fully implemented and qualified | **0 / 66 (0.00%)** |
| In-progress / not-started frameworks | **1 / 65** |
| Batches completed, total | **1,201** |
| Batches planned, total | **Unknown**; no project-wide batch baseline |
| Batches remaining, total | **Unknown**; acceptance items are not batches |
| Outstanding acceptance items | **1,686**: 330 gates + 264 naming tasks + 1,092 implementation tasks, less accepted items |
| Next proposed batch | `Batch-1202`: Investigate the two static ValueTask<TResult> equality operator blockers without changing their pinned public identities. |
| Progress measure | Equal-weight WP and SDK integration task completions; prerequisite gates excluded; partials receive zero credit. |

## Files changed

| Path | Purpose |
|---|---|
| `tools/oracle/dotj-core/verify-selected-method-java-declarations.py` | Generic-argument syntax probe correction and full ledger replay. |
| `tools/oracle/dotj-core/repair-generic-primitive-probes.py` | Generic-argument syntax probe correction and full ledger replay. |
| `tools/oracle/dotj-core/audit-java-declaration-ledgers.py` | Generic-argument syntax probe correction and full ledger replay. |
| `tools/progress/record-implementation-batch.py` | Generic-argument syntax probe correction and full ledger replay. |
| `tools/progress/verify-batch-plan.py` | Generic-argument syntax probe correction and full ledger replay. |
| `planning/stage-2/repos/dotj-core/evidence/n01-remaining-java-declarations-v10.0.12.json` | Generic-argument syntax probe correction and full ledger replay. |
| `planning/stage-2/repos/dotj-core/evidence/n01-generic-primitive-probe-revision-v10.0.12.json` | Generic-argument syntax probe correction and full ledger replay. |
| `planning/stage-2/repos/dotj-core/evidence/n01-java-declaration-audit-v10.0.12.json` | Generic-argument syntax probe correction and full ledger replay. |
| `planning/stage-2/repos/dotj-core/evidence/n01-java-erasure-outcomes-v10.0.12.json` | Generic-argument syntax probe correction and full ledger replay. |
| `planning/stage-2/IMPLEMENTATION-STATE.md` and `IMPLEMENTATION-PROGRESS.json` | Continuity and counts. |
| `planning/stage-2/implementation/batches/Batch-1201.md` | This report. |

**This batch is complete. The current request authorizes the next batch.**

## Verification

| Check | Result |
|---|---|
| Pinned source and metadata | PASS for remaining-method indices 217, 218, 219, and 293. |
| Corrected Java generic arguments | PASS: exact-name `System.Boolean` and `System.Int32` temporary reference types compiled where primitive generic arguments failed. |
| Full remaining-method replay | PASS: 327/327 source hashes, metadata hashes, declarations, and compiler/probe outcomes reproduced. |
| Combined audit | 426 records: 422 individually compile, three static-generic declarations blocked, one optional-parameter probe limitation. |
| Batch plan | PASS: 1,201 sequential batches; 1,686 acceptance items open. |

The revision evidence retains the four historical compiler failures. This change does not implement boxed .NET value semantics or a public facade.
