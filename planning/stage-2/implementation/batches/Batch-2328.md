# Batch-2328: Replaced global Number-style provider replacements with positional sign/decimal/group token handling, correcting collisions and prefix overlaps.

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; qualification remains open) |
| Framework / plan scope | dotj-core / DJ-001-N01-T2 |
| Outcome | Replaced global Number-style provider replacements with positional sign/decimal/group token handling, correcting collisions and prefix overlaps. |
| Validation | 343/343 foundation checks; 3180 groups from 1060 native calls across 11 colliding/overlapping provider profiles and String/Char-span Parse/TryParse, including immutable provider properties; previous JAR misreads a leading shared sign/decimal token; retained parsing/provider/UTF8/formatting/conversion/interface/API checks passed. |
| Limitation | Selected Number-style token precedence only; other style normalizers, space separators, full grammar, ambient cultures, exact input-error text and acceptance remain open. |
| Acceptance credit | None; no implementation task or qualification gate accepted |
| Numbered batches completed | 2,328 |
| Remaining to original 2,000 target | 0 |
| Remaining to authorized 2,500 milestone | 172 |
| Project batches planned / remaining | Unknown / unknown |
| Accepted implementation tasks | 0/1092 (0.00%) |
| Open acceptance items | 1686 |
| Qualified frameworks | 0/66 |
| Git workflow | Feature branch, merge to master after verification, then immediately push master and the completed feature branch. Actual merge/push results are reported after execution. |
| Next concrete task | Batch-2329: Qualify trailing NUL parsing across selected Decimal NumberStyles and correct non-Number style handling, retaining UTF8-specific flag validation. |

All temporary builds, downloads, caches, and execution logs belong under `D:\AI\Implementation\dotj Frameworks`.
