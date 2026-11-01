# Ownership source lifecycle oracle

Batch 2502 pairs the original Java `LifecycleConsumer`, `Owner`, `Resource` and `Producer` fixtures with a matched native program for `DJ-001-WP-01-T2` and `DJ-001-F01-03`.

## Result

The C# oracle ran on .NET 10.0.12 CoreLib `1125acc8...`, compiled with SDK 10.0.401. The comparison status is `PASS_MATCHED_LIFECYCLE_OBSERVABLES`: all 10 counters, the 14 guard observations and the route, token and flag values match the reviewed Java proof `d7caf568...`.

| Behavior | Observed on both sides |
|---|---|
| Owned resource | Disposed once, including through a repeated owner `DisposeAsync` |
| Borrowed resource | Not disposed or closed by the owner; disposed only by the caller |
| Pending completion | Genuinely pending `IValueTaskSource`, token -8, registered through `ConfigureAwait(false).UnsafeOnCompleted` with flags 0 |
| Failure before return | The same exception instance is thrown from `DisposeAsync` |
| Source fault | The same exception and cause instances surface from `GetResult` |
| Cleanup failure | A failure in `finally` replaces the body exception |

The native program replaces the earlier unmatched evidence, which used token 0, flags 3 and Task-backed faults.

## Reproduce

Run `run-capture.py <new-run-id>` from `tools/oracle/dotj-core/ownership-source-lifecycle-v1` with the pinned Python. `test_compare.py` holds 20 synthetic comparator controls. Evidence is in `evidence/ownership-source-lifecycle-v1`.

## Limits

- The Java side ran on a private runtime JAR, so this is not public API qualification. The public candidate still has no `System.IAsyncDisposable` or `System.Threading.Tasks.ValueTask`.
- `ZeroConsumer` stays blocked: its instance field initializer has no direct C# form (CS0236).
- Execution context, scheduling flags, concurrency and races are not covered.
- The check is not yet in the canonical foundation gate.
- `DJ-001-WP-01-T2` and `DJ-001-F01-03` remain open, and no acceptance credit is granted.
