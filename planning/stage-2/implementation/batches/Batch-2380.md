# Batch-2380: Implemented Decimal GetBits destination and TryGetBits managed-array bridges with exact bit copies and native short-buffer/aliased-holder semantics.

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; qualification remains open) |
| Framework / plan scope | dotj-core / DJ-001-N01-T2 |
| Outcome | Implemented Decimal GetBits destination and TryGetBits managed-array bridges with exact bit copies and native short-buffer/aliased-holder semantics. |
| Validation | 395/395 foundation checks; 3400 exact outcome/holder groups, 850 native calls and 850 Java facade calls; Decimal bit-copy bridges passed 850 native calls, 3400 groups and four explicit Java-only controls; full retained canonical gate, packaged consumers and API/signature audits passed. |
| Limitation | Managed-array projections only; typed Span<Int32> carriers, CLR by-ref ABI, generic math, complete Decimal qualification and acceptance remain open. |
| Acceptance credit | None; no implementation task or qualification gate accepted |
| Numbered batches completed | 2,380 |
| Remaining to original 2,000 target | 0 |
| Remaining to authorized 2,500 milestone | 120 |
| Project batches planned / remaining | Unknown / unknown |
| Accepted implementation tasks | 0/1092 (0.00%) |
| Open acceptance items | 1686 |
| Qualified frameworks | 0/66 |
| Git workflow | Feature branch, merge to master after verification, then immediately push master and the completed feature branch. Actual merge/push results are reported after execution. |
| Next concrete task | Batch-2381: Implement native-backed Span<Int32> carrier and Decimal bit-copy overloads, including sliced views, guarded prefixes/suffixes, overlapping output holders and invalid view bounds. |

All temporary builds, downloads, caches, and execution logs belong under `D:\AI\Implementation\dotj Frameworks`.
