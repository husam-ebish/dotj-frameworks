# DJ-015 .j Actors: Java architecture and contracts

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Provide virtual actors, activation, placement, persistence, reminders and distributed communication.

Product type: Distributed JVM framework. Public package names preserve the exact source namespace identity and casing, subject to explicit JVM/JPMS feasibility. `org.dotj.internal.*` is reserved for hidden implementation helpers. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are internal design/workstream vocabulary unless verified against the source. They are not authority to rename public APIs. N01 defines the exact source-derived public surface.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-actors-01 | ActorId, ActivationId, TurnContext, ReentrancyPolicy | Identity activation and scheduling |
| dotj-actors-02 | MemberEpoch, MembershipView, PlacementDecision | Membership placement and failure detection |
| dotj-actors-03 | InvocationEnvelope, RequestId, SerializerSchema, ProxyDescriptor | Messaging serialization and code generation |
| dotj-actors-04 | StateVersion, ReminderRecord, StreamSubscription | Persistence reminders and streams |
| dotj-actors-05 | ClusterManifest, ProviderContract, UpgradeScenario | Cluster operations and provider adapters |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Public async signatures retain the original Task/ValueTask type names and semantics; CompletionStage is permitted behind the compatibility facade or in optional Java interop, not as a silent replacement; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Grain identity, scheduling and reentrancy require explicit Java semantics. Delivery guarantees are not exactly-once and failures must remain observable.

## Feature contracts and invariants

### WP-01: Identity activation and scheduling

Internal analysis vocabulary (not permission to rename the public API): `ActorId`, `ActivationId`, `TurnContext`, `ReentrancyPolicy`.

Define persistent actor identity and activation ownership. Specify single-turn scheduling and allowed reentrancy. Handle activation/deactivation races and idle collection.

Required observable invariant: Concurrent first calls cannot silently create conflicting authoritative activations; reentrant waits have documented behavior; collected activations release resources.

### WP-02: Membership placement and failure detection

Internal analysis vocabulary (not permission to rename the public API): `MemberEpoch`, `MembershipView`, `PlacementDecision`.

Define membership store and failure-detector assumptions. Fence stale owners using versioned activation records. Model partitions recovery and rolling membership changes.

Required observable invariant: A partition scenario has an explicit availability/consistency outcome; stale epochs cannot commit ownership changes; placement is explainable.

### WP-03: Messaging serialization and code generation

Internal analysis vocabulary (not permission to rename the public API): `InvocationEnvelope`, `RequestId`, `SerializerSchema`, `ProxyDescriptor`.

Generate typed actor proxies and serializers from contracts. Version payload fields and remote exception boundaries. Specify retries deduplication timeouts and cancellation.

Required observable invariant: Unknown fields follow schema policy; lost replies never imply exactly-once execution; caller cancellation does not falsely prove remote rollback.

### WP-04: Persistence reminders and streams

Internal analysis vocabulary (not permission to rename the public API): `StateVersion`, `ReminderRecord`, `StreamSubscription`.

Use optimistic persistence tokens and explicit write outcomes. Separate durable reminders from ephemeral timers. Define stream backpressure ordering and subscription recovery.

Required observable invariant: Conflicting writes are surfaced; reminders survive activation loss according to store guarantees; slow subscribers cannot grow memory without bounds.

### WP-05: Cluster operations and provider adapters

Internal analysis vocabulary (not permission to rename the public API): `ClusterManifest`, `ProviderContract`, `UpgradeScenario`.

Isolate membership storage transport and stream providers. Specify mixed-version rollout compatibility and drain. Run node-loss partition and persistence-failure acceptance scenarios.

Required observable invariant: Unsupported provider guarantees are stated; rolling upgrades preserve declared schemas; no successful test is generalized into exactly-once delivery.

## Bootstrap and dependency boundaries

Executors, sockets, timers and own serializers; no Akka substitute.

Proposed .j dependencies: core,json,extensions. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing Orleans usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then preserve the original public API names and workflow; the internal analysis label `ActorId` is not a replacement public API. Document unavoidable syntax/representation differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Concurrent first calls cannot silently create conflicting authoritative activations; reentrant waits have documented behavior; collected activations release resources. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
