# Batch-2509: Public async disposal and selected nongeneric ValueTask

| Field | Result |
|---|---|
| Status | COMPLETE bounded implementation and verification; qualification remains open |
| Framework / plan scope | dotj-core / DJ-001-WP-01-T2 and DJ-001-WP-02-T1 |
| Implemented | IAsyncDisposable, nongeneric ValueTask, source status/flags, completion interfaces, direct/configured awaiters and Action_1 continuation carrier; 12 new Java product sources |
| Corrected after review | Virtual source hash dispatch; completed-value null continuations; invalid source callback state exception behavior. Source-backed null registration still passes through to the source. |
| Targeted validation | Genuine RED: 22 differences among 135 observations. GREEN: all 135 match, including the original 83 plus 52 boundary observations. Seven comparator parser controls passed. |
| Packaged validation | All 135 native/Java observations match using fixture-only compilation against the final JAR, without a public-source fallback. |
| Canonical validation | All 515 checks passed on 130 product sources in isolated Batch-2509-gate2; all retained checks executed with three supported independent workers. |
| Candidate JAR SHA-256 | `11a470a1e9210815981f57deba1712caa354c389e34573e2b448b74c38519e70` |
| Independent review | Task review, scoped fix re-review and whole-branch review passed; original cmp1/gate1/RED evidence retained. |
| Limitations | No Task, AsTask, Preserve, generic ValueTask, struct copying, ExecutionContext capture or scheduling-context posting. Java constructor helpers and generic delegate identity/combination qualification gaps are documented. |
| Acceptance credit | None; no implementation task or framework accepted |
| Numbered batches completed | 2509 |
| Remaining to original 2000 / old 2500 targets | 0 / 0; these are historical numbered milestones |
| Total project batches planned / remaining | Unknown / unknown |
| Accepted implementation tasks | 0/1092 (0.00%); 1092 remain |
| Open acceptance items | 1686 |
| Qualified frameworks | 0/66; 2 in progress and 64 not started |
| Git workflow | Feature branch; merge to master after verification, then push master and feature. Actual merge and push results are reported after execution. |
| Next concrete task | Batch-2510: Implement bounded Or and mixed And/Or precedence with explicit predecessor transitions and packaged regression qualification. |

| Work group | Batches done / selected | Remaining |
|---|---:|---:|
| Exceptions, nullable, serialization, methods, fields, enums and integration (2392–2500) | 109/109 | 0 in that bounded group |
| Public foundation scopes recorded in 2501–2509 | 9/9 | Further Task/context/ownership scopes not yet batch-baselined |
| Build condition composition | And feature merged; Or reference pair qualified | Or implementation and packaged qualification pending |
| Whole project | 2509 completed batches | Unknown; acceptance counts above are not batch counts |

The Java candidate uses JDK APIs and has no third-party Java runtime library dependency. Python and pinned .NET SDK 10.0.401/runtime 10.0.12 are development/reference-validation tools. No new dependency download was required. The broader dependency graph and public .j installer/feed remain open plans. MIT is selected; three E01 decisions remain open.

All new builds, temporary files, downloads, caches and logs stay under `D:\AI\Implementation\dotj Frameworks`. RooFlow is unavailable; the installed subagent-driven-development and agency-agents-orchestrator workflow was used with at most two active AI agents.
