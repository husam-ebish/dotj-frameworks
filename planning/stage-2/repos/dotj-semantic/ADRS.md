# DJ-061 .j Semantic: architecture decisions

Status: provisional planning decisions, reviewable without starting implementation. No additional user answer is required to complete these written plans.

| ADR | Decision | Reason | Reopen when |
|---|---|---|---|
| A01 | JDK 25 non-preview as the portable desktop/server language/API proposal; exact binary lock remains required | Avoid framework substitution and preview API dependency | Platform backend requires a smaller language/API subset or vendor qualification fails |
| A02 | Own this product behavior; reuse JDK primitives and explicitly reviewed narrow platform/native dependencies | Port the C# kernel/plugin, model connector and orchestration capabilities to owned Java modules. | A dependency cannot meet required semantics or redistribution obligations |
| A03 | Use the contract/module split in JAVA-ARCHITECTURE | Separate portable behavior from integrations and lifecycle ownership | Provider SDKs/services and agent module maturity need version-specific mapping; no live model dependency in deterministic tests. |
| A04 | Preserve upstream capability families with explicit Java adaptations | The upstream is multi-language: inspect C# functionality and do not reuse its Java implementation. Provider schemas evolve independently of framework API parity. | Source audit discovers a missing family or incompatible assumption |
| A05 | Treat sampled source pin as analysis evidence; qualify a release/oracle before source-derived implementation | Default branch and root license are insufficient release evidence | E01 selects a different immutable release or resolves rights |
| A06 | Use owned neutral fixture format and standalone bootstrap runner | Avoid circular reliance on unfinished SDK/test/registry products | The shared runners can consume the same fixtures without semantic changes |

## Product-specific planning decisions

Define C# capability boundary, then kernel/plugin contracts, connector protocols and orchestration with recorded fixtures.

Scope census: kernel, plugins, prompt-templates, connector-SPI, tool-calling, memory/vector abstractions, agents where present.

Each WP must append its API signatures, state transitions, serialization/storage schema where applicable and failure/cleanup examples to these decisions before its implementation begins. The names in this package are sufficient for work decomposition, not a substitute for compiler-level public API review.
