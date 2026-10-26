# Batch-2256: Qualified selected UTF16 decoder NUL/surrogate replacement cross-method and standard-buffer interleavings.

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; qualification remains open) |
| Framework / plan scope | dotj-core / DJ-001-WP-05-T2 |
| Outcome | Qualified selected UTF16 decoder NUL/surrogate replacement cross-method and standard-buffer interleavings. |
| Validation | 271/271 foundation checks; 1669248 groups across 663552 native calls and 55296 sequences; existing 98-source/API and retained consumers passed. |
| Limitation | Selected owned decoder arrays and standard buffers only; arbitrary callbacks/span cross-method protocols, pointer/byref ABI, encoder nonterminal mismatch/no-return policy, E01 and task acceptance remain open. |
| Acceptance credit | None; no implementation task or qualification gate accepted |
| Numbered batches completed | 2,256 |
| Remaining to original 2,000 target | 0 |
| Remaining to authorized 2,500 milestone | 244 |
| Project batches planned / remaining | Unknown / unknown |
| Accepted implementation tasks | 0/1092 (0.00%) |
| Open acceptance items | 1686 |
| Qualified frameworks | 0/66 |
| Git workflow | Feature branch, merge to master after verification, then immediately push master and the completed feature branch. Actual merge/push results are reported after execution. |
| Next concrete task | Batch-2257: Qualify shared integer output-cell assignment order for decoder replacement Convert arrays and heap spans, including NUL and surrogate replacements. |

All temporary builds, downloads, caches, and execution logs belong under `D:\AI\Implementation\dotj Frameworks`.
