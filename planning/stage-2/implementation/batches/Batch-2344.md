# Batch-2344: Corrected unsigned negative decimal-zero rejection and qualified live backing-array/output/token mutations across all five integer parsing facades.

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; qualification remains open) |
| Framework / plan scope | dotj-core / DJ-001-N01-T2 |
| Outcome | Corrected unsigned negative decimal-zero rejection and qualified live backing-array/output/token mutations across all five integer parsing facades. |
| Validation | 359/359 foundation checks; 201600 groups from 18900 native primary calls, 6300 native UTF8 cache primes and 25200 Java facade calls; whole buffers, outputs, exact outcomes, callback/type/identity and token state compared; prior JAR accepts unsigned negative zero with a consumed decimal separator; retained parser/formatting/Decimal matrices, packaged consumers and API/signature audits passed. |
| Limitation | Selected synchronous mutation and unsigned-zero distinction only; all-style unsigned-zero breadth, concurrent/reentrant parsing, full cultures/grammar/ABI and acceptance remain open. |
| Acceptance credit | None; no implementation task or qualification gate accepted |
| Numbered batches completed | 2,344 |
| Remaining to original 2,000 target | 0 |
| Remaining to authorized 2,500 milestone | 156 |
| Project batches planned / remaining | Unknown / unknown |
| Accepted implementation tasks | 0/1092 (0.00%) |
| Open acceptance items | 1686 |
| Qualified frameworks | 0/66 |
| Git workflow | Feature branch, merge to master after verification, then immediately push master and the completed feature branch. Actual merge/push results are reported after execution. |
| Next concrete task | Batch-2345: Qualify zero/sign handling across all 520 valid integer styles and unsigned widths, distinguishing fast Integer negative zero from general parser rejection and positive-sign precedence. |

All temporary builds, downloads, caches, and execution logs belong under `D:\AI\Implementation\dotj Frameworks`.
