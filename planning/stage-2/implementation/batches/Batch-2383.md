# Batch-2383: Implemented Decimal.CreateChecked Float/Double conversion with pinned 7/15-digit rounding, scale-28 underflow and exact overflow behavior.

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; qualification remains open) |
| Framework / plan scope | dotj-core / DJ-001-N01-T2 |
| Outcome | Implemented Decimal.CreateChecked Float/Double conversion with pinned 7/15-digit rounding, scale-28 underflow and exact overflow behavior. |
| Validation | 398/398 foundation checks; 2460 exact outcome/holder groups, 1230 native calls and 1230 Java facade calls; 1230 native and Java floating calls and 2460 exact result/input groups passed; full retained canonical gate, packaged consumers and API/signature audits passed. |
| Limitation | Selected JDK Float/Double and retained integer/Decimal carriers only; Half input identity, custom INumberBase dispatch, CLR generic constraints/ABI and acceptance remain open. |
| Acceptance credit | None; no implementation task or qualification gate accepted |
| Numbered batches completed | 2,383 |
| Remaining to original 2,000 target | 0 |
| Remaining to authorized 2,500 milestone | 117 |
| Project batches planned / remaining | Unknown / unknown |
| Accepted implementation tasks | 0/1092 (0.00%) |
| Open acceptance items | 1686 |
| Qualified frameworks | 0/66 |
| Git workflow | Feature branch, merge to master after verification, then immediately push master and the completed feature branch. Actual merge/push results are reported after execution. |
| Next concrete task | Batch-2384: Implement and qualify Decimal.CreateSaturating for selected integer/Decimal carriers with exact min/max clamping, signed-zero preservation and explicit generic carrier adaptation. |

All temporary builds, downloads, caches, and execution logs belong under `D:\AI\Implementation\dotj Frameworks`.
