# Batch-2329: Applied all-NUL trailing remainder handling across selected Decimal styles, rejected embedded NUL before recursive normalization and corrected identical invariant Any separators.

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; qualification remains open) |
| Framework / plan scope | dotj-core / DJ-001-N01-T2 |
| Outcome | Applied all-NUL trailing remainder handling across selected Decimal styles, rejected embedded NUL before recursive normalization and corrected identical invariant Any separators. |
| Validation | 344/344 foundation checks; 2816 groups from 1408 native calls across 16 styles, 22 NUL/plain inputs and String/Char-span Parse/TryParse; previous JAR rejects native NUL inputs and invariant Any decimals; retained parsing/provider/UTF8/formatting/conversion/interface/API checks passed. |
| Limitation | Selected trailing-NUL and shared invariant separator behavior only; NUL within provider tokens, composite styles, complete grammar, ambient cultures, exact input-error text and acceptance remain open. |
| Acceptance credit | None; no implementation task or qualification gate accepted |
| Numbered batches completed | 2,329 |
| Remaining to original 2,000 target | 0 |
| Remaining to authorized 2,500 milestone | 171 |
| Project batches planned / remaining | Unknown / unknown |
| Accepted implementation tasks | 0/1092 (0.00%) |
| Open acceptance items | 1686 |
| Qualified frameworks | 0/66 |
| Git workflow | Feature branch, merge to master after verification, then immediately push master and the completed feature branch. Actual merge/push results are reported after execution. |
| Next concrete task | Batch-2330: Implement and qualify all 128 combinations of basic Decimal whitespace, sign, parentheses, decimal-point and grouping flags against native invariant/custom provider profiles. |

All temporary builds, downloads, caches, and execution logs belong under `D:\AI\Implementation\dotj Frameworks`.
