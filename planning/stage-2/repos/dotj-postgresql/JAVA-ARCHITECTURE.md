# DJ-021 .j PostgreSQL: Java architecture and contracts

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Implement our own PostgreSQL wire client and investigate a JDBC-compatible facade.

Product type: JVM database driver. Public package names preserve the exact source namespace identity and casing, subject to explicit JVM/JPMS feasibility. `org.dotj.internal.*` is reserved for hidden implementation helpers. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are internal design/workstream vocabulary unless verified against the source. They are not authority to rename public APIs. N01 defines the exact source-derived public surface.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-postgresql-01 | PgMessage, SessionState, AuthenticationExchange | Wire framing startup and authentication |
| dotj-postgresql-02 | QueryCycle, Portal, PreparedStatement, CancelKey | Simple extended queries and cancellation |
| dotj-postgresql-03 | PgTypeId, TextCodec, BinaryCodec, TypeRegistry | Type codecs and PostgreSQL semantics |
| dotj-postgresql-04 | PoolLease, ConnectorState, HostPolicy | Pooling multiplexing and failover |
| dotj-postgresql-05 | CopySession, Notification, ReplicationPosition | COPY notifications replication and large objects |
| dotj-postgresql-06 | JdbcMethodMatrix, DatabaseMetaData, DriverCapability | JDBC facade and server compatibility |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Public async signatures retain the original Task/ValueTask type names and semantics; CompletionStage is permitted behind the compatibility facade or in optional Java interop, not as a silent replacement; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

PostgreSQL wire compatibility is primary; Npgsql API shape adapts to Java. JDBC completeness needs a method-by-method contract and test evidence.

## Feature contracts and invariants

### WP-01: Wire framing startup and authentication

Internal analysis vocabulary (not permission to rename the public API): `PgMessage`, `SessionState`, `AuthenticationExchange`.

Implement bounded length-delimited protocol decoding. Negotiate TLS startup parameters and SCRAM authentication. Validate server identity and authentication state transitions.

Required observable invariant: Truncated/oversized frames fail without unbounded allocation; SCRAM vectors pass; credentials never enter trace output.

### WP-02: Simple extended queries and cancellation

Internal analysis vocabulary (not permission to rename the public API): `QueryCycle`, `Portal`, `PreparedStatement`, `CancelKey`.

Model Parse Bind Describe Execute Sync and ReadyForQuery. Handle interleaved notices errors and transaction states. Use a separate cancellation channel with race-aware outcomes.

Required observable invariant: Error recovery reaches a valid sync boundary; cancel affects only its backend session; lost commit response remains an unknown outcome.

### WP-03: Type codecs and PostgreSQL semantics

Internal analysis vocabulary (not permission to rename the public API): `PgTypeId`, `TextCodec`, `BinaryCodec`, `TypeRegistry`.

Map numeric arrays ranges composites JSON time and nulls. Load server type metadata with versioned cache invalidation. Preserve precision infinities timezone and multidimensional array bounds.

Required observable invariant: Boundary values round trip; unknown OIDs return an explicit unsupported type; no decimal precision is silently truncated.

### WP-04: Pooling multiplexing and failover

Internal analysis vocabulary (not permission to rename the public API): `PoolLease`, `ConnectorState`, `HostPolicy`.

Reset session state before returning connectors to pools. Separate transaction-bound connectors from multiplexed work. Specify host selection authentication refresh and failed-lease eviction.

Required observable invariant: Session variables do not leak between leases; interrupted COPY does not return a dirty connector; ambiguous operations are not replayed silently.

### WP-05: COPY notifications replication and large objects

Internal analysis vocabulary (not permission to rename the public API): `CopySession`, `Notification`, `ReplicationPosition`.

Specify streaming COPY ownership and backpressure. Handle asynchronous notifications without corrupting query sequencing. Implement replication/large-object profiles behind versioned capability gates.

Required observable invariant: COPY cancellation restores or discards connection safely; notification queues are bounded; replication acknowledgments never exceed durably processed position.

### WP-06: JDBC facade and server compatibility

Internal analysis vocabulary (not permission to rename the public API): `JdbcMethodMatrix`, `DatabaseMetaData`, `DriverCapability`.

Map JDBC methods individually onto wire capabilities. Define unsupported methods transaction isolation and result-set modes. Run server-version TLS auth and protocol failure matrices.

Required observable invariant: JDBC unsupported operations raise explicit standard failures; advertised metadata matches tests; no existing PostgreSQL JDBC driver supplies the implementation.

## Bootstrap and dependency boundaries

Sockets/SSLEngine, JCA SCRAM primitives, ByteBuffer and java.sql; no existing JDBC driver substitution.

Proposed .j dependencies: core. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing Npgsql usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then preserve the original public API names and workflow; the internal analysis label `PgMessage` is not a replacement public API. Document unavoidable syntax/representation differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Truncated/oversized frames fail without unbounded allocation; SCRAM vectors pass; credentials never enter trace output. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
