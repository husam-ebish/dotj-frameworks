# Batch-2333: Implemented native ASCII hyphen aliases for seven configured Unicode negative signs in leading, trailing and exponent positions while preserving positive-sign priority.

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; qualification remains open) |
| Framework / plan scope | dotj-core / DJ-001-N01-T2 |
| Outcome | Implemented native ASCII hyphen aliases for seven configured Unicode negative signs in leading, trailing and exponent positions while preserving positive-sign priority. |
| Validation | 348/348 foundation checks; 93912 groups from 31304 native calls across 27 negative/positive sign profiles, 14 styles and String/Char-span Parse/TryParse; nearby/multichar/empty negative controls and positive-hyphen priority included; prior JAR rejects native aliases; retained all style/token/NUL/provider/UTF8 parsing, formatting, conversion, interface and API checks passed. |
| Limitation | Selected seven-sign native fallback and controls only; space-replacing UTF16/UTF8 token semantics, broader cultures, exact input-error text and complete grammar/acceptance remain open. |
| Acceptance credit | None; no implementation task or qualification gate accepted |
| Numbered batches completed | 2,333 |
| Remaining to original 2,000 target | 0 |
| Remaining to authorized 2,500 milestone | 167 |
| Project batches planned / remaining | Unknown / unknown |
| Accepted implementation tasks | 0/1092 (0.00%) |
| Open acceptance items | 1686 |
| Qualified frameworks | 0/66 |
| Git workflow | Feature branch, merge to master after verification, then immediately push master and the completed feature branch. Actual merge/push results are reported after execution. |
| Next concrete task | Batch-2334: Implement native code-unit space substitution for NBSP/narrow-NBSP provider tokens and preserve UTF8 raw-byte token matching versus UTF16 behavior. |

All temporary builds, downloads, caches, and execution logs belong under `D:\AI\Implementation\dotj Frameworks`.
