# Batch-220 report

| Field | Result |
|---|---|
| Status | COMPLETE (bounded outcome; framework remains IN PROGRESS) |
| Framework | `dotj-core` |
| Plan task | `E03` |
| Outcome | Replaced the long-lived wait cancellation callback with a removable internal signal registration. |
| Validation | Focused async fixture passed source-first, cancellation-first, fault, source cancellation, pre-signaled, and 100 repeated long-lived-signal cleanup checks; 12 Java sources/classes built; combined foundation gate passed. |
| Limitation | This is an internal Java adapter; public .NET cancellation tokens, awaiters, concurrent source-versus-wait ordering, and exact public names remain open. |
| Public API qualification | OPEN; no fully qualified public .j facade. |

## Progress

| Metric | Actual value |
|---|---:|
| Completed implementation tasks | **0 / 1,092 (0.00%)** |
| Remaining implementation tasks | **1,092 (100.00%)** |
| Frameworks fully implemented and qualified | **0 / 66 (0.00%)** |
| In-progress / not-started frameworks | **1 / 65** |
| Batches completed | **220** (`Batch-001` through `Batch-220`) |
| Batches still to do | **At least 66**; exact total is not baselined |
| Next proposed batch | `Batch-221`: Test concurrent source-completion versus wait-cancellation ordering. |
| Progress measure | Equal-weight WP and SDK integration task completions; prerequisite gates excluded; partials receive zero credit. |

## Tooling and naming questions

| Question | Answer |
|---|---|
| Why Python changes? | Python under `tools/oracle` runs pinned-source checks, Java probes, and the combined gate; `tools/progress` updates evidence and batch reports. It is development tooling, not code in the framework JAR. |
| Why `.csproj` changes? | The `.csproj` files define small standalone .NET oracle programs. They select the pinned runtime and let us compile C# observations against the actual CoreLib. They are not part of the Java product. |
| Why C# changes? | C# oracle code records selected .NET API shapes and behavior before mapping them to internal Java fixtures. It is reference evidence, not the framework implementation or a claim of Java parity. |
| Why `final class AsyncCompletion<T>` rather than `CompletionAsync<T>`? | `final` is Java's non-inheritance modifier; the class name is `AsyncCompletion`. It is package-private state machinery, not a public .NET API. The upstream public concept is `TaskCompletionSource` / `TaskCompletionSource<TResult>`, so renaming a public type to `CompletionAsync<T>` would violate the [exact-name policy](../../repos/dotj-core/ADRS.md). Java cannot declare the generic and non-generic types under one simple binary name in the same package; their public representation remains unresolved. Internal methods such as `waitAsync` also do not qualify a public `WaitAsync` API. |

## Files changed

| Path | Purpose |
|---|---|
| `dotj-core/dotj-core-01/src/main/java/org/dotj/internal/async/WaitCancellationSignal.java` | Removable wait cancellation registration and bounded evidence. |
| `dotj-core/dotj-core-01/src/main/java/org/dotj/internal/async/AsyncCompletion.java` | Removable wait cancellation registration and bounded evidence. |
| `dotj-core/dotj-core-01/src/test/java/org/dotj/internal/async/AsyncWaitTest.java` | Removable wait cancellation registration and bounded evidence. |
| `tools/oracle/dotj-core/build-internal-core.ps1` | Removable wait cancellation registration and bounded evidence. |
| `tools/oracle/dotj-core/run-foundation-gate.py` | Removable wait cancellation registration and bounded evidence. |
| `planning/stage-2/repos/dotj-core/evidence/async-state-map-v10.0.12.md` | Removable wait cancellation registration and bounded evidence. |
| `planning/stage-2/repos/dotj-core/evidence/internal-core-jar-v1.json` | Removable wait cancellation registration and bounded evidence. |
| `planning/stage-2/repos/dotj-core/evidence/foundation-gate-v10.0.12.json` | Removable wait cancellation registration and bounded evidence. |
| `planning/stage-2/repos/dotj-core/WP01-WP02-READINESS-v10.0.12.md` | Removable wait cancellation registration and bounded evidence. |
| `tools/progress/record-implementation-batch.py` | Removable wait cancellation registration and bounded evidence. |
| `planning/stage-2/IMPLEMENTATION-STATE.md` and `IMPLEMENTATION-PROGRESS.json` | Continuity and counts. |
| `planning/stage-2/implementation/batches/Batch-220.md` | This report. |

**STOPPED. Waiting for your CONTINUE signal before starting the next batch.**
