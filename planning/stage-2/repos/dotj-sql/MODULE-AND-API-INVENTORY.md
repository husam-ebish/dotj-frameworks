# DJ-020 .j SQL: module and API inventory

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

| Observed item | Count | Interpretation |
|---|---|---|
| Listed blob paths | 230 | recursive complete |
| Project-definition paths | 11 | Files, not restored packages |
| API-definition/ref paths | 14 | Candidate declarations, not a complete public API census |
| Test/fixture candidate paths | 96 | Lexical path classification, not runnable test count |
| Sampled text files | 15 | Metadata plus selected API/implementation/tests |
| Lexical public/protected declarations | 32 | May include test helpers; not semantic API count |
| Lexical test-method candidates | 8 | Attribute inference only; no test discovery or execution |

## Extraction method and remaining closure

The tree supplies path identity. Project suffixes identify structural module candidates. Public/protected lines and test-like methods are extracted lexically from sampled files; multiline declarations, conditional compilation, generated code, extension methods, overload relationships and fixture parameter expansion require compiler-aware extraction. E02 must evaluate every target framework/configuration, generated source and conditional reference. Unassigned members remain retained scope, never implicitly removed.

## Observed project/module ledger

| Pinned path | Role candidate | Disposition |
|---|---|---|
| [Build.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Build.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [Dapper.EntityFramework.StrongName/Dapper.EntityFramework.StrongName.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Dapper.EntityFramework.StrongName/Dapper.EntityFramework.StrongName.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [Dapper.EntityFramework/Dapper.EntityFramework.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Dapper.EntityFramework/Dapper.EntityFramework.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [Dapper.ProviderTools/Dapper.ProviderTools.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Dapper.ProviderTools/Dapper.ProviderTools.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [Dapper.Rainbow/Dapper.Rainbow.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Dapper.Rainbow/Dapper.Rainbow.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [Dapper.SqlBuilder/Dapper.SqlBuilder.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Dapper.SqlBuilder/Dapper.SqlBuilder.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [Dapper.StrongName/Dapper.StrongName.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Dapper.StrongName/Dapper.StrongName.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [Dapper/Dapper.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Dapper/Dapper.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/benchmarks/Dapper.Tests.Performance/Dapper.Tests.Performance.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [docs/docs.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/docs/docs.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [tests/Dapper.Tests/Dapper.Tests.csproj](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/tests/Dapper.Tests/Dapper.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |

## Sampled declaration candidates

| Source | Declaration candidate |
|---|---|
| [Dapper/NRT.cs:7](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Dapper/NRT.cs#L7) | `public UnconditionalSuppressMessageAttribute(string category, string checkId) { }` |
| [Dapper/NRT.cs:9](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Dapper/NRT.cs#L9) | `public string? Justification { get; set; }` |
| [Dapper/NRT.cs:15](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Dapper/NRT.cs#L15) | `public NotNullWhenAttribute(bool returnValue) => ReturnValue = returnValue;` |
| [Dapper/NRT.cs:17](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/Dapper/NRT.cs#L17) | `public bool ReturnValue { get; }` |
| [tests/Dapper.Tests/XmlTests.cs:8](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/tests/Dapper.Tests/XmlTests.cs#L8) | `public sealed class SystemSqlClientXmlTests : XmlTests<SystemSqlClientProvider> { }` |
| [tests/Dapper.Tests/XmlTests.cs:11](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/tests/Dapper.Tests/XmlTests.cs#L11) | `public sealed class MicrosoftSqlClientXmlTests : XmlTests<MicrosoftSqlClientProvider> { }` |
| [tests/Dapper.Tests/XmlTests.cs:13](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/tests/Dapper.Tests/XmlTests.cs#L13) | `public abstract class XmlTests<TProvider> : TestBase<TProvider> where TProvider : DatabaseProvider` |
| [tests/Dapper.Tests/XmlTests.cs:16](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/tests/Dapper.Tests/XmlTests.cs#L16) | `public void CommonXmlTypesSupported()` |
| [tests/Dapper.Tests/XmlTests.cs:33](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/tests/Dapper.Tests/XmlTests.cs#L33) | `public class Foo` |
| [tests/Dapper.Tests/XmlTests.cs:35](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/tests/Dapper.Tests/XmlTests.cs#L35) | `public XmlDocument? A { get; set; }` |
| [tests/Dapper.Tests/XmlTests.cs:36](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/tests/Dapper.Tests/XmlTests.cs#L36) | `public XDocument? B { get; set; }` |
| [tests/Dapper.Tests/XmlTests.cs:37](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/tests/Dapper.Tests/XmlTests.cs#L37) | `public XElement? C { get; set; }` |
| [tests/Dapper.Tests/EnumTests.cs:8](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/tests/Dapper.Tests/EnumTests.cs#L8) | `public sealed class SystemSqlClientEnumTests : EnumTests<SystemSqlClientProvider> { }` |
| [tests/Dapper.Tests/EnumTests.cs:11](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/tests/Dapper.Tests/EnumTests.cs#L11) | `public sealed class MicrosoftSqlClientEnumTests : EnumTests<MicrosoftSqlClientProvider> { }` |
| [tests/Dapper.Tests/EnumTests.cs:13](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/tests/Dapper.Tests/EnumTests.cs#L13) | `public abstract class EnumTests<TProvider> : TestBase<TProvider> where TProvider : DatabaseProvider` |
| [tests/Dapper.Tests/EnumTests.cs:16](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/tests/Dapper.Tests/EnumTests.cs#L16) | `public void TestEnumWeirdness()` |
| [tests/Dapper.Tests/EnumTests.cs:23](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/tests/Dapper.Tests/EnumTests.cs#L23) | `public void TestEnumStrings()` |
| [tests/Dapper.Tests/EnumTests.cs:33](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/tests/Dapper.Tests/EnumTests.cs#L33) | `public void TestEnumParamsWithNullable()` |
| [tests/Dapper.Tests/EnumTests.cs:45](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/tests/Dapper.Tests/EnumTests.cs#L45) | `public void TestEnumParamsWithoutNullable()` |
| [tests/Dapper.Tests/EnumTests.cs:65](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/tests/Dapper.Tests/EnumTests.cs#L65) | `public EnumParam A { get; set; }` |
| [tests/Dapper.Tests/EnumTests.cs:66](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/tests/Dapper.Tests/EnumTests.cs#L66) | `public EnumParam? B { get; set; }` |
| [tests/Dapper.Tests/EnumTests.cs:67](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/tests/Dapper.Tests/EnumTests.cs#L67) | `public EnumParam? C { get; set; }` |
| [tests/Dapper.Tests/EnumTests.cs:72](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/tests/Dapper.Tests/EnumTests.cs#L72) | `public EnumParam A { get; set; }` |
| [tests/Dapper.Tests/EnumTests.cs:73](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/tests/Dapper.Tests/EnumTests.cs#L73) | `public EnumParam? B { get; set; }` |
| [tests/Dapper.Tests/EnumTests.cs:74](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/tests/Dapper.Tests/EnumTests.cs#L74) | `public EnumParam? C { get; set; }` |
| [tests/Dapper.Tests/EnumTests.cs:84](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/tests/Dapper.Tests/EnumTests.cs#L84) | `public TestEnum? EnumEnum { get; set; }` |
| [tests/Dapper.Tests/EnumTests.cs:89](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/tests/Dapper.Tests/EnumTests.cs#L89) | `public TestEnum EnumEnum { get; set; }` |
| [tests/Dapper.Tests/EnumTests.cs:93](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/tests/Dapper.Tests/EnumTests.cs#L93) | `public void AdoNetEnumValue()` |
| [tests/Dapper.Tests/EnumTests.cs:109](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/tests/Dapper.Tests/EnumTests.cs#L109) | `public void DapperEnumValue_SqlServer() => Common.DapperEnumValue(connection);` |
| [tests/Dapper.Tests/EnumTests.cs:119](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/tests/Dapper.Tests/EnumTests.cs#L119) | `public SO27024806Class(SO27024806Enum myField)` |
| [tests/Dapper.Tests/EnumTests.cs:124](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/tests/Dapper.Tests/EnumTests.cs#L124) | `public SO27024806Enum MyField { get; set; }` |
| [tests/Dapper.Tests/EnumTests.cs:128](https://github.com/DapperLib/Dapper/blob/eb47546a408bbf6c178bda4f04dc205bc51ffbfe/tests/Dapper.Tests/EnumTests.cs#L128) | `public void SO27024806_TestVarcharEnumMemberWithExplicitConstructor()` |

Full lexical records (32) and complete listed paths are in [inventory.json](evidence/inventory.json). A display limit does not remove omitted records from scope.

## Capability ownership

| Package | Retained capability | Internal planning labels; public names come from source |
|---|---|---|
| WP-01 | Command and connection ownership | SqlCommand; CommandOptions; RowCursor |
| WP-02 | Parameters and type conversion | ParameterBinder; TypeHandler; ColumnValue |
| WP-03 | Row and object materialization | RowMapper; ConstructorBinding; MappingCacheKey |
| WP-04 | Multi-mapping streaming and batching | SplitPoint; GridReader; BatchResult |
| WP-05 | Provider integration and optional contrib | SqlDialect; ProviderCapability; ContribProfile |


Map every observed source module/member onto one of these packages or a new explicitly retained package during E02. Structural listing is complete only to the scope stated above; behavioral analysis is sampled.
