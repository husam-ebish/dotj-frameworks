# PUBLIC-TASK-N01-v2

Status: implemented selected nongeneric Task prerequisite, with targeted candidate-JAR qualification. Independent task review, the canonical foundation gate and final gate-JAR qualification remain pending. No batch, task, scenario or framework acceptance credit is claimed.

This is the current implementation contract. [PUBLIC-TASK-N01-v1.md](PUBLIC-TASK-N01-v1.md) remains the immutable historical preparation/fixture contract, including its preparation-time status. Its selected surface, native source anchors, 61 scenario rows, 697 typed observations and exclusions remain binding. V2 changes no frozen expectation.

## Implemented surface and state

The six product sources are `Task`, `TaskCompletionSource`, `TaskStatus`, `TaskCanceledException`, `TaskAwaiter` and `org.dotj.internal.async.TaskBridge`. Public native-shaped members are exactly the V1 selected nongeneric surface. `Task` has no public constructor or completion setter. The default `TaskCompletionSource` owns one stable Task; `CompletedTask` returns the implementation's stable successful instance.

The promise starts in `WaitingForActivation`. One producer wins success, single-exception fault or cancellation. A monitor serializes completion and continuation registration. The winner writes its original exception or cancellation token, detaches callbacks, publishes volatile terminal status and wakes result waiters before any user callback runs. Losing producers see the fully published terminal payload. `SetException(null)` and `TrySetException(null)` validate before checking completion. Duplicate Set calls throw the observed `InvalidOperationException`; Try calls return false.

The `Exception` property wraps the original fault in a new `AggregateException`. Awaiting throws that original object without flattening or inferring cancellation from an `OperationCanceledException`. Canceled tasks have a null `Exception` property. Awaiting cancellation creates a `TaskCanceledException` that retains the original Task and the recorded token. Canceling a promise does not cancel its token source. `TaskCanceledException(null)` retains null and the None token.

Pending `GetResult` waits for completion. JVM interruption does not abandon that obligation: the wait loop records interruptions and restores the flag in a finally block after success or either failure outcome. There is no new public Wait API.

## Java representation and dispatch

Each Task owns an anonymous instance of the read-only abstract `TaskBridge`; it exposes only completion observation, result consumption and continuation registration. There is no static installation protocol, reflection-based product access or global registry of tasks. The Java-public `TaskAwaiter(TaskBridge)` constructor and `org.dotj.internal` bridge are representation infrastructure, not additional native API. A caller-provided bridge can construct its own awaiter but cannot obtain producer authority over an existing Task. Exact native constructor/reflection/struct-default parity is not claimed.

Within the selected default-context, shallow-stack profile, a pending first callback runs inline on the completing thread. Second and later callbacks are queued before that first invocation. Late registration always queues. Duplicate Actions represent separate registrations. Terminal state is visible to callbacks, and callbacks execute outside the state monitor, so reentrant late registration is safe. Completion order and FIFO scheduling are not promised.

The private cached daemon-thread executor uses synchronous handoff. A blocked queued callback does not consume a fixed pool's last worker and serialize every later callback. Idle workers expire under the JDK executor policy. This is a Java adaptation, not a CLR thread-pool, fairness or resource-budget guarantee. As with other daemon work, JVM shutdown does not wait for these callbacks.

A rejected submission falls back to a new daemon thread. That thread reports the original rejection to its uncaught-exception handler, then invokes the callback in a finally block. A handler that throws therefore cannot discard the callback. This policy is exercised through a package-private dispatch seam with a rejecting executor; there is no replaceable global executor or public System mutation hook.

An exception thrown by a callback does not change terminal state or escape the completing call under normal thread-creation conditions. It is reported on a distinct daemon thread through that thread's uncaught-exception handler. Other callbacks remain independently dispatched. JVM handler behavior and CLR process-fatal unhandled-exception behavior are not equivalent and are not compared.

Catastrophic JVM inability to create a worker or failure-reporting thread, including resource exhaustion or thread-creation denial, remains an explicit boundary. Such failure is observable and may escape the calling operation after terminal publication; no delivery guarantee is claimed when the JVM cannot create the required thread. Completion attempts dispatch the remaining queued callbacks even if one dispatch fails, then run the first callback and surface the dispatch failure. The terminal payload is never rolled back.

Java null `CancellationToken` has no native value-type equivalent. Token-bearing producer overloads reject it with `ArgumentNullException("cancellationToken")`, even after completion; this is a representation-input policy, not a native observation. A null bridge passed to the representation-only awaiter constructor is rejected with Java `NullPointerException`.

## Evidence and packaging boundary

Root captured the native oracle once and froze its 61 rows / 697 scalar observations. The receipt SHA-256 is `7fb57ab11bb269cb2dea414eccb4a2bca5957a010f6a8c926092d0e7b6772392`; the root observation lock SHA-256 is `b76d0ec179c4d2ac4df23a5b277f7f2c34c93262a3f876b5e1873171f5056007`. The input lock SHA-256 is `7c2e2fceec39377023bbdee0a86990a51ff92412601be55583a13db107f46615`. All eight prepared source/tool/contract inputs remain byte-identical. No native, SDK or C# compiler process was launched during implementation.

The actual baseline candidate JAR lacked Task/TCS/awaiter APIs and failed javac before implementation; root retained the raw diagnostics and receipt. Targeted packaging imports the canonical builder's explicit 136-source and exact class inventories, verifies all 130 old product source hashes, compiles with the pinned JDK and uses the canonical deterministic archive recipe. The targeted JAR contains seven added classes, including the anonymous Task bridge, and no fixture classes.

The frozen paired Java fixture compiled alone against that actual JAR with `-implicit:none`, an empty source path and no product-source fallback. All 697 scalar observations matched. Separate Java boundary controls passed 49 checks: all six new product classes originate in the supplied JAR; consumer-first bridge initialization; no public Task mutation; interrupted pending results for success/fault/cancellation; asynchronous original callback failure handling; independent blocked queued callbacks; observable rejection fallback; and preservation of the callback when the rejection handler throws. The frozen comparator/ownership suite passed 69 deterministic controls. See [public-task-v1.json](evidence/public-task-v1.json) for hash-bound raw receipts.

These are targeted results, not the canonical gate. The source-to-class map has been extended for the six sources/seven classes, while its canonical artifact hash and `foundation-product-candidate-v1.json` remain the historical baseline pending root's actual canonical gate/export/binding. Targeted packaging does not fabricate that gate evidence. Root owns the retained 515-check gate, frozen Task and boundary reruns on its actual JAR, and same-JAR delegate/cancellation/ValueTask regressions.

## Remaining scope

All V1 exclusions remain: generic Task/TCS, creation options, schedulers and contexts, execution-context capture, configured Task awaiting, computational Task constructors/factories, explicit Wait APIs, exception collections, async builders and broad API/reflection parity. Task-backed ValueTask conversion and `CancellationTokenSource.CancelAsync` are still separate unimplemented integrations. This batch supplies their producer/consumer prerequisite only.
