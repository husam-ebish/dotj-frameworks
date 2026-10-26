# Batch-2260: Qualified selected stateless UTF16 decoder replacement TryGetChars count-based capacity decisions, written carriers and protected views.

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; qualification remains open) |
| Framework / plan scope | dotj-core / DJ-001-WP-05-T2 |
| Outcome | Qualified selected stateless UTF16 decoder replacement TryGetChars count-based capacity decisions, written carriers and protected views. |
| Validation | 275/275 foundation checks; 29808 groups across 9936 native calls, including 2486 false capacity returns and 26 recursive-fallback failures; existing 98-source/API and retained consumers passed. |
| Limitation | Selected stateless decoder TryGetChars heap spans only; arbitrary callbacks, full pointer/byref ABI, encoder nonterminal mismatch/no-return policy, E01 and task acceptance remain open. |
| Acceptance credit | None; no implementation task or qualification gate accepted |
| Numbered batches completed | 2,260 |
| Remaining to original 2,000 target | 0 |
| Remaining to authorized 2,500 milestone | 240 |
| Project batches planned / remaining | Unknown / unknown |
| Accepted implementation tasks | 0/1092 (0.00%) |
| Open acceptance items | 1686 |
| Qualified frameworks | 0/66 |
| Git workflow | Feature branch, merge to master after verification, then immediately push master and the completed feature branch. Actual merge/push results are reported after execution. |
| Next concrete task | Batch-2261: Correct the nonterminal encoder residual-fallback mismatch and compare every returned encoder case in the completed bounded reference corpus; retain native no-return rows as unqualified. |

All temporary builds, downloads, caches, and execution logs belong under `D:\AI\Implementation\dotj Frameworks`.
