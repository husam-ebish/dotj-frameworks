# DJ-020 .j SQL: Java architecture and contracts

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Offer lightweight query execution and row/object mapping without taking ownership of an ORM.

Product type: JVM data library. Public package names preserve the exact source namespace identity and casing, subject to explicit JVM/JPMS feasibility. `org.dotj.internal.*` is reserved for hidden implementation helpers. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are internal design/workstream vocabulary unless verified against the source. They are not authority to rename public APIs. N01 defines the exact source-derived public surface.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-sql-01 | SqlCommand, CommandOptions, RowCursor | Command and connection ownership |
| dotj-sql-02 | ParameterBinder, TypeHandler, ColumnValue | Parameters and type conversion |
| dotj-sql-03 | RowMapper, ConstructorBinding, MappingCacheKey | Row and object materialization |
| dotj-sql-04 | SplitPoint, GridReader, BatchResult | Multi-mapping streaming and batching |
| dotj-sql-05 | SqlDialect, ProviderCapability, ContribProfile | Provider integration and optional contrib |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Public async signatures retain the original Task/ValueTask type names and semantics; CompletionStage is permitted behind the compatibility facade or in optional Java interop, not as a silent replacement; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Java records/constructors and generic erasure replace CLR mapping conventions. Preserve command disposal and streaming resource ownership.

## Feature contracts and invariants

### WP-01: Command and connection ownership

Internal analysis vocabulary (not permission to rename the public API): `SqlCommand`, `CommandOptions`, `RowCursor`.

Define synchronous/asynchronous execution over JDBC contracts. Distinguish caller-supplied connections and transactions from owned ones. Specify timeout cancellation and connection reuse after errors.

Required observable invariant: Closing a result releases owned statements; caller transactions are not committed implicitly; cancellation outcome reflects driver uncertainty.

### WP-02: Parameters and type conversion

Internal analysis vocabulary (not permission to rename the public API): `ParameterBinder`, `TypeHandler`, `ColumnValue`.

Define named parameters list expansion null typing and output values. Map Java records primitives enums and database-specific types. Reject ambiguous parameter replacement inside strings/comments.

Required observable invariant: Empty lists follow declared SQL policy; null parameter types are explicit; placeholder parsing cannot rewrite literal SQL text.

### WP-03: Row and object materialization

Internal analysis vocabulary (not permission to rename the public API): `RowMapper`, `ConstructorBinding`, `MappingCacheKey`.

Resolve constructor/property mapping and column-name policies. Handle duplicate columns missing values and conversion failures. Cache mappings by complete result shape and target type.

Required observable invariant: Schema changes cannot reuse incompatible mappings; errors identify column and destination; primitive nulls use declared policy.

### WP-04: Multi-mapping streaming and batching

Internal analysis vocabulary (not permission to rename the public API): `SplitPoint`, `GridReader`, `BatchResult`.

Define split boundaries and parent/child result materialization. Enforce sequential multi-result ownership and streaming lifecycle. Specify batch partial-failure reporting.

Required observable invariant: Unread grids are drained or closed predictably; split ambiguity is reported; partial batch success is not collapsed into an all-or-nothing result.

### WP-05: Provider integration and optional contrib

Internal analysis vocabulary (not permission to rename the public API): `SqlDialect`, `ProviderCapability`, `ContribProfile`.

Test with owned PostgreSQL driver and explicit capabilities. Separate upstream contrib/external extension repositories from core scope. Measure buffered versus streaming allocation and query throughput.

Required observable invariant: Unsupported provider features fail visibly; extension provenance is separate; performance reports include query data and resource ownership assumptions.

## Bootstrap and dependency boundaries

JDBC interfaces, reflection and MethodHandles; own driver supplies database transport.

Proposed .j dependencies: postgresql,core. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing Dapper usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then preserve the original public API names and workflow; the internal analysis label `SqlCommand` is not a replacement public API. Document unavoidable syntax/representation differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Closing a result releases owned statements; caller transactions are not committed implicitly; cancellation outcome reflects driver uncertainty. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
