# PUBLIC-TASK-N01-v1

Status: source-backed static preparation for Batch 2512. No native capture, compiler execution, public implementation or accepted scenario is claimed. This is a nongeneric producer/consumer prerequisite for DJ-001-F02-04; CancelAsync remains unimplemented.

## Selected public surface

### System.Threading.Tasks.Task

```csharp
static Task CompletedTask { get; }
TaskStatus Status { get; }
bool IsCompleted { get; }
bool IsCompletedSuccessfully { get; }
bool IsFaulted { get; }
bool IsCanceled { get; }
AggregateException? Exception { get; }
TaskAwaiter GetAwaiter()
```

Same namespaces/casing; properties become get_*. No selected public Task constructor. Creation is owned by TCS and private CompletedTask factory. Do not add public completion/setter helpers or fake Task.Run/Wait/Dispose implementations.

### System.Threading.Tasks.TaskCompletionSource

```csharp
TaskCompletionSource()
Task Task { get; }
void SetResult()
bool TrySetResult()
void SetException(System.Exception exception)
bool TrySetException(System.Exception exception)
void SetCanceled()
void SetCanceled(CancellationToken cancellationToken)
bool TrySetCanceled()
bool TrySetCanceled(CancellationToken cancellationToken)
```

Same names; get_Task returns same owned instance. Exception means System.Exception, not arbitrary java.lang.Throwable. Default constructor only.

### System.Runtime.CompilerServices.TaskAwaiter

```csharp
bool IsCompleted { get; }
void GetResult()
void OnCompleted(System.Action continuation)
void UnsafeOnCompleted(System.Action continuation)
```

Follow class-backed ValueTask awaiter and existing System.Action convention. Native constructor is internal; any necessary Java public constructor is explicitly a representation helper outside selected native API. Do not introduce java.lang.Runnable as the public .NET continuation type.

### System.Threading.Tasks.TaskStatus

```csharp
enum TaskStatus { Created=0, WaitingForActivation=1, WaitingToRun=2, Running=3, WaitingForChildrenToComplete=4, RanToCompletion=5, Canceled=6, Faulted=7 }
```

Use existing raw Int32 carrier convention, constants/Equals/$raw/hashCode; raw values are data, never interpreted as permission to create unsupported states.

### System.Threading.Tasks.TaskCanceledException

```csharp
TaskCanceledException(Task? task)
Task? Task { get; }
```

Selected constructor accepts null task, retains exact task reference, copies its cancellation token, sets native default message via base; inherited HRESULT is COR_E_OPERATIONCANCELED. Other native constructors and serialization are not required by this slice.

TaskStatus is the existing raw Int32-carrier style with all eight native constants (0 through 7). Only WaitingForActivation, RanToCompletion, Canceled and Faulted are reachable through this selected producer. No public Task constructor is selected. TaskAwaiter implements existing ICriticalNotifyCompletion and inherited INotifyCompletion. A Java constructor/bridge required by the class representation is representation infrastructure, not extra native API.

## Selected semantics

**identity**: TCS.get_Task is stable, distinct producers own distinct tasks, callers cannot complete a Task without its producer. CompletedTask is successful; native repeated property reference identity is an implementation observation, not a general .NET contractual guarantee.

**state**: Default TCS promise starts WaitingForActivation(1), all four terminal predicates false, Exception null. Exactly one terminal transition succeeds to success5/cancel6/fault7. Set variants throw native InvalidOperationException on an already terminal task, Try variants return false. Task is fully terminal when any competing completion method returns. This does not require all asynchronous callbacks to have finished.

**atomicity**: Serialize/reserve and publish exception or token before exposing final status. Losers must see fully published winner state. Registration and terminal transition share one coherent linearization so no callback is lost or invoked twice. Detach callbacks and wake waiting GetResult callers before executing arbitrary callbacks; never invoke user code under state lock. Volatile/monitor or equivalent happens-before must make payload visible.

