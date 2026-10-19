# DJ-058 .j OpenXML: feature compatibility matrix

.NET packaging APIs become owned OPC abstractions; preserve namespaces and unknown parts without unsafe XML resolution.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | OPC package and relationships | Proposed Java contracts: OpcPackage, PackagePart, Relationship, ContentType | Traversal and duplicate-part attacks fail; relationships resolve predictably; caller-owned streams remain open according to options | Planned; evidence gates open |
| WP-02 | Schemas typed elements and generation | Proposed Java contracts: OpenXmlElement, SchemaType, GeneratorManifest | Generated models compile; unknown extensions survive supported round trips; schema licensing/provenance accompanies generation inputs | Planned; evidence gates open |
| WP-03 | Document families and feature coverage | Proposed Java contracts: WordprocessingDocument, SpreadsheetDocument, PresentationDocument | Every part family has a coverage state; unsupported extensions remain readable/preservable where declared; model support is not equated with rendering | Planned; evidence gates open |
| WP-04 | Validation markup compatibility and traversal | Proposed Java contracts: ValidationError, MarkupCompatibility, ElementVisitor | Validation reports part/path details; alternate-content handling follows profile; large documents can be processed without full DOM where supported | Planned; evidence gates open |
| WP-05 | Interoperability security and acceptance | Proposed Java contracts: PackageFixture, FormatProfile, PreservationReport | Security limits prevent resource exhaustion; preservation losses are reported; no Java office library replaces owned implementation | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Java contracts are proposals; they are not upstream class declarations. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Generated schemas and System.IO.Packaging dependencies require provenance; Strict/Transitional and Office extensions must be versioned.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
