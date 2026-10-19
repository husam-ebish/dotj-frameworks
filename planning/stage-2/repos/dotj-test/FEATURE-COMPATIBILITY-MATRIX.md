# DJ-051 .j Test: feature compatibility matrix

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

C# attributes and generic fixtures map to Java annotation/type-token policies; apartment-state tests remain platform-specific.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Test model discovery and attributes | Internal planning vocabulary (verify upstream public identity): TestSuite, TestCase, TestAttribute, Category | Invalid fixture combinations produce explicit errors; category filters are reproducible; discovery does not execute test bodies | Planned; evidence gates open |
| WP-02 | Constraint assertions and diagnostics | Internal planning vocabulary (verify upstream public identity): Constraint, ConstraintResult, ActualValue | Actual-value suppliers execute according to contract; compound constraints report meaningful subfailures; tolerance semantics are explicit | Planned; evidence gates open |
| WP-03 | Setup teardown and execution context | Internal planning vocabulary (verify upstream public identity): LifecyclePlan, ExecutionContext, TestResult | Failed setup has documented teardown behavior; context cannot leak across parallel tests; original failures survive cleanup exceptions | Planned; evidence gates open |
| WP-04 | Parameterized parallel and isolated execution | Internal planning vocabulary (verify upstream public identity): CaseSource, ParallelScope, WorkerSession | Case explosion has explicit limits; nonparallel rules are enforced; timed-out processes cannot corrupt runner state | Planned; evidence gates open |
| WP-05 | Runner reporting extensions and bootstrap | Internal planning vocabulary (verify upstream public identity): EngineProtocol, ResultXml, ExtensionPoint | Framework can run under a minimal owned harness; crashed tests have distinct results; external engine sources remain separately tracked | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Internal design labels are not public API replacements. Public contracts must preserve exact upstream names, casing and concepts under N01; the semantic mapping remains open. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Separate engine/adapter repositories must be tracked if not contained here; no JUnit bootstrap substitution.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
