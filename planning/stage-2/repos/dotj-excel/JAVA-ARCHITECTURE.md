# DJ-057 .j Excel: Java architecture and contracts

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Read/write and manipulate spreadsheets with formulas, styles and tables.

Product type: JVM document library. Public package names preserve the exact source namespace identity and casing, subject to explicit JVM/JPMS feasibility. `org.dotj.internal.*` is reserved for hidden implementation helpers. JPMS exports are limited to contracts; adapters and generated/internal implementations are separate modules. Names below are internal design/workstream vocabulary unless verified against the source. They are not authority to rename public APIs. N01 defines the exact source-derived public surface.

## Module responsibilities

| Proposed module | Contracts | Responsibility |
|---|---|---|
| dotj-excel-01 | Workbook, Worksheet, CellAddress, CellValue | Workbook worksheet and cell model |
| dotj-excel-02 | CellStyle, NumberFormat, ConditionalFormat, ValidationRule | Styles formatting and data features |
| dotj-excel-03 | FormulaNode, DependencyGraph, CalculationResult | Formula parsing and calculation |
| dotj-excel-04 | WorkbookReader, WorkbookWriter, PartPreservationPolicy | OpenXML serialization and preservation |
| dotj-excel-05 | WorkbookFixture, FormulaCoverage, CompatibilityProfile | Interoperability performance and licensing |

## Data, ownership, threading and errors

Use explicit immutable request/settings snapshots and typed result values where absence differs from null. Public async signatures retain the original Task/ValueTask type names and semantics; CompletionStage is permitted behind the compatibility facade or in optional Java interop, not as a silent replacement; streaming methods expose a demand-aware contract or explicitly state push-only semantics. Cancellation is a separate token and is not equivalent to cancelling a Java future. Caller-owned objects remain caller-owned; created resources close in reverse dependency order with aggregated cleanup failures. Capture context explicitly before scheduling work. Use monotonic time for durations and explicit zone/culture for civil values. Errors retain stable category/code, contextual path and original cause; public protocol responses and logs redact secrets. Native/UI callbacks have a declared owner thread and cannot outlive their handle/session.

Preserve date systems, formula semantics and workbook round trips; do not substitute Apache POI or assume Excel computes all cached values.

## Feature contracts and invariants

### WP-01: Workbook worksheet and cell model

Internal analysis vocabulary (not permission to rename the public API): `Workbook`, `Worksheet`, `CellAddress`, `CellValue`.

Define typed values shared formulas names tables and ranges. Specify row/column insertion and reference adjustment. Preserve workbook ownership and lazy loading limits.

Required observable invariant: Inserted rows update affected references correctly; empty and blank cells remain distinct; invalid addresses fail deterministically.

### WP-02: Styles formatting and data features

Internal analysis vocabulary (not permission to rename the public API): `CellStyle`, `NumberFormat`, `ConditionalFormat`, `ValidationRule`.

Deduplicate immutable style records. Implement number/date formatting with explicit locale/epoch rules. Map filters tables comments hyperlinks and validation features.

Required observable invariant: Style reuse prevents uncontrolled record growth; 1900/1904 date systems remain explicit; unsupported formatting round-trips without silent destruction where feasible.

### WP-03: Formula parsing and calculation

Internal analysis vocabulary (not permission to rename the public API): `FormulaNode`, `DependencyGraph`, `CalculationResult`.

Parse formulas and resolve ranges/names. Evaluate supported functions with spreadsheet coercion/error rules. Detect cycles and maintain recalculation dependencies.

Required observable invariant: Division errors remain spreadsheet errors; changed precedents invalidate dependents; unsupported functions are preserved and reported rather than fabricated.

### WP-04: OpenXML serialization and preservation

Internal analysis vocabulary (not permission to rename the public API): `WorkbookReader`, `WorkbookWriter`, `PartPreservationPolicy`.

Use owned openxml packaging/model contracts. Preserve unknown parts and relationships under an explicit policy. Bound archive sizes shared strings and XML nesting.

Required observable invariant: Saved files open in selected reference applications; malicious ZIP/XML inputs fail safely; unsupported parts are not discarded invisibly.

### WP-05: Interoperability performance and licensing

Internal analysis vocabulary (not permission to rename the public API): `WorkbookFixture`, `FormulaCoverage`, `CompatibilityProfile`.

Inventory ClosedXML dependencies such as parser/calculation libraries separately. Port worksheet/style/formula/regression fixtures. Measure large workbook memory and streaming limits.

Required observable invariant: Formula support is enumerated; dependency rights are checked; no Apache POI substitute supplies the workbook implementation.

## Bootstrap and dependency boundaries

Owned OpenXML package layer, ZIP/XML and numeric/date APIs.

Proposed .j dependencies: openxml,core. Optional adapters depend inward on contracts; product implementations do not become core dependencies. The first deliverable is a versioned contract and fixture set for WP-01. Later native/UI/cloud adapters activate only after their feasibility and rights gates pass.

## Migration walkthrough

Take one existing ClosedXML usage scenario in the first capability family, record its input/settings/expected failure and cleanup behavior against the pinned oracle, then preserve the original public API names and workflow; the internal analysis label `Workbook` is not a replacement public API. Document unavoidable syntax/representation differences documented in the feature matrix rather than translating C# syntax mechanically. The initial acceptance scenario is: Inserted rows update affected references correctly; empty and blank cells remain distinct; invalid addresses fail deterministically. For each public example, provide input, Java API usage once finalized, expected observable output, required artifacts and documented deviations. Examples are planned outputs; no uncompiled Java snippet is represented as working code.
