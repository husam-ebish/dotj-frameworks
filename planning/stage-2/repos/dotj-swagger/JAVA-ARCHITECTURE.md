# DJ-036 .j Swagger: Java architecture and contracts

Generate and serve OpenAPI descriptions from .j endpoints with interactive documentation integration.

Product type: JVM API tooling. Proposed Java package root: `org.dotj.swagger`. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are design proposals, not already implemented APIs.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-swagger-01 | ApiDescription, SchemaRegistry, OperationGenerator | Endpoint discovery and schema generation |
| dotj-swagger-02 | DocumentFilter, OperationFilter, SchemaFilter | Document filters and customization |
| dotj-swagger-03 | SwaggerEndpoint, UiAssetManifest, AccessPolicy | Document serving and UI assets |
| dotj-swagger-04 | DocumentGroup, SecurityScheme, ExampleProvider | Versioning and security descriptions |
| dotj-swagger-05 | SchemaFixture, OperationFixture, UiSmokeCase | Compatibility and generated-document acceptance |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Async methods return CompletionStage; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Preserve schema customization and endpoint discovery behavior, not ASP.NET reflection APIs. Swagger UI licensing/assets need explicit provenance.

## Feature contracts and invariants

### WP-01: Endpoint discovery and schema generation

Contract vocabulary: `ApiDescription`, `SchemaRegistry`, `OperationGenerator`.

Read web metadata through optional adapters. Generate schemas for Java generics nullability and polymorphism. Assign stable schema IDs with collision diagnostics.

Required observable invariant: Recursive types terminate via references; same-simple-name classes do not collide silently; ignored endpoints stay excluded.

### WP-02: Document filters and customization

Contract vocabulary: `DocumentFilter`, `OperationFilter`, `SchemaFilter`.

Define deterministic extension order and error reporting. Expose safe document mutation through dotj-openapi. Separate global and per-document configuration.

Required observable invariant: Filter failure identifies its source; multiple documents do not share mutable schemas; extensions survive serialization.

### WP-03: Document serving and UI assets

Contract vocabulary: `SwaggerEndpoint`, `UiAssetManifest`, `AccessPolicy`.

Serve versioned generated documents with cache invalidation. Inventory Swagger UI/ReDoc assets as separate upstream dependencies. Define UI authentication CSP and external URL policy.

Required observable invariant: Private docs require configured access; UI assets have provenance and pinned checksums; untrusted document URLs cannot bypass access policy.

### WP-04: Versioning and security descriptions

Contract vocabulary: `DocumentGroup`, `SecurityScheme`, `ExampleProvider`.

Integrate optional API version groups. Describe authentication schemes without asserting runtime enforcement. Validate examples against emitted schema where supported.

Required observable invariant: Document groups match routing version metadata; security declarations do not masquerade as enforcement; invalid examples are reported.

### WP-05: Compatibility and generated-document acceptance

Contract vocabulary: `SchemaFixture`, `OperationFixture`, `UiSmokeCase`.

Port schema naming operation filtering and regressions. Compare normalized documents using openapi model. Smoke-test UI against generated documents and base paths.

Required observable invariant: Each advertised generator behavior has fixtures; reverse-proxy base paths remain valid; no existing Java Swagger generator replaces implementation.

## Bootstrap and dependency boundaries

Reflection and annotations; share OpenAPI model with dotj-openapi; browser UI assets are separate dependencies.

Proposed .j dependencies: web,openapi. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing Swashbuckle usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then express the same intent with `ApiDescription` and its companion contracts. Preserve semantic differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Recursive types terminate via references; same-simple-name classes do not collide silently; ignored endpoints stay excluded. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
