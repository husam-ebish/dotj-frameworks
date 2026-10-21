# DJ-001 .j Core: dependencies and licenses

## Proposed Java dependencies

No product dependency in the base foundation

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: java.base, java.nio, java.time, java.util.concurrent, JCA; no replacement JVM or custom crypto.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|
| PackageReference | Microsoft.CodeAnalysis.CSharp | [eng/analyzers/PlatformDocAnalyzer/PlatformDocAnalyzer.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/eng/analyzers/PlatformDocAnalyzer/PlatformDocAnalyzer.csproj) |
| PackageReference | Microsoft.ManifestTool.CrossPlatform | [eng/common/internal/Tools.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/eng/common/internal/Tools.csproj) |
| PackageReference | Microsoft.VisualStudioEng.MicroBuild.Core | [eng/common/internal/Tools.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/eng/common/internal/Tools.csproj) |
| PackageReference | Microsoft.VisualStudioEng.MicroBuild.Plugins.SwixBuild | [eng/common/internal/Tools.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/eng/common/internal/Tools.csproj) |
| PackageReference | Microsoft.DotNet.IBCMerge | [eng/common/internal/Tools.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/eng/common/internal/Tools.csproj) |
| PackageReference | Drop.App | [eng/common/internal/Tools.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/eng/common/internal/Tools.csproj) |
| PackageReference | Microsoft.CodeAnalysis.CSharp.Workspaces | [eng/analyzers/PlatformDocAnalyzer.Tests/PlatformDocAnalyzer.Tests.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/eng/analyzers/PlatformDocAnalyzer.Tests/PlatformDocAnalyzer.Tests.csproj) |
| PackageReference | Microsoft.CodeAnalysis.CSharp.Analyzer.Testing | [eng/analyzers/PlatformDocAnalyzer.Tests/PlatformDocAnalyzer.Tests.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/eng/analyzers/PlatformDocAnalyzer.Tests/PlatformDocAnalyzer.Tests.csproj) |
| ProjectReference | ..\PlatformDocAnalyzer\PlatformDocAnalyzer.csproj | [eng/analyzers/PlatformDocAnalyzer.Tests/PlatformDocAnalyzer.Tests.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/eng/analyzers/PlatformDocAnalyzer.Tests/PlatformDocAnalyzer.Tests.csproj) |
| ProjectReference | $(LibrariesProjectRoot)\System.Private.CoreLib\gen\System.Private.CoreLib.Generators.csproj | [src/coreclr/System.Private.CoreLib/System.Private.CoreLib.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/coreclr/System.Private.CoreLib/System.Private.CoreLib.csproj) |
| ProjectReference | $(LibrariesProjectRoot)Microsoft.Extensions.DependencyInjection.Abstractions\src\Microsoft.Extensions.DependencyInjection.Abstractions.csproj | [src/libraries/Microsoft.Extensions.DependencyInjection/src/Microsoft.Extensions.DependencyInjection.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.DependencyInjection/src/Microsoft.Extensions.DependencyInjection.csproj) |
| PackageReference | System.Threading.Tasks.Extensions | [src/libraries/Microsoft.Extensions.DependencyInjection/src/Microsoft.Extensions.DependencyInjection.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.DependencyInjection/src/Microsoft.Extensions.DependencyInjection.csproj) |
| ProjectReference | $(LibrariesProjectRoot)Microsoft.Bcl.AsyncInterfaces\src\Microsoft.Bcl.AsyncInterfaces.csproj | [src/libraries/Microsoft.Extensions.DependencyInjection/src/Microsoft.Extensions.DependencyInjection.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.DependencyInjection/src/Microsoft.Extensions.DependencyInjection.csproj) |


## License evidence and eligibility gate

The project owner selected **MIT** for dotj-core source and binary distribution. The product [LICENSE](../../../../dotj-core/LICENSE) uses the [SPDX MIT text](https://spdx.org/licenses/MIT), credits dotj Frameworks contributors, and is embedded in the candidate JAR as `META-INF/LICENSE`.

The built foundation candidate has a separate [technical rights-input inventory](evidence/foundation-rights-inputs-v1.json): 30 hashed product Java sources compile into the candidate JAR, `java.base` is the observed JDK module dependency, and the product MIT license is packaged in source and binary form. The upstream license and third-party notice copies remain reference evidence outside the JAR. File-level upstream notice applicability, transitive rights and release approval still require review; this inventory does not grant release clearance.

[Local source introduction evidence](evidence/foundation-source-provenance-v1.json) records the first Git add event for each of the 30 Java files and verifies the current source hashes. None of their first 30 lines contains an SPDX identifier, copyright notice, or .NET Foundation name. These observations do not establish originality or resolve whether upstream notices apply to their contents.

A [bounded upstream text comparison](evidence/foundation-upstream-text-comparison-v1.json) screened all 30 product Java paths against direct name-matched paths at the pinned upstream commit. It found 29 direct upstream files (the internal `ThrowSite` has no file at the constructed path) and zero common contiguous 12-identifier runs in those pairs. This screen misses transformed code and other upstream paths and cannot determine notice applicability.

Observed root metadata/license text is evidence, not a completed eligibility review. Resolve conditional/transitive dependencies, embedded assets, generated inputs and redistributable binaries before source reuse or release.

| Retrieved notice/license | Immutable source |
|---|---|
| [LICENSE.TXT](evidence/notices/LICENSE.TXT) | [LICENSE.TXT](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/LICENSE.TXT) |
| [THIRD-PARTY-NOTICES.TXT](evidence/notices/THIRD-PARTY-NOTICES.TXT) | [THIRD-PARTY-NOTICES.TXT](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/THIRD-PARTY-NOTICES.TXT) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-core-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
