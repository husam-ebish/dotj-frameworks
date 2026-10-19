# DJ-006 .j Extensions: Java architecture and contracts

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Provide hosting, configuration and integration capabilities while respecting the actual source owners of Microsoft.Extensions packages.

Product type: JVM library. Public package names preserve the exact source namespace identity and casing, subject to explicit JVM/JPMS feasibility. `org.dotj.internal.*` is reserved for hidden implementation helpers. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are internal design/workstream vocabulary unless verified against the source. They are not authority to rename public APIs. N01 defines the exact source-derived public surface.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-extensions-01 | ExtensionModuleDescriptor, CapabilitySPI, IntegrationManifest | Package ownership and adapter graph |
| dotj-extensions-02 | ServiceEndpointResolver, HttpPipelineDecorator, DiscoverySnapshot | Resilience HTTP and service discovery |
| dotj-extensions-03 | MeterAdapter, Redactor, HealthProbe, ResourceSnapshot | Telemetry diagnostics and compliance |
| dotj-extensions-04 | ChatClient, EmbeddingClient, VectorStore, IngestionStage | AI vector and ingestion abstractions |
| dotj-extensions-05 | FakeTimeProvider, TestHost, ExtensionCompatibilityMatrix | Testing helpers and packaging |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Public async signatures retain the original Task/ValueTask type names and semantics; CompletionStage is permitted behind the compatibility facade or in optional Java interop, not as a silent replacement; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Map every package to runtime or extensions at a pinned revision; options validation, configuration precedence and lifecycle behavior require explicit Java contracts.

## Feature contracts and invariants

### WP-01: Package ownership and adapter graph

Internal analysis vocabulary (not permission to rename the public API): `ExtensionModuleDescriptor`, `CapabilitySPI`, `IntegrationManifest`.

Map each Microsoft.Extensions project to runtime or extensions source. Separate abstractions from optional adapters and generator/test packages. Record actual package dependencies and their target ownership.

Required observable invariant: Every inspected package has exactly one owner; core contracts never depend on richer adapters; no namespace-based ownership shortcut is accepted.

### WP-02: Resilience HTTP and service discovery

Internal analysis vocabulary (not permission to rename the public API): `ServiceEndpointResolver`, `HttpPipelineDecorator`, `DiscoverySnapshot`.

Integrate owned resilience with JDK/owned HTTP through bounded adapters. Specify endpoint refresh, health and configuration precedence. Keep retry/idempotency decisions explicit.

Required observable invariant: Refresh cannot publish half-built endpoint sets; retries never replay unsafe operations by default; discovery failures follow declared stale-data policy.

### WP-03: Telemetry diagnostics and compliance

Internal analysis vocabulary (not permission to rename the public API): `MeterAdapter`, `Redactor`, `HealthProbe`, `ResourceSnapshot`.

Define metrics/log enrichment with cardinality and privacy controls. Implement compliance/redaction contracts and health/resource probes. Isolate platform/container-resource readers behind capabilities.

Required observable invariant: Secrets are redacted before sinks; unbounded user labels are rejected or bounded; missing platform probes yield unknown rather than healthy; redaction never mutates the caller's object.

### WP-04: AI vector and ingestion abstractions

Internal analysis vocabulary (not permission to rename the public API): `ChatClient`, `EmbeddingClient`, `VectorStore`, `IngestionStage`.

Map AI/vector/data-ingestion contracts from actual extensions modules. Define streaming/tool-call/cancellation and content provenance. Build provider adapters through separately reviewed protocol interfaces.

Required observable invariant: Mocked provider streams obey cancellation/backpressure; malformed tool arguments fail validation; ingestion preserves source/provenance; no existing Java AI framework substitutes for these contracts.

### WP-05: Testing helpers and packaging

Internal analysis vocabulary (not permission to rename the public API): `FakeTimeProvider`, `TestHost`, `ExtensionCompatibilityMatrix`.

Provide deterministic test doubles for extension contracts. Package integration modules independently with optional dependencies. Validate compatibility against the core contracts and consumer products.

Required observable invariant: An application using only core APIs loads no AI/native/cloud code; deterministic fake time drives retry/health tests; adapter version conflicts are diagnosed before startup.

## Bootstrap and dependency boundaries

ServiceLoader, properties/environment/file APIs, executors and management APIs.

Proposed .j dependencies: core. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing .NET Extensions usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then preserve the original public API names and workflow; the internal analysis label `ExtensionModuleDescriptor` is not a replacement public API. Document unavoidable syntax/representation differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Every inspected package has exactly one owner; core contracts never depend on richer adapters; no namespace-based ownership shortcut is accepted. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
