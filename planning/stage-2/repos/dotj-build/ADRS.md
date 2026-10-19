# DJ-005 .j Build: architecture decisions

Status: provisional planning decisions, reviewable without starting implementation. No additional user answer is required to complete these written plans.

| ADR | Decision | Reason | Reopen when |
|---|---|---|---|
| A01 | JDK 25 non-preview as the portable desktop/server language/API proposal; exact binary lock remains required | Avoid framework substitution and preview API dependency | Platform backend requires a smaller language/API subset or vendor qualification fails |
| A02 | Own this product behavior; reuse JDK primitives and explicitly reviewed narrow platform/native dependencies | Create a Java build graph engine with evaluation, task execution and incremental-build capabilities. | A dependency cannot meet required semantics or redistribution obligations |
| A03 | Use the contract/module split in JAVA-ARCHITECTURE | Separate portable behavior from integrations and lifecycle ownership | Do we preserve MSBuild XML semantics or define a native Java project format plus importer? Inline task code and Windows registry access need separate decisions. |
| A04 | Preserve upstream capability families with explicit Java adaptations | MSBuild property/item evaluation and target ordering need explicit emulation; .NET task assemblies require Java replacements or an optional external process bridge. | Source audit discovers a missing family or incompatible assumption |
| A05 | Treat sampled source pin as analysis evidence; qualify a release/oracle before source-derived implementation | Default branch and root license are insufficient release evidence | E01 selects a different immutable release or resolves rights |
| A06 | Use owned neutral fixture format and standalone bootstrap runner | Avoid circular reliance on unfinished SDK/test/registry products | The shared runners can consume the same fixtures without semantic changes |

## Product-specific planning decisions

Model evaluation separately from execution; establish graph/cache semantics; add task SPI and portability contracts before SDK integration.

Scope census: project-evaluation, target-graph, task-host, incremental-state, parallel-scheduler, logging; compatibility importer is optional and explicit.

Each WP must append its API signatures, state transitions, serialization/storage schema where applicable and failure/cleanup examples to these decisions before its implementation begins. The names in this package are sufficient for work decomposition, not a substitute for compiler-level public API review.
