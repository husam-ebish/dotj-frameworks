# DJ-058 .j OpenXML: Java architecture and contracts

Provide typed Office Open XML parts, packaging and validation.

Product type: JVM document/format library. Proposed Java package root: `org.dotj.openxml`. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are design proposals, not already implemented APIs.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-openxml-01 | OpcPackage, PackagePart, Relationship, ContentType | OPC package and relationships |
| dotj-openxml-02 | OpenXmlElement, SchemaType, GeneratorManifest | Schemas typed elements and generation |
| dotj-openxml-03 | WordprocessingDocument, SpreadsheetDocument, PresentationDocument | Document families and feature coverage |
| dotj-openxml-04 | ValidationError, MarkupCompatibility, ElementVisitor | Validation markup compatibility and traversal |
| dotj-openxml-05 | PackageFixture, FormatProfile, PreservationReport | Interoperability security and acceptance |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Async methods return CompletionStage; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

.NET packaging APIs become owned OPC abstractions; preserve namespaces and unknown parts without unsafe XML resolution.

## Feature contracts and invariants

### WP-01: OPC package and relationships

Contract vocabulary: `OpcPackage`, `PackagePart`, `Relationship`, `ContentType`.

Define ZIP part naming URI validation and relationship rules. Separate core System.IO.Packaging behavior from product model. Support read-only/edit/save lifecycle with ownership contracts.

Required observable invariant: Traversal and duplicate-part attacks fail; relationships resolve predictably; caller-owned streams remain open according to options.

### WP-02: Schemas typed elements and generation

Contract vocabulary: `OpenXmlElement`, `SchemaType`, `GeneratorManifest`.

Inventory schema/version data and generated source ownership. Generate Java typed models deterministically. Preserve qualified names attributes child order and unknown elements.

Required observable invariant: Generated models compile; unknown extensions survive supported round trips; schema licensing/provenance accompanies generation inputs.

### WP-03: Document families and feature coverage

Contract vocabulary: `WordprocessingDocument`, `SpreadsheetDocument`, `PresentationDocument`.

Map Word Excel PowerPoint and supporting part families. Define strongly typed versus raw XML escape hatches. Track format-version and application-specific extensions.

Required observable invariant: Every part family has a coverage state; unsupported extensions remain readable/preservable where declared; model support is not equated with rendering.

### WP-04: Validation markup compatibility and traversal

Contract vocabulary: `ValidationError`, `MarkupCompatibility`, `ElementVisitor`.

Implement schema/semantic validation with locations. Apply compatibility choices under explicit target version. Define mutation traversal and streaming APIs.

Required observable invariant: Validation reports part/path details; alternate-content handling follows profile; large documents can be processed without full DOM where supported.

### WP-05: Interoperability security and acceptance

Contract vocabulary: `PackageFixture`, `FormatProfile`, `PreservationReport`.

Port package/schema/validation regressions. Test round trips in declared reference applications. Exercise ZIP bombs entity expansion malformed relationships and corrupt parts.

Required observable invariant: Security limits prevent resource exhaustion; preservation losses are reported; no Java office library replaces owned implementation.

## Bootstrap and dependency boundaries

ZIP, XML streaming, URI and JDK signatures where sufficient.

Proposed .j dependencies: core. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing Open XML SDK usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then express the same intent with `OpcPackage` and its companion contracts. Preserve semantic differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Traversal and duplicate-part attacks fail; relationships resolve predictably; caller-owned streams remain open according to options. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
