# Batch-2307: Corrected DigitShapes CompareTo boxed primitive type names and qualified scalar/target conversions, equality, hashing and wrong-domain comparisons.

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; qualification remains open) |
| Framework / plan scope | dotj-core / DJ-001-N01-T2 |
| Outcome | Corrected DigitShapes CompareTo boxed primitive type names and qualified scalar/target conversions, equality, hashing and wrong-domain comparisons. |
| Validation | 322/322 foundation checks; 2180 groups: 720 direct conversions, 1296 typed conversions, 100 comparison/equality/hash pairs, 60 domain controls and four identity checks; prior JAR fails Int16 guard text; retained DigitSubstitution consumer/API checks passed. |
| Limitation | Bounded Int32 enum conversion/domain contract only. HasFlag/span qualification follows; parsing, full enum ABI, cultures, E01 and task acceptance remain open. |
| Acceptance credit | None; no implementation task or qualification gate accepted |
| Numbered batches completed | 2,307 |
| Remaining to original 2,000 target | 0 |
| Remaining to authorized 2,500 milestone | 193 |
| Project batches planned / remaining | Unknown / unknown |
| Accepted implementation tasks | 0/1092 (0.00%) |
| Open acceptance items | 1686 |
| Qualified frameworks | 0/66 |
| Git workflow | Feature branch, merge to master after verification, then immediately push master and the completed feature branch. Actual merge/push results are reported after execution. |
| Next concrete task | Batch-2308: Qualify DigitShapes span formatting and HasFlag native bit/null/foreign-enum contracts, including short-buffer preservation. |

All temporary builds, downloads, caches, and execution logs belong under `D:\AI\Implementation\dotj Frameworks`.
