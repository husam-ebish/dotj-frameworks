# DJ-038 .j Graph Platform: Java architecture and contracts

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Reproduce server, client-generation and composition capabilities from the C# GraphQL platform.

Product type: JVM GraphQL framework/toolchain. Public package names preserve the exact source namespace identity and casing, subject to explicit JVM/JPMS feasibility. `org.dotj.internal.*` is reserved for hidden implementation helpers. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are internal design/workstream vocabulary unless verified against the source. They are not authority to rename public APIs. N01 defines the exact source-derived public surface.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-graph-platform-01 | GraphDocument, SchemaDefinition, ExecutionPlan | Language schema and execution ownership |
| dotj-graph-platform-02 | ResolverContext, FieldMiddleware, DataLoader | Resolver pipeline and data loading |
| dotj-graph-platform-03 | GraphRequest, SubscriptionSession, PersistedOperation | Transport subscriptions and persistence |
| dotj-graph-platform-04 | SubgraphSchema, CompositionResult, QueryPlan | Federation composition and gateway |
| dotj-graph-platform-05 | GeneratedClient, OperationManifest, SchemaDiff | Client generation tooling and schema evolution |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Public async signatures retain the original Task/ValueTask type names and semantics; CompletionStage is permitted behind the compatibility facade or in optional Java interop, not as a silent replacement; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Preserve GraphQL protocol behavior; generated .NET clients become Java clients with explicit cache and nullability semantics. Commercial tooling boundaries remain visible.

## Feature contracts and invariants

### WP-01: Language schema and execution ownership

Internal analysis vocabulary (not permission to rename the public API): `GraphDocument`, `SchemaDefinition`, `ExecutionPlan`.

Inventory Hot Chocolate Strawberry Shake and gateway families separately. Define parser schema validation and execution ownership. Keep this platform distinct from dotj-graphql implementation.

Required observable invariant: Every source product family has a target owner; independent executors do not silently share incompatible semantics; parser errors retain source spans.

### WP-02: Resolver pipeline and data loading

Internal analysis vocabulary (not permission to rename the public API): `ResolverContext`, `FieldMiddleware`, `DataLoader`.

Specify coercion null propagation field middleware and async scheduling. Batch/cache loaders within request scope. Define cancellation cost/depth limits and error redaction.

Required observable invariant: N+1 fixtures show intended batching; loader caches do not cross users; non-null failures propagate to the correct parent.

### WP-03: Transport subscriptions and persistence

Internal analysis vocabulary (not permission to rename the public API): `GraphRequest`, `SubscriptionSession`, `PersistedOperation`.

Define HTTP multipart/WebSocket profiles and operation lifecycle. Bind persisted operations to schema and authorization policy. Bound streaming results and subscription queues.

Required observable invariant: Unknown persisted IDs cannot bypass validation; disconnected subscriptions release resources; protocol-specific error behavior is tested.

### WP-04: Federation composition and gateway

Internal analysis vocabulary (not permission to rename the public API): `SubgraphSchema`, `CompositionResult`, `QueryPlan`.

Inventory fusion/federation semantics at the pinned baseline. Validate ownership and cross-service entity keys. Define partial failure deadlines and delegated authorization.

Required observable invariant: Conflicting field ownership fails composition; gateway cannot forward caller credentials beyond policy; partial errors preserve service context.

### WP-05: Client generation tooling and schema evolution

Internal analysis vocabulary (not permission to rename the public API): `GeneratedClient`, `OperationManifest`, `SchemaDiff`.

Generate typed Java clients from validated operations. Handle custom scalars fragments and response unions. Track breaking schema changes and reproducible generated output.

Required observable invariant: Invalid operations fail generation; union handling is exhaustive by profile; generated sources compile without reusing an existing Java GraphQL client.

## Bootstrap and dependency boundaries

Owned parsing, executors, web stack and annotation processing.

Proposed .j dependencies: web,json,core. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing Hot Chocolate / Strawberry Shake usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then preserve the original public API names and workflow; the internal analysis label `GraphDocument` is not a replacement public API. Document unavoidable syntax/representation differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Every source product family has a target owner; independent executors do not silently share incompatible semantics; parser errors retain source spans. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
