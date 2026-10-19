# DJ-024 .j Mapster: feature compatibility matrix

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

C# expression trees become explicit mapping IR; Java generic erasure and records require constructor and type-token policies.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Configuration and type model | Internal planning vocabulary (verify upstream public identity): MappingConfig, TypePair, MemberPath | A map has a reproducible effective configuration; ambiguous members fail early; configuration caches are isolated by scope | Planned; evidence gates open |
| WP-02 | Mapping plan and execution | Internal planning vocabulary (verify upstream public identity): MappingPlan, MemberAssignment, ConversionStep | Nested failures name the member path; cycles terminate by policy; collection replacement versus merge is predictable | Planned; evidence gates open |
| WP-03 | Generated mappings and diagnostics | Internal planning vocabulary (verify upstream public identity): GeneratedMapper, SourceLocation, GenerationManifest | Generated and runtime maps agree on fixed fixtures; clean rebuild produces equivalent source; diagnostics point to the declaration | Planned; evidence gates open |
| WP-04 | Queryable projection boundary | Internal planning vocabulary (verify upstream public identity): ProjectionPlan, QueryProviderAdapter, ProjectionCapability | Unsupported converter never falls back to full-table client mapping silently; projected null semantics match provider profile | Planned; evidence gates open |
| WP-05 | Adapters and behavior parity | Internal planning vocabulary (verify upstream public identity): MapperFacade, DependencyResolver, MapsterProfile | Core mapper loads without a DI framework; warm/cold results are reported separately; no existing Java mapper replaces implementation | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Internal design labels are not public API replacements. Public contracts must preserve exact upstream names, casing and concepts under N01; the semantic mapping remains open. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Query projection must target entity IR without pulling ORM into base mapper; source-generator package boundaries need inspection.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
