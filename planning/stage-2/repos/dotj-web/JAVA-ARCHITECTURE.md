# DJ-012 .j Web: Java architecture and contracts

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Reproduce ASP.NET Core's server application and component capabilities with an owned Java web stack.

Product type: JVM library plus browser/native integrations. Public package names preserve the exact source namespace identity and casing, subject to explicit JVM/JPMS feasibility. `org.dotj.internal.*` is reserved for hidden implementation helpers. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are internal design/workstream vocabulary unless verified against the source. They are not authority to rename public APIs. N01 defines the exact source-derived public surface.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-web-01 | ConnectionContext, HttpExchange, BodyPipe, ProtocolCapability | Server transport and HTTP lifecycle |
| dotj-web-02 | RequestDelegate, RoutePattern, EndpointMetadata, BindingResult | Middleware routing and APIs |
| dotj-web-03 | ActionDescriptor, ModelState, PageHandler, ViewResult | MVC and Razor Pages |
| dotj-web-04 | ComponentDescriptor, RenderBatch, CircuitId, HydrationState | Components and Blazor execution profiles |
| dotj-web-05 | Principal, AuthenticationScheme, AuthorizationPolicy, IdentityStore | Identity authentication and authorization |
| dotj-web-06 | AntiforgeryToken, ProtectionKeyRing, CorsPolicy, SecurityHeaders | Application security and data protection |
| dotj-web-07 | HubConnection, InvocationId, HubProtocol, GroupMembership | SignalR and real-time messaging |
| dotj-web-08 | WebHost, HealthEndpoint, RequestActivity, ServerOptions | Hosting diagnostics and integrated acceptance |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Public async signatures retain the original Task/ValueTask type names and semantics; CompletionStage is permitted behind the compatibility facade or in optional Java interop, not as a silent replacement; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Server rendering and persistent component circuits are plausible JVM tracks. Browser execution needs a separately justified JS/Wasm compilation/runtime design; browsers do not supply a JVM.

## Feature contracts and invariants

### WP-01: Server transport and HTTP lifecycle

Internal analysis vocabulary (not permission to rename the public API): `ConnectionContext`, `HttpExchange`, `BodyPipe`, `ProtocolCapability`.

Specify HTTP/1 parsing framing limits and connection states. Design TLS HTTP/2 and separately gated QUIC/HTTP3 backends. Define backpressure request abort trailers and upgrade ownership.

Required observable invariant: Conflicting framing is rejected; slow consumers bound buffers; abort terminates body reads; unsupported protocols are advertised honestly.

### WP-02: Middleware routing and APIs

Internal analysis vocabulary (not permission to rename the public API): `RequestDelegate`, `RoutePattern`, `EndpointMetadata`, `BindingResult`.

Define middleware order exception handling and terminal behavior. Compile route precedence constraints and endpoint selection. Bind parameters with explicit culture validation and response serialization.

Required observable invariant: Ambiguous routes fail deterministically; middleware can observe unwind order; malformed payloads have stable status/problem responses.

### WP-03: MVC and Razor Pages

Internal analysis vocabulary (not permission to rename the public API): `ActionDescriptor`, `ModelState`, `PageHandler`, `ViewResult`.

Map controller filters model binding validation and results. Define Razor Page handler selection and view-data lifetime. Connect compiled Razor output through a versioned rendering contract.

Required observable invariant: Filters execute in documented nesting; validation errors preserve field paths; generated pages render escaped output and source-linked errors.

### WP-04: Components and Blazor execution profiles

Internal analysis vocabulary (not permission to rename the public API): `ComponentDescriptor`, `RenderBatch`, `CircuitId`, `HydrationState`.

Specify server component lifecycle diffing events and reconnect. Define static rendering streaming and hydration boundaries. Run a separate browser compiler/runtime feasibility track without assuming a browser JVM.

Required observable invariant: Disconnected circuits expire and release state; duplicate events are handled explicitly; browser execution is not advertised before a runnable backend exists.

### WP-05: Identity authentication and authorization

Internal analysis vocabulary (not permission to rename the public API): `Principal`, `AuthenticationScheme`, `AuthorizationPolicy`, `IdentityStore`.

Define authentication scheme selection challenge forbid and claims. Specify user password token lockout and store concurrency contracts. Separate application Identity from OAuth/OIDC protocol engine integration.

Required observable invariant: Scheme confusion tests fail closed; password/reset secrets are protected; lockout and concurrent updates behave predictably; auth store adapters are optional.

### WP-06: Application security and data protection

Internal analysis vocabulary (not permission to rename the public API): `AntiforgeryToken`, `ProtectionKeyRing`, `CorsPolicy`, `SecurityHeaders`.

Bind CSRF tokens to their required session context. Specify key rotation persisted protection purposes and expiry. Test CORS cookies redirects encoding and request-size limits.

Required observable invariant: Cross-site requests cannot bypass token checks; old keys decrypt only under declared retention; untrusted redirects and markup are rejected or escaped.

### WP-07: SignalR and real-time messaging

Internal analysis vocabulary (not permission to rename the public API): `HubConnection`, `InvocationId`, `HubProtocol`, `GroupMembership`.

Define negotiation framing invocation streaming and cancellation. Specify reconnect session/group behavior and auth renewal. Add scale-out contracts without hidden delivery guarantees.

Required observable invariant: Invocation completion is correlated once; stream cancellation releases producers; reconnect behavior is documented under lost responses and node changes.

### WP-08: Hosting diagnostics and integrated acceptance

Internal analysis vocabulary (not permission to rename the public API): `WebHost`, `HealthEndpoint`, `RequestActivity`, `ServerOptions`.

Connect core hosting configuration logging and graceful drain. Define metrics cardinality and sensitive request data policy. Build cross-process HTTP security and component conformance suites.

Required observable invariant: Draining stops admission then bounds in-flight work; logs exclude credentials by default; claimed capabilities have per-protocol and per-platform evidence.

## Bootstrap and dependency boundaries

NIO, SSLEngine, HTTP client, executors and JCA; JDK simple HTTP server may bootstrap tests only, not establish server feature parity.

Proposed .j dependencies: core,razor,json. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing ASP.NET Core usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then preserve the original public API names and workflow; the internal analysis label `ConnectionContext` is not a replacement public API. Document unavoidable syntax/representation differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Conflicting framing is rejected; slow consumers bound buffers; abort terminates body reads; unsupported protocols are advertised honestly. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.

## Public API direction under the owner requirement

Preserve actual ASP.NET Core public identities such as HttpContext, RequestDelegate, IApplicationBuilder, ControllerBase and original middleware/endpoint methods where present in the selected profile. Keep MVC, Razor Pages, Blazor, Identity, SignalR and hosting concepts intact. Internal RenderBatch/transport models do not authorize renaming source public APIs.
