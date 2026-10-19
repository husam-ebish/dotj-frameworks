# DJ-020 .j SQL: feature compatibility matrix

Java records/constructors and generic erasure replace CLR mapping conventions. Preserve command disposal and streaming resource ownership.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Command and connection ownership | Proposed Java contracts: SqlCommand, CommandOptions, RowCursor | Closing a result releases owned statements; caller transactions are not committed implicitly; cancellation outcome reflects driver uncertainty | Planned; evidence gates open |
| WP-02 | Parameters and type conversion | Proposed Java contracts: ParameterBinder, TypeHandler, ColumnValue | Empty lists follow declared SQL policy; null parameter types are explicit; placeholder parsing cannot rewrite literal SQL text | Planned; evidence gates open |
| WP-03 | Row and object materialization | Proposed Java contracts: RowMapper, ConstructorBinding, MappingCacheKey | Schema changes cannot reuse incompatible mappings; errors identify column and destination; primitive nulls use declared policy | Planned; evidence gates open |
| WP-04 | Multi-mapping streaming and batching | Proposed Java contracts: SplitPoint, GridReader, BatchResult | Unread grids are drained or closed predictably; split ambiguity is reported; partial batch success is not collapsed into an all-or-nothing result | Planned; evidence gates open |
| WP-05 | Provider integration and optional contrib | Proposed Java contracts: SqlDialect, ProviderCapability, ContribProfile | Unsupported provider features fail visibly; extension provenance is separate; performance reports include query data and resource ownership assumptions | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Java contracts are proposals; they are not upstream class declarations. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Dapper extensions in other repos are not automatically included. Driver-specific type mapping needs explicit coverage.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
