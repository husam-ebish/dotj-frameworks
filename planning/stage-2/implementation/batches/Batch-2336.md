# Batch-2336: Matched provider tokens only through their native first-NUL prefix and consumed the matched prefix length while preserving original sign-alias metadata and provider/input state.

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; qualification remains open) |
| Framework / plan scope | dotj-core / DJ-001-N01-T2 |
| Outcome | Matched provider tokens only through their native first-NUL prefix and consumed the matched prefix length while preserving original sign-alias metadata and provider/input state. |
| Validation | 351/351 foundation checks; 321360 groups from 77740 native calls and 107120 Java facade calls across 56 token profiles and ten styles; empty/effective prefixes, suffix controls, Unicode alias metadata, space substitution and String/Char/UTF8 routes included; prior JAR rejects native prefixes; retained all parsing/formatting/conversion/interface/API checks passed. |
| Limitation | Selected first-NUL token prefixes only; exact parse error messages, all cultures, complete grammar/ABI and acceptance remain open. |
| Acceptance credit | None; no implementation task or qualification gate accepted |
| Numbered batches completed | 2,336 |
| Remaining to original 2,000 target | 0 |
| Remaining to authorized 2,500 milestone | 164 |
| Project batches planned / remaining | Unknown / unknown |
| Accepted implementation tasks | 0/1092 (0.00%) |
| Open acceptance items | 1686 |
| Qualified frameworks | 0/66 |
| Git workflow | Feature branch, merge to master after verification, then immediately push master and the completed feature branch. Actual merge/push results are reported after execution. |
| Next concrete task | Batch-2337: Match native Decimal Parse format/overflow error messages using original String/Char or UTF8-display input while preserving provider exception identity and TryParse result ordering. |

All temporary builds, downloads, caches, and execution logs belong under `D:\AI\Implementation\dotj Frameworks`.
