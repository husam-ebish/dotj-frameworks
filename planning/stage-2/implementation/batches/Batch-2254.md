# Batch-2254: Qualified selected UTF16 decoder Convert NUL/surrogate replacement outputs, signed consumption and subsequent state.

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; qualification remains open) |
| Framework / plan scope | dotj-core / DJ-001-WP-05-T2 |
| Outcome | Qualified selected UTF16 decoder Convert NUL/surrogate replacement outputs, signed consumption and subsequent state. |
| Validation | 269/269 foundation checks; 826272 groups across 235944 native calls, including 760 signed-consumption and 410 unreported-prefix observations; existing 98-source/API and retained consumers passed. |
| Limitation | Selected owned decoder array Convert replacement cases only; span replacement Convert, arbitrary callbacks, pointer/byref ABI, encoder nonterminal mismatch/no-return policy, E01 and task acceptance remain open. |
| Acceptance credit | None; no implementation task or qualification gate accepted |
| Numbered batches completed | 2,254 |
| Remaining to original 2,000 target | 0 |
| Remaining to authorized 2,500 milestone | 246 |
| Project batches planned / remaining | Unknown / unknown |
| Accepted implementation tasks | 0/1092 (0.00%) |
| Open acceptance items | 1686 |
| Qualified frameworks | 0/66 |
| Git workflow | Feature branch, merge to master after verification, then immediately push master and the completed feature branch. Actual merge/push results are reported after execution. |
| Next concrete task | Batch-2255: Qualify returned decoder replacement Convert heap spans and protected output views, including signed carriers and later carry/fallback state. |

All temporary builds, downloads, caches, and execution logs belong under `D:\AI\Implementation\dotj Frameworks`.
