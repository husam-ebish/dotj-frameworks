# DJ-019 .j Entity: architecture decisions

Status: provisional planning decisions, reviewable without starting implementation. No additional user answer is required to complete these written plans.

| ADR | Decision | Reason | Reopen when |
|---|---|---|---|
| A01 | JDK 25 non-preview as the portable desktop/server language/API proposal; exact binary lock remains required | Avoid framework substitution and preview API dependency | Platform backend requires a smaller language/API subset or vendor qualification fails |
| A02 | Own this product behavior; reuse JDK primitives and explicitly reviewed narrow platform/native dependencies | Provide an owned ORM with query translation, tracking, transactions and schema evolution. | A dependency cannot meet required semantics or redistribution obligations |
| A03 | Use the contract/module split in JAVA-ARCHITECTURE | Separate portable behavior from integrations and lifecycle ownership | Lazy proxies, provider variations, LINQ coverage and distributed transactions need contracts. Avoid entity depending on sql mapper by default. |
| A04 | Preserve upstream capability families with explicit Java adaptations | Java lambdas are not inspectable C# expression trees. Propose explicit typed query AST with generated metamodels; evaluate source analysis separately. | Source audit discovers a missing family or incompatible assumption |
| A05 | Treat sampled source pin as analysis evidence; qualify a release/oracle before source-derived implementation | Default branch and root license are insufficient release evidence | E01 selects a different immutable release or resolves rights |
| A06 | Use owned neutral fixture format and standalone bootstrap runner | Avoid circular reliance on unfinished SDK/test/registry products | The shared runners can consume the same fixtures without semantic changes |

## Product-specific planning decisions

Define provider SPI and query IR, then model/tracking, translation/update, migrations and tooling with provider-specific acceptance.

Scope census: model, query-IR, SQL-translator, tracking, change-detection, update-pipeline, transactions, migrations, provider-SPI, tooling.

Each WP must append its API signatures, state transitions, serialization/storage schema where applicable and failure/cleanup examples to these decisions before its implementation begins. The names in this package are sufficient for work decomposition, not a substitute for compiler-level public API review.
