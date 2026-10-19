# DJ-016 .j Auth: Java architecture and contracts

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Implement OAuth/OIDC client, server and validation capabilities with own protocol processing.

Product type: Security-sensitive JVM framework. Public package names preserve the exact source namespace identity and casing, subject to explicit JVM/JPMS feasibility. `org.dotj.internal.*` is reserved for hidden implementation helpers. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are internal design/workstream vocabulary unless verified against the source. They are not authority to rename public APIs. N01 defines the exact source-derived public surface.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-auth-01 | ProtocolRequest, ProtocolError, HandlerDescriptor | Protocol model and event pipeline |
| dotj-auth-02 | AuthorizationTransaction, GrantRecord, TokenRecord | Authorization server and token lifecycle |
| dotj-auth-03 | ClientRegistration, LoginState, DiscoveryDocument | Client discovery and login state |
| dotj-auth-04 | JoseHeader, ValidationPolicy, KeyResolver | JOSE and resource validation |
| dotj-auth-05 | AuthorizationStore, TokenStore, AuthWebAdapter | Stores web integration and conformance |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Public async signatures retain the original Task/ValueTask type names and semantics; CompletionStage is permitted behind the compatibility facade or in optional Java interop, not as a silent replacement; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Preserve protocol rules and event ordering; Java APIs adapt async and storage abstractions. No compliance claim from happy-path token issuance.

## Feature contracts and invariants

### WP-01: Protocol model and event pipeline

Internal analysis vocabulary (not permission to rename the public API): `ProtocolRequest`, `ProtocolError`, `HandlerDescriptor`.

Inventory grants endpoints response modes and event order. Define normalized parameter multiplicity and validation failures. Version protocol capability profiles separately from Java APIs.

Required observable invariant: Duplicate security parameters are rejected consistently; handlers execute in declared order; unsupported grants return explicit protocol errors.

### WP-02: Authorization server and token lifecycle

Internal analysis vocabulary (not permission to rename the public API): `AuthorizationTransaction`, `GrantRecord`, `TokenRecord`.

Specify authorization code PKCE consent and redirect validation. Define refresh rotation revocation expiry and concurrent redemption. Separate confidential/public client credential validation.

Required observable invariant: Codes cannot be redeemed twice; redirect matching is exact per profile; replayed refresh tokens follow declared family-revocation policy.

### WP-03: Client discovery and login state

Internal analysis vocabulary (not permission to rename the public API): `ClientRegistration`, `LoginState`, `DiscoveryDocument`.

Bind state nonce and PKCE to a bounded login transaction. Validate discovery endpoints issuer and transport trust. Specify callback errors logout and key-refresh behavior.

Required observable invariant: Cross-session callbacks fail; unexpected issuers fail closed; discovery refresh cannot downgrade transport or algorithm policy.

### WP-04: JOSE and resource validation

Internal analysis vocabulary (not permission to rename the public API): `JoseHeader`, `ValidationPolicy`, `KeyResolver`.

Use JDK cryptographic primitives through explicit algorithm allowlists. Validate issuer audience lifetime token type and critical headers. Define key rotation cache expiry and unknown-key retry limits.

Required observable invariant: Algorithm/key-type confusion and unsigned tokens fail; malformed critical headers fail; key refresh is bounded under attacker-supplied IDs.

### WP-05: Stores web integration and conformance

Internal analysis vocabulary (not permission to rename the public API): `AuthorizationStore`, `TokenStore`, `AuthWebAdapter`.

Define transactional store invariants without an entity dependency. Integrate web challenges cookies and authorization context. Run negative protocol vectors and independent conformance tooling.

Required observable invariant: Concurrent redemption is serialized by storage contract; secrets are redacted; protocol claims identify exact tested profiles and unresolved certification.

## Bootstrap and dependency boundaries

JCA/JCE, TLS, secure randomness and own JOSE serialization; existing crypto primitives remain JDK-owned.

Proposed .j dependencies: web,json,core. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing OpenIddict usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then preserve the original public API names and workflow; the internal analysis label `ProtocolRequest` is not a replacement public API. Document unavoidable syntax/representation differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Duplicate security parameters are rejected consistently; handlers execute in declared order; unsupported grants return explicit protocol errors. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
