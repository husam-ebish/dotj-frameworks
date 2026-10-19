# DJ-050 .j XTest: feature compatibility matrix

Fact/Theory metadata adapts to annotations; assembly isolation becomes classloader/process isolation with explicit fixture lifetimes.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Discovery attributes and test identity | Proposed Java contracts: TestCaseId, Fact, Theory, DiscoveryMessage | Discovery is deterministic; malformed theories report discovery errors; IDs stay stable under unrelated source changes | Planned; evidence gates open |
| WP-02 | Fixtures lifetime and execution | Proposed Java contracts: TestContext, FixtureScope, ExecutionResult | Fixtures dispose once; failed setup prevents test body; teardown errors remain visible beside assertion failure | Planned; evidence gates open |
| WP-03 | Assertions and data theories | Proposed Java contracts: AssertionFailure, DataProvider, ComparisonPolicy | Failure output identifies first meaningful difference; data streams close; async exceptions are observed rather than lost | Planned; evidence gates open |
| WP-04 | Runner protocols parallelism and reporting | Proposed Java contracts: RunnerMessage, ExecutionCollection, ReportWriter | A crashed worker is distinguishable from failed tests; nonparallel collections are honored; report totals reconcile with discovered/executed cases | Planned; evidence gates open |
| WP-05 | Bootstrap and upstream conformance | Proposed Java contracts: StandaloneRunner, CompatibilityFixture, Adapter | No JUnit engine supplies the implementation; self-tests include an independent subprocess oracle; adapter failures cannot masquerade as green tests | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Java contracts are proposals; they are not upstream class declarations. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Runner packages may live elsewhere and version families differ. Avoid dependency on dotj-mock for framework bootstrap.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
