# Batch-2257: Qualified selected UTF16 decoder NUL/surrogate replacement Convert shared output cells across arrays and heap spans.

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; qualification remains open) |
| Framework / plan scope | dotj-core / DJ-001-WP-05-T2 |
| Outcome | Qualified selected UTF16 decoder NUL/surrogate replacement Convert shared output cells across arrays and heap spans. |
| Validation | 272/272 foundation checks; 829440 groups across 55296 native cases with 27648 shared cases and 38936 successful counter distinctions; existing 98-source/API and retained consumers passed. |
| Limitation | Selected owned decoder replacement integer output-cell aliasing only; arbitrary callbacks, complete pointer/byref ABI, encoder nonterminal mismatch/no-return policy, E01 and task acceptance remain open. |
| Acceptance credit | None; no implementation task or qualification gate accepted |
| Numbered batches completed | 2,257 |
| Remaining to original 2,000 target | 0 |
| Remaining to authorized 2,500 milestone | 243 |
| Project batches planned / remaining | Unknown / unknown |
| Accepted implementation tasks | 0/1092 (0.00%) |
| Open acceptance items | 1686 |
| Qualified frameworks | 0/66 |
| Git workflow | Feature branch, merge to master after verification, then immediately push master and the completed feature branch. Actual merge/push results are reported after execution. |
| Next concrete task | Batch-2258: Qualify selected decoder replacement cross-method heap-span calls, primed fallback cursors, setters and Reset against pinned native behavior. |

All temporary builds, downloads, caches, and execution logs belong under `D:\AI\Implementation\dotj Frameworks`.
