# Public IAsyncDisposable and ValueTask

Batch 2509 adds the public async disposal contract and the nongeneric `ValueTask` for `DJ-001-WP-01-T2` and `DJ-001-WP-02-T1`. Both previously existed only in a private runtime JAR.

```java
ValueTask pending = new ValueTask(source, token);
pending.ConfigureAwait(false).GetAwaiter().UnsafeOnCompleted(new Action(() -> resume()));
```

## Selected public surface

| Type | Members |
|---|---|
| `System.IAsyncDisposable` | `DisposeAsync` |
| `System.Action_1<T>` | Lambda constructor, `Invoke(T)`, delegate combination |
| `ValueTask` | Default and `(IValueTaskSource, short)` constructors, `CompletedTask`, `IsCompleted`, `IsCompletedSuccessfully`, `IsFaulted`, `IsCanceled`, `GetAwaiter`, `ConfigureAwait`, equality, `GetHashCode` and operators |
| `ValueTaskAwaiter`, `ConfiguredValueTaskAwaitable` | `IsCompleted`, `GetResult`, `OnCompleted`, `UnsafeOnCompleted` |
| `IValueTaskSource`, `ValueTaskSourceStatus`, `ValueTaskSourceOnCompletedFlags` | The full source contract, with raw Int32 enum carriers |
| `INotifyCompletion`, `ICriticalNotifyCompletion` | The completion contracts |

`PublicValueTaskFixtures.java` uses these selected members, and `PublicValueTaskOracle.cs` runs the same scenarios on .NET 10.0.12. The paired probes cover completed, pending, succeeded, faulted, canceled and unknown source states, status and result call counts, source tokens, equality and hashes, and the flags each awaiter passes to the source: `OnCompleted` passes 3, `UnsafeOnCompleted` passes 1, and `ConfigureAwait(false)` passes 2 and 0. Continuations of a completed value run on another thread, and a source that is already done runs inline. Fix-round probes additionally cover virtual source hash dispatch, hash override call counts and thrown exception identity, all six completed null-continuation paths, source-backed null registration, and captured callbacks receiving null or the wrong state type. The evidence record reports the matched observation count and identifies source or packaged-candidate qualification.

## Representation

- A .NET generic `Action<T>` becomes `Action_1<T>`, because Java cannot give one name two arities. This is a recorded N01 representation gap.
- `ValueTask` is a Java class, so it copies by reference. Equality still compares source and token.
- Awaiters reach `ValueTask` state through `org.dotj.internal.async.ValueTaskBridge`.
- The public Java constructors `ValueTaskAwaiter(ValueTask)` and `ConfiguredValueTaskAwaitable(ValueTask, boolean)` are representation helpers; their native counterparts are internal. They are outside the selected surface table. Exact public API or reflection parity is not claimed.

## Limits

- The selected public nongeneric `Task` prerequisite now exists. The selected `AsTask`, `Preserve` and `new ValueTask(Task)` integration is defined in [the Task lifetime contract](PUBLIC-VALUETASK-TASK-N01-v1.md); current status belongs to Batch-2515. The Batch-2514 candidate implements selected `CancelAsync`; see [the current contract](PUBLIC-WORKTASK-CANCELASYNC-N01-v1.md). Independent task review approved; root canonical gate passed 516/516 checks and verified the identical final JAR. Whole-branch review and root integration/merge/push remain pending. No acceptance credit is claimed.
- Generic `ValueTask<T>`, `ValueTaskAwaiter<T>`, `ManualResetValueTaskSourceCore` and `ExecutionContext` capture are not provided.
- Scheduling-context posting is not implemented: the flags are passed to the source, but this layer does not post to a `SynchronizationContext`.
- Struct copy semantics are not claimed.
- The source-based comparator does not qualify the packaged JAR. Its optional `--candidate-jar PATH` mode compiles only the Java fixture against that JAR with `-implicit:none`, then runs with fixture classes and that JAR; the record binds the JAR, fixture and runner hashes.
- `Action_1<T>` delegate combination and runtime generic-instantiation identity are not established by these continuation probes.
- No acceptance credit is granted.
