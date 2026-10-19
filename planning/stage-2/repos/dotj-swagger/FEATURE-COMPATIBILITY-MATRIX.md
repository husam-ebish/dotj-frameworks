# DJ-036 .j Swagger: feature compatibility matrix

Preserve schema customization and endpoint discovery behavior, not ASP.NET reflection APIs. Swagger UI licensing/assets need explicit provenance.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Endpoint discovery and schema generation | Proposed Java contracts: ApiDescription, SchemaRegistry, OperationGenerator | Recursive types terminate via references; same-simple-name classes do not collide silently; ignored endpoints stay excluded | Planned; evidence gates open |
| WP-02 | Document filters and customization | Proposed Java contracts: DocumentFilter, OperationFilter, SchemaFilter | Filter failure identifies its source; multiple documents do not share mutable schemas; extensions survive serialization | Planned; evidence gates open |
| WP-03 | Document serving and UI assets | Proposed Java contracts: SwaggerEndpoint, UiAssetManifest, AccessPolicy | Private docs require configured access; UI assets have provenance and pinned checksums; untrusted document URLs cannot bypass access policy | Planned; evidence gates open |
| WP-04 | Versioning and security descriptions | Proposed Java contracts: DocumentGroup, SecurityScheme, ExampleProvider | Document groups match routing version metadata; security declarations do not masquerade as enforcement; invalid examples are reported | Planned; evidence gates open |
| WP-05 | Compatibility and generated-document acceptance | Proposed Java contracts: SchemaFixture, OperationFixture, UiSmokeCase | Each advertised generator behavior has fixtures; reverse-proxy base paths remain valid; no existing Java Swagger generator replaces implementation | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Java contracts are proposals; they are not upstream class declarations. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Swagger UI and OpenAPI model dependencies may live outside this repo; decide whether to port UI behavior or approve assets individually.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
