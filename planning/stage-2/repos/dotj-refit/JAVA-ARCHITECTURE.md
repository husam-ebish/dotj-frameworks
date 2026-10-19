# DJ-033 .j Refit: Java architecture and contracts

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Generate typed HTTP clients from annotated Java interfaces.

Product type: JVM generated HTTP client library. Public package names preserve the exact source namespace identity and casing, subject to explicit JVM/JPMS feasibility. `org.dotj.internal.*` is reserved for hidden implementation helpers. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are internal design/workstream vocabulary unless verified against the source. They are not authority to rename public APIs. N01 defines the exact source-derived public surface.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-refit-01 | HttpService, RouteAnnotation, ParameterBinding | Interface contract and annotation model |
| dotj-refit-02 | ClientDescriptor, GeneratedClient, InvocationPlan | Java proxy and source generation |
| dotj-refit-03 | ResponseType, ApiException, StreamResult | Serialization errors and streaming |
| dotj-refit-04 | ClientFactory, RequestHandler, AuthorizationProvider | Authentication handlers and client lifetime |
| dotj-refit-05 | RestTransportAdapter, ContractFixture, GeneratorDiagnostic | REST bridge and contract verification |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Public async signatures retain the original Task/ValueTask type names and semantics; CompletionStage is permitted behind the compatibility facade or in optional Java interop, not as a silent replacement; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Attribute-driven C# interfaces map to Java annotations; generic return types and async error handling need explicit representation.

## Feature contracts and invariants

### WP-01: Interface contract and annotation model

Internal analysis vocabulary (not permission to rename the public API): `HttpService`, `RouteAnnotation`, `ParameterBinding`.

Validate HTTP method paths headers body and return types. Resolve inherited interfaces generic methods and default values. Diagnose invalid declarations at generation time.

Required observable invariant: Conflicting bindings fail with member location; inherited methods retain metadata; unsupported signatures never produce runtime surprises.

### WP-02: Java proxy and source generation

Internal analysis vocabulary (not permission to rename the public API): `ClientDescriptor`, `GeneratedClient`, `InvocationPlan`.

Compare source generation with reflection-proxy fallback. Generate deterministic Java implementations. Keep generated transport requests inspectable for tests.

Required observable invariant: Generated and proxy paths produce equivalent requests; no runtime C# expression/codegen dependency is assumed.

### WP-03: Serialization errors and streaming

Internal analysis vocabulary (not permission to rename the public API): `ResponseType`, `ApiException`, `StreamResult`.

Define body serialization and per-method settings. Preserve response content and status in structured errors. Specify synchronous async streaming and cancellation contracts.

Required observable invariant: Deserialization failure retains HTTP context; streams close on cancellation; generic response types remain resolvable after erasure.

### WP-04: Authentication handlers and client lifetime

Internal analysis vocabulary (not permission to rename the public API): `ClientFactory`, `RequestHandler`, `AuthorizationProvider`.

Compose handlers in deterministic order. Resolve per-request credentials without static shared state. Define transport reuse and caller-owned client behavior.

Required observable invariant: Concurrent users cannot share credentials accidentally; caller transport is not closed by generated clients; handler failures release request resources.

### WP-05: REST bridge and contract verification

Internal analysis vocabulary (not permission to rename the public API): `RestTransportAdapter`, `ContractFixture`, `GeneratorDiagnostic`.

Use dotj-rest through an optional explicit adapter. Port request-construction and generator regression cases. Test compile-time and runtime failures separately.

Required observable invariant: Base generated clients need only accepted transport contracts; URI/header fixtures match profile; no Retrofit replacement supplies the implementation.

## Bootstrap and dependency boundaries

Annotation processing, reflection fallback and JDK HTTP client via own REST transport.

Proposed .j dependencies: rest,json;code(dev-optional). Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing Refit usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then preserve the original public API names and workflow; the internal analysis label `HttpService` is not a replacement public API. Document unavoidable syntax/representation differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Conflicting bindings fail with member location; inherited methods retain metadata; unsupported signatures never produce runtime surprises. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
