# Batch-2365: Corrected Decimal provider-before-format span reads and selected custom numeric/scientific rendering, preserving bits, error identity and native UTF8 literal behavior.

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; qualification remains open) |
| Framework / plan scope | dotj-core / DJ-001-N01-T2 |
| Outcome | Corrected Decimal provider-before-format span reads and selected custom numeric/scientific rendering, preserving bits, error identity and native UTF8 literal behavior. |
| Validation | 380/380 foundation checks; 36400 exact outcome/holder groups, 7280 native calls and 7280 Java facade calls; Decimal provider-before-format order and exact decimal custom rendering passed native view-mutation comparisons; full retained canonical gate, packaged consumers and API/signature audits passed. |
| Limitation | Selected mutable-view pairs and single-section custom paths only; broader Decimal format grammar, sections/aliasing/cultures/ABI and acceptance remain open. |
| Acceptance credit | None; no implementation task or qualification gate accepted |
| Numbered batches completed | 2,365 |
| Remaining to original 2,000 target | 0 |
| Remaining to authorized 2,500 milestone | 135 |
| Project batches planned / remaining | Unknown / unknown |
| Accepted implementation tasks | 0/1092 (0.00%) |
| Open acceptance items | 1686 |
| Qualified frameworks | 0/66 |
| Git workflow | Feature branch, merge to master after verification, then immediately push master and the completed feature branch. Actual merge/push results are reported after execution. |
| Next concrete task | Batch-2366: Qualify Decimal format precision/NUL/provider order and Char/UTF8 literal boundaries across ToString and array/span formatting, extending exact native evidence. |

All temporary builds, downloads, caches, and execution logs belong under `D:\AI\Implementation\dotj Frameworks`.
