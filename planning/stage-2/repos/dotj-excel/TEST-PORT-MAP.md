# DJ-057 .j Excel: test-port map

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [ClosedXML.Tests/OpenXmlTests.cs:12](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML.Tests/OpenXmlTests.cs#L12) | SetPackagePropertiesEntryToNullWithOpenXml | yes |
| [ClosedXML.Tests/ExcelDocsComparerTests.cs:11](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML.Tests/ExcelDocsComparerTests.cs#L11) | CheckEqual | yes |
| [ClosedXML.Tests/ExcelDocsComparerTests.cs:35](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML.Tests/ExcelDocsComparerTests.cs#L35) | CheckNonEqual | yes |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-057-F01-01 | WP-01 | Inserted rows update affected references correctly | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-057-F01-02 | WP-01 | empty and blank cells remain distinct | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-057-F01-03 | WP-01 | invalid addresses fail deterministically | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-057-F02-01 | WP-02 | Style reuse prevents uncontrolled record growth | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-057-F02-02 | WP-02 | 1900/1904 date systems remain explicit | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-057-F02-03 | WP-02 | unsupported formatting round-trips without silent destruction where feasible | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-057-F03-01 | WP-03 | Division errors remain spreadsheet errors | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-057-F03-02 | WP-03 | changed precedents invalidate dependents | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-057-F03-03 | WP-03 | unsupported functions are preserved and reported rather than fabricated | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-057-F04-01 | WP-04 | Saved files open in selected reference applications | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-057-F04-02 | WP-04 | malicious ZIP/XML inputs fail safely | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-057-F04-03 | WP-04 | unsupported parts are not discarded invisibly | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-057-F05-01 | WP-05 | Formula support is enumerated | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-057-F05-02 | WP-05 | dependency rights are checked | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-057-F05-03 | WP-05 | no Apache POI substitute supplies the workbook implementation | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

1900/1904 dates; formula errors; shared strings; styles; merged cells; large sparse sheets; repair warnings in reference viewers.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.
