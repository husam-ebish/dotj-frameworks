# DJ-026 .j Validation: feature compatibility matrix

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Property paths and lambda-based member discovery need generated accessors or explicit paths; avoid fragile serialized-lambda inspection.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Rule model and fluent construction | Internal planning vocabulary (verify upstream public identity): Validator, Rule, PropertyPath, RuleSet | Rule ordering is deterministic; nested paths preserve collection indices; concurrent validations do not share mutable request state | Planned; evidence gates open |
| WP-02 | Built-in validators and comparisons | Internal planning vocabulary (verify upstream public identity): Constraint, ComparisonContext, MessageArgument | Null-versus-empty behavior matches its profile; locale changes do not alter invariant constraints; pathological patterns obey declared resource limits | Planned; evidence gates open |
| WP-03 | Asynchronous and child validation | Internal planning vocabulary (verify upstream public identity): ValidationContext, AsyncRule, ChildValidator | Cancellation prevents later rules where promised; child failures retain paths; thrown application errors are not misreported as ordinary invalid input | Planned; evidence gates open |
| WP-04 | Messages localization and extensibility | Internal planning vocabulary (verify upstream public identity): MessageCatalog, CustomValidator, FailureFormatter | Missing translations use documented fallback; custom failures preserve codes/severity; passwords are not included in default messages | Planned; evidence gates open |
| WP-05 | Web integration and regression acceptance | Internal planning vocabulary (verify upstream public identity): ValidationAdapter, ValidationResult, RuleCoverage | Core validation runs without web dependencies; API responses retain stable field paths; upstream unsupported rules remain explicit inventory entries | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Internal design labels are not public API replacements. Public contracts must preserve exact upstream names, casing and concepts under N01; the semantic mapping remains open. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Locale resources and ASP.NET-specific automatic validation need adaptation; synchronous invocation of async rules needs explicit behavior.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
