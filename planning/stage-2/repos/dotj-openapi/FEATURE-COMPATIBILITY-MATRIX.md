# DJ-037 .j OpenAPI: feature compatibility matrix

C# client generation becomes a separate retained language-output track; Java output is primary. Specification version and nullable semantics must be explicit.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Document object model and dialects | Proposed Java contracts: OpenApiDocument, Schema, Operation, Dialect | Round trips preserve extensions; version-specific keywords are validated; incompatible dialect fields are not silently rewritten | Planned; evidence gates open |
| WP-02 | Readers writers and diagnostics | Proposed Java contracts: DocumentReader, DocumentWriter, Diagnostic | Malformed input yields path/location diagnostics; JSON output is deterministic; YAML support is not claimed before parser evidence exists | Planned; evidence gates open |
| WP-03 | Reference resolution and workspaces | Proposed Java contracts: ReferenceId, DocumentWorkspace, ResolutionPolicy | Recursive schemas terminate without losing references; untrusted documents cannot fetch arbitrary local files; changed content invalidates cache | Planned; evidence gates open |
| WP-04 | Validation transformations and visitors | Proposed Java contracts: ValidationRule, DocumentVisitor, VersionConverter | Duplicate/missing operation constraints are diagnosed; conversion lists dropped semantics; validation never repairs a document invisibly | Planned; evidence gates open |
| WP-05 | Diff utilities and conformance corpus | Proposed Java contracts: DocumentDiff, CompatibilityFinding, RoundTripCase | Formatting-only changes do not count as semantic breaks; unresolved references remain visible; no Swagger UI assets are folded into this model library | Planned; evidence gates open |
| WP-06 | NSwag schema and endpoint generation | Proposed Java contracts: SchemaGenerator, EndpointDescription, DocumentProcessor | Recursive schema generation terminates; processor errors retain source identity; owned schema scope is not claimed to exist just because the NSwag repo references it | Planned; evidence gates open |
| WP-07 | Java TypeScript and retained language generators | Proposed Java contracts: ClientGenerator, GeneratorSettings, GeneratedArtifact | Generated Java/TypeScript samples compile with locked toolchains; unsupported C# generation capabilities remain inventoried; runtime-specific annotations are not emitted accidentally | Planned; evidence gates open |
| WP-08 | CLI build integration and Studio tooling | Proposed Java contracts: NswagDocument, GenerationCommand, StudioProject | CLI generation needs no desktop runtime; configs reproduce outputs; Studio remains a visible feasibility gate rather than being omitted from scope | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Java contracts are proposals; they are not upstream class declarations. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

NJsonSchema and template-engine dependencies are outside inventory candidates. YAML support cannot be assumed from JDK.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
