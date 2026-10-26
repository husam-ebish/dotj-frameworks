# Batch-2250: Matched standard UTF16 decoder NUL/surrogate replacement writes and distinct count semantics across stateless/stateful arrays.

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; qualification remains open) |
| Framework / plan scope | dotj-core / DJ-001-WP-05-T2 |
| Outcome | Matched standard UTF16 decoder NUL/surrogate replacement writes and distinct count semantics across stateless/stateful arrays. |
| Validation | 265/265 foundation checks; 427680 groups across 25920 returned native decoder cases and eighteen configurations; retained encoder/decoder/buffer/stateless and 98-source/API checks passed. |
| Limitation | Selected decoder array replacement edges only; encoder no-return/liveness policy, equivalent spans/Convert edges, arbitrary custom callbacks, ABI/E01 and task acceptance remain open. |
| Acceptance credit | None; no implementation task or qualification gate accepted |
| Numbered batches completed | 2,250 |
| Remaining to original 2,000 target | 0 |
| Remaining to authorized 2,500 milestone | 250 |
| Project batches planned / remaining | Unknown / unknown |
| Accepted implementation tasks | 0/1092 (0.00%) |
| Open acceptance items | 1686 |
| Qualified frameworks | 0/66 |
| Git workflow | Feature branch, merge to master after verification, then immediately push master and the completed feature branch. Actual merge/push results are reported after execution. |
| Next concrete task | Batch-2251: Match selected stateless terminal UTF16 encoder NUL/surrogate fallback counts and writes; retain explicit open nonterminal interleavings and native no-return observations. |

All temporary builds, downloads, caches, and execution logs belong under `D:\AI\Implementation\dotj Frameworks`.
