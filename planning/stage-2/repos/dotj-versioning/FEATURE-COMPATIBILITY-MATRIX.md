# DJ-035 .j Versioning: feature compatibility matrix

Preserve query/header/media-type version negotiation and ambiguity behavior; Java endpoint metadata replaces ASP.NET action descriptors.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Version model and readers | Proposed Java contracts: ApiVersion, VersionReader, VersionSet | Same request cannot silently select between conflicting versions; invalid syntax has stable error details; neutral endpoints have explicit rules | Planned; evidence gates open |
| WP-02 | Endpoint selection and reporting | Proposed Java contracts: VersionedEndpoint, SelectionPolicy, VersionReport | Unsupported versions produce documented status; route ambiguity fails at startup; reports match registered endpoint metadata | Planned; evidence gates open |
| WP-03 | MVC and minimal API conventions | Proposed Java contracts: VersionConvention, ControllerVersionModel, EndpointGroup | Inherited actions resolve consistently; explicit declarations override conventions predictably; core version model loads without MVC | Planned; evidence gates open |
| WP-04 | API exploration and documentation | Proposed Java contracts: VersionedDescription, GroupName, ParameterSubstitution | Documents contain only applicable operations; conflicting operation IDs are diagnosed; URL substitution does not change unrelated parameters | Planned; evidence gates open |
| WP-05 | Migration and compatibility cases | Proposed Java contracts: VersioningProfile, RequestFixture, DeprecationPolicy | Examples produce reproducible routing outcomes; deprecation is metadata rather than silent removal; no unsupported version appears supported | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Java contracts are proposals; they are not upstream class declarations. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Legacy and current package families may differ; inspect MVC/minimal API/OData integrations independently.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
