# DJ-020 .j SQL: Java architecture and contracts

Offer lightweight query execution and row/object mapping without taking ownership of an ORM.

Product type: JVM data library. Proposed Java package root: `org.dotj.sql`. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are design proposals, not already implemented APIs.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-sql-01 | SqlCommand, CommandOptions, RowCursor | Command and connection ownership |
| dotj-sql-02 | ParameterBinder, TypeHandler, ColumnValue | Parameters and type conversion |
| dotj-sql-03 | RowMapper, ConstructorBinding, MappingCacheKey | Row and object materialization |
| dotj-sql-04 | SplitPoint, GridReader, BatchResult | Multi-mapping streaming and batching |
| dotj-sql-05 | SqlDialect, ProviderCapability, ContribProfile | Provider integration and optional contrib |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Async methods return CompletionStage; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Java records/constructors and generic erasure replace CLR mapping conventions. Preserve command disposal and streaming resource ownership.

## Feature contracts and invariants

### WP-01: Command and connection ownership

Contract vocabulary: `SqlCommand`, `CommandOptions`, `RowCursor`.

Define synchronous/asynchronous execution over JDBC contracts. Distinguish caller-supplied connections and transactions from owned ones. Specify timeout cancellation and connection reuse after errors.

Required observable invariant: Closing a result releases owned statements; caller transactions are not committed implicitly; cancellation outcome reflects driver uncertainty.

### WP-02: Parameters and type conversion

Contract vocabulary: `ParameterBinder`, `TypeHandler`, `ColumnValue`.

Define named parameters list expansion null typing and output values. Map Java records primitives enums and database-specific types. Reject ambiguous parameter replacement inside strings/comments.

Required observable invariant: Empty lists follow declared SQL policy; null parameter types are explicit; placeholder parsing cannot rewrite literal SQL text.

### WP-03: Row and object materialization

Contract vocabulary: `RowMapper`, `ConstructorBinding`, `MappingCacheKey`.

Resolve constructor/property mapping and column-name policies. Handle duplicate columns missing values and conversion failures. Cache mappings by complete result shape and target type.

Required observable invariant: Schema changes cannot reuse incompatible mappings; errors identify column and destination; primitive nulls use declared policy.

### WP-04: Multi-mapping streaming and batching

Contract vocabulary: `SplitPoint`, `GridReader`, `BatchResult`.

Define split boundaries and parent/child result materialization. Enforce sequential multi-result ownership and streaming lifecycle. Specify batch partial-failure reporting.

Required observable invariant: Unread grids are drained or closed predictably; split ambiguity is reported; partial batch success is not collapsed into an all-or-nothing result.

### WP-05: Provider integration and optional contrib

Contract vocabulary: `SqlDialect`, `ProviderCapability`, `ContribProfile`.

Test with owned PostgreSQL driver and explicit capabilities. Separate upstream contrib/external extension repositories from core scope. Measure buffered versus streaming allocation and query throughput.

Required observable invariant: Unsupported provider features fail visibly; extension provenance is separate; performance reports include query data and resource ownership assumptions.

## Bootstrap and dependency boundaries

JDBC interfaces, reflection and MethodHandles; own driver supplies database transport.

Proposed .j dependencies: postgresql,core. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing Dapper usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then express the same intent with `SqlCommand` and its companion contracts. Preserve semantic differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Closing a result releases owned statements; caller transactions are not committed implicitly; cancellation outcome reflects driver uncertainty. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
