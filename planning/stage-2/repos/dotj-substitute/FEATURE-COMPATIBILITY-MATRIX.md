# DJ-053 .j Substitute: feature compatibility matrix

Thread-local recording and fluent setup must avoid consuming production calls; Java primitive defaults and overloads need a documented DSL.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Substitution and call specification | Proposed Java contracts: Substitute, CallSpecification, ArgumentSpecification | Ambiguous matchers fail clearly; configuration does not count as an ordinary received call; overload matching is stable | Planned; evidence gates open |
| WP-02 | Returns callbacks and recursive values | Proposed Java contracts: ReturnSequence, CallAction, AutoValueProvider | Exhausted sequences obey documented policy; holder adaptation is explicit; recursive substitutes remain stable per configured path | Planned; evidence gates open |
| WP-03 | Received calls order and events | Proposed Java contracts: ReceivedCheck, CallOrder, EventAdapter | Order checks identify missing/out-of-order calls; predicate errors are diagnosable; listener raises follow declared exception rules | Planned; evidence gates open |
| WP-04 | Proxy instrumentation and thread state | Proposed Java contracts: SubstituteFactory, InterceptionCapability, ConfigurationScope | Parallel configuration cannot cross-contaminate substitutes; unsupported members fail explicitly; no Mockito implementation is adopted | Planned; evidence gates open |
| WP-05 | Integration and regression acceptance | Proposed Java contracts: SubstituteCase, AssertionAdapter, CleanupRecord | Substitutes run independently of NUnit/xUnit ports; reset clears only owned state; instrumentation capabilities are reported accurately | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Java contracts are proposals; they are not upstream class declarations. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Reuse only a neutral proxy submodule if suitable; preserve distinct public semantics and avoid dependency cycles with mock.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
