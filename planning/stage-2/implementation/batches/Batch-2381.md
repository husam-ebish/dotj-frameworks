# Batch-2381: Implemented array-backed Span<Int32> views and typed Decimal GetBits/TryGetBits overloads with sliced writes and overlap-safe managed operations.

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; qualification remains open) |
| Framework / plan scope | dotj-core / DJ-001-N01-T2 |
| Outcome | Implemented array-backed Span<Int32> views and typed Decimal GetBits/TryGetBits overloads with sliced writes and overlap-safe managed operations. |
| Validation | 396/396 foundation checks; 6824 exact outcome/holder groups, 1717 native calls and 1717 Java facade calls; 1717 native calls and 6824 groups plus five Java-only controls passed for Int32 spans and Decimal bit copying; full retained canonical gate, packaged consumers and API/signature audits passed. |
| Limitation | Selected Int32 managed-array carrier only; generic span indexing, ref returns, CLR by-ref ABI, full Decimal qualification and acceptance remain open. |
| Acceptance credit | None; no implementation task or qualification gate accepted |
| Numbered batches completed | 2,381 |
| Remaining to original 2,000 target | 0 |
| Remaining to authorized 2,500 milestone | 119 |
| Project batches planned / remaining | Unknown / unknown |
| Accepted implementation tasks | 0/1092 (0.00%) |
| Open acceptance items | 1686 |
| Qualified frameworks | 0/66 |
| Git workflow | Feature branch, merge to master after verification, then immediately push master and the completed feature branch. Actual merge/push results are reported after execution. |
| Next concrete task | Batch-2382: Implement and qualify Decimal.CreateChecked for selected signed/unsigned integer carriers with native checked overflow, exact bit representation and explicit Java carrier/constraint adaptation. |

All temporary builds, downloads, caches, and execution logs belong under `D:\AI\Implementation\dotj Frameworks`.
