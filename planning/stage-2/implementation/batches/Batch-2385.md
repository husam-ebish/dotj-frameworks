# Batch-2385: Implemented Float/Double Decimal.CreateSaturating with exact limit clamping and native scale-one NaN zero.

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; qualification remains open) |
| Framework / plan scope | dotj-core / DJ-001-N01-T2 |
| Outcome | Implemented Float/Double Decimal.CreateSaturating with exact limit clamping and native scale-one NaN zero. |
| Validation | 400/400 foundation checks; 2460 exact outcome/holder groups, 1230 native calls and 1230 Java facade calls; 1230 native and Java saturation calls and 2460 exact result/input groups passed, including native NaN scale one; full retained canonical gate, packaged consumers and API/signature audits passed. |
| Limitation | Selected JDK Float/Double plus retained integer/Decimal carriers only; Half identity, custom INumberBase dispatch, CLR generic constraints/ABI and acceptance remain open. |
| Acceptance credit | None; no implementation task or qualification gate accepted |
| Numbered batches completed | 2,385 |
| Remaining to original 2,000 target | 0 |
| Remaining to authorized 2,500 milestone | 115 |
| Project batches planned / remaining | Unknown / unknown |
| Accepted implementation tasks | 0/1092 (0.00%) |
| Open acceptance items | 1686 |
| Qualified frameworks | 0/66 |
| Git workflow | Feature branch, merge to master after verification, then immediately push master and the completed feature branch. Actual merge/push results are reported after execution. |
| Next concrete task | Batch-2386: Implement and qualify Decimal.CreateTruncating for selected integer/Decimal carriers, verifying native 96-bit clamping and signed-zero preservation rather than assuming fixed-width integer wrap semantics. |

All temporary builds, downloads, caches, and execution logs belong under `D:\AI\Implementation\dotj Frameworks`.
