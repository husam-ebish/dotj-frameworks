# DJ-019 .j Entity: Java architecture and contracts

Provide an owned ORM with query translation, tracking, transactions and schema evolution.

Product type: JVM data framework. Proposed Java package root: `org.dotj.entity`. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are design proposals, not already implemented APIs.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-entity-01 | EntityType, PropertyMapping, Relationship, ModelSnapshot | Model metadata and generated metamodel |
| dotj-entity-02 | QueryNode, Projection, SqlExpression, QueryPlan | Query IR and translation |
| dotj-entity-03 | IdentityMap, EntityEntry, StateTransition, ConcurrencyToken | Tracking relationships and change detection |
| dotj-entity-04 | RelationalProvider, CommandBatch, TransactionScope, Savepoint | Provider updates and transactions |
| dotj-entity-05 | SchemaModel, MigrationOperation, MigrationHistory | Migrations and schema comparison |
| dotj-entity-06 | DesignTimeContext, MigrationCli, QueryDiagnostic | Tooling providers and performance acceptance |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Async methods return CompletionStage; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Java lambdas are not inspectable C# expression trees. Propose explicit typed query AST with generated metamodels; evaluate source analysis separately.

## Feature contracts and invariants

### WP-01: Model metadata and generated metamodel

Contract vocabulary: `EntityType`, `PropertyMapping`, `Relationship`, `ModelSnapshot`.

Define keys owned types inheritance converters and nullability. Generate typed query/property references through annotation processing. Validate relationship cardinality and provider capabilities.

Required observable invariant: Ambiguous keys and unsupported mappings fail at model build; snapshots are deterministic; Java lambda bodies are not falsely treated as inspectable expressions.

### WP-02: Query IR and translation

Contract vocabulary: `QueryNode`, `Projection`, `SqlExpression`, `QueryPlan`.

Specify filters joins grouping ordering includes and parameterization. Apply SQL null/collation semantics explicitly. Reject unsupported server translation unless client evaluation is explicitly requested.

Required observable invariant: Injection payloads remain parameters; null-sensitive joins match reference cases; unsupported operations never silently load an entire table.

### WP-03: Tracking relationships and change detection

Contract vocabulary: `IdentityMap`, `EntityEntry`, `StateTransition`, `ConcurrencyToken`.

Define detached unchanged added modified and deleted transitions. Implement identity resolution relationship fixup and change snapshots. Specify optimistic concurrency conflict reporting.

Required observable invariant: One tracked key has one identity; relationship changes yield explainable updates; stale tokens produce conflicts without lost updates.

### WP-04: Provider updates and transactions

Contract vocabulary: `RelationalProvider`, `CommandBatch`, `TransactionScope`, `Savepoint`.

Separate database capability negotiation from common ORM logic. Order dependent inserts updates and deletes. Specify rollback savepoints cancellation and ambiguous commit outcomes.

Required observable invariant: Failed saves preserve documented tracking state; database transactions remain caller-owned when supplied; unknown commit outcome is not reported as safe retry.

### WP-05: Migrations and schema comparison

Contract vocabulary: `SchemaModel`, `MigrationOperation`, `MigrationHistory`.

Compute deterministic model/schema differences. Generate provider-specific reversible operations where possible. Require explicit acknowledgment of destructive or irreversible migration steps.

Required observable invariant: Schema diff handles renames only with evidence; history prevents duplicate application; failed migrations report actual transaction boundary.

### WP-06: Tooling providers and performance acceptance

Contract vocabulary: `DesignTimeContext`, `MigrationCli`, `QueryDiagnostic`.

Bootstrap with owned PostgreSQL provider and explicit provider SPI. Generate design-time models without application startup side effects. Measure query counts allocation and tracking overhead on fixed fixtures.

Required observable invariant: N+1 patterns are visible; tools reproduce locked schema output; no Hibernate or other Java ORM replaces the planned implementation.

## Bootstrap and dependency boundaries

java.sql contracts, reflection/MethodHandles and annotation processing; own PostgreSQL provider/client.

Proposed .j dependencies: core,postgresql. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing Entity Framework Core usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then express the same intent with `EntityType` and its companion contracts. Preserve semantic differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Ambiguous keys and unsupported mappings fail at model build; snapshots are deterministic; Java lambda bodies are not falsely treated as inspectable expressions. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
