# DJ-040 .j Presentation: dependencies and licenses

## Proposed Java dependencies

core,toolkit

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: JDK host/runtime plus optional FFM/JNI Win32/DirectWrite/Direct3D bindings; AWT may bootstrap a window only.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|
| PackageReference | System.Security.Permissions | [src/Microsoft.DotNet.Wpf/src/System.Xaml/System.Xaml.csproj](https://github.com/dotnet/wpf/blob/65d15adece1df9a73e3d1abc11f8bbf99e9fc7a9/src/Microsoft.DotNet.Wpf/src/System.Xaml/System.Xaml.csproj) |
| PackageReference | System.Windows.Extensions | [src/Microsoft.DotNet.Wpf/src/System.Xaml/System.Xaml.csproj](https://github.com/dotnet/wpf/blob/65d15adece1df9a73e3d1abc11f8bbf99e9fc7a9/src/Microsoft.DotNet.Wpf/src/System.Xaml/System.Xaml.csproj) |
| ProjectReference | $(WpfSourceDir)System.Xaml\ref\System.Xaml-ref.csproj | [src/Microsoft.DotNet.Wpf/src/System.Xaml/System.Xaml.csproj](https://github.com/dotnet/wpf/blob/65d15adece1df9a73e3d1abc11f8bbf99e9fc7a9/src/Microsoft.DotNet.Wpf/src/System.Xaml/System.Xaml.csproj) |
| ProjectReference | $(WpfSourceDir)DirectWriteForwarder\DirectWriteForwarder.vcxproj | [src/Microsoft.DotNet.Wpf/tests/UnitTests/PresentationCore.Tests/PresentationCore.Tests.csproj](https://github.com/dotnet/wpf/blob/65d15adece1df9a73e3d1abc11f8bbf99e9fc7a9/src/Microsoft.DotNet.Wpf/tests/UnitTests/PresentationCore.Tests/PresentationCore.Tests.csproj) |
| ProjectReference | $(WpfSourceDir)PresentationCore\PresentationCore.csproj | [src/Microsoft.DotNet.Wpf/tests/UnitTests/PresentationCore.Tests/PresentationCore.Tests.csproj](https://github.com/dotnet/wpf/blob/65d15adece1df9a73e3d1abc11f8bbf99e9fc7a9/src/Microsoft.DotNet.Wpf/tests/UnitTests/PresentationCore.Tests/PresentationCore.Tests.csproj) |
| ProjectReference | $(WpfSourceDir)WindowsBase\WindowsBase.csproj | [src/Microsoft.DotNet.Wpf/tests/UnitTests/PresentationCore.Tests/PresentationCore.Tests.csproj](https://github.com/dotnet/wpf/blob/65d15adece1df9a73e3d1abc11f8bbf99e9fc7a9/src/Microsoft.DotNet.Wpf/tests/UnitTests/PresentationCore.Tests/PresentationCore.Tests.csproj) |
| ProjectReference | $(WpfSourceDir)System.Xaml\System.Xaml.csproj | [src/Microsoft.DotNet.Wpf/tests/UnitTests/PresentationCore.Tests/PresentationCore.Tests.csproj](https://github.com/dotnet/wpf/blob/65d15adece1df9a73e3d1abc11f8bbf99e9fc7a9/src/Microsoft.DotNet.Wpf/tests/UnitTests/PresentationCore.Tests/PresentationCore.Tests.csproj) |
| ProjectReference | $(WpfSourceDir)System.Windows.Primitives\System.Windows.Primitives.csproj | [src/Microsoft.DotNet.Wpf/tests/UnitTests/PresentationCore.Tests/PresentationCore.Tests.csproj](https://github.com/dotnet/wpf/blob/65d15adece1df9a73e3d1abc11f8bbf99e9fc7a9/src/Microsoft.DotNet.Wpf/tests/UnitTests/PresentationCore.Tests/PresentationCore.Tests.csproj) |
| ProjectReference | $(WpfSourceDir)Extensions\PresentationFramework-SystemDrawing\PresentationFramework-SystemDrawing.csproj | [src/Microsoft.DotNet.Wpf/tests/UnitTests/PresentationCore.Tests/PresentationCore.Tests.csproj](https://github.com/dotnet/wpf/blob/65d15adece1df9a73e3d1abc11f8bbf99e9fc7a9/src/Microsoft.DotNet.Wpf/tests/UnitTests/PresentationCore.Tests/PresentationCore.Tests.csproj) |
| PackageReference | AwesomeAssertions | [src/Microsoft.DotNet.Wpf/tests/UnitTests/PresentationCore.Tests/PresentationCore.Tests.csproj](https://github.com/dotnet/wpf/blob/65d15adece1df9a73e3d1abc11f8bbf99e9fc7a9/src/Microsoft.DotNet.Wpf/tests/UnitTests/PresentationCore.Tests/PresentationCore.Tests.csproj) |
| PackageReference | Moq | [src/Microsoft.DotNet.Wpf/tests/UnitTests/PresentationCore.Tests/PresentationCore.Tests.csproj](https://github.com/dotnet/wpf/blob/65d15adece1df9a73e3d1abc11f8bbf99e9fc7a9/src/Microsoft.DotNet.Wpf/tests/UnitTests/PresentationCore.Tests/PresentationCore.Tests.csproj) |
| PackageReference | xunit.stafact | [src/Microsoft.DotNet.Wpf/tests/UnitTests/PresentationCore.Tests/PresentationCore.Tests.csproj](https://github.com/dotnet/wpf/blob/65d15adece1df9a73e3d1abc11f8bbf99e9fc7a9/src/Microsoft.DotNet.Wpf/tests/UnitTests/PresentationCore.Tests/PresentationCore.Tests.csproj) |
| PackageReference | System.Configuration.ConfigurationManager | [src/Microsoft.DotNet.Wpf/tests/UnitTests/PresentationCore.Tests/PresentationCore.Tests.csproj](https://github.com/dotnet/wpf/blob/65d15adece1df9a73e3d1abc11f8bbf99e9fc7a9/src/Microsoft.DotNet.Wpf/tests/UnitTests/PresentationCore.Tests/PresentationCore.Tests.csproj) |
| PackageReference | System.Formats.Nrbf | [src/Microsoft.DotNet.Wpf/tests/UnitTests/PresentationCore.Tests/PresentationCore.Tests.csproj](https://github.com/dotnet/wpf/blob/65d15adece1df9a73e3d1abc11f8bbf99e9fc7a9/src/Microsoft.DotNet.Wpf/tests/UnitTests/PresentationCore.Tests/PresentationCore.Tests.csproj) |
| PackageReference | $(SystemIOPackagingPackage) | [src/Microsoft.DotNet.Wpf/tests/UnitTests/PresentationCore.Tests/PresentationCore.Tests.csproj](https://github.com/dotnet/wpf/blob/65d15adece1df9a73e3d1abc11f8bbf99e9fc7a9/src/Microsoft.DotNet.Wpf/tests/UnitTests/PresentationCore.Tests/PresentationCore.Tests.csproj) |
| PackageReference | System.Runtime.Serialization.Formatters | [src/Microsoft.DotNet.Wpf/tests/UnitTests/PresentationCore.Tests/PresentationCore.Tests.csproj](https://github.com/dotnet/wpf/blob/65d15adece1df9a73e3d1abc11f8bbf99e9fc7a9/src/Microsoft.DotNet.Wpf/tests/UnitTests/PresentationCore.Tests/PresentationCore.Tests.csproj) |
| PackageReference | System.Private.Windows.Core.TestUtilities | [src/Microsoft.DotNet.Wpf/tests/UnitTests/PresentationCore.Tests/PresentationCore.Tests.csproj](https://github.com/dotnet/wpf/blob/65d15adece1df9a73e3d1abc11f8bbf99e9fc7a9/src/Microsoft.DotNet.Wpf/tests/UnitTests/PresentationCore.Tests/PresentationCore.Tests.csproj) |
| PackageReference | $(SystemDrawingCommonPackage) | [src/Microsoft.DotNet.Wpf/tests/UnitTests/PresentationCore.Tests/PresentationCore.Tests.csproj](https://github.com/dotnet/wpf/blob/65d15adece1df9a73e3d1abc11f8bbf99e9fc7a9/src/Microsoft.DotNet.Wpf/tests/UnitTests/PresentationCore.Tests/PresentationCore.Tests.csproj) |


## License evidence and eligibility gate

Observed metadata hint: `unavailable`.

Observed root metadata/license text is evidence, not a completed eligibility review. Resolve conditional/transitive dependencies, embedded assets, generated inputs and redistributable binaries before source reuse or release.

| Retrieved notice/license | Immutable source |
|---|---|
| [LICENSE.TXT](evidence/notices/LICENSE.TXT) | [LICENSE.TXT](https://github.com/dotnet/wpf/blob/65d15adece1df9a73e3d1abc11f8bbf99e9fc7a9/LICENSE.TXT) |
| [THIRD-PARTY-NOTICES.TXT](evidence/notices/THIRD-PARTY-NOTICES.TXT) | [THIRD-PARTY-NOTICES.TXT](https://github.com/dotnet/wpf/blob/65d15adece1df9a73e3d1abc11f8bbf99e9fc7a9/THIRD-PARTY-NOTICES.TXT) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-presentation-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
