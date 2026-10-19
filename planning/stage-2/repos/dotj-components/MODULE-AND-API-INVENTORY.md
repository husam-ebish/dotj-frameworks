# DJ-047 .j Components: module and API inventory

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

| Observed item | Count | Interpretation |
|---|---|---|
| Listed blob paths | 3410 | recursive complete |
| Project-definition paths | 11 | Files, not restored packages |
| API-definition/ref paths | 0 | Candidate declarations, not a complete public API census |
| Test/fixture candidate paths | 485 | Lexical path classification, not runnable test count |
| Sampled text files | 9 | Metadata plus selected API/implementation/tests |
| Lexical public/protected declarations | 17 | May include test helpers; not semantic API count |
| Lexical test-method candidates | 11 | Attribute inference only; no test discovery or execution |

## Extraction method and remaining closure

The tree supplies path identity. Project suffixes identify structural module candidates. Public/protected lines and test-like methods are extracted lexically from sampled files; multiline declarations, conditional compilation, generated code, extension methods, overload relationships and fixture parameter expansion require compiler-aware extraction. E02 must evaluate every target framework/configuration, generated source and conditional reference. Unassigned members remain retained scope, never implicitly removed.

## Observed project/module ledger

| Pinned path | Role candidate | Disposition |
|---|---|---|
| [Radzen.Blazor.Api.Generator/Radzen.Blazor.Api.Generator.csproj](https://github.com/radzenhq/radzen-blazor/blob/47709dc6fedfd92d66266017a0b50e0d327fa2c1/Radzen.Blazor.Api.Generator/Radzen.Blazor.Api.Generator.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [Radzen.Blazor.Api/Radzen.Blazor.Api.csproj](https://github.com/radzenhq/radzen-blazor/blob/47709dc6fedfd92d66266017a0b50e0d327fa2c1/Radzen.Blazor.Api/Radzen.Blazor.Api.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [Radzen.Blazor.Tests/Radzen.Blazor.Tests.csproj](https://github.com/radzenhq/radzen-blazor/blob/47709dc6fedfd92d66266017a0b50e0d327fa2c1/Radzen.Blazor.Tests/Radzen.Blazor.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [Radzen.Blazor.TrimRuntimeTest/Radzen.Blazor.TrimRuntimeTest.csproj](https://github.com/radzenhq/radzen-blazor/blob/47709dc6fedfd92d66266017a0b50e0d327fa2c1/Radzen.Blazor.TrimRuntimeTest/Radzen.Blazor.TrimRuntimeTest.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [Radzen.Blazor.TrimTest.Models/Radzen.Blazor.TrimTest.Models.csproj](https://github.com/radzenhq/radzen-blazor/blob/47709dc6fedfd92d66266017a0b50e0d327fa2c1/Radzen.Blazor.TrimTest.Models/Radzen.Blazor.TrimTest.Models.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [Radzen.Blazor.TrimTest/Radzen.Blazor.TrimTest.csproj](https://github.com/radzenhq/radzen-blazor/blob/47709dc6fedfd92d66266017a0b50e0d327fa2c1/Radzen.Blazor.TrimTest/Radzen.Blazor.TrimTest.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [Radzen.Blazor/Radzen.Blazor.csproj](https://github.com/radzenhq/radzen-blazor/blob/47709dc6fedfd92d66266017a0b50e0d327fa2c1/Radzen.Blazor/Radzen.Blazor.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [RadzenBlazorDemos.Host/RadzenBlazorDemos.Host.csproj](https://github.com/radzenhq/radzen-blazor/blob/47709dc6fedfd92d66266017a0b50e0d327fa2c1/RadzenBlazorDemos.Host/RadzenBlazorDemos.Host.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [RadzenBlazorDemos.Server/RadzenBlazorDemos.Server.csproj](https://github.com/radzenhq/radzen-blazor/blob/47709dc6fedfd92d66266017a0b50e0d327fa2c1/RadzenBlazorDemos.Server/RadzenBlazorDemos.Server.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [RadzenBlazorDemos.Tools/RadzenBlazorDemos.Tools.csproj](https://github.com/radzenhq/radzen-blazor/blob/47709dc6fedfd92d66266017a0b50e0d327fa2c1/RadzenBlazorDemos.Tools/RadzenBlazorDemos.Tools.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [RadzenBlazorDemos/RadzenBlazorDemos.csproj](https://github.com/radzenhq/radzen-blazor/blob/47709dc6fedfd92d66266017a0b50e0d327fa2c1/RadzenBlazorDemos/RadzenBlazorDemos.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |

## Sampled declaration candidates

| Source | Declaration candidate |
|---|---|
| [Radzen.Blazor/MD5.cs:10](https://github.com/radzenhq/radzen-blazor/blob/47709dc6fedfd92d66266017a0b50e0d327fa2c1/Radzen.Blazor/MD5.cs#L10) | `public class MD5` |
| [Radzen.Blazor/MD5.cs:50](https://github.com/radzenhq/radzen-blazor/blob/47709dc6fedfd92d66266017a0b50e0d327fa2c1/Radzen.Blazor/MD5.cs#L50) | `public static uint leftRotate(uint x, int c)` |
| [Radzen.Blazor/MD5.cs:61](https://github.com/radzenhq/radzen-blazor/blob/47709dc6fedfd92d66266017a0b50e0d327fa2c1/Radzen.Blazor/MD5.cs#L61) | `public static string Calculate(byte[] input)` |
| [Radzen.Blazor/Size.cs:6](https://github.com/radzenhq/radzen-blazor/blob/47709dc6fedfd92d66266017a0b50e0d327fa2c1/Radzen.Blazor/Size.cs#L6) | `public enum InputSize` |
| [Radzen.Blazor.Tests/FabTests.cs:6](https://github.com/radzenhq/radzen-blazor/blob/47709dc6fedfd92d66266017a0b50e0d327fa2c1/Radzen.Blazor.Tests/FabTests.cs#L6) | `public class FabTests` |
| [Radzen.Blazor.Tests/FabTests.cs:9](https://github.com/radzenhq/radzen-blazor/blob/47709dc6fedfd92d66266017a0b50e0d327fa2c1/Radzen.Blazor.Tests/FabTests.cs#L9) | `public void Fab_Renders_WithClassName()` |
| [Radzen.Blazor.Tests/FabTests.cs:19](https://github.com/radzenhq/radzen-blazor/blob/47709dc6fedfd92d66266017a0b50e0d327fa2c1/Radzen.Blazor.Tests/FabTests.cs#L19) | `public void Fab_Renders_IconParameter()` |
| [Radzen.Blazor.Tests/FabTests.cs:31](https://github.com/radzenhq/radzen-blazor/blob/47709dc6fedfd92d66266017a0b50e0d327fa2c1/Radzen.Blazor.Tests/FabTests.cs#L31) | `public void Fab_DefaultSize_IsLarge()` |
| [Radzen.Blazor.Tests/FabTests.cs:40](https://github.com/radzenhq/radzen-blazor/blob/47709dc6fedfd92d66266017a0b50e0d327fa2c1/Radzen.Blazor.Tests/FabTests.cs#L40) | `public void Fab_Renders_IconOnly_Class()` |
| [Radzen.Blazor.Tests/FabTests.cs:52](https://github.com/radzenhq/radzen-blazor/blob/47709dc6fedfd92d66266017a0b50e0d327fa2c1/Radzen.Blazor.Tests/FabTests.cs#L52) | `public void Fab_Renders_ButtonStyle()` |
| [Radzen.Blazor.Tests/FabTests.cs:64](https://github.com/radzenhq/radzen-blazor/blob/47709dc6fedfd92d66266017a0b50e0d327fa2c1/Radzen.Blazor.Tests/FabTests.cs#L64) | `public void Fab_Renders_Variant()` |
| [Radzen.Blazor.Tests/FabTests.cs:76](https://github.com/radzenhq/radzen-blazor/blob/47709dc6fedfd92d66266017a0b50e0d327fa2c1/Radzen.Blazor.Tests/FabTests.cs#L76) | `public void Fab_Renders_DisabledState()` |
| [Radzen.Blazor.Tests/FabTests.cs:88](https://github.com/radzenhq/radzen-blazor/blob/47709dc6fedfd92d66266017a0b50e0d327fa2c1/Radzen.Blazor.Tests/FabTests.cs#L88) | `public void Fab_Renders_TextParameter()` |
| [Radzen.Blazor.Tests/FabTests.cs:100](https://github.com/radzenhq/radzen-blazor/blob/47709dc6fedfd92d66266017a0b50e0d327fa2c1/Radzen.Blazor.Tests/FabTests.cs#L100) | `public void Fab_Renders_Shade()` |
| [Radzen.Blazor.Tests/FabTests.cs:112](https://github.com/radzenhq/radzen-blazor/blob/47709dc6fedfd92d66266017a0b50e0d327fa2c1/Radzen.Blazor.Tests/FabTests.cs#L112) | `public void Fab_NotVisible_DoesNotRender()` |
| [Radzen.Blazor.Tests/MD5Tests.cs:6](https://github.com/radzenhq/radzen-blazor/blob/47709dc6fedfd92d66266017a0b50e0d327fa2c1/Radzen.Blazor.Tests/MD5Tests.cs#L6) | `public class MD5Tests` |
| [Radzen.Blazor.Tests/MD5Tests.cs:22](https://github.com/radzenhq/radzen-blazor/blob/47709dc6fedfd92d66266017a0b50e0d327fa2c1/Radzen.Blazor.Tests/MD5Tests.cs#L22) | `public void InputsAroundThePaddingBoundaryHashLikeRfc1321(int length, string expected)` |

Full lexical records (17) and complete listed paths are in [inventory.json](evidence/inventory.json). A display limit does not remove omitted records from scope.

## Capability ownership

| Package | Retained capability | Internal planning labels; public names come from source |
|---|---|---|
| WP-01 | Component API and rendering | ComponentDescriptor; Parameter; RenderState |
| WP-02 | Forms input and validation | InputState; EditContext; ValidationMessage |
| WP-03 | Tables grids and data interaction | GridState; SortDescriptor; SelectionModel |
| WP-04 | Themes dialogs navigation and assets | Theme; DialogResult; NavigationItem; AssetManifest |
| WP-05 | Browser interop accessibility and coverage | BrowserAdapter; AccessibilityCase; ComponentMatrix |
| WP-06 | Charts scheduler upload and designer boundary | ChartSeries; SchedulerView; UploadSession; ComponentScope |


Map every observed source module/member onto one of these packages or a new explicitly retained package during E02. Structural listing is complete only to the scope stated above; behavioral analysis is sampled.
