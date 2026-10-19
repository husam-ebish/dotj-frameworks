# DJ-050 .j XTest: feature compatibility matrix

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Fact/Theory metadata adapts to annotations; assembly isolation becomes classloader/process isolation with explicit fixture lifetimes.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Discovery attributes and test identity | Internal planning vocabulary (verify upstream public identity): TestCaseId, Fact, Theory, DiscoveryMessage | Discovery is deterministic; malformed theories report discovery errors; IDs stay stable under unrelated source changes | Planned; evidence gates open |
| WP-02 | Fixtures lifetime and execution | Internal planning vocabulary (verify upstream public identity): TestContext, FixtureScope, ExecutionResult | Fixtures dispose once; failed setup prevents test body; teardown errors remain visible beside assertion failure | Planned; evidence gates open |
| WP-03 | Assertions and data theories | Internal planning vocabulary (verify upstream public identity): AssertionFailure, DataProvider, ComparisonPolicy | Failure output identifies first meaningful difference; data streams close; async exceptions are observed rather than lost | Planned; evidence gates open |
| WP-04 | Runner protocols parallelism and reporting | Internal planning vocabulary (verify upstream public identity): RunnerMessage, ExecutionCollection, ReportWriter | A crashed worker is distinguishable from failed tests; nonparallel collections are honored; report totals reconcile with discovered/executed cases | Planned; evidence gates open |
| WP-05 | Bootstrap and upstream conformance | Internal planning vocabulary (verify upstream public identity): StandaloneRunner, CompatibilityFixture, Adapter | No JUnit engine supplies the implementation; self-tests include an independent subprocess oracle; adapter failures cannot masquerade as green tests | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Internal design labels are not public API replacements. Public contracts must preserve exact upstream names, casing and concepts under N01; the semantic mapping remains open. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Runner packages may live elsewhere and version families differ. Avoid dependency on dotj-mock for framework bootstrap.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
