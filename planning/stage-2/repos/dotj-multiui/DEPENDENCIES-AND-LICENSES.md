# DJ-042 .j MultiUI: dependencies and licenses

## Proposed Java dependencies

core,toolkit;presentation(optional)

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: Android SDK/toolchain; Apple SDK/Xcode and Objective-C/Swift bridge or AOT research; Windows native bindings.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|
| PackageReference | Microsoft.Net.Compilers.Toolset | [Directory.Build.props](https://github.com/dotnet/maui/blob/3a7d72870b9c2ed006de7268a6257ae039cb7f99/Directory.Build.props) |
| PackageReference | MemoryAnalyzers | [src/Core/src/Core.csproj](https://github.com/dotnet/maui/blob/3a7d72870b9c2ed006de7268a6257ae039cb7f99/src/Core/src/Core.csproj) |
| PackageReference | Microsoft.Extensions.Configuration | [src/Core/src/Core.csproj](https://github.com/dotnet/maui/blob/3a7d72870b9c2ed006de7268a6257ae039cb7f99/src/Core/src/Core.csproj) |
| PackageReference | Microsoft.Extensions.DependencyInjection | [src/Core/src/Core.csproj](https://github.com/dotnet/maui/blob/3a7d72870b9c2ed006de7268a6257ae039cb7f99/src/Core/src/Core.csproj) |
| PackageReference | Microsoft.Extensions.Logging | [src/Core/src/Core.csproj](https://github.com/dotnet/maui/blob/3a7d72870b9c2ed006de7268a6257ae039cb7f99/src/Core/src/Core.csproj) |
| PackageReference | Microsoft.Extensions.Logging.Abstractions | [src/Core/src/Core.csproj](https://github.com/dotnet/maui/blob/3a7d72870b9c2ed006de7268a6257ae039cb7f99/src/Core/src/Core.csproj) |
| PackageReference | Microsoft.Extensions.Hosting.Abstractions | [src/Core/src/Core.csproj](https://github.com/dotnet/maui/blob/3a7d72870b9c2ed006de7268a6257ae039cb7f99/src/Core/src/Core.csproj) |
| ProjectReference | ..\..\Graphics\src\Graphics\Graphics.csproj | [src/Core/src/Core.csproj](https://github.com/dotnet/maui/blob/3a7d72870b9c2ed006de7268a6257ae039cb7f99/src/Core/src/Core.csproj) |
| PackageReference | System.Numerics.Vectors | [src/Core/src/Core.csproj](https://github.com/dotnet/maui/blob/3a7d72870b9c2ed006de7268a6257ae039cb7f99/src/Core/src/Core.csproj) |
| PackageReference | System.Text.Json | [src/Core/src/Core.csproj](https://github.com/dotnet/maui/blob/3a7d72870b9c2ed006de7268a6257ae039cb7f99/src/Core/src/Core.csproj) |
| PackageReference | Microsoft.WindowsAppSDK | [src/Core/src/Core.csproj](https://github.com/dotnet/maui/blob/3a7d72870b9c2ed006de7268a6257ae039cb7f99/src/Core/src/Core.csproj) |
| PackageReference | Microsoft.Web.WebView2 | [src/Core/src/Core.csproj](https://github.com/dotnet/maui/blob/3a7d72870b9c2ed006de7268a6257ae039cb7f99/src/Core/src/Core.csproj) |
| PackageReference | Microsoft.Windows.SDK.BuildTools | [src/Core/src/Core.csproj](https://github.com/dotnet/maui/blob/3a7d72870b9c2ed006de7268a6257ae039cb7f99/src/Core/src/Core.csproj) |
| PackageReference | Microsoft.Graphics.Win2D | [src/Core/src/Core.csproj](https://github.com/dotnet/maui/blob/3a7d72870b9c2ed006de7268a6257ae039cb7f99/src/Core/src/Core.csproj) |
| ProjectReference | ..\..\Graphics\src\Graphics.Win2D\Graphics.Win2D.csproj | [src/Core/src/Core.csproj](https://github.com/dotnet/maui/blob/3a7d72870b9c2ed006de7268a6257ae039cb7f99/src/Core/src/Core.csproj) |
| PackageReference | Xamarin.Android.Glide | [src/Core/src/Core.csproj](https://github.com/dotnet/maui/blob/3a7d72870b9c2ed006de7268a6257ae039cb7f99/src/Core/src/Core.csproj) |
| PackageReference | Xamarin.AndroidX.Lifecycle.LiveData | [src/Core/src/Core.csproj](https://github.com/dotnet/maui/blob/3a7d72870b9c2ed006de7268a6257ae039cb7f99/src/Core/src/Core.csproj) |
| PackageReference | Xamarin.Google.Android.Material | [src/Core/src/Core.csproj](https://github.com/dotnet/maui/blob/3a7d72870b9c2ed006de7268a6257ae039cb7f99/src/Core/src/Core.csproj) |
| PackageReference | Xamarin.AndroidX.SwipeRefreshLayout | [src/Core/src/Core.csproj](https://github.com/dotnet/maui/blob/3a7d72870b9c2ed006de7268a6257ae039cb7f99/src/Core/src/Core.csproj) |
| PackageReference | Xamarin.AndroidX.Navigation.UI | [src/Core/src/Core.csproj](https://github.com/dotnet/maui/blob/3a7d72870b9c2ed006de7268a6257ae039cb7f99/src/Core/src/Core.csproj) |
| PackageReference | Xamarin.AndroidX.Navigation.Fragment | [src/Core/src/Core.csproj](https://github.com/dotnet/maui/blob/3a7d72870b9c2ed006de7268a6257ae039cb7f99/src/Core/src/Core.csproj) |
| PackageReference | Xamarin.AndroidX.Navigation.Runtime | [src/Core/src/Core.csproj](https://github.com/dotnet/maui/blob/3a7d72870b9c2ed006de7268a6257ae039cb7f99/src/Core/src/Core.csproj) |
| PackageReference | Xamarin.AndroidX.Navigation.Common | [src/Core/src/Core.csproj](https://github.com/dotnet/maui/blob/3a7d72870b9c2ed006de7268a6257ae039cb7f99/src/Core/src/Core.csproj) |
| PackageReference | Tizen.UIExtensions.NUI | [src/Core/src/Core.csproj](https://github.com/dotnet/maui/blob/3a7d72870b9c2ed006de7268a6257ae039cb7f99/src/Core/src/Core.csproj) |
| ProjectReference | ..\..\Graphics\src\Graphics.Skia\Graphics.Skia.csproj | [src/Core/src/Core.csproj](https://github.com/dotnet/maui/blob/3a7d72870b9c2ed006de7268a6257ae039cb7f99/src/Core/src/Core.csproj) |
| ProjectReference | ..\..\Essentials\src\Essentials.csproj | [src/Core/src/Core.csproj](https://github.com/dotnet/maui/blob/3a7d72870b9c2ed006de7268a6257ae039cb7f99/src/Core/src/Core.csproj) |
| ProjectReference | ..\..\Graphics\src\Graphics\Graphics.csproj | [src/Core/src/Core.csproj](https://github.com/dotnet/maui/blob/3a7d72870b9c2ed006de7268a6257ae039cb7f99/src/Core/src/Core.csproj) |
| PackageReference | Microsoft.TypeScript.MSBuild | [src/Core/src/Core.csproj](https://github.com/dotnet/maui/blob/3a7d72870b9c2ed006de7268a6257ae039cb7f99/src/Core/src/Core.csproj) |
| PackageReference | xunit | [src/TestUtils/src/TestUtils/TestUtils.csproj](https://github.com/dotnet/maui/blob/3a7d72870b9c2ed006de7268a6257ae039cb7f99/src/TestUtils/src/TestUtils/TestUtils.csproj) |


## License evidence and eligibility gate

Observed metadata hint: `unavailable`.

Observed root metadata/license text is evidence, not a completed eligibility review. Resolve conditional/transitive dependencies, embedded assets, generated inputs and redistributable binaries before source reuse or release.

| Retrieved notice/license | Immutable source |
|---|---|
| [LICENSE.txt](evidence/notices/LICENSE.txt) | [LICENSE.txt](https://github.com/dotnet/maui/blob/3a7d72870b9c2ed006de7268a6257ae039cb7f99/LICENSE.txt) |
| [THIRD-PARTY-NOTICES.TXT](evidence/notices/THIRD-PARTY-NOTICES.TXT) | [THIRD-PARTY-NOTICES.TXT](https://github.com/dotnet/maui/blob/3a7d72870b9c2ed006de7268a6257ae039cb7f99/THIRD-PARTY-NOTICES.TXT) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-multiui-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
