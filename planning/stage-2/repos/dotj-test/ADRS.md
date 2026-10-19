# DJ-051 .j Test: architecture decisions

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Status: provisional planning decisions, reviewable without starting implementation. No additional user answer is required to complete these written plans.

| ADR | Decision | Reason | Reopen when |
|---|---|---|---|
| A01 | JDK 25 non-preview as the portable desktop/server language/API proposal; exact binary lock remains required | Avoid framework substitution and preview API dependency | Platform backend requires a smaller language/API subset or vendor qualification fails |
| A02 | Own this product behavior; reuse JDK primitives and explicitly reviewed narrow platform/native dependencies | Implement NUnit-style fixtures, parameterized tests, constraints and execution policies. | A dependency cannot meet required semantics or redistribution obligations |
| A03 | Use the contract/module split in JAVA-ARCHITECTURE | Separate portable behavior from integrations and lifecycle ownership | Separate engine/adapter repositories must be tracked if not contained here; no JUnit bootstrap substitution. |
| A04 | Preserve exact upstream public names, casing, concepts and workflows; isolate Java syntax/implementation differences | C# attributes and generic fixtures map to Java annotation/type-token policies; apartment-state tests remain platform-specific. | Source audit discovers a missing family or incompatible assumption |
| A05 | Treat sampled source pin as analysis evidence; qualify a release/oracle before source-derived implementation | Default branch and root license are insufficient release evidence | E01 selects a different immutable release or resolves rights |
| A06 | Use owned neutral fixture format and standalone bootstrap runner | Avoid circular reliance on unfinished SDK/test/registry products | The shared runners can consume the same fixtures without semantic changes |

## Product-specific planning decisions

Define fixture/constraint semantics, then execution scheduling and results, then adapters.

Scope census: attributes/annotations, fixture-builder, constraint-model, execution-context, parallelization, result-format.

Each WP must append its API signatures, state transitions, serialization/storage schema where applicable and failure/cleanup examples to these decisions before its implementation begins. The names in this package are sufficient for work decomposition, not a substitute for compiler-level public API review.

## A07: exact .NET public API identity

Status: **owner-required**. Public spelling, casing, namespaces and concepts follow the selected upstream profile exactly. Prior Java-style public naming proposals are superseded. Internal labels may remain private; language/JVM conflicts are explicit blockers. [Policy](../../08-DOTNET-API-COMPATIBILITY-POLICY.md). No feature may satisfy compatibility solely by offering similar behavior through different public names.
