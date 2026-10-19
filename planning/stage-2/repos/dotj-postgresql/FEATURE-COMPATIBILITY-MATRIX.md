# DJ-021 .j PostgreSQL: feature compatibility matrix

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

PostgreSQL wire compatibility is primary; Npgsql API shape adapts to Java. JDBC completeness needs a method-by-method contract and test evidence.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Wire framing startup and authentication | Internal planning vocabulary (verify upstream public identity): PgMessage, SessionState, AuthenticationExchange | Truncated/oversized frames fail without unbounded allocation; SCRAM vectors pass; credentials never enter trace output | Planned; evidence gates open |
| WP-02 | Simple extended queries and cancellation | Internal planning vocabulary (verify upstream public identity): QueryCycle, Portal, PreparedStatement, CancelKey | Error recovery reaches a valid sync boundary; cancel affects only its backend session; lost commit response remains an unknown outcome | Planned; evidence gates open |
| WP-03 | Type codecs and PostgreSQL semantics | Internal planning vocabulary (verify upstream public identity): PgTypeId, TextCodec, BinaryCodec, TypeRegistry | Boundary values round trip; unknown OIDs return an explicit unsupported type; no decimal precision is silently truncated | Planned; evidence gates open |
| WP-04 | Pooling multiplexing and failover | Internal planning vocabulary (verify upstream public identity): PoolLease, ConnectorState, HostPolicy | Session variables do not leak between leases; interrupted COPY does not return a dirty connector; ambiguous operations are not replayed silently | Planned; evidence gates open |
| WP-05 | COPY notifications replication and large objects | Internal planning vocabulary (verify upstream public identity): CopySession, Notification, ReplicationPosition | COPY cancellation restores or discards connection safely; notification queues are bounded; replication acknowledgments never exceed durably processed position | Planned; evidence gates open |
| WP-06 | JDBC facade and server compatibility | Internal planning vocabulary (verify upstream public identity): JdbcMethodMatrix, DatabaseMetaData, DriverCapability | JDBC unsupported operations raise explicit standard failures; advertised metadata matches tests; no existing PostgreSQL JDBC driver supplies the implementation | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Internal design labels are not public API replacements. Public contracts must preserve exact upstream names, casing and concepts under N01; the semantic mapping remains open. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Replication, multiplexing, GSS/SSPI and unsupported JDBC features require separate decisions and server-version matrix.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
