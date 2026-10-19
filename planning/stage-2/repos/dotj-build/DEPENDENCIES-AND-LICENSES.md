# DJ-005 .j Build: dependencies and licenses

## Proposed Java dependencies

core

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: XML streaming, ProcessBuilder, file hashing and executors; javac/jar bootstrap without Gradle or Maven framework dependencies.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|
| PackageVersion | Microsoft.Build.NuGetSdkResolver | [Directory.Packages.props](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.Collections | [Directory.Packages.props](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.Contracts | [Directory.Packages.props](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.PooledObjects | [Directory.Packages.props](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/Directory.Packages.props) |
| PackageVersion | Microsoft.DotNet.XUnitV3Extensions | [Directory.Packages.props](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/Directory.Packages.props) |
| PackageVersion | Microsoft.IO.Redist | [Directory.Packages.props](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/Directory.Packages.props) |
| PackageVersion | Microsoft.Net.Compilers.Toolset | [Directory.Packages.props](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/Directory.Packages.props) |
| PackageVersion | NuGet.Build.Tasks | [Directory.Packages.props](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/Directory.Packages.props) |
| PackageVersion | NuGet.Build.Tasks.Console | [Directory.Packages.props](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/Directory.Packages.props) |
| PackageVersion | NuGet.Frameworks | [Directory.Packages.props](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/Directory.Packages.props) |
| PackageVersion | System.CodeDom | [Directory.Packages.props](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/Directory.Packages.props) |
| PackageVersion | System.Collections.Immutable | [Directory.Packages.props](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/Directory.Packages.props) |
| PackageVersion | System.Configuration.ConfigurationManager | [Directory.Packages.props](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/Directory.Packages.props) |
| PackageVersion | System.Diagnostics.DiagnosticSource | [Directory.Packages.props](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/Directory.Packages.props) |
| PackageVersion | System.Diagnostics.EventLog | [Directory.Packages.props](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/Directory.Packages.props) |
| PackageVersion | System.Formats.Asn1 | [Directory.Packages.props](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/Directory.Packages.props) |
| PackageVersion | System.Formats.Nrbf | [Directory.Packages.props](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/Directory.Packages.props) |
| PackageVersion | System.Memory | [Directory.Packages.props](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/Directory.Packages.props) |
| PackageVersion | System.Reflection.Metadata | [Directory.Packages.props](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/Directory.Packages.props) |
| PackageVersion | System.Reflection.MetadataLoadContext | [Directory.Packages.props](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/Directory.Packages.props) |
| PackageVersion | System.Resources.Extensions | [Directory.Packages.props](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/Directory.Packages.props) |
| PackageVersion | System.Runtime.CompilerServices.Unsafe | [Directory.Packages.props](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/Directory.Packages.props) |
| PackageVersion | System.Security.Cryptography.Pkcs | [Directory.Packages.props](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/Directory.Packages.props) |
| PackageVersion | System.Security.Cryptography.ProtectedData | [Directory.Packages.props](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/Directory.Packages.props) |
| PackageVersion | System.Security.Cryptography.Xml | [Directory.Packages.props](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/Directory.Packages.props) |
| PackageVersion | System.Security.Principal.Windows | [Directory.Packages.props](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/Directory.Packages.props) |
| PackageVersion | System.Text.Encoding.CodePages | [Directory.Packages.props](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/Directory.Packages.props) |
| PackageVersion | System.Text.Json | [Directory.Packages.props](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/Directory.Packages.props) |
| PackageVersion | System.Threading.Channels | [Directory.Packages.props](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/Directory.Packages.props) |
| PackageVersion | System.Threading.Tasks.Dataflow | [Directory.Packages.props](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/Directory.Packages.props) |
| PackageVersion | System.Threading.Tasks.Extensions | [Directory.Packages.props](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/Directory.Packages.props) |
| PackageVersion | System.ValueTuple | [Directory.Packages.props](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/Directory.Packages.props) |
| PackageVersion | Microsoft.VisualStudio.Telemetry | [Directory.Packages.props](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/Directory.Packages.props) |
| PackageReference | Microsoft.ManifestTool.CrossPlatform | [eng/common/internal/Tools.csproj](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/eng/common/internal/Tools.csproj) |
| PackageReference | Microsoft.VisualStudioEng.MicroBuild.Core | [eng/common/internal/Tools.csproj](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/eng/common/internal/Tools.csproj) |
| PackageReference | Microsoft.VisualStudioEng.MicroBuild.Plugins.SwixBuild | [eng/common/internal/Tools.csproj](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/eng/common/internal/Tools.csproj) |
| PackageReference | Microsoft.DotNet.IBCMerge | [eng/common/internal/Tools.csproj](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/eng/common/internal/Tools.csproj) |
| PackageReference | Drop.App | [eng/common/internal/Tools.csproj](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/eng/common/internal/Tools.csproj) |
| ProjectReference | ..\Framework\Microsoft.Build.Framework.csproj | [src/Build/Microsoft.Build.csproj](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Build/Microsoft.Build.csproj) |
| PackageReference | Microsoft.VisualStudio.SolutionPersistence | [src/Build/Microsoft.Build.csproj](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Build/Microsoft.Build.csproj) |
| PackageReference | System.Configuration.ConfigurationManager | [src/Build/Microsoft.Build.csproj](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Build/Microsoft.Build.csproj) |
| PackageReference | System.Reflection.MetadataLoadContext | [src/Build/Microsoft.Build.csproj](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Build/Microsoft.Build.csproj) |
| PackageReference | Microsoft.BuildXL.Processes | [src/Build/Microsoft.Build.csproj](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Build/Microsoft.Build.csproj) |
| PackageReference | NETStandard.Library | [src/Build/Microsoft.Build.csproj](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Build/Microsoft.Build.csproj) |
| PackageReference | Microsoft.CodeAnalysis.Collections | [src/Build/Microsoft.Build.csproj](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Build/Microsoft.Build.csproj) |
| PackageReference | Microsoft.CodeAnalysis.PooledObjects | [src/Build/Microsoft.Build.csproj](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Build/Microsoft.Build.csproj) |
| PackageReference | System.Memory | [src/Build/Microsoft.Build.csproj](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Build/Microsoft.Build.csproj) |
| PackageReference | System.Security.Principal.Windows | [src/Build/Microsoft.Build.csproj](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Build/Microsoft.Build.csproj) |
| PackageReference | System.Text.Json | [src/Build/Microsoft.Build.csproj](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Build/Microsoft.Build.csproj) |
| PackageReference | System.Collections.Immutable | [src/Build/Microsoft.Build.csproj](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Build/Microsoft.Build.csproj) |
| PackageReference | System.Threading.Tasks.Dataflow | [src/Build/Microsoft.Build.csproj](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Build/Microsoft.Build.csproj) |
| PackageReference | System.Reflection.Metadata | [src/Build/Microsoft.Build.csproj](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Build/Microsoft.Build.csproj) |
| PackageReference | System.Text.Encoding.CodePages | [src/Build/Microsoft.Build.csproj](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Build/Microsoft.Build.csproj) |
| PackageReference | NuGet.Frameworks | [src/Build/Microsoft.Build.csproj](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Build/Microsoft.Build.csproj) |
| ProjectReference | ..\TaskAnalyzer\TaskAnalyzer.csproj | [src/Framework/Microsoft.Build.Framework.csproj](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Framework/Microsoft.Build.Framework.csproj) |
| PackageReference | Microsoft.CodeAnalysis.Contracts | [src/Framework/Microsoft.Build.Framework.csproj](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Framework/Microsoft.Build.Framework.csproj) |
| PackageReference | Microsoft.IO.Redist | [src/Framework/Microsoft.Build.Framework.csproj](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Framework/Microsoft.Build.Framework.csproj) |
| PackageReference | System.Runtime.CompilerServices.Unsafe | [src/Framework/Microsoft.Build.Framework.csproj](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Framework/Microsoft.Build.Framework.csproj) |
| PackageReference | System.Text.Json | [src/Framework/Microsoft.Build.Framework.csproj](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Framework/Microsoft.Build.Framework.csproj) |
| PackageReference | Microsoft.VisualStudio.Telemetry | [src/Framework/Microsoft.Build.Framework.csproj](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Framework/Microsoft.Build.Framework.csproj) |
| PackageReference | System.Collections.Immutable | [src/Framework/Microsoft.Build.Framework.csproj](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Framework/Microsoft.Build.Framework.csproj) |
| PackageReference | Microsoft.Win32.Registry | [src/Framework/Microsoft.Build.Framework.csproj](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Framework/Microsoft.Build.Framework.csproj) |
| PackageReference | System.Diagnostics.DiagnosticSource | [src/Framework/Microsoft.Build.Framework.csproj](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Framework/Microsoft.Build.Framework.csproj) |
| ProjectReference | ..\StringTools\StringTools.csproj | [src/Framework/Microsoft.Build.Framework.csproj](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Framework/Microsoft.Build.Framework.csproj) |
| PackageReference | Microsoft.Windows.CsWin32 | [src/Framework/Microsoft.Build.Framework.csproj](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Framework/Microsoft.Build.Framework.csproj) |
| PackageReference | PolySharp | [src/Framework/Microsoft.Build.Framework.csproj](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/src/Framework/Microsoft.Build.Framework.csproj) |


## License evidence and eligibility gate

Observed metadata hint: `MIT`.

Observed root metadata/license text is evidence, not a completed eligibility review. Resolve conditional/transitive dependencies, embedded assets, generated inputs and redistributable binaries before source reuse or release.

| Retrieved notice/license | Immutable source |
|---|---|
| [LICENSE](evidence/notices/LICENSE) | [LICENSE](https://github.com/dotnet/msbuild/blob/6348d0c087aeec18c323b01a2c77da089ddafea0/LICENSE) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-build-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