**fault**: Validate null exception before checking completion (including after success/cancel/fault). Fault stores original exception reference; Exception property is an AggregateException containing that exact object. Awaiter rethrows original exception, without wrapping or flattening. Passing an OperationCanceledException or an AggregateException to SetException still produces Faulted; it does not infer cancellation or flatten nested aggregates. Do not require repeated Exception aggregate wrapper identity.

**cancel**: SetCanceled(token) cancels regardless of whether supplied token was signaled. Preserve token value/source identity. Cancellation does not request cancellation on that token source. Exception property remains null. Each GetResult throws TaskCanceledException whose Task is original Task and whose token Equals the recorded token; do not require repeated thrown TCE identity. Default SetCanceled uses CancellationToken.None.

**getResult**: Returns void on success, throws original fault, or creates TCE on cancellation. Pending direct GetResult must wait for terminal publication; do not throw InvalidOperationException for pending Task and do not return early. Explicit public Wait/timeout/wait-all APIs remain deferred. JVM interruption behavior has no selected native equivalent and is an explicit adaptation; use a completion loop and restore Java interrupt flag rather than abandoning the native completion obligation.

**continuations**: Native default-context shallow-stack profile: single registered pending await continuation may inline on completion thread. Native list algorithm queues second and later await continuations before invoking first; therefore callback completion order is not guaranteed FIFO. Registration after completion always queues rather than invoking inline on registering stack. Use existing Action.Invoke, preserve duplicate registrations as separate callbacks, publish terminal state before dispatch, and support callback reentrancy/late registration without holding state lock. No custom context/scheduler/capture claimed.

**queuePolicy**: Use JDK executor support as an explicit Java adaptation (existing ValueTask uses ForkJoinPool.commonPool). Enqueued callbacks execute independently; do not serialize all behind a blocked first callback, silently drop accepted callbacks, swallow queue rejection or invent deterministic order. Any fallback/rejection behavior must be documented and verified at Java boundary; native thread-pool equivalence is not claimed.

**callbackFailures**: Native TaskContinuation.cs catches callback exceptions and routes Task.ThrowAsync; they do not change Task terminal state or escape SetResult/TrySetResult. Product dispatch must similarly keep completion stable and preserve other callbacks; route failure to explicit asynchronous uncaught-exception handling. Exact CLR unhandled exception/process-termination policy is excluded, and normally-returning callbacks define paired success profile. No broad catch-and-ignore allowed.

**bridge**: One internal org.dotj.internal.async.TaskBridge is allowed for cross-package await access only. Public System.* types gain no invented state getters/setters. Completion entry points remain package-private to Task/TCS; bridge exposes only observation/result/continuation operations. Prefer instance state with no publicly replaceable global installer; if following ValueTask Access pattern, demonstrate initialization safety and one-time installation, and classify Java-public internal infrastructure as representation-only. Ensure normal first use from Task/TCS/awaiter has no uninitialized access. Do not use reflection or a global task-retaining registry to avoid ordinary visibility design.

**arity**: Nongeneric exact names selected. Existing evidence proves same-name arity collisions; Task_1 is compile-only internal candidate, not an approved public replacement. Add no generic placeholder or declarations, and claim neither generic source lowering nor complete native public API parity.

## Source and observation boundary

Authority: dotnet/runtime commit `4271d88e0aebf3d04f188f1334c2220d80555ef6`. The following unmodified files and source anchors are independently hash-checked. Installed .NET 10.0.12 behavior must still be captured; source-to-installed-byte reconstruction is not claimed.

