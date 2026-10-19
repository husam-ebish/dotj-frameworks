# DJ-033 .j Refit: feature compatibility matrix

Attribute-driven C# interfaces map to Java annotations; generic return types and async error handling need explicit representation.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Interface contract and annotation model | Proposed Java contracts: HttpService, RouteAnnotation, ParameterBinding | Conflicting bindings fail with member location; inherited methods retain metadata; unsupported signatures never produce runtime surprises | Planned; evidence gates open |
| WP-02 | Java proxy and source generation | Proposed Java contracts: ClientDescriptor, GeneratedClient, InvocationPlan | Generated and proxy paths produce equivalent requests; no runtime C# expression/codegen dependency is assumed | Planned; evidence gates open |
| WP-03 | Serialization errors and streaming | Proposed Java contracts: ResponseType, ApiException, StreamResult | Deserialization failure retains HTTP context; streams close on cancellation; generic response types remain resolvable after erasure | Planned; evidence gates open |
| WP-04 | Authentication handlers and client lifetime | Proposed Java contracts: ClientFactory, RequestHandler, AuthorizationProvider | Concurrent users cannot share credentials accidentally; caller transport is not closed by generated clients; handler failures release request resources | Planned; evidence gates open |
| WP-05 | REST bridge and contract verification | Proposed Java contracts: RestTransportAdapter, ContractFixture, GeneratorDiagnostic | Base generated clients need only accepted transport contracts; URI/header fixtures match profile; no Retrofit replacement supplies the implementation | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Java contracts are proposals; they are not upstream class declarations. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Source-generated and runtime proxy modes need one contract; avoid requiring compiler tooling at runtime.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
