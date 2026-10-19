# DJ-064 .j Automap: Java architecture and contracts

Provide convention-based mapping, configuration validation and query projection.

Product type: JVM mapping library. Proposed Java package root: `org.dotj.automap`. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are design proposals, not already implemented APIs.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-automap-01 | MappingLicenseRecord, MappingProfile, TypeMap | License baseline and mapping contract |
| dotj-automap-02 | ResolutionContext, MemberPlan, ValueResolver | Mapping plan resolution and execution |
| dotj-automap-03 | ConfigurationProvider, InclusionRule, ConversionPolicy | Configuration validation and advanced mapping |
| dotj-automap-04 | ProjectionExpression, EntityProjectionAdapter, ProjectionDiagnostic | Query projection and expression adaptation |
| dotj-automap-05 | MapperService, MapFixture, LicenseGate | Adapters and behavioral verification |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Async methods return CompletionStage; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

C# expression trees and flattening conventions need Java equivalents; preserve distinctions from Mapster instead of merging products.

## Feature contracts and invariants

### WP-01: License baseline and mapping contract

Contract vocabulary: `MappingLicenseRecord`, `MappingProfile`, `TypeMap`.

Freeze inspected AutoMapper revision and applicable license options. Define member naming visibility null and constructor policies. Keep source reuse blocked until rights are resolved.

Required observable invariant: No source-derived implementation proceeds under assumed MIT terms; profile validation reports unmapped/conflicting members; rights gate is recorded separately from architecture.

### WP-02: Mapping plan resolution and execution

Contract vocabulary: `ResolutionContext`, `MemberPlan`, `ValueResolver`.

Build explicit Java mapping IR and conversion pipeline. Handle nested mappings inheritance collections and references. Define before/after hooks and error-path reporting.

Required observable invariant: Cycles follow declared preservation policy; hook order is stable; errors identify source/destination member paths.

### WP-03: Configuration validation and advanced mapping

Contract vocabulary: `ConfigurationProvider`, `InclusionRule`, `ConversionPolicy`.

Specify inherited/reverse maps conditional members and transformers. Validate configuration before execution. Separate immutable compiled plans from scoped resolver state.

Required observable invariant: Invalid reverse maps fail early; concurrent requests cannot share scoped resolver state; cache keys include configuration identity.

### WP-04: Query projection and expression adaptation

Contract vocabulary: `ProjectionExpression`, `EntityProjectionAdapter`, `ProjectionDiagnostic`.

Translate supported member expressions into entity query IR. Differentiate runtime-only resolvers from translatable nodes. Reject unsupported projections without implicit client evaluation.

Required observable invariant: Provider SQL remains parameterized; unsupported resolver yields a planning diagnostic; no entire-table fallback occurs silently.

### WP-05: Adapters and behavioral verification

Contract vocabulary: `MapperService`, `MapFixture`, `LicenseGate`.

Keep DI/provider integrations optional. Port mapping/configuration/projection regressions after rights review. Compare runtime/generated execution strategies on fixed cases.

Required observable invariant: Behavior evidence is separate from license clearance; no ModelMapper substitute is adopted; all unresolved licensed features remain listed.

## Bootstrap and dependency boundaries

Reflection, MethodHandles, annotations and own query IR adapter.

Proposed .j dependencies: core;entity(optional). Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing AutoMapper usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then express the same intent with `MappingLicenseRecord` and its companion contracts. Preserve semantic differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: No source-derived implementation proceeds under assumed MIT terms; profile validation reports unmapped/conflicting members; rights gate is recorded separately from architecture. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
