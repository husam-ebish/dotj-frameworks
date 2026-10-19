# DJ-038 .j Graph Platform: architecture decisions

Status: provisional planning decisions, reviewable without starting implementation. No additional user answer is required to complete these written plans.

| ADR | Decision | Reason | Reopen when |
|---|---|---|---|
| A01 | JDK 25 non-preview as the portable desktop/server language/API proposal; exact binary lock remains required | Avoid framework substitution and preview API dependency | Platform backend requires a smaller language/API subset or vendor qualification fails |
| A02 | Own this product behavior; reuse JDK primitives and explicitly reviewed narrow platform/native dependencies | Reproduce server, client-generation and composition capabilities from the C# GraphQL platform. | A dependency cannot meet required semantics or redistribution obligations |
| A03 | Use the contract/module split in JAVA-ARCHITECTURE | Separate portable behavior from integrations and lifecycle ownership | Do not conflate open C# source with separately licensed tooling. Share only a neutral syntax submodule with dotj-graphql if semantics align. |
| A04 | Preserve upstream capability families with explicit Java adaptations | Preserve GraphQL protocol behavior; generated .NET clients become Java clients with explicit cache and nullability semantics. Commercial tooling boundaries remain visible. | Source audit discovers a missing family or incompatible assumption |
| A05 | Treat sampled source pin as analysis evidence; qualify a release/oracle before source-derived implementation | Default branch and root license are insufficient release evidence | E01 selects a different immutable release or resolves rights |
| A06 | Use owned neutral fixture format and standalone bootstrap runner | Avoid circular reliance on unfinished SDK/test/registry products | The shared runners can consume the same fixtures without semantic changes |

## Product-specific planning decisions

Inventory product subtrees, establish executable schema contracts, then execution/client codegen and composition tracks.

Scope census: schema, execution, subscriptions, data-loading, federation/composition, client-codegen, tooling; keep Hot Chocolate and Strawberry Shake visible.

Each WP must append its API signatures, state transitions, serialization/storage schema where applicable and failure/cleanup examples to these decisions before its implementation begins. The names in this package are sufficient for work decomposition, not a substitute for compiler-level public API review.
