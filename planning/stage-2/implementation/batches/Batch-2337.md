# Batch-2337: Matched exact Decimal Parse format/overflow messages using original UTF16 input or valid-UTF8 display text, preserved provider failures and retired unreachable legacy parser branches.

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; qualification remains open) |
| Framework / plan scope | dotj-core / DJ-001-N01-T2 |
| Outcome | Matched exact Decimal Parse format/overflow messages using original UTF16 input or valid-UTF8 display text, preserved provider failures and retired unreachable legacy parser branches. |
| Validation | 352/352 foundation checks; 47520 groups from 6912 native calls and 9504 Java facade calls across nine styles, six providers and String/Char/UTF8 routes; exact text/type/HResult/parameter, callback count/type, provider exception identity and result bits compared; previous JAR mismatches messages; retained all parsing/formatting/conversion/interface/API checks passed. |
| Limitation | Selected exact English invariant error messages and provider boundaries only; mutable provider/input callback cases, all cultures, complete grammar/ABI and acceptance remain open. |
| Acceptance credit | None; no implementation task or qualification gate accepted |
| Numbered batches completed | 2,337 |
| Remaining to original 2,000 target | 0 |
| Remaining to authorized 2,500 milestone | 163 |
| Project batches planned / remaining | Unknown / unknown |
| Accepted implementation tasks | 0/1092 (0.00%) |
| Open acceptance items | 1686 |
| Qualified frameworks | 0/66 |
| Git workflow | Feature branch, merge to master after verification, then immediately push master and the completed feature branch. Actual merge/push results are reported after execution. |
| Next concrete task | Batch-2338: Qualify Decimal Parse/TryParse provider callbacks that mutate span backing arrays, output holders and NumberFormatInfo tokens before returning or throwing, including UTF8 cache refresh. |

All temporary builds, downloads, caches, and execution logs belong under `D:\AI\Implementation\dotj Frameworks`.
