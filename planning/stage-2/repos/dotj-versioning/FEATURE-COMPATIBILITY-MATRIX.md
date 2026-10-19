# DJ-035 .j Versioning: feature compatibility matrix

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Preserve query/header/media-type version negotiation and ambiguity behavior; Java endpoint metadata replaces ASP.NET action descriptors.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Version model and readers | Internal planning vocabulary (verify upstream public identity): ApiVersion, VersionReader, VersionSet | Same request cannot silently select between conflicting versions; invalid syntax has stable error details; neutral endpoints have explicit rules | Planned; evidence gates open |
| WP-02 | Endpoint selection and reporting | Internal planning vocabulary (verify upstream public identity): VersionedEndpoint, SelectionPolicy, VersionReport | Unsupported versions produce documented status; route ambiguity fails at startup; reports match registered endpoint metadata | Planned; evidence gates open |
| WP-03 | MVC and minimal API conventions | Internal planning vocabulary (verify upstream public identity): VersionConvention, ControllerVersionModel, EndpointGroup | Inherited actions resolve consistently; explicit declarations override conventions predictably; core version model loads without MVC | Planned; evidence gates open |
| WP-04 | API exploration and documentation | Internal planning vocabulary (verify upstream public identity): VersionedDescription, GroupName, ParameterSubstitution | Documents contain only applicable operations; conflicting operation IDs are diagnosed; URL substitution does not change unrelated parameters | Planned; evidence gates open |
| WP-05 | Migration and compatibility cases | Internal planning vocabulary (verify upstream public identity): VersioningProfile, RequestFixture, DeprecationPolicy | Examples produce reproducible routing outcomes; deprecation is metadata rather than silent removal; no unsupported version appears supported | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Internal design labels are not public API replacements. Public contracts must preserve exact upstream names, casing and concepts under N01; the semantic mapping remains open. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Legacy and current package families may differ; inspect MVC/minimal API/OData integrations independently.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
