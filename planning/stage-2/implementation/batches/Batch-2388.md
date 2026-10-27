# Batch-2388: Implemented selected Char/Byte/Int32 Span indexed value reads and assignments with exact bounds failures and shared-array writes.

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; qualification remains open) |
| Framework / plan scope | dotj-core / DJ-001-N01-T2 |
| Outcome | Implemented selected Char/Byte/Int32 Span indexed value reads and assignments with exact bounds failures and shared-array writes. |
| Validation | 403/403 foundation checks; 1320 exact outcome/holder groups, 660 native calls and 660 Java facade calls; 660 native/Java calls, 1320 exact outcome/backing-array groups and five Java-only carrier controls passed; full retained canonical gate, packaged consumers and API/signature audits passed. |
| Limitation | Value getter and explicit assignment projections only; native ref returns, generic span indexing beyond selected carriers, CLR byref ABI and acceptance remain open. |
| Acceptance credit | None; no implementation task or qualification gate accepted |
| Numbered batches completed | 2,388 |
| Remaining to original 2,000 target | 0 |
| Remaining to authorized 2,500 milestone | 112 |
| Project batches planned / remaining | Unknown / unknown |
| Accepted implementation tasks | 0/1092 (0.00%) |
| Open acceptance items | 1686 |
| Qualified frameworks | 0/66 |
| Git workflow | Feature branch, merge to master after verification, then immediately push master and the completed feature branch. Actual merge/push results are reported after execution. |
| Next concrete task | Batch-2389: Implement and qualify Char/Byte ReadOnlySpan indexed value reads, including primitive/boxed Byte bridges, empty/sliced bounds and visibility of external backing-array mutations. |

All temporary builds, downloads, caches, and execution logs belong under `D:\AI\Implementation\dotj Frameworks`.
