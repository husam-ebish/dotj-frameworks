# DJ-057 .j Excel: feature compatibility matrix

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

Preserve date systems, formula semantics and workbook round trips; do not substitute Apache POI or assume Excel computes all cached values.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Workbook worksheet and cell model | Internal planning vocabulary (verify upstream public identity): Workbook, Worksheet, CellAddress, CellValue | Inserted rows update affected references correctly; empty and blank cells remain distinct; invalid addresses fail deterministically | Planned; evidence gates open |
| WP-02 | Styles formatting and data features | Internal planning vocabulary (verify upstream public identity): CellStyle, NumberFormat, ConditionalFormat, ValidationRule | Style reuse prevents uncontrolled record growth; 1900/1904 date systems remain explicit; unsupported formatting round-trips without silent destruction where feasible | Planned; evidence gates open |
| WP-03 | Formula parsing and calculation | Internal planning vocabulary (verify upstream public identity): FormulaNode, DependencyGraph, CalculationResult | Division errors remain spreadsheet errors; changed precedents invalidate dependents; unsupported functions are preserved and reported rather than fabricated | Planned; evidence gates open |
| WP-04 | OpenXML serialization and preservation | Internal planning vocabulary (verify upstream public identity): WorkbookReader, WorkbookWriter, PartPreservationPolicy | Saved files open in selected reference applications; malicious ZIP/XML inputs fail safely; unsupported parts are not discarded invisibly | Planned; evidence gates open |
| WP-05 | Interoperability performance and licensing | Internal planning vocabulary (verify upstream public identity): WorkbookFixture, FormulaCoverage, CompatibilityProfile | Formula support is enumerated; dependency rights are checked; no Apache POI substitute supplies the workbook implementation | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Internal design labels are not public API replacements. Public contracts must preserve exact upstream names, casing and concepts under N01; the semantic mapping remains open. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Calculation/parser and graphics/font dependencies may sit outside this repo. Chart/macro preservation needs explicit read/write scope.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
