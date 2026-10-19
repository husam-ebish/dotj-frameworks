# DJ-019 .j Entity: feature compatibility matrix

Java lambdas are not inspectable C# expression trees. Propose explicit typed query AST with generated metamodels; evaluate source analysis separately.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Model metadata and generated metamodel | Proposed Java contracts: EntityType, PropertyMapping, Relationship, ModelSnapshot | Ambiguous keys and unsupported mappings fail at model build; snapshots are deterministic; Java lambda bodies are not falsely treated as inspectable expressions | Planned; evidence gates open |
| WP-02 | Query IR and translation | Proposed Java contracts: QueryNode, Projection, SqlExpression, QueryPlan | Injection payloads remain parameters; null-sensitive joins match reference cases; unsupported operations never silently load an entire table | Planned; evidence gates open |
| WP-03 | Tracking relationships and change detection | Proposed Java contracts: IdentityMap, EntityEntry, StateTransition, ConcurrencyToken | One tracked key has one identity; relationship changes yield explainable updates; stale tokens produce conflicts without lost updates | Planned; evidence gates open |
| WP-04 | Provider updates and transactions | Proposed Java contracts: RelationalProvider, CommandBatch, TransactionScope, Savepoint | Failed saves preserve documented tracking state; database transactions remain caller-owned when supplied; unknown commit outcome is not reported as safe retry | Planned; evidence gates open |
| WP-05 | Migrations and schema comparison | Proposed Java contracts: SchemaModel, MigrationOperation, MigrationHistory | Schema diff handles renames only with evidence; history prevents duplicate application; failed migrations report actual transaction boundary | Planned; evidence gates open |
| WP-06 | Tooling providers and performance acceptance | Proposed Java contracts: DesignTimeContext, MigrationCli, QueryDiagnostic | N+1 patterns are visible; tools reproduce locked schema output; no Hibernate or other Java ORM replaces the planned implementation | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Java contracts are proposals; they are not upstream class declarations. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Lazy proxies, provider variations, LINQ coverage and distributed transactions need contracts. Avoid entity depending on sql mapper by default.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
