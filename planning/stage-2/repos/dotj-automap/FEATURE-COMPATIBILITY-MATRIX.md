# DJ-064 .j Automap: feature compatibility matrix

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

C# expression trees and flattening conventions need Java equivalents; preserve distinctions from Mapster instead of merging products.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | License baseline and mapping contract | Internal planning vocabulary (verify upstream public identity): MappingLicenseRecord, MappingProfile, TypeMap | No source-derived implementation proceeds under assumed MIT terms; profile validation reports unmapped/conflicting members; rights gate is recorded separately from architecture | Planned; evidence gates open |
| WP-02 | Mapping plan resolution and execution | Internal planning vocabulary (verify upstream public identity): ResolutionContext, MemberPlan, ValueResolver | Cycles follow declared preservation policy; hook order is stable; errors identify source/destination member paths | Planned; evidence gates open |
| WP-03 | Configuration validation and advanced mapping | Internal planning vocabulary (verify upstream public identity): ConfigurationProvider, InclusionRule, ConversionPolicy | Invalid reverse maps fail early; concurrent requests cannot share scoped resolver state; cache keys include configuration identity | Planned; evidence gates open |
| WP-04 | Query projection and expression adaptation | Internal planning vocabulary (verify upstream public identity): ProjectionExpression, EntityProjectionAdapter, ProjectionDiagnostic | Provider SQL remains parameterized; unsupported resolver yields a planning diagnostic; no entire-table fallback occurs silently | Planned; evidence gates open |
| WP-05 | Adapters and behavioral verification | Internal planning vocabulary (verify upstream public identity): MapperService, MapFixture, LicenseGate | Behavior evidence is separate from license clearance; no ModelMapper substitute is adopted; all unresolved licensed features remain listed | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Internal design labels are not public API replacements. Public contracts must preserve exact upstream names, casing and concepts under N01; the semantic mapping remains open. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Version-specific licensing is a hard source-reuse decision. Inspect selected historical/current tags and notices before derivation.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
