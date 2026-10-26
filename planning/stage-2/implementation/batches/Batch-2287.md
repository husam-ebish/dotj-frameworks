# Batch-2287: Qualified selected Exception.Data values CopyTo primitive widening, rejected conversions, null defaults and raw floating-point bits.

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; qualification remains open) |
| Framework / plan scope | dotj-core / DJ-001-N01-T2 |
| Outcome | Qualified selected Exception.Data values CopyTo primitive widening, rejected conversions, null defaults and raw floating-point bits. |
| Validation | 302/302 foundation checks; 18240 comparisons across 2280 native cases, 38 boxed source profiles, ten destination kinds and six indices; signed extrema, char/bool, negative zero, NaN payloads, infinities, subnormals, partial writes and unchanged ordered dictionary state passed. |
| Limitation | Qualification expansion only; product source is unchanged from Batch 2286. Unsigned destinations, full boxing/Array ABI, reentrancy, serialization, E01 and task acceptance remain open. |
| Acceptance credit | None; no implementation task or qualification gate accepted |
| Numbered batches completed | 2,287 |
| Remaining to original 2,000 target | 0 |
| Remaining to authorized 2,500 milestone | 213 |
| Project batches planned / remaining | Unknown / unknown |
| Accepted implementation tasks | 0/1092 (0.00%) |
| Open acceptance items | 1686 |
| Qualified frameworks | 0/66 |
| Git workflow | Feature branch, merge to master after verification, then immediately push master and the completed feature branch. Actual merge/push results are reported after execution. |
| Next concrete task | Batch-2288: Capture once-only key equality callbacks that mutate Exception.Data during lookup and mutation; compare native node/count/version behavior and correct demonstrated reentrant collection deviations. |

All temporary builds, downloads, caches, and execution logs belong under `D:\AI\Implementation\dotj Frameworks`.
