# Batch-2386: Implemented selected Decimal.CreateTruncating with native integer clamping and exact Decimal self-bit preservation.

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; qualification remains open) |
| Framework / plan scope | dotj-core / DJ-001-N01-T2 |
| Outcome | Implemented selected Decimal.CreateTruncating with native integer clamping and exact Decimal self-bit preservation. |
| Validation | 401/401 foundation checks; 240 exact outcome/holder groups, 110 native calls and 120 Java facade calls; 110 native calls, 120 Java calls and 240 exact result/input groups passed with two Java-only controls; full retained canonical gate, packaged consumers and API/signature audits passed. |
| Limitation | Selected integer/Decimal creation profile only; floating truncation qualification, Half identity, custom INumberBase dispatch, CLR generic constraints/ABI and acceptance remain open. |
| Acceptance credit | None; no implementation task or qualification gate accepted |
| Numbered batches completed | 2,386 |
| Remaining to original 2,000 target | 0 |
| Remaining to authorized 2,500 milestone | 114 |
| Project batches planned / remaining | Unknown / unknown |
| Accepted implementation tasks | 0/1092 (0.00%) |
| Open acceptance items | 1686 |
| Qualified frameworks | 0/66 |
| Git workflow | Feature branch, merge to master after verification, then immediately push master and the completed feature branch. Actual merge/push results are reported after execution. |
| Next concrete task | Batch-2387: Qualify Float/Double Decimal.CreateTruncating raw IEEE results, including NaN scale-one zero, exact limit clamping and retained checked/saturating behavior. |

All temporary builds, downloads, caches, and execution logs belong under `D:\AI\Implementation\dotj Frameworks`.
