# Batch-2291: Corrected Exception.Data duplicate key IFormattable dispatch with native null format/provider and exact callback text.

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; qualification remains open) |
| Framework / plan scope | dotj-core / DJ-001-N01-T2 |
| Outcome | Corrected Exception.Data duplicate key IFormattable dispatch with native null format/provider and exact callback text. |
| Validation | 306/306 foundation checks; 5184 comparisons across 288 native object/IFormattable combinations, normal/null/throwing text, aliases and four UTF-16 profiles; null format/provider and callback order matched; previous JAR fails dispatch witness; retained consumers/API/map passed. |
| Limitation | Selected invariant-culture object/IFormattable formatting only. Other cultures, reentrant formatting, complete boxed object ABI, serialization, E01 and task acceptance remain open. |
| Acceptance credit | None; no implementation task or qualification gate accepted |
| Numbered batches completed | 2,291 |
| Remaining to original 2,000 target | 0 |
| Remaining to authorized 2,500 milestone | 209 |
| Project batches planned / remaining | Unknown / unknown |
| Accepted implementation tasks | 0/1092 (0.00%) |
| Open acceptance items | 1686 |
| Qualified frameworks | 0/66 |
| Git workflow | Feature branch, merge to master after verification, then immediately push master and the completed feature branch. Actual merge/push results are reported after execution. |
| Next concrete task | Batch-2292: Capture once-only duplicate-key text callbacks that mutate the dictionary, then compare diagnostics, callback order, stored/view counts, reachable entries and enumerator state. |

All temporary builds, downloads, caches, and execution logs belong under `D:\AI\Implementation\dotj Frameworks`.
