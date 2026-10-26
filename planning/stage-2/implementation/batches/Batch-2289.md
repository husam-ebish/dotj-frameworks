# Batch-2289: Corrected native CopyTo bounds failures after selected reentrant callbacks leave stored count different from reachable nodes.

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; qualification remains open) |
| Framework / plan scope | dotj-core / DJ-001-N01-T2 |
| Outcome | Corrected native CopyTo bounds failures after selected reentrant callbacks leave stored count different from reachable nodes. |
| Validation | 304/304 foundation checks; 16128 comparisons across 2688 native cases, all four distinct divergent-count states, three views, seven array kinds, four lengths and eight indices; 60 native bounds failures; prior JAR leaks Java bounds exception; retained consumers/API/map passed. |
| Limitation | Four selected returned divergent-count states only. Arbitrary callbacks, concurrency, full Array/object ABI, nonzero bounds, serialization, E01 and task acceptance remain open. |
| Acceptance credit | None; no implementation task or qualification gate accepted |
| Numbered batches completed | 2,289 |
| Remaining to original 2,000 target | 0 |
| Remaining to authorized 2,500 milestone | 211 |
| Project batches planned / remaining | Unknown / unknown |
| Accepted implementation tasks | 0/1092 (0.00%) |
| Open acceptance items | 1686 |
| Qualified frameworks | 0/66 |
| Git workflow | Feature branch, merge to master after verification, then immediately push master and the completed feature branch. Actual merge/push results are reported after execution. |
| Next concrete task | Batch-2290: Capture duplicate Exception.Data key formatting with null, throwing and Unicode ToString results; compare callback order and exact failure text and correct demonstrated formatting deviations. |

All temporary builds, downloads, caches, and execution logs belong under `D:\AI\Implementation\dotj Frameworks`.
