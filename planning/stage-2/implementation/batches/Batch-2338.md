# Batch-2338: Qualified mutable Decimal parsing providers that change whole Char/Byte backing arrays, output holders and NumberFormatInfo tokens before returning or throwing; current product unchanged.

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; qualification remains open) |
| Framework / plan scope | dotj-core / DJ-001-N01-T2 |
| Outcome | Qualified mutable Decimal parsing providers that change whole Char/Byte backing arrays, output holders and NumberFormatInfo tokens before returning or throwing; current product unchanged. |
| Validation | 353/353 foundation checks; 40320 groups from 3780 native primary calls, 1260 native UTF8 cache primes and 5040 Java facade calls; whole buffers, holder bits, exact outcomes, callback/type/identity and token state compared; current JAR passes unchanged and earlier snapshot-order control fails; retained all parsing/formatting/conversion/interface/API checks passed. |
| Limitation | Selected synchronous callback mutations/cache refresh only; concurrent/reentrant parsing, other numeric UTF8 token handling, all cultures/full grammar/ABI and acceptance remain open. |
| Acceptance credit | None; no implementation task or qualification gate accepted |
| Numbered batches completed | 2,338 |
| Remaining to original 2,000 target | 0 |
| Remaining to authorized 2,500 milestone | 162 |
| Project batches planned / remaining | Unknown / unknown |
| Accepted implementation tasks | 0/1092 (0.00%) |
| Open acceptance items | 1686 |
| Qualified frameworks | 0/66 |
| Git workflow | Feature branch, merge to master after verification, then immediately push master and the completed feature branch. Actual merge/push results are reported after execution. |
| Next concrete task | Batch-2339: Inspect and correct selected Int32 UTF8 provider-token byte matching and malformed-byte replacement acceptance while preserving native style/provider/error precedence. |

All temporary builds, downloads, caches, and execution logs belong under `D:\AI\Implementation\dotj Frameworks`.
