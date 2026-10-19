# DJ-039 .j GraphQL: feature compatibility matrix

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

GraphQL semantics can interoperate while C# resolver delegates adapt to Java. No reuse of graphql-java.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Parser AST and schema types | Internal planning vocabulary (verify upstream public identity): DocumentNode, GraphType, Schema | Malformed documents have stable spans; invalid schemas fail before execution; scalar coercion is defined for literals and variables | Planned; evidence gates open |
| WP-02 | Validation coercion and operation planning | Internal planning vocabulary (verify upstream public identity): ValidationContext, VariableValue, ExecutionPlan | Omitted and explicit-null inputs differ correctly; fragment cycles fail; stale schema plans cannot execute silently | Planned; evidence gates open |
| WP-03 | Execution errors and asynchronous fields | Internal planning vocabulary (verify upstream public identity): ExecutionContext, FieldResult, ExecutionError | Errors retain field/index paths; non-null violations bubble correctly; internal stack traces are hidden unless explicitly enabled | Planned; evidence gates open |
| WP-04 | Subscriptions loaders and adapters | Internal planning vocabulary (verify upstream public identity): SubscriptionSource, DataLoader, GraphHttpAdapter | Disconnect closes subscriptions; cache entries cannot leak across requests; core executor needs no web framework | Planned; evidence gates open |
| WP-05 | Specification and upstream regression suite | Internal planning vocabulary (verify upstream public identity): GraphProfile, ValidationCase, ExecutionTrace | Claims identify exact specification/profile; expensive requests are bounded; no graphql-java substitution implements the port | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Internal design labels are not public API replacements. Public contracts must preserve exact upstream names, casing and concepts under N01; the semantic mapping remains open. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Keep this engine independent of graph-platform; optional shared syntax ownership must not force identical execution models.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
