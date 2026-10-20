# WP-01/WP-02 bounded readiness at Batch-216

Reference: .NET runtime `v10.0.12`, source commit `4271d88e0aebf3d04f188f1334c2220d80555ef6`, installed CoreLib SHA-256 `1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678`.

| Area | Verified here | Remaining gate |
|---|---|---|
| E01 source and rights | Pinned archive, runtime artifact, selected MIT headers, [candidate distribution scope](evidence/idisposable-distribution-scope-v10.0.12.md), byte-matched notices, and a [file-level map](evidence/idisposable-file-notice-map-v10.0.12.json) checked against a deterministic two-entry compile-only JAR. | Actual product package contents, project license, notice applicability, generated/transitive inputs, and required licensing review are open. No release clearance is claimed. |
| E02 API inventory | Seven WP-01 and seven WP-02 selected declared-public CoreLib shapes reconcile with pinned source hashes. [Async arity evidence](evidence/task-family-arity-v10.0.12.json) verifies three non-generic/generic pairs against six pinned source files and installed CoreLib metadata. | Conditional/source-generated APIs, inherited members, dependency graph, and full semantic mapping remain open. |
| E03 behavior | [Combined gate](evidence/foundation-gate-v10.0.12.json): 12 WP-01 Java fixtures (including 25 boundary assertions), 5 .NET oracles, 15 WP-02 internal Java fixtures (including 26 boundary assertions), 10 selected pinned cancellation tests, and [25 selected Task/ValueTask reference cases](evidence/task-behavior-v10.0.12/oracle-output.json) pass. An external Java consumer dispatches through the compile-only `System.IDisposable` JAR. | Selected reference observations do not establish Java parity and do not cover all ownership, Task/ValueTask, callback races, platform conditions, or error semantics. |
| N01 names | `IDisposable`, `IAsyncDisposable` and three cancellation names compile as syntax-only Java probes; the `IDisposable` probe also compiles into a two-entry candidate JAR whose `javap` shape matches the selected source identity. [WP-02 ledger](evidence/wp02-n01-candidate-v10.0.12.json) preserves seven exact source identities. Three Java compiler probes confirm exact-name collisions for the `Task`, `TaskCompletionSource`, and `ValueTask` non-generic/generic pairs. | CLR value types, Task generic/non-generic naming, ambient context, `ValueTask`, and exact exception behavior need a qualified public .j representation and compiled API comparison. |
| WP-01 implementation | Internal ownership, type identity, and explicit context helpers compile and pass bounded fixtures covering cleanup order/failures, context limits, and generic identity boundaries. | No public `System` facade or complete WP-01 contract. |
| WP-02 implementation | Eight internal foundation source files build into a repeatable JDK-only JAR; the cancellation prototype covers registration, LIFO dispatch, late callbacks, unregister, blocking close, async completion, reset, linked sources, and timer cases. Null linked-parent input is now validated before any parent callback is registered. | Internal `CompletableFuture` and Java exceptions are not public .NET `Task`/`AggregateException` substitutes; `DisposeAsync`, full Task/ValueTask state/awaiter behavior, context dispatch, and wider race tests remain open. |
| Q01 release | None. | Public API, integration, distribution, and release gates are not qualified. |

| Progress measure | Result |
|---|---:|
| Completed equal-weight implementation tasks | **0 / 1,092 (0.00%)** |
| Qualified frameworks | **0 / 66 (0.00%)** |
| In-progress frameworks | **1** |
| Completed batches | **216** |
| Further batches | **At least 66** to touch 66 unqualified frameworks; exact total is not baselined. |

The task percentage counts completed WP and SDK integration task IDs, not elapsed effort. Every task touched here remains in progress because its required public contract or qualification is incomplete. The next bounded technical step is to map the selected `Task`/`ValueTask` state transitions to an internal Java prototype while the public generic/non-generic naming decision remains open. The separate product licensing review is still required before public release qualification.
