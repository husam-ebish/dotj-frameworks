# DJ-037 .j OpenAPI: module and API inventory

| Observed item | Count | Interpretation |
|---|---|---|
| Listed blob paths | 911 | recursive complete |
| Project-definition paths | 38 | Files, not restored packages |
| API-definition/ref paths | 0 | Candidate declarations, not a complete public API census |
| Test/fixture candidate paths | 407 | Lexical path classification, not runnable test count |
| Sampled text files | 11 | Metadata plus selected API/implementation/tests |
| Lexical public/protected declarations | 11 | May include test helpers; not semantic API count |
| Lexical test-method candidates | 5 | Attribute inference only; no test discovery or execution |

## Extraction method and remaining closure

The tree supplies path identity. Project suffixes identify structural module candidates. Public/protected lines and test-like methods are extracted lexically from sampled files; multiline declarations, conditional compilation, generated code, extension methods, overload relationships and fixture parameter expansion require compiler-aware extraction. E02 must evaluate every target framework/configuration, generated source and conditional reference. Unassigned members remain retained scope, never implicitly removed.

## Observed project/module ledger

| Pinned path | Role candidate | Disposition |
|---|---|---|
| [build/_build.csproj](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/build/_build.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/NSwag.Annotations/NSwag.Annotations.csproj](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.Annotations/NSwag.Annotations.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/NSwag.AspNet.Owin/NSwag.AspNet.Owin.csproj](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.AspNet.Owin/NSwag.AspNet.Owin.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/NSwag.AspNet.WebApi/NSwag.AspNet.WebApi.csproj](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.AspNet.WebApi/NSwag.AspNet.WebApi.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/NSwag.AspNetCore.Launcher.x86/NSwag.AspNetCore.Launcher.x86.csproj](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.AspNetCore.Launcher.x86/NSwag.AspNetCore.Launcher.x86.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/NSwag.AspNetCore.Launcher/NSwag.AspNetCore.Launcher.csproj](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.AspNetCore.Launcher/NSwag.AspNetCore.Launcher.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/NSwag.AspNetCore/NSwag.AspNetCore.csproj](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.AspNetCore/NSwag.AspNetCore.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/NSwag.CodeGeneration.CSharp.Tests/NSwag.CodeGeneration.CSharp.Tests.csproj](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.CodeGeneration.CSharp.Tests/NSwag.CodeGeneration.CSharp.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/NSwag.CodeGeneration.CSharp/NSwag.CodeGeneration.CSharp.csproj](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.CodeGeneration.CSharp/NSwag.CodeGeneration.CSharp.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/NSwag.CodeGeneration.Tests/NSwag.CodeGeneration.Tests.csproj](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.CodeGeneration.Tests/NSwag.CodeGeneration.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/NSwag.CodeGeneration.TypeScript.Tests/NSwag.CodeGeneration.TypeScript.Tests.csproj](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.CodeGeneration.TypeScript.Tests/NSwag.CodeGeneration.TypeScript.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/NSwag.CodeGeneration.TypeScript/NSwag.CodeGeneration.TypeScript.csproj](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.CodeGeneration.TypeScript/NSwag.CodeGeneration.TypeScript.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/NSwag.CodeGeneration/NSwag.CodeGeneration.csproj](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.CodeGeneration/NSwag.CodeGeneration.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/NSwag.Commands/NSwag.Commands.csproj](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.Commands/NSwag.Commands.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/NSwag.Console.x86/NSwag.Console.x86.csproj](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.Console.x86/NSwag.Console.x86.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/NSwag.Console/NSwag.Console.csproj](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.Console/NSwag.Console.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/NSwag.ConsoleCore.Tests/NSwag.ConsoleCore.Tests.csproj](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.ConsoleCore.Tests/NSwag.ConsoleCore.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/NSwag.ConsoleCore/NSwag.ConsoleCore.csproj](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.ConsoleCore/NSwag.ConsoleCore.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/NSwag.Core.Tests/NSwag.Core.Tests.csproj](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.Core.Tests/NSwag.Core.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/NSwag.Core.Yaml.Tests/NSwag.Core.Yaml.Tests.csproj](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.Core.Yaml.Tests/NSwag.Core.Yaml.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/NSwag.Core.Yaml/NSwag.Core.Yaml.csproj](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.Core.Yaml/NSwag.Core.Yaml.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/NSwag.Core/NSwag.Core.csproj](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.Core/NSwag.Core.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/NSwag.Generation.AspNetCore.Tests.Web/NSwag.Generation.AspNetCore.Tests.Web.csproj](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.Generation.AspNetCore.Tests.Web/NSwag.Generation.AspNetCore.Tests.Web.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/NSwag.Generation.AspNetCore.Tests/NSwag.Generation.AspNetCore.Tests.csproj](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.Generation.AspNetCore.Tests/NSwag.Generation.AspNetCore.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/NSwag.Generation.AspNetCore/NSwag.Generation.AspNetCore.csproj](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.Generation.AspNetCore/NSwag.Generation.AspNetCore.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/NSwag.Generation.Tests/NSwag.Generation.Tests.csproj](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.Generation.Tests/NSwag.Generation.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/NSwag.Generation.WebApi.Tests/NSwag.Generation.WebApi.Tests.csproj](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.Generation.WebApi.Tests/NSwag.Generation.WebApi.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/NSwag.Generation.WebApi/NSwag.Generation.WebApi.csproj](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.Generation.WebApi/NSwag.Generation.WebApi.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/NSwag.Generation/NSwag.Generation.csproj](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.Generation/NSwag.Generation.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/NSwag.Sample.Common/NSwag.Sample.Common.csproj](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.Sample.Common/NSwag.Sample.Common.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [src/NSwag.Sample.NET100/NSwag.Sample.NET100.csproj](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.Sample.NET100/NSwag.Sample.NET100.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [src/NSwag.Sample.NET100Minimal/NSwag.Sample.NET100Minimal.csproj](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.Sample.NET100Minimal/NSwag.Sample.NET100Minimal.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [src/NSwag.Sample.NET80/NSwag.Sample.NET80.csproj](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.Sample.NET80/NSwag.Sample.NET80.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [src/NSwag.Sample.NET80Minimal/NSwag.Sample.NET80Minimal.csproj](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.Sample.NET80Minimal/NSwag.Sample.NET80Minimal.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [src/NSwag.Sample.NET90/NSwag.Sample.NET90.csproj](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.Sample.NET90/NSwag.Sample.NET90.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [src/NSwag.Sample.NET90Minimal/NSwag.Sample.NET90Minimal.csproj](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.Sample.NET90Minimal/NSwag.Sample.NET90Minimal.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [src/NSwag.VersionMissmatchTest/NSwag.VersionMissmatchTest.csproj](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.VersionMissmatchTest/NSwag.VersionMissmatchTest.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/NSwagStudio/NSwagStudio.csproj](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwagStudio/NSwagStudio.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |

## Sampled declaration candidates

| Source | Declaration candidate |
|---|---|
| [src/NSwag.Core/Polyfills.cs:6](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.Core/Polyfills.cs#L6) | `public static bool StartsWith(this string str, char c) => str.Length > 0 && str[0] == c;` |
| [src/NSwag.Core/Polyfills.cs:7](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.Core/Polyfills.cs#L7) | `public static bool EndsWith(this string str, char c) => str.Length > 0 && str[str.Length - 1] == c;` |
| [src/NSwag.Core/Polyfills.cs:8](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.Core/Polyfills.cs#L8) | `public static bool Contains(this string str, string s, StringComparison comparison) => str.IndexOf(s, comparison) != -1;` |
| [src/NSwagStudio/App.xaml.cs:8](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwagStudio/App.xaml.cs#L8) | `public partial class App : Application` |
| [src/NSwag.Core.Tests/HttpLoadingTests.cs:5](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.Core.Tests/HttpLoadingTests.cs#L5) | `public class HttpLoadingTests` |
| [src/NSwag.Core.Tests/HttpLoadingTests.cs:8](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.Core.Tests/HttpLoadingTests.cs#L8) | `public async Task When_Swagger_is_loaded_from_url_then_it_works()` |
| [src/NSwag.Core.Tests/HttpLoadingTests.cs:21](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.Core.Tests/HttpLoadingTests.cs#L21) | `public async Task When_Swagger_is_loaded_from_url_schematype_is_Swagger2()` |
| [src/NSwag.Core.Tests/HttpLoadingTests.cs:34](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.Core.Tests/HttpLoadingTests.cs#L34) | `public async Task When_openapi_is_loaded_without_scopes_it_should_deserialize()` |
| [src/NSwag.Core.Tests/HttpLoadingTests.cs:48](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.Core.Tests/HttpLoadingTests.cs#L48) | `public async Task When_OpenApi_is_loaded_from_url_schematype_is_OpenApi3()` |
| [src/NSwag.Core.Tests/OperationIdTests.cs:5](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.Core.Tests/OperationIdTests.cs#L5) | `public class OperationIdTests` |
| [src/NSwag.Core.Tests/OperationIdTests.cs:8](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.Core.Tests/OperationIdTests.cs#L8) | `public void When_generating_operation_ids_then_all_are_set()` |

Full lexical records (11) and complete listed paths are in [inventory.json](evidence/inventory.json). A display limit does not remove omitted records from scope.

## Capability ownership

| Package | Retained capability | Proposed contract names |
|---|---|---|
| WP-01 | Document object model and dialects | OpenApiDocument; Schema; Operation; Dialect |
| WP-02 | Readers writers and diagnostics | DocumentReader; DocumentWriter; Diagnostic |
| WP-03 | Reference resolution and workspaces | ReferenceId; DocumentWorkspace; ResolutionPolicy |
| WP-04 | Validation transformations and visitors | ValidationRule; DocumentVisitor; VersionConverter |
| WP-05 | Diff utilities and conformance corpus | DocumentDiff; CompatibilityFinding; RoundTripCase |
| WP-06 | NSwag schema and endpoint generation | SchemaGenerator; EndpointDescription; DocumentProcessor |
| WP-07 | Java TypeScript and retained language generators | ClientGenerator; GeneratorSettings; GeneratedArtifact |
| WP-08 | CLI build integration and Studio tooling | NswagDocument; GenerationCommand; StudioProject |


Map every observed source module/member onto one of these packages or a new explicitly retained package during E02. Structural listing is complete only to the scope stated above; behavioral analysis is sampled.
