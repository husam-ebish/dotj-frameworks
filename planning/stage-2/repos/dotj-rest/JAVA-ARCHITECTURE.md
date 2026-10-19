# DJ-032 .j REST: Java architecture and contracts

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Provide ergonomic request construction, authentication, serialization and response handling.

Product type: JVM HTTP client library. Public package names preserve the exact source namespace identity and casing, subject to explicit JVM/JPMS feasibility. `org.dotj.internal.*` is reserved for hidden implementation helpers. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are internal design/workstream vocabulary unless verified against the source. They are not authority to rename public APIs. N01 defines the exact source-derived public surface.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-rest-01 | RestRequest, Parameter, ResourcePath | Request model and URI construction |
| dotj-rest-02 | RestClient, Response, ResponseBody | Transport and response lifecycle |
| dotj-rest-03 | BodySerializer, MultipartPart, ContentType | Serialization and multipart bodies |
| dotj-rest-04 | Authenticator, RedirectPolicy, CookieJar | Authentication redirects and cookies |
| dotj-rest-05 | RequestInterceptor, ClientOptions, RestCompatibilityCase | Interceptors adapters and compatibility |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Public async signatures retain the original Task/ValueTask type names and semantics; CompletionStage is permitted behind the compatibility facade or in optional Java interop, not as a silent replacement; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Preserve encoding, multipart, errors and cancellation behavior; Java transport redirect/cookie defaults must not silently replace source defaults.

## Feature contracts and invariants

### WP-01: Request model and URI construction

Internal analysis vocabulary (not permission to rename the public API): `RestRequest`, `Parameter`, `ResourcePath`.

Define query path header cookie form and body precedence. Encode URI components exactly once. Make request mutation/snapshot timing explicit.

Required observable invariant: Reserved characters survive expected encoding; duplicate headers follow policy; concurrent calls do not mutate a shared request unexpectedly.

### WP-02: Transport and response lifecycle

Internal analysis vocabulary (not permission to rename the public API): `RestClient`, `Response`, `ResponseBody`.

Use a transport SPI with JDK HTTP baseline. Separate protocol status from transport/deserialization failure. Define streaming cancellation timeouts and body ownership.

Required observable invariant: Non-success HTTP can retain its body; cancellation closes owned streams; response resources are released on conversion failure.

### WP-03: Serialization and multipart bodies

Internal analysis vocabulary (not permission to rename the public API): `BodySerializer`, `MultipartPart`, `ContentType`.

Keep JSON XML and custom serializers optional. Stream multipart content with safe header construction. Define content-length versus chunked behavior by transport capability.

Required observable invariant: Binary parts preserve bytes; filenames cannot inject headers; serializer failure occurs before unsafe automatic retries.

### WP-04: Authentication redirects and cookies

Internal analysis vocabulary (not permission to rename the public API): `Authenticator`, `RedirectPolicy`, `CookieJar`.

Specify credential application and redirect trust boundaries. Prevent cross-origin forwarding of sensitive headers by default. Define cookie expiry domain path and per-client isolation.

Required observable invariant: Redirects cannot leak authorization across trust boundaries; expired cookies are not sent; failed auth hooks produce diagnosable outcomes.

### WP-05: Interceptors adapters and compatibility

Internal analysis vocabulary (not permission to rename the public API): `RequestInterceptor`, `ClientOptions`, `RestCompatibilityCase`.

Order request/response hooks and document exception behavior. Map upstream overload families into Java APIs. Test URI encoding status handling and transport failure regressions.

Required observable invariant: Hook order is deterministic; unsupported overload semantics are recorded; optional integration artifacts do not enter the base client.

## Bootstrap and dependency boundaries

java.net.http.HttpClient and own JSON serializer.

Proposed .j dependencies: json,core. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing RestSharp usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then preserve the original public API names and workflow; the internal analysis label `RestRequest` is not a replacement public API. Document unavoidable syntax/representation differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Reserved characters survive expected encoding; duplicate headers follow policy; concurrent calls do not mutate a shared request unexpectedly. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
