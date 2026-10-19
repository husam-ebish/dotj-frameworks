# DJ-006 .j Extensions: dependencies and licenses

## Proposed Java dependencies

core

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: ServiceLoader, properties/environment/file APIs, executors and management APIs.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|
| PackageReference | System.CommandLine | [eng/Tools/ApiChief/ApiChief.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/eng/Tools/ApiChief/ApiChief.csproj) |
| PackageReference | System.CommandLine.NamingConventionBinder | [eng/Tools/ApiChief/ApiChief.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/eng/Tools/ApiChief/ApiChief.csproj) |
| PackageReference | ICSharpCode.Decompiler | [eng/Tools/ApiChief/ApiChief.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/eng/Tools/ApiChief/ApiChief.csproj) |
| PackageReference | Microsoft.Extensions.Logging.Abstractions | [eng/Tools/DiagConfig/DiagConfig.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/eng/Tools/DiagConfig/DiagConfig.csproj) |
| PackageReference | System.CommandLine | [eng/Tools/DiagConfig/DiagConfig.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/eng/Tools/DiagConfig/DiagConfig.csproj) |
| PackageReference | System.CommandLine.NamingConventionBinder | [eng/Tools/DiagConfig/DiagConfig.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/eng/Tools/DiagConfig/DiagConfig.csproj) |
| PackageReference | Microsoft.CodeAnalysis.Common | [eng/Tools/DiagConfig/DiagConfig.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/eng/Tools/DiagConfig/DiagConfig.csproj) |
| PackageReference | Microsoft.CodeAnalysis.CSharp.Workspaces | [eng/Tools/DiagConfig/DiagConfig.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/eng/Tools/DiagConfig/DiagConfig.csproj) |
| PackageReference | Microsoft.CodeAnalysis.CSharp | [eng/Tools/DiagConfig/DiagConfig.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/eng/Tools/DiagConfig/DiagConfig.csproj) |
| PackageReference | YamlDotNet | [eng/Tools/DiagConfig/DiagConfig.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/eng/Tools/DiagConfig/DiagConfig.csproj) |
| ProjectReference | ..\..\..\src\Libraries\Microsoft.AspNetCore.Diagnostics.Middleware\Microsoft.AspNetCore.Diagnostics.Middleware.csproj | [bench/Libraries/Microsoft.AspNetCore.Diagnostics.Middleware.PerformanceTests/Microsoft.AspNetCore.Diagnostics.Middleware.PerformanceTests.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/bench/Libraries/Microsoft.AspNetCore.Diagnostics.Middleware.PerformanceTests/Microsoft.AspNetCore.Diagnostics.Middleware.PerformanceTests.csproj) |
| ProjectReference | ..\..\..\src\Libraries\Microsoft.Extensions.Compliance.Testing\Microsoft.Extensions.Compliance.Testing.csproj | [bench/Libraries/Microsoft.AspNetCore.Diagnostics.Middleware.PerformanceTests/Microsoft.AspNetCore.Diagnostics.Middleware.PerformanceTests.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/bench/Libraries/Microsoft.AspNetCore.Diagnostics.Middleware.PerformanceTests/Microsoft.AspNetCore.Diagnostics.Middleware.PerformanceTests.csproj) |
| PackageReference | Microsoft.CodeAnalysis.CSharp.Workspaces | [src/Analyzers/Microsoft.Analyzers.Extra/Microsoft.Analyzers.Extra.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/Analyzers/Microsoft.Analyzers.Extra/Microsoft.Analyzers.Extra.csproj) |
| PackageReference | Microsoft.CodeAnalysis.Analyzers | [src/Analyzers/Microsoft.Analyzers.Extra/Microsoft.Analyzers.Extra.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/Analyzers/Microsoft.Analyzers.Extra/Microsoft.Analyzers.Extra.csproj) |
| PackageReference | Microsoft.CodeAnalysis.CSharp.Workspaces | [src/Analyzers/Microsoft.Analyzers.Local/Microsoft.Analyzers.Local.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/Analyzers/Microsoft.Analyzers.Local/Microsoft.Analyzers.Local.csproj) |
| PackageReference | Microsoft.CodeAnalysis.Analyzers | [src/Analyzers/Microsoft.Analyzers.Local/Microsoft.Analyzers.Local.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/Analyzers/Microsoft.Analyzers.Local/Microsoft.Analyzers.Local.csproj) |
| ProjectReference | ..\Microsoft.Extensions.Resilience\Microsoft.Extensions.Resilience.csproj | [src/Libraries/Microsoft.Extensions.Http.Resilience/Microsoft.Extensions.Http.Resilience.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/Libraries/Microsoft.Extensions.Http.Resilience/Microsoft.Extensions.Http.Resilience.csproj) |
| ProjectReference | ..\Microsoft.Extensions.Http.Diagnostics\Microsoft.Extensions.Http.Diagnostics.csproj | [src/Libraries/Microsoft.Extensions.Http.Resilience/Microsoft.Extensions.Http.Resilience.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/Libraries/Microsoft.Extensions.Http.Resilience/Microsoft.Extensions.Http.Resilience.csproj) |


## License evidence and eligibility gate

Observed metadata hint: `MIT`.

Observed root metadata/license text is evidence, not a completed eligibility review. Resolve conditional/transitive dependencies, embedded assets, generated inputs and redistributable binaries before source reuse or release.

| Retrieved notice/license | Immutable source |
|---|---|
| [LICENSE](evidence/notices/LICENSE) | [LICENSE](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/LICENSE) |
| [THIRD-PARTY-NOTICES.TXT](evidence/notices/THIRD-PARTY-NOTICES.TXT) | [THIRD-PARTY-NOTICES.TXT](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/THIRD-PARTY-NOTICES.TXT) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-extensions-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
