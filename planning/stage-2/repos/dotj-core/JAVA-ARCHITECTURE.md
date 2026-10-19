# DJ-001 .j Core: Java architecture and contracts

Reproduce base-library contracts on the JVM while retaining the JDK VM, GC, threads and standard collections.

Product type: JVM library; runtime feasibility boundary. Proposed Java package root: `org.dotj.core`. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are design proposals, not already implemented APIs.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-core-01 | TypeToken<T>, Outcome<T>, AsyncCloseable, explicit ContextSnapshot | Foundation types and ownership |
| dotj-core-02 | CancellationToken, CancellationSource, Registration, Deadline | Cancellation and asynchronous operations |
| dotj-core-03 | ServiceKey<T>, ServiceDescriptor, Scope, ConfigValue, ConfigurationRoot | Default DI and configuration |
| dotj-core-04 | OptionsFactory<T>, OptionsMonitor<T>, Logger, HostedService, Host | Options logging and hosting |
| dotj-core-05 | DotjDecimal, DotjDateTime, EncodingProfile, CultureProfile | Numeric text and time compatibility |
| dotj-core-06 | Sequence<T>, QueryExpression, ExpressionVisitor, CollectionAdapters | Collections LINQ and expression services |
| dotj-core-07 | OwnedStream, Pipe, HttpMessage, SocketChannelAdapter, DataRecord | I/O networking and data contracts |
| dotj-core-08 | SystemJsonProfile, XmlModel, CryptoProvider, MetadataReader, ReflectionAdapter | Formats serialization security and reflection |
| dotj-core-09 | PlatformCapability, NativeBinding, RuntimeCapabilityMatrix | Native runtime and complete BCL disposition |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Async methods return CompletionStage; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Define decimal, unsigned numeric, culture, DateTime, encoding, exception and disposal semantics; Java erasure and memory-model differences preclude CLR binary compatibility.

## Feature contracts and invariants

### WP-01: Foundation types and ownership

Contract vocabulary: `TypeToken<T>`, `Outcome<T>`, `AsyncCloseable`, `explicit ContextSnapshot`.

Specify nullability, type identity and exception-cause mapping. Define borrowed versus owned resource lifetimes and close failure ordering. Define context capture and executor transfer without copying arbitrary thread locals.

Required observable invariant: Equal parameterized types share identity; different generic arguments do not; supplied resources are never closed implicitly; context values do not leak between requests.

### WP-02: Cancellation and asynchronous operations

Contract vocabulary: `CancellationToken`, `CancellationSource`, `Registration`, `Deadline`.

Specify register/cancel/link/timer/reset state transitions and linearization points. Separate unregister, blocking close, async close and future cancellation. Define callback order, failure aggregation and explicit context dispatch.

Required observable invariant: Late registration runs synchronously; sequential callbacks use the declared LIFO profile; self-close cannot deadlock; cancelAsync completion waits for callbacks; token identity survives source disposal as specified.

### WP-03: Default DI and configuration

Contract vocabulary: `ServiceKey<T>`, `ServiceDescriptor`, `Scope`, `ConfigValue`, `ConfigurationRoot`.

Map keyed/open-generic resolution, constructor selection and lifetime caches. Specify present-null configuration, last-provider lookup and write-to-all semantics. Define scope deduplication, reverse cleanup and reload-generation behavior.

Required observable invariant: Concurrent singleton resolves return one published identity; aliases close once; supplied singleton stays caller-owned; empty-provider writes fail; failed reload does not acquire an invented atomic guarantee.

### WP-04: Options logging and hosting

Contract vocabulary: `OptionsFactory<T>`, `OptionsMonitor<T>`, `Logger`, `HostedService`, `Host`.

Specify configure/postconfigure/validate order and named cache lifetimes. Define structured state/formatter scopes independent from concrete loggers. Specify startup, background failure, stop deadlines and OS-lifetime adapters.

Required observable invariant: Invalid options never publish as valid; monitor close removes subscriptions; disabled log handling follows declared formatter behavior; partial host startup releases completed services in defined order.

### WP-05: Numeric text and time compatibility

Contract vocabulary: `DotjDecimal`, `DotjDateTime`, `EncodingProfile`, `CultureProfile`.

Specify range, scale, signed representation, overflow and rounding vectors. Map UTF encoders, fallback behavior, normalization and culture comparisons. Separate wall-clock calendar operations from monotonic deadlines.

Required observable invariant: Decimal bit-preserving paths retain scale/sign; invalid byte sequences follow explicit modes; Turkish casing and DST ambiguity are fixture-covered; Instant conversion cannot discard unspecified Kind silently.

### WP-06: Collections LINQ and expression services

Contract vocabulary: `Sequence<T>`, `QueryExpression`, `ExpressionVisitor`, `CollectionAdapters`.

Partition standard JDK reuse from .NET-observable ordering/equality adapters. Specify lazy enumeration, exception timing and parallel-query cancellation. Design explicit expression IR for consumers without introspecting arbitrary Java lambdas.

Required observable invariant: Enumerator disposal and deferred exceptions match profiles; grouping/null/equality differences are explicit; query IR round trips preserve node types and constants; provider translation has no silent client execution.

### WP-07: I/O networking and data contracts

Contract vocabulary: `OwnedStream`, `Pipe`, `HttpMessage`, `SocketChannelAdapter`, `DataRecord`.

Map files, archives, pipelines, channels and connection lifecycles. Separate .NET HTTP/mail/socket profiles from web/server and MailKit products. Specify JDBC/data abstractions and local transaction enlistment boundaries.

Required observable invariant: Partial reads/writes and half-closes retain data; bounded buffers enforce backpressure; file handles close on failure; network cancellation does not imply rollback; unsupported distributed enlistment fails explicitly.

### WP-08: Formats serialization security and reflection

Contract vocabulary: `SystemJsonProfile`, `XmlModel`, `CryptoProvider`, `MetadataReader`, `ReflectionAdapter`.

Inventory runtime JSON, XML, CBOR, ASN.1, packaging and serializer profiles. Use JDK crypto primitives while defining algorithm/encoding/key contracts. Separate reflection metadata and dynamic generation from CLR loading/IL execution.

Required observable invariant: System.Text.Json tests cannot be satisfied merely by Newtonsoft behavior; unsafe type activation is disabled; signature bytes and canonicalization use vectors; CLR assembly execution is never claimed from metadata parsing.

### WP-09: Native runtime and complete BCL disposition

Contract vocabulary: `PlatformCapability`, `NativeBinding`, `RuntimeCapabilityMatrix`.

Assign every library directory and source branch to a retained workstream. Specify COM, Windows auth, intrinsics, AOT, browser and VM feasibility experiments. Define explicit fail-fast capability discovery and platform artifact packaging.

Required observable invariant: All 218 known library directories have ownership and test routes; unsupported backend calls report capability gaps; no custom VM is assumed; a backend remains blocked until a reproducible execution experiment succeeds.

## Bootstrap and dependency boundaries

java.base, java.nio, java.time, java.util.concurrent, JCA; no replacement JVM or custom crypto.

Proposed .j dependencies: No product dependency in the base foundation. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing .NET runtime and base libraries usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then express the same intent with `TypeToken<T>` and its companion contracts. Preserve semantic differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Equal parameterized types share identity; different generic arguments do not; supplied resources are never closed implicitly; context values do not leak between requests. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.

## Deeper foundation contracts

[Cancellation, DI, configuration, options and lifecycle source analysis](foundation-research/JAVA-ARCHITECTURE.md) retains the earlier exact contract work. Read it alongside this whole-core work breakdown; neither sample claims complete BCL parity.
