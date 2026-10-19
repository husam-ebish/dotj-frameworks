> Earlier source-backed foundation research retained as evidence. Current whole-core scope and readiness are in the parent directory. This sample is not whole-core completion.

**Naming correction:** earlier Java-style public proposals are superseded by [DOTNET-API-EXACT-001](../../../08-DOTNET-API-COMPATIBILITY-POLICY.md). The exact .NET public identity is required; helper contracts remain internal. This research remains sampled, not a complete API map.

# Java architecture: core foundation contract draft

Status: **PROPOSED, INCOMPLETE**. These are planning contracts, not implemented APIs. Decisions are in [ADRS](ADRS.md); source evidence and tests are linked in the compatibility and test maps.

## Artifact boundaries

All artifacts below live in the future dotj-core repository. Public packages retain exact source namespaces and casing under DOTNET-API-EXACT-001; `org.dotj.internal.*` is reserved for hidden implementation helpers. Artifact/module coordinates remain .j-owned. Each artifact is independently compilable over JDK APIs plus its declared lower-level .j artifacts. There is no mandatory aggregate core dependency.

| Artifact suffix | Responsibility | Proposed dependencies |
|---|---|---|
| contracts | Errors, explicit context carrier, resource ownership vocabulary | JDK |
| cancellation | Tokens, sources, registrations, timers and cancellation outcomes | contracts |
| async | Async close and explicitly owned executor/stream adapters | contracts, cancellation |
| primitives | Change tokens and selected compatible value adapters | cancellation, async |
| di-abstractions | Service keys, type tokens, provider and scope interfaces | contracts, async |
| di | Runtime-origin default DI engine | di-abstractions |
| configuration-abstractions | Presence-aware values, sections, provider SPI | primitives |
| configuration | Provider ordering, root and change-token lifecycle | configuration-abstractions |
| logging-abstractions | Level, event ID, state/formatter and scope contracts | contracts |
| logging | Provider fan-out and runtime-origin logger implementation | logging-abstractions; DI integration separate |
| options | Named configuration/validation/cache contracts | primitives; DI/configuration integrations separate |
| hosting-abstractions | Host and service lifecycle contracts | cancellation, async |
| hosting | Host composition and shutdown coordinator | hosting-abstractions, di, configuration, options, logging |
| numerics-compat | Decimal and unsigned semantic adapters | JDK; contracts where needed |
| time-compat | Date/time representations and deterministic clock boundaries | JDK; contracts where needed |
| system-json | System.Text.Json behavior profile, later analysis | contracts and selected core value adapters |
| configuration-json | JSON configuration provider | configuration, system-json |

This is the first artifact partition, not a complete mapping of all 218 directories. Other BCL, network, crypto, serialization, interop and runtime groups remain retained in the inventory and require separate detailed analysis.

## Contract C-001: cancellation and registration

Propose the following Java signatures as the design vocabulary. Types and overloads require API review; no source file is created here.

| Proposed operation | Behavior contract |
|---|---|
| `CancellationToken.get_IsCancellationRequested(): boolean` | Observable cooperative cancellation state; never implies remote rollback |
| `CancellationToken.ThrowIfCancellationRequested(): void` | Throws a typed cancellation exception carrying token identity |
| `CancellationToken.Register(Action): CancellationTokenRegistration` | Captures the explicit .j context; already-canceled token invokes synchronously and propagates callback failure |
| `CancellationToken.UnsafeRegister(Action/state overload): CancellationTokenRegistration` | Does not capture .j context; distinct from the capturing overload |
| `CancellationTokenSource.Cancel(boolean throwOnFirstException): void` | Marks cancellation before callbacks; LIFO callback dispatch for the declared sequential-registration case; failure policy must match the chosen source profile |
| `CancellationTokenSource.CancelAsync(): Task` | State becomes requested during the call; returned stage represents completion of callback processing, not cancellation of all downstream work |
| `CancellationTokenRegistration.Unregister(): boolean` | Removes a not-yet-running callback if possible; does not wait for an executing callback |
| `CancellationTokenRegistration.Dispose(): void` | Waits for executing callback completion where required, except self-disposal must not deadlock |
| `CancellationTokenRegistration.DisposeAsync(): ValueTask` | Async completion fence for callback deregistration/completion |

Cancellation source lifetime, linking, timer replacement, reset, equality and disposed-source behavior need their full edge-case matrix before this contract is frozen. Distinguish token identity from source disposal; don't clear token identity merely because the source closes. Do not map `CompletableFuture.cancel` or thread interruption directly to this contract. Document any propagation adapter explicitly.

.NET ExecutionContext/SynchronizationContext cannot be captured wholesale on Java. The proposed .j context is an explicit immutable key/value carrier with bounded captured values. Caller-selected dispatchers are an optional adapter, not implicit thread-local cloning. This is an adaptation requiring paired fixtures; .NET ambient context parity is not claimed.

## Contract C-002: resource ownership and asynchronous close

Preserve `IAsyncDisposable.DisposeAsync(): ValueTask` and `IDisposable.Dispose(): void`. JDK AutoCloseable/CompletionStage may be used behind optional interop bridges, not as replacement public contracts. A borrowed stream/provider/executor remains caller-owned. Scope-owned factory-created objects are released by the owning scope. Externally supplied singleton instances remain caller-owned unless an explicit ownership overload is added and labeled as a Java extension.

