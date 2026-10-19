# DJ-057 .j Excel: module and API inventory

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

| Observed item | Count | Interpretation |
|---|---|---|
| Listed blob paths | 1504 | recursive complete |
| Project-definition paths | 6 | Files, not restored packages |
| API-definition/ref paths | 0 | Candidate declarations, not a complete public API census |
| Test/fixture candidate paths | 193 | Lexical path classification, not runnable test count |
| Sampled text files | 11 | Metadata plus selected API/implementation/tests |
| Lexical public/protected declarations | 28 | May include test helpers; not semantic API count |
| Lexical test-method candidates | 3 | Attribute inference only; no test discovery or execution |

## Extraction method and remaining closure

The tree supplies path identity. Project suffixes identify structural module candidates. Public/protected lines and test-like methods are extracted lexically from sampled files; multiline declarations, conditional compilation, generated code, extension methods, overload relationships and fixture parameter expansion require compiler-aware extraction. E02 must evaluate every target framework/configuration, generated source and conditional reference. Unassigned members remain retained scope, never implicitly removed.

## Observed project/module ledger

| Pinned path | Role candidate | Disposition |
|---|---|---|
| [ClosedXML.Examples/ClosedXML.Examples.csproj](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML.Examples/ClosedXML.Examples.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [ClosedXML.IO.CodeGen/ClosedXML.IO.CodeGen.csproj](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML.IO.CodeGen/ClosedXML.IO.CodeGen.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [ClosedXML.IO/ClosedXML.IO.csproj](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML.IO/ClosedXML.IO.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [ClosedXML.Sandbox/ClosedXML.Sandbox.csproj](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML.Sandbox/ClosedXML.Sandbox.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [ClosedXML.Tests/ClosedXML.Tests.csproj](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML.Tests/ClosedXML.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [ClosedXML/ClosedXML.csproj](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML/ClosedXML.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |

## Sampled declaration candidates

| Source | Declaration candidate |
|---|---|
| [ClosedXML/XLHelper.cs:13](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML/XLHelper.cs#L13) | `public static partial class XLHelper` |
| [ClosedXML/XLHelper.cs:15](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML/XLHelper.cs#L15) | `public const int MinRowNumber = 1;` |
| [ClosedXML/XLHelper.cs:16](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML/XLHelper.cs#L16) | `public const int MinColumnNumber = 1;` |
| [ClosedXML/XLHelper.cs:17](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML/XLHelper.cs#L17) | `public const int MaxRowNumber = 1048576;` |
| [ClosedXML/XLHelper.cs:18](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML/XLHelper.cs#L18) | `public const int MaxColumnNumber = 16384;` |
| [ClosedXML/XLHelper.cs:19](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML/XLHelper.cs#L19) | `public const String MaxColumnLetter = "XFD";` |
| [ClosedXML/XLHelper.cs:21](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML/XLHelper.cs#L21) | `public const Double Epsilon = 1e-10;` |
| [ClosedXML/XLHelper.cs:40](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML/XLHelper.cs#L40) | `public static Encoding NoBomUTF8 = new UTF8Encoding(false);` |
| [ClosedXML/XLHelper.cs:42](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML/XLHelper.cs#L42) | `public static String LastCell { get { return $"{MaxColumnLetter}{MaxRowNumber}"; } }` |
| [ClosedXML/XLHelper.cs:121](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML/XLHelper.cs#L121) | `public static int GetColumnNumberFromLetter(string columnLetter)` |
| [ClosedXML/XLHelper.cs:142](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML/XLHelper.cs#L142) | `public static string GetColumnLetterFromNumber(int columnNumber, bool trimToAllowed = false)` |
| [ClosedXML/XLHelper.cs:163](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML/XLHelper.cs#L163) | `public static bool IsValidColumn(string column)` |
| [ClosedXML/XLHelper.cs:194](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML/XLHelper.cs#L194) | `public static bool IsValidRow(string rowString)` |
| [ClosedXML/XLHelper.cs:201](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML/XLHelper.cs#L201) | `public static bool IsValidA1Address(string address)` |
| [ClosedXML/XLHelper.cs:218](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML/XLHelper.cs#L218) | `public static bool IsValidRCAddress(string address)` |
| [ClosedXML/XLHelper.cs:226](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML/XLHelper.cs#L226) | `public static Boolean IsValidRangeAddress(String rangeAddress)` |
| [ClosedXML/XLHelper.cs:234](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML/XLHelper.cs#L234) | `public static Boolean IsValidRangeAddress(IXLRangeAddress rangeAddress)` |
| [ClosedXML/XLHelper.cs:243](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML/XLHelper.cs#L243) | `public static int GetColumnNumberFromAddress(string cellAddressString)` |
| [ClosedXML/XLHelper.cs:310](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML/XLHelper.cs#L310) | `public static Boolean AreEqual(Double d1, Double d2)` |
| [ClosedXML/XLHelper.cs:315](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML/XLHelper.cs#L315) | `public static DateTime GetDate(Object v)` |
| [ClosedXML/XLHelper_ASF.cs:25](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML/XLHelper_ASF.cs#L25) | `public static partial class XLHelper` |
| [ClosedXML/XLHelper_ASF.cs:43](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML/XLHelper_ASF.cs#L43) | `public static string CreateSafeSheetName(string nameProposal, char replaceChar = ' ')` |
| [ClosedXML/XLHelper_ASF.cs:91](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML/XLHelper_ASF.cs#L91) | `public static void ValidateSheetName(String sheetName)` |
| [ClosedXML.Tests/OpenXmlTests.cs:8](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML.Tests/OpenXmlTests.cs#L8) | `public class OpenXmlTests` |
| [ClosedXML.Tests/OpenXmlTests.cs:12](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML.Tests/OpenXmlTests.cs#L12) | `public static void SetPackagePropertiesEntryToNullWithOpenXml()` |
| [ClosedXML.Tests/ExcelDocsComparerTests.cs:8](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML.Tests/ExcelDocsComparerTests.cs#L8) | `public class ExcelDocsComparerTests` |
| [ClosedXML.Tests/ExcelDocsComparerTests.cs:11](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML.Tests/ExcelDocsComparerTests.cs#L11) | `public void CheckEqual()` |
| [ClosedXML.Tests/ExcelDocsComparerTests.cs:35](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML.Tests/ExcelDocsComparerTests.cs#L35) | `public void CheckNonEqual()` |

Full lexical records (28) and complete listed paths are in [inventory.json](evidence/inventory.json). A display limit does not remove omitted records from scope.

## Capability ownership

| Package | Retained capability | Internal planning labels; public names come from source |
|---|---|---|
| WP-01 | Workbook worksheet and cell model | Workbook; Worksheet; CellAddress; CellValue |
| WP-02 | Styles formatting and data features | CellStyle; NumberFormat; ConditionalFormat; ValidationRule |
| WP-03 | Formula parsing and calculation | FormulaNode; DependencyGraph; CalculationResult |
| WP-04 | OpenXML serialization and preservation | WorkbookReader; WorkbookWriter; PartPreservationPolicy |
| WP-05 | Interoperability performance and licensing | WorkbookFixture; FormulaCoverage; CompatibilityProfile |


Map every observed source module/member onto one of these packages or a new explicitly retained package during E02. Structural listing is complete only to the scope stated above; behavioral analysis is sampled.
