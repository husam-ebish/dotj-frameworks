# DJ-039 .j GraphQL: module and API inventory

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

| Observed item | Count | Interpretation |
|---|---|---|
| Listed blob paths | 1408 | recursive complete |
| Project-definition paths | 31 | Files, not restored packages |
| API-definition/ref paths | 0 | Candidate declarations, not a complete public API census |
| Test/fixture candidate paths | 528 | Lexical path classification, not runnable test count |
| Sampled text files | 9 | Metadata plus selected API/implementation/tests |
| Lexical public/protected declarations | 28 | May include test helpers; not semantic API count |
| Lexical test-method candidates | 9 | Attribute inference only; no test discovery or execution |

## Extraction method and remaining closure

The tree supplies path identity. Project suffixes identify structural module candidates. Public/protected lines and test-like methods are extracted lexically from sampled files; multiline declarations, conditional compilation, generated code, extension methods, overload relationships and fixture parameter expansion require compiler-aware extraction. E02 must evaluate every target framework/configuration, generated source and conditional reference. Unassigned members remain retained scope, never implicitly removed.

## Observed project/module ledger

| Pinned path | Role candidate | Disposition |
|---|---|---|
| [samples/GraphQL.AotCompilationSample.CodeFirst/GraphQL.AotCompilationSample.CodeFirst.csproj](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/samples/GraphQL.AotCompilationSample.CodeFirst/GraphQL.AotCompilationSample.CodeFirst.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/GraphQL.AotCompilationSample.TypeFirst/GraphQL.AotCompilationSample.TypeFirst.csproj](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/samples/GraphQL.AotCompilationSample.TypeFirst/GraphQL.AotCompilationSample.TypeFirst.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/GraphQL.DataLoader.Sample.DI/GraphQL.DataLoader.Sample.DI.csproj](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/samples/GraphQL.DataLoader.Sample.DI/GraphQL.DataLoader.Sample.DI.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/GraphQL.DataLoader.Sample.Default/GraphQL.DataLoader.Sample.Default.csproj](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/samples/GraphQL.DataLoader.Sample.Default/GraphQL.DataLoader.Sample.Default.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/GraphQL.Federation.CodeFirst.Sample3/GraphQL.Federation.CodeFirst.Sample3.csproj](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/samples/GraphQL.Federation.CodeFirst.Sample3/GraphQL.Federation.CodeFirst.Sample3.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/GraphQL.Federation.SchemaFirst.Sample1/GraphQL.Federation.SchemaFirst.Sample1.csproj](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/samples/GraphQL.Federation.SchemaFirst.Sample1/GraphQL.Federation.SchemaFirst.Sample1.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/GraphQL.Federation.SchemaFirst.Sample2/GraphQL.Federation.SchemaFirst.Sample2.csproj](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/samples/GraphQL.Federation.SchemaFirst.Sample2/GraphQL.Federation.SchemaFirst.Sample2.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/GraphQL.Federation.Tests/GraphQL.Federation.Tests.csproj](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/samples/GraphQL.Federation.Tests/GraphQL.Federation.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [samples/GraphQL.Federation.TypeFirst.Sample4/GraphQL.Federation.TypeFirst.Sample4.csproj](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/samples/GraphQL.Federation.TypeFirst.Sample4/GraphQL.Federation.TypeFirst.Sample4.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/GraphQL.Harness.Tests/GraphQL.Harness.Tests.csproj](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/samples/GraphQL.Harness.Tests/GraphQL.Harness.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [samples/GraphQL.Harness/GraphQL.Harness.csproj](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/samples/GraphQL.Harness/GraphQL.Harness.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/GraphQL.Server.Polyfill/GraphQL.Server.Polyfill.csproj](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/samples/GraphQL.Server.Polyfill/GraphQL.Server.Polyfill.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [src/GraphQL.Analyzers.CodeFixes/GraphQL.Analyzers.CodeFixes.csproj](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL.Analyzers.CodeFixes/GraphQL.Analyzers.CodeFixes.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/GraphQL.Analyzers.Package/GraphQL.Analyzers.Package.csproj](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL.Analyzers.Package/GraphQL.Analyzers.Package.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/GraphQL.Analyzers.Tests/GraphQL.Analyzers.Tests.csproj](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL.Analyzers.Tests/GraphQL.Analyzers.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/GraphQL.Analyzers/GraphQL.Analyzers.csproj](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL.Analyzers/GraphQL.Analyzers.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/GraphQL.ApiTests/GraphQL.ApiTests.csproj](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL.ApiTests/GraphQL.ApiTests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/GraphQL.Benchmarks.Merge/GraphQL.Benchmarks.Merge.csproj](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL.Benchmarks.Merge/GraphQL.Benchmarks.Merge.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [src/GraphQL.Benchmarks/GraphQL.Benchmarks.csproj](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL.Benchmarks/GraphQL.Benchmarks.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [src/GraphQL.DataLoader.Tests/GraphQL.DataLoader.Tests.csproj](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL.DataLoader.Tests/GraphQL.DataLoader.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/GraphQL.DataLoader/GraphQL.DataLoader.csproj](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL.DataLoader/GraphQL.DataLoader.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/GraphQL.Dummy/GraphQL.Dummy.csproj](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL.Dummy/GraphQL.Dummy.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/GraphQL.MemoryCache/GraphQL.MemoryCache.csproj](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL.MemoryCache/GraphQL.MemoryCache.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/GraphQL.MicrosoftDI.Tests/GraphQL.MicrosoftDI.Tests.csproj](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL.MicrosoftDI.Tests/GraphQL.MicrosoftDI.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/GraphQL.MicrosoftDI/GraphQL.MicrosoftDI.csproj](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL.MicrosoftDI/GraphQL.MicrosoftDI.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/GraphQL.NewtonsoftJson/GraphQL.NewtonsoftJson.csproj](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL.NewtonsoftJson/GraphQL.NewtonsoftJson.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/GraphQL.StarWars.TypeFirst/GraphQL.StarWars.TypeFirst.csproj](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL.StarWars.TypeFirst/GraphQL.StarWars.TypeFirst.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/GraphQL.StarWars/GraphQL.StarWars.csproj](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL.StarWars/GraphQL.StarWars.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/GraphQL.SystemTextJson/GraphQL.SystemTextJson.csproj](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL.SystemTextJson/GraphQL.SystemTextJson.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/GraphQL.Tests/GraphQL.Tests.csproj](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL.Tests/GraphQL.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/GraphQL/GraphQL.csproj](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL/GraphQL.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |

## Sampled declaration candidates

| Source | Declaration candidate |
|---|---|
| [src/GraphQL/BoolBox.cs:4](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL/BoolBox.cs#L4) | `public static class BoolBox` |
| [src/GraphQL/BoolBox.cs:9](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL/BoolBox.cs#L9) | `public static readonly object True = true;` |
| [src/GraphQL/BoolBox.cs:14](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL/BoolBox.cs#L14) | `public static readonly object False = false;` |
| [src/GraphQL/BoolBox.cs:19](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL/BoolBox.cs#L19) | `public static object Boxed(this bool value) => value switch` |
| [src/GraphQL/BoolBox.cs:28](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL/BoolBox.cs#L28) | `public static object? Boxed(this bool? value) => value switch` |
| [src/GraphQL/VariableName.cs:9](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL/VariableName.cs#L9) | `public struct VariableName` |
| [src/GraphQL/VariableName.cs:14](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL/VariableName.cs#L14) | `public VariableName(VariableName variableName, int index)` |
| [src/GraphQL/VariableName.cs:24](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL/VariableName.cs#L24) | `public VariableName(VariableName variableName, string childName)` |
| [src/GraphQL/VariableName.cs:43](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL/VariableName.cs#L43) | `public string Name { get; set; }` |
| [src/GraphQL/VariableName.cs:48](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL/VariableName.cs#L48) | `public int? Index { get; set; }` |
| [src/GraphQL/VariableName.cs:53](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL/VariableName.cs#L53) | `public string? ChildName { get; set; }` |
| [src/GraphQL/VariableName.cs:63](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL/VariableName.cs#L63) | `public static implicit operator VariableName(string name) => new() { Name = name };` |
| [src/GraphQL/VariableName.cs:66](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL/VariableName.cs#L66) | `public static implicit operator string(VariableName variableName) => variableName.ToString();` |
| [src/GraphQL.ApiTests/BomTests.cs:5](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL.ApiTests/BomTests.cs#L5) | `public class BomTests` |
| [src/GraphQL.ApiTests/BomTests.cs:9](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL.ApiTests/BomTests.cs#L9) | `public void Files_Should_Not_Use_BOM()` |
| [src/GraphQL.Tests/AuthorizationTests.cs:5](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL.Tests/AuthorizationTests.cs#L5) | `public class AuthorizationTests` |
| [src/GraphQL.Tests/AuthorizationTests.cs:8](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL.Tests/AuthorizationTests.cs#L8) | `public void Field()` |
| [src/GraphQL.Tests/AuthorizationTests.cs:29](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL.Tests/AuthorizationTests.cs#L29) | `public void NoRoles()` |
| [src/GraphQL.Tests/AuthorizationTests.cs:40](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL.Tests/AuthorizationTests.cs#L40) | `public void AllowAnonymous()` |
| [src/GraphQL.Tests/AuthorizationTests.cs:49](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL.Tests/AuthorizationTests.cs#L49) | `public void Authorize()` |
| [src/GraphQL.Tests/AuthorizationTests.cs:58](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL.Tests/AuthorizationTests.cs#L58) | `public void FieldBuilder()` |
| [src/GraphQL.Tests/AuthorizationTests.cs:78](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL.Tests/AuthorizationTests.cs#L78) | `public void ConnectionBuilder()` |
| [src/GraphQL.Tests/AuthorizationTests.cs:98](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL.Tests/AuthorizationTests.cs#L98) | `public void AutoOutputGraphType()` |
| [src/GraphQL.Tests/AuthorizationTests.cs:124](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL.Tests/AuthorizationTests.cs#L124) | `public void SchemaBuilder()` |
| [src/GraphQL.Tests/AuthorizationTests.cs:171](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL.Tests/AuthorizationTests.cs#L171) | `public string Id { get; set; }` |
| [src/GraphQL.Tests/AuthorizationTests.cs:178](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL.Tests/AuthorizationTests.cs#L178) | `public string Name { get; set; }` |
| [src/GraphQL.Tests/AuthorizationTests.cs:180](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL.Tests/AuthorizationTests.cs#L180) | `public string Value { get; set; }` |
| [src/GraphQL.Tests/AuthorizationTests.cs:182](https://github.com/graphql-dotnet/graphql-dotnet/blob/af0b3e77b874cc73167d70910103ac708f14ed28/src/GraphQL.Tests/AuthorizationTests.cs#L182) | `public string Public { get; set; }` |

Full lexical records (28) and complete listed paths are in [inventory.json](evidence/inventory.json). A display limit does not remove omitted records from scope.

## Capability ownership

| Package | Retained capability | Internal planning labels; public names come from source |
|---|---|---|
| WP-01 | Parser AST and schema types | DocumentNode; GraphType; Schema |
| WP-02 | Validation coercion and operation planning | ValidationContext; VariableValue; ExecutionPlan |
| WP-03 | Execution errors and asynchronous fields | ExecutionContext; FieldResult; ExecutionError |
| WP-04 | Subscriptions loaders and adapters | SubscriptionSource; DataLoader; GraphHttpAdapter |
| WP-05 | Specification and upstream regression suite | GraphProfile; ValidationCase; ExecutionTrace |


Map every observed source module/member onto one of these packages or a new explicitly retained package during E02. Structural listing is complete only to the scope stated above; behavioral analysis is sampled.
