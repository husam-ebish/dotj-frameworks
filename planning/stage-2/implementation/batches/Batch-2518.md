# Batch-2518: numeric and version ordering conditions

Status: one selected private implementation group is implemented and qualified. Independent product review is approved. Whole-branch approval is required before integration; terminal merge/push is verified from Git ancestry and remote equality, not asserted by this preintegration report.

The private evaluator supports `<`, `<=`, `>` and `>=` for numeric pairs, version pairs and both mixed operand directions at existing condition sites. Conversion order, version component parsing, NaN comparisons and selected error-side behavior follow the pinned sources and observed reference contract. Equality, Boolean short circuit, immutable raw AST caching, reached single-pass expansion, warnings, owner isolation, bounds and the no-task boundary remain preserved. No public facade or module exports were added.

One qualified JAR, `6bc95bc7ed6d702ed58f455f10fe35ed0c71389dd175034afefaee2e259e089f` (109934 bytes), supplies every new and historical execution. The 308 new cases classify 220 native-success comparisons, 81 selected private error mappings and seven explicit existing restrictions. Those restrictions cover skipped malformed syntax, four Unicode/ASCII boundaries and the private grouping/node limits; they do not claim native parity. M1 observes a warning before a real ordering-conversion failure, then reuses the exact cached raw tree across valid, false and other-owner evaluations without state leakage.

The identical JAR passes Boolean297, 16 private inputs and 14 groups with only the observed BOOL-BOUND-ordering success transition. All 12 remaining historical JVMs pass. The stable94 rows match the retained golden bytes exactly; the two prior typed-equality transitions and the single import-path-only exclusion remain unchanged. Condition28/5/2 and four warnings, cache8+4 and its warning vector, And9+1+24, predicate32+6/four private groups, and predecessor18/391/223 obligations remain covered. Actual compiled consumers and every product class origin are bound to the candidate; no unrelated core518 gate was replayed.

Reference capture retains two matching 308-case passes: 222 native successes and86 project errors per pass. Eight capture phases are qualified; one older timed-out controller's native invocation count remains UNKNOWN. Original native failures, the development compiler setup failure, the historical class-prefix false positive, the transparently reissued review after a disk disconnect and the interrupted root PowerShell audit remain preserved. The successful bounded Python audit checked existing results without rerunning workloads.

| Measure | Recorded result | Remaining |
| --- | --- | --- |
| Numbered qualified candidate records in this checkout | 2518 | terminal integration from Git |
| Historical Batch-2500 target | 2500/2500 | 0 to that target |
| Whole-project batches | UNKNOWN | UNKNOWN |
| Selected private ordering group | 1/1 qualified | 0 implementation checks |
| Accepted implementation tasks | 0/1092 (0%) | 1092 |
| Open acceptance items | 1686 | no closure credit here |
| Qualified frameworks | 0/66 | 66 |
| Git workflow | feature/batch-2518-build-ordering-conditions-v1 to master | whole-branch gate, then verify merge/push |
| Next concrete work | verify integration, then select remaining acceptance scope | no further batch number assigned |

`completedBatches` records qualified numbered candidates in the checkout; on a feature branch it includes that candidate. It does not assert that a future merge or push has happened. The canonical baseline before this integration was Batch2517 at86ae. Root records terminal merge/push separately and reports the verified mainline result.

Product dependencies are JDK `java.base` and `java.xml`, with no third-party Java runtime library. Python, the pinned JDK and the .NET reference tools are development/validation tools. Paths in the evidence describe this machine, not portable installation requirements. The broader66-framework dependency graph, public .j installer/feed, full public API/platform/item/glob coverage and release qualification remain open. No full .NET parity, accepted work-package task or qualified framework is claimed. See [selected evidence](../../repos/dotj-build/evidence/private-condition-ordering-v1.json).