| Source | SHA-256 | Anchors |
| --- | --- | --- |
| `src/libraries/System.Private.CoreLib/src/System/Threading/Tasks/Task.cs` | `5b0d6892267269233dcf5c6191f357b0ba6c4257d1e757ca4d2fe93272b29d9b` | 27-69 TaskStatus ordinal constants 0..7; 316-345 promise initialization and option boundary; 1248-1305 Exception and Status; 1375-1408 completion predicates and loser publication wait; 1470 CompletedTask; 2440-2443 GetAwaiter; 2484-2550 registration and late queue; 3336-3440 terminal atomic reservation/payload publication; 3442-3595 continuation sentinel, first inline and later queued |
| `src/libraries/System.Private.CoreLib/src/System/Threading/Tasks/TaskCompletionSource.cs` | `f2e62b5b0dc67fdd2715c49acc5c9474db77c61c47bf5cd88edcab76e27a3e55` | 33-37 class and default constructor; 89-93 Task identity; 104-163 single exception validation and completion; 243-275 result completion; 289-352 cancellation completion; other constructors, enumerable and SetFromTask deliberately deferred |
| `src/libraries/System.Private.CoreLib/src/System/Runtime/CompilerServices/TaskAwaiter.cs` | `24276f05a960c41c7b074713aa84cb01cae4672f89e225b6dcd2fe9b297a3a39` | 20-78 TaskAwaiter and completion callbacks; 90-123 pending GetResult waits; 125-163 cancellation and first-fault rethrow; 174-198 continuation null validation |
| `src/libraries/System.Private.CoreLib/src/System/Threading/Tasks/TaskCanceledException.cs` | `aa4c4341e6202943b5fcee0ff76e6183ba2c260b1bccfa65cf42957b88849328` | 24-28 base type and task field; 72-76 nullable Task constructor and token; 98 Task property |
| `src/libraries/System.Private.CoreLib/src/System/Threading/Tasks/TaskContinuation.cs` | `21c12b75b72d0ed3579a2533dad7d6ecc6997b19ffd5a7daf7a3bba1c381f53a` | 604-618 default-context inlining eligibility; 727-752 continuation execution and asynchronous exception dispatch |
| `src/libraries/System.Private.CoreLib/src/Resources/Strings.resx` | `1d109264f46cab42c410771f08d213d61676b747827aa42d72c2d2306f5decd9` | 3599 TaskCanceledException_ctor_DefaultMessage; 3629 TaskT_TransitionToFinal_AlreadyCompleted |

The source default messages are `A task was canceled.` and `An attempt was made to transition a task to a final state when it had already completed.` Null argument names, exception class/message/HResult, fault object identity, cancellation-token equality and Task identity are separate exact scalar observations. The native capture—not Java—supplies frozen exception observations.

## Prepared fixture and execution profile

The explicit typed schema contains **61 scenario rows and 697 paired scalar observations**, plus one native runtime metadata scalar. PT01=3, PT02=22, PT03=3, PT04=5, PT05=20, PT06=3, PT07=3, PT08=2. The two race rows each run 32 bounded rounds; 64 rounds are not 64 acceptance cases. The root approved 689→697 scalar expansion before capture to cover the selected default and token-bearing TrySetCanceled overloads; scenario count stayed 61.

Each fixture independently calls its runtime public Task APIs. A preparation-only shared scenario-body authoring template produces C# and Java source; runtime adapters map public properties, Action and bounded synchronization. The schema is explicit, not inferred from native output. It rejects missing, duplicate, extra, malformed and empty keys, type errors and unexpected runtime. Only CRLF/LF line framing and canonical base64 string decoding are allowed; no semantic normalization or broad string substitution.

The pending single-callback profile uses a dedicated/default-context completing stack. The held-first test queues the additional callback before the first callback is released; no FIFO is asserted. Late registration compares a thread-identity relation within the same process, never cross-runtime thread IDs. Pending GetResult is confirmed on an owned worker in its waiting state before producer release. All waits/joins are bounded at five seconds; finally paths release barriers and terminal producers. Fixture callbacks catch and retain fixture failures to avoid accidentally testing CLR process-fatal behavior.

Native capture uses pinned direct `dotnet exec csc.dll`, net10.0 reference assemblies, SDK 10.0.401/runtime 10.0.12 and English/invariant formatting. No restore, network, SDK build or repeated automatic capture. JAR validation compiles the fixture alone with `-implicit:none`, an empty D-only source path, and only the supplied actual candidate JAR on the classpath. The runtime classpath is fresh fixture classes plus that same JAR. Binary/source/manifest/compiled artifact hashes are verified before and after relevant steps.

