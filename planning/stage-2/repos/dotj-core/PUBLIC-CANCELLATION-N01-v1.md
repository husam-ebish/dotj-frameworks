# Public cancellation

Batch 2508 adds the first public `System.Threading` types for `DJ-001-WP-02-T1` and `DJ-001-WP-02-T2`, using the delegate form chosen in Batch 2507.

```java
CancellationTokenSource source = new CancellationTokenSource();
CancellationToken token = source.get_Token();
CancellationTokenRegistration registration = token.Register(new Action(() -> Log()));
source.Cancel();
registration.Dispose();
```

## Selected public surface

| Type | Members |
|---|---|
| `CancellationToken` | Constructors, `None`, `IsCancellationRequested`, `CanBeCanceled`, `Register(Action)`, `ThrowIfCancellationRequested`, equality, `op_Equality`, `op_Inequality` |
| `CancellationTokenSource` | Constructors, `Token`, `IsCancellationRequested`, `Cancel`, `CancelAfter`, `TryReset`, `CreateLinkedTokenSource`, `Dispose` |
| `CancellationTokenRegistration` | `Token`, `Unregister`, `Dispose` |
| Exceptions | Selected `OperationCanceledException`, `ObjectDisposedException` and `AggregateException` members |

`PublicCancellationFixtures.java` uses only these public names, and `PublicCancellationOracle.cs` runs the same scenarios on .NET 10.0.12. All 48 observations match, including exception types, HRESULT values and messages.

## Syntax differences

- Properties use accessors such as `get_Token()`.
- Operators use `op_Equality` and `op_Inequality`.
- `CancellationToken` and `CancellationTokenRegistration` are Java classes, so copies share identity. Token equality still compares the source.

## Limits

- The current Batch-2514 candidate implements selected `CancelAsync` and its callback-completion integration, including late empty registrations and disposed-source messages. See [the selected contract](PUBLIC-WORKTASK-CANCELASYNC-N01-v1.md); independent review, full gate and final-artifact qualification remain pending.
- `WaitHandle`, `Register` state overloads, `UnsafeRegister` and `ExecutionContext` capture are not provided.
- `F02-04` therefore remains internal only, and `Cancel` catches only `System.Exception` callback failures.
- No acceptance credit is granted.
