# DJ-012 .j Web: architecture decisions

Status: provisional planning decisions, reviewable without starting implementation. No additional user answer is required to complete these written plans.

| ADR | Decision | Reason | Reopen when |
|---|---|---|---|
| A01 | JDK 25 non-preview as the portable desktop/server language/API proposal; exact binary lock remains required | Avoid framework substitution and preview API dependency | Platform backend requires a smaller language/API subset or vendor qualification fails |
| A02 | Own this product behavior; reuse JDK primitives and explicitly reviewed narrow platform/native dependencies | Reproduce ASP.NET Core's server application and component capabilities with an owned Java web stack. | A dependency cannot meet required semantics or redistribution obligations |
| A03 | Use the contract/module split in JAVA-ARCHITECTURE | Separate portable behavior from integrations and lifecycle ownership | HTTP/2 and HTTP/3, QUIC bindings, browser runtime and Identity stores require feasibility and threat reviews. Maintain all listed subsystems visibly. |
| A04 | Preserve upstream capability families with explicit Java adaptations | Server rendering and persistent component circuits are plausible JVM tracks. Browser execution needs a separately justified JS/Wasm compilation/runtime design; browsers do not supply a JVM. | Source audit discovers a missing family or incompatible assumption |
| A05 | Treat sampled source pin as analysis evidence; qualify a release/oracle before source-derived implementation | Default branch and root license are insufficient release evidence | E01 selects a different immutable release or resolves rights |
| A06 | Use owned neutral fixture format and standalone bootstrap runner | Avoid circular reliance on unfinished SDK/test/registry products | The shared runners can consume the same fixtures without semantic changes |

## Product-specific planning decisions

Partition server transport and application layers; agree Razor IR; plan security and protocols; investigate browser backend independently.

Scope census: middleware, HTTP/Kestrel-equivalent server, routing, MVC, APIs, Razor Pages, Blazor-style components, Identity, security, SignalR, hosting and diagnostics.

Each WP must append its API signatures, state transitions, serialization/storage schema where applicable and failure/cleanup examples to these decisions before its implementation begins. The names in this package are sufficient for work decomposition, not a substitute for compiler-level public API review.