A synchronous scope close uses synchronous close when an object supports both forms. Async scope close prefers async close and awaits each owned resource in reverse capture order. An async-only object reached by synchronous Dispose yields a defined error; do not block implicitly on its stage. Current source behavior deduplicates shared object instances and continues disposal after failures, aggregating errors. Preserve that profile only for the chosen reference revision; verify against the selected released baseline.

Use reference identity for ownership deduplication. Equality overrides must not cause two different resources to be treated as one. Closing a resource is not evidence that in-flight remote operations rolled back. Exception ordering and single-versus-multiple-failure representation belong in the compatibility contract.

## Contract C-003: service identity, lifetimes and resolution

Internally a TypeToken/ServiceKey representation may track closed generic identity and optional keyed-service values. Preserve the upstream public System.Type/service-provider vocabulary; do not require applications to learn replacement helper types. Define separate paths for an unkeyed service and a keyed service with a null key if source behavior requires that distinction. Do not use raw `Class<T>` as a substitute for all closed generic service identities.

Preserve the actual source public families `GetService`, `GetRequiredService`, `GetServices`, `CreateScope` and keyed-service members where present in the selected profile, with their original declaring types and overload identity. ServiceKey/TypeToken are hidden helpers, not replacement public API signatures. Resolution order, constructor selection, open generics, keyed registrations, singleton/scoped/transient caching and validation-on-build are individual compatibility features. The current default DI source is owned here; Autofac features remain dotj-container scope.

Build freezes the registration sequence into an immutable resolution model. Call-site generation can initially use reflection/MethodHandles; CLR IL emission is not translated literally. Factories run outside broad global locks. Exactly-one published singleton and disposal races need an explicit linearization design and stress tests before selecting a cache algorithm. Captive dependencies are diagnosed according to the declared validation mode, not silently repaired.

## Contract C-004: configuration presence, ordering and reload

Propose `ConfigValue(present, value)` where value can be null when present. Java Optional alone is insufficient to represent missing versus present-null. Section objects preserve path/key independently of a scalar value, and children can exist when the section value is null.

Root lookup searches providers from last to first and stops at the first present result. Root set forwards to all configured providers and fails when no source exists. Sources/children retain their specified ordering and key-comparison semantics. .NET ordinal case-insensitive semantics need explicit Unicode fixtures; `toLowerCase()` under the current Java locale is not an acceptable substitute.

Reload loads providers and rotates the root change token as observed. Stage 1's blanket immutable-snapshot suggestion must not be called exact upstream behavior: the inspected root reload does not establish an atomic transaction across all providers. An optional transactional snapshot API may be a Java extension, clearly separated from the compatibility profile.

A change token is one notification generation. Re-subscribing observers obtains new tokens. Closing a subscription suppresses future re-registration according to source tests, including close during callback and producer failure. Callback exception and async completion propagation are part of the API, not implementation details.

## Contract C-005: logging and context

Keep logging interfaces independent from concrete loggers, DI and configuration. Represent level, event ID, state and formatter separately. Upstream-compatible logging does not imply Serilog message-template destructuring; that behavior remains dotj-structured-log. Scopes are closeable and use the explicit context model across executor boundaries. Formatter invocation, disabled logging allocation, exception attachment and scope nesting still need implementation-source/test analysis; reference declarations alone do not establish them.

## Contract C-006: options and lifecycle

Named options require explicit default-name normalization, ordered configuration, post-configuration and validation. Cache semantics distinguish value, snapshot and monitor interfaces. Failure must not publish an invalid value. The inspected snapshot contains asynchronous validation and startup-specific cache behavior; those features are retained but require release-baseline selection and additional class-level analysis before Java signatures are finalized.

Host/service interfaces preserve original Task/ValueTask and CancellationToken signatures, including StartAsync/StopAsync where defined; Java futures remain internal or optional interop. The hosting implementation, startup ordering, rollback after failed startup, shutdown timeout and OS service adapters remain pending analysis. Do not claim the draft supports systemd or Windows services merely because interfaces compile on a JVM.

## Contract C-007: numeric/time adapters

A Java BigDecimal wrapper needs .NET decimal range/scale, rounding, overflow and bit-representation decisions. Numeric equality is not representation identity: don't normalize away scale or signed zero where the declared API exposes them. Keep 96-bit coefficient and scale/sign behavior as an explicit investigation track.

DateTime adaptation must retain ticks, Kind and local/unspecified distinctions when required; normalizing every value to Instant loses information. DateTimeOffset, TimeSpan, calendars, parsing cultures and time-zone ambiguity remain separate unsampled scope. Time limits use monotonic deadlines; calendar timestamps use an explicit wall clock. Neither direction asserts CLR/JVM identity.

## Bootstrap and security boundaries

Use javac/jar and a plain-Java independent test runner only after implementation authorization. No framework dependency is needed for these contracts. A .NET oracle runs separately at a pinned compatible toolchain. Do not evaluate arbitrary code from configuration or instantiate arbitrary classes from untrusted type names. Scope recursion, callback storms and reflection access require bounded diagnostics. Preserve JPMS boundaries and avoid default unrestricted `setAccessible` behavior.
