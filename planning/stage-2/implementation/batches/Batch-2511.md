# Batch-2511: Repeated-condition warning behavior

| Field | Result |
|---|---|
| Status | COMPLETE bounded implementation/qualification; framework acceptance remains open |
| Framework / task | dotj-build / DJ-005-WP-01-T1 and DJ-005-F01-01 |
| Native reference | 8 ordered cases in 6 groups, 10 XML files and 22 condition occurrences; two fresh .NET processes (10048 and 16196), both exit0, full payload agreement after fixture-path substitution only |
| Observed warnings | `[1,0,0,1,1,1,0,1]`, total5; repeated identical XML with different globals preserved true/false/true value freshness |
| Genuine product RED | Actual baseline JAR emitted `[2,2,2,7,2,2,0,1]`, total18; all values/imports matched. Original pre-change failure and final frozen-consumer baseline failure retained. |
| Implemented | Immutable parsed syntax and mixed-operator flag keyed by exact raw text; only reached conditions populate the cache. No expanded values, evaluation State, owner paths or globals retained. Standalone whole-XML validation does not warm warning state. |
| Source-derived bound | Clear before lookup when size exceeds3000. Sequential Default/AllowProperties behavior is qualified; source pooling internals and native eviction/concurrency are not claimed equivalent. |
| Final GREEN | Same new JAR: eight cache cases/five warnings, 94 current rows, retained35 (26 evaluations/5 native-failure boundaries/4 declared boundaries/four warnings), And9+1+24, four cache-state/owner controls, capture29 and qualification10 Python controls |
| Independent verification | Root observed final lock/receipt hashes, ran separate --check-receipt exit0 with empty stderr; independent task review approved with zero findings; final whole-branch review gates merge. |
| Final product source SHA-256 | `713ab126bc156137dcd6ff87109cfbc4417101bc67beccb36b9c25ab8e4ae08e` |
| Final candidate JAR SHA-256 | `add631430ab15623f4ba083a9da434d607894685a3def59fc44419d29048e3fa` |
| Final candidate-lock SHA-256 | `89f10070971287b8802578935b80ce0039e745b187e081465062417677bc97bc` |
| Native observation SHA-256 | `9612d662aa80501614b04475236169d7bb839ef5e0d41b932e2964bd0d2d688c` |
| Preserved | Existing current94 runner, And consumer, frozen v3/history, native capture tools/fixtures/reference inputs; no core product changes or repeated native captures after pairing |
| Limitations | Native cache internals, concurrency, eviction, multiple classloaders, same-live-Project reevaluation, alternate ParserOptions and full MSBuild cache parity remain unqualified. Full warning text/failure ABI and public API/framework qualification stay open. |
| Acceptance credit | None; no task/framework accepted. 8 cases run twice are not16 unique cases; warnings and reused regression categories are not an added unique acceptance total. |
| Numbered batches completed | 2511 |
| Remaining to old 2000 / 2500 milestones | 0 / 0; historical numbered targets only |
| Total project batches planned / remaining | Unknown / unknown |
| Accepted implementation tasks | 0/1092 (0.00%); 1092 remain |
| Open acceptance items | 1686 |
| Qualified frameworks | 0/66; 2 in progress and 64 not started |
| Git workflow | Feature branch, no-ff merge to master after reviews, then push master and feature; actual merge/push results reported after execution. |
| Next concrete task | Batch-2512: Establish and implement a bounded public Task/completion/awaiting prerequisite with paired native fixtures to unblock CancellationTokenSource.CancelAsync. |

| Bounded work group | Done / selected | Remaining |
|---|---:|---:|
| Original2392–2500 groups | 109/109 | 0 in that group |
| Core/build continuation scopes2501–2509 | 9/9 | Future work unbaselined |
| Packaged build-condition qualification2510 | 1/1 | 0 |
| Warning/cache implementation/qualification2511 | 1/1 | 0 in selected profile |
| Next public Task prerequisite | Selected next scope | Exact future batch count unbaselined |
| Whole project | 2511 completed batches | Unknown; acceptance/task totals above are not batch totals |

Product runtime: JDK APIs, no third-party Java runtime library. Development/reference validation: Python3.13.9, Java/javac/jar21.0.12.1, SDK10.0.401/runtime10.0.12 were independently available on this machine; no download needed. The requested C: candidate build path was absent; verified artifacts are on D:. Broader dependency resolution and the public .j installer/feed remain plans, not released downloads.

All new assets remain under `D:\AI\Implementation\dotj Frameworks`. RooFlow is unavailable; installed subagent-driven-development and agency-agents-orchestrator workflows used at most two active AI agents. Prelaunch timeout-stream and cleanup-executable findings were fixed and independently re-reviewed before either native pass.