Fresh physical/available-commit floors are 512 MiB/16 GiB. A local GlobalMemoryStatusEx query has a two-second freshness limit, a resource wait is at most 120 seconds, and every heavy launch rechecks age. Native heap=128 MiB, managed processors=2, runtime timeout=30 seconds; JVM heap=128 MiB, active processors=2, runtime timeout=120 seconds; compiler timeout=120 seconds. These are runtime heap/processor controls, not a claim of 128 MiB total process working set. Inner aggregate deadline=540 seconds; outer Python controller=600 seconds; every owned cleanup=5 seconds.

Windows children are created suspended, assigned to kill-on-close Job objects, and resumed through the owned process handle. Parent cleanup owns the entire descendant tree and never uses a PID-based/global kill. Raw stdout/stderr are file-backed, avoiding the previous interrupted-pipe-drain race; timeout keeps raw files and records failure without retry. All new homes/temp/cache/logs/artifacts are under the D storage root. Windows OS DLLs remain read-only C inputs.

One successful native capture may be frozen after root review and reused. The actual baseline JAR is root-bound to all 130 current public Java sources and the packaging script; missing API compilation must be genuine before product edits. The existing canonical gate and old delegate/cancellation/ValueTask captures remain untouched.

Each compiler stream has a 2 MiB threshold. Runtime and outer-controller stdout have a 2 MiB threshold; their stderr thresholds are 512 KiB. While the child runs, file sizes are checked between waits of at most 100 ms under the same absolute process deadline. Overflow triggers failure and owned-job cleanup; already-exited oversized output also fails. These are detection thresholds, not zero-overshoot storage guarantees: output may grow between checks and during the existing five-second cleanup. All raw bytes already captured remain on disk without truncation. Oversized streams are marked as retained but not hashed; other files are hashed incrementally. Parsing checks file size before a bounded read. Wire parsing accepts LF or CRLF only and rejects other line separators.

## Explicit exclusions and Java-only controls

- No complete Task API/interface/reflection parity: IAsyncResult/IDisposable, computational constructors, Start, Task.Run, Factory, ContinueWith, Wait/WaitAll/WaitAny/WaitAsync/Delay/WhenAll/WhenAny, Id/AsyncState and disposal omitted rather than faked.
- No TaskCreationOptions or RunContinuationsAsynchronously constructor in this slice; default pending continuation behavior and late queueing are real source-backed selected behavior.
- No SynchronizationContext, custom TaskScheduler, ExecutionContext/AsyncLocal capture, debugger/ETW, thread-pool fairness/stack-growth/finalizer unobserved-fault events, or CLR process-fatal callback policy equivalence.
- No generic Task/TCS, compiler async builders, Java struct default/copy representation, generic arity lowering or source API closure. Java public awaiter constructor/internal bridge is a documented representation helper.
- No exception-list overload ordering, SetFromTask copying, static FromException/FromCanceled factories, configured awaiters, ValueTask.AsTask/Preserve/new ValueTask(Task), CancellationTokenSource.CancelAsync, registration async disposal or WaitHandle.
- Java null CancellationToken has no native value-type equivalent; document as out-of-profile representation input and do not present any invented normalization/exception as observed .NET behavior.
- Race matrix establishes bounded observations, not formal proof or exhaustive native concurrency parity. Queue scheduling and callback order remain nondeterministic; no timing throughput guarantees.
- Task Exception wrapper identity and CompletedTask reference identity are implementation details; only selected relation observations may be reported.

The manifest specifies post-RED Java-only interrupt restoration, bridge first-use/public-mutation visibility, and uncaught callback-failure controls. They are planned and unexecuted in this phase. No native process-fatal callback is run. Pending Java implementation and its queue/rejection policy require independent implementation review.

## Credit

This preparation adds zero completed batches, accepted tasks, accepted scenarios or qualified frameworks. DJ-001-F02-04 is not accepted. Existing 0/1092 accepted tasks, 1686 open items and 0/66 qualified frameworks remain unchanged.
