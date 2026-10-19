# DJ-064 .j Automap: module and API inventory

| Observed item | Count | Interpretation |
|---|---|---|
| Listed blob paths | 591 | recursive complete |
| Project-definition paths | 6 | Files, not restored packages |
| API-definition/ref paths | 0 | Candidate declarations, not a complete public API census |
| Test/fixture candidate paths | 423 | Lexical path classification, not runnable test count |
| Sampled text files | 8 | Metadata plus selected API/implementation/tests |
| Lexical public/protected declarations | 91 | May include test helpers; not semantic API count |
| Lexical test-method candidates | 14 | Attribute inference only; no test discovery or execution |

## Extraction method and remaining closure

The tree supplies path identity. Project suffixes identify structural module candidates. Public/protected lines and test-like methods are extracted lexically from sampled files; multiline declarations, conditional compilation, generated code, extension methods, overload relationships and fixture parameter expansion require compiler-aware extraction. E02 must evaluate every target framework/configuration, generated source and conditional reference. Unassigned members remain retained scope, never implicitly removed.

## Observed project/module ledger

| Pinned path | Role candidate | Disposition |
|---|---|---|
| [src/AutoMapper.DI.Tests/AutoMapper.DI.Tests.csproj](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/AutoMapper.DI.Tests/AutoMapper.DI.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/AutoMapper/AutoMapper.csproj](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/AutoMapper/AutoMapper.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/Benchmark/Benchmark.csproj](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/Benchmark/Benchmark.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [src/IntegrationTests/AutoMapper.IntegrationTests.csproj](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/IntegrationTests/AutoMapper.IntegrationTests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/TestApp/TestApp.csproj](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/TestApp/TestApp.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/UnitTests/AutoMapper.UnitTests.csproj](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/AutoMapper.UnitTests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |

## Sampled declaration candidates

| Source | Declaration candidate |
|---|---|
| [src/AutoMapper/Mapper.cs:5](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/AutoMapper/Mapper.cs#L5) | `public interface IMapperBase` |
| [src/AutoMapper/Mapper.cs:50](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/AutoMapper/Mapper.cs#L50) | `public interface IMapper : IMapperBase` |
| [src/AutoMapper/Mapper.cs:131](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/AutoMapper/Mapper.cs#L131) | `public interface IRuntimeMapper : IMapperBase` |
| [src/AutoMapper/Mapper.cs:140](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/AutoMapper/Mapper.cs#L140) | `public sealed class Mapper : IMapper, IInternalRuntimeMapper` |
| [src/AutoMapper/Mapper.cs:145](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/AutoMapper/Mapper.cs#L145) | `public Mapper(IConfigurationProvider configuration) : this(configuration, configuration.Internal().ServiceCtor) { }` |
| [src/AutoMapper/Mapper.cs:146](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/AutoMapper/Mapper.cs#L146) | `public Mapper(IConfigurationProvider configuration, Factory serviceCtor)` |
| [src/AutoMapper/Mapper.cs:156](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/AutoMapper/Mapper.cs#L156) | `public IConfigurationProvider ConfigurationProvider => _configuration;` |
| [src/AutoMapper/Mapper.cs:157](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/AutoMapper/Mapper.cs#L157) | `public TDestination Map<TDestination>(object source) => Map(source, default(TDestination));` |
| [src/AutoMapper/Mapper.cs:158](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/AutoMapper/Mapper.cs#L158) | `public TDestination Map<TDestination>(object source, Action<IMappingOperationOptions<object, TDestination>> opts) => Map(source, default, opts);` |
| [src/AutoMapper/Mapper.cs:159](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/AutoMapper/Mapper.cs#L159) | `public TDestination Map<TSource, TDestination>(TSource source) => Map(source, default(TDestination));` |
| [src/AutoMapper/Mapper.cs:160](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/AutoMapper/Mapper.cs#L160) | `public TDestination Map<TSource, TDestination>(TSource source, Action<IMappingOperationOptions<TSource, TDestination>> opts) =>` |
| [src/AutoMapper/Mapper.cs:162](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/AutoMapper/Mapper.cs#L162) | `public TDestination Map<TSource, TDestination>(TSource source, TDestination destination) =>` |
| [src/AutoMapper/Mapper.cs:164](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/AutoMapper/Mapper.cs#L164) | `public TDestination Map<TSource, TDestination>(TSource source, TDestination destination, Action<IMappingOperationOptions<TSource, TDestination>> opts) =>` |
| [src/AutoMapper/Mapper.cs:166](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/AutoMapper/Mapper.cs#L166) | `public object Map(object source, Type sourceType, Type destinationType) => Map(source, null, sourceType, destinationType);` |
| [src/AutoMapper/Mapper.cs:167](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/AutoMapper/Mapper.cs#L167) | `public object Map(object source, Type sourceType, Type destinationType, Action<IObjectMappingOperationOptions> opts) =>` |
| [src/AutoMapper/Mapper.cs:169](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/AutoMapper/Mapper.cs#L169) | `public object Map(object source, object destination, Type sourceType, Type destinationType) =>` |
| [src/AutoMapper/Mapper.cs:171](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/AutoMapper/Mapper.cs#L171) | `public object Map(object source, object destination, Type sourceType, Type destinationType, Action<IObjectMappingOperationOptions> opts) =>` |
| [src/AutoMapper/Mapper.cs:173](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/AutoMapper/Mapper.cs#L173) | `public IQueryable<TDestination> ProjectTo<TDestination>(IQueryable source, object parameters, params Expression<Func<TDestination, object>>[] membersToExpand)` |
| [src/AutoMapper/Mapper.cs:175](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/AutoMapper/Mapper.cs#L175) | `public IQueryable<TDestination> ProjectTo<TDestination>(IQueryable source, IDictionary<string, object> parameters, params string[] membersToExpand)` |
| [src/AutoMapper/Mapper.cs:177](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/AutoMapper/Mapper.cs#L177) | `public IQueryable ProjectTo(IQueryable source, Type destinationType, IDictionary<string, object> parameters, params string[] membersToExpand)` |
| [src/AutoMapper/PathMap.cs:5](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/AutoMapper/PathMap.cs#L5) | `public sealed class PathMap(LambdaExpression destinationExpression, MemberPath memberPath, TypeMap typeMap)` |
| [src/AutoMapper/PathMap.cs:8](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/AutoMapper/PathMap.cs#L8) | `public PathMap(PathMap pathMap, TypeMap typeMap, IncludedMember includedMember) : this(pathMap.DestinationExpression, pathMap.MemberPath, typeMap)` |
| [src/AutoMapper/PathMap.cs:15](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/AutoMapper/PathMap.cs#L15) | `public override Type SourceType => Resolver.ResolvedType;` |
| [src/AutoMapper/PathMap.cs:16](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/AutoMapper/PathMap.cs#L16) | `public LambdaExpression DestinationExpression { get; } = destinationExpression;` |
| [src/AutoMapper/PathMap.cs:17](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/AutoMapper/PathMap.cs#L17) | `public MemberPath MemberPath { get; } = memberPath;` |
| [src/AutoMapper/PathMap.cs:18](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/AutoMapper/PathMap.cs#L18) | `public override string DestinationName => MemberPath.ToString();` |
| [src/AutoMapper/PathMap.cs:19](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/AutoMapper/PathMap.cs#L19) | `public override bool CanBeSet => ReflectionHelper.CanBeSet(MemberPath.Last);` |
| [src/AutoMapper/PathMap.cs:20](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/AutoMapper/PathMap.cs#L20) | `public override bool Ignored { get; set; }` |
| [src/AutoMapper/PathMap.cs:21](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/AutoMapper/PathMap.cs#L21) | `public override IncludedMember IncludedMember { get; protected set; }` |
| [src/AutoMapper/PathMap.cs:22](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/AutoMapper/PathMap.cs#L22) | `public override LambdaExpression Condition { get; set; }` |
| [src/UnitTests/MaxDepthTests.cs:3](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/MaxDepthTests.cs#L3) | `public class MaxDepthTests` |
| [src/UnitTests/MaxDepthTests.cs:5](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/MaxDepthTests.cs#L5) | `public class Source` |
| [src/UnitTests/MaxDepthTests.cs:7](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/MaxDepthTests.cs#L7) | `public int Level { get; set; }` |
| [src/UnitTests/MaxDepthTests.cs:8](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/MaxDepthTests.cs#L8) | `public IList<Source> Children { get; set; }` |
| [src/UnitTests/MaxDepthTests.cs:9](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/MaxDepthTests.cs#L9) | `public Source Parent { get; set; }` |
| [src/UnitTests/MaxDepthTests.cs:11](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/MaxDepthTests.cs#L11) | `public Source(int level)` |
| [src/UnitTests/MaxDepthTests.cs:17](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/MaxDepthTests.cs#L17) | `public void AddChild(Source child)` |
| [src/UnitTests/MaxDepthTests.cs:24](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/MaxDepthTests.cs#L24) | `public class Destination` |
| [src/UnitTests/MaxDepthTests.cs:26](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/MaxDepthTests.cs#L26) | `public int Level { get; set; }` |
| [src/UnitTests/MaxDepthTests.cs:27](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/MaxDepthTests.cs#L27) | `public IList<Destination> Children { get; set; }` |
| [src/UnitTests/MaxDepthTests.cs:28](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/MaxDepthTests.cs#L28) | `public Destination Parent { get; set; }` |
| [src/UnitTests/MaxDepthTests.cs:33](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/MaxDepthTests.cs#L33) | `public MaxDepthTests()` |
| [src/UnitTests/MaxDepthTests.cs:54](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/MaxDepthTests.cs#L54) | `public void Second_level_children_is_empty_with_max_depth_1()` |
| [src/UnitTests/MaxDepthTests.cs:62](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/MaxDepthTests.cs#L62) | `public void Second_level_children_are_not_null_with_max_depth_2()` |
| [src/UnitTests/MaxDepthTests.cs:75](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/MaxDepthTests.cs#L75) | `public void Third_level_children_is_empty_with_max_depth_2()` |
| [src/UnitTests/MaxDepthTests.cs:86](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/MaxDepthTests.cs#L86) | `public void Third_level_children_are_not_null_max_depth_3()` |
| [src/UnitTests/IgnoreAllTests.cs:3](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/IgnoreAllTests.cs#L3) | `public class When_overriding_global_ignore : AutoMapperSpecBase` |
| [src/UnitTests/IgnoreAllTests.cs:7](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/IgnoreAllTests.cs#L7) | `public class Source` |
| [src/UnitTests/IgnoreAllTests.cs:9](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/IgnoreAllTests.cs#L9) | `public int ShouldBeMapped { get; set; }` |
| [src/UnitTests/IgnoreAllTests.cs:12](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/IgnoreAllTests.cs#L12) | `public class Destination` |
| [src/UnitTests/IgnoreAllTests.cs:14](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/IgnoreAllTests.cs#L14) | `public int ShouldBeMapped { get; set; }` |
| [src/UnitTests/IgnoreAllTests.cs:17](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/IgnoreAllTests.cs#L17) | `protected override MapperConfiguration CreateConfiguration() => new(cfg =>` |
| [src/UnitTests/IgnoreAllTests.cs:23](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/IgnoreAllTests.cs#L23) | `protected override void Because_of()` |
| [src/UnitTests/IgnoreAllTests.cs:29](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/IgnoreAllTests.cs#L29) | `public void Should_not_ignore()` |
| [src/UnitTests/IgnoreAllTests.cs:35](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/IgnoreAllTests.cs#L35) | `public class IgnoreAllTests` |
| [src/UnitTests/IgnoreAllTests.cs:37](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/IgnoreAllTests.cs#L37) | `public class Source` |
| [src/UnitTests/IgnoreAllTests.cs:39](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/IgnoreAllTests.cs#L39) | `public string ShouldBeMapped { get; set; }` |
| [src/UnitTests/IgnoreAllTests.cs:42](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/IgnoreAllTests.cs#L42) | `public class Destination` |
| [src/UnitTests/IgnoreAllTests.cs:44](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/IgnoreAllTests.cs#L44) | `public string ShouldBeMapped { get; set; }` |
| [src/UnitTests/IgnoreAllTests.cs:45](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/IgnoreAllTests.cs#L45) | `public string StartingWith_ShouldNotBeMapped { get; set; }` |
| [src/UnitTests/IgnoreAllTests.cs:46](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/IgnoreAllTests.cs#L46) | `public List<string> StartingWith_ShouldBeNullAfterwards { get; set; }` |
| [src/UnitTests/IgnoreAllTests.cs:47](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/IgnoreAllTests.cs#L47) | `public string AnotherString_ShouldBeNullAfterwards { get; set; }` |
| [src/UnitTests/IgnoreAllTests.cs:50](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/IgnoreAllTests.cs#L50) | `public class DestinationWrongType` |
| [src/UnitTests/IgnoreAllTests.cs:52](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/IgnoreAllTests.cs#L52) | `public Destination ShouldBeMapped { get; set; }` |
| [src/UnitTests/IgnoreAllTests.cs:55](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/IgnoreAllTests.cs#L55) | `public class FooProfile : Profile` |
| [src/UnitTests/IgnoreAllTests.cs:57](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/IgnoreAllTests.cs#L57) | `public FooProfile()` |
| [src/UnitTests/IgnoreAllTests.cs:65](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/IgnoreAllTests.cs#L65) | `public void GlobalIgnore_ignores_all_properties_beginning_with_string()` |
| [src/UnitTests/IgnoreAllTests.cs:79](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/IgnoreAllTests.cs#L79) | `public void GlobalIgnore_ignores_all_properties_beginning_with_string_in_profiles()` |
| [src/UnitTests/IgnoreAllTests.cs:92](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/IgnoreAllTests.cs#L92) | `public void GlobalIgnore_ignores_properties_with_names_matching_but_different_types()` |
| [src/UnitTests/IgnoreAllTests.cs:105](https://github.com/LuckyPennySoftware/AutoMapper/blob/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1/src/UnitTests/IgnoreAllTests.cs#L105) | `public void Ignored_properties_should_be_default_value()` |

Full lexical records (91) and complete listed paths are in [inventory.json](evidence/inventory.json). A display limit does not remove omitted records from scope.

## Capability ownership

| Package | Retained capability | Proposed contract names |
|---|---|---|
| WP-01 | License baseline and mapping contract | MappingLicenseRecord; MappingProfile; TypeMap |
| WP-02 | Mapping plan resolution and execution | ResolutionContext; MemberPlan; ValueResolver |
| WP-03 | Configuration validation and advanced mapping | ConfigurationProvider; InclusionRule; ConversionPolicy |
| WP-04 | Query projection and expression adaptation | ProjectionExpression; EntityProjectionAdapter; ProjectionDiagnostic |
| WP-05 | Adapters and behavioral verification | MapperService; MapFixture; LicenseGate |


Map every observed source module/member onto one of these packages or a new explicitly retained package during E02. Structural listing is complete only to the scope stated above; behavioral analysis is sampled.
