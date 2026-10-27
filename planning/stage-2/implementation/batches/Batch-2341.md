# Batch-2341: Matched native UTF8 numeric format/overflow and invalid-style error text for four small integer facades via a shared exact boundary, preserving Int32 behavior and provider failures.

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; qualification remains open) |
| Framework / plan scope | dotj-core / DJ-001-N01-T2 |
| Outcome | Matched native UTF8 numeric format/overflow and invalid-style error text for four small integer facades via a shared exact boundary, preserving Int32 behavior and provider failures. |
| Validation | 356/356 foundation checks; 435600 exact-message groups from the existing 43560 pinned native cases and 87120 Java facade calls; all five integer types now compare full messages/type/HResult/parameter with callback/holder/identity controls; previous JAR mismatches small-integer text; retained parsers, formatting, packaged consumers and API/erasure checks passed. |
| Limitation | Exact UTF8 messages within selected existing corpus only; Int32/small-integer Char/String breadth, all cultures, complete grammar/ABI and acceptance remain open. |
| Acceptance credit | None; no implementation task or qualification gate accepted |
| Numbered batches completed | 2,341 |
| Remaining to original 2,000 target | 0 |
| Remaining to authorized 2,500 milestone | 159 |
| Project batches planned / remaining | Unknown / unknown |
| Accepted implementation tasks | 0/1092 (0.00%) |
| Open acceptance items | 1686 |
| Qualified frameworks | 0/66 |
| Git workflow | Feature branch, merge to master after verification, then immediately push master and the completed feature branch. Actual merge/push results are reported after execution. |
| Next concrete task | Batch-2342: Align Int32 String/Char Parse and TryParse with the shared native integer-style scanner, exact error messages and provider/result ordering while retaining UTF8 behavior. |

All temporary builds, downloads, caches, and execution logs belong under `D:\AI\Implementation\dotj Frameworks`.
