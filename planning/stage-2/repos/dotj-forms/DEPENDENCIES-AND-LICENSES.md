# DJ-041 .j Forms: dependencies and licenses

## Proposed Java dependencies

core

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: FFM/JNI to Win32 common controls, COM where necessary; JDK host process.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|
| PackageVersion | Microsoft.Win32.SystemEvents | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | Microsoft.Windows.CsWin32 | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | System.CodeDom | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | System.ComponentModel.TypeConverter.TestData | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | System.Configuration.ConfigurationManager | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | System.Data.SqlClient | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | System.Drawing.Common.TestData | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | System.Formats.Asn1 | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | System.Formats.Nrbf | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | System.IO.Hashing | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | System.Management | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | System.Resources.Extensions | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | System.Runtime.CompilerServices.Unsafe | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | System.Runtime.Serialization.Formatters | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | System.Windows.Extensions | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | System.Windows.Extensions.TestData | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | System.Windows.Forms.DataVisualization | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | Microsoft.DotNet.Build.Tasks.Templating | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | Microsoft.DotNet.GenFacades | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | AwesomeAssertions | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | Moq | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | Microsoft.DotNet.RemoteExecutor | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | Microsoft.DotNet.XUnitV3Extensions | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | Microsoft.VisualStudio.Threading | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | Verify.XunitV3 | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | xunit.v3.assert | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | xunit.stafact | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | coverlet.msbuild | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | Codecov | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | ReportGenerator | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | CSharpIsNullAnalyzer | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | DotNetAnalyzers.DocumentationAnalyzers | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.Analyzers | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.Common | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp.Analyzer.Testing | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp.CodeFix.Testing | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp.CodeRefactoring.Testing | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp.SourceGenerators.Testing | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.VisualBasic.Analyzer.Testing | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.VisualBasic.CodeFix.Testing | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.VisualBasic.CodeRefactoring.Testing | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.VisualBasic.SourceGenerators.Testing | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp.Workspaces | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.NetAnalyzers | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.PublicApiAnalyzers | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.VisualBasic | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.VisualBasic.Workspaces | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.Workspaces.Common | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | NuGet.Packaging | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | StyleCop.Analyzers | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | Microsoft.TargetingPack.NETFramework.v4.7.2 | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | Microsoft.WindowsDesktop.App.Ref | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | Newtonsoft.Json | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | Microsoft.DotNet.IBCMerge | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | Microsoft.ManifestTool.CrossPlatform | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | Microsoft.VisualStudioEng.MicroBuild.Core | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | Microsoft.VisualStudioEng.MicroBuild.Plugins.SwixBuild | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | PolySharp | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | System.Diagnostics.DiagnosticSource | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| PackageVersion | System.ComponentModel.Annotations | [Directory.Packages.props](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/Directory.Packages.props) |
| ProjectReference | ..\System.Windows.Forms.PrivateSourceGenerators\src\System.Windows.Forms.PrivateSourceGenerators.csproj | [src/System.Windows.Forms/System.Windows.Forms.csproj](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/System.Windows.Forms/System.Windows.Forms.csproj) |
| ProjectReference | ..\Accessibility\src\Accessibility.ilproj | [src/System.Windows.Forms/System.Windows.Forms.csproj](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/System.Windows.Forms/System.Windows.Forms.csproj) |
| ProjectReference | ..\System.Private.Windows.Core\src\System.Private.Windows.Core.csproj | [src/System.Windows.Forms/System.Windows.Forms.csproj](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/System.Windows.Forms/System.Windows.Forms.csproj) |
| ProjectReference | ..\System.Windows.Forms.Primitives\src\System.Windows.Forms.Primitives.csproj | [src/System.Windows.Forms/System.Windows.Forms.csproj](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/System.Windows.Forms/System.Windows.Forms.csproj) |
| PackageReference | System.Configuration.ConfigurationManager | [src/System.Windows.Forms/System.Windows.Forms.csproj](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/System.Windows.Forms/System.Windows.Forms.csproj) |
| PackageReference | System.Resources.Extensions | [src/System.Windows.Forms/System.Windows.Forms.csproj](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/System.Windows.Forms/System.Windows.Forms.csproj) |
| PackageReference | System.Windows.Extensions | [src/System.Windows.Forms/System.Windows.Forms.csproj](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/System.Windows.Forms/System.Windows.Forms.csproj) |
| ProjectReference | ..\..\..\BuildAssist\BuildAssist.msbuildproj | [src/test/integration/WinformsControlsTest/WinformsControlsTest.csproj](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/test/integration/WinformsControlsTest/WinformsControlsTest.csproj) |
| ProjectReference | ..\..\..\System.Design\src\System.Design.Facade.csproj | [src/test/integration/WinformsControlsTest/WinformsControlsTest.csproj](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/test/integration/WinformsControlsTest/WinformsControlsTest.csproj) |
| ProjectReference | ..\..\..\System.Drawing.Common\src\System.Drawing.Common.csproj | [src/test/integration/WinformsControlsTest/WinformsControlsTest.csproj](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/test/integration/WinformsControlsTest/WinformsControlsTest.csproj) |
| ProjectReference | ..\..\..\System.Drawing.Design\src\System.Drawing.Design.Facade.csproj | [src/test/integration/WinformsControlsTest/WinformsControlsTest.csproj](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/test/integration/WinformsControlsTest/WinformsControlsTest.csproj) |
| ProjectReference | ..\..\..\System.Windows.Forms.Design\src\System.Windows.Forms.Design.csproj | [src/test/integration/WinformsControlsTest/WinformsControlsTest.csproj](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/test/integration/WinformsControlsTest/WinformsControlsTest.csproj) |
| ProjectReference | ..\..\..\System.Windows.Forms\System.Windows.Forms.csproj | [src/test/integration/WinformsControlsTest/WinformsControlsTest.csproj](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/test/integration/WinformsControlsTest/WinformsControlsTest.csproj) |
| ProjectReference | ..\System.Windows.Forms.IntegrationTests.Common\System.Windows.Forms.IntegrationTests.Common.csproj | [src/test/integration/WinformsControlsTest/WinformsControlsTest.csproj](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/test/integration/WinformsControlsTest/WinformsControlsTest.csproj) |
| PackageReference | System.Data.SqlClient | [src/test/integration/WinformsControlsTest/WinformsControlsTest.csproj](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/test/integration/WinformsControlsTest/WinformsControlsTest.csproj) |
| PackageReference | System.Management | [src/test/integration/WinformsControlsTest/WinformsControlsTest.csproj](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/test/integration/WinformsControlsTest/WinformsControlsTest.csproj) |
| PackageReference | System.Windows.Forms.DataVisualization | [src/test/integration/WinformsControlsTest/WinformsControlsTest.csproj](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/test/integration/WinformsControlsTest/WinformsControlsTest.csproj) |
| ProjectReference | ..\..\..\System.Windows.Forms.Analyzers\src\System.Windows.Forms.Analyzers.csproj | [src/test/integration/WinformsControlsTest/WinformsControlsTest.csproj](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/test/integration/WinformsControlsTest/WinformsControlsTest.csproj) |
| ProjectReference | ..\..\..\System.Windows.Forms.Analyzers.CSharp\src\System.Windows.Forms.Analyzers.CSharp.csproj | [src/test/integration/WinformsControlsTest/WinformsControlsTest.csproj](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/test/integration/WinformsControlsTest/WinformsControlsTest.csproj) |


## License evidence and eligibility gate

Observed metadata hint: `unavailable`.

Observed root metadata/license text is evidence, not a completed eligibility review. Resolve conditional/transitive dependencies, embedded assets, generated inputs and redistributable binaries before source reuse or release.

| Retrieved notice/license | Immutable source |
|---|---|
| [LICENSE.TXT](evidence/notices/LICENSE.TXT) | [LICENSE.TXT](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/LICENSE.TXT) |
| [THIRD-PARTY-NOTICES.TXT](evidence/notices/THIRD-PARTY-NOTICES.TXT) | [THIRD-PARTY-NOTICES.TXT](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/THIRD-PARTY-NOTICES.TXT) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-forms-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
