# Batch-2258: Qualified selected UTF16 decoder replacement cross-method heap-span and standard-buffer interleavings.

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; qualification remains open) |
| Framework / plan scope | dotj-core / DJ-001-WP-05-T2 |
| Outcome | Qualified selected UTF16 decoder replacement cross-method heap-span and standard-buffer interleavings. |
| Validation | 273/273 foundation checks; 1669248 groups across 663552 native calls and 55296 sequences; existing 98-source/API and retained consumers passed. |
| Limitation | Selected owned decoder heap spans and standard buffers only; arbitrary callbacks, complete pointer/byref ABI, encoder nonterminal mismatch/no-return policy, E01 and task acceptance remain open. |
| Acceptance credit | None; no implementation task or qualification gate accepted |
| Numbered batches completed | 2,258 |
| Remaining to original 2,000 target | 0 |
| Remaining to authorized 2,500 milestone | 242 |
| Project batches planned / remaining | Unknown / unknown |
| Accepted implementation tasks | 0/1092 (0.00%) |
| Open acceptance items | 1686 |
| Qualified frameworks | 0/66 |
| Git workflow | Feature branch, merge to master after verification, then immediately push master and the completed feature branch. Actual merge/push results are reported after execution. |
| Next concrete task | Batch-2259: Qualify stateless decoder replacement allocating GetChars and GetString surfaces, preserving the native distinction between counted capacity and written output for NUL replacements. |

All temporary builds, downloads, caches, and execution logs belong under `D:\AI\Implementation\dotj Frameworks`.
