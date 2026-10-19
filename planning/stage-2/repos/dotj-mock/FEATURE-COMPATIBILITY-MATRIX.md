# DJ-052 .j Mock: feature compatibility matrix

C# expression-based setups need an owned invocation DSL. Final/static/private mocking is not assumed; capability tiers must be explicit.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Mock model and invocation recording | Proposed Java contracts: Mock, Invocation, MethodKey, ArgumentMatcher | Overload identities do not collide; strict unexpected calls fail immediately; matcher state does not leak between threads | Planned; evidence gates open |
| WP-02 | Setup return callbacks and verification | Proposed Java contracts: Setup, Answer, Verification, Times | Setup order is deterministic; failed verification shows actual calls; callbacks throwing still record invocation according to contract | Planned; evidence gates open |
| WP-03 | Proxy and instrumentation feasibility | Proposed Java contracts: ProxyFactory, InstrumentationCapability, ClassTransform | Interface mocks work without an agent; unsupported member interception fails clearly; instrumentation is not secretly provided by Mockito/ByteBuddy | Planned; evidence gates open |
| WP-04 | Lifecycle concurrency and cleanup | Proposed Java contracts: MockScope, InvocationStore, AgentSession | Reset cannot corrupt active invocations; classloader stress shows no unbounded retention; failed transformations preserve valid classes | Planned; evidence gates open |
| WP-05 | Language adaptations and conformance | Proposed Java contracts: MockExpression, MatchSpecification, MockCase | DSL validates method identity before use; adaptations are visible; upstream features without Java equivalents remain explicit coverage entries | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Java contracts are proposals; they are not upstream class declarations. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Inspect Castle/DynamicProxy dependency and version-specific provenance. Agent attachment and JPMS access constraints need explicit support policy.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
