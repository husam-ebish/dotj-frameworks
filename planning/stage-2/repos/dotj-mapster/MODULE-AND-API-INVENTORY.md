# DJ-024 .j Mapster: module and API inventory

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

| Observed item | Count | Interpretation |
|---|---|---|
| Listed blob paths | 463 | recursive complete |
| Project-definition paths | 26 | Files, not restored packages |
| API-definition/ref paths | 0 | Candidate declarations, not a complete public API census |
| Test/fixture candidate paths | 126 | Lexical path classification, not runnable test count |
| Sampled text files | 10 | Metadata plus selected API/implementation/tests |
| Lexical public/protected declarations | 50 | May include test helpers; not semantic API count |
| Lexical test-method candidates | 6 | Attribute inference only; no test discovery or execution |

## Extraction method and remaining closure

The tree supplies path identity. Project suffixes identify structural module candidates. Public/protected lines and test-like methods are extracted lexically from sampled files; multiline declarations, conditional compilation, generated code, extension methods, overload relationships and fixture parameter expansion require compiler-aware extraction. E02 must evaluate every target framework/configuration, generated source and conditional reference. Unassigned members remain retained scope, never implicitly removed.

## Observed project/module ledger

| Pinned path | Role candidate | Disposition |
|---|---|---|
| [src/Benchmark.Development/Benchmark.Development.csproj](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Benchmark.Development/Benchmark.Development.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [src/Benchmark/Benchmark.csproj](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Benchmark/Benchmark.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [src/ExpressionDebugger.Console/ExpressionDebugger.Console.csproj](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/ExpressionDebugger.Console/ExpressionDebugger.Console.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/ExpressionDebugger.Tests/ExpressionDebugger.Tests.csproj](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/ExpressionDebugger.Tests/ExpressionDebugger.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/ExpressionDebugger/ExpressionDebugger.csproj](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/ExpressionDebugger/ExpressionDebugger.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/ExpressionTranslator/ExpressionTranslator.csproj](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/ExpressionTranslator/ExpressionTranslator.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/Mapster.Async.Tests/Mapster.Async.Tests.csproj](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster.Async.Tests/Mapster.Async.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/Mapster.Async/Mapster.Async.csproj](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster.Async/Mapster.Async.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/Mapster.Core/Mapster.Core.csproj](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster.Core/Mapster.Core.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/Mapster.DependencyInjection.Tests/Mapster.DependencyInjection.Tests.csproj](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster.DependencyInjection.Tests/Mapster.DependencyInjection.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/Mapster.DependencyInjection/Mapster.DependencyInjection.csproj](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster.DependencyInjection/Mapster.DependencyInjection.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/Mapster.EF6/Mapster.EF6.csproj](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster.EF6/Mapster.EF6.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/Mapster.EFCore.Tests/Mapster.EFCore.Tests.csproj](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster.EFCore.Tests/Mapster.EFCore.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/Mapster.EFCore/Mapster.EFCore.csproj](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster.EFCore/Mapster.EFCore.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/Mapster.Immutable.Tests/Mapster.Immutable.Tests.csproj](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster.Immutable.Tests/Mapster.Immutable.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/Mapster.Immutable/Mapster.Immutable.csproj](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster.Immutable/Mapster.Immutable.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/Mapster.JsonNet.Tests/Mapster.JsonNet.Tests.csproj](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster.JsonNet.Tests/Mapster.JsonNet.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/Mapster.JsonNet/Mapster.JsonNet.csproj](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster.JsonNet/Mapster.JsonNet.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/Mapster.SourceGenerator/Mapster.SourceGenerator.csproj](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster.SourceGenerator/Mapster.SourceGenerator.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/Mapster.Tests/Mapster.Tests.csproj](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster.Tests/Mapster.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/Mapster.Tool.Tests/Mapster.Tool.Tests.csproj](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster.Tool.Tests/Mapster.Tool.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/Mapster.Tool/Mapster.Tool.csproj](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster.Tool/Mapster.Tool.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/Mapster/Mapster.csproj](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster/Mapster.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/Sample.AspNetCore/Sample.AspNetCore.csproj](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Sample.AspNetCore/Sample.AspNetCore.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [src/Sample.CodeGen/Sample.CodeGen.csproj](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Sample.CodeGen/Sample.CodeGen.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [src/TemplateTest/TemplateTest.csproj](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/TemplateTest/TemplateTest.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |

## Sampled declaration candidates

| Source | Declaration candidate |
|---|---|
| [src/ExpressionDebugger/ExpressionCompiler.cs:16](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/ExpressionDebugger/ExpressionCompiler.cs#L16) | `public class ExpressionCompiler` |
| [src/ExpressionDebugger/ExpressionCompiler.cs:18](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/ExpressionDebugger/ExpressionCompiler.cs#L18) | `public List<ExpressionTranslator> Translators { get; } = new List<ExpressionTranslator>();` |
| [src/ExpressionDebugger/ExpressionCompiler.cs:21](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/ExpressionDebugger/ExpressionCompiler.cs#L21) | `public ExpressionCompiler(ExpressionCompilationOptions? options = null)` |
| [src/ExpressionDebugger/ExpressionCompiler.cs:27](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/ExpressionDebugger/ExpressionCompiler.cs#L27) | `public void AddFile(string code, string filename)` |
| [src/ExpressionDebugger/ExpressionCompiler.cs:54](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/ExpressionDebugger/ExpressionCompiler.cs#L54) | `public void AddFile(LambdaExpression node, ExpressionDefinitions? definitions = null)` |
| [src/ExpressionDebugger/ExpressionCompiler.cs:66](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/ExpressionDebugger/ExpressionCompiler.cs#L66) | `public Assembly CreateAssembly()` |
| [src/Mapster/Mapper.cs:9](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster/Mapper.cs#L9) | `public class Mapper : IMapper` |
| [src/Mapster/Mapper.cs:11](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster/Mapper.cs#L11) | `public TypeAdapterConfig Config { get; }` |
| [src/Mapster/Mapper.cs:13](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster/Mapper.cs#L13) | `public Mapper() : this(TypeAdapterConfig.GlobalSettings) { }` |
| [src/Mapster/Mapper.cs:15](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster/Mapper.cs#L15) | `public Mapper(TypeAdapterConfig config)` |
| [src/Mapster/Mapper.cs:26](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster/Mapper.cs#L26) | `public virtual ITypeAdapterBuilder<TSource> From<TSource>(TSource source)` |
| [src/Mapster/Mapper.cs:38](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster/Mapper.cs#L38) | `public virtual TDestination Map<TDestination>(object source)` |
| [src/Mapster/Mapper.cs:56](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster/Mapper.cs#L56) | `public virtual TDestination Map<TSource, TDestination>(TSource source)` |
| [src/Mapster/Mapper.cs:71](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster/Mapper.cs#L71) | `public virtual TDestination Map<TSource, TDestination>(TSource source, TDestination destination)` |
| [src/Mapster/Mapper.cs:85](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster/Mapper.cs#L85) | `public virtual object Map(object source, Type sourceType, Type destinationType)` |
| [src/Mapster/Mapper.cs:103](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster/Mapper.cs#L103) | `public virtual object Map(object source, object destination, Type sourceType, Type destinationType)` |
| [src/Mapster.Tests/DynamicTypeGeneratorTests.cs:10](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster.Tests/DynamicTypeGeneratorTests.cs#L10) | `public class DynamicTypeGeneratorTests` |
| [src/Mapster.Tests/DynamicTypeGeneratorTests.cs:18](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster.Tests/DynamicTypeGeneratorTests.cs#L18) | `public interface ISimpleInterface` |
| [src/Mapster.Tests/DynamicTypeGeneratorTests.cs:24](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster.Tests/DynamicTypeGeneratorTests.cs#L24) | `public interface IInheritedInterface : ISimpleInterface` |
| [src/Mapster.Tests/DynamicTypeGeneratorTests.cs:29](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster.Tests/DynamicTypeGeneratorTests.cs#L29) | `public class Foo` |
| [src/Mapster.Tests/DynamicTypeGeneratorTests.cs:31](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster.Tests/DynamicTypeGeneratorTests.cs#L31) | `public int Id { get; set; }` |
| [src/Mapster.Tests/DynamicTypeGeneratorTests.cs:32](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster.Tests/DynamicTypeGeneratorTests.cs#L32) | `public string Name { get; set; }` |
| [src/Mapster.Tests/DynamicTypeGeneratorTests.cs:35](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster.Tests/DynamicTypeGeneratorTests.cs#L35) | `public interface IComplexBaseInterface` |
| [src/Mapster.Tests/DynamicTypeGeneratorTests.cs:42](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster.Tests/DynamicTypeGeneratorTests.cs#L42) | `public interface IComplexInterface : IComplexBaseInterface` |
| [src/Mapster.Tests/DynamicTypeGeneratorTests.cs:55](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster.Tests/DynamicTypeGeneratorTests.cs#L55) | `public void ThrowExceptionWhenInterfaceIsNotVisible()` |
| [src/Mapster.Tests/DynamicTypeGeneratorTests.cs:64](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster.Tests/DynamicTypeGeneratorTests.cs#L64) | `public void CreateTypeForSimpleInterface()` |
| [src/Mapster.Tests/DynamicTypeGeneratorTests.cs:80](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster.Tests/DynamicTypeGeneratorTests.cs#L80) | `public void CreateTypeForInheritedInterface()` |
| [src/Mapster.Tests/DynamicTypeGeneratorTests.cs:98](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster.Tests/DynamicTypeGeneratorTests.cs#L98) | `public void CreateTypeForComplexInterface()` |
| [src/Mapster.Tests/DynamicTypeGeneratorTests.cs:128](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster.Tests/DynamicTypeGeneratorTests.cs#L128) | `public void WhenMappingDerivedFromInterfaceWithoutMembers()` |
| [src/Mapster.Tests/DynamicTypeGeneratorTests.cs:138](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster.Tests/DynamicTypeGeneratorTests.cs#L138) | `public interface ISource` |
| [src/Mapster.Tests/DynamicTypeGeneratorTests.cs:142](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster.Tests/DynamicTypeGeneratorTests.cs#L142) | `public class Source : ISource` |
| [src/Mapster.Tests/DynamicTypeGeneratorTests.cs:144](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster.Tests/DynamicTypeGeneratorTests.cs#L144) | `public string Tag { get; set; }` |
| [src/Mapster.Tests/DynamicTypeGeneratorTests.cs:147](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster.Tests/DynamicTypeGeneratorTests.cs#L147) | `public interface IDestination` |
| [src/Mapster.Tests/DynamicTypeGeneratorTests.cs:151](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster.Tests/DynamicTypeGeneratorTests.cs#L151) | `public class Destination : IDestination` |
| [src/Mapster.Tests/DynamicTypeGeneratorTests.cs:153](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/Mapster.Tests/DynamicTypeGeneratorTests.cs#L153) | `public string Tag { get; set; }` |
| [src/TemplateTest/FooTest.cs:10](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/TemplateTest/FooTest.cs#L10) | `public class FooTest` |
| [src/TemplateTest/FooTest.cs:13](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/TemplateTest/FooTest.cs#L13) | `public void TestCreateMapExpression()` |
| [src/TemplateTest/FooTest.cs:33](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/TemplateTest/FooTest.cs#L33) | `public class Foo` |
| [src/TemplateTest/FooTest.cs:35](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/TemplateTest/FooTest.cs#L35) | `public string Name { get; set; }` |
| [src/TemplateTest/FooTest.cs:37](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/TemplateTest/FooTest.cs#L37) | `public int Int32 { get; set; }` |
| [src/TemplateTest/FooTest.cs:39](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/TemplateTest/FooTest.cs#L39) | `public long Int64 { set; get; }` |
| [src/TemplateTest/FooTest.cs:41](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/TemplateTest/FooTest.cs#L41) | `public int? NullInt { get; set; }` |
| [src/TemplateTest/FooTest.cs:43](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/TemplateTest/FooTest.cs#L43) | `public float Floatn { get; set; }` |
| [src/TemplateTest/FooTest.cs:45](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/TemplateTest/FooTest.cs#L45) | `public double Doublen { get; set; }` |
| [src/TemplateTest/FooTest.cs:47](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/TemplateTest/FooTest.cs#L47) | `public DateTime DateTime { get; set; }` |
| [src/TemplateTest/FooTest.cs:49](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/TemplateTest/FooTest.cs#L49) | `public Foo Foo1 { get; set; }` |
| [src/TemplateTest/FooTest.cs:51](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/TemplateTest/FooTest.cs#L51) | `public IEnumerable<Foo> Foos { get; set; }` |
| [src/TemplateTest/FooTest.cs:53](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/TemplateTest/FooTest.cs#L53) | `public Foo[] FooArr { get; set; }` |
| [src/TemplateTest/FooTest.cs:55](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/TemplateTest/FooTest.cs#L55) | `public int[] IntArr { get; set; }` |
| [src/TemplateTest/FooTest.cs:57](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/TemplateTest/FooTest.cs#L57) | `public IEnumerable<int> Ints { get; set; }` |

Full lexical records (50) and complete listed paths are in [inventory.json](evidence/inventory.json). A display limit does not remove omitted records from scope.

## Capability ownership

| Package | Retained capability | Internal planning labels; public names come from source |
|---|---|---|
| WP-01 | Configuration and type model | MappingConfig; TypePair; MemberPath |
| WP-02 | Mapping plan and execution | MappingPlan; MemberAssignment; ConversionStep |
| WP-03 | Generated mappings and diagnostics | GeneratedMapper; SourceLocation; GenerationManifest |
| WP-04 | Queryable projection boundary | ProjectionPlan; QueryProviderAdapter; ProjectionCapability |
| WP-05 | Adapters and behavior parity | MapperFacade; DependencyResolver; MapsterProfile |


Map every observed source module/member onto one of these packages or a new explicitly retained package during E02. Structural listing is complete only to the scope stated above; behavioral analysis is sampled.
