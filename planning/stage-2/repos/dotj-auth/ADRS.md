# DJ-016 .j Auth: architecture decisions

Status: provisional planning decisions, reviewable without starting implementation. No additional user answer is required to complete these written plans.

| ADR | Decision | Reason | Reopen when |
|---|---|---|---|
| A01 | JDK 25 non-preview as the portable desktop/server language/API proposal; exact binary lock remains required | Avoid framework substitution and preview API dependency | Platform backend requires a smaller language/API subset or vendor qualification fails |
| A02 | Own this product behavior; reuse JDK primitives and explicitly reviewed narrow platform/native dependencies | Implement OAuth/OIDC client, server and validation capabilities with own protocol processing. | A dependency cannot meet required semantics or redistribution obligations |
| A03 | Use the contract/module split in JAVA-ARCHITECTURE | Separate portable behavior from integrations and lifecycle ownership | Investigate IdentityModel/JWT dependencies, supported grants, JOSE algorithms and optional certification suites. Store adapters must not create a core/entity cycle. |
| A04 | Preserve upstream capability families with explicit Java adaptations | Preserve protocol rules and event ordering; Java APIs adapt async and storage abstractions. No compliance claim from happy-path token issuance. | Source audit discovers a missing family or incompatible assumption |
| A05 | Treat sampled source pin as analysis evidence; qualify a release/oracle before source-derived implementation | Default branch and root license are insufficient release evidence | E01 selects a different immutable release or resolves rights |
| A06 | Use owned neutral fixture format and standalone bootstrap runner | Avoid circular reliance on unfinished SDK/test/registry products | The shared runners can consume the same fixtures without semantic changes |

## Product-specific planning decisions

Freeze protocol surface and threat model; partition cryptography adapters and stores; then plan server/client validation evidence.

Scope census: protocol-model, server-pipeline, client-pipeline, token-validation, store-contracts, web-integration.

Each WP must append its API signatures, state transitions, serialization/storage schema where applicable and failure/cleanup examples to these decisions before its implementation begins. The names in this package are sufficient for work decomposition, not a substitute for compiler-level public API review.
