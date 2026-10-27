# Batch-2364: Qualified native shared Char format/destination backing arrays across overlapping layouts, provider mutations and capacity boundaries; current product passed unchanged.

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; qualification remains open) |
| Framework / plan scope | dotj-core / DJ-001-N01-T2 |
| Outcome | Qualified native shared Char format/destination backing arrays across overlapping layouts, provider mutations and capacity boundaries; current product passed unchanged. |
| Validation | 379/379 foundation checks; 105000 exact outcome/holder groups, 21000 native calls and 21000 Java facade calls; byte-identical prior formatter passed all shared-array alias comparisons; full retained canonical gate, packaged consumers and API/signature audits passed. |
| Limitation | Selected managed Char-array alias layouts only; cross-element aliases, arbitrary format grammar/cultures/ABI and acceptance remain open. |
| Acceptance credit | None; no implementation task or qualification gate accepted |
| Numbered batches completed | 2,364 |
| Remaining to original 2,000 target | 0 |
| Remaining to authorized 2,500 milestone | 136 |
| Project batches planned / remaining | Unknown / unknown |
| Accepted implementation tasks | 0/1092 (0.00%) |
| Open acceptance items | 1686 |
| Qualified frameworks | 0/66 |
| Git workflow | Feature branch, merge to master after verification, then immediately push master and the completed feature branch. Actual merge/push results are reported after execution. |
| Next concrete task | Batch-2365: Align Decimal provider-before-format classification with pinned Decimal.cs; read mutable Char format backing after GetFormat and qualify literal/UTF8 error behavior. |

All temporary builds, downloads, caches, and execution logs belong under `D:\AI\Implementation\dotj Frameworks`.
