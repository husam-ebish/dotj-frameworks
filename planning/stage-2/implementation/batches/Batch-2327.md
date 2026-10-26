# Batch-2327: Rejected malformed Decimal UTF8 before replacement tokens can match provider signs; retained provider/output precedence and pinned UTF8-specific integer-style validation.

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; qualification remains open) |
| Framework / plan scope | dotj-core / DJ-001-N01-T2 |
| Outcome | Rejected malformed Decimal UTF8 before replacement tokens can match provider signs; retained provider/output precedence and pinned UTF8-specific integer-style validation. |
| Validation | 342/342 foundation checks; 47040 groups from 3920 native calls and 7840 primitive/boxed UTF8 facade calls across 49 byte vectors, eight styles and five providers; prior JAR accepts malformed replacement tokens; retained Char parsing, provider, conversion, formatting, interfaces and API checks passed. |
| Limitation | Selected UTF8 validity and pinned style/provider boundaries only. Shared sign/decimal token normalization is independently deferred to next batch; complete grammar, cultures, exact input error text and acceptance remain open. |
| Acceptance credit | None; no implementation task or qualification gate accepted |
| Numbered batches completed | 2,327 |
| Remaining to original 2,000 target | 0 |
| Remaining to authorized 2,500 milestone | 173 |
| Project batches planned / remaining | Unknown / unknown |
| Accepted implementation tasks | 0/1092 (0.00%) |
| Open acceptance items | 1686 |
| Qualified frameworks | 0/66 |
| Git workflow | Feature branch, merge to master after verification, then immediately push master and the completed feature branch. Actual merge/push results are reported after execution. |
| Next concrete task | Batch-2328: Correct Decimal Number-style lexical provider token precedence when signs, decimal and group separators collide, using the preserved native shared-token counterexample. |

All temporary builds, downloads, caches, and execution logs belong under `D:\AI\Implementation\dotj Frameworks`.
