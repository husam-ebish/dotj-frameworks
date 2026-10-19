# DJ-037 .j OpenAPI: Java architecture and contracts

Generate OpenAPI documents and typed clients with owned tooling.

Product type: JVM developer/library project. Proposed Java package root: `org.dotj.openapi`. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are design proposals, not already implemented APIs.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-openapi-01 | OpenApiDocument, Schema, Operation, Dialect | Document object model and dialects |
| dotj-openapi-02 | DocumentReader, DocumentWriter, Diagnostic | Readers writers and diagnostics |
| dotj-openapi-03 | ReferenceId, DocumentWorkspace, ResolutionPolicy | Reference resolution and workspaces |
| dotj-openapi-04 | ValidationRule, DocumentVisitor, VersionConverter | Validation transformations and visitors |
| dotj-openapi-05 | DocumentDiff, CompatibilityFinding, RoundTripCase | Diff utilities and conformance corpus |
| dotj-openapi-06 | SchemaGenerator, EndpointDescription, DocumentProcessor | NSwag schema and endpoint generation |
| dotj-openapi-07 | ClientGenerator, GeneratorSettings, GeneratedArtifact | Java TypeScript and retained language generators |
| dotj-openapi-08 | NswagDocument, GenerationCommand, StudioProject | CLI build integration and Studio tooling |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Async methods return CompletionStage; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

C# client generation becomes a separate retained language-output track; Java output is primary. Specification version and nullable semantics must be explicit.

## Feature contracts and invariants

### WP-01: Document object model and dialects

Contract vocabulary: `OpenApiDocument`, `Schema`, `Operation`, `Dialect`.

Inventory supported OpenAPI versions and JSON Schema dialects. Model extensions nullable references and ordered metadata. Preserve unknown extension values without arbitrary type activation.

Required observable invariant: Round trips preserve extensions; version-specific keywords are validated; incompatible dialect fields are not silently rewritten.

### WP-02: Readers writers and diagnostics

Contract vocabulary: `DocumentReader`, `DocumentWriter`, `Diagnostic`.

Implement JSON through owned serializer contracts. Treat YAML parser as an explicitly owned/dependency-gated component. Preserve source locations and stable canonical output.

Required observable invariant: Malformed input yields path/location diagnostics; JSON output is deterministic; YAML support is not claimed before parser evidence exists.

### WP-03: Reference resolution and workspaces

Contract vocabulary: `ReferenceId`, `DocumentWorkspace`, `ResolutionPolicy`.

Resolve local/external references with cycle detection. Restrict network/file resolution through caller policy. Cache by URI and content identity.

Required observable invariant: Recursive schemas terminate without losing references; untrusted documents cannot fetch arbitrary local files; changed content invalidates cache.

### WP-04: Validation transformations and visitors

Contract vocabulary: `ValidationRule`, `DocumentVisitor`, `VersionConverter`.

Separate structural validation from semantic rules. Define visitor mutation and extension behavior. Report lossy version conversions explicitly.

Required observable invariant: Duplicate/missing operation constraints are diagnosed; conversion lists dropped semantics; validation never repairs a document invisibly.

### WP-05: Diff utilities and conformance corpus

Contract vocabulary: `DocumentDiff`, `CompatibilityFinding`, `RoundTripCase`.

Map upstream utilities and optional integrations to owned modules. Port reader/writer/reference regression fixtures. Compare normalized documents with format-aware rules.

Required observable invariant: Formatting-only changes do not count as semantic breaks; unresolved references remain visible; no Swagger UI assets are folded into this model library.

### WP-06: NSwag schema and endpoint generation

Contract vocabulary: `SchemaGenerator`, `EndpointDescription`, `DocumentProcessor`.

Inventory NJsonSchema and template-engine source dependencies explicitly. Generate schemas/documents from Java types and dotj-web endpoint metadata. Define processor order inheritance nullability and polymorphic schemas.

Required observable invariant: Recursive schema generation terminates; processor errors retain source identity; owned schema scope is not claimed to exist just because the NSwag repo references it.

### WP-07: Java TypeScript and retained language generators

Contract vocabulary: `ClientGenerator`, `GeneratorSettings`, `GeneratedArtifact`.

Generate Java clients as primary JVM adaptation. Retain TypeScript and C# client/controller outputs as separately specified language tracks. Define authentication cancellation errors templates and deterministic source output.

Required observable invariant: Generated Java/TypeScript samples compile with locked toolchains; unsupported C# generation capabilities remain inventoried; runtime-specific annotations are not emitted accidentally.

### WP-08: CLI build integration and Studio tooling

Contract vocabulary: `NswagDocument`, `GenerationCommand`, `StudioProject`.

Read versioned generation configurations and resolve variables safely. Expose standalone CLI before optional build/SDK adapters. Keep NSwagStudio-equivalent desktop UI behind a separate platform work package.

Required observable invariant: CLI generation needs no desktop runtime; configs reproduce outputs; Studio remains a visible feasibility gate rather than being omitted from scope.

## Bootstrap and dependency boundaries

Own JSON, XML where required, Java source generation and filesystem.

Proposed .j dependencies: json;code(dev-optional). Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing NSwag usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then express the same intent with `OpenApiDocument` and its companion contracts. Preserve semantic differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Round trips preserve extensions; version-specific keywords are validated; incompatible dialect fields are not silently rewritten. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
