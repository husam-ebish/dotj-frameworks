# Batch-2372: Qualified Decimal standard formatting at signed-zero, midpoint, scale-28, 96-bit and exponent carry boundaries without a product change.

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; qualification remains open) |
| Framework / plan scope | dotj-core / DJ-001-N01-T2 |
| Outcome | Qualified Decimal standard formatting at signed-zero, midpoint, scale-28, 96-bit and exponent carry boundaries without a product change. |
| Validation | 387/387 foundation checks; 163856 exact outcome/holder groups, 41474 native calls and 41474 Java facade calls; product JAR unchanged from prior qualified candidate; full retained canonical gate, packaged consumers and API/signature audits passed. |
| Limitation | Selected precision and two provider profiles only; exhaustive pattern combinations, arbitrary cultures/ABI and acceptance remain open. |
| Acceptance credit | None; no implementation task or qualification gate accepted |
| Numbered batches completed | 2,372 |
| Remaining to original 2,000 target | 0 |
| Remaining to authorized 2,500 milestone | 128 |
| Project batches planned / remaining | Unknown / unknown |
| Accepted implementation tasks | 0/1092 (0.00%) |
| Open acceptance items | 1686 |
| Qualified frameworks | 0/66 |
| Git workflow | Feature branch, merge to master after verification, then immediately push master and the completed feature branch. Actual merge/push results are reported after execution. |
| Next concrete task | Batch-2373: Qualify all five Decimal number-negative patterns with custom decimal/group separators, group-size stopping rules and Char/UTF8 encoding. |

All temporary builds, downloads, caches, and execution logs belong under `D:\AI\Implementation\dotj Frameworks`.
