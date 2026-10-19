# DJ-024 .j Mapster: Java architecture and contracts

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Provide convention-based object mapping with compiled or generated mapping plans.

Product type: JVM mapping/code-generation library. Public package names preserve the exact source namespace identity and casing, subject to explicit JVM/JPMS feasibility. `org.dotj.internal.*` is reserved for hidden implementation helpers. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are internal design/workstream vocabulary unless verified against the source. They are not authority to rename public APIs. N01 defines the exact source-derived public surface.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-mapster-01 | MappingConfig, TypePair, MemberPath | Configuration and type model |
| dotj-mapster-02 | MappingPlan, MemberAssignment, ConversionStep | Mapping plan and execution |
| dotj-mapster-03 | GeneratedMapper, SourceLocation, GenerationManifest | Generated mappings and diagnostics |
| dotj-mapster-04 | ProjectionPlan, QueryProviderAdapter, ProjectionCapability | Queryable projection boundary |
| dotj-mapster-05 | MapperFacade, DependencyResolver, MapsterProfile | Adapters and behavior parity |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Public async signatures retain the original Task/ValueTask type names and semantics; CompletionStage is permitted behind the compatibility facade or in optional Java interop, not as a silent replacement; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

C# expression trees become explicit mapping IR; Java generic erasure and records require constructor and type-token policies.

## Feature contracts and invariants

### WP-01: Configuration and type model

Internal analysis vocabulary (not permission to rename the public API): `MappingConfig`, `TypePair`, `MemberPath`.

Define global scoped and per-map configuration precedence. Resolve Java generic types records and accessors. Validate conflicting rules before compilation.

Required observable invariant: A map has a reproducible effective configuration; ambiguous members fail early; configuration caches are isolated by scope.

### WP-02: Mapping plan and execution

Internal analysis vocabulary (not permission to rename the public API): `MappingPlan`, `MemberAssignment`, `ConversionStep`.

Compile explicit mapping IR instead of CLR expression trees. Handle null propagation converters nested objects and collections. Preserve configured reference identity and cycle behavior.

Required observable invariant: Nested failures name the member path; cycles terminate by policy; collection replacement versus merge is predictable.

### WP-03: Generated mappings and diagnostics

Internal analysis vocabulary (not permission to rename the public API): `GeneratedMapper`, `SourceLocation`, `GenerationManifest`.

Generate Java source through stable compiler interfaces. Report unsupported conversions at generation time. Make generated output reproducible and inspectable.

Required observable invariant: Generated and runtime maps agree on fixed fixtures; clean rebuild produces equivalent source; diagnostics point to the declaration.

### WP-04: Queryable projection boundary

Internal analysis vocabulary (not permission to rename the public API): `ProjectionPlan`, `QueryProviderAdapter`, `ProjectionCapability`.

Represent database projections using entity query IR. Separate in-memory conversion from translatable operations. Reject unsupported projection nodes before query execution.

Required observable invariant: Unsupported converter never falls back to full-table client mapping silently; projected null semantics match provider profile.

### WP-05: Adapters and behavior parity

Internal analysis vocabulary (not permission to rename the public API): `MapperFacade`, `DependencyResolver`, `MapsterProfile`.

Keep DI integrations optional. Port configuration inheritance collection and conversion regressions. Measure compile time versus steady-state mapping separately.

Required observable invariant: Core mapper loads without a DI framework; warm/cold results are reported separately; no existing Java mapper replaces implementation.

## Bootstrap and dependency boundaries

Reflection, MethodHandles and annotation processors.

Proposed .j dependencies: core;entity(optional). Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing Mapster usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then preserve the original public API names and workflow; the internal analysis label `MappingConfig` is not a replacement public API. Document unavoidable syntax/representation differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: A map has a reproducible effective configuration; ambiguous members fail early; configuration caches are isolated by scope. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
