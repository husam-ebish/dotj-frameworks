# DJ-020 .j SQL: feature compatibility matrix

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Java records/constructors and generic erasure replace CLR mapping conventions. Preserve command disposal and streaming resource ownership.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Command and connection ownership | Internal planning vocabulary (verify upstream public identity): SqlCommand, CommandOptions, RowCursor | Closing a result releases owned statements; caller transactions are not committed implicitly; cancellation outcome reflects driver uncertainty | Planned; evidence gates open |
| WP-02 | Parameters and type conversion | Internal planning vocabulary (verify upstream public identity): ParameterBinder, TypeHandler, ColumnValue | Empty lists follow declared SQL policy; null parameter types are explicit; placeholder parsing cannot rewrite literal SQL text | Planned; evidence gates open |
| WP-03 | Row and object materialization | Internal planning vocabulary (verify upstream public identity): RowMapper, ConstructorBinding, MappingCacheKey | Schema changes cannot reuse incompatible mappings; errors identify column and destination; primitive nulls use declared policy | Planned; evidence gates open |
| WP-04 | Multi-mapping streaming and batching | Internal planning vocabulary (verify upstream public identity): SplitPoint, GridReader, BatchResult | Unread grids are drained or closed predictably; split ambiguity is reported; partial batch success is not collapsed into an all-or-nothing result | Planned; evidence gates open |
| WP-05 | Provider integration and optional contrib | Internal planning vocabulary (verify upstream public identity): SqlDialect, ProviderCapability, ContribProfile | Unsupported provider features fail visibly; extension provenance is separate; performance reports include query data and resource ownership assumptions | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Internal design labels are not public API replacements. Public contracts must preserve exact upstream names, casing and concepts under N01; the semantic mapping remains open. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Dapper extensions in other repos are not automatically included. Driver-specific type mapping needs explicit coverage.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
