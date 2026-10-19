# DJ-038 .j Graph Platform: feature compatibility matrix

Preserve GraphQL protocol behavior; generated .NET clients become Java clients with explicit cache and nullability semantics. Commercial tooling boundaries remain visible.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Language schema and execution ownership | Proposed Java contracts: GraphDocument, SchemaDefinition, ExecutionPlan | Every source product family has a target owner; independent executors do not silently share incompatible semantics; parser errors retain source spans | Planned; evidence gates open |
| WP-02 | Resolver pipeline and data loading | Proposed Java contracts: ResolverContext, FieldMiddleware, DataLoader | N+1 fixtures show intended batching; loader caches do not cross users; non-null failures propagate to the correct parent | Planned; evidence gates open |
| WP-03 | Transport subscriptions and persistence | Proposed Java contracts: GraphRequest, SubscriptionSession, PersistedOperation | Unknown persisted IDs cannot bypass validation; disconnected subscriptions release resources; protocol-specific error behavior is tested | Planned; evidence gates open |
| WP-04 | Federation composition and gateway | Proposed Java contracts: SubgraphSchema, CompositionResult, QueryPlan | Conflicting field ownership fails composition; gateway cannot forward caller credentials beyond policy; partial errors preserve service context | Planned; evidence gates open |
| WP-05 | Client generation tooling and schema evolution | Proposed Java contracts: GeneratedClient, OperationManifest, SchemaDiff | Invalid operations fail generation; union handling is exhaustive by profile; generated sources compile without reusing an existing Java GraphQL client | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Java contracts are proposals; they are not upstream class declarations. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Do not conflate open C# source with separately licensed tooling. Share only a neutral syntax submodule with dotj-graphql if semantics align.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
