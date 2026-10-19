# DJ-011 .j Containers: module and API inventory

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

| Observed item | Count | Interpretation |
|---|---|---|
| Listed blob paths | 1941 | recursive complete |
| Project-definition paths | 14 | Files, not restored packages |
| API-definition/ref paths | 0 | Candidate declarations, not a complete public API census |
| Test/fixture candidate paths | 766 | Lexical path classification, not runnable test count |
| Sampled text files | 10 | Metadata plus selected API/implementation/tests |
| Lexical public/protected declarations | 21 | May include test helpers; not semantic API count |
| Lexical test-method candidates | 12 | Attribute inference only; no test discovery or execution |

## Extraction method and remaining closure

The tree supplies path identity. Project suffixes identify structural module candidates. Public/protected lines and test-like methods are extracted lexically from sampled files; multiline declarations, conditional compilation, generated code, extension methods, overload relationships and fixture parameter expansion require compiler-aware extraction. E02 must evaluate every target framework/configuration, generated source and conditional reference. Unassigned members remain retained scope, never implicitly removed.

## Observed project/module ledger

| Pinned path | Role candidate | Disposition |
|---|---|---|
| [eng/shared/Microsoft.DotNet.Docker.Shared.csproj](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/eng/shared/Microsoft.DotNet.Docker.Shared.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [eng/update-dependencies/update-dependencies.csproj](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/eng/update-dependencies/update-dependencies.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/AspNetCoreNativeAot/AspNetCoreNativeAot.csproj](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/samples/AspNetCoreNativeAot/AspNetCoreNativeAot.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/AspNetCoreRazorApp/AspNetCoreRazorApp/AspNetCoreRazorApp.csproj](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/samples/AspNetCoreRazorApp/AspNetCoreRazorApp/AspNetCoreRazorApp.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/ConsoleApp/ConsoleApp.csproj](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/samples/ConsoleApp/ConsoleApp.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/ConsoleAppSelfContained/ConsoleAppSelfContained.csproj](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/samples/ConsoleAppSelfContained/ConsoleAppSelfContained.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/ConsoleAppWithGlobalization/ConsoleAppWithGlobalization.csproj](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/samples/ConsoleAppWithGlobalization/ConsoleAppWithGlobalization.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/MultiProjectApp/LibBar/LibBar.csproj](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/samples/MultiProjectApp/LibBar/LibBar.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/MultiProjectApp/LibFoo/LibFoo.csproj](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/samples/MultiProjectApp/LibFoo/LibFoo.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/MultiProjectApp/MultiProjectApp/MultiProjectApp.csproj](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/samples/MultiProjectApp/MultiProjectApp/MultiProjectApp.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [samples/MultiProjectApp/Tests/Tests.csproj](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/samples/MultiProjectApp/Tests/Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [tests/Microsoft.DotNet.Docker.Tests/Microsoft.DotNet.Docker.Tests.csproj](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/tests/Microsoft.DotNet.Docker.Tests/Microsoft.DotNet.Docker.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [tests/Microsoft.DotNet.Docker.Tests/TestAppArtifacts/otlptestlistener/OtlpTestListener/OtlpTestListener.csproj](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/tests/Microsoft.DotNet.Docker.Tests/TestAppArtifacts/otlptestlistener/OtlpTestListener/OtlpTestListener.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [tests/UpdateDependencies.Tests/UpdateDependencies.Tests.csproj](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/tests/UpdateDependencies.Tests/UpdateDependencies.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |

## Sampled declaration candidates

| Source | Declaration candidate |
|---|---|
| [tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs:26](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs#L26) | `public class SdkImageTests : ProductImageTests` |
| [tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs:46](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs#L46) | `public SdkImageTests(ITestOutputHelper outputHelper)` |
| [tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs:51](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs#L51) | `protected override DotNetImageRepo ImageRepo => DotNetImageRepo.SDK;` |
| [tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs:53](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs#L53) | `public static IEnumerable<object[]> GetImageData()` |
| [tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs:62](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs#L62) | `public async void VerifyBlazorWasmScenario(ProductImageData imageData)` |
| [tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs:91](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs#L91) | `public void VerifyInsecureFiles(ProductImageData imageData)` |
| [tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs:98](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs#L98) | `public void VerifyNoSasToken(ProductImageData imageData)` |
| [tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs:105](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs#L105) | `public void VerifyEnvironmentVariables(ProductImageData imageData)` |
| [tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs:142](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs#L142) | `public async Task VerifyDotnetFolderContents(ProductImageData imageData)` |
| [tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs:174](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs#L174) | `public void VerifyInstalledPackages(ProductImageData imageData)` |
| [tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs:181](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs#L181) | `public void VerifyDefaultUser(ProductImageData imageData)` |
| [tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs:191](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs#L191) | `public void VerifyGitInstallation(ProductImageData imageData)` |
| [tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs:204](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs#L204) | `public void VerifyTarInstallation(ProductImageData imageData)` |
| [tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs:219](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs#L219) | `public void VerifyDnxInstallation(ProductImageData imageData)` |
| [tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs:407](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs#L407) | `public string Path { get; init; }` |
| [tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs:408](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs#L408) | `public string Sha512 { get; init; }` |
| [tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs:410](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/tests/Microsoft.DotNet.Docker.Tests/SdkImageTests.cs#L410) | `public SdkContentFileInfo(string path, string sha512)` |
| [tests/Microsoft.DotNet.Docker.Tests/TestDataTests.cs:16](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/tests/Microsoft.DotNet.Docker.Tests/TestDataTests.cs#L16) | `public class TestDataTests(ITestOutputHelper outputHelper)` |
| [tests/Microsoft.DotNet.Docker.Tests/TestDataTests.cs:24](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/tests/Microsoft.DotNet.Docker.Tests/TestDataTests.cs#L24) | `public static readonly IEnumerable<object[]> ImageRepos =` |
| [tests/Microsoft.DotNet.Docker.Tests/TestDataTests.cs:32](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/tests/Microsoft.DotNet.Docker.Tests/TestDataTests.cs#L32) | `public void VerifyTestData(DotNetImageRepo imageRepo)` |
| [tests/Microsoft.DotNet.Docker.Tests/TestDataTests.cs:90](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/tests/Microsoft.DotNet.Docker.Tests/TestDataTests.cs#L90) | `public void VerifyTestDataDockerfilePaths(DotNetImageRepo imageRepo)` |

Full lexical records (21) and complete listed paths are in [inventory.json](evidence/inventory.json). A display limit does not remove omitted records from scope.

## Capability ownership

| Package | Retained capability | Internal planning labels; public names come from source |
|---|---|---|
| WP-01 | Image families and binary inputs | ImageRole; JdkBinaryLock; BaseImageLock |
| WP-02 | Reproducible image assembly | LayerPlan; RuntimeModuleSet; ImageManifest |
| WP-03 | Runtime behavior and hardening | ContainerLaunchContract; HealthProbe; ShutdownPolicy |
| WP-04 | Architecture and Windows tracks | PlatformManifest; NativeInventory; SmokeMatrix |
| WP-05 | Publishing and patch maintenance | Sbom; RebuildRecord; ImageSupportPolicy |


Map every observed source module/member onto one of these packages or a new explicitly retained package during E02. Structural listing is complete only to the scope stated above; behavioral analysis is sampled.
