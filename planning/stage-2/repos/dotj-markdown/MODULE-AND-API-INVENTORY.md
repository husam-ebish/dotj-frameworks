# DJ-059 .j Markdown: module and API inventory

| Observed item | Count | Interpretation |
|---|---|---|
| Listed blob paths | 615 | recursive complete |
| Project-definition paths | 10 | Files, not restored packages |
| API-definition/ref paths | 0 | Candidate declarations, not a complete public API census |
| Test/fixture candidate paths | 116 | Lexical path classification, not runnable test count |
| Sampled text files | 8 | Metadata plus selected API/implementation/tests |
| Lexical public/protected declarations | 49 | May include test helpers; not semantic API count |
| Lexical test-method candidates | 35 | Attribute inference only; no test discovery or execution |

## Extraction method and remaining closure

The tree supplies path identity. Project suffixes identify structural module candidates. Public/protected lines and test-like methods are extracted lexically from sampled files; multiline declarations, conditional compilation, generated code, extension methods, overload relationships and fixture parameter expansion require compiler-aware extraction. E02 must evaluate every target framework/configuration, generated source and conditional reference. Unassigned members remain retained scope, never implicitly removed.

## Observed project/module ledger

| Pinned path | Role candidate | Disposition |
|---|---|---|
| [src/Markdig.Benchmarks/Markdig.Benchmarks.csproj](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Benchmarks/Markdig.Benchmarks.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [src/Markdig.Fuzzing/Markdig.Fuzzing.csproj](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Fuzzing/Markdig.Fuzzing.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/Markdig.Signed/Markdig.Signed.csproj](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Signed/Markdig.Signed.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/Markdig.Tests/Markdig.Tests.csproj](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/Markdig.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/Markdig.WebApp/Markdig.WebApp.csproj](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.WebApp/Markdig.WebApp.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/Markdig/Markdig.csproj](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig/Markdig.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/SpecFileGen/SpecFileGen.csproj](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/SpecFileGen/SpecFileGen.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/UnicodeNormDApp/UnicodeNormDApp.csproj](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/UnicodeNormDApp/UnicodeNormDApp.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/mdtoc/mdtoc.csproj](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/mdtoc/mdtoc.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [tools/GfmTableDifferential/GfmTableDifferential.csproj](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/tools/GfmTableDifferential/GfmTableDifferential.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |

## Sampled declaration candidates

| Source | Declaration candidate |
|---|---|
| [src/Markdig/Markdown.cs:20](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig/Markdown.cs#L20) | `public static class Markdown` |
| [src/Markdig/Markdown.cs:26](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig/Markdown.cs#L26) | `public static string Version => field ??= typeof(Markdown).Assembly.GetCustomAttribute<AssemblyFileVersionAttribute>()?.Version ?? "Unknown";` |
| [src/Markdig/Markdown.cs:57](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig/Markdown.cs#L57) | `public static string Normalize([StringSyntax("Markdown")] string markdown, NormalizeOptions? options = null, MarkdownPipeline? pipeline = null, MarkdownParserContext? context = null)` |
| [src/Markdig/Markdown.cs:73](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig/Markdown.cs#L73) | `public static MarkdownDocument Normalize([StringSyntax("Markdown")] string markdown, TextWriter writer, NormalizeOptions? options = null, MarkdownPipeline? pipeline = null, MarkdownParserContext? context = null)` |
| [src/Markdig/Markdown.cs:98](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig/Markdown.cs#L98) | `public static string ToHtml([StringSyntax("Markdown")] string markdown, MarkdownPipeline? pipeline = null, MarkdownParserContext? context = null)` |
| [src/Markdig/Markdown.cs:116](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig/Markdown.cs#L116) | `public static string ToHtml(this MarkdownDocument document, MarkdownPipeline? pipeline = null)` |
| [src/Markdig/Markdown.cs:139](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig/Markdown.cs#L139) | `public static void ToHtml(this MarkdownDocument document, TextWriter writer, MarkdownPipeline? pipeline = null)` |
| [src/Markdig/Markdown.cs:162](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig/Markdown.cs#L162) | `public static MarkdownDocument ToHtml([StringSyntax("Markdown")] string markdown, TextWriter writer, MarkdownPipeline? pipeline = null, MarkdownParserContext? context = null)` |
| [src/Markdig/Markdown.cs:184](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig/Markdown.cs#L184) | `public static object Convert([StringSyntax("Markdown")] string markdown, IMarkdownRenderer renderer, MarkdownPipeline? pipeline = null, MarkdownParserContext? context = null)` |
| [src/Markdig/Markdown.cs:204](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig/Markdown.cs#L204) | `public static MarkdownDocument Parse([StringSyntax("Markdown")] string markdown, bool trackTrivia = false)` |
| [src/Markdig/Markdown.cs:221](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig/Markdown.cs#L221) | `public static MarkdownDocument Parse([StringSyntax("Markdown")] string markdown, MarkdownPipeline? pipeline, MarkdownParserContext? context = null)` |
| [src/Markdig/Markdown.cs:239](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig/Markdown.cs#L239) | `public static MarkdownDocument ToPlainText([StringSyntax("Markdown")] string markdown, TextWriter writer, MarkdownPipeline? pipeline = null, MarkdownParserContext? context = null)` |
| [src/Markdig/Markdown.cs:271](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig/Markdown.cs#L271) | `public static string ToPlainText([StringSyntax("Markdown")] string markdown, MarkdownPipeline? pipeline = null, MarkdownParserContext? context = null)` |
| [src/Markdig.Tests/MiscTests.cs:10](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L10) | `public class MiscTests` |
| [src/Markdig.Tests/MiscTests.cs:13](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L13) | `public void LinkWithInvalidNonAsciiDomainNameIsIgnored()` |
| [src/Markdig.Tests/MiscTests.cs:42](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L42) | `public void LinkTextMayContainBalancedBrackets(string linkText)` |
| [src/Markdig.Tests/MiscTests.cs:72](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L72) | `public void GuardsAgainstHighlyNestedNodes(char c, int count, bool parseOnly, bool shouldThrow)` |
| [src/Markdig.Tests/MiscTests.cs:89](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L89) | `public void MaximumNestingDepthCanBeRaisedForDeepListExtras()` |
| [src/Markdig.Tests/MiscTests.cs:101](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L101) | `public void MaximumNestingDepthCanBeLowered()` |
| [src/Markdig.Tests/MiscTests.cs:113](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L113) | `public void IsIssue356Corrected()` |
| [src/Markdig.Tests/MiscTests.cs:123](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L123) | `public void IsIssue365Corrected()` |
| [src/Markdig.Tests/MiscTests.cs:133](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L133) | `public void TestAltTextIsCorrectlyEscaped()` |
| [src/Markdig.Tests/MiscTests.cs:141](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L141) | `public void TestFixHang()` |
| [src/Markdig.Tests/MiscTests.cs:148](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L148) | `public void TestInvalidHtmlEntity()` |
| [src/Markdig.Tests/MiscTests.cs:155](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L155) | `public void TestInvalidCharacterHandling()` |
| [src/Markdig.Tests/MiscTests.cs:162](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L162) | `public void TestInvalidCodeEscape()` |
| [src/Markdig.Tests/MiscTests.cs:169](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L169) | `public void TestEmphasisAndHtmlEntity()` |
| [src/Markdig.Tests/MiscTests.cs:176](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L176) | `public void TestThematicInsideCodeBlockInsideList()` |
| [src/Markdig.Tests/MiscTests.cs:195](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L195) | `public void VisualizeMathExpressions()` |
| [src/Markdig.Tests/MiscTests.cs:224](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L224) | `public void InlineMathExpression()` |
| [src/Markdig.Tests/MiscTests.cs:246](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L246) | `public void BlockMathExpression()` |
| [src/Markdig.Tests/MiscTests.cs:269](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L269) | `public void CanDisableParsingHeadings()` |
| [src/Markdig.Tests/MiscTests.cs:285](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L285) | `public void CanOpenAutoLinksInNewWindow()` |
| [src/Markdig.Tests/MiscTests.cs:295](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L295) | `public void CanUseHttpsPrefixForWWWAutoLinks()` |
| [src/Markdig.Tests/MiscTests.cs:305](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L305) | `public void RootInlineHasCorrectSourceSpan()` |
| [src/Markdig.Tests/MiscTests.cs:317](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L317) | `public void RootInlineInTableCellHasCorrectSourceSpan()` |
| [src/Markdig.Tests/MiscTests.cs:330](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L330) | `public void TestGridTableShortLine()` |
| [src/Markdig.Tests/MiscTests.cs:352](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L352) | `public void TestGridTableLastCellWithoutClosingPipe(string lineEnding)` |
| [src/Markdig.Tests/MiscTests.cs:377](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L377) | `public void TestDefinitionListInListItemWithBlankLine()` |
| [src/Markdig.Tests/MiscTests.cs:400](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L400) | `public void TestAlertWithinAlertOrNestedBlock()` |
| [src/Markdig.Tests/MiscTests.cs:427](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L427) | `public void TestNestedAlertInsideBlockquote()` |
| [src/Markdig.Tests/MiscTests.cs:445](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L445) | `public void TestNestedAlertInsideAlert()` |
| [src/Markdig.Tests/MiscTests.cs:466](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L466) | `public void TestAlertInsideListItem()` |
| [src/Markdig.Tests/MiscTests.cs:486](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L486) | `public void TestAlertInsideNestedListItem()` |
| [src/Markdig.Tests/MiscTests.cs:513](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L513) | `public void TestIssue887ListAfterNestedBlockQuote()` |
| [src/Markdig.Tests/MiscTests.cs:568](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L568) | `public void TestIssue845ListItemBlankLine()` |
| [src/Markdig.Tests/MiscTests.cs:597](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L597) | `public void TestEmptyListItemAfterParagraph(string markdown, string expected)` |
| [src/Markdig.Tests/MiscTests.cs:618](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/MiscTests.cs#L618) | `public void TestEmptyListItemWithTrailingWhitespace(string markdown, string expected)` |
| [src/Markdig.Tests/Program.cs:9](https://github.com/xoofx/markdig/blob/ccb9d8593f7a0aac232342a6705e8afc8c4f374d/src/Markdig.Tests/Program.cs#L9) | `public static void Main(string[] args)` |

Full lexical records (49) and complete listed paths are in [inventory.json](evidence/inventory.json). A display limit does not remove omitted records from scope.

## Capability ownership

| Package | Retained capability | Proposed contract names |
|---|---|---|
| WP-01 | Parsing blocks and inline syntax | MarkdownDocument; BlockParser; InlineParser |
| WP-02 | Extension pipeline and syntax families | MarkdownExtension; Pipeline; ExtensionOrder |
| WP-03 | HTML and alternative renderers | Renderer; HtmlPolicy; OutputContext |
| WP-04 | Editing utilities and transformations | SourceMap; SyntaxVisitor; DocumentTransform |
| WP-05 | Specification regression and performance | MarkdownCase; ExtensionCase; ParseLimit |


Map every observed source module/member onto one of these packages or a new explicitly retained package during E02. Structural listing is complete only to the scope stated above; behavioral analysis is sampled.
