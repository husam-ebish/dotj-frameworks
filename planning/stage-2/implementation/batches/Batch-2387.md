# Batch-2387: Qualified Decimal.CreateTruncating Float/Double exact IEEE conversion, NaN scale-one zero and native limit clamping without an additional product change.

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; qualification remains open) |
| Framework / plan scope | dotj-core / DJ-001-N01-T2 |
| Outcome | Qualified Decimal.CreateTruncating Float/Double exact IEEE conversion, NaN scale-one zero and native limit clamping without an additional product change. |
| Validation | 402/402 foundation checks; 2460 exact outcome/holder groups, 1230 native calls and 1230 Java facade calls; product JAR unchanged from prior qualified candidate; full retained canonical gate, packaged consumers and API/signature audits passed. |
| Limitation | Selected owned/JDK numeric carriers only; Half identity, custom INumberBase dispatch, CLR generic constraints/ABI and acceptance remain open. |
| Acceptance credit | None; no implementation task or qualification gate accepted |
| Numbered batches completed | 2,387 |
| Remaining to original 2,000 target | 0 |
| Remaining to authorized 2,500 milestone | 113 |
| Project batches planned / remaining | Unknown / unknown |
| Accepted implementation tasks | 0/1092 (0.00%) |
| Open acceptance items | 1686 |
| Qualified frameworks | 0/66 |
| Git workflow | Feature branch, merge to master after verification, then immediately push master and the completed feature branch. Actual merge/push results are reported after execution. |
| Next concrete task | Batch-2388: Implement and qualify selected Char/Byte/Int32 Span element reads and writes through array-backed views, including aliasing, bounds, full-buffer preservation and explicit ref-return adaptation limits. |

All temporary builds, downloads, caches, and execution logs belong under `D:\AI\Implementation\dotj Frameworks`.
