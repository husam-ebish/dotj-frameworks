# DJ-043 .j Avalonia: dependencies and licenses

## Proposed Java dependencies

core,toolkit

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: JVM plus candidate native rendering/font bindings; no JavaFX substitution.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|
| PackageVersion | Appium.WebDriver | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | Avalonia.Angle.Windows.Natives | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | Avalonia.BuildServices | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | AvaloniaUI.DiagnosticsSupport | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | BenchmarkDotNet | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | CommunityToolkit.Mvvm | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | Dotnet.Bundle | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | GtkSharp | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | HarfBuzzSharp | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | HarfBuzzSharp.NativeAssets.Linux | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | HarfBuzzSharp.NativeAssets.WebAssembly | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | MicroCom.CodeGenerator | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | MicroCom.CodeGenerator.MSBuild | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | MicroCom.CodeGenerator.Roslyn | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | MicroCom.Runtime | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | Microsoft.Bcl.AsyncInterfaces | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | Microsoft.Build.Framework | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | Microsoft.Build.Utilities.Core | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.Analyzers | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp.Analyzer.Testing | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp.CodeFix.Testing | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp.Workspaces | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.VisualBasic | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.Workspaces.Common | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | Microsoft.CSharp | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | Microsoft.NET.Test.Sdk | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | Microsoft.Reactive.Testing | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | Microsoft.Testing.Extensions.TrxReport | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | Microsoft.Windows.CsWin32 | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | Microsoft.Windows.SDK.BuildTools | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | Microsoft.WindowsAppSDK | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | Mono.Cecil | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | MonoMac.NetStandard | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | Moq | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | Nito.AsyncEx.Context | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | NuGet.Protocol | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | Nuke.Common | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | Numerge | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | NUnit | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | NUnit3TestAdapter | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | NWayland | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | NWayland.Server | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | Quamotion.RemoteViewing | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | SharpCompress | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | Silk.NET.Direct3D.Compilers | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | Silk.NET.Direct3D11 | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | Silk.NET.Vulkan | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | Silk.NET.Vulkan.Extensions.EXT | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | Silk.NET.Vulkan.Extensions.KHR | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | SkiaSharp | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | SkiaSharp.NativeAssets.Linux | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | SkiaSharp.NativeAssets.WebAssembly | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | System.ComponentModel.Annotations | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | System.Diagnostics.DiagnosticSource | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | System.Memory | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | System.Net.Http | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | System.Numerics.Vectors | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | System.Reactive | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | System.Reflection.Emit | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | System.Runtime.CompilerServices.Unsafe | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | System.Security.Cryptography.Pkcs | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | System.Text.Json | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | System.Text.RegularExpressions | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | Tmds.DBus.Protocol | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | unofficial.mesa.softwarerenderer | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | Tmds.DBus.Generator | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | Xamarin.AndroidX.AppCompat | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | Xamarin.AndroidX.Core.SplashScreen | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | Xamarin.AndroidX.DocumentFile | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | Xamarin.AndroidX.Window | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | xunit.runner.visualstudio | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | Xunit.StaFact | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | xunit.v3.extensibility.core | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| PackageVersion | xunit.v3.mtp-v2 | [Directory.Packages.props](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/Directory.Packages.props) |
| ProjectReference | ..\..\..\packages\Avalonia\Avalonia.csproj | [src/Android/Avalonia.Android/Avalonia.Android.csproj](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/src/Android/Avalonia.Android/Avalonia.Android.csproj) |
| PackageReference | Xamarin.AndroidX.AppCompat | [src/Android/Avalonia.Android/Avalonia.Android.csproj](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/src/Android/Avalonia.Android/Avalonia.Android.csproj) |
| PackageReference | Xamarin.AndroidX.Window | [src/Android/Avalonia.Android/Avalonia.Android.csproj](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/src/Android/Avalonia.Android/Avalonia.Android.csproj) |
| PackageReference | Xamarin.AndroidX.DocumentFile | [src/Android/Avalonia.Android/Avalonia.Android.csproj](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/src/Android/Avalonia.Android/Avalonia.Android.csproj) |
| ProjectReference | ..\..\Avalonia.Base\Avalonia.Base.csproj | [src/Android/Avalonia.Android/Avalonia.Android.csproj](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/src/Android/Avalonia.Android/Avalonia.Android.csproj) |
| ProjectReference | ..\..\HarfBuzz\Avalonia.HarfBuzz\Avalonia.HarfBuzz.csproj | [src/Android/Avalonia.Android/Avalonia.Android.csproj](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/src/Android/Avalonia.Android/Avalonia.Android.csproj) |
| ProjectReference | ..\..\Skia\Avalonia.Skia\Avalonia.Skia.csproj | [src/Android/Avalonia.Android/Avalonia.Android.csproj](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/src/Android/Avalonia.Android/Avalonia.Android.csproj) |
| PackageReference | Dotnet.Bundle | [samples/IntegrationTestApp/IntegrationTestApp.csproj](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/samples/IntegrationTestApp/IntegrationTestApp.csproj) |
| PackageReference | MonoMac.NetStandard | [samples/IntegrationTestApp/IntegrationTestApp.csproj](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/samples/IntegrationTestApp/IntegrationTestApp.csproj) |
| ProjectReference | ..\..\src\Avalonia.Themes.Fluent\Avalonia.Themes.Fluent.csproj | [samples/IntegrationTestApp/IntegrationTestApp.csproj](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/samples/IntegrationTestApp/IntegrationTestApp.csproj) |
| ProjectReference | ..\..\src\Avalonia.Fonts.Inter\Avalonia.Fonts.Inter.csproj | [samples/IntegrationTestApp/IntegrationTestApp.csproj](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/samples/IntegrationTestApp/IntegrationTestApp.csproj) |
| ProjectReference | ..\MiniMvvm\MiniMvvm.csproj | [samples/IntegrationTestApp/IntegrationTestApp.csproj](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/samples/IntegrationTestApp/IntegrationTestApp.csproj) |


## License evidence and eligibility gate

Observed metadata hint: `unavailable`.

Root licence.md contains MIT text; NOTICE contains separate third-party notices. Root license alone does not clear fonts, native binaries, Skia/HarfBuzz, optional commercial backends or all assets.

| Retrieved notice/license | Immutable source |
|---|---|
| [NOTICE.md](evidence/notices/NOTICE.md) | [NOTICE.md](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/NOTICE.md) |
| [licence.md](evidence/notices/licence.md) | [licence.md](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/licence.md) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-avalonia-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
