# Batch-2290: Corrected Exception.Data duplicate key null ToString results while preserving throwing callbacks, order, aliases and exact Unicode text.

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; qualification remains open) |
| Framework / plan scope | dotj-core / DJ-001-N01-T2 |
| Outcome | Corrected Exception.Data duplicate key null ToString results while preserving throwing callbacks, order, aliases and exact Unicode text. |
| Validation | 305/305 foundation checks; 1296 comparisons across 72 native cases, normal/null/throwing object ToString, four UTF-16 text profiles and aliased keys; 40 duplicate and 32 text failures; previous JAR fails null-text witness; retained consumers/API/map passed. |
| Limitation | Selected object ToString formatting only. IFormattable dispatch, ambient cultures, reentrant formatting, serialization, complete object ABI, E01 and task acceptance remain open. |
| Acceptance credit | None; no implementation task or qualification gate accepted |
| Numbered batches completed | 2,290 |
| Remaining to original 2,000 target | 0 |
| Remaining to authorized 2,500 milestone | 210 |
| Project batches planned / remaining | Unknown / unknown |
| Accepted implementation tasks | 0/1092 (0.00%) |
| Open acceptance items | 1686 |
| Qualified frameworks | 0/66 |
| Git workflow | Feature branch, merge to master after verification, then immediately push master and the completed feature branch. Actual merge/push results are reported after execution. |
| Next concrete task | Batch-2291: Capture duplicate key IFormattable versus object ToString dispatch, null format/provider values and failures; implement the demonstrated dispatch and verify exact callbacks and text. |

All temporary builds, downloads, caches, and execution logs belong under `D:\AI\Implementation\dotj Frameworks`.
