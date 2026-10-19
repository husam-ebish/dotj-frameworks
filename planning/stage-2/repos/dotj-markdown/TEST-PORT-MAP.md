# DJ-059 .j Markdown: test-port map

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [src/Markdig.Tests/MiscTests.cs:13](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L13) | LinkWithInvalidNonAsciiDomainNameIsIgnored | yes |
| [src/Markdig.Tests/MiscTests.cs:42](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L42) | LinkTextMayContainBalancedBrackets | yes |
| [src/Markdig.Tests/MiscTests.cs:72](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L72) | GuardsAgainstHighlyNestedNodes | yes |
| [src/Markdig.Tests/MiscTests.cs:89](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L89) | MaximumNestingDepthCanBeRaisedForDeepListExtras | yes |
| [src/Markdig.Tests/MiscTests.cs:101](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L101) | MaximumNestingDepthCanBeLowered | yes |
| [src/Markdig.Tests/MiscTests.cs:113](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L113) | IsIssue356Corrected | yes |
| [src/Markdig.Tests/MiscTests.cs:123](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L123) | IsIssue365Corrected | yes |
| [src/Markdig.Tests/MiscTests.cs:133](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L133) | TestAltTextIsCorrectlyEscaped | yes |
| [src/Markdig.Tests/MiscTests.cs:141](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L141) | TestFixHang | yes |
| [src/Markdig.Tests/MiscTests.cs:148](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L148) | TestInvalidHtmlEntity | yes |
| [src/Markdig.Tests/MiscTests.cs:155](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L155) | TestInvalidCharacterHandling | yes |
| [src/Markdig.Tests/MiscTests.cs:162](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L162) | TestInvalidCodeEscape | yes |
| [src/Markdig.Tests/MiscTests.cs:169](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L169) | TestEmphasisAndHtmlEntity | yes |
| [src/Markdig.Tests/MiscTests.cs:176](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L176) | TestThematicInsideCodeBlockInsideList | yes |
| [src/Markdig.Tests/MiscTests.cs:195](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L195) | VisualizeMathExpressions | yes |
| [src/Markdig.Tests/MiscTests.cs:224](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L224) | InlineMathExpression | yes |
| [src/Markdig.Tests/MiscTests.cs:246](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L246) | BlockMathExpression | yes |
| [src/Markdig.Tests/MiscTests.cs:269](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L269) | CanDisableParsingHeadings | yes |
| [src/Markdig.Tests/MiscTests.cs:285](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L285) | CanOpenAutoLinksInNewWindow | yes |
| [src/Markdig.Tests/MiscTests.cs:295](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L295) | CanUseHttpsPrefixForWWWAutoLinks | yes |
| [src/Markdig.Tests/MiscTests.cs:305](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L305) | RootInlineHasCorrectSourceSpan | yes |
| [src/Markdig.Tests/MiscTests.cs:317](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L317) | RootInlineInTableCellHasCorrectSourceSpan | yes |
| [src/Markdig.Tests/MiscTests.cs:330](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L330) | TestGridTableShortLine | yes |
| [src/Markdig.Tests/MiscTests.cs:352](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L352) | TestGridTableLastCellWithoutClosingPipe | yes |
| [src/Markdig.Tests/MiscTests.cs:377](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L377) | TestDefinitionListInListItemWithBlankLine | yes |
| [src/Markdig.Tests/MiscTests.cs:400](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L400) | TestAlertWithinAlertOrNestedBlock | yes |
| [src/Markdig.Tests/MiscTests.cs:427](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L427) | TestNestedAlertInsideBlockquote | yes |
| [src/Markdig.Tests/MiscTests.cs:445](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L445) | TestNestedAlertInsideAlert | yes |
| [src/Markdig.Tests/MiscTests.cs:466](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L466) | TestAlertInsideListItem | yes |
| [src/Markdig.Tests/MiscTests.cs:486](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L486) | TestAlertInsideNestedListItem | yes |
| [src/Markdig.Tests/MiscTests.cs:513](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L513) | TestIssue887ListAfterNestedBlockQuote | yes |
| [src/Markdig.Tests/MiscTests.cs:568](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L568) | TestIssue845ListItemBlankLine | yes |
| [src/Markdig.Tests/MiscTests.cs:597](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L597) | TestEmptyListItemAfterParagraph | yes |
| [src/Markdig.Tests/MiscTests.cs:618](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L618) | TestEmptyListItemWithTrailingWhitespace | yes |
| [src/Markdig.Tests/Program.cs:9](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/Program.cs#L9) | Main | not confirmed |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-059-F01-01 | WP-01 | Spec examples have explicit expected AST/output | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-059-F01-02 | WP-01 | deeply nested input obeys limits | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-059-F01-03 | WP-01 | source spans remain valid after Unicode input | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-059-F02-01 | WP-02 | Conflicting extensions are diagnosed | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-059-F02-02 | WP-02 | disabled extensions do not alter core syntax | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-059-F02-03 | WP-02 | state cannot leak between parses | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-059-F03-01 | WP-03 | Untrusted URLs/HTML follow explicit policy | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-059-F03-02 | WP-03 | generated attributes cannot be injected | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-059-F03-03 | WP-03 | renderer choice does not mutate AST unexpectedly | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-059-F04-01 | WP-04 | Transformations maintain parent/child invariants | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-059-F04-02 | WP-04 | source maps identify synthetic nodes | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-059-F04-03 | WP-04 | unsupported incremental semantics are not claimed | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-059-F05-01 | WP-05 | Runtime does not grow catastrophically on selected adversarial families | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-059-F05-02 | WP-05 | every advertised extension has fixtures | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-059-F05-03 | WP-05 | no flexmark/commonmark-java replacement | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

CommonMark fixtures; emphasis edge cases; tables; source spans; adversarial nesting; raw HTML handling.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.

## Mandatory naming and concept regression cases

| Fixture | Required observation |
|---|---|
| DJ-059-NF01 | Supported public types/members/namespaces match the selected upstream identities with exact spelling and casing; no lowerCamelCase conversion, dropped I prefix, removed Async suffix or replacement domain name is introduced. |
| DJ-059-NF02 | Paired C#/.j examples use the same framework concepts, lifecycle and operation names; every syntax-only difference is documented and internal Java helper types do not become mandatory new public concepts. |
| DJ-059-NF03 | Unrepresentable signatures or semantics are reported as blocked/unsupported with source identity and evidence; no renamed API, JDK substitute type or changed behavior is falsely marked exact compatibility. |

These additional cases enforce the owner naming decision across public signatures, generated APIs and paired examples. They are designed requirements, not executed results.
