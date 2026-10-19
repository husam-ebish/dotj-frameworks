# DJ-002 .j SDK: dependencies and licenses

## Proposed Java dependencies

build,templates,packages

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: ProcessBuilder, ToolProvider, file APIs and JAR tooling; installed javac/jar bootstrap the toolchain.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|
| PackageVersion | AwesomeAssertions | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | AwesomeAssertions.Json | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Azure.Monitor.OpenTelemetry.Exporter | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Basic.CompilerLog.Util | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | BenchmarkDotNet | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | BenchmarkDotNet.Diagnostics.Windows | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | JsonSchema.Net | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | MessagePack | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.DeveloperCertificates.XPlat | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.Mvc.Razor.Extensions.Tooling.Internal | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.TestHost | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.Bcl.AsyncInterfaces | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.Build.NuGetSdkResolver | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.Build.TaskAuthoring.Analyzer | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | OpenTelemetry | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | OpenTelemetry.Exporter.InMemory | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | OpenTelemetry.Exporter.OpenTelemetryProtocol | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | OpenTelemetry.Instrumentation.Http | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | OpenTelemetry.Instrumentation.Runtime | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | OpenTelemetry.PersistentStorage.FileSystem | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.Analyzer.Testing | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.BuildClient | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.Common | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.Contracts | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.Analyzers | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp.CodeStyle | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp.Features | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp.Workspaces | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.Features | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.PublicApiAnalyzers | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.Razor.Tooling.Internal | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.VisualBasic | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.VisualBasic.CodeStyle | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.VisualBasic.Features | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.VisualBasic.Workspaces | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.Workspaces.Common | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.Workspaces.MSBuild | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.ExternalAccess.HotReload | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp.CodeFix.Testing | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp.CodeRefactoring.Testing | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.VisualBasic.CodeFix.Testing | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.VisualBasic.CodeRefactoring.Testing | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.Css.Parser | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.DiaSymReader | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.Deployment.DotNet.Releases | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.DotNet.Build.Tasks.Installers | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.DotNet.Build.Tasks.Templating | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.DotNet.Build.Tasks.Workloads | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.DotNet.Installer.Windows.Security.TestData | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.DotNet.SignCheckTask | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.DotNet.XUnitV3Extensions | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Configuration.EnvironmentVariables | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.DependencyModel | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.DependencyInjection.Abstractions | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.FileProviders.Abstractions | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.FileSystemGlobbing | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Logging | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Logging.Abstractions | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Logging.Console | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.ObjectPool | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.FSharp.Compiler | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.IO.Redist | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.Net.Compilers.Toolset.Framework | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.Management.Infrastructure | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.NET.HostModel | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.NET.ProjectData.Tasks | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.NET.Sdk.Razor.SourceGenerators.Transport | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.NETCore.App.Runtime.win-x86 | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.NETCore.App.Runtime.win-x64 | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.NETCore.App.Runtime.win-arm64 | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.NETCore.DotNetHostResolver | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.NETCore.Targets | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.Signed.Wix | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.TestPlatform.Build | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.TestPlatform.CLI | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.TestPlatform.ObjectModel | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.VisualStudioEng.MicroBuild.Plugins.SwixBuild | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.VisualStudio.Composition | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.VisualStudio.Setup.Configuration.Interop | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.VisualStudio.SolutionPersistence | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.Web.Deployment | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.Web.Xdt | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.Win32.SystemEvents | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.Windows.CsWin32 | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.Wix | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.WixToolset.Bal.wixext | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.WixToolset.Dependency.wixext | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.WixToolset.Dtf.WindowsInstaller | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.WixToolset.Heat | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.WixToolset.Util.wixext | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.WixToolset.UI.wixext | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | MSBuild.StructuredLogger | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.TypeScript.MSBuild | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Moq | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Newtonsoft.Json | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | NuGet.Build.Tasks | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | NuGet.Build.Tasks.Console | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | NuGet.Build.Tasks.Pack | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | NuGet.CommandLine.XPlat | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | NuGet.Commands | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | NuGet.Common | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | NuGet.Configuration | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | NuGet.Credentials | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | NuGet.Frameworks | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | NuGet.LibraryModel | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | NuGet.Localization | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | NuGet.Packaging | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | NuGet.ProjectModel | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | NuGet.Protocol | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | NuGet.Versioning | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | runtime.linux-musl-x64.Microsoft.NETCore.DotNetHostResolver | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | runtime.linux-x64.Microsoft.NETCore.DotNetHostResolver | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | runtime.osx-x64.Microsoft.NETCore.DotNetHostResolver | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Spectre.Console | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Spectre.Console.Testing | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | StyleCop.Analyzers | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | System.CodeDom | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | System.CommandLine | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | System.CommandLine.NamingConventionBinder | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | System.ComponentModel.Composition | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | System.Composition.AttributedModel | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | System.Composition.Convention | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | System.Composition.Hosting | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | System.Composition.Runtime | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | System.Composition.TypedParts | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | System.Configuration.ConfigurationManager | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | System.Diagnostics.DiagnosticSource | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | System.Formats.Asn1 | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | System.IO.Hashing | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | System.Reflection.MetadataLoadContext | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | System.Resources.Extensions | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | System.Security.Cryptography.Pkcs | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | System.Security.Cryptography.ProtectedData | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | System.Security.Cryptography.Xml | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | System.Security.Permissions | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | System.ServiceProcess.ServiceController | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | System.Text.Encoding.CodePages | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | System.Text.Json | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | System.Windows.Extensions | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Valleysoft.DockerCredsProvider | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Xunit.Combinatorial | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | xunit.v3.extensibility.core | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.Build | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.Build.Framework | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.Build.Localization | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.Build.Locator | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.Build.Runtime | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.Build.Tasks.Core | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.Build.Utilities.Core | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.NET.StringTools | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.Build | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.Build.Framework | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.Build.Localization | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.Build.Locator | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.Build.Runtime | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.Build.Tasks.Core | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.Build.Utilities.Core | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | Microsoft.NET.StringTools | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageVersion | PolySharp | [Directory.Packages.props](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/Directory.Packages.props) |
| PackageReference | Microsoft.ManifestTool.CrossPlatform | [eng/common/internal/Tools.csproj](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/eng/common/internal/Tools.csproj) |
| PackageReference | Microsoft.VisualStudioEng.MicroBuild.Core | [eng/common/internal/Tools.csproj](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/eng/common/internal/Tools.csproj) |
| PackageReference | Microsoft.VisualStudioEng.MicroBuild.Plugins.SwixBuild | [eng/common/internal/Tools.csproj](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/eng/common/internal/Tools.csproj) |
| PackageReference | Microsoft.DotNet.IBCMerge | [eng/common/internal/Tools.csproj](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/eng/common/internal/Tools.csproj) |
| PackageReference | Drop.App | [eng/common/internal/Tools.csproj](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/eng/common/internal/Tools.csproj) |
| PackageReference | Microsoft.NET.Test.Sdk | [documentation/TemplateEngine/Samples/content/05-multi-project/MyProject.Console.Test/MyProject.Console.Test.csproj](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/documentation/TemplateEngine/Samples/content/05-multi-project/MyProject.Console.Test/MyProject.Console.Test.csproj) |
| PackageReference | xunit | [documentation/TemplateEngine/Samples/content/05-multi-project/MyProject.Console.Test/MyProject.Console.Test.csproj](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/documentation/TemplateEngine/Samples/content/05-multi-project/MyProject.Console.Test/MyProject.Console.Test.csproj) |
| PackageReference | xunit.runner.visualstudio | [documentation/TemplateEngine/Samples/content/05-multi-project/MyProject.Console.Test/MyProject.Console.Test.csproj](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/documentation/TemplateEngine/Samples/content/05-multi-project/MyProject.Console.Test/MyProject.Console.Test.csproj) |
| ProjectReference | ../MyProject.Console/MyProject.Console.csproj | [documentation/TemplateEngine/Samples/content/05-multi-project/MyProject.Console.Test/MyProject.Console.Test.csproj](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/documentation/TemplateEngine/Samples/content/05-multi-project/MyProject.Console.Test/MyProject.Console.Test.csproj) |
| PackageReference | Microsoft.Build.Framework | [src/BlazorWasmSdk/Tasks/Microsoft.NET.Sdk.BlazorWebAssembly.Tasks.csproj](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/src/BlazorWasmSdk/Tasks/Microsoft.NET.Sdk.BlazorWebAssembly.Tasks.csproj) |
| PackageReference | Microsoft.Build.Utilities.Core | [src/BlazorWasmSdk/Tasks/Microsoft.NET.Sdk.BlazorWebAssembly.Tasks.csproj](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/src/BlazorWasmSdk/Tasks/Microsoft.NET.Sdk.BlazorWebAssembly.Tasks.csproj) |
| PackageReference | System.IO.Hashing | [src/BlazorWasmSdk/Tasks/Microsoft.NET.Sdk.BlazorWebAssembly.Tasks.csproj](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/src/BlazorWasmSdk/Tasks/Microsoft.NET.Sdk.BlazorWebAssembly.Tasks.csproj) |
| PackageReference | System.CommandLine | [src/BlazorWasmSdk/Tool/Microsoft.NET.Sdk.BlazorWebAssembly.Tool.csproj](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/src/BlazorWasmSdk/Tool/Microsoft.NET.Sdk.BlazorWebAssembly.Tool.csproj) |
| PackageReference | Microsoft.CodeAnalysis | [src/Microsoft.CodeAnalysis.NetAnalyzers/tests/Microsoft.CodeAnalysis.NetAnalyzers.UnitTests/Microsoft.CodeAnalysis.NetAnalyzers.UnitTests.csproj](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/src/Microsoft.CodeAnalysis.NetAnalyzers/tests/Microsoft.CodeAnalysis.NetAnalyzers.UnitTests/Microsoft.CodeAnalysis.NetAnalyzers.UnitTests.csproj) |
| PackageReference | Microsoft.CodeAnalysis.CSharp | [src/Microsoft.CodeAnalysis.NetAnalyzers/tests/Microsoft.CodeAnalysis.NetAnalyzers.UnitTests/Microsoft.CodeAnalysis.NetAnalyzers.UnitTests.csproj](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/src/Microsoft.CodeAnalysis.NetAnalyzers/tests/Microsoft.CodeAnalysis.NetAnalyzers.UnitTests/Microsoft.CodeAnalysis.NetAnalyzers.UnitTests.csproj) |
| ProjectReference | ..\Test.Utilities\Test.Utilities.csproj | [src/Microsoft.CodeAnalysis.NetAnalyzers/tests/Microsoft.CodeAnalysis.NetAnalyzers.UnitTests/Microsoft.CodeAnalysis.NetAnalyzers.UnitTests.csproj](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/src/Microsoft.CodeAnalysis.NetAnalyzers/tests/Microsoft.CodeAnalysis.NetAnalyzers.UnitTests/Microsoft.CodeAnalysis.NetAnalyzers.UnitTests.csproj) |
| ProjectReference | ..\..\src\Microsoft.CodeAnalysis.NetAnalyzers\Microsoft.CodeAnalysis.NetAnalyzers.csproj | [src/Microsoft.CodeAnalysis.NetAnalyzers/tests/Microsoft.CodeAnalysis.NetAnalyzers.UnitTests/Microsoft.CodeAnalysis.NetAnalyzers.UnitTests.csproj](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/src/Microsoft.CodeAnalysis.NetAnalyzers/tests/Microsoft.CodeAnalysis.NetAnalyzers.UnitTests/Microsoft.CodeAnalysis.NetAnalyzers.UnitTests.csproj) |
| ProjectReference | ..\..\src\Microsoft.CodeAnalysis.CSharp.NetAnalyzers\Microsoft.CodeAnalysis.CSharp.NetAnalyzers.csproj | [src/Microsoft.CodeAnalysis.NetAnalyzers/tests/Microsoft.CodeAnalysis.NetAnalyzers.UnitTests/Microsoft.CodeAnalysis.NetAnalyzers.UnitTests.csproj](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/src/Microsoft.CodeAnalysis.NetAnalyzers/tests/Microsoft.CodeAnalysis.NetAnalyzers.UnitTests/Microsoft.CodeAnalysis.NetAnalyzers.UnitTests.csproj) |
| ProjectReference | ..\..\src\Microsoft.CodeAnalysis.VisualBasic.NetAnalyzers\Microsoft.CodeAnalysis.VisualBasic.NetAnalyzers.vbproj | [src/Microsoft.CodeAnalysis.NetAnalyzers/tests/Microsoft.CodeAnalysis.NetAnalyzers.UnitTests/Microsoft.CodeAnalysis.NetAnalyzers.UnitTests.csproj](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/src/Microsoft.CodeAnalysis.NetAnalyzers/tests/Microsoft.CodeAnalysis.NetAnalyzers.UnitTests/Microsoft.CodeAnalysis.NetAnalyzers.UnitTests.csproj) |


## License evidence and eligibility gate

Observed metadata hint: `MIT`.

Observed root metadata/license text is evidence, not a completed eligibility review. Resolve conditional/transitive dependencies, embedded assets, generated inputs and redistributable binaries before source reuse or release.

| Retrieved notice/license | Immutable source |
|---|---|
| [LICENSE.TXT](evidence/notices/LICENSE.TXT) | [LICENSE.TXT](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/LICENSE.TXT) |
| [THIRD-PARTY-NOTICES.TXT](evidence/notices/THIRD-PARTY-NOTICES.TXT) | [THIRD-PARTY-NOTICES.TXT](https://github.com/dotnet/sdk/blob/c70b3856e7948678daa3950ec5517759754bf47c/THIRD-PARTY-NOTICES.TXT) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-sdk-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
