# WP-01 explicit context transfer contract

Status: bounded internal adaptation, 2026-10-20. No public `ExecutionContext` or `SynchronizationContext` equivalent is qualified.

| Question | Pinned .NET 10.0.12 observation | Current internal Java behavior |
|---|---|---|
| What moves to scheduled work? | `AsyncLocal` flows into `Task.Run` through captured `ExecutionContext` by default. | Only a caller-selected `ContextSnapshot` argument moves through `ContextTransfer.execute`. |
| When is the value selected? | The two scheduled tasks observed their respective scheduling values, `A` and `B`. | The deferred executor fixture received the snapshot selected at scheduling time. |
| Can ambient flow be suppressed? | `ExecutionContext.SuppressFlow` produced a null `AsyncLocal` observation in the bounded oracle. | There is no ambient capture to suppress. The caller may pass an empty snapshot. |
| Are requests isolated? | The bounded oracle observed `A` then `B`; it did not test the full CLR ambient-context surface. | The reused-worker fixture observed explicit `A` then `B` even while a stale `ThreadLocal` value was present. |

The only common acceptance observation for designed fixture `DJ-001-F01-04` is that request B must not receive request A's selected value. The two mechanisms are **not interchangeable**: the Java helper has string-only bounded values and never copies arbitrary thread locals. A future public API must retain exact upstream names and pass its own E02/N01 review. [Fixture status](evidence/wp01-fixture-corpus-v10.0.12.json) remains partial because upstream context tests have not been mapped or executed and broader CLR behavior is unverified.

Evidence: [independent .NET oracle](evidence/context-flow-oracle-v10.0.12.json), `ContextSnapshotTest`, `ContextTransferTest`, and `ContextIsolationTest` in `dotj-core-01`.
