# DJ-057 .j Excel: feature compatibility matrix

Preserve date systems, formula semantics and workbook round trips; do not substitute Apache POI or assume Excel computes all cached values.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Workbook worksheet and cell model | Proposed Java contracts: Workbook, Worksheet, CellAddress, CellValue | Inserted rows update affected references correctly; empty and blank cells remain distinct; invalid addresses fail deterministically | Planned; evidence gates open |
| WP-02 | Styles formatting and data features | Proposed Java contracts: CellStyle, NumberFormat, ConditionalFormat, ValidationRule | Style reuse prevents uncontrolled record growth; 1900/1904 date systems remain explicit; unsupported formatting round-trips without silent destruction where feasible | Planned; evidence gates open |
| WP-03 | Formula parsing and calculation | Proposed Java contracts: FormulaNode, DependencyGraph, CalculationResult | Division errors remain spreadsheet errors; changed precedents invalidate dependents; unsupported functions are preserved and reported rather than fabricated | Planned; evidence gates open |
| WP-04 | OpenXML serialization and preservation | Proposed Java contracts: WorkbookReader, WorkbookWriter, PartPreservationPolicy | Saved files open in selected reference applications; malicious ZIP/XML inputs fail safely; unsupported parts are not discarded invisibly | Planned; evidence gates open |
| WP-05 | Interoperability performance and licensing | Proposed Java contracts: WorkbookFixture, FormulaCoverage, CompatibilityProfile | Formula support is enumerated; dependency rights are checked; no Apache POI substitute supplies the workbook implementation | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Java contracts are proposals; they are not upstream class declarations. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Calculation/parser and graphics/font dependencies may sit outside this repo. Chart/macro preservation needs explicit read/write scope.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
