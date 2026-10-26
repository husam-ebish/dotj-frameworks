# Batch-2252: Qualified selected UTF16 decoder NUL/surrogate replacement heap spans, carry state and protected destination windows.

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; qualification remains open) |
| Framework / plan scope | dotj-core / DJ-001-WP-05-T2 |
| Outcome | Qualified selected UTF16 decoder NUL/surrogate replacement heap spans, carry state and protected destination windows. |
| Validation | 267/267 foundation checks; 834624 groups across 119232 returned native decoder span cases and eighteen configurations; existing 98-source/API and retained consumers passed. |
| Limitation | Selected owned decoder heap spans only; replacement Convert/custom callback/pointer/byref ABI, encoder nonterminal mismatch/no-return policy, E01 and task acceptance remain open. |
| Acceptance credit | None; no implementation task or qualification gate accepted |
| Numbered batches completed | 2,252 |
| Remaining to original 2,000 target | 0 |
| Remaining to authorized 2,500 milestone | 248 |
| Project batches planned / remaining | Unknown / unknown |
| Accepted implementation tasks | 0/1092 (0.00%) |
| Open acceptance items | 1686 |
| Qualified frameworks | 0/66 |
| Git workflow | Feature branch, merge to master after verification, then immediately push master and the completed feature branch. Actual merge/push results are reported after execution. |
| Next concrete task | Batch-2253: Qualify stateless terminal encoder replacement count/write heap spans and protected views while keeping nonterminal interleavings explicitly unqualified. |

All temporary builds, downloads, caches, and execution logs belong under `D:\AI\Implementation\dotj Frameworks`.
