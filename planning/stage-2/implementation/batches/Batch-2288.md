# Batch-2288: Corrected bounded reentrant Exception.Data equality using node identity, detached traversal and separate stored/view counts.

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; qualification remains open) |
| Framework / plan scope | dotj-core / DJ-001-N01-T2 |
| Outcome | Corrected bounded reentrant Exception.Data equality using node identity, detached traversal and separate stored/view counts. |
| Validation | 303/303 foundation checks; 7980 comparisons across 420 native cases, seven once-only callback actions, five operations, three initial sizes and two query identities; 24 native null-reference and 78 duplicate failures; prior JAR fails count witness; retained consumers/API/source map passed. |
| Limitation | Once-only selected CLR equality mutations only. Concurrency, unbounded recursion, CopyTo after inconsistent counts, complete object/serialization ABI, E01 and task acceptance remain open. |
| Acceptance credit | None; no implementation task or qualification gate accepted |
| Numbered batches completed | 2,288 |
| Remaining to original 2,000 target | 0 |
| Remaining to authorized 2,500 milestone | 212 |
| Project batches planned / remaining | Unknown / unknown |
| Accepted implementation tasks | 0/1092 (0.00%) |
| Open acceptance items | 1686 |
| Qualified frameworks | 0/66 |
| Git workflow | Feature branch, merge to master after verification, then immediately push master and the completed feature branch. Actual merge/push results are reported after execution. |
| Next concrete task | Batch-2289: Qualify CopyTo after the selected reentrant callbacks leave stored count different from reachable nodes; compare validation, partial writes and array bounds exceptions for dictionary/keys/values views. |

All temporary builds, downloads, caches, and execution logs belong under `D:\AI\Implementation\dotj Frameworks`.
