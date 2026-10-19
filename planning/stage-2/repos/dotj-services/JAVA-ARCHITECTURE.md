# DJ-018 .j Services: Java architecture and contracts

Host WCF-compatible service contracts and bindings on the .j stack.

Product type: JVM service framework. Proposed Java package root: `org.dotj.services`. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are design proposals, not already implemented APIs.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-services-01 | DispatchTable, OperationInvoker, ServiceInstance | Dispatch and operation selection |
| dotj-services-02 | ServiceHost, ListenerBinding, RequestChannel | Host and transport bindings |
| dotj-services-03 | ServiceBehavior, MessageInspector, MetadataExporter | Behaviors middleware and metadata |
| dotj-services-04 | CallerIdentity, AuthorizationDecision, TransactionContext | Authentication authorization and transactions |
| dotj-services-05 | ServiceCompatibilityProfile, DotnetClientFixture, LoadScenario | Server interoperability and hosting acceptance |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Async methods return CompletionStage; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Sharing wire codecs with service-client is proposed; server hosting semantics remain independent. Define impersonation and transaction differences.

## Feature contracts and invariants

### WP-01: Dispatch and operation selection

Contract vocabulary: `DispatchTable`, `OperationInvoker`, `ServiceInstance`.

Bind service metadata to endpoints and action selectors. Define instance lifetime concurrency and operation context. Separate application exceptions from protocol faults.

Required observable invariant: Ambiguous operations fail at host startup; per-call instances are disposed once; unhandled exceptions do not disclose stack traces by default.

### WP-02: Host and transport bindings

Contract vocabulary: `ServiceHost`, `ListenerBinding`, `RequestChannel`.

Use web and neutral service-client wire contracts. Specify listener admission drain and channel abort. Maintain per-binding quotas and capabilities.

Required observable invariant: Stopping a host rejects new work and bounds draining; binding limits are enforced before deserialization; client codecs do not depend on server dispatch.

### WP-03: Behaviors middleware and metadata

Contract vocabulary: `ServiceBehavior`, `MessageInspector`, `MetadataExporter`.

Define behavior ordering and safe request/response inspection. Generate WSDL/XSD from accepted service contracts. Preserve endpoint policy and namespace identities.

Required observable invariant: Exported metadata reimports into reference clients; inspector failures have defined cleanup; behavior order is deterministic.

### WP-04: Authentication authorization and transactions

Contract vocabulary: `CallerIdentity`, `AuthorizationDecision`, `TransactionContext`.

Map portable authorization and credential profiles. Isolate impersonation and distributed transaction feasibility. Define local transaction propagation and fault behavior.

Required observable invariant: Unauthorized operations never invoke service code; unavailable impersonation fails explicitly; timeouts do not claim a committed transaction was rolled back.

### WP-05: Server interoperability and hosting acceptance

Contract vocabulary: `ServiceCompatibilityProfile`, `DotnetClientFixture`, `LoadScenario`.

Exercise pinned .NET clients across supported bindings. Test concurrent instances message failures and host restarts. Document deployment credentials certificates and native prerequisites.

Required observable invariant: Every supported binding has bidirectional fault/streaming evidence; resource use remains bounded; unsupported WS-* profiles remain enumerated.

## Bootstrap and dependency boundaries

Own web server, XML APIs and sockets; optional native authentication bindings.

Proposed .j dependencies: service-client,web,extensions. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing CoreWCF usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then express the same intent with `DispatchTable` and its companion contracts. Preserve semantic differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Ambiguous operations fail at host startup; per-call instances are disposed once; unhandled exceptions do not disclose stack traces by default. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
