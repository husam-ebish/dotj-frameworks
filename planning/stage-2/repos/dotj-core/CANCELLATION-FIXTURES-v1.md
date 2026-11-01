# Cancellation fixtures

Batch 2505 runs fixtures `DJ-001-F02-01` to `DJ-001-F02-05` against real .NET 10.0.12 `CancellationTokenSource` and the internal Java `CancellationSource`. All 29 observations match.

| Fixture | Criterion | Observed on both sides |
|---|---|---|
| `F02-01` | Late registration runs synchronously | The callback runs on the registering thread before `Register` returns |
| `F02-02` | Sequential callbacks use the LIFO profile | Reverse order, unregister skips a callback, failures aggregate in run order, stop-on-first stops |
| `F02-03` | Self-close cannot deadlock | A callback can close its registration or source; another thread's close waits for the callback |
| `F02-04` | `CancelAsync` completion waits for callbacks | Requested at once, pending while a callback runs, callbacks on another thread |
| `F02-05` | Token identity survives source disposal | A retained token stays readable; `Token` on a disposed source is refused |

## Defect fixed

Registering on a token whose source was canceled and then disposed must still run the callback. `CancellationSource.register` checked `closed` first and dropped it. The fix checks `cancellationRequested` first, and `CancellationDisposeTest` now covers it. A disposed source that was never canceled still ignores the callback, as native does.

## Reproduce

Run `run-comparison.py <new-run-id>` from `tools/oracle/dotj-core/cancellation-fixtures-v1` with the pinned Python. Results are in `evidence/cancellation-fixtures-v1.json`.

## Limits

- The Java side is package-private internal code, not a public `System.Threading` API. Public `Register(Action)` depends on the delegate representation.
- Exception types are not compared: Java `CancellationCallbackException` stands in for `AggregateException`.
- `CancelAsync` uses `CompletableFuture`, not `Task`.
- The check is not yet in the canonical foundation gate. The older internal `run-foundation-gate.py` could not run here because its prebuilt oracle is absent.
- `WP-02` tasks stay open and no acceptance credit is granted.
