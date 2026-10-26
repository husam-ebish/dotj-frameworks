# Batch-2255: Qualified selected UTF16 decoder replacement Convert heap spans, signed carriers and protected output views.

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; qualification remains open) |
| Framework / plan scope | dotj-core / DJ-001-WP-05-T2 |
| Outcome | Qualified selected UTF16 decoder replacement Convert heap spans, signed carriers and protected output views. |
| Validation | 270/270 foundation checks; 822528 groups across 235008 native calls, including 760 signed-consumption and 410 unreported-prefix observations; existing 98-source/API and retained consumers passed. |
| Limitation | Selected owned decoder heap-span replacement Convert only; arbitrary callbacks, pointer/byref ABI, encoder nonterminal mismatch/no-return policy, E01 and task acceptance remain open. |
| Acceptance credit | None; no implementation task or qualification gate accepted |
| Numbered batches completed | 2,255 |
| Remaining to original 2,000 target | 0 |
| Remaining to authorized 2,500 milestone | 245 |
| Project batches planned / remaining | Unknown / unknown |
| Accepted implementation tasks | 0/1092 (0.00%) |
| Open acceptance items | 1686 |
| Qualified frameworks | 0/66 |
| Git workflow | Feature branch, merge to master after verification, then immediately push master and the completed feature branch. Actual merge/push results are reported after execution. |
| Next concrete task | Batch-2256: Review and qualify decoder replacement NUL/surrogate cross-method interleavings, fallback cursor operations, setters and Reset behavior. |

All temporary builds, downloads, caches, and execution logs belong under `D:\AI\Implementation\dotj Frameworks`.
