# Batch-2326: Corrected Decimal Number parsing to native ASCII whitespace, whitespace before trailing signs and all-NUL trailing remainder rules.

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; qualification remains open) |
| Framework / plan scope | dotj-core / DJ-001-N01-T2 |
| Outcome | Corrected Decimal Number parsing to native ASCII whitespace, whitespace before trailing signs and all-NUL trailing remainder rules. |
| Validation | 341/341 foundation checks; 2784 groups from 1392 native String/Char-span default Parse/TryParse calls over 348 Unicode/ASCII whitespace, sign-spacing and trailing-NUL inputs; previous JAR accepts forbidden Unicode whitespace or rejects native NUL/sign spacing; retained parsing/formatting/conversion/interface/API checks passed. |
| Limitation | Selected invariant Number-style whitespace/sign/NUL behavior only; other styles, culture, UTF8, exact input-error messages and full acceptance remain open. |
| Acceptance credit | None; no implementation task or qualification gate accepted |
| Numbered batches completed | 2,326 |
| Remaining to original 2,000 target | 0 |
| Remaining to authorized 2,500 milestone | 174 |
| Project batches planned / remaining | Unknown / unknown |
| Accepted implementation tasks | 0/1092 (0.00%) |
| Open acceptance items | 1686 |
| Qualified frameworks | 0/66 |
| Git workflow | Feature branch, merge to master after verification, then immediately push master and the completed feature branch. Actual merge/push results are reported after execution. |
| Next concrete task | Batch-2327: Verify and correct Decimal UTF8 parsing so malformed bytes cannot become valid replacement-character provider tokens; retain provider/error/output precedence. |

All temporary builds, downloads, caches, and execution logs belong under `D:\AI\Implementation\dotj Frameworks`.
