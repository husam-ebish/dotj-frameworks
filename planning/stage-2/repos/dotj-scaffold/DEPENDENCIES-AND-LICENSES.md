# DJ-009 .j Scaffold: dependencies and licenses

## Proposed Java dependencies

code,templates,web,entity

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: Compiler tree APIs, filesystem, XML parsing and template engine.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|
| PackageVersion | Azure.Identity | [Directory.Packages.props](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/Directory.Packages.props) |
| PackageVersion | Humanizer.Core | [Directory.Packages.props](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/Directory.Packages.props) |
| PackageVersion | Microsoft.Build.Locator | [Directory.Packages.props](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/Directory.Packages.props) |
| PackageVersion | Microsoft.Build | [Directory.Packages.props](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/Directory.Packages.props) |
| PackageVersion | Microsoft.Build.Framework | [Directory.Packages.props](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/Directory.Packages.props) |
| PackageVersion | Microsoft.Build.Runtime | [Directory.Packages.props](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/Directory.Packages.props) |
| PackageVersion | Microsoft.Build.Tasks.Core | [Directory.Packages.props](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/Directory.Packages.props) |
| PackageVersion | Microsoft.Build.Utilities.Core | [Directory.Packages.props](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.Razor.Language | [Directory.Packages.props](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.Common | [Directory.Packages.props](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp | [Directory.Packages.props](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp.Features | [Directory.Packages.props](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp.Workspaces | [Directory.Packages.props](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.Features | [Directory.Packages.props](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.Razor | [Directory.Packages.props](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.Workspaces.Common | [Directory.Packages.props](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.Workspaces.MSBuild | [Directory.Packages.props](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/Directory.Packages.props) |
| PackageVersion | Microsoft.EntityFrameworkCore | [Directory.Packages.props](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/Directory.Packages.props) |
| PackageVersion | Microsoft.EntityFrameworkCore.SqlServer | [Directory.Packages.props](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/Directory.Packages.props) |
| PackageVersion | Microsoft.EntityFrameworkCore.Design | [Directory.Packages.props](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.CommandLineUtils.Sources | [Directory.Packages.props](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Configuration | [Directory.Packages.props](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Configuration.Abstractions | [Directory.Packages.props](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Configuration.Binder | [Directory.Packages.props](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Configuration.CommandLine | [Directory.Packages.props](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.DependencyInjection | [Directory.Packages.props](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.DependencyModel | [Directory.Packages.props](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.FileProviders.Embedded | [Directory.Packages.props](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.FileProviders.Physical | [Directory.Packages.props](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Logging.Console | [Directory.Packages.props](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Logging.Debug | [Directory.Packages.props](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/Directory.Packages.props) |
| PackageVersion | Microsoft.Graph | [Directory.Packages.props](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/Directory.Packages.props) |
| PackageVersion | Microsoft.Identity.Client.Extensions.Msal | [Directory.Packages.props](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/Directory.Packages.props) |
| PackageVersion | Mono.TextTemplating | [Directory.Packages.props](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/Directory.Packages.props) |
| PackageVersion | Moq | [Directory.Packages.props](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/Directory.Packages.props) |
| PackageVersion | Newtonsoft.Json | [Directory.Packages.props](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/Directory.Packages.props) |
| PackageVersion | NuGet.Packaging | [Directory.Packages.props](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/Directory.Packages.props) |
| PackageVersion | NuGet.ProjectModel | [Directory.Packages.props](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/Directory.Packages.props) |
| PackageVersion | Spectre.Console.Flow | [Directory.Packages.props](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/Directory.Packages.props) |
| PackageVersion | Spectre.Console | [Directory.Packages.props](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/Directory.Packages.props) |
| PackageVersion | Spectre.Console.Cli | [Directory.Packages.props](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/Directory.Packages.props) |
| PackageVersion | System.CommandLine | [Directory.Packages.props](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/Directory.Packages.props) |
| PackageVersion | System.Security.Cryptography.ProtectedData | [Directory.Packages.props](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/Directory.Packages.props) |
| PackageVersion | xunit.skippablefact | [Directory.Packages.props](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/Directory.Packages.props) |
| PackageVersion | System.Formats.Asn1 | [Directory.Packages.props](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/Directory.Packages.props) |
| PackageReference | Microsoft.ManifestTool.CrossPlatform | [eng/common/internal/Tools.csproj](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/eng/common/internal/Tools.csproj) |
| PackageReference | Microsoft.VisualStudioEng.MicroBuild.Core | [eng/common/internal/Tools.csproj](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/eng/common/internal/Tools.csproj) |
| PackageReference | Microsoft.VisualStudioEng.MicroBuild.Plugins.SwixBuild | [eng/common/internal/Tools.csproj](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/eng/common/internal/Tools.csproj) |
| PackageReference | Microsoft.DotNet.IBCMerge | [eng/common/internal/Tools.csproj](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/eng/common/internal/Tools.csproj) |
| PackageReference | Drop.App | [eng/common/internal/Tools.csproj](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/eng/common/internal/Tools.csproj) |
| PackageReference | Azure.Identity | [src/MSIdentityScaffolding/Microsoft.DotNet.MSIdentity/Microsoft.DotNet.MSIdentity.csproj](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/src/MSIdentityScaffolding/Microsoft.DotNet.MSIdentity/Microsoft.DotNet.MSIdentity.csproj) |
| PackageReference | Microsoft.Extensions.Configuration | [src/MSIdentityScaffolding/Microsoft.DotNet.MSIdentity/Microsoft.DotNet.MSIdentity.csproj](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/src/MSIdentityScaffolding/Microsoft.DotNet.MSIdentity/Microsoft.DotNet.MSIdentity.csproj) |
| PackageReference | Microsoft.Extensions.Configuration.Binder | [src/MSIdentityScaffolding/Microsoft.DotNet.MSIdentity/Microsoft.DotNet.MSIdentity.csproj](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/src/MSIdentityScaffolding/Microsoft.DotNet.MSIdentity/Microsoft.DotNet.MSIdentity.csproj) |
| PackageReference | Microsoft.Extensions.Configuration.CommandLine | [src/MSIdentityScaffolding/Microsoft.DotNet.MSIdentity/Microsoft.DotNet.MSIdentity.csproj](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/src/MSIdentityScaffolding/Microsoft.DotNet.MSIdentity/Microsoft.DotNet.MSIdentity.csproj) |
| PackageReference | Microsoft.Graph | [src/MSIdentityScaffolding/Microsoft.DotNet.MSIdentity/Microsoft.DotNet.MSIdentity.csproj](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/src/MSIdentityScaffolding/Microsoft.DotNet.MSIdentity/Microsoft.DotNet.MSIdentity.csproj) |
| PackageReference | Microsoft.Identity.Client.Extensions.Msal | [src/MSIdentityScaffolding/Microsoft.DotNet.MSIdentity/Microsoft.DotNet.MSIdentity.csproj](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/src/MSIdentityScaffolding/Microsoft.DotNet.MSIdentity/Microsoft.DotNet.MSIdentity.csproj) |
| PackageReference | Newtonsoft.Json | [src/MSIdentityScaffolding/Microsoft.DotNet.MSIdentity/Microsoft.DotNet.MSIdentity.csproj](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/src/MSIdentityScaffolding/Microsoft.DotNet.MSIdentity/Microsoft.DotNet.MSIdentity.csproj) |
| PackageReference | System.Security.Cryptography.ProtectedData | [src/MSIdentityScaffolding/Microsoft.DotNet.MSIdentity/Microsoft.DotNet.MSIdentity.csproj](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/src/MSIdentityScaffolding/Microsoft.DotNet.MSIdentity/Microsoft.DotNet.MSIdentity.csproj) |
| ProjectReference | $(RepoRoot)src\Shared\Microsoft.DotNet.Scaffolding.Shared\Microsoft.DotNet.Scaffolding.Shared.csproj | [src/MSIdentityScaffolding/Microsoft.DotNet.MSIdentity/Microsoft.DotNet.MSIdentity.csproj](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/src/MSIdentityScaffolding/Microsoft.DotNet.MSIdentity/Microsoft.DotNet.MSIdentity.csproj) |
| ProjectReference | $(RepoRoot)src\MSIdentityScaffolding\Microsoft.DotNet.MSIdentity\Microsoft.DotNet.MSIdentity.csproj | [test/MSIdentityScaffolding/Microsoft.DotNet.MSIdentity.Tests/Microsoft.DotNet.MSIdentity.Tests.csproj](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/test/MSIdentityScaffolding/Microsoft.DotNet.MSIdentity.Tests/Microsoft.DotNet.MSIdentity.Tests.csproj) |
| ProjectReference | $(RepoRoot)src\MSIdentityScaffolding\dotnet-msidentity\dotnet-msidentity.csproj | [test/MSIdentityScaffolding/Microsoft.DotNet.MSIdentity.Tests/Microsoft.DotNet.MSIdentity.Tests.csproj](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/test/MSIdentityScaffolding/Microsoft.DotNet.MSIdentity.Tests/Microsoft.DotNet.MSIdentity.Tests.csproj) |
| PackageReference | System.CommandLine | [src/MSIdentityScaffolding/dotnet-msidentity/dotnet-msidentity.csproj](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/src/MSIdentityScaffolding/dotnet-msidentity/dotnet-msidentity.csproj) |
| ProjectReference | $(RepoRoot)src\MSIdentityScaffolding\Microsoft.DotNet.MSIdentity\Microsoft.DotNet.MSIdentity.csproj | [src/MSIdentityScaffolding/dotnet-msidentity/dotnet-msidentity.csproj](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/src/MSIdentityScaffolding/dotnet-msidentity/dotnet-msidentity.csproj) |


## License evidence and eligibility gate

Observed metadata hint: `MIT`.

Observed root metadata/license text is evidence, not a completed eligibility review. Resolve conditional/transitive dependencies, embedded assets, generated inputs and redistributable binaries before source reuse or release.

| Retrieved notice/license | Immutable source |
|---|---|
| [LICENSE](evidence/notices/LICENSE) | [LICENSE](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/LICENSE) |
| [NOTICE.txt](evidence/notices/NOTICE.txt) | [NOTICE.txt](https://github.com/dotnet/Scaffolding/blob/107111c945bcf1264c035457a0744318b6bae3d9/NOTICE.txt) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-scaffold-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
