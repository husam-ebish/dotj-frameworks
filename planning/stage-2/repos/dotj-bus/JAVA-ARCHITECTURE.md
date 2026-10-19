# DJ-066 .j Bus: Java architecture and contracts

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Provide owned message-bus abstractions, transports, consumers, sagas and reliable-delivery patterns.

Product type: Distributed messaging framework. Public package names preserve the exact source namespace identity and casing, subject to explicit JVM/JPMS feasibility. `org.dotj.internal.*` is reserved for hidden implementation helpers. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are internal design/workstream vocabulary unless verified against the source. They are not authority to rename public APIs. N01 defines the exact source-derived public surface.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-bus-01 | MessageEnvelope, EndpointAddress, TransportAdapter | Message contracts topology and transport SPI |
| dotj-bus-02 | ConsumeContext, Consumer, Middleware, FaultMessage | Consumers pipelines retries and faults |
| dotj-bus-03 | SagaId, StateMachine, CorrelationRule, SagaStore | Sagas state machines and persistence |
| dotj-bus-04 | OutboxRecord, InboxKey, DeliveryAttempt, ScheduledMessage | Outbox inbox scheduling and delivery guarantees |
| dotj-bus-05 | BusHost, EndpointHealth, TransportMatrix, UpgradePlan | Transports orchestration and operational acceptance |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Public async signatures retain the original Task/ValueTask type names and semantics; CompletionStage is permitted behind the compatibility facade or in optional Java interop, not as a silent replacement; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Broker interoperability is transport-specific; at-least-once delivery and transactional outbox do not imply exactly-once effects. Saga state evolution needs contracts.

## Feature contracts and invariants

### WP-01: Message contracts topology and transport SPI

Internal analysis vocabulary (not permission to rename the public API): `MessageEnvelope`, `EndpointAddress`, `TransportAdapter`.

Define type identity headers correlation and versioned serialization. Separate publish/send/request-response topology semantics. Inventory broker clients and transport-specific source dependencies.

Required observable invariant: Unknown message versions fail explicitly; send and publish have distinct routing; transport claims are scoped to tested adapters.

### WP-02: Consumers pipelines retries and faults

Internal analysis vocabulary (not permission to rename the public API): `ConsumeContext`, `Consumer`, `Middleware`, `FaultMessage`.

Define deserialization scope middleware order and acknowledgments. Separate in-memory retry delayed redelivery and poison-message handling. Propagate cancellation without false rollback claims.

Required observable invariant: Acknowledge occurs at declared durability boundary; repeated failures reach observable quarantine; faults do not recursively create unbounded fault loops.

### WP-03: Sagas state machines and persistence

Internal analysis vocabulary (not permission to rename the public API): `SagaId`, `StateMachine`, `CorrelationRule`, `SagaStore`.

Define event correlation transitions and optimistic concurrency. Specify missing/duplicate/out-of-order event policy. Persist state and side-effect intent through explicit transactional boundaries.

Required observable invariant: Concurrent events cannot silently overwrite state; unknown correlations are diagnosable; transition history explains duplicate handling.

### WP-04: Outbox inbox scheduling and delivery guarantees

Internal analysis vocabulary (not permission to rename the public API): `OutboxRecord`, `InboxKey`, `DeliveryAttempt`, `ScheduledMessage`.

Specify durable outbox write/publish and inbox deduplication. Handle acknowledgment loss crashes and replay windows. Isolate scheduling/routing-slip/job-consumer capability families.

Required observable invariant: Lost broker acknowledgment can produce duplicates but not a false exactly-once claim; deduplication window is explicit; recovery replays only committed intents.

### WP-05: Transports orchestration and operational acceptance

Internal analysis vocabulary (not permission to rename the public API): `BusHost`, `EndpointHealth`, `TransportMatrix`, `UpgradePlan`.

Implement selected broker protocols or reviewed narrow bindings independently. Test startup drain topology permissions and rolling contract upgrades. Run broker-loss partition storage-failure and poison-message scenarios.

Required observable invariant: Every transport has its own guarantee matrix; host shutdown bounds outstanding work; inspected Apache source terms are not generalized to all product versions.

## Bootstrap and dependency boundaries

Sockets/HTTP, own serializers/storage and optional protocol-specific native bindings only if justified.

Proposed .j dependencies: core,json,resilience;postgresql(optional);scheduler(optional). Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing MassTransit usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then preserve the original public API names and workflow; the internal analysis label `MessageEnvelope` is not a replacement public API. Document unavoidable syntax/representation differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Unknown message versions fail explicitly; send and publish have distinct routing; transport claims are scoped to tested adapters. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
