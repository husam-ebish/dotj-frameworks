# DJ-062 .j Packages: dependencies and licenses

## Proposed Java dependencies

core,json

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: HTTP client, ZIP/JAR, cryptographic verification and XML/JSON.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|
| PackageVersion | AwesomeAssertions | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | BenchmarkDotNet | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | ILRepack | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | Lucene.Net | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | Microsoft.Build | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | Microsoft.Build.Artifacts | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | Microsoft.Build.Framework | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | Microsoft.Build.Locator | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | Microsoft.Build.Utilities.Core | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.Common | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.Features | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.Workspaces.Common | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | Microsoft.CSharp | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | Microsoft.DataAI.NuGetRecommender.Contracts | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | Microsoft.DotNet.Build.Tasks.Feed | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | Microsoft.DotNet.Maestro.Tasks | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | Microsoft.DotNet.XliffTasks | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | Microsoft.DotNet.SignTool | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.FileProviders.Abstractions | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.FileSystemGlobbing | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | Microsoft.Internal.VisualStudio.Shell.Framework | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | Microsoft.NET.Test.Sdk | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | Microsoft.PowerShell.3.ReferenceAssemblies | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | Microsoft.TeamFoundationServer.ExtendedClient | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | Microsoft.Test.Apex.VisualStudio | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | Microsoft.TestPlatform.Portable | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | Microsoft.VisualStudio.ComponentModelHost | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | Microsoft.VisualStudio.Copilot | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | Microsoft.VisualStudio.LanguageServices | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | Microsoft.VisualStudio.Markdown.Platform | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | Microsoft.VisualStudio.ProjectSystem | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | Microsoft.VisualStudio.ProjectSystem.Managed.VS | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | Microsoft.VisualStudio.ProjectSystem.VS | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | Microsoft.VisualStudio.Extensibility.Sdk | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | Microsoft.VisualStudio.Extensibility.Build | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | Microsoft.VisualStudio.SDK | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | Microsoft.VisualStudio.Sdk.TestFramework.Xunit | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | Microsoft.VisualStudio.Setup.Configuration.Interop | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | Microsoft.VisualStudio.Shell.Styles | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | Microsoft.VisualStudio.TemplateWizardInterface | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | Microsoft.VSSDK.BuildTools | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | Microsoft.Web.Xdt | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | Moq | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | MSTest.TestAdapter | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | MSTest.TestFramework | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | Newtonsoft.Json | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | NuGet.Client.EndToEnd.TestData | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | NuGet.Core | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | NuGetValidator | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | SharpZipLib | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | Spectre.Console | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | Spectre.Console.Testing | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | System.Collections.Immutable | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | System.CommandLine | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | System.ComponentModel.Composition | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | System.Formats.Asn1 | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | System.Memory | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | System.Security.Cryptography.Pkcs | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | System.Security.Cryptography.ProtectedData | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | System.Text.Json | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | System.Threading.Tasks.Dataflow | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | VsWebSite.Interop | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | xunit | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | xunit.runner.visualstudio | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | Xunit.StaFact | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | MessagePack | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | Microsoft.IdentityModel.JsonWebTokens | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | System.IdentityModel.Tokens.Jwt | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | Microsoft.ServiceHub.Framework | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| PackageVersion | Microsoft.VisualStudio.Shell.15.0 | [Directory.Packages.props](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/Directory.Packages.props) |
| ProjectReference | ..\..\NuGet.Core\Microsoft.Build.NuGetSdkResolver\Microsoft.Build.NuGetSdkResolver.csproj | [src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj) |
| ProjectReference | ..\..\NuGet.Core\NuGet.Build.Tasks\NuGet.Build.Tasks.csproj | [src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj) |
| ProjectReference | ..\..\NuGet.Core\NuGet.Build.Tasks.Console\NuGet.Build.Tasks.Console.csproj | [src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj) |
| ProjectReference | ..\..\NuGet.Core\NuGet.Common\NuGet.Common.csproj | [src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj) |
| ProjectReference | ..\..\NuGet.Core\NuGet.Configuration\NuGet.Configuration.csproj | [src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj) |
| ProjectReference | ..\..\NuGet.Core\NuGet.DependencyResolver.Core\NuGet.DependencyResolver.Core.csproj | [src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj) |
| ProjectReference | ..\..\NuGet.Core\NuGet.Frameworks\NuGet.Frameworks.csproj | [src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj) |
| ProjectReference | ..\..\NuGet.Core\NuGet.LibraryModel\NuGet.LibraryModel.csproj | [src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj) |
| ProjectReference | ..\..\NuGet.Core\NuGet.PackageManagement\NuGet.PackageManagement.csproj | [src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj) |
| ProjectReference | ..\..\NuGet.Core\NuGet.Packaging\NuGet.Packaging.csproj | [src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj) |
| ProjectReference | ..\..\NuGet.Core\NuGet.ProjectModel\NuGet.ProjectModel.csproj | [src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj) |
| ProjectReference | ..\..\NuGet.Core\NuGet.Protocol\NuGet.Protocol.csproj | [src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj) |
| ProjectReference | ..\..\NuGet.Core\NuGet.Resolver\NuGet.Resolver.csproj | [src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj) |
| ProjectReference | ..\..\NuGet.Core\NuGet.Versioning\NuGet.Versioning.csproj | [src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj) |
| ProjectReference | ..\NuGet.Tools\NuGet.Tools.csproj | [src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj) |
| ProjectReference | ..\NuGet.Indexing\NuGet.Indexing.csproj | [src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj) |
| ProjectReference | ..\..\NuGet.Core\NuGet.Commands\NuGet.Commands.csproj | [src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj) |
| ProjectReference | ..\..\NuGet.Core\NuGet.Credentials\NuGet.Credentials.csproj | [src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj) |
| ProjectReference | ..\NuGet.SolutionRestoreManager\NuGet.SolutionRestoreManager.csproj | [src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj) |
| ProjectReference | ..\NuGet.VisualStudio.Contracts\NuGet.VisualStudio.Contracts.csproj | [src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj) |
| ProjectReference | ..\NuGet.VisualStudio.Implementation\NuGet.VisualStudio.Implementation.csproj | [src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj) |
| ProjectReference | ..\NuGet.PackageManagement.PowerShellCmdlets\NuGet.PackageManagement.PowerShellCmdlets.csproj | [src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj) |
| ProjectReference | ..\NuGet.PackageManagement.UI\NuGet.PackageManagement.UI.csproj | [src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj) |
| ProjectReference | ..\NuGet.PackageManagement.VisualStudio\NuGet.PackageManagement.VisualStudio.csproj | [src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj) |
| ProjectReference | ..\NuGet.VisualStudio.Internal.Contracts\NuGet.VisualStudio.Internal.Contracts.csproj | [src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj) |
| ProjectReference | ..\NuGet.VisualStudio.Interop\NuGet.VisualStudio.Interop.csproj | [src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj) |
| ProjectReference | ..\NuGet.VisualStudio.Common\NuGet.VisualStudio.Common.csproj | [src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj) |
| ProjectReference | ..\NuGet.VisualStudio\NuGet.VisualStudio.csproj | [src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj) |
| ProjectReference | ..\NuGet.Console\NuGet.Console.csproj | [src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj) |
| PackageReference | Microsoft.VisualStudio.Extensibility.Sdk | [src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj) |
| PackageReference | Microsoft.VisualStudio.Extensibility.Build | [src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj) |
| PackageReference | Lucene.Net | [src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj) |
| PackageReference | SharpZipLib | [src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj) |
| PackageReference | Newtonsoft.Json | [src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj) |
| PackageReference | Microsoft.Web.Xdt | [src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj) |
| PackageReference | Microsoft.VSSDK.BuildTools | [src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/src/NuGet.Clients/NuGet.VisualStudio.Client/NuGet.VisualStudio.Client.csproj) |
| ProjectReference | ..\..\..\src\NuGet.Core\NuGet.Configuration\NuGet.Configuration.csproj | [test/NuGet.Core.Tests/NuGet.Configuration.Test/NuGet.Configuration.Test.csproj](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/test/NuGet.Core.Tests/NuGet.Configuration.Test/NuGet.Configuration.Test.csproj) |
| ProjectReference | ..\..\TestUtilities\Test.Utility\Test.Utility.csproj | [test/NuGet.Core.Tests/NuGet.Configuration.Test/NuGet.Configuration.Test.csproj](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/test/NuGet.Core.Tests/NuGet.Configuration.Test/NuGet.Configuration.Test.csproj) |


## License evidence and eligibility gate

Observed metadata hint: `unavailable`.

Observed root metadata/license text is evidence, not a completed eligibility review. Resolve conditional/transitive dependencies, embedded assets, generated inputs and redistributable binaries before source reuse or release.

| Retrieved notice/license | Immutable source |
|---|---|
| [LICENSE.txt](evidence/notices/LICENSE.txt) | [LICENSE.txt](https://github.com/NuGet/NuGet.Client/blob/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f/LICENSE.txt) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-packages-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
