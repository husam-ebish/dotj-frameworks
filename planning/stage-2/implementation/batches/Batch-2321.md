# Batch-2321: Added Decimal.ToString(String format), retained provider-overload null intent explicitly in product/consumer call sites and updated strict API declaration scope.

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; qualification remains open) |
| Framework / plan scope | dotj-core / DJ-001-N01-T2 |
| Outcome | Added Decimal.ToString(String format), retained provider-overload null intent explicitly in product/consumer call sites and updated strict API declaration scope. |
| Validation | 336/336 foundation checks; 482 groups: 240 native format calls, immutable bits, exact method shape and ambiguous-null compile rejection; previous JAR lacks String overload; retained packaged consumers, conversion, spans and strict API checks passed. |
| Limitation | Selected invariant current-culture profile and existing formats only. Ambient cultures, complete formatting/ABI/generic numerics and task acceptance remain open. |
| Acceptance credit | None; no implementation task or qualification gate accepted |
| Numbered batches completed | 2,321 |
| Remaining to original 2,000 target | 0 |
| Remaining to authorized 2,500 milestone | 179 |
| Project batches planned / remaining | Unknown / unknown |
| Accepted implementation tasks | 0/1092 (0.00%) |
| Open acceptance items | 1686 |
| Qualified frameworks | 0/66 |
| Git workflow | Feature branch, merge to master after verification, then immediately push master and the completed feature branch. Actual merge/push results are reported after execution. |
| Next concrete task | Batch-2322: Inspect and implement the next selected Decimal ReadOnlySpan<Char> Parse overloads against native style/provider/error precedence, retaining explicit Java null-overload decisions. |

All temporary builds, downloads, caches, and execution logs belong under `D:\AI\Implementation\dotj Frameworks`.
