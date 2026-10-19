# DJ-046 .j Material: module and API inventory

| Observed item | Count | Interpretation |
|---|---|---|
| Listed blob paths | 3565 | recursive complete |
| Project-definition paths | 17 | Files, not restored packages |
| API-definition/ref paths | 0 | Candidate declarations, not a complete public API census |
| Test/fixture candidate paths | 347 | Lexical path classification, not runnable test count |
| Sampled text files | 9 | Metadata plus selected API/implementation/tests |
| Lexical public/protected declarations | 14 | May include test helpers; not semantic API count |
| Lexical test-method candidates | 9 | Attribute inference only; no test discovery or execution |

## Extraction method and remaining closure

The tree supplies path identity. Project suffixes identify structural module candidates. Public/protected lines and test-like methods are extracted lexically from sampled files; multiline declarations, conditional compilation, generated code, extension methods, overload relationships and fixture parameter expansion require compiler-aware extraction. E02 must evaluate every target framework/configuration, generated source and conditional reference. Unassigned members remain retained scope, never implicitly removed.

## Observed project/module ledger

| Pinned path | Role candidate | Disposition |
|---|---|---|
| [src/MudBlazor.Analyzers.CodeFixes/MudBlazor.Analyzers.CodeFixes.csproj](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor.Analyzers.CodeFixes/MudBlazor.Analyzers.CodeFixes.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/MudBlazor.Analyzers.TestComponents/MudBlazor.Analyzers.TestComponents.csproj](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor.Analyzers.TestComponents/MudBlazor.Analyzers.TestComponents.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/MudBlazor.Analyzers/MudBlazor.Analyzers.csproj](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor.Analyzers/MudBlazor.Analyzers.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/MudBlazor.Benchmarks/MudBlazor.Benchmarks.csproj](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor.Benchmarks/MudBlazor.Benchmarks.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [src/MudBlazor.Docs.Compiler/MudBlazor.Docs.Compiler.csproj](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor.Docs.Compiler/MudBlazor.Docs.Compiler.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/MudBlazor.Docs.Server/MudBlazor.Docs.Server.csproj](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor.Docs.Server/MudBlazor.Docs.Server.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/MudBlazor.Docs.Wasm/MudBlazor.Docs.Wasm.csproj](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor.Docs.Wasm/MudBlazor.Docs.Wasm.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/MudBlazor.Docs.WasmHost/MudBlazor.Docs.WasmHost.csproj](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor.Docs.WasmHost/MudBlazor.Docs.WasmHost.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/MudBlazor.Docs/MudBlazor.Docs.csproj](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor.Docs/MudBlazor.Docs.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/MudBlazor.Examples.Data/MudBlazor.Examples.Data.csproj](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor.Examples.Data/MudBlazor.Examples.Data.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [src/MudBlazor.UnitTests.Analyzers/MudBlazor.UnitTests.Analyzers.csproj](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor.UnitTests.Analyzers/MudBlazor.UnitTests.Analyzers.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/MudBlazor.UnitTests.Docs.Generator/MudBlazor.UnitTests.Docs.Generator.csproj](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor.UnitTests.Docs.Generator/MudBlazor.UnitTests.Docs.Generator.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/MudBlazor.UnitTests.Docs/MudBlazor.UnitTests.Docs.csproj](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor.UnitTests.Docs/MudBlazor.UnitTests.Docs.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/MudBlazor.UnitTests.Shared/MudBlazor.UnitTests.Shared.csproj](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor.UnitTests.Shared/MudBlazor.UnitTests.Shared.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/MudBlazor.UnitTests.Viewer/MudBlazor.UnitTests.Viewer.csproj](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor.UnitTests.Viewer/MudBlazor.UnitTests.Viewer.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/MudBlazor.UnitTests/MudBlazor.UnitTests.csproj](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor.UnitTests/MudBlazor.UnitTests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/MudBlazor/MudBlazor.csproj](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor/MudBlazor.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |

## Sampled declaration candidates

| Source | Declaration candidate |
|---|---|
| [src/MudBlazor/Enums/Edge.cs:16](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor/Enums/Edge.cs#L16) | `public enum Edge` |
| [src/MudBlazor/Enums/Page.cs:10](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor/Enums/Page.cs#L10) | `public enum Page` |
| [tools/watch.cs:193](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/tools/watch.cs#L193) | `public required string BunVersion { get; init; }` |
| [src/MudBlazor.UnitTests/Components/FabTests.cs:11](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor.UnitTests/Components/FabTests.cs#L11) | `public class FabTests : BunitTest` |
| [src/MudBlazor.UnitTests/Components/FabTests.cs:17](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor.UnitTests/Components/FabTests.cs#L17) | `public void DefaultAppearance()` |
| [src/MudBlazor.UnitTests/Components/FabTests.cs:33](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor.UnitTests/Components/FabTests.cs#L33) | `public void VariantSetsClasses(Variant variant, string variantClass, string colorClass, bool hasLegacyColorClass)` |
| [src/MudBlazor.UnitTests/Components/FabTests.cs:51](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor.UnitTests/Components/FabTests.cs#L51) | `public void DisabledKeepsVariantClass(Variant variant, string variantClass)` |
| [src/MudBlazor.UnitTests/Components/FabTests.cs:66](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor.UnitTests/Components/FabTests.cs#L66) | `public void DisabledRemovesRipple()` |
| [src/MudBlazor.UnitTests/Components/FabTests.cs:78](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor.UnitTests/Components/FabTests.cs#L78) | `public void LabelExtendsFabBetweenIcons()` |
| [src/MudBlazor.UnitTests/Components/FabTests.cs:96](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor.UnitTests/Components/FabTests.cs#L96) | `public void RendersNoIconWhenNoneIsSet()` |
| [src/MudBlazor.UnitTests/Components/FabTests.cs:107](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor.UnitTests/Components/FabTests.cs#L107) | `public void DropShadowOffRemovesElevation()` |
| [src/MudBlazor.UnitTests/Components/CardTests.cs:13](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor.UnitTests/Components/CardTests.cs#L13) | `public class CardTests : BunitTest` |
| [src/MudBlazor.UnitTests/Components/CardTests.cs:16](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor.UnitTests/Components/CardTests.cs#L16) | `public async Task CardChildContent()` |
| [src/MudBlazor.UnitTests/Components/CardTests.cs:31](https://github.com/MudBlazor/MudBlazor/blob/f28086704d9d488c3c200e74ff960022af34a6ef/src/MudBlazor.UnitTests/Components/CardTests.cs#L31) | `public void CardMedia_Should_KeepUserSuppliedTitle()` |

Full lexical records (14) and complete listed paths are in [inventory.json](evidence/inventory.json). A display limit does not remove omitted records from scope.

## Capability ownership

| Package | Retained capability | Proposed contract names |
|---|---|---|
| WP-01 | MudBlazor component contracts and lifecycle | MaterialComponent; ComponentParameter; RenderState |
| WP-02 | Forms inputs and validation | FormContext; InputState; ValidationBinding |
| WP-03 | Tables grids and virtualization | GridState; FilterDefinition; SortDefinition; ItemKey |
| WP-04 | Dialogs overlays navigation and feedback | DialogHost; Overlay; Snackbar; NavigationState |
| WP-05 | Themes icons CSS and browser bridge | MaterialTheme; IconManifest; BrowserInterop |
| WP-06 | Accessibility examples and qualification | ComponentCoverage; AriaCase; VisualFixture |


Map every observed source module/member onto one of these packages or a new explicitly retained package during E02. Structural listing is complete only to the scope stated above; behavioral analysis is sampled.
