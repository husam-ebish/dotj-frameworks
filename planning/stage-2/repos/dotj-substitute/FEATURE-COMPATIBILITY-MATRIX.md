# DJ-053 .j Substitute: feature compatibility matrix

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Thread-local recording and fluent setup must avoid consuming production calls; Java primitive defaults and overloads need a documented DSL.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Substitution and call specification | Internal planning vocabulary (verify upstream public identity): Substitute, CallSpecification, ArgumentSpecification | Ambiguous matchers fail clearly; configuration does not count as an ordinary received call; overload matching is stable | Planned; evidence gates open |
| WP-02 | Returns callbacks and recursive values | Internal planning vocabulary (verify upstream public identity): ReturnSequence, CallAction, AutoValueProvider | Exhausted sequences obey documented policy; holder adaptation is explicit; recursive substitutes remain stable per configured path | Planned; evidence gates open |
| WP-03 | Received calls order and events | Internal planning vocabulary (verify upstream public identity): ReceivedCheck, CallOrder, EventAdapter | Order checks identify missing/out-of-order calls; predicate errors are diagnosable; listener raises follow declared exception rules | Planned; evidence gates open |
| WP-04 | Proxy instrumentation and thread state | Internal planning vocabulary (verify upstream public identity): SubstituteFactory, InterceptionCapability, ConfigurationScope | Parallel configuration cannot cross-contaminate substitutes; unsupported members fail explicitly; no Mockito implementation is adopted | Planned; evidence gates open |
| WP-05 | Integration and regression acceptance | Internal planning vocabulary (verify upstream public identity): SubstituteCase, AssertionAdapter, CleanupRecord | Substitutes run independently of NUnit/xUnit ports; reset clears only owned state; instrumentation capabilities are reported accurately | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Internal design labels are not public API replacements. Public contracts must preserve exact upstream names, casing and concepts under N01; the semantic mapping remains open. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Reuse only a neutral proxy submodule if suitable; preserve distinct public semantics and avoid dependency cycles with mock.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
