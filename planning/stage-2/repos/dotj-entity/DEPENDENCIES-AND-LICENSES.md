# DJ-019 .j Entity: dependencies and licenses

## Proposed Java dependencies

core,postgresql

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: java.sql contracts, reflection/MethodHandles and annotation processing; own PostgreSQL provider/client.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|
| PackageVersion | System.Text.Json | [Directory.Packages.props](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Caching.Memory | [Directory.Packages.props](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Logging | [Directory.Packages.props](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.DependencyModel | [Directory.Packages.props](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.HostFactoryResolver.Sources | [Directory.Packages.props](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp | [Directory.Packages.props](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp.Workspaces | [Directory.Packages.props](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.Workspaces.MSBuild | [Directory.Packages.props](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/Directory.Packages.props) |
| PackageVersion | DotNetAnalyzers.DocumentationAnalyzers | [Directory.Packages.props](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/Directory.Packages.props) |
| PackageVersion | Microsoft.Build.Framework | [Directory.Packages.props](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/Directory.Packages.props) |
| PackageVersion | Microsoft.Build.Utilities.Core | [Directory.Packages.props](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/Directory.Packages.props) |
| PackageVersion | Microsoft.Build.Tasks.Core | [Directory.Packages.props](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/Directory.Packages.props) |
| PackageVersion | Microsoft.DotNet.Build.Tasks.Templating | [Directory.Packages.props](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/Directory.Packages.props) |
| PackageVersion | Microsoft.Azure.Cosmos | [Directory.Packages.props](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/Directory.Packages.props) |
| PackageVersion | Microsoft.Data.SqlClient | [Directory.Packages.props](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/Directory.Packages.props) |
| PackageVersion | Microsoft.SqlServer.Types | [Directory.Packages.props](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/Directory.Packages.props) |
| PackageVersion | Castle.Core | [Directory.Packages.props](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/Directory.Packages.props) |
| PackageVersion | Humanizer.Core | [Directory.Packages.props](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/Directory.Packages.props) |
| PackageVersion | Mono.TextTemplating | [Directory.Packages.props](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/Directory.Packages.props) |
| PackageVersion | NetTopologySuite | [Directory.Packages.props](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/Directory.Packages.props) |
| PackageVersion | NetTopologySuite.IO.SpatiaLite | [Directory.Packages.props](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/Directory.Packages.props) |
| PackageVersion | NetTopologySuite.IO.SqlServerBytes | [Directory.Packages.props](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/Directory.Packages.props) |
| PackageVersion | Newtonsoft.Json | [Directory.Packages.props](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/Directory.Packages.props) |
| PackageVersion | mod_spatialite | [Directory.Packages.props](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/Directory.Packages.props) |
| PackageVersion | SQLitePCLRaw.core | [Directory.Packages.props](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/Directory.Packages.props) |
| PackageVersion | SQLitePCLRaw.bundle_e_sqlite3 | [Directory.Packages.props](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/Directory.Packages.props) |
| PackageVersion | SQLite3MC.PCLRaw.bundle | [Directory.Packages.props](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/Directory.Packages.props) |
| PackageReference | System.CommandLine | [eng/Tools/ApiChief/ApiChief.csproj](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/eng/Tools/ApiChief/ApiChief.csproj) |
| PackageReference | ICSharpCode.Decompiler | [eng/Tools/ApiChief/ApiChief.csproj](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/eng/Tools/ApiChief/ApiChief.csproj) |
| PackageReference | Microsoft.ManifestTool.CrossPlatform | [eng/common/internal/Tools.csproj](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/eng/common/internal/Tools.csproj) |
| PackageReference | Microsoft.VisualStudioEng.MicroBuild.Core | [eng/common/internal/Tools.csproj](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/eng/common/internal/Tools.csproj) |
| PackageReference | Microsoft.VisualStudioEng.MicroBuild.Plugins.SwixBuild | [eng/common/internal/Tools.csproj](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/eng/common/internal/Tools.csproj) |
| PackageReference | Microsoft.DotNet.IBCMerge | [eng/common/internal/Tools.csproj](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/eng/common/internal/Tools.csproj) |
| PackageReference | Drop.App | [eng/common/internal/Tools.csproj](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/eng/common/internal/Tools.csproj) |
| ProjectReference | ..\..\src\EFCore.Analyzers\EFCore.Analyzers.csproj | [test/EFCore.Analyzers.Tests/EFCore.Analyzers.Tests.csproj](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Analyzers.Tests/EFCore.Analyzers.Tests.csproj) |
| ProjectReference | ..\..\src\EFCore.Relational\EFCore.Relational.csproj | [test/EFCore.Analyzers.Tests/EFCore.Analyzers.Tests.csproj](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Analyzers.Tests/EFCore.Analyzers.Tests.csproj) |
| ProjectReference | ..\EFCore.Tests\EFCore.Tests.csproj | [test/EFCore.Analyzers.Tests/EFCore.Analyzers.Tests.csproj](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Analyzers.Tests/EFCore.Analyzers.Tests.csproj) |
| PackageReference | Microsoft.Extensions.DependencyModel | [test/EFCore.Analyzers.Tests/EFCore.Analyzers.Tests.csproj](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Analyzers.Tests/EFCore.Analyzers.Tests.csproj) |
| PackageReference | Microsoft.CodeAnalysis.CSharp.Analyzer.Testing | [test/EFCore.Analyzers.Tests/EFCore.Analyzers.Tests.csproj](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Analyzers.Tests/EFCore.Analyzers.Tests.csproj) |
| PackageReference | Microsoft.CodeAnalysis.CSharp.CodeFix.Testing | [test/EFCore.Analyzers.Tests/EFCore.Analyzers.Tests.csproj](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Analyzers.Tests/EFCore.Analyzers.Tests.csproj) |
| PackageReference | Microsoft.CodeAnalysis.Analyzer.Testing | [test/EFCore.Analyzers.Tests/EFCore.Analyzers.Tests.csproj](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Analyzers.Tests/EFCore.Analyzers.Tests.csproj) |
| PackageReference | Microsoft.CodeAnalysis.CSharp | [test/EFCore.Analyzers.Tests/EFCore.Analyzers.Tests.csproj](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Analyzers.Tests/EFCore.Analyzers.Tests.csproj) |
| PackageReference | Microsoft.CodeAnalysis.CSharp.Workspaces | [test/EFCore.Analyzers.Tests/EFCore.Analyzers.Tests.csproj](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Analyzers.Tests/EFCore.Analyzers.Tests.csproj) |
| PackageReference | Microsoft.CodeAnalysis.Workspaces.MSBuild | [test/EFCore.Analyzers.Tests/EFCore.Analyzers.Tests.csproj](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/test/EFCore.Analyzers.Tests/EFCore.Analyzers.Tests.csproj) |
| PackageReference | Microsoft.CodeAnalysis.CSharp.Workspaces | [src/EFCore.Analyzers/EFCore.Analyzers.csproj](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/src/EFCore.Analyzers/EFCore.Analyzers.csproj) |
| PackageReference | Microsoft.Extensions.Caching.Memory | [src/EFCore/EFCore.csproj](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/src/EFCore/EFCore.csproj) |
| PackageReference | Microsoft.Extensions.Logging | [src/EFCore/EFCore.csproj](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/src/EFCore/EFCore.csproj) |
| ProjectReference | ..\EFCore.Abstractions\EFCore.Abstractions.csproj | [src/EFCore/EFCore.csproj](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/src/EFCore/EFCore.csproj) |
| ProjectReference | ..\EFCore.Analyzers\EFCore.Analyzers.csproj | [src/EFCore/EFCore.csproj](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/src/EFCore/EFCore.csproj) |


## License evidence and eligibility gate

Observed metadata hint: `MIT`.

Observed root metadata/license text is evidence, not a completed eligibility review. Resolve conditional/transitive dependencies, embedded assets, generated inputs and redistributable binaries before source reuse or release.

| Retrieved notice/license | Immutable source |
|---|---|
| [LICENSE.txt](evidence/notices/LICENSE.txt) | [LICENSE.txt](https://github.com/dotnet/efcore/blob/2e8882748cc45b317a98a6f27f0680948221ae3b/LICENSE.txt) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-entity-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
