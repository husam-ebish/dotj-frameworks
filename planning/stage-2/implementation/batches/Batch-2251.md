# Batch-2251: Matched stateless UTF16 terminal malformed-input NUL and surrogate replacement counts and writes using actual fallback buffers.

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; qualification remains open) |
| Framework / plan scope | dotj-core / DJ-001-WP-05-T2 |
| Outcome | Matched stateless UTF16 terminal malformed-input NUL and surrogate replacement counts and writes using actual fallback buffers. |
| Validation | 266/266 foundation checks; 12960 comparison groups across 2880 returned native terminal encoder cases and eighteen configurations; retained encoder/decoder/buffer and 98-source/API checks passed. |
| Limitation | Selected stateless terminal malformed-input array cases only; nonterminal residual-fallback interleavings remain mismatched/unqualified. Owned state, spans/Convert replacement edges, native no-return policy, ABI/E01 and task acceptance remain open. |
| Acceptance credit | None; no implementation task or qualification gate accepted |
| Numbered batches completed | 2,251 |
| Remaining to original 2,000 target | 0 |
| Remaining to authorized 2,500 milestone | 249 |
| Project batches planned / remaining | Unknown / unknown |
| Accepted implementation tasks | 0/1092 (0.00%) |
| Open acceptance items | 1686 |
| Qualified frameworks | 0/66 |
| Git workflow | Feature branch, merge to master after verification, then immediately push master and the completed feature branch. Actual merge/push results are reported after execution. |
| Next concrete task | Batch-2252: Qualify decoder replacement NUL/surrogate count/write heap-span forwarding and protected destination windows against pinned native behavior. |

All temporary builds, downloads, caches, and execution logs belong under `D:\AI\Implementation\dotj Frameworks`.
