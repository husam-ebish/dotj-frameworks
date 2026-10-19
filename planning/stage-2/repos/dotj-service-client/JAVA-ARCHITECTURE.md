# DJ-017 .j Service Client: Java architecture and contracts

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Consume WCF services from Java through explicit binding and serialization contracts.

Product type: JVM protocol/native integration. Public package names preserve the exact source namespace identity and casing, subject to explicit JVM/JPMS feasibility. `org.dotj.internal.*` is reserved for hidden implementation helpers. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are internal design/workstream vocabulary unless verified against the source. They are not authority to rename public APIs. N01 defines the exact source-derived public surface.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-service-client-01 | ServiceContract, OperationDescription, WsdlModel | Contracts metadata and proxy generation |
| dotj-service-client-02 | SoapEnvelope, MessageEncoder, FaultDetail | XML SOAP and message codecs |
| dotj-service-client-03 | ChannelFactory, ChannelState, BindingProfile | Channels bindings and transport state |
| dotj-service-client-04 | CredentialProfile, SecurityContext, SessionToken | Security federation and sessions |
| dotj-service-client-05 | WireContract, ReferenceServiceFixture, ClientCompatibilityProfile | Interoperability and shared wire modules |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Public async signatures retain the original Task/ValueTask type names and semantics; CompletionStage is permitted behind the compatibility facade or in optional Java interop, not as a silent replacement; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

SOAP interoperability is separate from CLR type serialization or Windows-integrated security. Preserve deprecated feature history as versioned scope.

## Feature contracts and invariants

### WP-01: Contracts metadata and proxy generation

Internal analysis vocabulary (not permission to rename the public API): `ServiceContract`, `OperationDescription`, `WsdlModel`.

Map WSDL/XSD service operations and generated Java types. Preserve qualified names action identifiers and message parts. Report unsupported policy assertions during import.

Required observable invariant: Generated clients retain wire names; ambiguous schemas fail with locations; unsupported binding assertions are never silently ignored.

### WP-02: XML SOAP and message codecs

Internal analysis vocabulary (not permission to rename the public API): `SoapEnvelope`, `MessageEncoder`, `FaultDetail`.

Implement namespace-correct SOAP versions and fault models. Define quotas streaming and secure XML parsing. Separate text MTOM and binary XML encoding profiles.

Required observable invariant: External entities are disabled by default; attachments preserve bytes; SOAP faults retain codes and typed details; binary XML remains gated until verified.

### WP-03: Channels bindings and transport state

Internal analysis vocabulary (not permission to rename the public API): `ChannelFactory`, `ChannelState`, `BindingProfile`.

Specify open send receive close abort and fault transitions. Implement HTTP transport before separately gated TCP/pipe profiles. Define timeout budgets and resource ownership.

Required observable invariant: Aborting releases pending calls; a faulted channel cannot be reused silently; transport-specific capabilities are reported before opening.

### WP-04: Security federation and sessions

Internal analysis vocabulary (not permission to rename the public API): `CredentialProfile`, `SecurityContext`, `SessionToken`.

Inventory WS-Security federation and Windows-integrated dependencies. Define replay key lifetime and endpoint identity checks. Isolate native authentication behind explicit platform capabilities.

Required observable invariant: Security policy mismatch fails before application data is sent; replay fixtures fail; Windows identity is not emulated by passing a username header.

### WP-05: Interoperability and shared wire modules

Internal analysis vocabulary (not permission to rename the public API): `WireContract`, `ReferenceServiceFixture`, `ClientCompatibilityProfile`.

Create neutral codec modules reusable by dotj-services. Run pinned .NET service fixtures for each claimed binding. Record cancellation fault and large-message behavior.

Required observable invariant: Interoperation evidence is binding/version specific; client and server modules have no cycle; missing reference environment blocks claims rather than disappearing from scope.

## Bootstrap and dependency boundaries

XML streaming, sockets, HTTP client, JCA and optional OS bindings.

Proposed .j dependencies: core. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing WCF client libraries usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then preserve the original public API names and workflow; the internal analysis label `ServiceContract` is not a replacement public API. Document unavoidable syntax/representation differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Generated clients retain wire names; ambiguous schemas fail with locations; unsupported binding assertions are never silently ignored. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
