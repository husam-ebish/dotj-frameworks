# DJ-025 .j Container: feature compatibility matrix

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Translate open generics to type tokens; ownership and scope disposal must be explicit. Dynamic class interception is not JDK interface proxy equivalence.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Registration model and resolution | Internal planning vocabulary (verify upstream public identity): ServiceKey, Registration, ResolutionContext | Ambiguous constructors fail deterministically; generic constraints are enforced; circular resolution errors identify the cycle | Planned; evidence gates open |
| WP-02 | Scopes ownership and disposal | Internal planning vocabulary (verify upstream public identity): LifetimeScope, OwnedValue, ReleaseAction | Externally supplied objects remain untouched; alias registrations dispose once; failed activation cleans partially constructed owned dependencies | Planned; evidence gates open |
| WP-03 | Modules scanning and activation pipelines | Internal planning vocabulary (verify upstream public identity): RegistrationModule, ComponentScanner, ActivationMiddleware | Scanning executes no static application initialization; activation hook failures do not leak instances; module precedence is reproducible | Planned; evidence gates open |
| WP-04 | Advanced relationships and interception | Internal planning vocabulary (verify upstream public identity): LazyService, ServiceFactory, MetadataValue, InterceptorAdapter | Lazy/factory values respect originating scope; metadata does not force instantiation; unsupported final-class interception is explicit | Planned; evidence gates open |
| WP-05 | Core bridge and concurrent acceptance | Internal planning vocabulary (verify upstream public identity): CoreContainerAdapter, ScopeDiagnostic, StressScenario | Bridge differences are documented; a disposed scope cannot admit new resolutions; optional adapter creates no core-to-container dependency | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Internal design labels are not public API replacements. Public contracts must preserve exact upstream names, casing and concepts under N01; the semantic mapping remains open. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Core owns minimal DI contracts; this repo owns the richer engine. Proxy integration is optional and must not introduce a mock-library cycle.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
